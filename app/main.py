"""
QuantumVault Academy — Main Entry Point
Teaches Post-Quantum Cryptography from K–12.
"""

import os
import streamlit as st
import datetime
from modules.mfa import render_mfa_login
from modules.users import get_user, update_plan, get_user_count
from modules.elementary import render_elementary
from modules.middle_school import render_middle_school
from modules.high_school import render_high_school
from modules.leaderboard import render_leaderboard
from modules.mission_map import render_mission_map
from modules.teacher_dashboard import render_teacher_dashboard
from utils.security import sanitize_input, get_level, get_level_progress, get_next_level_xp
from modules.progress_tracker import render_full_progress_page, mark_complete, render_progress_card
from modules.payments import render_pricing_page
from modules.ai_tutor import render_ai_tutor
from modules.trading_cards import render_trading_cards
from modules.daily_challenge import render_daily_challenge
from modules.share_cards import render_share_page
from modules.character import render_character_page
from modules.world_map import render_world_map
from modules.explainers import render_explainers_page
from modules.crypto_lab import render_crypto_lab
from modules.research_journal import render_research_journal
from modules.weekly_email import render_weekly_email
from modules.school_leaderboard import render_school_leaderboard
from modules.cipher_decoder import render_cipher_decoder
from modules.escape_room import render_escape_room
from modules.tls_simulator import render_tls_simulator
from modules.threat_thermometer import render_threat_thermometer
from modules.algo_battle import render_algo_battle
from modules.quantum_orbital import render_quantum_orbital
from modules.games import render_prime_factor_game, render_network_defender, render_secret_message, render_falling_blocks, render_ctf_game, render_code_shield, render_pqc_python_lab, render_cipher_quest
from modules.career_explorer import render_career_explorer
from modules.harvest_timeline import render_harvest_timeline
from modules.pqc_demo import render_pqc_demo
from modules.story_adventure import render_story_adventure
from modules.quantum_sandbox import render_quantum_sandbox
from modules.privacy_policy import render_privacy_policy, render_terms_of_service
# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QuantumVault Academy",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
with open(os.path.join(os.path.dirname(__file__), "static/style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
if "level" not in st.session_state:
    st.session_state.level = None
if "badges" not in st.session_state:
    st.session_state.badges = []
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "plan_type" not in st.session_state:
    st.session_state.plan_type = "free"
if "free_module" not in st.session_state:
    st.session_state.free_module = None

# ── Developer override ────────────────────────────────────────────────────────
_dev_password = st.secrets.get("DEV_PASSWORD", "")
if _dev_password:
    _dev_input = st.sidebar.text_input(
        "🔑 Admin:", type="password", key="dev_unlock",
        label_visibility="collapsed",
        placeholder="Admin access..."
    )
    if _dev_input == _dev_password:
        st.session_state.plan_type = "admin"
        st.session_state.mfa_verified = True
        st.session_state.is_admin = True
        st.session_state.free_module = None


# ── Google Search Console Verification ──────────────────────────────────────
_query = st.query_params
if _query.get("google_verify") == "a3abbd1f357726a3":
    st.write("google-site-verification: googlea3abbd1f357726a3.html")
    st.stop()

# ── Load user plan from DB if logged in ──────────────────────────────────────
# ── SESSION EXPIRY (8 hours) ─────────────────────────────────────────────────
import time as _time
_SESSION_TTL = 8 * 3600  # 8 hours
if st.session_state.get("mfa_verified"):
    _login_time = st.session_state.get("login_timestamp", 0)
    if _time.time() - _login_time > _SESSION_TTL:
        # Session expired - clear auth state
        for _k in ["mfa_verified","user_email","mfa_step","mfa_code","mfa_code_time","mfa_email","mfa_attempts"]:
            if _k in st.session_state:
                del st.session_state[_k]
        st.warning("Session expired. Please log in again.")
        st.rerun()

# ── AUDIT LOGGING ─────────────────────────────────────────────────────────────
import logging as _logging
_audit_log = _logging.getLogger("quantumvault.audit")
if not _audit_log.handlers:
    _h = _logging.StreamHandler()
    _h.setFormatter(_logging.Formatter('%(asctime)s AUDIT %(message)s'))
    _audit_log.addHandler(_h)
    _audit_log.setLevel(_logging.INFO)

def log_audit(action, detail=""):
    _email = st.session_state.get("user_email", "anonymous")
    _audit_log.info(f"user={_email} action={action} detail={detail}")

# ── CSP HEADERS via Streamlit meta injection ──────────────────────────────────
st.markdown("""
<meta http-equiv="Content-Security-Policy" 
    content="default-src 'self' https:; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline';">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
""", unsafe_allow_html=True)

_user_email = st.session_state.get("user_email", "")
if _user_email and st.session_state.get("mfa_verified"):
    _db_user = get_user(_user_email)
    if _db_user:
        st.session_state.plan_type = _db_user.get("plan", "free")

# ── Email MFA Gate — only for paid/upgraded users ────────────────────────────
_gmail = st.secrets.get("GMAIL_USER", "")
_plan = st.session_state.get("plan_type", "free")
_mfa_verified = st.session_state.get("mfa_verified", False)

if _gmail and _plan == "paid" and not _mfa_verified:
    if not render_mfa_login():
        st.stop()

if "streak_days" not in st.session_state:
    st.session_state.streak_days = 0
if "last_visit" not in st.session_state:
    st.session_state.last_visit = None
if "streak_bonus_claimed" not in st.session_state:
    st.session_state.streak_bonus_claimed = False

# ── Daily streak logic ────────────────────────────────────────────────────────
def update_streak():
    today = datetime.date.today()
    last = st.session_state.last_visit
    if last is None:
        st.session_state.streak_days = 1
        st.session_state.last_visit = today
        st.session_state.streak_bonus_claimed = False
    elif last == today:
        pass  # Already visited today
    elif last == today - datetime.timedelta(days=1):
        st.session_state.streak_days += 1
        st.session_state.last_visit = today
        st.session_state.streak_bonus_claimed = False
    else:
        st.session_state.streak_days = 1
        st.session_state.last_visit = today
        st.session_state.streak_bonus_claimed = False

update_streak()


# ── Sidebar ───────────────────────────────────────────────────────────────────
def sidebar():
    st.sidebar.title("🔐 QuantumVault Academy")
    st.sidebar.markdown(
        "🔒 **Privacy:** This app collects no personal data. Safe for all ages."
    )

    # ── Custom styled navigation ─────────────────────────────────────────
    SECTIONS = [
        {"label": "📚 LEARN", "color": "#10b981", "items": [
            ("🟢", "Elementary (K-5)",    "🟢 Elementary (K–5)"),
            ("🟡", "Middle School (6-8)", "🟡 Middle School (6–8)"),
            ("🔴", "High School (9-12)",  "🔴 High School (9–12)"),
            ("🦸", "Story Adventure",   "🦸 Story Adventure"),
        ]},
        {"label": "🎮 GAMES", "color": "#f59e0b", "items": [
            ("🔤", "Secret Message",    "🔤 Secret Message Maker"),
            ("🔢", "Prime Factor",      "🔢 Prime Factor Cracker"),
            ("🌐", "Network Defender",  "🌐 Network Defender"),
            ("🚀", "Quantum Orbital", "🚀 Quantum Orbital"),
            ("🧱", "Falling Blocks",    "🧱 Falling Blocks"),
            ("🧪", "Quantum Sandbox",   "🧪 Quantum Sandbox"),
            ("🚩", "CTF Challenge",    "🚩 CTF Challenge"),
            ("─", "── Coding Games Trial ──", "─ Coding Games"),
            ("🛡️", "Code the Shield",   "🛡️ Code the Shield"),
            ("🐍", "PQC Python Lab",    "🐍 PQC Python Lab"),
            ("🎮", "Cipher Quest",      "🎮 Cipher Quest"),
            ("─", "── Premium Games ──", "─"),
            ("🧩", "Cipher Decoder",   "🧩 Cipher Decoder"),
            ("🏃", "Escape Room",      "🏃 Escape Room"),
            ("🃏", "Algo Battle",      "🃏 Algo Battle"),
            ("🎯", "Daily Challenge",  "🎯 Daily Challenge"),
        ]},
        {"label": "🔬 LABS", "color": "#8b5cf6", "items": [
            ("🧪", "Crypto Lab",         "🧪 Crypto Lab"),
            ("📡", "TLS Simulator",      "📡 TLS Simulator"),
            ("🌡️", "Threat Thermometer", "🌡️ Threat Thermometer"),
            ("⚛️", "PQC Live Demo",     "⚛️ PQC Live Demo"),
            ("📺", "Explainers",         "📺 Explainers"),
        ]},
        {"label": "👤 PROFILE", "color": "#3b82f6", "items": [
            ("📊", "My Progress",       "📊 My Progress"),
            ("🎨", "My Character",      "🎨 My Character"),
            ("🃏", "Trading Cards",     "🃏 Trading Cards"),
            ("📸", "Share Achievement", "📸 Share Achievement"),
        ]},
        {"label": "🏆 COMMUNITY", "color": "#ec4899", "items": [
            ("🏆", "Leaderboard",     "🏆 Leaderboard"),
            ("🏫", "School Rankings", "🏫 School Rankings"),
            ("🗺️", "Mission Map",     "🗺️ Mission Map"),
            ("🌍", "World Map",       "🌍 World Map"),
        ]},
        {"label": "📖 RESOURCES", "color": "#06b6d4", "items": [
            ("🤖", "AI Tutor",          "🤖 AI Tutor"),
            ("📖", "Research Journal",  "📖 Research Journal"),
            ("🗺️", "Career Explorer",   "🗺️ Career Explorer"),
            ("📧", "Weekly Report",     "📧 Weekly Report"),
        ]},
        {"label": "⚙️ ACCOUNT", "color": "#6b7280", "items": [
            ("👨‍🏫", "Teacher Dashboard", "👨‍🏫 Teacher Dashboard"),
            ("💎", "Pricing & Plans",    "💎 Pricing & Plans"),
            ("🔒", "Privacy Policy",      "🔒 Privacy Policy"),
            ("📋", "Terms of Service",    "📋 Terms of Service"),
        ]},
    ]

    current = st.session_state.get("level", "")

    def get_active_section(cur):
        for sec in SECTIONS:
            for _, _, route in sec["items"]:
                if route == cur:
                    return sec["label"]
        return None

    active_sec = get_active_section(current)

    for sec in SECTIONS:
        c = sec["color"]
        is_open = (active_sec == sec["label"])
        with st.sidebar.expander(sec["label"], expanded=is_open):
            for emoji, label, route in sec["items"]:
                if route.startswith("─"):
                    st.markdown(
                        f"<div style='color:#475569;font-size:10px;"
                        f"padding:2px 0;border-top:1px solid #1e293b;"
                        f"margin:3px 0'>{label}</div>",
                        unsafe_allow_html=True
                    )
                    continue
                if route == current:
                    st.markdown(
                        f"<div style='background:{c}20;border-left:3px solid {c};"
                        f"padding:5px 8px;border-radius:4px;color:{c};"
                        f"font-size:12px;font-weight:bold;margin:2px 0'>"
                        f"{emoji} {label} ◀</div>",
                        unsafe_allow_html=True
                    )
                else:
                    if st.button(
                        f"{emoji} {label}",
                        key=f"nav_{route}",
                        use_container_width=True,
                    ):
                        st.session_state.level = route
                        st.rerun()
    st.sidebar.markdown("---")

    xp = st.session_state.xp
    xp_rank = get_level(xp)
    progress = get_level_progress(xp)
    next_xp = get_next_level_xp(xp)

    st.sidebar.markdown(f"### {xp_rank}")
    bar_filled = int(progress * 10)
    bar_empty = 10 - bar_filled
    bar_visual = "🟦" * bar_filled + "⬜" * bar_empty
    st.sidebar.markdown(f"{bar_visual}")
    st.sidebar.caption(f"⭐ {xp} XP — {next_xp - xp} XP to next rank")

    # ── Plan badge ────────────────────────────────────────────────────────
    plan = st.session_state.get("plan_type", "free")
    if plan == "free":
        st.sidebar.markdown(
            "<div style='background:#6b728015;border:1px solid #6b728040;"
            "border-radius:8px;padding:6px 12px;margin:4px 0;text-align:center;'>"
            "<span style='font-size:0.75rem;color:#9ca3af'>🆓 Free Plan — </span>"
            "<span style='font-size:0.75rem;color:#4f46e5;font-weight:bold;'>"
            "Upgrade for full access</span></div>",
            unsafe_allow_html=True
        )
    else:
        st.sidebar.markdown(
            "<div style='background:#10b98115;border:1px solid #10b98140;"
            "border-radius:8px;padding:6px 12px;margin:4px 0;text-align:center;'>"
            "<span style='font-size:0.75rem;color:#10b981;font-weight:bold;'>"
            "✅ Pro Plan — Full Access</span></div>",
            unsafe_allow_html=True
        )

    # ── Streak display ────────────────────────────────────────────────────
    streak = st.session_state.streak_days
    if streak >= 7:
        streak_emoji = "🔥🔥🔥"
        streak_color = "#ef4444"
    elif streak >= 3:
        streak_emoji = "🔥🔥"
        streak_color = "#f97316"
    elif streak >= 1:
        streak_emoji = "🔥"
        streak_color = "#f59e0b"
    else:
        streak_emoji = "💤"
        streak_color = "#6b7280"

    st.sidebar.markdown(
        f"<div style='background:{streak_color}15;border:1px solid {streak_color}40;"
        f"border-radius:8px;padding:8px 12px;margin:6px 0;'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
        f"<span style='font-size:0.8rem;font-weight:bold;color:{streak_color}'>"
        f"{streak_emoji} {streak} Day Streak!</span>"
        f"<span style='font-size:0.7rem;color:#888'>Keep it up!</span>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    # ── Streak bonus XP ───────────────────────────────────────────────────
    if not st.session_state.streak_bonus_claimed and streak > 1:
        bonus_xp = min(streak * 5, 50)
        st.session_state.xp += bonus_xp
        st.session_state.streak_bonus_claimed = True
        st.sidebar.success(f"🔥 Streak bonus! +{bonus_xp} XP for {streak} day streak!")

    # ── Streak milestones ─────────────────────────────────────────────────
    if streak == 3:
        if "streak_3" not in st.session_state.badges:
            st.session_state.badges.append("🔥 3-Day Streak")
            st.sidebar.success("🏅 Badge: 3-Day Streak!")
    elif streak == 7:
        if "streak_7" not in st.session_state.badges:
            st.session_state.badges.append("🔥 7-Day Streak")
            st.sidebar.success("🏅 Badge: 7-Day Streak! You are on fire!")
    elif streak == 30:
        if "streak_30" not in st.session_state.badges:
            st.session_state.badges.append("🔥 30-Day Streak")
            st.sidebar.success("🏅 Badge: 30-Day Streak! Quantum Guardian!")

    if st.session_state.badges:
        st.sidebar.markdown("**🏅 Badges earned:**")
        for badge in st.session_state.badges:
            st.sidebar.markdown(f"- {badge}")

    st.sidebar.markdown("---")

    # ── Background Music ──────────────────────────────────────────────────
    if "music_on" not in st.session_state:
        st.session_state.music_on = False

    music_col1, music_col2 = st.sidebar.columns([1, 3])
    with music_col1:
        if st.button("🎵" if not st.session_state.music_on else "🔇", key="music_toggle"):
            st.session_state.music_on = not st.session_state.music_on
            st.rerun()
    with music_col2:
        st.caption("Music " + ("ON" if st.session_state.music_on else "OFF"))

    if st.session_state.music_on:
        import streamlit.components.v1 as _music_comp
        _music_comp.html("""
<script>
(function() {
    if (window._qvMusicStarted) return;
    window._qvMusicStarted = true;

    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const master = ctx.createGain();
    master.gain.setValueAtTime(0.18, ctx.currentTime);
    master.connect(ctx.destination);

    // Add reverb for warmth
    const convolver = ctx.createConvolver();
    const revGain = ctx.createGain();
    revGain.gain.setValueAtTime(0.25, ctx.currentTime);
    convolver.connect(revGain);
    revGain.connect(master);

    // Create impulse response for reverb
    const rate = ctx.sampleRate;
    const length = rate * 1.5;
    const impulse = ctx.createBuffer(2, length, rate);
    for (let c = 0; c < 2; c++) {
        const data = impulse.getChannelData(c);
        for (let i = 0; i < length; i++) {
            data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i/length, 2.5);
        }
    }
    convolver.buffer = impulse;

    // Smooth jazz chord progression: Cmaj7 - Am7 - Dm7 - G7
    // Notes in Hz (jazz voicings)
    const PROGRESSION = [
        // Cmaj7: C E G B
        {melody:[523,659,784,987], bass:130, dur:2.0},
        // Am7: A C E G
        {melody:[440,523,659,784], bass:110, dur:2.0},
        // Dm7: D F A C
        {melody:[587,698,880,1047],bass:146, dur:2.0},
        // G7: G B D F
        {melody:[784,987,587,698], bass:196, dur:2.0},
        // Fmaj7: F A C E
        {melody:[698,880,1047,1319],bass:174,dur:2.0},
        // Em7: E G B D
        {melody:[659,784,987,1174],bass:164, dur:2.0},
        // Dm7: D F A C
        {melody:[587,698,880,1047],bass:146, dur:2.0},
        // G7: G B D F
        {melody:[784,987,1174,698],bass:196, dur:2.0},
    ];

    // Walking bass line notes
    const WALK = [
        [130,146,164,174], [110,123,130,146],
        [146,164,174,196], [196,220,246,261],
        [174,196,220,246], [164,174,196,220],
        [146,164,174,196], [196,220,246,130],
    ];

    // Jazz melody riff
    const RIFF = [
        [784,0,659,0,523,587,0,523],
        [440,0,523,0,587,523,0,440],
        [587,0,698,0,784,698,0,587],
        [784,659,0,523,0,659,784,0],
    ];

    function playSmooth(freq, vol, start, dur, type="sine") {
        if (!freq) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        const filter = ctx.createBiquadFilter();
        filter.type = "lowpass";
        filter.frequency.setValueAtTime(2000, start);
        osc.connect(filter);
        filter.connect(gain);
        gain.connect(master);
        gain.connect(convolver);
        osc.type = type;
        osc.frequency.setValueAtTime(freq, start);
        // Smooth attack and release
        gain.gain.setValueAtTime(0, start);
        gain.gain.linearRampToValueAtTime(vol, start + 0.08);
        gain.gain.setValueAtTime(vol, start + dur - 0.15);
        gain.gain.linearRampToValueAtTime(0, start + dur);
        osc.start(start);
        osc.stop(start + dur + 0.05);
    }

    function playChord(notes, vol, start, dur) {
        notes.forEach((freq, i) => {
            // Stagger notes slightly for jazz feel
            setTimeout(() => {
                playSmooth(freq, vol / notes.length, start, dur, "sine");
            }, i * 30);
        });
    }

    let progIdx = 0;
    let riffIdx = 0;
    let beatCount = 0;

    function scheduleJazz() {
        const now = ctx.currentTime;
        const chord = PROGRESSION[progIdx % PROGRESSION.length];
        const walk = WALK[progIdx % WALK.length];
        const riff = RIFF[riffIdx % RIFF.length];
        const dur = chord.dur;

        // Play chord (soft background)
        playChord(chord.melody, 0.06, now, dur * 0.95);

        // Walking bass
        for (let i = 0; i < 4; i++) {
            playSmooth(walk[i], 0.12, now + i * (dur/4), dur/4 * 0.85, "triangle");
        }

        // Melody riff (every other chord)
        if (beatCount % 2 === 0) {
            riff.forEach((freq, i) => {
                if (freq) {
                    playSmooth(freq, 0.05, now + i * (dur/8), dur/8 * 0.7, "sine");
                }
            });
            riffIdx++;
        }

        progIdx++;
        beatCount++;
    }

    ctx.resume().then(() => {
        scheduleJazz();
        setInterval(scheduleJazz, 2000);
    });
})();
</script>
""", height=0)

    st.sidebar.info(
        "QuantumVault Academy is a safe, ad-free learning environment. "
        "No personal data is stored."
    )


# ── Main router ───────────────────────────────────────────────────────────────
def main():
    sidebar()

    if not st.session_state.level:
        st.markdown(
            """
            <div class="hero">
                <h1>🔐 QuantumVault Academy</h1>
                <p class="subtitle">
                    Learn the cryptography that protects the future — from quantum monsters
                    all the way to real-world NIST standards.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("🟢 **Elementary**\nPuzzles & stories about secret locks")
        with col2:
            st.warning("🟡 **Middle School**\nLattice mazes & hash factories")
        with col3:
            st.error("🔴 **High School**\nReal PQC algorithms & code labs")
        st.markdown("*← Pick your grade level in the sidebar to begin!*")
        return

    level = st.session_state.level
    plan = st.session_state.get("plan_type", "free")
    free_mod = st.session_state.get("free_module", "")

    # FREE TIER GATING
    FREE_ALLOWED = [
        "💎 Pricing & Plans",
        "🔒 Privacy Policy",
        "📋 Terms of Service",
        "🏆 Leaderboard",
        "🌍 World Map",
        "🗺️ Mission Map",
        "📊 My Progress",
        "🔢 Prime Factor Cracker",
        "🌐 Network Defender",
        "☠️ Harvest Timeline",
        "🚀 Quantum Orbital",
        "🔤 Secret Message Maker",
        "🧱 Falling Blocks",
        "🚩 CTF Challenge",
        "🛡️ Code the Shield",
        "🐍 PQC Python Lab",
        "🎮 Cipher Quest",
        "⚛️ PQC Live Demo",
        "🦸 Story Adventure",
    ]

    GRADE_MAP = {
        "Elementary": "🟢 Elementary (K–5)",
        "Middle":     "🟡 Middle School (6–8)",
        "High":       "🔴 High School (9–12)",
    }

    if plan == "free" and level and not level.startswith("─"):
        allowed = False
        # Always allow free pages
        for fa in FREE_ALLOWED:
            if fa in level:
                allowed = True
                break
        # Allow the chosen free module
        if free_mod:
            for key, val in GRADE_MAP.items():
                if key in free_mod and key in level:
                    allowed = True
                    break
        # If not allowed show upgrade prompt
        if not allowed and level not in ["", None]:
            st.markdown(
                "<div style='background:#071520;border:2px solid #1d4ed8;"
                "border-radius:16px;padding:30px;text-align:center;margin:20px 0'>"
                "<div style='font-size:3rem;margin-bottom:10px'>🔐</div>"
                "<h2 style='color:#60a5fa;margin-bottom:8px'>Premium Feature</h2>"
                "<p style='color:#94a3b8;margin-bottom:16px'>"
                "This feature is available on paid plans.<br>"
                "Your free plan includes: <b style='color:#60a5fa'>"
                + (free_mod if free_mod else "one grade module of your choice") +
                "</b></p>"
                "</div>",
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("🚀 View Plans & Upgrade", type="primary",
                             use_container_width=True, key="gate_upgrade"):
                    st.session_state.level = "💎 Pricing & Plans"
                    st.rerun()
                st.markdown(
                    "<div style='text-align:center;margin-top:8px;"
                    "font-size:0.85rem;color:#475569'>"
                    "School license from $1,999/yr · 30-day free trial · No credit card</div>",
                    unsafe_allow_html=True
                )
            st.stop()

    if not level or level.startswith("─"):
        st.markdown(
            "<div style='text-align:center;padding:60px 20px'>"
            "<div style='font-size:4rem'>🔐</div>"
            "<h2 style='color:#a5b4fc'>Welcome to QuantumVault Academy!</h2>"
            "<p style='color:#888'>Select a section from the dropdown in the sidebar to get started!</p>"
            "</div>",
            unsafe_allow_html=True
        )
        st.stop()
    if "Elementary" in level:
        render_elementary()
    elif "Middle" in level:
        render_middle_school()
    elif "High School" in level:
        plan = st.session_state.get("plan_type", "free")
        free_mod = st.session_state.get("free_module", "")
        if plan == "free" and free_mod and "High" not in free_mod:
            st.warning("Your free plan includes: " + free_mod)
            st.markdown("Upgrade to access all three grade levels!")
            if st.button("Upgrade Now", type="primary", key="upg_hs"):
                st.session_state.level = "💎 Pricing & Plans"
                st.rerun()
        else:
            render_high_school()
    elif "Leaderboard" in level:
        render_leaderboard()
    elif "Mission Map" in level:
        render_mission_map()
    elif "Teacher Dashboard" in level:
        if st.session_state.get("plan_type", "free") == "free":
            st.title("👨‍🏫 Teacher Dashboard")
            st.warning("The Teacher Dashboard is available on paid plans.")
            st.markdown("Upgrade to unlock class analytics, XP charts, and CSV export.")
            if st.button("🚀 Upgrade Now", type="primary", key="upgrade_teacher"):
                st.session_state.level = "💎 Pricing & Plans"
                st.rerun()
        else:
            render_teacher_dashboard()
    elif "My Progress" in level:
        render_full_progress_page()
    elif "Pricing" in level:
        render_pricing_page()
    elif "Trading Cards" in level:
        render_trading_cards()
    elif "Prime Factor" in level:
        render_prime_factor_game()
    elif "Network Defender" in level:
        render_network_defender()
    elif "Quantum Orbital" in level:
        render_quantum_orbital()
    elif "Secret Message" in level:
        render_secret_message()
    elif "Quantum Sandbox" in level:
        render_quantum_sandbox()
    elif "Falling Blocks" in level:
        render_falling_blocks()
    elif "CTF Challenge" in level:
        render_ctf_game()
    elif "Code the Shield" in level:
        render_code_shield()
    elif "PQC Python Lab" in level:
        render_pqc_python_lab()
    elif "Cipher Quest" in level:
        render_cipher_quest()
    elif "Daily Challenge" in level:
        render_daily_challenge()
    elif "Share Achievement" in level:
        render_share_page()
    elif "My Character" in level:
        render_character_page()
    elif "World Map" in level:
        render_world_map()
    elif "Explainers" in level:
        render_explainers_page()
    elif "Crypto Lab" in level:
        render_crypto_lab()
    elif "Research Journal" in level:
        render_research_journal()
    elif "Weekly Report" in level:
        render_weekly_email()
    elif "School Rankings" in level:
        render_school_leaderboard()
    elif "Cipher Decoder" in level:
        render_cipher_decoder()
    elif "Escape Room" in level:
        render_escape_room()
    elif "TLS Simulator" in level:
        render_tls_simulator()
    elif "Threat Thermometer" in level:
        render_threat_thermometer()
    elif "Algo Battle" in level:
        render_algo_battle()
    elif "Story Adventure" in level:
        render_story_adventure()
    elif "PQC Live Demo" in level:
        render_pqc_demo()
    elif "Career Explorer" in level:
        render_career_explorer()
    elif "Harvest Timeline" in level:
        render_harvest_timeline()
    elif "Privacy Policy" in level:
        render_privacy_policy()
    elif "Terms of Service" in level:
        render_terms_of_service()
    elif "AI Tutor" in level:
        if st.session_state.get("plan_type", "free") == "free":
            st.title("🤖 AI Tutor")
            st.warning("The AI Tutor is available on paid plans.")
            st.markdown("Upgrade to unlock grade-adaptive AI tutoring powered by Claude AI.")
            if st.button("🚀 Upgrade Now", type="primary", key="upgrade_tutor"):
                st.session_state.level = "💎 Pricing & Plans"
                st.rerun()
        else:
            render_ai_tutor()

if __name__ == "__main__":
    main()