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
            "quantumcraft_elem": "⛏️ Played QuantumCraft Crypto Kingdom",
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
            "quantumcraft_mid":    "⛏️ Played QuantumCraft Lattice Mines",
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
            "quantumcraft_hs":     "🏃 Played Cipher Ruins runner",
        }
    }
}


def load_progress() -> dict:
    """Load all student progress from file."""
    try:
        if PROGRESS_FILE.exists():
            return json.loads(PROGRESS_FILE.read_text())
    except Exception:
        pass
    return {}


def save_progress(data: dict):
    """Save all student progress to file."""
    try:
        PROGRESS_FILE.write_text(json.dumps(data, indent=2))
    except Exception:
        pass


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