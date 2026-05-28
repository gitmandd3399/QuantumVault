"""
modules/mission_map.py
Mission World Map — unlockable zones based on XP level.
"""

import streamlit as st
import plotly.graph_objects as go
from utils.security import get_level

ZONES = [
    {"name": "🔒 Secret Keepers",      "desc": "Learn what cryptography is",               "x": 1,    "y": 4,   "xp_required": 0,   "grade": "K-5"},
    {"name": "🎨 Color Key Island",     "desc": "Master the color mixing key exchange",      "x": 2.5,  "y": 5,   "xp_required": 10,  "grade": "K-5"},
    {"name": "🔑 Lock Puzzle Fortress", "desc": "Identify quantum-safe locks",               "x": 4,    "y": 4.5, "xp_required": 25,  "grade": "6-8"},
    {"name": "🏗️ Lattice Maze",         "desc": "Navigate the LWE grid",                    "x": 5.5,  "y": 6,   "xp_required": 50,  "grade": "6-8"},
    {"name": "🏭 Hash Factory",          "desc": "Build SHA-3 hashes",                       "x": 7,    "y": 5,   "xp_required": 75,  "grade": "6-8"},
    {"name": "⚡ Quantum Race Track",   "desc": "Race RSA vs Kyber",                         "x": 8.5,  "y": 6.5, "xp_required": 100, "grade": "9-12"},
    {"name": "📅 NIST Tower",           "desc": "Climb the NIST timeline",                  "x": 10,   "y": 5.5, "xp_required": 150, "grade": "9-12"},
    {"name": "🛡️ Cipher Corps HQ",      "desc": "Master threat modeling and Kyber code",    "x": 11.5, "y": 7,   "xp_required": 300, "grade": "9-12"},
    {"name": "🌐 Quantum Guardian Peak","desc": "Ultimate challenge",                        "x": 13,   "y": 6,   "xp_required": 500, "grade": "Elite"},
]


def render_mission_map():
    st.title("🗺️ Mission World Map")
    xp = st.session_state.xp
    level = get_level(xp)

    st.markdown(f"**{level}** — {xp} XP earned. Unlock new zones by earning more XP!")

    fig = go.Figure()

    path_x = [z["x"] for z in ZONES]
    path_y = [z["y"] for z in ZONES]
    fig.add_trace(go.Scatter(
        x=path_x, y=path_y,
        mode="lines",
        line=dict(color="#e5e7eb", width=3, dash="dot"),
        showlegend=False,
        hoverinfo="skip",
    ))

    for zone in ZONES:
        unlocked = xp >= zone["xp_required"]
        color  = "#10b981" if unlocked else "#9ca3af"
        symbol = "star"    if unlocked else "circle"
        size   = 22        if unlocked else 16
        label  = zone["name"] if unlocked else "🔒 " + str(zone["xp_required"]) + " XP"
        status = "UNLOCKED" if unlocked else "Locked"

        fig.add_trace(go.Scatter(
            x=[zone["x"]], y=[zone["y"]],
            mode="markers+text",
            marker=dict(size=size, color=color, symbol=symbol,
                        line=dict(color="white", width=2)),
            text=[label],
            textposition="top center",
            textfont=dict(size=9, color="#374151"),
            name=zone["name"],
            hovertemplate=(
                "<b>" + zone["name"] + "</b><br>" +
                zone["desc"] + "<br>" +
                "Grade: " + zone["grade"] + "<br>" +
                "XP Required: " + str(zone["xp_required"]) + "<br>" +
                status +
                "<extra></extra>"
            ),
        ))

    fig.update_layout(
        height=500,
        showlegend=False,
        plot_bgcolor="rgba(15, 23, 42, 0.95)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 14]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[3, 8.5]),
        margin=dict(l=10, r=10, t=20, b=10),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Zone Progress")
    unlocked_count = sum(1 for z in ZONES if xp >= z["xp_required"])
    st.progress(unlocked_count / len(ZONES))
    st.caption(f"{unlocked_count} of {len(ZONES)} zones unlocked")

    st.markdown("---")
    for zone in ZONES:
        unlocked = xp >= zone["xp_required"]
        col1, col2, col3 = st.columns([0.5, 3.5, 2])
        with col1:
            st.markdown("✅" if unlocked else "🔒")
        with col2:
            st.markdown(
                f"**{zone['name']}**  \n"
                f"<span style='font-size:12px;color:#6b7280'>{zone['desc']}</span>",
                unsafe_allow_html=True
            )
        with col3:
            if unlocked:
                st.success("Unlocked!", icon="🎉")
            else:
                needed = zone["xp_required"] - xp
                st.caption(f"Need {needed} more XP")
