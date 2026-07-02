"""cd ~/Desktop/QV_fresh
python3 - << 'EOF'
# What this does:
# Completely rewrites the mob system in quantum_sandbox.py to match
# People Playground character style:
# - Two-segment limbs (upper arm + forearm, thigh + shin)
# - Visible elbow and knee joints as small circles
# - Verlet physics on EACH segment independently (not just one body)
# - Grab individual limbs and body follows
# - Limp collapse when knocked hard (joint stiffness drops to near-zero)
# - Different mob types have different proportions

with open('app/modules/quantum_sandbox.py', 'r') as f:
    content = f.read()

# ── Find and replace the entire mob system ────────────────────────────────────
old_mob_system_start = content.find('// ── SIMPLE MOB PHYSICS')
old_mob_system_end = content.find('\n// ── REGULAR OBJECTS')

if old_mob_system_start == -1 or old_mob_system_end == -1:
    print('Markers not found!')
    # Show what we have
    idx = content.find('function createMob')
    print(repr(content[idx:idx+100]))
else:
    new_system = r"""// ══════════════════════════════════════════════════════════════════════════════
// PEOPLE PLAYGROUND STYLE MOB SYSTEM
// Each mob is a skeleton of Verlet points connected by distance constraints.
// Two-segment limbs: upper arm + forearm, thigh + shin.
// Joints are visible circles. Grab any point and drag — body follows.
// Knockback sets all joint velocities. Collapse flag loosens all constraints.
// ══════════════════════════════════════════════════════════════════════════════

const GRAVITY_MOB = 0.45;
const AIR_DAMP = 0.993;     // very light air resistance
const GND_BOUNCE = 0.28;
const GND_FRIC   = 0.82;
const WALL_BOUNCE = 0.35;
const CONSTRAINT_ITERS = 6; // iterations per frame (higher = stiffer joints)

// ── Verlet point ──────────────────────────────────────────────────────────────
function mkPt(x, y) {
    return { x, y, ox: x, oy: y, pinned: false };
}

// ── Integrate one point ───────────────────────────────────────────────────────
function integratePt(p, grav) {
    if (p.pinned) return;
    const vx = (p.x - p.ox) * AIR_DAMP;
    const vy = (p.y - p.oy) * AIR_DAMP;
    p.ox = p.x; p.oy = p.y;
    p.x += vx;
    p.y += vy + grav;
}

// ── Collide one point with world ──────────────────────────────────────────────
function collidePt(p, r, groundY) {
    if (p.y + r > groundY) {
        const vx = p.x - p.ox;
        p.y = groundY - r;
        p.oy = p.y + (p.y - p.oy) * GND_BOUNCE * -1;
        p.ox = p.x - vx * GND_FRIC;
    }
    if (p.x - r < 0)  { p.x = r;   p.ox = p.x + (p.x - p.ox) * WALL_BOUNCE; }
    if (p.x + r > W)  { p.x = W-r; p.ox = p.x + (p.x - p.ox) * WALL_BOUNCE; }
    if (p.y - r < 0)  { p.y = r;   p.oy = p.y + (p.y - p.oy) * WALL_BOUNCE; }
}

// ── Distance constraint (keep two points a fixed length apart) ────────────────
function constrain(a, b, len, stiff) {
    const dx = b.x - a.x, dy = b.y - a.y;
    const d = Math.sqrt(dx*dx + dy*dy) || 0.0001;
    const diff = (d - len) / d * 0.5 * stiff;
    const offX = dx * diff, offY = dy * diff;
    if (!a.pinned) { a.x += offX; a.y += offY; }
    if (!b.pinned) { b.x -= offX; b.y -= offY; }
}

// ── Build a mob skeleton ──────────────────────────────────────────────────────
// Skeleton layout (all offsets from spawn centre):
//
//          [HEAD]
//            |
//          [NECK]
//         /      \
//     [LSHO]    [RSHO]   <- shoulders
//       |            |
//     [LELB]    [RELB]   <- elbows
//       |            |
//     [LHAN]    [RHAN]   <- hands
//
//          [HIP]
//         /      \
//     [LKNE]    [RKNE]   <- knees
//       |            |
//     [LFOT]    [RFOT]   <- feet
//
// Extra "cheat" sticks keep head above hips so standing is stable:
// NECK<->HIP   LSHO<->RSHO (shoulder brace)   LKNE<->RKNE (hip brace)

