"""
modules/crypto_lab.py
──────────────────────
Interactive Crypto Lab Sandbox.
Students generate real keys, encrypt messages,
and simulate quantum attacks.
"""

import streamlit as st
import hashlib
import secrets
import time


def simple_kyber_sim(seed: int):
    """Simulate Kyber key generation (educational approximation)."""
    import random
    rng = random.Random(seed)  # nosec B311
    q = 3329  # Kyber modulus
    n = 8     # Simplified (real is 256)

    # Generate matrix A
    A = [[rng.randint(0, q-1) for _ in range(n)] for _ in range(n)]

    # Generate secret s (small coefficients)
    s = [rng.randint(-3, 3) for _ in range(n)]

    # Generate noise e (small)
    e = [rng.randint(-2, 2) for _ in range(n)]

    # Public key: b = A*s + e mod q
    b = []
    for i in range(n):
        val = sum(A[i][j] * s[j] for j in range(n)) + e[i]
        b.append(val % q)

    return {
        "public_key": b,
        "private_key": s,
        "matrix_A": A[0][:4],  # Show first row
        "noise": e,
        "modulus": q,
    }


def sha3_hash(message: str) -> str:
    return hashlib.sha3_256(message.encode()).hexdigest()


def sha3_512_hash(message: str) -> str:
    return hashlib.sha3_512(message.encode()).hexdigest()


def simple_encrypt(message: str, key: list) -> list:
    """XOR-based encryption using key bytes (educational demo)."""
    key_bytes = bytes([abs(k) % 256 for k in key])
    msg_bytes = message.encode()
    encrypted = []
    for i, b in enumerate(msg_bytes):
        encrypted.append(b ^ key_bytes[i % len(key_bytes)])
    return encrypted


def simple_decrypt(encrypted: list, key: list) -> str:
    """Decrypt the XOR-encrypted message."""
    key_bytes = bytes([abs(k) % 256 for k in key])
    decrypted = []
    for i, b in enumerate(encrypted):
        decrypted.append(b ^ key_bytes[i % len(key_bytes)])
    try:
        return bytes(decrypted).decode()
    except Exception:
        return "[Decryption failed]"


