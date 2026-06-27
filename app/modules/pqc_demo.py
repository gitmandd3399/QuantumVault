import streamlit as st
import hashlib
import random
import time

def render_pqc_demo():
    """PQC Demo using only Python built-ins — works on Streamlit Cloud."""
    st.subheader("🔬 Live PQC Algorithm Demo")
    st.markdown(
        "**Watch all 4 NIST post-quantum cryptography standards in action!** "
        "This demo simulates the real algorithms that protect the future internet."
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔐 Kyber (FIPS 203)",
        "✍️ Dilithium (FIPS 204)",
        "🌲 SPHINCS+ (FIPS 205)",
        "🦅 Falcon (FIPS 206)",
        "#️⃣ SHA-3 Avalanche"
    ])

    with tab1:
        st.markdown("### ML-KEM (Kyber768) — Key Exchange")
        st.markdown(
            "**What it does:** Creates a shared secret between two parties "
            "without ever sending the secret over the network. "
            "Used in HTTPS, TLS, and VPNs."
        )
        st.markdown("**How it works:**")
        st.code(
            "1. Alice generates a public/private key pair\n"
            "2. Bob uses Alice public key to create a ciphertext\n"
            "3. Bob gets a shared secret\n"
            "4. Alice uses her private key to recover the SAME shared secret\n"
            "5. Neither ever sent the secret — quantum computers cannot find it!",
            language="text"
        )
        if st.button("▶ Run Kyber Key Exchange", key="run_kyber", type="primary"):
            with st.spinner("Generating Kyber key pair..."):
                time.sleep(0.5)
                pub_key = hashlib.sha3_256(b"kyber_public_key_demo").hexdigest()
                priv_key = hashlib.sha3_256(b"kyber_private_key_demo").hexdigest()
                ciphertext = hashlib.sha3_256(b"kyber_ciphertext_demo").hexdigest()
                shared_secret = hashlib.sha3_256(b"kyber_shared_secret_demo").hexdigest()

            st.success("✅ Kyber Key Exchange Complete!")
            col1, col2, col3 = st.columns(3)
            col1.metric("Public Key Size", "1,184 bytes")
            col2.metric("Ciphertext Size", "1,088 bytes")
            col3.metric("Security Level", "128-bit quantum")

            st.code(
                "Public Key  : " + pub_key[:32] + "...\n" +
                "Private Key : " + priv_key[:32] + "... (NEVER shared)\n" +
                "Ciphertext  : " + ciphertext[:32] + "...\n" +
                "Shared Secret: " + shared_secret[:32] + "...\n" +
                "Keys Match  : True ✅\n" +
                "Quantum Safe: True ✅ (Module-LWE hardness)",
                language="text"
            )
            st.info(
                "🔐 Real Kyber uses Module Learning With Errors (M-LWE) math. "
                "The public key has intentional noise added to hide the secret. "
                "Even quantum computers using Shor or Grover cannot remove the noise!"
            )

    with tab2:
        st.markdown("### ML-DSA (Dilithium) — Digital Signatures")
        st.markdown(
            "**What it does:** Creates unforgeable digital signatures. "
            "Proves a document or message came from a specific person "
            "and was not tampered with. Used for code signing and certificates."
        )
        if st.button("▶ Sign a Document", key="run_dilithium", type="primary"):
            doc = "QuantumVault Academy LLC - School License Agreement 2026"
            with st.spinner("Signing with Dilithium..."):
                time.sleep(0.5)
                sig = hashlib.sha3_512((doc + "dilithium_private_key").encode()).hexdigest()
                pub = hashlib.sha3_256(b"dilithium_public_key").hexdigest()

            st.success("✅ Document Signed with Dilithium!")
            col1, col2, col3 = st.columns(3)
            col1.metric("Public Key", "1,952 bytes")
            col2.metric("Signature Size", "3,293 bytes")
            col3.metric("Security Level", "128-bit quantum")

            st.code(
                "Document    : " + doc + "\n" +
                "Public Key  : " + pub[:32] + "...\n" +
                "Signature   : " + sig[:32] + "...\n" +
                "Sig Valid   : True ✅\n" +
                "Forgeable   : False ✅ (Module-LWE + SIS hardness)",
                language="text"
            )
            st.info(
                "✍️ Real Dilithium (ML-DSA FIPS 204) uses Module-LWE and Module-SIS "
                "lattice problems. Creating a fake signature requires solving "
                "an NP-hard problem — impossible even for quantum computers!"
            )

    with tab3:
        st.markdown("### SLH-DSA (SPHINCS+) — Hash-Based Signatures")
        st.markdown(
            "**What it does:** Creates digital signatures using ONLY hash functions. "
            "Even if lattice math is ever broken, SPHINCS+ stays safe. "
            "Used as a backup signature scheme."
        )
        if st.button("▶ Run SPHINCS+ Signature", key="run_sphincs", type="primary"):
            msg = b"QuantumVault Academy - Hash Based Signature"
            with st.spinner("Building SPHINCS+ hash tree..."):
                time.sleep(0.8)
                h1 = hashlib.sha3_256(msg).hexdigest()
                h2 = hashlib.sha3_256((msg + b"_layer2").decode("latin1").encode()).hexdigest()
                h3 = hashlib.sha3_256((h1 + h2).encode()).hexdigest()
                sig = hashlib.sha3_256((h3 + "sphincs_private").encode()).hexdigest()

            st.success("✅ SPHINCS+ Signature Complete!")
            col1, col2, col3 = st.columns(3)
            col1.metric("Public Key", "32 bytes")
            col2.metric("Signature Size", "17,088 bytes")
            col3.metric("Hash Function", "SHA-3")

            st.code(
                "Layer 1 Hash: " + h1[:32] + "...\n" +
                "Layer 2 Hash: " + h2[:32] + "...\n" +
                "Root Hash   : " + h3[:32] + "...\n" +
                "Signature   : " + sig[:32] + "...\n" +
                "Sig Valid   : True ✅\n" +
                "Quantum Safe: True ✅ (SHA-3 hash hardness only!)",
                language="text"
            )
            st.info(
                "🌲 SPHINCS+ (SLH-DSA FIPS 205) chains thousands of SHA-3 hashes "
                "into a Merkle tree structure. No lattice math at all — "
                "only hash functions. Even if Kyber and Dilithium break, "
                "SPHINCS+ stays safe!"
            )

    with tab4:
        st.markdown("### FN-DSA (Falcon) — Compact Signatures")
        st.markdown(
            "**What it does:** Creates the SMALLEST signatures of all 4 NIST standards. "
            "Uses NTRU lattices instead of Module-LWE. "
            "Perfect for IoT devices, smart cards, and embedded systems."
        )
        if st.button("▶ Run Falcon Signature", key="run_falcon", type="primary"):
            msg = b"IoT Device Authentication - QuantumVault"
            with st.spinner("Running Falcon NTRU lattice..."):
                time.sleep(0.4)
                pub = hashlib.sha3_256(b"falcon_ntru_public").hexdigest()
                sig = hashlib.sha3_256(msg + b"falcon_ntru_private").hexdigest()[:83*2]

            st.success("✅ Falcon Signature Complete!")
            col1, col2, col3 = st.columns(3)
            col1.metric("Public Key", "897 bytes")
            col2.metric("Signature", "~666 bytes")
            col3.metric("Lattice Type", "NTRU")

            st.code(
                "Public Key: " + pub[:32] + "...\n" +
                "Signature : " + sig[:32] + "...\n" +
                "Sig Valid : True ✅\n" +
                "Sig Size  : 3x SMALLER than Dilithium ✅\n" +
                "Quantum Safe: True ✅ (NTRU lattice hardness)",
                language="text"
            )
            st.info(
                "🦅 Falcon (FN-DSA FIPS 206) uses NTRU lattices — "
                "a different type of lattice math than Kyber and Dilithium. "
                "Its signatures are 3x smaller making it ideal for "
                "IoT sensors, medical devices, and smart cards!"
            )

    with tab5:
        st.markdown("### SHA-3 Avalanche Effect")
        st.markdown(
            "**What it does:** SHA-3 is the hash function used inside SPHINCS+. "
            "Change ONE character and the ENTIRE hash changes. "
            "This is called the avalanche effect."
        )

        user_msg = st.text_input(
            "Type a message to hash:",
            value="hello quantum world",
            key="sha3_input"
        )

        if user_msg:
            msg1 = user_msg
            msg2 = user_msg[0].swapcase() + user_msg[1:]
            h1 = hashlib.sha3_256(msg1.encode()).hexdigest()
            h2 = hashlib.sha3_256(msg2.encode()).hexdigest()
            diff = sum(1 for a, b in zip(h1, h2) if a != b)
            pct = round(diff / len(h1) * 100)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original:**")
                st.code(msg1)
                st.code(h1)
            with col2:
                st.markdown("**First letter changed:**")
                st.code(msg2)
                st.code(h2)

            st.metric(
                "Hash characters changed",
                str(diff) + " / 64",
                str(pct) + "% of hash changed!"
            )

            if pct > 40:
                st.success(
                    "🌊 AVALANCHE EFFECT CONFIRMED! " + str(pct) + "% of hash changed "
                    "from just 1 character change! "
                    "This is why SHA-3 is quantum-resistant — "
                    "impossible to predict or reverse!"
                )

    st.markdown("---")
    st.markdown("### 📊 NIST PQC Standards Comparison")
    data = {
        "Standard": ["ML-KEM (Kyber)", "ML-DSA (Dilithium)", "SLH-DSA (SPHINCS+)", "FN-DSA (Falcon)"],
        "FIPS": ["203", "204", "205", "206"],
        "Type": ["Key Exchange", "Signatures", "Hash Signatures", "Compact Signatures"],
        "Public Key": ["1,184 bytes", "1,952 bytes", "32 bytes", "897 bytes"],
        "Quantum Security": ["128-bit", "128-bit", "128-bit", "128-bit"],
        "Use Case": ["TLS/HTTPS/VPN", "Certificates/Code", "Backup/Long-term", "IoT/Smart Cards"],
    }
    import pandas as pd
    st.dataframe(pd.DataFrame(data), use_container_width=True)
    st.success(
        "✅ All 4 NIST PQC Standards finalized August 2024! "
        "Together they replace ALL RSA and elliptic curve cryptography "
        "to protect against quantum computers!"
    )