function createMob(cx_spawn, cy_spawn, template) {
    const s = (template.scale || 1) * (0.9 + Math.random() * 0.2); // slight height variance
    const c = template.color;

    // Joint positions (y increases downward)
    const head  = mkPt(cx_spawn,        cy_spawn - 36*s);
    const neck  = mkPt(cx_spawn,        cy_spawn - 24*s);
    const lsho  = mkPt(cx_spawn - 10*s, cy_spawn - 20*s);
    const rsho  = mkPt(cx_spawn + 10*s, cy_spawn - 20*s);
    const lelb  = mkPt(cx_spawn - 18*s, cy_spawn - 8*s);
    const relb  = mkPt(cx_spawn + 18*s, cy_spawn - 8*s);
    const lhan  = mkPt(cx_spawn - 18*s, cy_spawn + 4*s);
    const rhan  = mkPt(cx_spawn + 18*s, cy_spawn + 4*s);
    const hip   = mkPt(cx_spawn,        cy_spawn);
    const lkne  = mkPt(cx_spawn - 6*s,  cy_spawn + 14*s);
    const rkne  = mkPt(cx_spawn + 6*s,  cy_spawn + 14*s);
    const lfot  = mkPt(cx_spawn - 6*s,  cy_spawn + 28*s);
    const rfot  = mkPt(cx_spawn + 6*s,  cy_spawn + 28*s);

    const pts = { head, neck, lsho, rsho, lelb, relb, lhan, rhan,
                  hip, lkne, rkne, lfot, rfot };

    // Sticks: {a, b, len, stiff}
    const dist = (a,b) => Math.hypot(a.x-b.x, a.y-b.y);
    const sticks = [
        // Spine
        {a:'head', b:'neck', len:dist(head,neck), stiff:0.9},
        {a:'neck', b:'hip',  len:dist(neck,hip),  stiff:0.85},
        // Shoulders
        {a:'neck', b:'lsho', len:dist(neck,lsho), stiff:0.85},
        {a:'neck', b:'rsho', len:dist(neck,rsho), stiff:0.85},
        {a:'lsho', b:'rsho', len:dist(lsho,rsho), stiff:0.7},  // shoulder brace
        // Arms
        {a:'lsho', b:'lelb', len:dist(lsho,lelb), stiff:0.88},
        {a:'rsho', b:'relb', len:dist(rsho,relb), stiff:0.88},
        {a:'lelb', b:'lhan', len:dist(lelb,lhan), stiff:0.88},
        {a:'relb', b:'rhan', len:dist(relb,rhan), stiff:0.88},
        // Hips and legs
        {a:'hip',  b:'lkne', len:dist(hip, lkne), stiff:0.88},
        {a:'hip',  b:'rkne', len:dist(hip, rkne), stiff:0.88},
        {a:'lkne', b:'rkne', len:dist(lkne,rkne), stiff:0.6},  // hip brace
        {a:'lkne', b:'lfot', len:dist(lkne,lfot), stiff:0.88},
        {a:'rkne', b:'rfot', len:dist(rkne,rfot), stiff:0.88},
        // Cross braces to stop full collapse
        {a:'neck', b:'lkne', len:dist(neck,lkne), stiff:0.3},
        {a:'neck', b:'rkne', len:dist(neck,rkne), stiff:0.3},
    ];

    return {
        type: 'mob',
        pts, sticks, s, c,
        face: template.face,
        color: template.color,
        hp: template.hp, maxHp: template.hp,
        frozen: false, shielded: false,
        id: Math.random(),
        collapsed: false,
        // convenience centre for HUD / collision queries
        get x() { return (this.pts.neck.x + this.pts.hip.x) * 0.5; },
        get y() { return (this.pts.neck.y + this.pts.hip.y) * 0.5; },
    };
}