def render_crypto_lab():
    st.title("🧪 Crypto Lab Sandbox")
    st.markdown(
        "Experiment with real cryptographic operations! "
        "Generate keys, encrypt messages, and see the math behind PQC."
    )

    lab_tab1, lab_tab2, lab_tab3, lab_tab4 = st.tabs([
        "🔐 Kyber Key Generator",
        "🔢 SHA-3 Hash Lab",
        "🔒 Encrypt a Message",
        "💥 Simulate RSA Attack",
    ])

    # ── Tab 1: Kyber Key Generator ────────────────────────────────────────
    with lab_tab1:
        st.subheader("🔐 Kyber Key Generator")
        st.markdown(
            "Generate a simplified Kyber keypair! "
            "Real Kyber uses 256 dimensions — we use 8 for demonstration."
        )

        col1, col2 = st.columns(2)
        with col1:
            seed = st.number_input(
                "Random seed (or use random):",
                min_value=0, max_value=99999,
                value=42, key="kyber_seed"
            )
        with col2:
            if st.button("🎲 Random Seed", key="random_seed"):
                st.session_state.kyber_seed = secrets.randbelow(99999)
                st.rerun()

        if st.button("🔑 Generate Keypair!", key="gen_kyber", type="primary"):
            with st.spinner("Generating Kyber keypair..."):
                time.sleep(0.5)
                result = simple_kyber_sim(seed)
                st.session_state.kyber_result = result
                st.session_state.xp = st.session_state.get("xp", 0) + 10
                st.success("+10 XP for generating a keypair!")

        if "kyber_result" in st.session_state:
            r = st.session_state.kyber_result
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🌐 Public Key** (share with everyone)")
                st.code(
                    f"b = {r['public_key']}\n"
                    f"(mod q={r['modulus']})",
                    language="python"
                )
                st.caption("Anyone can see this!")

            with col2:
                st.markdown("**🔒 Private Key** (keep secret!)")
                st.code(
                    f"s = {r['private_key']}\n"
                    f"(small secret coefficients)",
                    language="python"
                )
                st.caption("Never share this with anyone!")

            st.markdown("**🏗️ How it was generated:**")
            st.code(
                f"Matrix A (first row): {r['matrix_A']}\n"
                f"Noise e:              {r['noise']}\n"
                f"b = A·s + e mod {r['modulus']}\n"
                f"b = {r['public_key']}",
                language="python"
            )

            st.info(
                "🔍 **Key insight:** The public key `b` hides the secret `s` "
                "because of the noise `e`. To find `s` from `b` and `A`, "
                "you would need to solve the Learning With Errors problem — "
                "impossible for quantum computers in high dimensions!"
            )

            st.markdown("**📏 Key Size Comparison:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Our Demo (8D)", "tiny", "educational only")
            with col2:
                st.metric("Real Kyber-512", "800 bytes", "production ready")
            with col3:
                st.metric("RSA-2048", "256,000 bytes", "quantum vulnerable")

    # ── Tab 2: SHA-3 Hash Lab ─────────────────────────────────────────────
    with lab_tab2:
        st.subheader("🔢 SHA-3 Hash Lab")
        st.markdown(
            "Type any message and see the real SHA-3 hash! "
            "Try changing one character and watch the entire hash change."
        )

        col1, col2 = st.columns(2)
        with col1:
            msg1 = st.text_area(
                "Message 1:",
                value="Hello World",
                height=80,
                key="hash_msg1"
            )
            hash_type1 = st.selectbox(
                "Algorithm:", ["SHA3-256", "SHA3-512"], key="hash_type1"
            )
            h1 = sha3_hash(msg1) if hash_type1 == "SHA3-256" else sha3_512_hash(msg1)
            st.markdown("**Hash output:**")
            st.code(h1, language=None)
            st.caption(f"{len(h1)*4} bits output")

        with col2:
            msg2 = st.text_area(
                "Message 2 (try changing one character):",
                value="hello World",
                height=80,
                key="hash_msg2"
            )
            hash_type2 = st.selectbox(
                "Algorithm:", ["SHA3-256", "SHA3-512"], key="hash_type2"
            )
            h2 = sha3_hash(msg2) if hash_type2 == "SHA3-256" else sha3_512_hash(msg2)
            st.markdown("**Hash output:**")
            st.code(h2, language=None)
            st.caption(f"{len(h2)*4} bits output")

        # Avalanche effect analysis
        if h1 and h2:
            diff_chars = sum(1 for a, b in zip(h1, h2) if a != b)
            diff_pct = round(diff_chars / len(h1) * 100)
            st.markdown("---")
            st.markdown("**🌊 Avalanche Effect Analysis:**")
            if msg1 == msg2:
                st.success("✅ Identical messages → Identical hashes!")
            else:
                st.info(
                    f"**{diff_chars}/{len(h1)} characters changed** ({diff_pct}%) "
                    f"— from changing '{msg1[:20]}...' to '{msg2[:20]}...'"
                )
                st.progress(diff_pct / 100)

            if st.button("✅ I found the avalanche effect! +15 XP", key="avalanche_found"):
                st.session_state.xp = st.session_state.get("xp", 0) + 15
                st.balloons()
                st.success("+15 XP! The avalanche effect makes hash functions secure!")

    # ── Tab 3: Encrypt a Message ──────────────────────────────────────────
    with lab_tab3:
        st.subheader("🔒 Encrypt a Secret Message")
        st.markdown(
            "Use your generated Kyber private key to encrypt a message! "
            "This demonstrates the concept of symmetric encryption using a derived key."
        )

        if "kyber_result" not in st.session_state:
            st.warning("First generate a Kyber keypair in the Key Generator tab!")
        else:
            r = st.session_state.kyber_result
            st.success(f"Using private key: `{r['private_key'][:4]}...`")

            plaintext = st.text_input(
                "Enter your secret message:",
                value="Kyber protects this message!",
                key="encrypt_msg"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔒 Encrypt!", key="do_encrypt", type="primary"):
                    encrypted = simple_encrypt(plaintext, r["private_key"])
                    st.session_state.encrypted_msg = encrypted
                    st.session_state.original_msg = plaintext
                    st.success("Message encrypted!")

            with col2:
                if st.button("🔓 Decrypt!", key="do_decrypt"):
                    if "encrypted_msg" in st.session_state:
                        decrypted = simple_decrypt(
                            st.session_state.encrypted_msg,
                            r["private_key"]
                        )
                        if decrypted == st.session_state.get("original_msg"):
                            st.success(f"✅ Decrypted: **{decrypted}**")
                        else:
                            st.error("Decryption failed!")
                    else:
                        st.warning("Encrypt a message first!")

            if "encrypted_msg" in st.session_state:
                st.markdown("**🔢 Encrypted bytes:**")
                st.code(
                    str(st.session_state.encrypted_msg[:16]) + "...",
                    language=None
                )
                st.caption(
                    "These bytes are meaningless without the private key! "
                    "The key derived from your Kyber private key was used to XOR the message."
                )

                st.info(
                    "🔐 **Real world:** In practice Kyber encapsulates a random session key, "
                    "then that key is used with AES-256 to encrypt the actual message. "
                    "This is called a hybrid encryption scheme!"
                )

    # ── Tab 4: Simulate RSA Attack ────────────────────────────────────────
    with lab_tab4:
        st.subheader("💥 Simulate a Quantum Attack on RSA")
        st.markdown(
            "Watch what happens when a quantum computer runs Shor's Algorithm against RSA! "
            "We simulate a TINY RSA key to show the concept."
        )

        st.warning(
            "⚠️ **Educational simulation only!** "
            "Real RSA uses 2048-bit numbers. We use tiny numbers to demonstrate the concept."
        )

        col1, col2 = st.columns(2)
        with col1:
            p = st.selectbox("Prime p:", [11, 13, 17, 19, 23, 29], key="rsa_p")
            q_rsa = st.selectbox(
                "Prime q:", [11, 13, 17, 19, 23, 29], index=1, key="rsa_q"
            )

        with col2:
            n = p * q_rsa
            st.metric("n = p × q", n)
            e = 65537
            st.metric("Public exponent e", e)

        st.markdown(f"**Public key:** (n={n}, e={e})")
        st.markdown(f"**Secret:** p={p} and q={q_rsa} (must NEVER be revealed)")
        st.markdown("---")

        if st.button("⚛️ Run Shor's Algorithm (Simulated)!", key="run_shor", type="primary"):
            progress = st.progress(0)
            status = st.empty()

            for i in range(101):
                time.sleep(0.02)
                progress.progress(i)
                if i < 20:
                    status.markdown(f"🔄 Initializing qubits... {i}%")
                elif i < 50:
                    status.markdown(f"⚛️ Quantum Fourier Transform running... {i}%")
                elif i < 80:
                    status.markdown(f"🌀 Finding period of f(x) = a^x mod {n}... {i}%")
                elif i < 95:
                    status.markdown(f"🧮 Computing GCD to find factors... {i}%")
                else:
                    status.markdown(f"💥 Factoring complete! {i}%")

            st.error(f"💀 RSA CRACKED! Found: p={p}, q={q_rsa}")
            st.markdown(
                f"**Quantum computer factored n={n} into p={p} × q={q_rsa}!**\n\n"
                f"With p and q known, the private key can be computed instantly. "
                f"Real quantum computers running Shor's Algorithm on RSA-2048 "
                f"(which has 617-digit numbers) would take hours — not millions of years!"
            )

            st.success(
                "✅ **But Kyber is safe!** Shor's Algorithm only attacks "
                "problems based on factoring and discrete logarithms. "
                "Kyber's lattice LWE problem is immune to Shor's Algorithm!"
            )

            if st.button("✅ I understand why we need PQC! +20 XP", key="understand_pqc"):
                st.session_state.xp = st.session_state.get("xp", 0) + 20
                st.balloons()
                st.success("+20 XP! You now understand the quantum threat!")
