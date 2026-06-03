from modules.progress_tracker import mark_complete, is_complete
"""
modules/high_school.py
──────────────────────
Grades 9–12 learning module: "Cipher Corps"

Concepts taught:
  - NIST PQC standardization timeline
  - Algorithm comparison (RSA vs ECC vs Kyber vs Dilithium)
  - Real SHA-3/SHAKE usage as in PQC schemes
  - Guided coding exercises (simplified lattice Python)
  - Threat modeling basics
"""

import hashlib
import random
import time
import streamlit as st
from utils.security import sanitize_input, check_rate_limit

# ── XP Constants ──────────────────────────────────────────────────────────────
XP_CORRECT_ANSWER = 10
XP_STREAK_BONUS = 5
XP_BADGE_EARNED = 25
XP_SPEED_BONUS = 15
XP_VOCAB_COMPLETE = 5

# ── Helpers ───────────────────────────────────────────────────────────────────

def award_badge(badge: str, xp: int = 10):
    if badge not in st.session_state.badges:
        st.session_state.badges.append(badge)
        st.session_state.xp += xp
        from utils import play_sound, show_badge_pop
        st.markdown(play_sound("badge"), unsafe_allow_html=True)
        st.markdown(
            f'<div class="flash-correct">'
            f'{show_badge_pop("🏅")} '
            f'<strong>Badge Earned: {badge}!</strong> +{xp} XP'
            f'</div>',
            unsafe_allow_html=True
        )
        st.balloons()


# ── Main render ───────────────────────────────────────────────────────────────

