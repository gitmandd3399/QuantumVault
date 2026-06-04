"""
modules/algo_battle.py
Algorithm Battle Card Game — PQC cards vs Quantum Monster cards.
"""
import streamlit as st
import random
import streamlit.components.v1 as components


PLAYER_CARDS = [
    {"name":"Kyber Crystal","emoji":"🔐","type":"KEM","power":95,"defense":90,"color":"#10b981",
     "special":"Lattice Shield: Immune to quantum attacks!","fact":"FIPS 203 — Module-LWE"},
    {"name":"Dilithium Shield","emoji":"✍️","type":"Signature","power":88,"defense":92,"color":"#3b82f6",
     "special":"Rejection Sampling: Cannot be forged!","fact":"FIPS 204 — Module-LWE+SIS"},
    {"name":"Falcon Strike","emoji":"🦅","type":"Compact","power":85,"defense":88,"color":"#f59e0b",
     "special":"NTRU Lattice: Smallest signature!","fact":"FIPS 206 — NTRU lattices"},
    {"name":"SPHINCS Guardian","emoji":"🌲","type":"Hash","power":80,"defense":99,"color":"#8b5cf6",
     "special":"Hash Fortress: Survives if lattices fall!","fact":"FIPS 205 — SHA-3 based"},
    {"name":"SHA-3 Phantom","emoji":"🔢","type":"Hash","power":75,"defense":95,"color":"#ec4899",
     "special":"Avalanche Effect: Unhashable!","fact":"256-bit quantum security"},
    {"name":"AES-256 Tank","emoji":"🛡️","type":"Symmetric","power":90,"defense":85,"color":"#06b6d4",
     "special":"Grover Resistant: 128-bit quantum safe!","fact":"Still secure against Grover"},
]

ENEMY_CARDS = [
    {"name":"Shor Algorithm","emoji":"⚛️","power":99,"weakness":"Lattice","color":"#ef4444",
     "attack":"Quantum Factoring! Breaks RSA instantly!"},
    {"name":"Grover Speeder","emoji":"🌀","power":70,"weakness":"Large Keys","color":"#f97316",
     "attack":"Search Speedup! Halves key security!"},
    {"name":"Quantum MITM","emoji":"👾","power":75,"weakness":"KEM","color":"#a855f7",
     "attack":"Intercept! Tries to steal the key exchange!"},
    {"name":"Harvest Bot","emoji":"🤖","power":65,"weakness":"PQC","color":"#6b7280",
     "attack":"Collect now, decrypt later! Stores your data!"},
]


