"""
modules/trading_cards.py
─────────────────────────
PQC Trading Card collection system.
Students earn cards by completing activities.
"""

import streamlit as st
import streamlit.components.v1 as components

CARDS = [
    {
        "id": "kyber",
        "name": "Kyber Crystal",
        "algo": "ML-KEM FIPS 203",
        "rarity": "Legendary",
        "rarity_color": "#f59e0b",
        "color": "#10b981",
        "emoji": "🔐",
        "type": "Key Encapsulation",
        "power": 95,
        "speed": 88,
        "security": 99,
        "size": 82,
        "lore": "Born from the depths of lattice mathematics, Kyber Crystal protects the world's secrets from quantum attackers. NIST chose this warrior in 2024.",
        "unlock": "Complete the Lock Puzzle in Elementary",
        "unlock_key": "lock_puzzle",
    },
    {
        "id": "dilithium",
        "name": "Dilithium Shield",
        "algo": "ML-DSA FIPS 204",
        "rarity": "Legendary",
        "rarity_color": "#f59e0b",
        "color": "#3b82f6",
        "emoji": "✍️",
        "type": "Digital Signature",
        "power": 92,
        "speed": 85,
        "security": 98,
        "size": 78,
        "lore": "Named after the Star Trek crystal, Dilithium Shield forges unbreakable signatures. No quantum force can forge its seal.",
        "unlock": "Complete the Key Workshop in Middle School",
        "unlock_key": "kyber_workshop",
    },
    {
        "id": "sphincs",
        "name": "SPHINCS Guardian",
        "algo": "SLH-DSA FIPS 205",
        "rarity": "Rare",
        "rarity_color": "#8b5cf6",
        "color": "#8b5cf6",
        "emoji": "🌲",
        "type": "Hash Signature",
        "power": 88,
        "speed": 72,
        "security": 99,
        "size": 65,
        "lore": "The ancient guardian of hash forests. SPHINCS+ stands firm even if lattice math ever falls. The ultimate backup defender.",
        "unlock": "Complete the Hash Factory in Middle School",
        "unlock_key": "hash_factory",
    },
    {
        "id": "falcon",
        "name": "Falcon Strike",
        "algo": "FN-DSA FIPS 206",
        "rarity": "Rare",
        "rarity_color": "#8b5cf6",
        "color": "#f59e0b",
        "emoji": "🦅",
        "type": "Compact Signature",
        "power": 85,
        "speed": 96,
        "security": 95,
        "size": 99,
        "lore": "Swift as a falcon, this NTRU lattice warrior produces the smallest quantum-safe signatures. Perfect for devices with limited storage.",
        "unlock": "Reach Level 3 in the Lattice Maze",
        "unlock_key": "lattice_challenge",
    },
    {
        "id": "shor",
        "name": "Shor Breaker",
        "algo": "Quantum Threat",
        "rarity": "Rare",
        "rarity_color": "#8b5cf6",
        "color": "#ef4444",
        "emoji": "⚛️",
        "type": "Quantum Algorithm",
        "power": 99,
        "speed": 99,
        "security": 0,
        "size": 50,
        "lore": "The quantum destroyer that breaks RSA. Peter Shor created this algorithm in 1994. It factors large numbers exponentially faster.",
        "unlock": "Complete the Quantum Race in Middle School",
        "unlock_key": "quantum_race",
    },
    {
        "id": "lattice",
        "name": "Lattice Fortress",
        "algo": "LWE Problem",
        "rarity": "Common",
        "rarity_color": "#6b7280",
        "color": "#06b6d4",
        "emoji": "🏗️",
        "type": "Math Foundation",
        "power": 90,
        "speed": 80,
        "security": 97,
        "size": 75,
        "lore": "The mathematical fortress that stumps quantum computers. Finding the shortest vector in 1000 dimensions is computationally infeasible.",
        "unlock": "Use the Lattice Explorer in Middle School",
        "unlock_key": "lattice_visualizer",
    },
    {
        "id": "sha3",
        "name": "SHA-3 Phantom",
        "algo": "SHA-3 / Keccak",
        "rarity": "Common",
        "rarity_color": "#6b7280",
        "color": "#ec4899",
        "emoji": "🔢",
        "type": "Hash Function",
        "power": 80,
        "speed": 92,
        "security": 94,
        "size": 88,
        "lore": "The phantom fingerprinter. SHA-3 transforms any message into a unique 256-bit fingerprint. Change one letter and everything changes.",
        "unlock": "Discover the Avalanche Effect in Middle School",
        "unlock_key": "hash_avalanche",
    },
    {
        "id": "nist",
        "name": "NIST Arbiter",
        "algo": "Standards Body",
        "rarity": "Common",
        "rarity_color": "#6b7280",
        "color": "#374151",
        "emoji": "🏛️",
        "type": "Organization",
        "power": 70,
        "speed": 60,
        "security": 100,
        "size": 70,
        "lore": "The ultimate arbiter of cryptographic trust. NIST ran a 6-year competition selecting the four PQC standards that protect humanity.",
        "unlock": "Study the NIST Timeline in High School",
        "unlock_key": "nist_timeline",
    },
    {
        "id": "lwe",
        "name": "LWE Crystal",
        "algo": "Learning With Errors",
        "rarity": "Legendary",
        "rarity_color": "#f59e0b",
        "color": "#ec4899",
        "emoji": "🧮",
        "type": "Hard Problem",
        "power": 88,
        "speed": 75,
        "security": 99,
        "size": 80,
        "lore": "The hardest math problem in post-quantum cryptography. Given a noisy equation, find the secret. Even quantum computers fail.",
        "unlock": "Complete the LWE Code Lab in High School",
        "unlock_key": "lwe_code_lab",
    },
    {
        "id": "grover",
        "name": "Grover Speedster",
        "algo": "Grover Algorithm",
        "rarity": "Common",
        "rarity_color": "#6b7280",
        "color": "#f97316",
        "emoji": "🌀",
        "type": "Quantum Algorithm",
        "power": 75,
        "speed": 99,
        "security": 0,
        "size": 60,
        "lore": "The quantum speedster that searches N items in sqrt(N) steps. Dangerous against hashes but defeated by doubling key sizes.",
        "unlock": "Complete the Algorithm Lab in High School",
        "unlock_key": "algorithm_lab",
    },
    {
        "id": "rsa",
        "name": "RSA Relic",
        "algo": "RSA (Broken)",
        "rarity": "Common",
        "rarity_color": "#6b7280",
        "color": "#6b7280",
        "emoji": "💀",
        "type": "Classical Crypto",
        "power": 60,
        "speed": 70,
        "security": 10,
        "size": 30,
        "lore": "Once the king of cryptography. RSA protected the internet for 45 years. Now vulnerable to Shor Algorithm on quantum computers.",
        "unlock": "Read the Agent Pixel story in Elementary",
        "unlock_key": "story_read",
    },
    {
        "id": "guardian",
        "name": "Quantum Guardian",
        "algo": "Ultimate Defender",
        "rarity": "Legendary",
        "rarity_color": "#f59e0b",
        "color": "#4f46e5",
        "emoji": "🛡️",
        "type": "Master Card",
        "power": 100,
        "speed": 100,
        "security": 100,
        "size": 100,
        "lore": "The ultimate defender of the quantum age. Earned only by those who master all four NIST PQC standards. You are the last line of defense.",
        "unlock": "Earn 500 XP and complete all modules",
        "unlock_key": "quantum_guardian",
    },
]


