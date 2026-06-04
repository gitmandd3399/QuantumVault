"""
modules/cipher_decoder.py
Cipher Decoder Game — 12 levels from Caesar cipher to PQC concepts.
"""
import streamlit as st

LEVELS = [
    {"level":1,"name":"Caesar Shift","grade":"K-5","color":"#10b981",
     "desc":"Shift each letter back by 3. D=A, E=B, F=C...","encrypted":"NBST LFZ",
     "answer":"KYBER","hint":"Shift each letter back 3 places in the alphabet",
     "fact":"Caesar cipher is 2000 years old — quantum computers break it instantly!"},
    {"level":2,"name":"ROT13","grade":"K-5","color":"#10b981",
     "desc":"Shift each letter by 13. N=A, O=B...","encrypted":"YNGGVPR",
     "answer":"LATTICE","hint":"ROT13 means rotate 13 — apply it twice to get back the original",
     "fact":"ROT13 is so weak you can decode it in your head — not quantum safe at all!"},
    {"level":3,"name":"Reverse Cipher","grade":"K-5","color":"#10b981",
     "desc":"The message is written backwards!","encrypted":"TSIN",
     "answer":"NIST","hint":"Just read it backwards!",
     "fact":"Reversing text is not encryption — any computer cracks it in milliseconds!"},
    {"level":4,"name":"Number Code","grade":"6-8","color":"#3b82f6",
     "desc":"Each number is a letter position (A=1, B=2, C=3...)","encrypted":"8-1-19-8",
     "answer":"HASH","hint":"H=8, A=1, S=19, H=8",
     "fact":"Number substitution is a simple cipher — computers check all 26 possibilities instantly!"},
    {"level":5,"name":"Atbash Cipher","grade":"6-8","color":"#3b82f6",
     "desc":"Reverse the alphabet: A=Z, B=Y, C=X...","encrypted":"SZHS",
     "answer":"HASH","hint":"In Atbash: H becomes S, A becomes Z, S becomes H",
     "fact":"Atbash was used in the Hebrew Bible 3000 years ago — still not quantum safe!"},
    {"level":6,"name":"Vigenere Cipher","grade":"6-8","color":"#3b82f6",
     "desc":"Use keyword KEY to decode: subtract each keyword letter","encrypted":"UISVI",
     "answer":"KYBER","hint":"K-K=0=A, Y-E=20=U... subtract keyword letter values",
     "fact":"Vigenere was unbroken for 300 years! Classical computers cracked it in 1863."},
    {"level":7,"name":"Binary to Text","grade":"6-8","color":"#8b5cf6",
     "desc":"Convert binary to ASCII (8 bits per letter)","encrypted":"01001110 01001001 01010011 01010100",
     "answer":"NIST","hint":"N=78=01001110, I=73=01001001, S=83=01010011, T=84=01010100",
     "fact":"Computers store everything as binary! But binary encoding is not encryption at all."},
    {"level":8,"name":"Hex Encoding","grade":"9-12","color":"#f59e0b",
     "desc":"Hexadecimal encoding — each letter is 2 hex digits","encrypted":"4C5754",
     "answer":"LWE","hint":"L=4C(76), W=57(87), E=45(69) in ASCII hex",
     "fact":"Hex is how SHA-3 hash outputs are displayed — 64 hex chars for SHA3-256!"},
    {"level":9,"name":"XOR Cipher","grade":"9-12","color":"#ef4444",
     "desc":"XOR each ASCII value with key 10","encrypted":"65 83 88 75 79",
     "answer":"KYBER","hint":"K=75 XOR 10=65, Y=89 XOR 10=83, B=66 XOR 10=88...",
     "fact":"XOR is used inside AES encryption — a real cryptographic building block!"},
    {"level":10,"name":"Modular Cipher","grade":"9-12","color":"#ef4444",
     "desc":"Letters encoded as (value x 3) mod 26, A=0","encrypted":"2 24 1 4 17",
     "answer":"KYBER","hint":"K=10: 10*3=30 mod 26=4... find inverse of 3 mod 26=9, then 2*9 mod 26=18=S? Try: multiply each by 9 mod 26",
     "fact":"Modular arithmetic is the foundation of RSA — and also appears in Kyber!"},
    {"level":11,"name":"FIPS Lookup","grade":"9-12","color":"#4f46e5",
     "desc":"Which 3-letter name does FIPS 203 standardize? (hint: it is the key encapsulation standard)","encrypted":"FIPS 203 = ML-___ (3 letters)",
     "answer":"KEM","hint":"ML-KEM stands for Module Lattice Key Encapsulation Mechanism",
     "fact":"FIPS 203 (ML-KEM) was published in August 2024 — the first quantum-safe key exchange standard!"},
    {"level":12,"name":"LWE Master","grade":"9-12","color":"#4f46e5",
     "desc":"Solve the LWE equation: 5s + (-1) = 19 mod 23. What is s?","encrypted":"5s - 1 ≡ 19 (mod 23)",
     "answer":"4","hint":"5s ≡ 20 mod 23, so s = 20 * inverse(5) mod 23. inv(5) mod 23 = 14, so s = 20*14 mod 23 = 4",
     "fact":"This IS the Learning With Errors math that protects Kyber! In 256 dimensions with real noise it is impossible!"},
]