def render_algo_battle():
    st.title("🃏 Algorithm Battle Card Game!")
    st.markdown(
        "⚔️ **The Quantum Monster is attacking!** Use your PQC algorithm cards to defend. "
        "Each card has attack and defense stats — pick the right card to counter each threat!"
    )

    if "battle_score" not in st.session_state:
        st.session_state.battle_score = 0
    if "battle_round" not in st.session_state:
        st.session_state.battle_round = 1
    if "battle_hp" not in st.session_state:
        st.session_state.battle_hp = 100
    if "battle_selected" not in st.session_state:
        st.session_state.battle_selected = None
    if "battle_result" not in st.session_state:
        st.session_state.battle_result = None
    if "battle_enemy" not in st.session_state:
        st.session_state.battle_enemy = random.choice(ENEMY_CARDS)

    # HUD
    col1, col2, col3 = st.columns(3)
    with col1:
        hp_color = "#10b981" if st.session_state.battle_hp > 50 else "#f59e0b" if st.session_state.battle_hp > 25 else "#ef4444"
        st.markdown(
            f"<div style='background:{hp_color}15;border:1px solid {hp_color};"
            f"border-radius:8px;padding:8px;text-align:center'>"
            f"<div style='font-size:0.75rem;color:#888'>❤️ HP</div>"
            f"<div style='font-size:1.4rem;font-weight:bold;color:{hp_color}'>{st.session_state.battle_hp}/100</div>"
            f"</div>", unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"<div style='background:#4f46e515;border:1px solid #4f46e5;"
            f"border-radius:8px;padding:8px;text-align:center'>"
            f"<div style='font-size:0.75rem;color:#888'>⭐ Score</div>"
            f"<div style='font-size:1.4rem;font-weight:bold;color:#a5b4fc'>{st.session_state.battle_score}</div>"
            f"</div>", unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"<div style='background:#1e293b;border:1px solid #334155;"
            f"border-radius:8px;padding:8px;text-align:center'>"
            f"<div style='font-size:0.75rem;color:#888'>🌊 Round</div>"
            f"<div style='font-size:1.4rem;font-weight:bold;color:white'>{st.session_state.battle_round}</div>"
            f"</div>", unsafe_allow_html=True
        )

    if st.session_state.battle_hp <= 0:
        st.error(f"💀 GAME OVER! Score: {st.session_state.battle_score}")
        if st.button("🔄 Play Again", key="battle_restart"):
            st.session_state.battle_score = 0
            st.session_state.battle_round = 1
            st.session_state.battle_hp = 100
            st.session_state.battle_result = None
            st.session_state.battle_enemy = random.choice(ENEMY_CARDS)
            st.rerun()
        return

    st.markdown("---")
    enemy = st.session_state.battle_enemy

    st.markdown("### 👾 Enemy Attack!")
    st.markdown(
        f"<div style='background:{enemy['color']}15;border:2px solid {enemy['color']}60;"
        f"border-radius:12px;padding:14px;text-align:center;margin-bottom:12px'>"
        f"<div style='font-size:3rem'>{enemy['emoji']}</div>"
        f"<div style='font-weight:bold;color:{enemy['color']};font-size:1.1rem'>{enemy['name']}</div>"
        f"<div style='color:#ccc;font-size:0.85rem;margin:4px 0'>{enemy['attack']}</div>"
        f"<div style='font-size:0.75rem;color:#888'>Weakness: {enemy['weakness']}</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    if st.session_state.battle_result:
        result = st.session_state.battle_result
        rc = "#10b981" if result["win"] else "#ef4444"
        st.markdown(
            f"<div style='background:{rc}15;border:2px solid {rc};border-radius:10px;"
            f"padding:12px;text-align:center;margin:8px 0'>"
            f"<b style='color:{rc}'>{'⚔️ WIN! +' + str(result['xp']) + ' XP' if result['win'] else '💥 BLOCKED! -20 HP'}</b><br>"
            f"<span style='color:#888;font-size:0.82rem'>{result['msg']}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
        if st.button("⚔️ Next Round!", key="battle_next", type="primary"):
            st.session_state.battle_result = None
            st.session_state.battle_enemy = random.choice(ENEMY_CARDS)
            st.session_state.battle_round += 1
            st.rerun()
    else:
        st.markdown("### 🃏 Choose Your Card!")
        card_cols = st.columns(3)
        for i, card in enumerate(PLAYER_CARDS):
            with card_cols[i % 3]:
                c = card["color"]
                st.markdown(
                    f"<div style='background:{c}12;border:2px solid {c}50;"
                    f"border-radius:12px;padding:12px;text-align:center;margin:4px 0'>"
                    f"<div style='font-size:2rem'>{card['emoji']}</div>"
                    f"<div style='font-weight:bold;color:{c};font-size:0.85rem'>{card['name']}</div>"
                    f"<div style='font-size:0.7rem;color:#888;margin:3px 0'>{card['type']}</div>"
                    f"<div style='display:flex;justify-content:space-around;margin:6px 0'>"
                    f"<div style='font-size:0.72rem;color:#10b981'>⚔️{card['power']}</div>"
                    f"<div style='font-size:0.72rem;color:#3b82f6'>🛡️{card['defense']}</div>"
                    f"</div>"
                    f"<div style='font-size:0.65rem;color:#888;line-height:1.3'>{card['special']}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                if st.button(f"Play {card['emoji']}", key=f"play_{i}", use_container_width=True):
                    win = card["type"] == enemy["weakness"] or card["power"] >= enemy["power"]
                    if win:
                        xp = 15 + (card["power"] - enemy["power"] + 30)
                        st.session_state.battle_score += xp
                        st.session_state.xp = st.session_state.get("xp", 0) + xp
                        msg = f"{card['name']} counters {enemy['name']}! {card['fact']}"
                        st.session_state.battle_result = {"win": True, "xp": xp, "msg": msg}
                    else:
                        st.session_state.battle_hp = max(0, st.session_state.battle_hp - 20)
                        msg = f"{enemy['name']} broke through! Use a {enemy['weakness']} card next time!"
                        st.session_state.battle_result = {"win": False, "xp": 0, "msg": msg}
                    if st.session_state.battle_score >= 100:
                        st.session_state.badges = st.session_state.get("badges", []) + ["🃏 Card Battle Champion"]
                    st.rerun()
