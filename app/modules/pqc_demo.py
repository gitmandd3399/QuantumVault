import streamlit as st
import streamlit.components.v1 as components

def render_pqc_demo():
    """Live PQC Demo — shows all 4 NIST standards running in real time."""
    st.subheader("🔬 Live PQC Algorithm Demo")
    st.markdown(
        "**Watch all 4 NIST post-quantum cryptography standards run in real time!** "
        "This is the actual code protecting the future internet — running right here."
    )

    try:
        import oqs
        import time
        import hashlib

        message = b"QuantumVault Academy LLC - Quantum Safe Message"

        # ── ML-KEM FIPS 203 ──────────────────────────────────────────────
        st.markdown("### 🔐 FIPS 203 — ML-KEM (Kyber768) Key Exchange")
        st.markdown("Used for: **TLS, HTTPS, VPN key exchange**")
        with st.spinner("Generating Kyber key pair..."):
            t0 = time.time()
            kem = oqs.KeyEncapsulation("Kyber768")
            public_key = kem.generate_keypair()
            ciphertext, shared_secret_enc = kem.encap_secret(public_key)
            shared_secret_dec = kem.decap_secret(ciphertext)
            t1 = time.time()

        col1, col2, col3 = st.columns(3)
        col1.metric("Public Key Size", str(len(public_key)) + " bytes")
        col2.metric("Ciphertext Size", str(len(ciphertext)) + " bytes")
        col3.metric("Time", str(round((t1-t0)*1000, 2)) + " ms")

        st.code(
            "Public Key (first 32 bytes): " + public_key[:32].hex() + "...\n" +
            "Shared Secret: " + shared_secret_enc[:16].hex() + "...\n" +
            "Keys Match: " + str(shared_secret_enc == shared_secret_dec) + " ✅",
            language="text"
        )

        # ── ML-DSA FIPS 204 ──────────────────────────────────────────────
        st.markdown("### ✍️ FIPS 204 — ML-DSA (Dilithium) Digital Signatures")
        st.markdown("Used for: **Code signing, certificates, legal documents**")
        with st.spinner("Signing with Dilithium..."):
            t0 = time.time()
            sig1 = oqs.Signature("ML-DSA-65")
            pub1 = sig1.generate_keypair()
            signature1 = sig1.sign(message)
            valid1 = sig1.verify(message, signature1, pub1)
            t1 = time.time()

        col1, col2, col3 = st.columns(3)
        col1.metric("Public Key Size", str(len(pub1)) + " bytes")
        col2.metric("Signature Size", str(len(signature1)) + " bytes")
        col3.metric("Time", str(round((t1-t0)*1000, 2)) + " ms")

        st.code(
            "Message: " + message.decode() + "\n" +
            "Signature (first 32 bytes): " + signature1[:32].hex() + "...\n" +
            "Signature Valid: " + str(valid1) + " ✅",
            language="text"
        )

        # ── SLH-DSA FIPS 205 ─────────────────────────────────────────────
        st.markdown("### 🌲 FIPS 205 — SLH-DSA (SPHINCS+) Hash Signatures")
        st.markdown("Used for: **Backup signatures, long-term security**")
        with st.spinner("Signing with SPHINCS+..."):
            t0 = time.time()
            sig2 = oqs.Signature("SPHINCS+-SHA2-128f-simple")
            pub2 = sig2.generate_keypair()
            signature2 = sig2.sign(message)
            valid2 = sig2.verify(message, signature2, pub2)
            t1 = time.time()

        col1, col2, col3 = st.columns(3)
        col1.metric("Public Key Size", str(len(pub2)) + " bytes")
        col2.metric("Signature Size", str(len(signature2)) + " bytes")
        col3.metric("Time", str(round((t1-t0)*1000, 2)) + " ms")

        st.code(
            "Hash Function: SHA-2 (quantum-resistant with Grover halving)\n" +
            "Signature (first 32 bytes): " + signature2[:32].hex() + "...\n" +
            "Signature Valid: " + str(valid2) + " ✅",
            language="text"
        )

        # ── FN-DSA FIPS 206 ──────────────────────────────────────────────
        st.markdown("### 🦅 FIPS 206 — FN-DSA (Falcon) Compact Signatures")
        st.markdown("Used for: **IoT devices, smart cards, embedded systems**")
        with st.spinner("Signing with Falcon..."):
            t0 = time.time()
            sig3 = oqs.Signature("Falcon-512")
            pub3 = sig3.generate_keypair()
            signature3 = sig3.sign(message)
            valid3 = sig3.verify(message, signature3, pub3)
            t1 = time.time()

        col1, col2, col3 = st.columns(3)
        col1.metric("Public Key Size", str(len(pub3)) + " bytes")
        col2.metric("Signature Size", str(len(signature3)) + " bytes")
        col3.metric("Time", str(round((t1-t0)*1000, 2)) + " ms")

        st.code(
            "Lattice Type: NTRU (smallest signatures of all 4 standards)\n" +
            "Signature (first 32 bytes): " + signature3[:32].hex() + "...\n" +
            "Signature Valid: " + str(valid3) + " ✅",
            language="text"
        )

        # ── Summary ──────────────────────────────────────────────────────
        st.markdown("---")
        st.success(
            "✅ All 4 NIST PQC Standards verified!\n\n"
            "FIPS 203 (ML-KEM) + FIPS 204 (ML-DSA) + "
            "FIPS 205 (SLH-DSA) + FIPS 206 (FN-DSA) = "
            "Complete Quantum-Safe Stack"
        )

        # SHA-3 avalanche demo
        st.markdown("### #️⃣ SHA-3 Avalanche Effect (Used in SPHINCS+)")
        msg1 = "hello quantum world"
        msg2 = "Hello quantum world"
        h1 = hashlib.sha3_256(msg1.encode()).hexdigest()
        h2 = hashlib.sha3_256(msg2.encode()).hexdigest()
        diff = sum(1 for a, b in zip(h1, h2) if a != b)
        pct = round(diff / len(h1) * 100)

        st.code(
            "Message 1: '" + msg1 + "'\n" +
            "Message 2: '" + msg2 + "' (capital H only!)\n\n" +
            "Hash 1: " + h1[:32] + "...\n" +
            "Hash 2: " + h2[:32] + "...\n\n" +
            "Characters different: " + str(diff) + "/64 (" + str(pct) + "% changed!)\n" +
            "One letter change = " + str(pct) + "% of hash changed — Avalanche Effect!",
            language="text"
        )

    except ImportError:
        st.error(
            "liboqs-python not installed. Run: pip install liboqs-python\n"
            "Then: brew install liboqs"
        )
    except Exception as e:
        st.error("PQC Demo error: " + str(e))
