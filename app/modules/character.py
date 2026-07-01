"""
modules/character.py
─────────────────────
Character customization system.
Students customize Agent Pixel using XP-unlocked cosmetics.
"""

import streamlit as st
import streamlit.components.v1 as components


HAIR_STYLES = [
    {"id":"h1", "name":"Default",     "emoji":"👤", "xp":0,   "color":"#a5b4fc"},
    {"id":"h2", "name":"Purple",      "emoji":"💜", "xp":25,  "color":"#8b5cf6"},
    {"id":"h3", "name":"Fire Red",    "emoji":"🔴", "xp":50,  "color":"#ef4444"},
    {"id":"h4", "name":"Ocean Blue",  "emoji":"🔵", "xp":75,  "color":"#3b82f6"},
    {"id":"h5", "name":"Galaxy",      "emoji":"🌌", "xp":150, "color":"#4f46e5"},
    {"id":"h6", "name":"Gold Crown",  "emoji":"👑", "xp":300, "color":"#f59e0b"},
]

OUTFITS = [
    {"id":"o1", "name":"Cadet Suit",     "emoji":"🧑‍💻", "xp":0,   "color":"#6b7280"},
    {"id":"o2", "name":"Cyber Blue",     "emoji":"🦺",  "xp":50,  "color":"#3b82f6"},
    {"id":"o3", "name":"Lattice Armor",  "emoji":"🛡️",  "xp":100, "color":"#10b981"},
    {"id":"o4", "name":"Quantum Cloak",  "emoji":"🧣",  "xp":200, "color":"#8b5cf6"},
    {"id":"o5", "name":"NIST Uniform",   "emoji":"🎖️",  "xp":350, "color":"#f59e0b"},
    {"id":"o6", "name":"Guardian Armor", "emoji":"⚔️",  "xp":500, "color":"#ec4899"},
]

ACCESSORIES = [
    {"id":"a1", "name":"None",          "emoji":"",    "xp":0,   "color":"#6b7280"},
    {"id":"a2", "name":"Kyber Crystal", "emoji":"💎",  "xp":30,  "color":"#10b981"},
    {"id":"a3", "name":"Jetpack",       "emoji":"🚀",  "xp":80,  "color":"#3b82f6"},
    {"id":"a4", "name":"Laser Shield",  "emoji":"🔮",  "xp":150, "color":"#8b5cf6"},
    {"id":"a5", "name":"Quantum Wings", "emoji":"🦋",  "xp":300, "color":"#f59e0b"},
    {"id":"a6", "name":"Byte Robot",    "emoji":"🤖",  "xp":450, "color":"#ec4899"},
]

BACKGROUNDS = [
    {"id":"b1", "name":"Deep Space",    "emoji":"🌌", "xp":0,   "color":"#0f172a"},
    {"id":"b2", "name":"Lattice Grid",  "emoji":"🏗️", "xp":40,  "color":"#1e1b4b"},
    {"id":"b3", "name":"Cyber City",    "emoji":"🌆", "xp":100, "color":"#1e293b"},
    {"id":"b4", "name":"Quantum Lab",   "emoji":"🔬", "xp":200, "color":"#0c4a6e"},
    {"id":"b5", "name":"NIST HQ",       "emoji":"🏛️", "xp":350, "color":"#1a1a2e"},
    {"id":"b6", "name":"Kyber Vault",   "emoji":"🔐", "xp":500, "color":"#2d1b69"},
]


def get_unlocked(items, xp):
    return [i for i in items if xp >= i["xp"]]