// ── Update one mob ────────────────────────────────────────────────────────────
function updateMobNew(mob, groundY) {
    if (mob.frozen) return;
    const grav = gravityOn ? GRAVITY_MOB : 0;
    const ptArr = Object.values(mob.pts);

    // 1. Integrate (apply gravity + inertia to every point)
    ptArr.forEach(p => integratePt(p, grav));

    // 2. Satisfy constraints + collide (several passes)
    const stiffScale = mob.collapsed ? 0.15 : 1.0;
    for (let iter = 0; iter < CONSTRAINT_ITERS; iter++) {
        mob.sticks.forEach(s => {
            constrain(mob.pts[s.a], mob.pts[s.b], s.len, s.stiff * stiffScale);
        });
        ptArr.forEach(p => collidePt(p, 3, groundY));
    }
}

// ── Apply impulse (knockback) ─────────────────────────────────────────────────
function knockMob(mob, srcX, srcY, force) {
    Object.values(mob.pts).forEach(p => {
        const dx = p.x - srcX, dy = p.y - srcY;
        const d = Math.sqrt(dx*dx + dy*dy) || 1;
        const f = force * Math.max(0, 1 - d / 240);
        // Move oldX/oldY backward to create Verlet velocity impulse
        p.ox -= (dx/d) * f * (0.4 + Math.random()*0.35);
        p.oy -= (dy/d) * f * (0.4 + Math.random()*0.35) + f * 0.12;
    });
    if (force > 7) { mob.collapsed = true; setTimeout(() => mob.collapsed = false, 1200); }
}

// ── Find mob/point at screen position ────────────────────────────────────────
function getMobAt(x, y) {
    return mobs.find(m => {
        return Object.values(m.pts).some(p => Math.hypot(p.x-x, p.y-y) < 10);
    });
}
function getMobPtKeyAt(mob, x, y) {
    return Object.entries(mob.pts)
        .find(([k,p]) => Math.hypot(p.x-x, p.y-y) < 14)?.[0] || null;
}

"""
    content = content[:old_mob_system_start] + new_system + content[old_mob_system_end:]
    with open('app/modules/quantum_sandbox.py', 'w') as f:
        f.write(content)
    print('Mob system replaced with People Playground skeleton style!')
EOF
modules/teacher_dashboard.py
─────────────────────────────
Full teacher dashboard — class insights, progress charts,
student table, and CSV export. Password protected.
"""

import json
import pathlib
import streamlit as st
from modules.users import get_user, update_plan, get_all_users, get_user_count
import plotly.graph_objects as go
import plotly.express as px
from utils.security import get_level, sanitize_input

SCORES_FILE = pathlib.Path(__file__).parent.parent / "static" / "scores.json"
import streamlit as _st_td
TEACHER_PASSWORD = _st_td.secrets.get("TEACHER_PASSWORD", "")


def load_scores() -> dict:
    try:
        if SCORES_FILE.exists():
            return json.loads(SCORES_FILE.read_text())
    except Exception as _e:
        logging.warning("Dashboard read error: %s", _e)  # nosec B110
    return {}