def is_card_unlocked(card: dict) -> bool:
    completed = st.session_state.get("completed_activities", set())
    xp = st.session_state.get("xp", 0)
    if card["unlock_key"] == "quantum_guardian":
        return xp >= 500
    return card["unlock_key"] in completed


def render_trading_cards():
    st.title("🃏 PQC Trading Card Collection")
    st.markdown(
        "Collect all 12 post-quantum cryptography trading cards! "
        "Complete activities to unlock new cards."
    )

    completed = st.session_state.get("completed_activities", set())
    xp = st.session_state.get("xp", 0)
    unlocked = sum(1 for c in CARDS if is_card_unlocked(c))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🃏 Cards Collected", f"{unlocked}/12")
    with col2:
        st.metric("⭐ Your XP", xp)
    with col3:
        legendary = sum(1 for c in CARDS if c["rarity"]=="Legendary" and is_card_unlocked(c))
        st.metric("✨ Legendary Cards", f"{legendary}/4")

    st.markdown("---")

    # Filter tabs
    filter_tab1, filter_tab2, filter_tab3, filter_tab4 = st.tabs([
        "🃏 All Cards", "✨ Legendary", "💜 Rare", "⚪ Common"
    ])

    def render_cards(cards_to_show):
        cols = st.columns(3)
        for i, card in enumerate(cards_to_show):
            with cols[i % 3]:
                unlocked_card = is_card_unlocked(card)
                render_card(card, unlocked_card)

    def render_card(card, unlocked_card):
        color = card["color"] if unlocked_card else "#374151"
        rarity_color = card["rarity_color"] if unlocked_card else "#6b7280"
        opacity = "1" if unlocked_card else "0.4"

        components.html(f"""
<style>
.card {{
    background: linear-gradient(135deg, {color}22, {color}08);
    border: 2px solid {color}{"60" if unlocked_card else "20"};
    border-radius: 16px;
    padding: 16px;
    margin: 6px 0;
    opacity: {opacity};
    font-family: sans-serif;
    color: white;
    position: relative;
    overflow: hidden;
}}
.card::before {{
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, {color}15 0%, transparent 70%);
    pointer-events: none;
}}
.rarity {{
    font-size: 9px;
    font-weight: bold;
    color: {rarity_color};
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}}
.card-emoji {{
    font-size: 2.5rem;
    margin: 6px 0;
    display: block;
}}
.card-name {{
    font-size: 15px;
    font-weight: bold;
    color: white;
    margin: 4px 0 2px;
}}
.card-algo {{
    font-size: 9px;
    color: {color};
    font-weight: bold;
    margin-bottom: 6px;
    letter-spacing: 1px;
}}
.card-type {{
    display: inline-block;
    background: {color}30;
    border: 1px solid {color}50;
    border-radius: 100px;
    padding: 2px 8px;
    font-size: 9px;
    color: {color};
    margin-bottom: 8px;
}}
.stats {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px;
    margin: 6px 0;
}}
.stat {{
    font-size: 9px;
    color: #888;
}}
.stat-bar {{
    height: 4px;
    background: #1e293b;
    border-radius: 2px;
    overflow: hidden;
    margin-top: 2px;
}}
.stat-fill {{
    height: 100%;
    border-radius: 2px;
    background: {color};
}}
.lore {{
    font-size: 9px;
    color: #888;
    line-height: 1.4;
    margin: 6px 0;
    font-style: italic;
}}
.unlock-info {{
    font-size: 8px;
    color: {"#10b981" if unlocked_card else "#6b7280"};
    margin-top: 6px;
    padding-top: 6px;
    border-top: 1px solid #334155;
}}
.locked-overlay {{
    font-size: 2rem;
    text-align: center;
    margin: 8px 0;
}}
</style>
<div class="card">
    <div class="rarity">{"★ " if card["rarity"]=="Legendary" else "◆ " if card["rarity"]=="Rare" else "• "}{card["rarity"]}</div>
    <div class="card-emoji">{card["emoji"] if unlocked_card else "🔒"}</div>
    <div class="card-name">{card["name"] if unlocked_card else "???"}</div>
    <div class="card-algo">{card["algo"] if unlocked_card else "LOCKED"}</div>
    <div class="card-type">{card["type"] if unlocked_card else "???"}</div>
    {"" if not unlocked_card else f'''
    <div class="stats">
        <div class="stat">⚔️ Power: {card["power"]}
            <div class="stat-bar"><div class="stat-fill" style="width:{card["power"]}%"></div></div>
        </div>
        <div class="stat">⚡ Speed: {card["speed"]}
            <div class="stat-bar"><div class="stat-fill" style="width:{card["speed"]}%"></div></div>
        </div>
        <div class="stat">🛡️ Security: {card["security"]}
            <div class="stat-bar"><div class="stat-fill" style="width:{card["security"]}%"></div></div>
        </div>
        <div class="stat">📦 Size: {card["size"]}
            <div class="stat-bar"><div class="stat-fill" style="width:{card["size"]}%"></div></div>
        </div>
    </div>
    <div class="lore">{card["lore"]}</div>
    '''}
    <div class="unlock-info">
        {"✅ UNLOCKED" if unlocked_card else "🔒 Unlock: " + card["unlock"]}
    </div>
</div>
""", height=380 if unlocked_card else 220, scrolling=True)

    with filter_tab1:
        render_cards(CARDS)
    with filter_tab2:
        render_cards([c for c in CARDS if c["rarity"] == "Legendary"])
    with filter_tab3:
        render_cards([c for c in CARDS if c["rarity"] == "Rare"])
    with filter_tab4:
        render_cards([c for c in CARDS if c["rarity"] == "Common"])

    st.markdown("---")
    st.markdown("### 🎯 How to Unlock All Cards")
    for card in CARDS:
        unlocked_card = is_card_unlocked(card)
        status = "✅" if unlocked_card else "🔒"
        st.markdown(
            f"{status} **{card['name']}** ({card['rarity']}) — {card['unlock']}"
        )