def render_cipher_decoder():
    st.title("🧩 Cipher Decoder Challenge — 12 Levels!")
    st.markdown(
        "🕵️ **Become a codebreaker!** Decode messages using cryptographic techniques "
        "from ancient Caesar ciphers all the way to modern quantum-safe math. "
        "Each level teaches you WHY we needed better cryptography!"
    )

    if "cipher_level" not in st.session_state:
        st.session_state.cipher_level = 1
    if "cipher_solved" not in st.session_state:
        st.session_state.cipher_solved = set()
    if "cipher_hints" not in st.session_state:
        st.session_state.cipher_hints = {}

    solved = len(st.session_state.cipher_solved)
    st.progress(solved / len(LEVELS))
    st.caption(f"🔓 {solved}/12 ciphers decoded!")

    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        level_names = []
        for l in LEVELS:
            done = l["level"] in st.session_state.cipher_solved
            level_names.append(f"{'✅' if done else '🔒'} Level {l['level']} — {l['name']} ({l['grade']})")
        sel = st.selectbox("Choose level:", level_names,
                           index=st.session_state.cipher_level - 1, key="cipher_sel")
        st.session_state.cipher_level = int(sel.split("Level ")[1].split(" ")[0])
    with col2:
        if st.session_state.cipher_level > 1:
            if st.button("Prev", key="cipher_prev", use_container_width=True):
                st.session_state.cipher_level -= 1
                st.rerun()
    with col3:
        if st.session_state.cipher_level < 12:
            if st.button("Next", key="cipher_next", use_container_width=True):
                st.session_state.cipher_level += 1
                st.rerun()

    lvl = LEVELS[st.session_state.cipher_level - 1]
    color = lvl["color"]
    already_solved = lvl["level"] in st.session_state.cipher_solved

    st.markdown("---")
    st.markdown(
        f"<div style='background:{color}15;border:2px solid {color}50;"
        f"border-radius:14px;padding:20px;margin:8px 0'>"
        f"<div style='display:flex;justify-content:space-between'>"
        f"<h3 style='color:{color};margin:0'>Level {lvl['level']}: {lvl['name']}</h3>"
        f"<span style='background:{color}30;color:{color};font-size:0.75rem;"
        f"padding:2px 8px;border-radius:100px'>{lvl['grade']}</span>"
        f"</div>"
        f"<p style='color:#ccc;margin:8px 0 4px;font-size:0.9rem'>{lvl['desc']}</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    st.markdown("### 🔐 Encrypted Message:")
    st.markdown(
        f"<div style='background:#0f172a;border:2px solid {color}60;"
        f"border-radius:10px;padding:16px;text-align:center;"
        f"font-family:monospace;font-size:1.3rem;color:{color};"
        f"letter-spacing:3px;font-weight:bold;margin:8px 0'>"
        f"{lvl['encrypted']}"
        f"</div>",
        unsafe_allow_html=True
    )

    hint_key = f"hint_{lvl['level']}"
    if hint_key not in st.session_state.cipher_hints:
        st.session_state.cipher_hints[hint_key] = False

    col1, col2 = st.columns([3, 1])
    with col1:
        answer = st.text_input("Your decoded answer:", placeholder="Type here...",
                               key=f"cipher_ans_{lvl['level']}", disabled=already_solved)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Hint", key=f"hint_btn_{lvl['level']}"):
            st.session_state.cipher_hints[hint_key] = True
            st.rerun()

    if st.session_state.cipher_hints.get(hint_key):
        st.info(f"💡 {lvl['hint']}")

    if not already_solved:
        if st.button("Submit Answer", key=f"cipher_submit_{lvl['level']}", type="primary"):
            if answer.upper().strip() == lvl["answer"].upper().strip():
                st.session_state.cipher_solved.add(lvl["level"])
                xp = 20 if not st.session_state.cipher_hints.get(hint_key) else 10
                st.session_state.xp = st.session_state.get("xp", 0) + xp
                st.balloons()
                st.success(f"CORRECT! +{xp} XP!")
                if len(st.session_state.cipher_solved) == 12:
                    st.session_state.badges = st.session_state.get("badges", []) + ["🧩 Master Decoder"]
                    st.success("🏆 ALL 12 DECODED! Master Decoder badge!")
                st.rerun()
            else:
                st.error("Not quite! Check your decoding.")
    else:
        st.success(f"Already solved! Answer: **{lvl['answer']}**")

    st.markdown(
        f"<div style='background:#1e293b;border-left:4px solid {color};"
        f"border-radius:0 8px 8px 0;padding:12px 16px;margin-top:12px'>"
        f"<div style='font-size:0.75rem;color:#888'>🔐 PQC FACT</div>"
        f"<div style='color:#ccc;font-size:0.88rem'>{lvl['fact']}</div>"
        f"</div>",
        unsafe_allow_html=True
    )