def render_teacher_dashboard():
    st.title("👨‍🏫 Teacher Dashboard")

    # ── Password gate ─────────────────────────────────────────────────────
    if "teacher_auth" not in st.session_state:
        st.session_state.teacher_auth = False

    if not st.session_state.teacher_auth:
        st.markdown(
            "This dashboard is for teachers only. "
            "Enter your teacher password to access class insights."
        )
        col1, col2 = st.columns([3, 1])
        with col1:
            pwd = st.text_input(
                "Teacher password:",
                type="password",
                placeholder="Enter password",
                key="teacher_pwd"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔓 Login", key="teacher_login"):
                import time as _time
                _now = _time.time()
                _attempts = st.session_state.get("teacher_attempts", 0)
                _window = st.session_state.get("teacher_window", _now)
                if _now - _window > 300:
                    st.session_state.teacher_attempts = 0
                    st.session_state.teacher_window = _now
                st.session_state.teacher_attempts = _attempts + 1
                if _attempts >= 5:
                    remaining = int(300 - (_now - _window))
                    st.error(f"Too many attempts. Try again in {remaining} seconds.")
                    st.stop()
                if pwd == TEACHER_PASSWORD:
                    st.session_state.teacher_auth = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Contact your school administrator.")
        st.info(
            "💡 Contact hello@quantumvaultacademy.com for teacher access credentials."
        )
        return

    # ── Logout button ─────────────────────────────────────────────────────
    if st.button("🔒 Logout", key="teacher_logout"):
        st.session_state.teacher_auth = False
        st.rerun()

    scores = load_scores()

    if not scores:
        st.info(
            "📊 No student data yet! Students need to save their scores "
            "on the Leaderboard page first."
        )
        st.markdown(
            "**How to get data:**\n"
            "1. Have students complete modules and earn XP\n"
            "2. Direct them to the 🏆 Leaderboard page\n"
            "3. Ask them to enter a codename and save their score\n"
            "4. Refresh this dashboard to see their progress"
        )
        return

    # ── Build data ────────────────────────────────────────────────────────
    students = []
    for nickname, data in scores.items():
        xp = data.get("xp", 0)
        level = get_level(xp)
        students.append({
            "Nickname": nickname,
            "XP": xp,
            "Level": level,
            "Grade Tier": _get_grade_tier(xp),
        })

    students.sort(key=lambda x: x["XP"], reverse=True)
    total = len(students)
    avg_xp = sum(s["XP"] for s in students) // total if total else 0
    top_xp = max(s["XP"] for s in students) if students else 0
    total_xp = sum(s["XP"] for s in students)

    # ── Metric cards ──────────────────────────────────────────────────────
    st.markdown("### 📊 Class Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total Students", total)
    with col2:
        st.metric("⭐ Average XP", avg_xp)
    with col3:
        st.metric("🏆 Top Score", top_xp)
    with col4:
        st.metric("⚡ Total XP Earned", total_xp)

    st.markdown("---")

    # ── Charts row ────────────────────────────────────────────────────────
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("#### 🎯 XP Distribution")
        xp_values = [s["XP"] for s in students]
        fig_hist = go.Figure(go.Histogram(
            x=xp_values,
            nbinsx=10,
            marker_color="#7c6dfa",
            opacity=0.85,
        ))
        fig_hist.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="XP", color="#888"),
            yaxis=dict(title="Students", color="#888"),
            font=dict(color="#ccc"),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with chart_col2:
        st.markdown("#### 🏅 Level Distribution")
        level_counts = {}
        for s in students:
            level_counts[s["Level"]] = level_counts.get(s["Level"], 0) + 1

        level_order = [
            "🔰 Recruit", "🕵️ Cadet", "🔐 Agent",
            "⚡ Specialist", "🛡️ Cipher Corps", "🌐 Quantum Guardian"
        ]
        labels = [l for l in level_order if l in level_counts]
        values = [level_counts[l] for l in labels]
        colors = ["#6b7280", "#3b82f6", "#10b981",
                  "#f59e0b", "#8b5cf6", "#14d4a8"]

        fig_pie = go.Figure(go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors[:len(labels)]),
            hole=0.4,
            textinfo="label+value",
            textfont=dict(size=11),
        ))
        fig_pie.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            font=dict(color="#ccc"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Progress bar chart ────────────────────────────────────────────────
    st.markdown("#### 📈 Top 10 Students by XP")
    top10 = students[:10]
    fig_bar = go.Figure(go.Bar(
        x=[s["Nickname"] for s in top10],
        y=[s["XP"] for s in top10],
        marker=dict(
            color=[s["XP"] for s in top10],
            colorscale=[[0, "#4f46e5"], [0.5, "#7c6dfa"], [1, "#14d4a8"]],
        ),
        text=[s["XP"] for s in top10],
        textposition="outside",
    ))
    fig_bar.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="#888"),
        yaxis=dict(title="XP", color="#888"),
        font=dict(color="#ccc"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # ── Grade tier breakdown ──────────────────────────────────────────────
    st.markdown("### 🎓 Grade Tier Engagement")
    tier_counts = {}
    for s in students:
        tier = s["Grade Tier"]
        tier_counts[tier] = tier_counts.get(tier, 0) + 1

    tier_col1, tier_col2, tier_col3 = st.columns(3)
    tiers = [
        ("🟢 Elementary (K-5)", tier_counts.get("Elementary", 0), "#14d4a8"),
        ("🟡 Middle School (6-8)", tier_counts.get("Middle School", 0), "#7c6dfa"),
        ("🔴 High School (9-12)", tier_counts.get("High School", 0), "#f45c5c"),
    ]
    for col, (label, count, color) in zip(
        [tier_col1, tier_col2, tier_col3], tiers
    ):
        pct = round(count / total * 100) if total else 0
        with col:
            st.markdown(
                f"""
                <div style="
                    background: {color}15;
                    border: 1px solid {color}40;
                    border-left: 4px solid {color};
                    border-radius: 10px;
                    padding: 1rem;
                    text-align: center;
                ">
                    <div style="font-size:1.6rem;font-weight:700;color:{color}">{count}</div>
                    <div style="font-size:0.8rem;color:#888">{label}</div>
                    <div style="font-size:0.75rem;color:#555">{pct}% of class</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # ── Class insights ────────────────────────────────────────────────────
    st.markdown("### 💡 Class Insights")

    struggling = [s for s in students if s["XP"] < 50]
    progressing = [s for s in students if 50 <= s["XP"] < 300]
    advanced = [s for s in students if s["XP"] >= 300]

    ins_col1, ins_col2, ins_col3 = st.columns(3)
    with ins_col1:
        st.error(
            f"**⚠️ Needs Attention ({len(struggling)} students)**\n\n"
            "Students with under 50 XP — may need extra encouragement "
            "or a different grade level module."
        )
    with ins_col2:
        st.warning(
            f"**📈 On Track ({len(progressing)} students)**\n\n"
            "Students making steady progress. "
            "Encourage them to try higher grade modules."
        )
    with ins_col3:
        st.success(
            f"**🚀 Advanced ({len(advanced)} students)**\n\n"
            "High performers! Ready for the High School module "
            "and real Python LWE code challenges."
        )

    # ── Teaching tips ─────────────────────────────────────────────────────
    with st.expander("📋 Teaching Tips Based on Class Data"):
        if len(struggling) > total * 0.4:
            st.markdown(
                "**40%+ of your class is under 50 XP.** Consider:\n"
                "- Starting with the Elementary module regardless of grade\n"
                "- Running a class demo of the Falling Blocks game together\n"
                "- Pairing struggling students with advanced ones"
            )
        if len(advanced) > 0:
            st.markdown(
                f"**{len(advanced)} advanced students** are ready for:\n"
                "- High School LWE Python code lab\n"
                "- Real NIST FIPS 203/204/205 documentation\n"
                "- NSA GenCyber camp applications"
            )
        st.markdown(
            "**General tips:**\n"
            "- Run Zombie Blast as a class warmup — 5 minutes before lessons\n"
            "- Use the RSA vs Kyber Race as a lecture opener\n"
            "- Award badges publicly to motivate lower XP students"
        )

    st.markdown("---")

    # ── Full student table ────────────────────────────────────────────────
    st.markdown("### 📋 Full Student Roster")

    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * (len(students) - 3)
    for i, student in enumerate(students):
        col1, col2, col3, col4, col5 = st.columns([0.5, 2.5, 1.5, 2, 1.5])
        with col1:
            st.markdown(f"**{medals[min(i, len(medals)-1)]}**")
        with col2:
            st.markdown(f"**{sanitize_input(str(student['Nickname']), max_length=50)}**")
        with col3:
            st.markdown(f"⭐ {student['XP']} XP")
        with col4:
            st.markdown(f"{student['Level']}")
        with col5:
            xp = student["XP"]
            next_xp = _get_next_xp(xp)
            pct = min(int((xp / next_xp) * 100), 100) if next_xp else 100
            st.progress(pct / 100)

    st.markdown("---")

    # ── CSV Export ────────────────────────────────────────────────────────
    st.markdown("### 📥 Export Class Data")

    csv_lines = ["Rank,Nickname,XP,Level,Grade Tier"]
    for i, s in enumerate(students):
        csv_lines.append(
            f"{i+1},{s['Nickname']},{s['XP']},{s['Level']},{s['Grade Tier']}"
        )
    csv_data = "\n".join(csv_lines)

    st.download_button(
        label="⬇️ Download Class Report (CSV)",
        data=csv_data,
        file_name="quantumvault_class_report.csv",
        mime="text/csv",
        help="Download a CSV file you can open in Excel or Google Sheets"
    )

    st.caption(
        "🔒 This report contains only anonymous codenames. "
        "No real student names or personal data are stored."
    )


def _get_grade_tier(xp: int) -> str:
    if xp < 100:
        return "Elementary"
    elif xp < 300:
        return "Middle School"
    else:
        return "High School"


def _get_next_xp(xp: int) -> int:
    thresholds = [50, 150, 300, 500, 750]
    for t in thresholds:
        if xp < t:
            return t
    return 750

def render_teacher_feedback():
    """Teacher feedback form — sends directly to developer."""
    import requests
    st.markdown("---")
    st.subheader("📬 Send Feedback to QuantumVault")
    st.markdown(
        "Have a suggestion, found a bug, or want to share what your students loved? "
        "We read every message and use your feedback to improve the platform!"
    )

    feedback_type = st.selectbox(
        "Feedback type:",
        [
            "💡 Feature Request — I want something new",
            "🐛 Bug Report — Something is broken",
            "❤️ Positive Feedback — Something students loved",
            "📚 Curriculum Suggestion — Content improvement",
            "💰 Pricing Feedback — About the plans",
            "🔧 Technical Issue — Performance or display problem",
            "❓ Question — I need help with something",
        ],
        key="feedback_type"
    )

    col1, col2 = st.columns(2)
    with col1:
        teacher_name = st.text_input("Your name:", placeholder="Ms. Johnson", key="fb_name")
        school_name  = st.text_input("School:", placeholder="Lincoln Elementary", key="fb_school")
    with col2:
        teacher_email = st.text_input("Your email:", placeholder="teacher@school.edu", key="fb_email")
        grade_level   = st.selectbox("Grade level you teach:", [
            "K-5 Elementary", "6-8 Middle School", "9-12 High School", "Mixed grades"
        ], key="fb_grade")

    feedback_text = st.text_area(
        "Your feedback:",
        placeholder=(
            "Tell us what you think! Be as specific as possible — "
            "which activity, which grade level, what happened, what you'd like to see..."
        ),
        height=150,
        max_chars=2000,
        key="fb_text"
    )

    rating = st.select_slider(
        "Overall rating of QuantumVault Academy:",
        options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        value="⭐⭐⭐⭐⭐",
        key="fb_rating"
    )

    would_recommend = st.radio(
        "Would you recommend QuantumVault to other teachers?",
        ["Yes, definitely!", "Probably yes", "Not sure", "Probably not"],
        horizontal=True,
        key="fb_recommend"
    )

    if st.button("📬 Send Feedback!", key="fb_submit", type="primary"):
        if not feedback_text or len(feedback_text.strip()) < 10:
            st.error("Please write at least a sentence of feedback!")
        elif not teacher_email or "@" not in teacher_email:
            st.error("Please enter a valid email address!")
        else:
            msg = (
                f"TYPE: {feedback_type}\n"
                f"FROM: {teacher_name or 'Anonymous'} at {school_name or 'Unknown School'}\n"
                f"EMAIL: {teacher_email}\n"
                f"GRADE: {grade_level}\n"
                f"RATING: {rating}\n"
                f"RECOMMEND: {would_recommend}\n\n"
                f"FEEDBACK:\n{feedback_text}"
            )
            try:
                resp = requests.post(
                    "https://formspree.io/f/mredvlgp",
                    data={
                        "email": teacher_email,
                        "subject": f"QuantumVault Teacher Feedback: {feedback_type[:30]}",
                        "message": msg,
                        "_replyto": teacher_email,
                    },
                    headers={"Accept": "application/json"},
                    timeout=10
                )
                if resp.status_code == 200:
                    st.success(
                        "✅ Feedback sent! Thank you so much — "
                        "we read every message and will follow up within 48 hours."
                    )
                    st.balloons()
                else:
                    st.warning(
                        "Feedback form unavailable right now. "
                        "Please email us directly at hello@quantumvaultacademy.com"
                    )
            except Exception:
                st.info(
                    "Could not connect to feedback service. "
                    "Please email hello@quantumvaultacademy.com directly!"
                )
    render_teacher_feedback()



