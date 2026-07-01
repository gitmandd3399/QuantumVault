"""
modules/world_map.py
─────────────────────
Interactive world map for navigating QuantumVault Academy.
Students click zones to enter modules.
"""

import streamlit as st
import streamlit.components.v1 as components


def render_world_map():
    st.title("🌍 QuantumVault World Map")
    st.markdown(
        "Click a zone to enter! Complete activities to unlock new areas. "
        "Your XP unlocks higher zones."
    )

    xp = st.session_state.get("xp", 0)

    st.iframe(f"""
<!DOCTYPE html>
<html>
<head>
<style>
* {{ margin:0;padding:0;box-sizing:border-box; }}
body {{ background:#0f172a;font-family:sans-serif;color:white;padding:10px; }}
.map-wrap {{ max-width:700px;margin:0 auto;position:relative; }}
.map-title {{ text-align:center;font-size:13px;color:#6b7280;margin-bottom:12px; }}
.map-canvas {{ position:relative;width:100%;background:linear-gradient(180deg,#0c0a1e,#0f172a);
    border:2px solid #4f46e5;border-radius:16px;overflow:hidden; }}
svg {{ width:100%;height:auto; }}
.zone {{ cursor:pointer;transition:all 0.2s; }}
.zone:hover {{ filter:brightness(1.3); }}
.zone.locked {{ cursor:not-allowed;filter:grayscale(0.8); }}
.tooltip {{ position:absolute;background:rgba(15,23,42,0.95);border:1px solid #4f46e5;
    border-radius:10px;padding:10px 14px;font-size:12px;pointer-events:none;
    display:none;z-index:100;max-width:180px; }}
.tooltip h4 {{ color:#a5b4fc;margin-bottom:4px;font-size:13px; }}
.tooltip p {{ color:#888;font-size:11px;margin:2px 0; }}
.tooltip .xp-req {{ color:#10b981;font-weight:bold;margin-top:4px; }}
.btn-enter {{ display:block;width:100%;padding:8px;border-radius:8px;border:none;
    cursor:pointer;font-size:12px;font-weight:bold;margin-top:6px;
    background:#4f46e5;color:white; }}
.hud {{ display:flex;justify-content:space-between;padding:8px 12px;
    background:rgba(79,70,229,0.1);border-top:1px solid #334155;
    font-size:12px;color:#a5b4fc; }}
</style>
</head>
<body>
<div class="map-wrap">
<div class="map-title">Your XP: ⭐ {xp} — Click a zone to explore!</div>
<div class="map-canvas">
<svg viewBox="0 0 700 500" xmlns="http://www.w3.org/2000/svg">
    <!-- Stars background -->
    <rect width="700" height="500" fill="#0c0a1e"/>
    {''.join([f'<circle cx="{(i*137)%700}" cy="{(i*97)%500}" r="{0.5 + (i%3)*0.5}" fill="white" opacity="{0.3 + (i%5)*0.1}"/>' for i in range(80)])}

    <!-- Space station grid lines -->
    <line x1="0" y1="250" x2="700" y2="250" stroke="#4f46e5" stroke-opacity="0.1" stroke-width="1"/>
    <line x1="350" y1="0" x2="350" y2="500" stroke="#4f46e5" stroke-opacity="0.1" stroke-width="1"/>

    <!-- Zone 1: Elementary Forest -->
    <g class="zone" id="zone-elementary" onclick="enterZone('elementary')">
        <ellipse cx="150" cy="380" rx="130" ry="85" fill="#10b981" opacity="0.2"/>
        <ellipse cx="150" cy="380" rx="130" ry="85" fill="none" stroke="#10b981" stroke-width="2" stroke-dasharray="5,3"/>
        <!-- Trees -->
        <text x="90" y="360" font-size="28">🌲</text>
        <text x="140" y="345" font-size="24">🌳</text>
        <text x="185" y="358" font-size="26">🌲</text>
        <text x="115" y="400" font-size="20">🏡</text>
        <text x="160" y="405" font-size="18">🔐</text>
        <!-- Zone label -->
        <rect x="85" y="415" width="135" height="28" rx="8" fill="#10b981" opacity="0.9"/>
        <text x="152" y="433" text-anchor="middle" font-size="12" font-weight="bold" fill="white">🟢 Elementary K-5</text>
    </g>

    <!-- Zone 2: Middle School City -->
    <g class="zone" id="zone-middle" onclick="enterZone('middle')">
        <ellipse cx="530" cy="350" rx="140" ry="90" fill="#7c6dfa" opacity="0.2"/>
        <ellipse cx="530" cy="350" rx="140" ry="90" fill="none" stroke="#7c6dfa" stroke-width="2" stroke-dasharray="5,3"/>
        <!-- Buildings -->
        <text x="460" y="340" font-size="26">🏗️</text>
        <text x="510" y="325" font-size="24">🏢</text>
        <text x="558" y="338" font-size="22">🔬</text>
        <text x="495" y="375" font-size="20">💻</text>
        <text x="545" y="378" font-size="18">🧮</text>
        <!-- Zone label -->
        <rect x="450" y="398" width="162" height="28" rx="8" fill="#7c6dfa" opacity="0.9"/>
        <text x="531" y="416" text-anchor="middle" font-size="12" font-weight="bold" fill="white">🟡 Middle School 6-8</text>
    </g>

    <!-- Zone 3: High School Space Station -->
    <g class="zone {'locked' if xp < 50 else ''}" id="zone-high" onclick="enterZone('high')">
        <ellipse cx="350" cy="150" rx="150" ry="100" fill="#f45c5c" opacity="{'0.15' if xp < 50 else '0.2'}"/>
        <ellipse cx="350" cy="150" rx="150" ry="100" fill="none" stroke="#f45c5c" stroke-width="2" stroke-dasharray="5,3"/>
        <!-- Space elements -->
        <text x="270" y="140" font-size="26">🚀</text>
        <text x="320" y="120" font-size="24">🛸</text>
        <text x="375" y="132" font-size="22">⚛️</text>
        <text x="300" y="175" font-size="20">🔭</text>
        <text x="360" y="178" font-size="18">🛡️</text>
        {"<text x='350' y='155' text-anchor='middle' font-size='28' opacity='0.5'>🔒</text>" if xp < 50 else ""}
        <!-- Zone label -->
        <rect x="255" y="195" width="190" height="28" rx="8" fill="#f45c5c" opacity="{'0.5' if xp < 50 else '0.9'}"/>
        <text x="350" y="213" text-anchor="middle" font-size="12" font-weight="bold" fill="white">
            {"🔒 High School (50 XP)" if xp < 50 else "🔴 High School 9-12"}
        </text>
    </g>

    <!-- Zone 4: Leaderboard Arena -->
    <g class="zone" id="zone-leaderboard" onclick="enterZone('leaderboard')">
        <ellipse cx="150" cy="160" rx="110" ry="75" fill="#f59e0b" opacity="0.2"/>
        <ellipse cx="150" cy="160" rx="110" ry="75" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="5,3"/>
        <text x="100" y="150" font-size="26">🏆</text>
        <text x="148" y="140" font-size="22">⭐</text>
        <text x="185" y="152" font-size="20">🥇</text>
        <text x="125" y="185" font-size="18">📊</text>
        <rect x="68" y="192" width="165" height="26" rx="8" fill="#f59e0b" opacity="0.9"/>
        <text x="150" y="209" text-anchor="middle" font-size="11" font-weight="bold" fill="white">🏆 Leaderboard Arena</text>
    </g>

    <!-- Zone 5: AI Tutor Tower -->
    <g class="zone" id="zone-tutor" onclick="enterZone('tutor')">
        <ellipse cx="550" cy="160" rx="110" ry="75" fill="#3b82f6" opacity="0.2"/>
        <ellipse cx="550" cy="160" rx="110" ry="75" fill="none" stroke="#3b82f6" stroke-width="2" stroke-dasharray="5,3"/>
        <text x="500" y="148" font-size="26">🤖</text>
        <text x="548" y="135" font-size="22">💬</text>
        <text x="590" y="148" font-size="20">🧠</text>
        <text x="525" y="182" font-size="18">✨</text>
        <rect x="468" y="192" width="165" height="26" rx="8" fill="#3b82f6" opacity="0.9"/>
        <text x="550" y="209" text-anchor="middle" font-size="11" font-weight="bold" fill="white">🤖 AI Tutor Tower</text>
    </g>

    <!-- Zone 6: Card Collection -->
    <g class="zone" id="zone-cards" onclick="enterZone('cards')">
        <ellipse cx="350" cy="430" rx="100" ry="55" fill="#ec4899" opacity="0.2"/>
        <ellipse cx="350" cy="430" rx="100" ry="55" fill="none" stroke="#ec4899" stroke-width="2" stroke-dasharray="5,3"/>
        <text x="310" y="425" font-size="22">🃏</text>
        <text x="348" y="418" font-size="20">✨</text>
        <text x="385" y="425" font-size="20">🎴</text>
        <rect x="270" y="445" width="160" height="26" rx="8" fill="#ec4899" opacity="0.9"/>
        <text x="350" y="462" text-anchor="middle" font-size="11" font-weight="bold" fill="white">🃏 Card Collection</text>
    </g>

    <!-- Connecting paths -->
    <path d="M 150 295 Q 250 220 350 250" stroke="#4f46e5" stroke-width="1.5" fill="none" stroke-opacity="0.4" stroke-dasharray="6,4"/>
    <path d="M 350 250 Q 440 290 530 260" stroke="#4f46e5" stroke-width="1.5" fill="none" stroke-opacity="0.4" stroke-dasharray="6,4"/>
    <path d="M 350 250 Q 350 200 350 200" stroke="#f45c5c" stroke-width="1.5" fill="none" stroke-opacity="0.4" stroke-dasharray="6,4"/>
    <path d="M 150 295 Q 150 230 150 235" stroke="#f59e0b" stroke-width="1.5" fill="none" stroke-opacity="0.4" stroke-dasharray="6,4"/>
    <path d="M 530 260 Q 542 215 550 235" stroke="#3b82f6" stroke-width="1.5" fill="none" stroke-opacity="0.4" stroke-dasharray="6,4"/>

    <!-- Player marker -->
    <g id="player-marker">
        <circle cx="150" cy="340" r="12" fill="#10b981" opacity="0.3">
            <animate attributeName="r" values="10;14;10" dur="2s" repeatCount="indefinite"/>
        </circle>
        <text x="150" y="345" text-anchor="middle" font-size="16">🕵️</text>
    </g>
</svg>
</div>
<div class="hud">
    <span>⭐ {xp} XP</span>
    <span>🗺️ Click any zone to explore!</span>
    <span>🔥 Keep learning!</span>
</div>
</div>

<div class="tooltip" id="tooltip"></div>

<script>
const ZONES = {{
    elementary:  {{name:"Elementary K-5",  desc:"Story time, games, puzzles!", xp:0,   color:"#10b981", nav:"🟢 Elementary (K–5)"}},
    middle:      {{name:"Middle School 6-8",desc:"Lattice math, hashing, keys!", xp:0,  color:"#7c6dfa", nav:"🟡 Middle School (6–8)"}},
    high:        {{name:"High School 9-12", desc:"Advanced PQC and math!",       xp:50,  color:"#f45c5c", nav:"🔴 High School (9–12)"}},
    leaderboard: {{name:"Leaderboard Arena",desc:"Compete with classmates!",     xp:0,   color:"#f59e0b", nav:"🏆 Leaderboard"}},
    tutor:       {{name:"AI Tutor Tower",   desc:"Ask any PQC question!",        xp:0,   color:"#3b82f6", nav:"🤖 AI Tutor"}},
    cards:       {{name:"Card Collection",  desc:"Collect all 12 PQC cards!",    xp:0,   color:"#ec4899", nav:"🃏 Trading Cards"}},
}};

const userXP = {xp};

function enterZone(zone) {{
    const z = ZONES[zone];
    if (!z) return;
    if (userXP < z.xp) {{
        alert("🔒 Need " + z.xp + " XP to enter " + z.name + "! Keep learning!");
        return;
    }}
    // Send message to parent Streamlit
    window.parent.postMessage({{type:"streamlit:setComponentValue", value:z.nav}}, "*");
}}

// Animate player to clicked zone
document.querySelectorAll('.zone').forEach(zone => {{
    zone.addEventListener('mouseenter', function(e) {{
        const id = this.id.replace('zone-', '');
        const z = ZONES[id];
        if (!z) return;
        const tooltip = document.getElementById('tooltip');
        tooltip.style.display = 'block';
        tooltip.innerHTML = '<h4>' + z.name + '</h4><p>' + z.desc + '</p>' +
            '<p class="xp-req">' + (z.xp > 0 ? '🔒 Requires ' + z.xp + ' XP' : '✅ Unlocked!') + '</p>';
        tooltip.style.left = (e.offsetX + 10) + 'px';
        tooltip.style.top = (e.offsetY + 10) + 'px';
    }});
    zone.addEventListener('mouseleave', function() {{
        document.getElementById('tooltip').style.display = 'none';
    }});
}});
</script>
</body>
</html>
""", height=580)

    st.markdown("---")
    st.markdown("### 🗺️ Navigate Directly")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🟢 Elementary", use_container_width=True):
            st.session_state.level = "🟢 Elementary (K–5)"
            st.rerun()
        if st.button("🏆 Leaderboard", use_container_width=True):
            st.session_state.level = "🏆 Leaderboard"
            st.rerun()

    with col2:
        if st.button("🟡 Middle School", use_container_width=True):
            st.session_state.level = "🟡 Middle School (6–8)"
            st.rerun()
        if st.button("🤖 AI Tutor", use_container_width=True):
            st.session_state.level = "🤖 AI Tutor"
            st.rerun()

    with col3:
        if xp >= 50:
            if st.button("🔴 High School", use_container_width=True):
                st.session_state.level = "🔴 High School (9–12)"
                st.rerun()
        else:
            st.button(f"🔒 High School ({50-xp} XP needed)", use_container_width=True, disabled=True)
        if st.button("🃏 Trading Cards", use_container_width=True):
            st.session_state.level = "🃏 Trading Cards"
            st.rerun()
