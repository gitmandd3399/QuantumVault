"""
modules/tls_simulator.py
Interactive TLS 1.3 Handshake Simulator with Kyber.
"""
import streamlit as st
import streamlit.components.v1 as components

STEPS_CLASSICAL = [
    {"title":"Step 1: Client Hello","client":"Hello! TLS 1.3\nCipher suites:\n- ECDH-P256\n- AES-256-GCM\nRandom nonce: abc123","server":"Waiting...","desc":"Browser introduces itself and lists supported algorithms.","fact":"The ClientHello includes a random nonce to prevent replay attacks!"},
    {"title":"Step 2: Server Hello","client":"Waiting...","server":"Chosen: ECDH-P256\n+ AES-256-GCM\nHere is my certificate","desc":"Server picks algorithms and sends its identity certificate.","fact":"Server certificate is signed by a CA — soon using Dilithium signatures!"},
    {"title":"Step 3: ECDH Key Exchange","client":"My ECDH public key:\nPoint on P-256 curve\n(x=..., y=...)","server":"My ECDH public key:\nPoint on P-256 curve\n(x=..., y=...)","desc":"Both sides compute the same shared secret using elliptic curve math.","fact":"WARNING: ECDH is broken by Shor's Algorithm on quantum computers!"},
    {"title":"Step 4: Shared Secret","client":"Shared secret derived!\nDeriving AES key...","server":"Shared secret derived!\nDeriving AES key...","desc":"Both compute the SAME shared secret independently.","fact":"The shared secret goes through a KDF to create the actual AES session key!"},
    {"title":"Step 5: Encrypted!","client":"AES-256-GCM active!\nAll traffic encrypted!","server":"AES-256-GCM active!\nAll traffic encrypted!","desc":"Connection fully encrypted! All HTTP traffic protected by AES-256.","fact":"AES-256 remains safe against quantum computers — Grover only gives sqrt speedup!"},
]

STEPS_PQC = [
    {"title":"Step 1: Client Hello (PQC)","client":"Hello! TLS 1.3 + PQC\nSupported KEMs:\n- ML-KEM-768 (Kyber)\nRandom nonce: abc123","server":"Waiting...","desc":"Browser announces post-quantum key exchange support.","fact":"Google Chrome and Cloudflare already support hybrid Kyber+ECDH in TLS!"},
    {"title":"Step 2: Server Hello (PQC)","client":"Waiting...","server":"Using ML-KEM-768!\nMy Kyber public key:\nt = As+e (1184 bytes)\nAnd my certificate","desc":"Server sends its 1184-byte Kyber lattice-based public key.","fact":"The Kyber public key encodes a Module-LWE problem quantum computers cannot solve!"},
    {"title":"Step 3: Encapsulation","client":"Encapsulating secret\nwith your Kyber key...\nSending ciphertext\n(1088 bytes)!","server":"Waiting for\nciphertext...","desc":"Browser generates a random secret and encapsulates it with the server Kyber key.","fact":"Encapsulation is one-way — only the Kyber private key holder can recover the secret!"},
    {"title":"Step 4: Decapsulation","client":"Waiting...","server":"Decapsulating with\nmy private key s...\nShared secret\nrecovered!","desc":"Server uses its Kyber PRIVATE key to recover the same shared secret.","fact":"This is IND-CCA2 secure — attackers learn nothing even from chosen ciphertext attacks!"},
    {"title":"Step 5: Quantum-Safe!","client":"AES-256-GCM active!\nQUANTUM-SAFE connection!\nKyber protected us!","server":"AES-256-GCM active!\nQUANTUM-SAFE!\nLattice math wins!","desc":"Connection is now quantum-safe — even a CRQC cannot break this session.","fact":"This is exactly what production TLS 1.3 + ML-KEM looks like today!"},
]