def render_high_school():
    st.title("🔴 Cipher Corps — High School Edition")
    st.markdown(
        "Welcome to the advanced division. You'll work with real algorithms, "
        "real standards, and real Python code. Let's build the future of security. 🛡️"
    )

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📅 NIST Timeline",
        "⚖️ Algorithm Lab",
        "💻 Code It Yourself",
        "🛡️ Threat Modeler",
        "🔬 Research Journal",
        "🎮 Tower Defense",
        "🧮 Math Challenge",
    ])

    # ── Tab 1: NIST PQC Timeline ──────────────────────────────────────────────
    with tab1:
        st.subheader("📅 The Road to Post-Quantum Standards")
        st.markdown(
            """
            NIST (National Institute of Standards and Technology) ran a multi-year
            competition to find quantum-resistant algorithms. Here's the timeline:
            """
        )

        timeline = [
            ("2016", "NIST opens PQC competition — 82 submissions received"),
            ("2017", "Round 1: 69 candidates pass initial screening"),
            ("2019", "Round 2: 26 candidates advance"),
            ("2020", "Round 3: 7 finalists + 8 alternates"),
            ("2022", "NIST announces 4 algorithms for standardization"),
            ("2024", "FIPS 203 (ML-KEM/Kyber), FIPS 204 (ML-DSA/Dilithium), FIPS 205 (SLH-DSA) finalized"),
            ("2025+", "Industry migration begins — TLS, SSH, and VPNs upgrading"),
        ]

        for year, event in timeline:
            col1, col2 = st.columns([1, 5])
            with col1:
                st.markdown(f"**{year}**")
            with col2:
                st.markdown(f"→ {event}")

        st.markdown("---")
        st.markdown("### 🏆 The Four NIST Winners")
        winners = {
            "🔑 ML-KEM (Kyber)": "Key Encapsulation Mechanism — for encrypting data",
            "✍️ ML-DSA (Dilithium)": "Digital Signature — for verifying identity",
            "✍️ SLH-DSA (SPHINCS+)": "Hash-based Digital Signature — backup standard",
            "✍️ FN-DSA (FALCON)": "Compact lattice signature — for constrained devices",
        }
        for name, desc in winners.items():
            st.info(f"**{name}** — {desc}")

        quiz_ans = st.radio(
            "❓ Which NIST standard is used for KEY EXCHANGE?",
            ["ML-DSA (Dilithium)", "SLH-DSA (SPHINCS+)", "ML-KEM (Kyber)", "RSA-4096"],
            key="nist_quiz",
        )
        if st.button("Check Answer", key="nist_check"):
            if quiz_ans == "ML-KEM (Kyber)":
                st.success("✅ Correct! ML-KEM (formerly CRYSTALS-Kyber) handles key encapsulation.")
                award_badge("📅 NIST Scholar", xp=20)
            else:
                st.error("❌ Not quite. Hint: KEM = Key Encapsulation Mechanism.")

    # ── Tab 2: Algorithm Comparison Lab ──────────────────────────────────────
    with tab2:
        st.subheader("⚖️ Algorithm Comparison Lab")
        st.markdown("Compare classical and post-quantum algorithms side by side:")

        algo_data = {
            "Algorithm": ["RSA-2048", "ECC-256", "ML-KEM-512", "ML-KEM-768", "ML-KEM-1024"],
            "Type": ["Classical", "Classical", "Post-Quantum", "Post-Quantum", "Post-Quantum"],
            "Security Level (bits)": [112, 128, 128, 192, 256],
            "Public Key Size (bytes)": [256, 64, 800, 1184, 1568],
            "Ciphertext Size (bytes)": [256, 96, 768, 1088, 1568],
            "Quantum Safe?": ["❌ No", "❌ No", "✅ Yes", "✅ Yes", "✅ Yes"],
        }

        st.dataframe(algo_data, use_container_width=True)

        st.markdown("### 📊 Key Size Visualized")
        selected = st.selectbox("Select algorithm:", algo_data["Algorithm"])
        idx = algo_data["Algorithm"].index(selected)
        pk_size = algo_data["Public Key Size (bytes)"][idx]
        ct_size = algo_data["Ciphertext Size (bytes)"][idx]

        col1, col2 = st.columns(2)
        col1.metric("Public Key", f"{pk_size} bytes", delta=f"{'Quantum Safe' if '✅' in algo_data['Quantum Safe?'][idx] else 'Vulnerable'}")
        col2.metric("Ciphertext", f"{ct_size} bytes")

        st.markdown(
            """
            > **Why are PQC keys bigger?** Lattice problems need more data to encode
            > the hard math. It's a trade-off: slightly bigger keys for quantum security.
            """
        )

        st.markdown("---")
        st.markdown("### ⚡ Quantum Computer Attack Simulator")
        st.markdown(
            "Watch what happens when a quantum computer attacks RSA vs Kyber. "
            "Click **Start Race** to see the difference in real time."
        )

        if st.button("🚀 Start Race", key="start_race"):
            import time

            col1, col2 = st.columns(2)

            with col1:
                st.error("🔑 RSA-2048")
                st.caption("Classical encryption — vulnerable to Shor's Algorithm")
                rsa_bar = st.progress(0)
                rsa_status = st.empty()

            with col2:
                st.success("🔐 ML-KEM (Kyber)")
                st.caption("Post-quantum encryption — lattice-based")
                kyber_bar = st.progress(0)
                kyber_status = st.empty()

            # ── Simulate the race ─────────────────────────────────────────
            rsa_progress = 0
            kyber_progress = 0

            for step in range(100):
                # RSA gets cracked fast by quantum (Shor's algorithm)
                rsa_progress = min(100, rsa_progress + 4)

                # Kyber barely moves — quantum gets stuck on lattice math
                if step < 30:
                    kyber_progress = min(100, kyber_progress + 0.3)
                else:
                    kyber_progress = min(15, kyber_progress + 0.05)

                rsa_bar.progress(int(rsa_progress))
                kyber_bar.progress(int(kyber_progress))

                if rsa_progress < 100:
                    rsa_status.markdown(
                        f"💥 Quantum cracking... **{int(rsa_progress)}%** broken"
                    )
                else:
                    rsa_status.markdown("💀 **RSA BROKEN** — key exposed!")

                if kyber_progress < 15:
                    kyber_status.markdown(
                        f"🛡️ Quantum stuck on lattice... **{int(kyber_progress)}%** progress"
                    )
                else:
                    kyber_status.markdown("✅ **Kyber HOLDING** — quantum computer lost!")

                time.sleep(0.05)

            # ── Final verdict ─────────────────────────────────────────────
            st.markdown("---")
            verdict_col1, verdict_col2 = st.columns(2)
            with verdict_col1:
                st.error(
                    "❌ **RSA Result**\n\n"
                    "Broken in minutes by a cryptographically-relevant "
                    "quantum computer using Shor's Algorithm."
                )
            with verdict_col2:
                st.success(
                    "✅ **Kyber Result**\n\n"
                    "Quantum computer made less than 15% progress. "
                    "Lattice problems remain hard even for quantum!"
                )
            st.balloons()
            mark_complete("quantum_race_hs")
            award_badge("⚡ Quantum Race Champion", xp=30)

        if st.button("⚖️ I understand the trade-offs!", key="lab_done"):
            award_badge("⚖️ Algorithm Analyst", xp=25)

    # ── Tab 3: Code It Yourself ───────────────────────────────────────────────
    with tab3:
        st.subheader("💻 Code It Yourself — Simplified Lattice in Python")
        st.markdown(
            """
            Below is real, runnable Python that demonstrates the CORE IDEA of
            Learning With Errors (LWE) — the math problem underlying Kyber.
            You can paste this directly into VS Code!
            """
        )

        lwe_code = '''"""
Simplified LWE (Learning With Errors) Demo
============================================
This is NOT production cryptography — it's a teaching tool.
For real PQC, use: pip install liboqs-python
"""
import random

MOD = 97  # Small prime modulus (real Kyber uses 3329)
N   = 4   # Dimension  (real Kyber uses 256)


def gen_secret(n: int, mod: int) -> list[int]:
    """Generate a random secret vector s."""
    return [random.randint(0, mod - 1) for _ in range(n)]


def gen_public_key(s: list[int], mod: int) -> tuple[list[list[int]], list[int]]:
    """
    Public key = (A, b) where b = A*s + e  (mod p)
    A is a random matrix, e is a small noise vector.
    """
    n = len(s)
    A = [[random.randint(0, mod - 1) for _ in range(n)] for _ in range(n)]
    e = [random.randint(-2, 2) for _ in range(n)]          # small noise
    b = [(sum(A[i][j] * s[j] for j in range(n)) + e[i]) % mod for i in range(n)]
    return A, b


def encrypt(A, b, message_bit: int, mod: int) -> tuple[list[int], int]:
    """Encrypt a single bit (0 or 1) using the public key."""
    n = len(b)
    r  = [random.randint(0, 1) for _ in range(n)]      # random vector
    e1 = [random.randint(-1, 1) for _ in range(n)]     # noise
    e2 = random.randint(-1, 1)

    u = [(sum(A[j][i] * r[j] for j in range(n)) + e1[i]) % mod for i in range(n)]
    v = (sum(b[i] * r[i] for i in range(n)) + e2 + (mod // 2) * message_bit) % mod
    return u, v


def decrypt(s: list[int], u: list[int], v: int, mod: int) -> int:
    """Decrypt using secret key — noise cancels out, message emerges."""
    noisy = (v - sum(s[i] * u[i] for i in range(len(s)))) % mod
    # If noisy ≈ 0 → bit was 0;  if noisy ≈ mod//2 → bit was 1
    return 1 if abs(noisy - mod // 2) < mod // 4 else 0


if __name__ == "__main__":
    secret = gen_secret(N, MOD)
    A, b   = gen_public_key(secret, MOD)

    for bit in [0, 1]:
        u, v     = encrypt(A, b, bit, MOD)
        recovered = decrypt(secret, u, v, MOD)
        status   = "✅" if recovered == bit else "❌"
        print(f"Sent: {bit}  |  Received: {recovered}  {status}")
'''

        st.code(lwe_code, language="python")

        # Run a live demo
        if st.button("▶️ Run Demo Live", key="run_lwe"):
            MOD, N = 97, 4

            def gen_secret(n, mod): return [random.randint(0, mod - 1) for _ in range(n)]

            def gen_pk(s, mod):
                n = len(s)
                A = [[random.randint(0, mod - 1) for _ in range(n)] for _ in range(n)]
                e = [random.randint(-2, 2) for _ in range(n)]
                b = [(sum(A[i][j] * s[j] for j in range(n)) + e[i]) % mod for i in range(n)]
                return A, b

            def enc(A, b, m, mod):
                n = len(b)
                r  = [random.randint(0, 1) for _ in range(n)]
                e1 = [random.randint(-1, 1) for _ in range(n)]
                e2 = random.randint(-1, 1)
                u  = [(sum(A[j][i] * r[j] for j in range(n)) + e1[i]) % mod for i in range(n)]
                v  = (sum(b[i] * r[i] for i in range(n)) + e2 + (mod // 2) * m) % mod
                return u, v

            def dec(s, u, v, mod):
                noisy = (v - sum(s[i] * u[i] for i in range(len(s)))) % mod
                return 1 if abs(noisy - mod // 2) < mod // 4 else 0

            sk = gen_secret(N, MOD)
            A, b = gen_pk(sk, MOD)
            results = []
            for bit in [0, 1]:
                u, v = enc(A, b, bit, MOD)
                rec  = dec(sk, u, v, MOD)
                results.append((bit, rec, rec == bit))

            for sent, recv, ok in results:
                icon = "✅" if ok else "❌"
                st.write(f"{icon} Sent: `{sent}` → Received: `{recv}`")

            award_badge("💻 LWE Coder", xp=35)

    # ── Tab 4: Threat Modeler ─────────────────────────────────────────────────
    with tab4:
        st.subheader("🛡️ Threat Modeling Simulator")
        st.markdown(
            "Design a secure system by choosing the right algorithms. "
            "Then defend against a simulated attack!"
        )

        col1, col2 = st.columns(2)
        with col1:
            key_algo = st.selectbox("Key Exchange Algorithm:", ["RSA-2048", "ECDH", "ML-KEM-768"])
            sig_algo = st.selectbox("Signature Algorithm:", ["RSA-PSS", "ECDSA", "ML-DSA-65"])
            hash_algo = st.selectbox("Hash Function:", ["SHA-256", "SHA3-256", "SHAKE-256"])

        with col2:
            attacker = st.selectbox("Attacker type:", [
                "Classical hacker (today)",
                "Nation-state with classical HPC",
                "Adversary with cryptographically-relevant quantum computer (CRQC)"
            ])

        if st.button("🎯 Run Threat Assessment", key="threat_run"):
            if not check_rate_limit("threat_run", st.session_state):
                st.warning("Rate limit reached. Try again shortly.")
            else:
                crqc = "quantum" in attacker.lower()
                safe_key  = "ML-KEM" in key_algo
                safe_sig  = "ML-DSA" in sig_algo
                safe_hash = "SHA3" in hash_algo or "SHAKE" in hash_algo

                st.markdown("### 🔍 Assessment Report")
                results = {
                    "Key Exchange": ("✅ Quantum-Safe" if safe_key else "❌ BROKEN by CRQC" if crqc else "⚠️ Vulnerable in future"),
                    "Signatures":   ("✅ Quantum-Safe" if safe_sig else "❌ BROKEN by CRQC" if crqc else "⚠️ Vulnerable in future"),
                    "Hashing":      ("✅ Sufficient" if safe_hash or not crqc else "⚠️ Grover halves security"),
                }
                all_safe = all("✅" in v for v in results.values())
                for area, verdict in results.items():
                    st.write(f"**{area}:** {verdict}")

                if all_safe:
                    st.success("🎉 Your system is quantum-resistant! Well designed.")
                    award_badge("🛡️ Threat Modeler", xp=40)
                elif crqc:
                    st.error(
                        "💥 A quantum adversary broke into your system. "
                        "Switch to ML-KEM + ML-DSA + SHA3 to be safe!"
                    )
                else:
                    st.warning("Your system is safe today but should migrate to PQC soon.")

    # ── Tab 5: Research Journal ───────────────────────────────────────────────
    with tab5:
        st.subheader("🔬 Research Journal")
        st.markdown("Record your notes and learnings. Export them when you're done!")

        entry = st.text_area(
            "Write your research entry:",
            placeholder="What I learned about post-quantum cryptography today...",
            max_chars=2000,
            height=200,
            key="journal_entry",
        )
        topic = st.text_input("Topic/Title:", max_chars=80, key="journal_topic")

        if st.button("💾 Save Entry", key="journal_save"):
            if not check_rate_limit("journal_save", st.session_state):
                st.warning("Save rate limit reached. Wait a moment.")
            else:
                clean_entry = sanitize_input(entry, max_length=2000)
                clean_topic = sanitize_input(topic, max_length=80)
                if len(clean_entry) < 20:
                    st.warning("Write at least a sentence or two!")
                else:
                    if "journal" not in st.session_state:
                        st.session_state.journal = []
                    st.session_state.journal.append({
                        "topic": clean_topic or "Untitled",
                        "entry": clean_entry,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M"),
                    })
                    st.success("✅ Entry saved!")
                    award_badge("🔬 PQC Researcher", xp=15)

        if "journal" in st.session_state and st.session_state.journal:
            st.markdown("---")
            st.markdown("### 📚 Your Entries")
            for j in reversed(st.session_state.journal):
                with st.expander(f"📝 {j['topic']} — {j['timestamp']}"):
                    st.write(j["entry"])

    with tab6:
        from modules.games import render_tower_defense, render_zombie_blast, render_quantumcraft_highschool
        game_choice = st.radio("Pick a game:", ["🛡️ Tower Defense", "🧟 Zombie Blast", "🏃 Cipher Ruins"], horizontal=True)
        if game_choice == "🛡️ Tower Defense":
            render_tower_defense()
        elif game_choice == "🧟 Zombie Blast":
            render_zombie_blast(difficulty="hard")
        else:
            render_quantumcraft_highschool()
    with tab7:
        st.subheader("🧮 QuantumMath Challenge")
        xp = st.session_state.xp
        LEVELS = [
            {"name": "Level 1 - Modular Arithmetic",  "xp_required": 0,    "color": "#10b981", "emoji": "🔢"},
            {"name": "Level 2 - Prime Numbers",        "xp_required": 50,   "color": "#3b82f6", "emoji": "🔑"},
            {"name": "Level 3 - Matrix Math",          "xp_required": 150,  "color": "#8b5cf6", "emoji": "🏗"},
            {"name": "Level 4 - Number Theory",        "xp_required": 300,  "color": "#f59e0b", "emoji": "📐"},
            {"name": "Level 5 - Lattice Problems",     "xp_required": 500,  "color": "#ec4899", "emoji": "⚡"},
            {"name": "Level 6 - Hash Functions",       "xp_required": 700,  "color": "#06b6d4", "emoji": "🔢"},
            {"name": "Level 7 - Digital Signatures",   "xp_required": 900,  "color": "#f97316", "emoji": "✍️"},
            {"name": "Level 8 - Kyber Deep Dive",      "xp_required": 1100, "color": "#a855f7", "emoji": "🔐"},
            {"name": "Level 9 - Quantum Algorithms",   "xp_required": 1300, "color": "#ef4444", "emoji": "⚛️"},
            {"name": "Level 10 - Advanced LWE",        "xp_required": 1500, "color": "#14b8a6", "emoji": "🧮"},
            {"name": "Level 11 - NIST Standards",      "xp_required": 1800, "color": "#eab308", "emoji": "🏛️"},
            {"name": "Level 12 - Grandmaster PQC",     "xp_required": 2000, "color": "#4f46e5", "emoji": "🛡️"},
        ]
        available = [l for l in LEVELS if xp >= l["xp_required"]]
        if not available:
            st.warning("Earn XP in other modules to unlock math challenges!")
        else:
            selected = st.selectbox("Choose a level:", [l["name"] for l in available], key="math_sel")
            idx = next(i for i, l in enumerate(LEVELS) if l["name"] == selected)
            lvl = LEVELS[idx]
            color = lvl["color"]

            BODIES = [
                ("Modular Arithmetic - Clock Math",
                 """**What is Modular Arithmetic?**

Modular arithmetic is clock math. On a 12-hour clock, 10 + 5 = 3 not 15 because numbers wrap around.

**The formula:** a mod b = the remainder when a is divided by b

**Examples:**
- 17 mod 5 = 2 because 17 = 3x5 + 2
- 25 mod 7 = 4 because 25 = 3x7 + 4
- 22 mod 11 = 0 wraps around perfectly

**Key concepts you will be tested on:**
- Basic mod calculations
- Modular addition and multiplication
- Modular inverse: find x where a times x is congruent to 1 mod n
- Modular exponentiation: computing a to the power b mod n""",
                 "ALL cryptography uses modular arithmetic! RSA encrypts using m^e mod n. Kyber does lattice math mod q=3329. Without mod arithmetic there is no crypto!"),
                ("Prime Numbers - Foundation of RSA",
                 """**What are Prime Numbers?**

A prime number has exactly two factors: 1 and itself.
Examples: 2, 3, 5, 7, 11, 13, 17, 19...

The number 4 is NOT prime because 4 = 2 times 2.

**Prime factorization:** Every number breaks into unique prime factors
- 60 = 2 times 2 times 3 times 5
- 35 = 5 times 7

**The big idea:** Multiplying two primes is EASY. Finding which primes were multiplied (factoring) is HARD for large numbers!

**Key concepts you will be tested on:**
- Identifying prime numbers
- Prime factorization
- Fermat Little Theorem
- Relatively prime numbers: gcd(a,b) = 1""",
                 "RSA security depends on prime factoring being hard! RSA uses n=p times q where p and q are secret 512-digit primes. A quantum computer running Shor Algorithm factors n and breaks RSA in hours. Kyber avoids primes entirely!"),
                ("Matrix Math - The Language of Lattices",
                 """**What are Matrices?**

A matrix is a rectangular grid of numbers. A vector is a single row or column of numbers.

**Dot product:** [1,2] dot [3,4] = 1 times 3 + 2 times 4 = 11

**The LWE equation:**
b = A times s + e
Where A is a public matrix, s is the secret vector, e is small noise.

**Key concepts you will be tested on:**
- Dot products and matrix multiplication
- Matrix dimensions and shapes
- Transpose: flipping rows and columns
- Identity matrix
- Linear independence
- Determinants""",
                 "Kyber public key IS a matrix! Key generation computes b = A times s + e mod q. Given A and b, finding s in 1000+ dimensions is impossible even for quantum computers. This is the LWE problem!"),
                ("Number Theory - Deep Integer Math",
                 """**What is Number Theory?**

Number theory studies integers and their deep properties.

**Euler totient phi(n):** Count of integers less than n that share no factors with n
- phi(8) = 4 because numbers 1, 3, 5, 7 are coprime to 8
- phi(p) = p-1 for any prime p

**Abstract algebra:**
- Group: set with one operation following specific rules
- Ring: set with + and times like polynomial rings in Kyber
- Field: ring where division is always possible

**Key concepts you will be tested on:**
- Euler totient function
- Chinese Remainder Theorem
- Discrete logarithm problem
- Groups, rings, and fields""",
                 "Kyber works in the polynomial ring Zq[x] divided by (x^n+1). This ring structure makes computation fast while keeping the lattice problem hard. RSA uses Euler totient phi(n)=(p-1)(q-1) computable only if you know the secret primes!"),
                ("Lattice Problems - The Future of Crypto",
                 """**What are Lattice Problems?**

A lattice is an infinite grid of points in multi-dimensional space.

**SVP (Shortest Vector Problem):** Find the shortest nonzero vector in a lattice
- In 2D: easy to solve
- In 1000 dimensions: computationally impossible

**LWE (Learning With Errors):**
Given noisy equations A times s + e = b, find secret s.
The noise e makes this impossible to reverse!

**Why quantum-safe?**
- No quantum algorithm gives significant speedup on SVP
- Grover gives at most square root speedup - not enough
- Shor Algorithm does not help at all

**Key concepts you will be tested on:**
- SVP and CVP hardness
- LWE and MLWE problems
- Kyber key sizes and security levels
- Why Grover gives only quadratic speedup""",
                 "This IS the math behind Kyber, Dilithium, and Falcon! NIST chose lattice crypto because SVP and LWE have no known quantum speedup. Shor Algorithm does not help. Grover gives only square root speedup - not enough to break 256-bit lattice security!"),
                ("Hash Functions - SHA-3 and Keccak",
                 """**What is a Hash Function?**

A cryptographic hash function maps any input to a fixed-size output called a digest.

**SHA-3 Properties:**
- One-way: cannot reverse hash to get input
- Deterministic: same input always gives same hash
- Avalanche effect: changing one bit changes ~50% of output
- Collision resistant: impossible to find two inputs with same hash

**SHA-3 (Keccak) Structure:**
- Uses a sponge construction with 5x5x64 state matrix
- Absorb phase: XOR input blocks into state
- Squeeze phase: output hash from state
- Permutation: 24 rounds of theta, rho, pi, chi, iota

**Security levels:**
- SHA3-256: 128-bit quantum security
- SHA3-384: 192-bit quantum security  
- SHA3-512: 256-bit quantum security

**PQC Connection:** SPHINCS+ uses hash functions as its security foundation!""",
                 "SHA-3 is quantum-resistant because Grover only gives sqrt speedup. SHA3-256 has 128-bit quantum security — still strong enough for most applications!"),
                ("Digital Signatures - Dilithium and Falcon",
                 """**What is a Digital Signature?**

A digital signature proves: (1) the message came from the claimed sender, and (2) the message was not modified.

**Classical vs Post-Quantum:**
- RSA signatures: based on prime factoring — broken by Shor
- ECDSA signatures: based on discrete log — broken by Shor
- Dilithium (ML-DSA): based on Module LWE — quantum safe!
- Falcon (FN-DSA): based on NTRU lattices — quantum safe!

**How Dilithium Signs:**
1. Generate random nonce y
2. Compute w = Ay mod q
3. Compute challenge c = H(w, message)
4. Compute response z = y + cs
5. If z is too large, reject and retry (rejection sampling!)

**Falcon vs Dilithium:**
- Falcon signatures are 3x smaller than Dilithium
- Falcon requires Gaussian sampling (harder to implement)
- Dilithium is simpler and safer to implement correctly""",
                 "Rejection sampling in Dilithium prevents secret key leakage — without it, an attacker could recover the private key from enough signatures!"),
                ("Kyber Deep Dive - CRYSTALS Architecture",
                 """**Kyber Internal Structure**

Kyber uses Module-LWE over polynomial ring Rq = Zq[x]/(x^n + 1)

**Parameters:**
- Kyber-512: n=256, k=2, q=3329 → 128-bit security
- Kyber-768: n=256, k=3, q=3329 → 192-bit security
- Kyber-1024: n=256, k=4, q=3329 → 256-bit security

**Number Theoretic Transform (NTT):**
Kyber uses NTT for fast polynomial multiplication
- Naive: O(n²) multiplications
- NTT: O(n log n) multiplications — 100x faster!

**Key Generation:**
1. A ← sample matrix of polynomials mod q
2. s, e ← sample small polynomials (noise)
3. t = As + e (public key = noisy product)

**Encapsulation:**
1. r, e1, e2 ← sample small polynomials
2. u = A^T r + e1
3. v = t^T r + e2 + encode(m)
4. Ciphertext = (u, v)

**Why secure:** Recovering m requires finding s from t = As + e""",
                 "The NTT transform is what makes Kyber fast enough for real-world use. Without NTT, polynomial multiplication would be too slow for TLS handshakes!"),
                ("Quantum Algorithms - Shor and Grover",
                 """**Shor's Algorithm (1994)**

Breaks RSA and ECC by factoring large numbers on quantum computers.

**How it works:**
1. Choose random a coprime to n
2. Use quantum phase estimation to find period r of f(x) = a^x mod n
3. If r is even: gcd(a^(r/2) ± 1, n) gives factors of n!

**Complexity:**
- Classical best: O(exp(n^(1/3))) — super-exponential
- Shor on quantum: O(n³) — polynomial!

**What it breaks:** RSA, DH, ECDH, ECDSA — anything based on factoring or discrete log

**Grover's Algorithm (1996)**

Speeds up unstructured search on quantum computers.

**How it works:**
1. Apply oracle that marks the solution
2. Apply diffusion operator (Grover diffusion)
3. Repeat sqrt(N) times — solution amplified!

**Complexity:**
- Classical: O(N) search
- Grover: O(sqrt(N)) — quadratic speedup only

**Impact on PQC:**
- Symmetric crypto (AES): double key size
- Hash functions (SHA-3): double output size
- Lattice crypto: minimal impact — SVP not searchable this way""",
                 "Shor breaks RSA in polynomial time — that's why we need PQC NOW. But Grover only gives quadratic speedup, so doubling hash/key sizes is sufficient defense!"),
                ("Advanced LWE - Variants and Parameters",
                 """**LWE Variants Used in NIST Standards**

**Standard LWE:**
Given A ∈ Z_q^(m×n), b = As + e mod q — find s
- s is secret vector
- e is small noise vector
- Hard when n ≥ 256 and q ≈ 3329

**Ring-LWE (RLWE):**
Operations in ring R_q = Z_q[x]/(x^n + 1)
- Faster than LWE — polynomial multiplication
- Used in early Kyber variants

**Module-LWE (MLWE):**
Uses k×k matrix of ring elements
- Combines RLWE efficiency with LWE flexibility
- Used in Kyber-512/768/1024 and Dilithium

**Learning With Rounding (LWR):**
b = round(As/p) mod q — no explicit noise!
- Rounding replaces random noise
- Used in some NIST alternate candidates

**Security Reduction:**
Worst-case SVP ≤ Average-case LWE
This means: breaking LWE is as hard as the worst possible lattice problem!

**Key insight:** MLWE security reduces to standard LWE which reduces to SVP""",
                 "The security reduction from SVP to LWE is what makes Kyber provably secure. Breaking Kyber requires solving the hardest possible lattice problem!"),
                ("NIST Standards - Complete Reference",
                 """**The Four NIST PQC Standards (2024)**

**FIPS 203 — ML-KEM (Kyber)**
- Type: Key Encapsulation Mechanism
- Security: 128/192/256-bit (Kyber-512/768/1024)
- Key sizes: 800/1184/1568 bytes (public)
- Based on: Module-LWE
- Use case: TLS key exchange, encrypted messaging

**FIPS 204 — ML-DSA (Dilithium)**
- Type: Digital Signature
- Security: 128/192/256-bit (Dilithium2/3/5)
- Signature sizes: 2420/3293/4595 bytes
- Based on: Module-LWE and Module-SIS
- Use case: Document signing, code signing

**FIPS 205 — SLH-DSA (SPHINCS+)**
- Type: Hash-based Digital Signature (backup standard)
- Security: 128/192/256-bit
- Signature sizes: 8-50 KB (varies by parameter)
- Based on: SHA-3 hash functions only
- Use case: Long-term signatures, CA certificates

**FIPS 206 — FN-DSA (Falcon)**
- Type: Compact Digital Signature
- Security: 128/256-bit (Falcon-512/1024)
- Signature sizes: 666/1280 bytes
- Based on: NTRU lattices and Gaussian sampling
- Use case: IoT devices, constrained environments

**Migration Timeline:**
- 2024: NIST publishes final standards
- 2026: Federal agencies begin migration
- 2030: All new systems must use PQC
- 2035: Legacy RSA/ECC systems fully retired""",
                 "Knowing all four NIST standards cold is your competitive advantage in any cybersecurity career. These are the algorithms that will protect the internet for the next 50 years!"),
                ("Grandmaster PQC - Comprehensive Challenge",
                 """**Grandmaster Level — All Topics Combined**

This is the ultimate QuantumVault Math Challenge covering every concept:

**Topics tested:**
1. Modular arithmetic and clock math
2. Prime numbers and factorization
3. Matrix and polynomial multiplication
4. Number theory — Euler totient, GCD, Fermat
5. Lattice problems — SVP, CVP, LWE, MLWE
6. Hash function properties — SHA-3, avalanche
7. Digital signature schemes — Dilithium, Falcon
8. Kyber internals — NTT, parameters, security
9. Quantum algorithms — Shor, Grover, complexity
10. Advanced LWE variants — RLWE, MLWE, LWR
11. NIST standards — FIPS 203/204/205/206
12. Real-world applications and migration

**You are ready for this level if:**
- You can explain LWE from first principles
- You know all four NIST PQC algorithm families
- You understand why Shor breaks RSA but not lattices
- You can compare Kyber-512 vs Kyber-1024 parameters
- You know the difference between MLWE and standard LWE

If you score 100% here you are ready for a cybersecurity career in the post-quantum era!""",
                 "Grandmaster level means you understand post-quantum cryptography better than most professional cryptographers did just 10 years ago. This knowledge will be in demand for the next 30 years!"),
            ]

            title, body, pqc = BODIES[idx]
            st.markdown(
                "<div style='background:" + color + "10;border-left:4px solid " + color + ";"
                "border-radius:0 10px 10px 0;padding:1rem 1.5rem;margin-bottom:1rem;'>"
                "<h3 style='color:" + color + ";margin:0'>" + lvl["emoji"] + " " + title + "</h3>"
                "</div>",
                unsafe_allow_html=True
            )
            st.markdown(body)
            st.info("🔐 PQC Connection: " + pqc)
            st.markdown("---")
            st.markdown("### Ready to test your knowledge?")
            st.caption("10 questions - 30 seconds each - time bonus points!")

            if st.button("▶ Start Challenge", key="math_start_btn", type="primary"):
                st.session_state.math_game_active = True
                st.session_state.math_level = idx
                st.rerun()

            if st.session_state.get("math_game_active") and st.session_state.get("math_level") == idx:
                import streamlit.components.v1 as cmath
                cmath.html("""
<style>
body{margin:0;background:#0f172a;font-family:sans-serif;color:white;padding:10px;}
.wrap{max-width:540px;margin:0 auto;}
.hud{display:flex;gap:5px;margin-bottom:8px;}
.hb{background:#1e293b;border:1px solid #334155;border-radius:8px;
padding:5px 8px;font-size:11px;font-weight:bold;color:#a5b4fc;flex:1;text-align:center;}
.qbox{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:16px;margin:6px 0;}
.qt{font-size:1.2rem;font-weight:bold;color:white;margin-bottom:5px;}
.qc{font-size:0.78rem;color:#888;margin-bottom:12px;}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:8px 0;}
.opt{padding:10px;border-radius:8px;border:2px solid #334155;cursor:pointer;
font-size:12px;font-weight:bold;background:#1e293b;color:#a5b4fc;text-align:center;}
.opt:hover{border-color:#4f46e5;}
.opt.correct{border-color:#10b981;background:rgba(16,185,129,0.2);color:#10b981;}
.opt.wrong{border-color:#ef4444;background:rgba(239,68,68,0.15);color:#ef4444;}
.fb{padding:9px;border-radius:8px;margin:5px 0;font-size:12px;text-align:center;display:none;}
.fb.ok{background:rgba(16,185,129,0.15);border:1px solid #10b981;color:#10b981;}
.fb.bad{background:rgba(239,68,68,0.12);border:1px solid #ef4444;color:#ef4444;}
.fc{background:rgba(79,70,229,0.12);border:1px solid rgba(79,70,229,0.35);
border-radius:8px;padding:7px;margin:5px 0;font-size:11px;color:#a5b4fc;text-align:center;display:none;}
.nb{width:100%;padding:11px;border-radius:8px;border:none;cursor:pointer;
font-size:13px;font-weight:bold;background:#4f46e5;color:white;margin-top:7px;display:none;}
.tb{height:5px;background:#334155;border-radius:3px;margin:5px 0;overflow:hidden;}
.tf{height:100%;border-radius:3px;background:#10b981;}
.done{background:rgba(16,185,129,0.08);border:1px solid #10b981;border-radius:12px;
padding:20px;text-align:center;display:none;}
</style>
<div class="wrap">
<div class="hud">
    <div class="hb">Score<br><b id="sc">0</b></div>
    <div class="hb">Right<br><b id="ok">0</b></div>
    <div class="hb">Wrong<br><b id="wr">0</b></div>
    <div class="hb">Time<br><b id="tm">30</b>s</div>
    <div class="hb">Q<br><b id="qn">1</b>/10</div>
</div>
<div class="tb"><div class="tf" id="tf" style="width:100%"></div></div>
<div class="qbox" id="qbox">
    <div class="qt" id="qt"></div>
    <div class="qc" id="qc"></div>
    <div class="opts" id="opts"></div>
    <div class="fb" id="fb"></div>
    <div class="fc" id="fc"></div>
    <button class="nb" id="nb" onclick="nextQ()">Next Question</button>
</div>
<div class="done" id="done">
    <div style="font-size:2.5rem">🏆</div>
    <h2 style="color:#10b981;margin:8px 0">Level Complete!</h2>
    <p id="dm" style="color:#888;margin:8px 0"></p>
    <button onclick="restart()" style="padding:9px 22px;border-radius:8px;border:none;
        cursor:pointer;background:#4f46e5;color:white;font-size:13px;font-weight:bold;">
        Play Again
    </button>
</div>
</div>
<script>
var ALL_QS=[
    // Level 1 - Modular Arithmetic
    [
    {q:"What is 17 mod 5?",opts:["2","3","4","1"],ans:0,ctx:"17 = 3x5 + 2",fact:"RSA uses mod with huge primes. Kyber uses mod q=3329!"},
    {q:"What is 25 mod 7?",opts:["3","4","2","5"],ans:1,ctx:"25 = 3x7 + 4",fact:"In Kyber all math happens mod q. This keeps numbers small!"},
    {q:"What is (13+9) mod 11?",opts:["0","2","3","1"],ans:0,ctx:"13+9=22, 22=2x11+0",fact:"Hash functions use modular addition inside SHA-3!"},
    {q:"What is 100 mod 13?",opts:["9","10","11","8"],ans:0,ctx:"100 = 7x13 + 9",fact:"Modular reduction keeps Kyber coefficients in range [0, q-1]!"},
    {q:"What is (7 x 8) mod 5?",opts:["1","2","3","4"],ans:0,ctx:"7x8=56, 56=11x5+1",fact:"Modular multiplication is used in every cryptographic operation!"},
    {q:"Which is correct: 15 mod 15 = ?",opts:["0","1","15","5"],ans:0,ctx:"Any number mod itself = 0",fact:"In Kyber, coefficients mod q=3329 wrap around at 3329!"},
    {q:"What is 2^10 mod 7?",opts:["2","3","4","1"],ans:0,ctx:"1024 mod 7 = 2",fact:"Modular exponentiation is the core of RSA encryption!"},
    {q:"If a = 5 mod 11, what is 3a mod 11?",opts:["4","5","6","3"],ans:0,ctx:"3x5=15, 15 mod 11 = 4",fact:"Linear operations mod q are used in LWE: b = as + e mod q!"},
    {q:"What is (-3) mod 7?",opts:["4","3","1","5"],ans:0,ctx:"-3 + 7 = 4",fact:"Negative mod: add modulus until positive. Used in lattice math!"},
    {q:"Kyber uses modular arithmetic with q equal to?",opts:["3329","3999","4096","2048"],ans:0,ctx:"Kyber modulus q = 3329 (prime)",fact:"3329 is chosen because it is prime and NTT-friendly!"},
    ],
    // Level 2 - Prime Numbers
    [
    {q:"Which number is prime?",opts:["97","91","87","93"],ans:0,ctx:"97 has no factors except 1 and 97",fact:"RSA uses primes with 512+ digits. Shor Algorithm breaks this!"},
    {q:"Prime factors of 15?",opts:["3 and 5","3 and 4","5 and 7","2 and 7"],ans:0,ctx:"15 = 3 x 5",fact:"RSA multiplies two primes. Shor Algorithm factors the product!"},
    {q:"What is gcd(12, 8)?",opts:["4","3","2","6"],ans:0,ctx:"gcd(12,8) = 4",fact:"gcd is used in RSA key generation and Euclidean algorithm!"},
    {q:"Which is NOT prime?",opts:["51","53","59","61"],ans:0,ctx:"51 = 3 x 17",fact:"Testing primality efficiently is crucial for RSA key generation!"},
    {q:"Fermat Little Theorem: a^p mod p = ?",opts:["a","1","0","p"],ans:0,ctx:"For prime p and a not divisible by p: a^p ≡ a mod p",fact:"Fermat Little Theorem is the basis for RSA encryption!"},
    {q:"How many primes are less than 10?",opts:["4","3","5","6"],ans:0,ctx:"Primes: 2, 3, 5, 7",fact:"The prime counting function pi(x) grows as x/ln(x)!"},
    {q:"What is the largest prime factor of 84?",opts:["7","6","4","3"],ans:0,ctx:"84 = 2x2x3x7",fact:"Integer factorization is the hard problem RSA relies on!"},
    {q:"If p=11 and q=13, what is p*q?",opts:["143","134","141","131"],ans:0,ctx:"11 x 13 = 143",fact:"In RSA, n=p*q is the public modulus. Shor factors n to find p and q!"},
    {q:"What is Euler phi(7)?",opts:["6","7","5","4"],ans:0,ctx:"phi(p) = p-1 for prime p",fact:"RSA private key uses phi(n)=(p-1)(q-1) in its computation!"},
    {q:"Which algorithm breaks RSA by factoring?",opts:["Shor","Grover","Kyber","Dilithium"],ans:0,ctx:"Shor Algorithm factors n in polynomial time on quantum computers",fact:"Shor Algorithm is why we need post-quantum cryptography now!"},
    ],
    // Level 3 - Matrix Math
    [
    {q:"Dot product of [1,2] and [3,4]?",opts:["11","10","12","8"],ans:0,ctx:"1x3 + 2x4 = 11",fact:"Kyber uses matrix-vector dot products for its public key!"},
    {q:"Matrix [[1,2],[3,4]] times vector [1,1]?",opts:["[3,7]","[1,4]","[2,6]","[4,8]"],ans:0,ctx:"[1+2, 3+4] = [3, 7]",fact:"Kyber key generation: t = As + e uses exactly this matrix mult!"},
    {q:"What is the transpose of [[1,2],[3,4]]?",opts:["[[1,3],[2,4]]","[[4,3],[2,1]]","[[2,1],[4,3]]","[[1,2],[3,4]]"],ans:0,ctx:"Rows become columns",fact:"Kyber encapsulation uses A-transpose: u = A^T r + e1!"},
    {q:"In Kyber-512, what is the matrix A dimension?",opts:["2x2","3x3","4x4","1x1"],ans:0,ctx:"Kyber-512 uses k=2, so A is a 2x2 matrix of polynomials",fact:"Larger matrix means more security: Kyber-1024 uses k=4!"},
    {q:"If A = [[2,1],[1,3]] and s = [1,2], what is As?",opts:["[4,7]","[3,6]","[5,8]","[2,4]"],ans:0,ctx:"[2*1+1*2, 1*1+3*2] = [4, 7]",fact:"This exact computation appears in Kyber key generation!"},
    {q:"What operation does NTT speed up in Kyber?",opts:["Polynomial multiplication","Matrix inversion","Hash computation","Key storage"],ans:0,ctx:"NTT = Number Theoretic Transform",fact:"NTT reduces polynomial multiplication from O(n²) to O(n log n)!"},
    {q:"In matrix multiplication AB, if A is 2x3, B must be?",opts:["3xN","2xN","Nx2","Nx3"],ans:0,ctx:"Inner dimensions must match: (2x3)(3xN) = 2xN",fact:"Kyber matrices must have compatible dimensions for key generation!"},
    {q:"What is the norm of vector [3,4]?",opts:["5","7","12","25"],ans:0,ctx:"sqrt(3²+4²) = sqrt(25) = 5",fact:"Short vector norms are central to SVP and lattice security!"},
    {q:"Polynomial (x+1)(x+2) = ?",opts:["x²+3x+2","x²+2x+2","x²+3x+1","x²+x+2"],ans:0,ctx:"FOIL: x²+2x+x+2 = x²+3x+2",fact:"Kyber works with polynomial rings: Rq = Zq[x]/(x^n+1)!"},
    {q:"In Kyber, n (polynomial degree) equals?",opts:["256","128","512","1024"],ans:0,ctx:"All Kyber variants use n=256",fact:"n=256 gives 256 coefficients per polynomial — right balance of speed and security!"},
    ],
    // Level 4 - Number Theory
    [
    {q:"Euler totient of prime p equals?",opts:["p-1","p","p+1","p/2"],ans:0,ctx:"All numbers 1 to p-1 are coprime to prime p",fact:"RSA uses phi(n)=(p-1)(q-1). Only computable if you know p and q!"},
    {q:"What is gcd(35, 14)?",opts:["7","5","14","2"],ans:0,ctx:"35=5x7, 14=2x7, gcd=7",fact:"Euclidean algorithm computes gcd efficiently — used in RSA!"},
    {q:"Modular inverse of 3 mod 7?",opts:["5","4","6","2"],ans:0,ctx:"3 x 5 = 15 = 2x7+1, so 3x5≡1 mod 7",fact:"Modular inverse is used in RSA decryption and lattice algorithms!"},
    {q:"Chinese Remainder Theorem solves?",opts:["Simultaneous modular equations","Prime factorization","Matrix inversion","Hash collisions"],ans:0,ctx:"CRT: given x≡a mod m and x≡b mod n, find x",fact:"NTT in Kyber uses CRT for fast polynomial evaluation!"},
    {q:"What is Euler phi(15)?",opts:["8","6","10","4"],ans:0,ctx:"phi(15)=phi(3)xphi(5)=2x4=8",fact:"RSA security relies on phi(n) being hard to compute without knowing p,q!"},
    {q:"Quadratic residue of 4 mod 11 is?",opts:["5","4","6","3"],ans:0,ctx:"2²=4, 3²=9, 4²=16≡5, so 4 is QR with sqrt=2",fact:"Quadratic residues appear in Falcon signature generation!"},
    {q:"Extended Euclidean algorithm computes?",opts:["gcd and Bezout coefficients","Only gcd","Only modular inverse","Prime factors"],ans:0,ctx:"Bezout: gcd(a,b) = ax + by",fact:"Extended Euclidean algorithm is used to compute RSA private keys!"},
    {q:"What is Fermat Little Theorem used for?",opts:["Primality testing","Factoring","Hashing","Signatures"],ans:0,ctx:"a^(p-1) ≡ 1 mod p for prime p",fact:"Miller-Rabin primality test uses Fermat Little Theorem!"},
    {q:"If p=7, what is the multiplicative order of 3 mod 7?",opts:["6","3","7","2"],ans:0,ctx:"3^6≡1 mod 7, no smaller power works",fact:"Multiplicative order relates to the period found by Shor Algorithm!"},
    {q:"Discrete logarithm problem: find x where 2^x≡3 mod 7. Hard because?",opts:["No efficient classical algorithm","Computers are slow","Numbers are too big","Math is wrong"],ans:0,ctx:"DLP: given g^x mod p, find x",fact:"DLP is the basis of Diffie-Hellman and ECDH — both broken by Shor!"},
    ],
    // Level 5 - Lattice Problems
    [
    {q:"What makes SVP hard in 1000 dimensions?",opts:["No efficient algorithm exists","Computers are too slow","The math is wrong","Quantum helps a lot"],ans:0,ctx:"SVP = Shortest Vector Problem",fact:"SVP hardness is exactly why Kyber is quantum-safe!"},
    {q:"Grover Algorithm gives what speedup on search?",opts:["Square root speedup","Exponential speedup","No speedup","Doubles the speed"],ans:0,ctx:"Grover searches N items in sqrt(N) steps",fact:"Grover gives sqrt speedup only. Not enough to break 256-bit lattice crypto!"},
    {q:"In LWE: b = As + e, what is e?",opts:["Small noise vector","The secret","Public key","The message"],ans:0,ctx:"LWE = Learning With Errors",fact:"The noise e is what makes LWE impossible to solve!"},
    {q:"What is CVP (Closest Vector Problem)?",opts:["Find lattice point nearest to target","Find shortest lattice vector","Factor a large number","Solve linear equations"],ans:0,ctx:"CVP: given lattice L and target t, find closest v in L to t",fact:"CVP is NP-hard in general — the basis of lattice crypto security!"},
    {q:"Kyber security reduces to which hard problem?",opts:["Module-LWE","RSA factoring","Discrete log","SAT problem"],ans:0,ctx:"MLWE hardness ≤ RLWE hardness ≤ SVP hardness",fact:"Breaking Kyber requires solving the hardest lattice problems!"},
    {q:"What dimension lattices does Kyber-512 use?",opts:["256","512","128","1024"],ans:0,ctx:"Kyber-512 uses k=2 with n=256, giving 512-dimensional lattice",fact:"More dimensions = more security but larger keys!"},
    {q:"LWE noise e must be small because?",opts:["Large noise prevents decryption","Small noise is harder to find","Large keys are needed","Quantum computers need it"],ans:0,ctx:"Decryption works by rounding off the noise",fact:"If noise is too large, decryption fails! Kyber uses centered binomial distribution!"},
    {q:"Which problem did Ajtai prove reduces to lattice SVP?",opts:["SIS (Short Integer Solution)","RSA factoring","SHA-3 preimage","ECDLP"],ans:0,ctx:"SIS security reduces to worst-case SVP",fact:"SIS hardness is the basis for Dilithium signature security!"},
    {q:"Babai nearest plane algorithm solves?",opts:["CVP approximately","SVP exactly","LWE exactly","NTT efficiently"],ans:0,ctx:"Babai gives 2^n approximation to CVP",fact:"Approximate CVP algorithms are the best known attacks on lattice crypto!"},
    {q:"BKZ (Block Korkine-Zolotarev) algorithm is used for?",opts:["Lattice basis reduction","Hash computation","Polynomial multiplication","Key generation"],ans:0,ctx:"BKZ is the best known algorithm for SVP approximation",fact:"Kyber parameters are chosen so BKZ would take 2^128 operations!"},
    ],
    // Level 6 - Hash Functions
    [
    {q:"SHA-3 is based on which sponge construction?",opts:["Keccak","Merkle","Davies-Meyer","Matyas-Meyer"],ans:0,ctx:"SHA-3 uses the Keccak sponge permutation",fact:"Keccak won the NIST hash competition in 2012 defeating 64 candidates!"},
    {q:"Changing one bit of SHA-3 input changes approximately what percent of output?",opts:["50%","1%","100%","25%"],ans:0,ctx:"Avalanche effect: ~50% of output bits flip",fact:"This is the avalanche effect — essential for cryptographic security!"},
    {q:"SHA3-256 produces how many output bits?",opts:["256","512","128","384"],ans:0,ctx:"SHA3-256 name tells you the output size",fact:"256 bits gives 128-bit quantum security against Grover Algorithm!"},
    {q:"A collision in a hash function means?",opts:["Two inputs with same hash","Hash that runs slowly","Hash that is reversible","Output with all zeros"],ans:0,ctx:"Collision: H(m1) = H(m2) for m1 ≠ m2",fact:"SHA-3 is collision resistant — no known practical collisions exist!"},
    {q:"What is a preimage attack?",opts:["Find input given hash output","Find two inputs with same hash","Reverse the hash function","Find partial hash match"],ans:0,ctx:"Preimage: given h, find m such that H(m) = h",fact:"SHA-3 is preimage resistant — you cannot reverse it to find the input!"},
    {q:"SPHINCS+ uses hash functions because?",opts:["Hash security does not depend on lattices","Hash is faster than lattice math","Hashes are quantum-safe by default","All of the above"],ans:3,ctx:"SPHINCS+ security relies only on hash function properties",fact:"If lattice crypto is ever broken, SPHINCS+ backup is based on completely different math!"},
    {q:"SHA-3 internal state size is?",opts:["1600 bits","512 bits","256 bits","1024 bits"],ans:0,ctx:"SHA-3 uses a 5x5x64 bit state = 1600 bits",fact:"Large internal state provides security against length extension attacks!"},
    {q:"Merkle tree root hash proves?",opts:["Integrity of all leaves","A single file is correct","Hash is correct","Key is valid"],ans:0,ctx:"Merkle root = hash of all child nodes",fact:"SPHINCS+ uses Merkle trees internally for its signature scheme!"},
    {q:"Grover Algorithm reduces SHA3-256 security to?",opts:["128 bits","64 bits","256 bits","32 bits"],ans:0,ctx:"Grover gives sqrt speedup: 2^256 → 2^128",fact:"128-bit quantum security is considered safe for at least 30 more years!"},
    {q:"Which NIST standard uses hash functions as its security basis?",opts:["FIPS 205 (SPHINCS+)","FIPS 203 (Kyber)","FIPS 204 (Dilithium)","FIPS 206 (Falcon)"],ans:0,ctx:"SPHINCS+ = Stateless Hash-based Digital Signature",fact:"SPHINCS+ is the backup standard in case lattice problems are ever solved!"},
    ],
    // Level 7 - Digital Signatures
    [
    {q:"What does a digital signature prove?",opts:["Authenticity and integrity","Only authenticity","Only integrity","File size"],ans:0,ctx:"Signature proves who sent it and it was not modified",fact:"Digital signatures are used to sign code, documents, and SSL certificates!"},
    {q:"Dilithium is based on which hard problem?",opts:["Module-LWE","RSA factoring","SHA-3 preimage","Discrete log"],ans:0,ctx:"ML-DSA (Dilithium) = Module Lattice Digital Signature",fact:"Dilithium is FIPS 204 — one of only 4 NIST approved PQC standards!"},
    {q:"Why does Dilithium use rejection sampling?",opts:["Prevent secret key leakage","Speed up signing","Reduce signature size","Improve security level"],ans:0,ctx:"Without rejection sampling, signatures leak information about the secret key",fact:"Rejection sampling restarts if the response z is too large — preventing attacks!"},
    {q:"Falcon signatures are smaller than Dilithium because?",opts:["Uses NTRU lattices with Gaussian sampling","Uses smaller keys","Uses fewer hash rounds","Has lower security"],ans:0,ctx:"NTRU lattices allow more compact signatures",fact:"Falcon-512 signature = 666 bytes vs Dilithium2 = 2420 bytes!"},
    {q:"SPHINCS+ is considered a backup standard because?",opts:["Signatures are very large","Lower security than Dilithium","Slower key generation","Less tested"],ans:0,ctx:"SPHINCS+ signatures range from 8KB to 50KB",fact:"Large size is the tradeoff for pure hash-based security!"},
    {q:"Which NIST standard should be used for IoT signatures?",opts:["FIPS 206 (Falcon)","FIPS 204 (Dilithium)","FIPS 205 (SPHINCS+)","FIPS 203 (Kyber)"],ans:0,ctx:"Falcon has smallest signatures — best for constrained devices",fact:"IoT devices need small signatures to fit in limited memory and bandwidth!"},
    {q:"To verify a Dilithium signature you need?",opts:["Public key and message","Private key only","Hash of message","Secret noise"],ans:0,ctx:"Verification uses public key A and computes challenge",fact:"Anyone can verify but only the private key holder can sign!"},
    {q:"What is the Fiat-Shamir transform?",opts:["Converts interactive proof to signature","Converts hash to key","Converts lattice to matrix","Converts prime to polynomial"],ans:0,ctx:"Fiat-Shamir makes non-interactive signatures from interactive proofs",fact:"Dilithium uses Fiat-Shamir with Aborts (FSwA) — rejection sampling variant!"},
    {q:"Which attack does rejection sampling prevent?",opts:["Statistical key recovery","Collision attack","Length extension","Side channel"],ans:0,ctx:"Without rejection, each signature reveals bits of secret key s",fact:"After just a few signatures without rejection sampling, s could be recovered!"},
    {q:"Kyber is NOT a signature scheme because?",opts:["It is a KEM not a signature","It is too slow","It uses wrong math","NIST rejected it"],ans:0,ctx:"Kyber = Key Encapsulation Mechanism, not signature",fact:"Use Kyber for key exchange and Dilithium for signatures — different purposes!"},
    ],
    // Level 8 - Kyber Deep Dive
    [
    {q:"Kyber-768 provides how many bits of security?",opts:["192","128","256","512"],ans:0,ctx:"Kyber-512=128bit, Kyber-768=192bit, Kyber-1024=256bit",fact:"Choose security level based on how long you need data protected!"},
    {q:"NTT stands for?",opts:["Number Theoretic Transform","Nonce Token Transfer","Network Transfer Token","Noise Tolerance Test"],ans:0,ctx:"NTT = Number Theoretic Transform — fast polynomial multiplication",fact:"NTT makes Kyber 100x faster than naive polynomial multiplication!"},
    {q:"In Kyber, the public key t = As + e. What does A represent?",opts:["Public random matrix","Secret key","Noise vector","Ciphertext"],ans:0,ctx:"A is a publicly known random matrix, generated from seed",fact:"A is generated deterministically from a random seed — anyone can regenerate it!"},
    {q:"Kyber secret s has coefficients from which distribution?",opts:["Centered binomial","Uniform random","Gaussian","Binary"],ans:0,ctx:"Small coefficients from CBD(η) distribution",fact:"Small secret coefficients are what makes decryption possible!"},
    {q:"In Kyber encapsulation, what does Alice send to Bob?",opts:["Ciphertext (u,v)","Her private key","Random seed","Hash of message"],ans:0,ctx:"Encapsulation produces ciphertext c = (u, v)",fact:"The ciphertext encapsulates the shared secret — only Bob can decrypt it!"},
    {q:"What does Bob use to recover the shared secret?",opts:["His private key s","Alice public key","Random seed","Matrix A"],ans:0,ctx:"Decapsulation uses private key s: v - s^T u ≈ message/2",fact:"The noise cancels out during decryption — that is the magic of LWE!"},
    {q:"Kyber is used for which purpose in TLS 1.3?",opts:["Key exchange (KEM)","Authentication","Certificate signing","Encryption"],ans:0,ctx:"Kyber replaces ECDH for quantum-safe key exchange",fact:"CloudFlare and Google are already testing Kyber in TLS!"},
    {q:"The compress function in Kyber is used to?",opts:["Reduce ciphertext size","Increase security","Speed up NTT","Generate randomness"],ans:0,ctx:"Compress rounds coefficients to fewer bits",fact:"Compression trades tiny security margin for much smaller ciphertext!"},
    {q:"Kyber is an IND-CCA2 secure scheme, meaning?",opts:["Secure against adaptive chosen ciphertext attacks","Only secure against passive attacks","Secure against timing attacks","Post-quantum secure only"],ans:0,ctx:"IND-CCA2 is the strongest practical security definition for KEMs",fact:"IND-CCA2 is required for secure use in real protocols like TLS!"},
    {q:"Which transform converts between coefficient and NTT domain?",opts:["Inverse NTT","Matrix transpose","Modular reduction","Polynomial expansion"],ans:0,ctx:"NTT and inverse-NTT convert between domains",fact:"Kyber operates in NTT domain for efficiency, converting back only when needed!"},
    ],
    // Level 9 - Quantum Algorithms
    [
    {q:"Shor Algorithm solves which problem in polynomial time?",opts:["Integer factorization","SVP","SHA-3 preimage","LWE"],ans:0,ctx:"Shor factors n in O(n³) quantum time",fact:"RSA-2048 would fall to Shor in hours on a large enough quantum computer!"},
    {q:"Grover Algorithm provides what speedup over classical search?",opts:["Quadratic (sqrt N)","Exponential","Linear","Logarithmic"],ans:0,ctx:"Grover: O(N) classical → O(sqrt N) quantum",fact:"Quadratic speedup is not enough to break 256-bit keys!"},
    {q:"Quantum superposition allows a qubit to be?",opts:["0 and 1 simultaneously","Only 0","Only 1","Either 0 or 1 sequentially"],ans:0,ctx:"Superposition: |ψ⟩ = α|0⟩ + β|1⟩",fact:"Superposition is what gives quantum computers their parallel processing power!"},
    {q:"Shor Algorithm uses Quantum Fourier Transform to find?",opts:["Period of modular exponentiation","Shortest lattice vector","Hash preimage","Prime factors directly"],ans:0,ctx:"QFT finds period r of f(x) = a^x mod n",fact:"The period r is then used with GCD to factor n!"},
    {q:"How many logical qubits would break RSA-2048 with Shor?",opts:["~4000","~100","~1 million","~20"],ans:0,ctx:"Approximately 4000 error-corrected logical qubits needed",fact:"Current best quantum computers have ~1000 noisy qubits — not enough yet!"},
    {q:"What does quantum entanglement enable in algorithms?",opts:["Correlated measurements across qubits","Independent qubit operations","Classical speedup","Parallel memory access"],ans:0,ctx:"Entangled qubits have correlated states when measured",fact:"Entanglement is essential for quantum error correction in large quantum computers!"},
    {q:"Harvest now decrypt later attack means?",opts:["Collect encrypted data now, decrypt with quantum computer later","Decrypt data immediately with AI","Store quantum states for later use","Break encryption in real time"],ans:0,ctx:"Nation states may store encrypted data to decrypt when quantum computers arrive",fact:"This is why migrating to PQC NOW is urgent — even if quantum computers do not exist yet!"},
    {q:"Which NIST algorithm is immune to Shor Algorithm?",opts:["Kyber (ML-KEM)","RSA-4096","ECDH-521","Diffie-Hellman"],ans:0,ctx:"Kyber uses lattice LWE, not factoring or discrete log",fact:"Shor only attacks problems based on factoring and discrete logarithms!"},
    {q:"Quantum advantage means quantum computer is faster than?",opts:["All classical computers combined","A single laptop","A supercomputer","A GPU cluster"],ans:0,ctx:"Quantum advantage: quantum beats best possible classical algorithm",fact:"True quantum advantage for cryptographic attacks requires millions of stable qubits!"},
    {q:"Post-quantum cryptography protects against?",opts:["Both classical and quantum attacks","Only quantum attacks","Only classical attacks","Side channel attacks"],ans:0,ctx:"PQC algorithms are secure against both types",fact:"NIST standards must be secure against today's computers AND future quantum computers!"},
    ],
    // Level 10 - Advanced LWE
    [
    {q:"MLWE uses polynomial rings instead of integers because?",opts:["More efficient and equally secure","Less secure but faster","Harder to implement","Required by NIST"],ans:0,ctx:"Ring structure allows NTT and reduces key sizes",fact:"MLWE gives same security as LWE with 10-100x smaller keys!"},
    {q:"The learning with rounding (LWR) problem differs from LWE by?",opts:["Rounding replaces random noise","Using matrices instead of vectors","Adding more noise","Removing the secret"],ans:0,ctx:"LWR: b = round(As/p) mod q — deterministic noise",fact:"LWR is used in some NIST alternate candidates for its efficiency!"},
    {q:"In MLWE, polynomials are reduced modulo?",opts:["x^n + 1","x^n - 1","x^256","x + 1"],ans:0,ctx:"Ring: Rq = Zq[x]/(x^n+1)",fact:"x^n+1 is chosen because it makes NTT especially efficient!"},
    {q:"Worst case to average case reduction for LWE was proved by?",opts:["Regev (2005)","Shor (1994)","Diffie and Hellman","NIST"],ans:0,ctx:"Oded Regev proved LWE hardness reduces to worst-case lattice problems",fact:"This reduction is what gives Kyber its provable security guarantee!"},
    {q:"The LWE error distribution must be?",opts:["Small compared to q","Larger than q","Equal to q","Zero"],ans:0,ctx:"Error e much smaller than q allows decryption",fact:"Kyber uses centered binomial distribution — errors in range [-2, 2] with q=3329!"},
    {q:"MLWE security level increases when?",opts:["k (matrix dimension) increases","Noise decreases","q decreases","n decreases"],ans:0,ctx:"Larger k = more equations = harder to solve",fact:"Kyber-1024 uses k=4 for 256-bit security vs Kyber-512 k=2!"},
    {q:"The hardness of MLWE in ring Rq assumes?",opts:["x^n+1 is irreducible mod q","x^n-1 is prime","q is composite","n is even"],ans:0,ctx:"x^n+1 irreducibility ensures the ring has good properties",fact:"For Kyber, n=256 and x^256+1 factors mod q — but security still holds!"},
    {q:"Converting from LWE to ring variant (RLWE) gains?",opts:["Smaller keys and faster operations","Higher security","Simpler implementation","Better quantum resistance"],ans:0,ctx:"Ring structure allows NTT — polynomial time operations",fact:"RLWE keys are O(n) size vs LWE O(n²) — massive efficiency gain!"},
    {q:"LWE decryption fails when noise e is too large because?",opts:["Rounding step cannot recover message","Key generation fails","Matrix A is wrong","Ciphertext too large"],ans:0,ctx:"Decryption rounds off noise — too large noise → wrong bit recovered",fact:"Kyber parameters ensure decryption failure probability less than 2^-139!"},
    {q:"Module-SIS (Short Integer Solution) is the basis for?",opts:["Dilithium security","Kyber security","SPHINCS+ security","Falcon security"],ans:0,ctx:"Dilithium signatures rely on MLWE and Module-SIS hardness",fact:"SIS: find short vector in lattice kernel — different from LWE but equally hard!"},
    ],
    // Level 11 - NIST Standards
    [
    {q:"When did NIST publish the final PQC standards?",opts:["2024","2022","2026","2020"],ans:0,ctx:"NIST published FIPS 203/204/205/206 in August 2024",fact:"The 6-year NIST competition ran from 2016 to 2022 selection plus 2 years finalization!"},
    {q:"How many algorithms did NIST initially evaluate?",opts:["69","44","12","100"],ans:0,ctx:"69 algorithms submitted in 2017, reduced to 26, then 15, then 7 finalists",fact:"The open competition ensured global cryptographers could analyze and attack candidates!"},
    {q:"Which algorithm was NOT selected as a primary NIST standard?",opts:["NTRU","Kyber","Dilithium","SPHINCS+"],ans:0,ctx:"NTRU was alternate candidate, not primary standard",fact:"NTRU was a finalist but NIST preferred Kyber for key encapsulation!"},
    {q:"FIPS 203 is the standard number for?",opts:["ML-KEM (Kyber)","ML-DSA (Dilithium)","SLH-DSA (SPHINCS+)","FN-DSA (Falcon)"],ans:0,ctx:"FIPS 203 = Federal Information Processing Standard 203",fact:"FIPS numbers are assigned sequentially — 203-206 are the four PQC standards!"},
    {q:"NSM-10 requires federal agencies to migrate to PQC by?",opts:["2035","2030","2040","2028"],ans:0,ctx:"National Security Memorandum 10 sets 2035 deadline",fact:"Agencies must inventory all cryptographic systems and begin migration now!"},
    {q:"Which NIST standard is recommended for certificate authorities?",opts:["FIPS 205 (SPHINCS+)","FIPS 203 (Kyber)","FIPS 204 (Dilithium)","FIPS 206 (Falcon)"],ans:0,ctx:"SPHINCS+ large signatures are acceptable for long-lived CA certs",fact:"CA certificates are issued infrequently so large SPHINCS+ signatures are fine!"},
    {q:"Hybrid PQC schemes combine classical and post-quantum algorithms to?",opts:["Maintain security if either is broken","Double the speed","Reduce key sizes","Simplify implementation"],ans:0,ctx:"If lattice crypto fails, classical provides backup and vice versa",fact:"NIST recommends hybrid schemes during transition period!"},
    {q:"What is the crypto-agility principle?",opts:["Design systems to swap algorithms easily","Use multiple algorithms simultaneously","Avoid algorithm standardization","Test algorithms continuously"],ans:0,ctx:"Crypto-agile systems can update algorithms without full system redesign",fact:"Systems deployed today should be crypto-agile to adopt future PQC updates!"},
    {q:"FIPS 206 (Falcon) is based on which lattice structure?",opts:["NTRU lattices","Module-LWE","Hash chains","Ring-SIS"],ans:0,ctx:"FN-DSA = Fast-Fourier lattice-based compact signature from NTRU",fact:"NTRU lattices allow Gaussian sampling for extremely compact signatures!"},
    {q:"Which attack justifies migrating to PQC before quantum computers exist?",opts:["Harvest now decrypt later","Zero day exploit","SQL injection","Phishing"],ans:0,ctx:"Adversaries collect encrypted data now to decrypt with future quantum computers",fact:"Intelligence agencies may already be harvesting encrypted data for future decryption!"},
    ],
    // Level 12 - Grandmaster PQC
    [
    {q:"Which best describes the security reduction in Kyber?",opts:["MLWE hardness implies Kyber security","Kyber security implies MLWE hardness","SVP and Kyber are equivalent","Kyber relies on factoring"],ans:0,ctx:"Cryptographic reduction: breaking Kyber requires solving MLWE",fact:"Provable security via reduction is what separates NIST standards from ad-hoc crypto!"},
    {q:"The NTT in Kyber operates in which domain?",opts:["Polynomial ring Rq = Zq[x]/(x^256+1)","Integer ring Z_q","Binary field GF(2^256)","Complex number field"],ans:0,ctx:"Kyber uses ring of polynomials mod x^256+1 over integers mod q=3329",fact:"The ring structure is carefully chosen to make NTT maximally efficient!"},
    {q:"Dilithium rejection sampling threshold is based on?",opts:["Infinity norm of response z","Euclidean norm of secret s","SHA-3 hash output","Matrix A condition number"],ans:0,ctx:"If |z|∞ ≥ γ1 - β, reject and restart",fact:"The threshold is set so rejected signatures reveal zero information about s!"},
    {q:"In Falcon, Gaussian sampling over NTRU lattices requires?",opts:["Floating point with high precision","Integer arithmetic only","Binary operations","Matrix inversion"],ans:0,ctx:"Falcon requires 64-bit floating point Gaussian sampling",fact:"Precision requirements make Falcon harder to implement correctly than Dilithium!"},
    {q:"MLWE with k=3 (Kyber-768) claims 180-bit classical security. Why 180 not 192?",opts:["BKZ attacks reduce it below k*64 bits","Grover reduces security","Shor applies partially","Parameter choice error"],ans:0,ctx:"BKZ-β attacks provide asymptotic advantage over brute force",fact:"Actual security is estimated using BKZ simulation — always slightly below theoretical max!"},
    {q:"The Fiat-Shamir with Aborts transform ensures?",opts:["Zero-knowledge without leaking secret s","Faster signature generation","Smaller public keys","Compatibility with RSA"],ans:0,ctx:"FSwA: if response leaks info, abort and restart",fact:"Zero-knowledge property means an attacker learns nothing about s from valid signatures!"},
    {q:"Hash-based signature SPHINCS+ uses a hypertree structure to?",opts:["Authenticate many one-time keys","Speed up signing","Reduce signature size","Provide quantum speedup"],ans:0,ctx:"Hypertree: tree of XMSS trees, each signing WOTS+ keys",fact:"SPHINCS+ hypertree allows stateless signing unlike plain XMSS!"},
    {q:"Post-quantum TLS 1.3 handshake using Kyber performs how many KEM operations?",opts:["One encapsulation and one decapsulation","Two encapsulations","One encapsulation only","Four total operations"],ans:0,ctx:"Client encapsulates to server public key, server decapsulates",fact:"Single KEM operation gives both parties the same shared secret for symmetric encryption!"},
    {q:"Which statement about CRYSTALS (Kyber and Dilithium) is correct?",opts:["Both use Module-LWE security","Both use same signature size","Both require floating point","Both have same key size"],ans:0,ctx:"CRYSTALS = Cryptographic Suite for Algebraic Lattices",fact:"Kyber and Dilithium share mathematical structure — both from Module-LWE family!"},
    {q:"A quantum computer with 1 million logical qubits could break RSA-2048 in approximately?",opts:["Hours","Centuries","Milliseconds","Years"],ans:0,ctx:"With sufficient qubits, Shor runs in polynomial time",fact:"We do not have 1 million logical qubits yet — but the timeline is uncertain. Migrate now!"},
    ],
];
var QS = ALL_QS[Math.min(''' + str(idx) + ''', ALL_QS.length-1)];
var qi=0,sc=0,ok=0,wr=0,answered=false,tl=30,ti;
function loadQ(){
    answered=false;
    var q=QS[qi];
    document.getElementById("qt").textContent=q.q;
    document.getElementById("qc").textContent=q.ctx;
    document.getElementById("qn").textContent=(qi+1);
    document.getElementById("fb").style.display="none";
    document.getElementById("fc").style.display="none";
    document.getElementById("nb").style.display="none";
    var od=document.getElementById("opts");
    od.innerHTML="";
    for(var i=0;i<q.opts.length;i++){
        var b=document.createElement("button");
        b.className="opt";
        b.textContent=q.opts[i];
        b.setAttribute("data-i",i);
        b.onclick=function(){answer(parseInt(this.getAttribute("data-i")));};
        od.appendChild(b);
    }
    clearInterval(ti);
    tl=30;
    ti=setInterval(function(){
        tl--;
        document.getElementById("tm").textContent=tl;
        var pct=(tl/30)*100;
        var f=document.getElementById("tf");
        f.style.width=pct+"%";
        f.style.background=tl>15?"#10b981":tl>8?"#f59e0b":"#ef4444";
        if(tl<=0){clearInterval(ti);if(!answered)timeUp();}
    },1000);
}
function timeUp(){
    answered=true;wr++;
    var q=QS[qi];
    var btns=document.querySelectorAll(".opt");
    btns[q.ans].className="opt correct";
    var f=document.getElementById("fb");
    f.textContent="Time up! Answer: "+q.opts[q.ans];
    f.className="fb bad";f.style.display="block";
    document.getElementById("wr").textContent=wr;
    document.getElementById("nb").style.display="block";
}
function answer(i){
    if(answered)return;
    answered=true;
    clearInterval(ti);
    var q=QS[qi];
    var btns=document.querySelectorAll(".opt");
    btns[q.ans].className="opt correct";
    if(i!==q.ans)btns[i].className="opt wrong";
    var correct=i===q.ans;
    var bonus=Math.floor(tl/3);
    var pts=correct?100+bonus:0;
    sc+=pts;
    if(correct)ok++;else wr++;
    document.getElementById("sc").textContent=sc;
    document.getElementById("ok").textContent=ok;
    document.getElementById("wr").textContent=wr;
    var fb=document.getElementById("fb");
    fb.textContent=correct?"Correct! +"+pts+" pts (time bonus +"+bonus+")":"Wrong! Answer: "+q.opts[q.ans];
    fb.className="fb "+(correct?"ok":"bad");
    fb.style.display="block";
    var fc=document.getElementById("fc");
    fc.textContent="PQC: "+q.fact;
    fc.style.display="block";
    document.getElementById("nb").style.display="block";
}
function nextQ(){
    qi++;
    if(qi>=QS.length){
        clearInterval(ti);
        document.getElementById("qbox").style.display="none";
        document.getElementById("done").style.display="block";
        var pct=Math.round(ok/QS.length*100);
        document.getElementById("dm").textContent="Score: "+sc+" | Accuracy: "+pct+"% | "+ok+"/10 correct";
    } else {
        loadQ();
    }
}
function restart(){
    qi=0;sc=0;ok=0;wr=0;
    document.getElementById("sc").textContent=0;
    document.getElementById("ok").textContent=0;
    document.getElementById("wr").textContent=0;
    document.getElementById("qbox").style.display="block";
    document.getElementById("done").style.display="none";
    loadQ();
}
loadQ();
</script>
""", height=600)
                if st.button("Back to Intro", key="math_back"):
                    st.session_state.math_game_active = False
                    st.rerun()
