"""
QuantumVault Academy — Main Entry Point
Teaches Post-Quantum Cryptography from K–12.
"""

import os
import streamlit as st
import datetime
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

    grade = st.sidebar.selectbox(
        "Choose your grade level:",
        [
            "",
            "🟢 Elementary (K–5)",
            "🟡 Middle School (6–8)",
            "🔴 High School (9–12)",
            "🏆 Leaderboard",
            "🗺️ Mission Map",
            "👨‍🏫 Teacher Dashboard",
            "📊 My Progress",
            "💎 Pricing & Plans",
            "🤖 AI Tutor",

        ],
    )

    if grade:
        st.session_state.level = grade

    st.sidebar.markdown("---")

    xp = st.session_state.xp
    level = get_level(xp)
    progress = get_level_progress(xp)
    next_xp = get_next_level_xp(xp)

    st.sidebar.markdown(f"### {level}")
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
        st.sidebar.components.v1.html("""
<script>
(function() {
    if (window._qvMusicStarted) return;
    window._qvMusicStarted = true;

    const ctx = new (window.AudioContext || window.webkitAudioContext)();

    // Chiptune melody notes (frequencies in Hz)
    const MELODY = [
        261, 293, 329, 349, 392, 349, 329, 293,
        261, 261, 293, 329, 261, 261, 0,   0,
        349, 349, 392, 440, 392, 349, 329, 293,
        261, 0,   261, 293, 329, 293, 261, 0,
    ];

    const BASS = [
        130, 0, 130, 0, 146, 0, 146, 0,
        130, 0, 130, 0, 116, 0, 116, 0,
        174, 0, 174, 0, 164, 0, 164, 0,
        130, 0, 130, 0, 146, 0, 146, 0,
    ];

    let noteIdx = 0;
    const BPM = 120;
    const NOTE_DUR = 60 / BPM / 2;

    function playNote(freq, vol, type, start, dur) {
        if (freq === 0) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.type = type;
        osc.frequency.setValueAtTime(freq, start);
        gain.gain.setValueAtTime(vol, start);
        gain.gain.exponentialRampToValueAtTime(0.001, start + dur * 0.9);
        osc.start(start);
        osc.stop(start + dur);
    }

    function scheduleNotes() {
        const now = ctx.currentTime;
        for (let i = 0; i < 8; i++) {
            const t = now + i * NOTE_DUR;
            const idx = (noteIdx + i) % MELODY.length;
            playNote(MELODY[idx], 0.08, "square", t, NOTE_DUR * 0.8);
            playNote(BASS[idx],   0.06, "triangle", t, NOTE_DUR * 0.9);
        }
        noteIdx = (noteIdx + 8) % MELODY.length;
    }

    ctx.resume().then(() => {
        scheduleNotes();
        setInterval(scheduleNotes, NOTE_DUR * 8 * 1000);
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