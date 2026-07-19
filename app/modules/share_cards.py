"""
modules/share_cards.py
───────────────────────
Generate shareable achievement cards for students.
Students can download and share their accomplishments.
"""

import streamlit as st
import streamlit.components.v1 as components
from utils.security import get_level


def render_share_card(badge: str, xp: int, level: str, streak: int):
    """Render a single shareable achievement card."""
    components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
* {{ margin:0;padding:0;box-sizing:border-box; }}
body {{ background:#0f172a;display:flex;justify-content:center;
    padding:10px;font-family:sans-serif; }}
.card {{
    width:400px;
    background:linear-gradient(135deg,#1e1b4b,#0f172a);
    border:2px solid #4f46e5;
    border-radius:20px;
    padding:24px;
    position:relative;
    overflow:hidden;
}}
.card::before {{
    content:'';position:absolute;top:-60px;right:-60px;
    width:200px;height:200px;
    background:radial-gradient(circle,rgba(79,70,229,0.3),transparent);
    border-radius:50%;
}}
.card::after {{
    content:'';position:absolute;bottom:-60px;left:-60px;
    width:200px;height:200px;
    background:radial-gradient(circle,rgba(16,185,129,0.2),transparent);
    border-radius:50%;
}}
.logo {{ font-size:11px;color:#6b7280;letter-spacing:3px;
    text-transform:uppercase;margin-bottom:16px; }}
.badge-emoji {{ font-size:3.5rem;margin:8px 0;display:block; }}
.badge-name {{ font-size:1.3rem;font-weight:bold;color:white;margin:6px 0; }}
.level {{ font-size:0.85rem;color:#a5b4fc;margin-bottom:16px; }}
.divider {{ height:1px;background:linear-gradient(to right,transparent,#4f46e5,transparent);
    margin:12px 0; }}
.stats {{ display:flex;justify-content:space-around;margin:12px 0; }}
.stat {{ text-align:center; }}
.stat-val {{ font-size:1.6rem;font-weight:bold;color:#10b981; }}
.stat-label {{ font-size:0.7rem;color:#6b7280;text-transform:uppercase;letter-spacing:1px; }}
.streak {{ display:flex;align-items:center;justify-content:center;gap:6px;
    margin:10px 0;font-size:0.85rem;color:#f59e0b; }}
.footer {{ font-size:0.7rem;color:#4b5563;margin-top:14px;text-align:center; }}
.download-btn {{ width:100%;padding:10px;border-radius:10px;border:none;
    cursor:pointer;background:#4f46e5;color:white;font-size:13px;
    font-weight:bold;margin-top:12px;display:block; }}
.download-btn:hover {{ background:#6d60ff; }}
</style>
</head>
<body>
<div>
<div class="card" id="shareCard">
    <div class="logo">🔐 QuantumVault Academy</div>
    <div class="badge-emoji">{badge.split()[0] if badge else "🏅"}</div>
    <div class="badge-name">{badge}</div>
    <div class="level">Rank: {level}</div>
    <div class="divider"></div>
    <div class="stats">
        <div class="stat">
            <div class="stat-val">{xp}</div>
            <div class="stat-label">Total XP</div>
        </div>
        <div class="stat">
            <div class="stat-val">{streak}</div>
            <div class="stat-label">Day Streak</div>
        </div>
    </div>
    <div class="streak">🔥 {streak} Day Learning Streak!</div>
    <div class="divider"></div>
    <div class="footer">
        I am learning post-quantum cryptography at QuantumVault Academy!
        NIST FIPS 203 · 204 · 205 · 206
    </div>
</div>
<button class="download-btn" onclick="downloadCard()">
    📥 Download Achievement Card
</button>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script>
function downloadCard() {{
    const card = document.getElementById("shareCard");
    html2canvas(card, {{
        backgroundColor: "#0f172a",
        scale: 2,
        useCORS: true
    }}).then(canvas => {{
        const link = document.createElement("a");
        link.download = "QuantumVault_Achievement.png";
        link.href = canvas.toDataURL("image/png");
        link.click();
    }});
}}
</script>
</body>
</html>
""", height=480, scrolling=True)


def render_share_page():
    st.title("📸 Share Your Achievement")
    st.markdown(
        "Generate a shareable achievement card to show off your PQC learning progress! "
        "Download and share with friends, parents, or teachers."
    )

    xp = st.session_state.get("xp", 0)
    badges = st.session_state.get("badges", [])
    streak = st.session_state.get("streak_days", 1)
    level = get_level(xp)

    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🎨 Customize Your Card")

        selected_badge = st.selectbox(
            "Choose a badge to feature:",
            badges if badges else ["🏅 Just Getting Started"],
            key="share_badge_select"
        )

        st.markdown("**Your Stats:**")
        st.metric("⭐ Total XP", xp)
        st.metric("🏅 Rank", level)
        st.metric("🔥 Day Streak", streak)
        st.metric("🏅 Badges Earned", len(badges))

        if not badges:
            st.info(
                "Complete activities to earn badges first! "
                "Try the Lock Puzzle in Elementary."
            )

    with col2:
        st.markdown("### 👀 Preview")
        render_share_card(selected_badge, xp, level, streak)

    st.markdown("---")

    # Text share option
    st.markdown("### 📋 Copy Text Version")
    share_text = (
        f"🔐 I just earned '{selected_badge}' in QuantumVault Academy! "
        f"I have {xp} XP, reached {level} rank, and have a {streak}-day learning streak. "
        f"Learning post-quantum cryptography — the math that will protect the internet from quantum computers! "
        f"#QuantumVault #PQC #Cybersecurity #STEM"
    )

    st.code(share_text, language=None)
    st.caption("Copy this text to share on social media!")

    st.markdown("---")

    # All badges gallery
    if badges:
        st.markdown("### 🏅 All Your Badges")
        badge_cols = st.columns(4)
        for i, badge in enumerate(badges):
            with badge_cols[i % 4]:
                st.markdown(
                    f"<div style='background:rgba(79,70,229,0.1);"
                    f"border:1px solid rgba(79,70,229,0.3);"
                    f"border-radius:10px;padding:10px;text-align:center;"
                    f"margin:4px;font-size:0.85rem;'>{badge}</div>",
                    unsafe_allow_html=True
                )
