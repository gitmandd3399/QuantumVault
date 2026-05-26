"""
QuantumVault Academy — Main Entry Point
Teaches Post-Quantum Cryptography from K–12.
"""

import streamlit as st
from modules.elementary import render_elementary
from modules.middle_school import render_middle_school
from modules.high_school import render_high_school
from utils.security import sanitize_input

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QuantumVault Academy",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ── Session state defaults ────────────────────────────────────────────────────
if "level" not in st.session_state:
    st.session_state.level = None
if "badges" not in st.session_state:
    st.session_state.badges = []
if "xp" not in st.session_state:
    st.session_state.xp = 0


# ── Sidebar — grade selector ──────────────────────────────────────────────────
def sidebar():
    st.sidebar.image("static/logo.png", use_column_width=True) if False else None
    st.sidebar.title("🔐 QuantumVault Academy")
    st.sidebar.markdown("---")

    grade = st.sidebar.selectbox(
        "Choose your grade level:",
        ["", "🟢 Elementary (K–5)", "🟡 Middle School (6–8)", "🔴 High School (9–12)"],
    )

    if grade:
        st.session_state.level = grade

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"⭐ **XP:** {st.session_state.xp}")
    if st.session_state.badges:
        st.sidebar.markdown("🏅 **Badges:** " + " ".join(st.session_state.badges))
    st.sidebar.markdown("---")
    st.sidebar.info(
        "QuantumVault Academy is a safe, ad-free learning environment. "
        "No personal data is stored."
    )


# ── Main router ───────────────────────────────────────────────────────────────
def main():
    sidebar()

    if not st.session_state.level:
        # Landing page
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


if __name__ == "__main__":
    main()
