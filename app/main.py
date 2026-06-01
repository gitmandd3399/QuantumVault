"""
QuantumVault Academy — Main Entry Point
Teaches Post-Quantum Cryptography from K–12.
"""

import os
import streamlit as st
from modules.elementary import render_elementary
from modules.middle_school import render_middle_school
from modules.high_school import render_high_school
from modules.leaderboard import render_leaderboard
from modules.mission_map import render_mission_map
from modules.teacher_dashboard import render_teacher_dashboard
from utils.security import sanitize_input, get_level, get_level_progress, get_next_level_xp
from modules.progress_tracker import render_full_progress_page, mark_complete, render_progress_card
from modules.payments import render_pricing_page
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

if __name__ == "__main__":
    main()