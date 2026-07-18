"""
modules/progress_tracker.py
────────────────────────────
Student progress tracking — saves which modules, tabs,
and activities each student has completed.
Stored in session state and optionally to a JSON file.
"""

import json
import pathlib
import streamlit as st
from utils.security import get_level, get_level_progress, get_next_level_xp

PROGRESS_FILE = pathlib.Path(__file__).parent.parent / "static" / "progress.json"

# ── All trackable activities ──────────────────────────────────────────────────
ACTIVITIES = {
    "elementary": {
        "label": "🟢 Elementary (K-5)",
        "color": "#14d4a8",
        "items": {
            "story_read":        "📖 Read the Agent Pixel story",
            "color_mixing":      "🎨 Completed color mixing key exchange",
            "lock_puzzle":       "🔒 Solved the lock puzzle",
            "lock_speed_bonus":  "⚡ Earned speed bonus on lock puzzle",
            "vocab_cards":       "📝 Completed vocabulary flashcards",
            "falling_blocks":    "🧱 Played Falling Blocks game",
            "zombie_blast_easy": "🧟 Played Zombie Blast (Easy)",
        }
    },
    "middle_school": {
        "label": "🟡 Middle School (6-8)",
        "color": "#7c6dfa",
        "items": {
            "lattice_visualizer":  "🏗️ Used the lattice visualizer",
            "lattice_challenge":   "🎯 Solved the lattice challenge",
            "hash_factory":        "🏭 Used the hash factory",
            "hash_avalanche":      "💥 Discovered the avalanche effect",
            "quantum_race":        "⚡ Completed the quantum vs classical race",
            "kyber_workshop":      "🔑 Completed the Kyber key workshop",
            "lattice_maze":        "🌀 Played the lattice maze",
            "zombie_blast_medium": "🧟 Played Zombie Blast (Medium)",
        }
    },
    "high_school": {
        "label": "🔴 High School (9-12)",
        "color": "#f45c5c",
        "items": {
            "nist_timeline":       "📅 Studied the NIST timeline",
            "algorithm_lab":       "⚖️ Used the algorithm comparison lab",
            "quantum_race_hs":     "⚡ Ran RSA vs Kyber attack race",
            "lwe_code_lab":        "💻 Completed the LWE code lab",
            "threat_modeler":      "🛡️ Used the threat modeler",
            "tower_defense":       "🛡️ Played PQC Tower Defense",
            "zombie_blast_hard":   "🧟 Played Zombie Blast (Hard)",
        }
    }
}


def load_progress() -> dict:
    """Load all student progress from file."""
    try:
        if PROGRESS_FILE.exists():
            return json.loads(PROGRESS_FILE.read_text())
    except Exception as _e:
        logging.warning("Progress read error: %s", _e)  # nosec B110
    return {}


def save_progress(data: dict):
    """Save all student progress to file."""
    try:
        PROGRESS_FILE.write_text(json.dumps(data, indent=2))
    except Exception as _e:
        import logging; logging.warning("Progress write error: %s", _e)  # nosec B110


def mark_complete(activity_key: str):
    """
    Mark an activity as complete for the current session.
    Call this from any module when a student completes an activity.
    Example: mark_complete("lock_puzzle")
    """
    if "completed_activities" not in st.session_state:
        st.session_state.completed_activities = set()
    st.session_state.completed_activities.add(activity_key)


def is_complete(activity_key: str) -> bool:
    """Check if an activity has been completed this session."""
    if "completed_activities" not in st.session_state:
        return False
    return activity_key in st.session_state.completed_activities


def get_completion_stats() -> dict:
    """Get completion percentages for each module."""
    completed = getattr(st.session_state, "completed_activities", set())
    stats = {}
    for module_key, module_data in ACTIVITIES.items():
        total = len(module_data["items"])
        done = sum(1 for k in module_data["items"] if k in completed)
        stats[module_key] = {
            "done": done,
            "total": total,
            "pct": round(done / total * 100) if total else 0,
            "label": module_data["label"],
            "color": module_data["color"],
        }
    return stats


