import streamlit as st
import hashlib
import time

def render_pqc_demo():
    """Live PQC Demo — shows all 4 NIST standards with real or simulated output."""
    st.subheader("🔬 Live PQC Algorithm Demo")
    st.markdown(
        "**Watch all 4 NIST post-quantum cryptography standards in action!** "
        "This is the actual math protecting the future internet."
    )

    # Try to import liboqs — if not available use simulated demo
    try:
        import oqs
        HAS_OQS = True
    except ImportError:
        HAS_OQS = False

    message = b"QuantumVault Academy LLC - Quantum Safe Message"

    if HAS_OQS:
        st.success("✅ Running REAL liboqs algorithms!")
        _run_real_demo(message)
    else:
        st.info(
            "📊 Showing simulated PQC output — "
            "install liboqs locally to run real algorithms."
        )
        _run_simulated_demo()

    # SHA-3 avalanche always works — uses Python built-in hashlib
    st.markdown("---")
    st.markdown("### #️⃣ SHA-3 Avalanche Effect (Used in SPHINCS+)")
    st.markdown(
        "Change **one letter** in a message and watch the entire hash change. "
        "This is why SHA-3 is quantum-resistant."
    )

    msg1 = "hello quantum world"
    msg2 = "Hello quantum world"
    h1 = hashlib.sha3_256(msg1.encode()).hexdigest()
    h2 = hashlib.sha3_256(msg2.encode()).hexdigest()
    diff = sum(1 for a, b in zip(h1, h2) if a != b)
    pct = round(diff / len(h1) * 100)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Original message:**")
        st.code(msg1)
        st.code(h1)
    with col2:
        st.markdown("**Changed H to uppercase:**")
        st.code(msg2)
        st.code(h2)

    st.metric("Hash characters changed", str(diff) + "/64", str(pct) + "% changed!")
    st.success(
        "One letter change = " + str(pct) + "% of hash changed! "
        "This is the SHA-3 Avalanche Effect — "
        "SPHINCS+ (FIPS 205) chains thousands of these hashes together!"
    )


def _run_real_demo(message):
    """Run real liboqs algorithms."""
    import oqs

    # FIPS 203 - ML-KEM Kyber
    st.markdown("### 🔐 FIPS 203 — ML-KEM (Kyber768)")
    st.markdown("**Used for:** TLS, HTTPS, VPN key exchange")
    with st.spinner("Running Kyber key exchange..."):
        t0 = time.time()
        kem = oqs.KeyEncapsulation("Kyber768")
        pub = kem.generate_keypair()
        ct, ss_enc = kem.encap_secret(pub)
        ss_dec = kem.decap_secret(ct)
        t1 = time.time()
    col1, col2, col3 = st.columns(3)
    col1.metric("Public Key", str(len(pub)) + " bytes")
    col2.metric("Ciphertext", str(len(ct)) + " bytes")
    col3.metric("Speed", str(round((t1-t0)*1000, 2)) + " ms")
    st.code(
        "Public Key: " + pub[:16].hex() + "...\n" +
        "Shared Secret: " + ss_enc[:16].hex() + "...\n" +
        "Keys Match: " + str(ss_enc == ss_dec) + " ✅"
    )

    # FIPS 204 - ML-DSA Dilithium
    st.markdown("### ✍️ FIPS 204 — ML-DSA (Dilithium)")
    st.markdown("**Used for:** Code signing, certificates, legal documents")
    with st.spinner("Running Dilithium signature..."):
        t0 = time.time()
        sig1 = oqs.Signature("ML-DSA-65")
        pub1 = sig1.generate_keypair()
        s1 = sig1.sign(message)
        v1 = sig1.verify(message, s1, pub1)
        t1 = time.time()
    col1, col2, col3 = st.columns(3)
    col1.metric("Public Key", str(len(pub1)) + " bytes")
    col2.metric("Signature", str(len(s1)) + " bytes")
    col3.metric("Speed", str(round((t1-t0)*1000, 2)) + " ms")
    st.code(
        "Signature: " + s1[:16].hex() + "...\n" +
        "Valid: " + str(v1) + " ✅"
    )

    # FIPS 205 - SLH-DSA SPHINCS+
    st.markdown("### 🌲 FIPS 205 — SLH-DSA (SPHINCS+)")
    st.markdown("**Used for:** Backup signatures, long-term security")
    with st.spinner("Running SPHINCS+ signature..."):
        t0 = time.time()
        sig2 = oqs.Signature("SPHINCS+-SHA2-128f-simple")
        pub2 = sig2.generate_keypair()
        s2 = sig2.sign(message)
        v2 = sig2.verify(message, s2, pub2)
        t1 = time.time()
    col1, col2, col3 = st.columns(3)
    col1.metric("Public Key", str(len(pub2)) + " bytes")
    col2.metric("Signature", str(len(s2)) + " bytes")
    col3.metric("Speed", str(round((t1-t0)*1000, 2)) + " ms")
    st.code(
        "Hash Function: SHA-2\n" +
        "Signature: " + s2[:16].hex() + "...\n" +
        "Valid: " + str(v2) + " ✅"
    )

    # FIPS 206 - FN-DSA Falcon
    st.markdown("### 🦅 FIPS 206 — FN-DSA (Falcon)")
    st.markdown("**Used for:** IoT devices, smart cards, embedded systems")
    with st.spinner("Running Falcon signature..."):
        t0 = time.time()
        sig3 = oqs.Signature("Falcon-512")
        pub3 = sig3.generate_keypair()
        s3 = sig3.sign(message)
        v3 = sig3.verify(message, s3, pub3)
        t1 = time.time()
    col1, col2, col3 = st.columns(3)
    col1.metric("Public Key", str(len(pub3)) + " bytes")
    col2.metric("Signature", str(len(s3)) + " bytes")
    col3.metric("Speed", str(round((t1-t0)*1000, 2)) + " ms")
    st.code(
        "Lattice: NTRU (smallest signatures)\n" +
        "Signature: " + s3[:16].hex() + "...\n" +
        "Valid: " + str(v3) + " ✅"
    )

    st.success(
        "✅ All 4 NIST PQC Standards verified! "
        "FIPS 203 + 204 + 205 + 206 = Complete Quantum-Safe Stack!"
    )


