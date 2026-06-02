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
            "🃏 Trading Cards",
            "🎯 Daily Challenge",
            "📸 Share Achievement",
            "🎨 My Character",
            "🌍 World Map",
            "📺 Explainers",
            "🧪 Crypto Lab",
            "📖 Research Journal",
            "📧 Weekly Report",
            "🏫 School Rankings",

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