def render_progress_card():
    """
    Render a compact progress card for the sidebar or any page.
    Shows completion % per module.
    """
    stats = get_completion_stats()
    total_done = sum(s["done"] for s in stats.values())
    total_items = sum(s["total"] for s in stats.values())
    overall_pct = round(total_done / total_items * 100) if total_items else 0

    st.markdown(f"**📊 Overall Progress: {overall_pct}%**")
    st.progress(overall_pct / 100)

    for module_key, s in stats.items():
        color = s["color"]
        st.markdown(
            f"""
            <div style="margin:4px 0;">
                <div style="display:flex;justify-content:space-between;
                    font-size:0.78rem;color:#888;margin-bottom:2px;">
                    <span>{s['label']}</span>
                    <span style="color:{color}">{s['done']}/{s['total']}</span>
                </div>
                <div style="background:rgba(255,255,255,0.08);
                    border-radius:4px;height:5px;overflow:hidden;">
                    <div style="background:{color};height:5px;
                        width:{s['pct']}%;border-radius:4px;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_full_progress_page():
    """Full progress page showing all activities with checkmarks."""
    st.title("📊 My Progress")

    xp = st.session_state.xp
    level = get_level(xp)
    progress = get_level_progress(xp)
    next_xp = get_next_level_xp(xp)

    # ── XP summary ────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⭐ Total XP", xp)
    with col2:
        st.metric("🏅 Current Rank", level)
    with col3:
        st.metric("🎯 XP to Next Rank", next_xp - xp)

    st.progress(progress)
    st.caption(f"Progress to {level} → next rank")

    st.markdown("---")

    # ── Badges ────────────────────────────────────────────────────────────
    if st.session_state.badges:
        st.markdown("### 🏅 Badges Earned")
        badge_cols = st.columns(4)
        for i, badge in enumerate(st.session_state.badges):
            with badge_cols[i % 4]:
                st.markdown(
                    f"""
                    <div style="background:rgba(124,109,250,0.1);
                        border:1px solid rgba(124,109,250,0.3);
                        border-radius:8px;padding:0.5rem;
                        text-align:center;font-size:0.8rem;
                        margin-bottom:6px;">
                        {badge}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.markdown("---")

    # ── Activity completion ────────────────────────────────────────────────
    st.markdown("### 📋 Activity Completion")
    completed = getattr(st.session_state, "completed_activities", set())

    for module_key, module_data in ACTIVITIES.items():
        color = module_data["color"]
        items = module_data["items"]
        done = sum(1 for k in items if k in completed)
        total = len(items)
        pct = round(done / total * 100) if total else 0

        st.markdown(
            f"""
            <div style="background:{color}10;border:1px solid {color}30;
                border-left:4px solid {color};border-radius:10px;
                padding:1rem 1.25rem;margin:0.75rem 0;">
                <div style="display:flex;justify-content:space-between;
                    align-items:center;margin-bottom:0.75rem;">
                    <strong style="color:{color}">{module_data['label']}</strong>
                    <span style="font-size:0.85rem;color:#888">
                        {done}/{total} completed ({pct}%)
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        for activity_key, activity_label in items.items():
            done_check = "✅" if activity_key in completed else "⬜"
            col1, col2 = st.columns([0.5, 9.5])
            with col1:
                st.markdown(done_check)
            with col2:
                st.markdown(
                    f"<span style='font-size:0.875rem;color:"
                    f"{'#ccc' if activity_key in completed else '#666'}'>"
                    f"{activity_label}</span>",
                    unsafe_allow_html=True
                )

    st.markdown("---")
    render_certificate_section()
    st.markdown("---")

    # ── Suggestions ───────────────────────────────────────────────────────
    st.markdown("### 💡 What to do next")
    completed = getattr(st.session_state, "completed_activities", set())

    all_items = {}
    for module_data in ACTIVITIES.values():
        all_items.update(module_data["items"])

    incomplete = [
        label for key, label in all_items.items()
        if key not in completed
    ]

    if incomplete:
        st.markdown("You still have these activities to complete:")
        for item in incomplete[:5]:
            st.markdown(f"→ {item}")
        if len(incomplete) > 5:
            st.caption(f"...and {len(incomplete) - 5} more!")
    else:
        st.success(
            "🎉 You've completed everything! You're a true Quantum Guardian. "
            "Ask your teacher about real NIST PQC documentation."
        )

    # ── Reset button ──────────────────────────────────────────────────────
    st.markdown("---")
    if st.button("🔄 Reset my progress", key="reset_progress"):
        st.session_state.completed_activities = set()
        st.session_state.xp = 0
        st.session_state.badges = []
        st.success("Progress reset! Starting fresh.")
        st.rerun()

        

def generate_certificate(student_name: str, grade_level: str, completed_count: int, total_count: int) -> str:
    """Generate a printable HTML certificate."""
    from datetime import date
    today = date.today().strftime("%B %d, %Y")
    
    grade_colors = {
        "Elementary (K-5)": ("#10b981", "#059669", "🟢"),
        "Middle School (6-8)": ("#7c6dfa", "#6d28d9", "🟡"),
        "High School (9-12)": ("#f45c5c", "#dc2626", "🔴"),
    }
    color, dark, emoji = grade_colors.get(grade_level, ("#4f46e5", "#3730a3", "🏅"))
    pct = round(completed_count / total_count * 100) if total_count else 0

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap');
  * {{ margin:0;padding:0;box-sizing:border-box; }}
  body {{ background:#0f172a;display:flex;justify-content:center;
    align-items:center;min-height:100vh;font-family:'Inter',sans-serif; }}
  .cert {{ background:white;width:900px;padding:60px;position:relative;
    border-top:12px solid {color}; }}
  .border-inner {{ border:3px solid {color}33;padding:40px;position:relative; }}
  .corner {{ position:absolute;width:30px;height:30px;border-color:{color};border-style:solid; }}
  .tl {{ top:-3px;left:-3px;border-width:3px 0 0 3px; }}
  .tr {{ top:-3px;right:-3px;border-width:3px 3px 0 0; }}
  .bl {{ bottom:-3px;left:-3px;border-width:0 0 3px 3px; }}
  .br {{ bottom:-3px;right:-3px;border-width:0 3px 3px 0; }}
  .logo {{ text-align:center;margin-bottom:20px; }}
  .logo-text {{ font-size:1.1rem;font-weight:600;color:{color};letter-spacing:3px;text-transform:uppercase; }}
  .divider {{ height:2px;background:linear-gradient(to right,transparent,{color},{color},transparent);margin:20px 0; }}
  .title {{ text-align:center;font-family:'Playfair Display',serif;
    font-size:3rem;color:#1e293b;margin:16px 0 8px; }}
  .subtitle {{ text-align:center;font-size:1rem;color:#64748b;
    letter-spacing:4px;text-transform:uppercase;margin-bottom:24px; }}
  .presented {{ text-align:center;font-size:0.9rem;color:#94a3b8;
    margin-bottom:8px;text-transform:uppercase;letter-spacing:2px; }}
  .student-name {{ text-align:center;font-family:'Playfair Display',serif;
    font-size:2.8rem;color:{color};margin:8px 0 24px;
    border-bottom:2px solid {color}33;padding-bottom:16px; }}
  .description {{ text-align:center;font-size:1rem;color:#475569;
    line-height:1.7;max-width:600px;margin:0 auto 24px; }}
  .grade-badge {{ display:inline-block;background:{color}15;border:2px solid {color};
    border-radius:100px;padding:8px 24px;font-size:0.9rem;
    font-weight:600;color:{color};margin-bottom:24px; }}
  .stats {{ display:flex;justify-content:center;gap:40px;margin:24px 0; }}
  .stat {{ text-align:center; }}
  .stat-num {{ font-size:2rem;font-weight:700;color:{color}; }}
  .stat-label {{ font-size:0.75rem;color:#94a3b8;text-transform:uppercase;letter-spacing:1px; }}
  .algorithms {{ background:{color}08;border:1px solid {color}20;
    border-radius:8px;padding:16px;margin:20px 0;text-align:center; }}
  .algo-title {{ font-size:0.75rem;color:#94a3b8;text-transform:uppercase;
    letter-spacing:2px;margin-bottom:8px; }}
  .algo-tags {{ display:flex;flex-wrap:wrap;gap:8px;justify-content:center; }}
  .algo-tag {{ background:{color}15;border:1px solid {color}30;
    border-radius:100px;padding:4px 12px;font-size:0.78rem;color:{color};font-weight:600; }}
  .footer {{ display:flex;justify-content:space-between;align-items:flex-end;
    margin-top:32px;padding-top:24px;border-top:1px solid #e2e8f0; }}
  .sig-line {{ width:200px;border-top:1px solid #94a3b8;padding-top:8px;
    font-size:0.78rem;color:#94a3b8;text-align:center; }}
  .date {{ font-size:0.85rem;color:#94a3b8; }}
  .seal {{ width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,{color},{dark});
    display:flex;align-items:center;justify-content:center;
    font-size:2rem;box-shadow:0 4px 20px {color}40; }}
  .nist {{ text-align:center;margin-top:16px;font-size:0.72rem;
    color:#94a3b8;letter-spacing:1px; }}
  @media print {{
    body {{ background:white; }}
    .no-print {{ display:none; }}
  }}
</style>
</head>
<body>
<div class="cert">
  <div class="border-inner">
    <div class="corner tl"></div>
    <div class="corner tr"></div>
    <div class="corner bl"></div>
    <div class="corner br"></div>

    <div class="logo">
      <div style="font-size:2rem">🔐</div>
      <div class="logo-text">QuantumVault Academy</div>
    </div>

    <div class="divider"></div>

    <div class="title">Certificate of Achievement</div>
    <div class="subtitle">Post-Quantum Cryptography Curriculum</div>

    <div class="presented">This certifies that</div>
    <div class="student-name">{student_name}</div>

    <div style="text-align:center">
      <span class="grade-badge">{emoji} {grade_level}</span>
    </div>

    <p class="description">
      has successfully completed the <strong>QuantumVault Academy</strong> 
      post-quantum cryptography curriculum, demonstrating knowledge of 
      NIST-standardized quantum-safe algorithms and their mathematical foundations.
    </p>

    <div class="stats">
      <div class="stat">
        <div class="stat-num">{completed_count}</div>
        <div class="stat-label">Activities Completed</div>
      </div>
      <div class="stat">
        <div class="stat-num">{pct}%</div>
        <div class="stat-label">Completion Rate</div>
      </div>
      <div class="stat">
        <div class="stat-num">{today.split()[2]}</div>
        <div class="stat-label">Year</div>
      </div>
    </div>

    <div class="algorithms">
      <div class="algo-title">NIST PQC Standards Studied</div>
      <div class="algo-tags">
        <span class="algo-tag">ML-KEM (Kyber) FIPS 203</span>
        <span class="algo-tag">ML-DSA (Dilithium) FIPS 204</span>
        <span class="algo-tag">SLH-DSA (SPHINCS+) FIPS 205</span>
        <span class="algo-tag">FN-DSA (Falcon) FIPS 206</span>
      </div>
    </div>

    <div class="footer">
      <div class="sig-line">
        QuantumVault Academy<br>Director of Education
      </div>
      <div class="seal">🔐</div>
      <div class="sig-line">
        {today}<br>Date of Completion
      </div>
    </div>

    <div class="nist">
      Aligned with NIST Post-Quantum Cryptography Standards · 
      NSA GenCyber Eligible · COPPA Compliant
    </div>
  </div>
</div>
<script>
  window.onload = function() {{ window.print(); }}
</script>
</body>
</html>"""


def render_certificate_section():
    """Render certificate download section in progress page."""
    import streamlit as st
    
    st.markdown("### 🏆 Certificates of Completion")
    
    completed = getattr(st.session_state, "completed_activities", set())
    stats = get_completion_stats()
    
    # Check which grade levels are complete enough for a certificate
    GRADE_ACTIVITIES = {
        "Elementary (K-5)": "elementary",
        "Middle School (6-8)": "middle_school", 
        "High School (9-12)": "high_school",
    }

    student_name = st.text_input(
        "Enter your name for the certificate:",
        placeholder="Your Name",
        key="cert_name"
    )

    any_eligible = False
    for grade_label, module_key in GRADE_ACTIVITIES.items():
        if module_key in stats:
            s = stats[module_key]
            pct = s["pct"]
            color = s["color"]
            done = s["done"]
            total = s["total"]

            eligible = pct >= 70

            st.markdown(
                f"<div style='background:{color}10;border:1px solid {color}30;"
                f"border-radius:10px;padding:12px;margin:8px 0;"
                f"display:flex;justify-content:space-between;align-items:center;'>"
                f"<div>"
                f"<strong style='color:{color}'>{grade_label}</strong>"
                f"<div style='font-size:0.8rem;color:#888'>{done}/{total} activities ({pct}% complete)</div>"
                f"</div>"
                f"<div style='font-size:1.5rem'>{'🏆' if eligible else '🔒'}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

            if eligible:
                any_eligible = True
                if st.button(
                    f"📥 Download {grade_label} Certificate",
                    key=f"cert_{module_key}",
                    type="primary" if pct == 100 else "secondary"
                ):
                    if not student_name:
                        st.warning("Please enter your name above!")
                    else:
                        cert_html = generate_certificate(
                            student_name, grade_label, done, total
                        )
                        st.download_button(
                            label=f"⬇️ Save Certificate as HTML",
                            data=cert_html,
                            file_name=f"QuantumVault_{grade_label.replace(' ','_')}_Certificate.html",
                            mime="text/html",
                            key=f"dl_{module_key}"
                        )
                        st.success("Certificate ready! Click the button above to download, then open it in your browser and print!")
            else:
                st.caption(f"Complete 70% of {grade_label} activities to unlock your certificate (need {70 - pct}% more)")

    if not any_eligible:
        st.info("Complete at least 70% of any grade level to earn your certificate!")