def render_character_page():
    st.title("🎨 Customize Agent Pixel")
    st.markdown(
        "Earn XP to unlock new cosmetics! "
        "Your character appears on your achievement cards and profile."
    )

    xp = st.session_state.get("xp", 0)

    # Initialize character state
    if "char_hair" not in st.session_state:
        st.session_state.char_hair = "h1"
    if "char_outfit" not in st.session_state:
        st.session_state.char_outfit = "o1"
    if "char_accessory" not in st.session_state:
        st.session_state.char_accessory = "a1"
    if "char_bg" not in st.session_state:
        st.session_state.char_bg = "b1"
    if "char_name" not in st.session_state:
        st.session_state.char_name = "Agent Pixel"

    # Get current selections
    hair = next((h for h in HAIR_STYLES if h["id"] == st.session_state.char_hair), HAIR_STYLES[0])
    outfit = next((o for o in OUTFITS if o["id"] == st.session_state.char_outfit), OUTFITS[0])
    acc = next((a for a in ACCESSORIES if a["id"] == st.session_state.char_accessory), ACCESSORIES[0])
    bg = next((b for b in BACKGROUNDS if b["id"] == st.session_state.char_bg), BACKGROUNDS[0])

    st.markdown("---")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 👤 Your Character")

        # Character display card
        components.html(f"""
<style>
body{{margin:0;background:#0f172a;font-family:sans-serif;}}
.char-card{{
    background:{bg["color"]};
    border:2px solid #4f46e5;
    border-radius:20px;
    padding:24px;
    text-align:center;
    position:relative;
    overflow:hidden;
    width:240px;
    margin:0 auto;
}}
.char-card::before{{
    content:'';position:absolute;top:-40px;left:-40px;
    width:150px;height:150px;
    background:radial-gradient(circle,rgba(79,70,229,0.3),transparent);
}}
.char-emoji{{font-size:4rem;display:block;margin:12px 0;}}
.char-acc{{font-size:1.8rem;position:absolute;top:16px;right:16px;}}
.char-name{{font-size:1rem;font-weight:bold;color:white;margin:6px 0;}}
.char-outfit{{font-size:0.75rem;color:#a5b4fc;margin:2px 0;}}
.char-xp{{font-size:0.8rem;color:#10b981;margin-top:8px;font-weight:bold;}}
.stat-bar{{height:4px;background:#1e293b;border-radius:2px;margin:4px 0;overflow:hidden;}}
.stat-fill{{height:100%;border-radius:2px;}}
</style>
<div class="char-card">
    <div class="char-acc">{acc["emoji"]}</div>
    <div style="font-size:1.2rem;color:{hair['color']};margin-bottom:4px;">{hair["emoji"]} {hair["name"]}</div>
    <div class="char-emoji">{outfit["emoji"]}</div>
    <div class="char-name">{st.session_state.char_name}</div>
    <div class="char-outfit">{outfit["name"]} · {bg["name"]}</div>
    <div class="char-xp">⭐ {xp} XP</div>
</div>
""", height=280)

        st.markdown("<br>", unsafe_allow_html=True)
        new_name = st.text_input(
            "Character Name:",
            value=st.session_state.char_name,
            max_chars=20,
            key="char_name_input"
        )
        if new_name != st.session_state.char_name:
            st.session_state.char_name = new_name
            st.rerun()

    with col2:
        st.markdown("### 🛍️ Cosmetic Shop")

        shop_tab1, shop_tab2, shop_tab3, shop_tab4 = st.tabs([
            "💇 Hair", "👕 Outfit", "✨ Accessory", "🌌 Background"
        ])

        def render_shop_items(items, state_key, category):
            for item in items:
                unlocked = xp >= item["xp"]
                col_a, col_b = st.columns([1, 3])
                with col_a:
                    st.markdown(
                        f"<div style='font-size:1.8rem;text-align:center;"
                        f"opacity:{'1' if unlocked else '0.4'}'>{item['emoji'] or '⬜'}</div>",
                        unsafe_allow_html=True
                    )
                with col_b:
                    selected = st.session_state.get(state_key) == item["id"]
                    if unlocked:
                        if st.button(
                            f"{'✅ ' if selected else ''}{item['name']}",
                            key=f"{category}_{item['id']}",
                            type="primary" if selected else "secondary"
                        ):
                            st.session_state[state_key] = item["id"]
                            st.rerun()
                    else:
                        st.markdown(
                            f"<div style='font-size:0.8rem;color:#6b7280;"
                            f"padding:6px 0;'>🔒 {item['name']} — {item['xp']} XP</div>",
                            unsafe_allow_html=True
                        )

        with shop_tab1:
            render_shop_items(HAIR_STYLES, "char_hair", "hair")
        with shop_tab2:
            render_shop_items(OUTFITS, "char_outfit", "outfit")
        with shop_tab3:
            render_shop_items(ACCESSORIES, "char_accessory", "acc")
        with shop_tab4:
            render_shop_items(BACKGROUNDS, "char_bg", "bg")

    st.markdown("---")

    # Unlock progress
    st.markdown("### 🔓 Unlock Progress")
    total = len(HAIR_STYLES) + len(OUTFITS) + len(ACCESSORIES) + len(BACKGROUNDS)
    unlocked_count = (
        len(get_unlocked(HAIR_STYLES, xp)) +
        len(get_unlocked(OUTFITS, xp)) +
        len(get_unlocked(ACCESSORIES, xp)) +
        len(get_unlocked(BACKGROUNDS, xp))
    )
    st.progress(unlocked_count / total)
    st.caption(f"{unlocked_count}/{total} cosmetics unlocked — earn more XP to unlock everything!")

    # Next unlock
    all_items = HAIR_STYLES + OUTFITS + ACCESSORIES + BACKGROUNDS
    locked = [i for i in all_items if xp < i["xp"]]
    if locked:
        next_item = min(locked, key=lambda x: x["xp"])
        st.info(
            f"🎯 Next unlock: **{next_item['emoji']} {next_item['name']}** "
            f"at {next_item['xp']} XP — you need {next_item['xp'] - xp} more XP!"
        )
    else:
        st.success("🎉 All cosmetics unlocked! You are a true Quantum Guardian!")
