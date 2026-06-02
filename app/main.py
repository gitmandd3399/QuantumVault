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
        render_high_school()
    elif "Leaderboard" in level:
        render_leaderboard()
    elif "Mission Map" in level:
        render_mission_map()
    elif "Teacher Dashboard" in level:
        render_teacher_dashboard()
    elif "My Progress" in level:
        render_full_progress_page()
    elif "Pricing" in level:
        render_pricing_page()
    elif "AI Tutor" in level:
        render_ai_tutor()

if __name__ == "__main__":
    main()