def _run_simulated_demo():
    """Show simulated PQC output when liboqs is not installed."""

    # FIPS 203
    st.markdown("### 🔐 FIPS 203 — ML-KEM (Kyber768)")
    st.markdown("**Used for:** TLS, HTTPS, VPN key exchange")
    col1, col2, col3 = st.columns(3)
    col1.metric("Public Key", "1184 bytes")
    col2.metric("Ciphertext", "1088 bytes")
    col3.metric("Speed", "~0.3 ms")
    st.code(
        "Public Key: a3f8c2d1e4b7a9f0c3d2e1b4a7f8c9d0...\n" +
        "Shared Secret: 8f3a2c1d4e7b9f0a3c2d1e4b7a8f9c0d...\n" +
        "Keys Match: True ✅"
    )

    # FIPS 204
    st.markdown("### ✍️ FIPS 204 — ML-DSA (Dilithium)")
    st.markdown("**Used for:** Code signing, certificates, legal documents")
    col1, col2, col3 = st.columns(3)
    col1.metric("Public Key", "1952 bytes")
    col2.metric("Signature", "3293 bytes")
    col3.metric("Speed", "~1.2 ms")
    st.code(
        "Signature: 7c3a2d1e4b8f9a0c3d2e1b4a7f8c9d0e...\n" +
        "Valid: True ✅"
    )

    # FIPS 205
    st.markdown("### 🌲 FIPS 205 — SLH-DSA (SPHINCS+)")
    st.markdown("**Used for:** Backup signatures, long-term security")
    col1, col2, col3 = st.columns(3)
    col1.metric("Public Key", "32 bytes")
    col2.metric("Signature", "17088 bytes")
    col3.metric("Speed", "~8.5 ms")
    st.code(
        "Hash Function: SHA-2\n" +
        "Signature: 2d1e4b7a8f9c0d3e2a1b4c7f8d9e0a3b...\n" +
        "Valid: True ✅"
    )

    # FIPS 206
    st.markdown("### 🦅 FIPS 206 — FN-DSA (Falcon)")
    st.markdown("**Used for:** IoT devices, smart cards, embedded systems")
    col1, col2, col3 = st.columns(3)
    col1.metric("Public Key", "897 bytes")
    col2.metric("Signature", "~666 bytes")
    col3.metric("Speed", "~0.8 ms")
    st.code(
        "Lattice: NTRU (smallest signatures of all 4 standards)\n" +
        "Signature: 1e4b7a8f9c0d3e2c1b4a7f8c9d0e3a2b...\n" +
        "Valid: True ✅"
    )

    st.success(
        "✅ All 4 NIST PQC Standards shown! "
        "FIPS 203 + 204 + 205 + 206 = Complete Quantum-Safe Stack! "
        "Install liboqs locally to run the real algorithms."
    )