def render_tls_simulator():
    st.title("📡 TLS Handshake Simulator")
    st.markdown(
        "🌐 **Every HTTPS connection starts with a TLS handshake.** "
        "This is how your browser and server agree on a secret key "
        "without anyone listening being able to figure it out. "
        "Post-quantum TLS uses Kyber instead of ECDH!"
    )

    if "tls_step" not in st.session_state:
        st.session_state.tls_step = 0

    col1, col2 = st.columns([3, 1])
    with col1:
        algo = st.selectbox("TLS Mode:", [
            "Classical (ECDH)",
            "Post-Quantum (ML-KEM/Kyber)",
            "Hybrid (ECDH + Kyber)"
        ], key="tls_algo_sel")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Reset", key="tls_reset"):
            st.session_state.tls_step = 0
            st.rerun()

    is_pqc = "Kyber" in algo or "Hybrid" in algo
    color = "#10b981" if "Post-Quantum" in algo else "#3b82f6" if "Hybrid" in algo else "#f59e0b"
    steps = STEPS_PQC if is_pqc else STEPS_CLASSICAL
    step = min(st.session_state.tls_step, len(steps) - 1)
    current = steps[step]

    st.iframe(f"""
<style>
body{{margin:0;background:#0f172a;font-family:sans-serif;padding:8px;}}
.conn{{display:flex;align-items:center;justify-content:center;gap:8px;}}
.party{{background:#1e293b;border:2px solid {color};border-radius:12px;
padding:12px 16px;width:180px;text-align:center;}}
.party-name{{font-size:0.72rem;font-weight:bold;color:{color};margin-bottom:6px;}}
.party-msg{{font-size:0.7rem;color:#ccc;white-space:pre-line;line-height:1.5;min-height:70px;}}
.line{{flex:1;height:3px;background:{color};position:relative;}}
.arrow{{position:absolute;top:-8px;right:-2px;color:{color};font-size:14px;}}
</style>
<div class="conn">
<div class="party">
<div class="party-name">🌐 Browser</div>
<div class="party-msg">{current["client"]}</div>
</div>
<div class="line"><div class="arrow">→</div></div>
<div class="party">
<div class="party-name">🖥️ Server</div>
<div class="party-msg">{current["server"]}</div>
</div>
</div>
""", height=160)

    st.markdown(
        f"<div style='background:#1e293b;border-left:4px solid {color};"
        f"border-radius:0 10px 10px 0;padding:12px 16px;margin:8px 0'>"
        f"<h4 style='color:{color};margin:0 0 4px'>{current['title']}</h4>"
        f"<p style='color:#ccc;margin:0 0 4px;font-size:0.88rem'>{current['desc']}</p>"
        f"<p style='color:#888;margin:0;font-size:0.8rem'>💡 {current['fact']}</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    dot_html = "".join([
        f"<span style='width:10px;height:10px;border-radius:50%;display:inline-block;"
        f"margin:3px;background:{'%s' % color if i<=step else '#334155'}'></span>"
        for i in range(len(steps))
    ])
    st.markdown(f"<div style='text-align:center'>{dot_html}</div>", unsafe_allow_html=True)
    st.caption(f"Step {step+1} of {len(steps)}")

    col1, col2 = st.columns(2)
    with col1:
        if step > 0:
            if st.button("Back", key="tls_back", use_container_width=True):
                st.session_state.tls_step -= 1
                st.rerun()
    with col2:
        if step < len(steps) - 1:
            if st.button("Next Step", key="tls_next", type="primary", use_container_width=True):
                st.session_state.tls_step += 1
                st.rerun()
        else:
            if st.button("Complete! +20 XP", key="tls_done", type="primary", use_container_width=True):
                st.session_state.xp = st.session_state.get("xp", 0) + 20
                st.session_state.badges = st.session_state.get("badges", []) + ["📡 TLS Expert"]
                st.balloons()
                st.success("Badge unlocked: TLS Expert! +20 XP")
