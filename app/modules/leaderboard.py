"""
modules/leaderboard.py
──────────────────────
COPPA-safe leaderboard — nicknames only, no real names or personal data.
Scores stored in a local JSON file during the session.
"""

import json
import pathlib
import streamlit as st
from utils.security import sanitize_input, check_rate_limit, get_level

SCORES_FILE = pathlib.Path(__file__).parent.parent / "static" / "scores.json"


def load_scores() -> dict:
    """Load scores from JSON file. Returns empty dict if file doesn't exist."""
    try:
        if SCORES_FILE.exists():
            return json.loads(SCORES_FILE.read_text())
    except Exception as _e:
        logging.warning("Leaderboard read error: %s", _e)  # nosec B110
    return {}


def save_scores(scores: dict):
    """Save scores to JSON file safely."""
    try:
        SCORES_FILE.write_text(json.dumps(scores, indent=2))
    except Exception as _e:
        import logging; logging.warning("Leaderboard write error: %s", _e)  # nosec B110


def render_leaderboard():
    st.title("🏆 Leaderboard — Top Agents")
    st.markdown(
        "Enter your agent codename to save your score. "
        "No real names — COPPA safe! 🔒"
    )

    # ── Save score ────────────────────────────────────────────────────────
    xp = st.session_state.xp
    level = get_level(xp)

    col1, col2 = st.columns([3, 1])
    with col1:
        nickname = st.text_input(
            "Your agent codename:",
            max_chars=20,
            placeholder="e.g. QuantumFox, CipherKid, LatticeHero",
            key="leaderboard_nickname"
        )
    with col2:
        st.metric("Your XP", xp)

    if st.button("💾 Save my score", key="save_score"):
        if not check_rate_limit("leaderboard_save", st.session_state):
            st.warning("Slow down agent! Try again in a moment.")
        else:
            clean_name = sanitize_input(nickname, max_length=20)
            if len(clean_name) < 2:
                st.warning("Please enter a codename of at least 2 characters!")
            elif xp == 0:
                st.warning("Earn some XP first before saving your score!")
            else:
                scores = load_scores()
                # Only update if new score is higher
                if clean_name not in scores or scores[clean_name]["xp"] < xp:
                    scores[clean_name] = {"xp": xp, "level": level}
                    save_scores(scores)
                    st.success(f"✅ Score saved! **{clean_name}** — {xp} XP — {level}")
                else:
                    st.info(
                        f"Your previous score of {scores[clean_name]['xp']} XP "
                        "is already higher — keep earning to beat it!"
                    )

    st.markdown("---")

    # ── Top 10 display ────────────────────────────────────────────────────
    scores = load_scores()

    if not scores:
        st.info("🏅 No scores yet — be the first agent on the board!")
        return

    st.markdown("### 🥇 Top 10 Agents")

    sorted_scores = sorted(
        scores.items(),
        key=lambda x: x[1]["xp"],
        reverse=True
    )[:10]

    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7

    for i, (name, data) in enumerate(sorted_scores):
        col1, col2, col3, col4 = st.columns([0.5, 2.5, 1.5, 2])
        with col1:
            st.markdown(f"**{medals[i]}**")
        with col2:
            st.markdown(f"**{sanitize_input(str(name), max_length=50)}**")
        with col3:
            st.markdown(f"⭐ {data['xp']} XP")
        with col4:
            st.markdown(f"{data['level']}")

    st.markdown("---")
    st.caption(
        "🔒 Only codenames and XP scores are stored. "
        "No personal information is collected."
    )