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
            {"name": "Level 1 - Modular Arithmetic", "xp_required": 0,   "color": "#10b981", "emoji": "🔢"},
            {"name": "Level 2 - Prime Numbers",       "xp_required": 50,  "color": "#3b82f6", "emoji": "🔑"},
            {"name": "Level 3 - Matrix Math",         "xp_required": 150, "color": "#8b5cf6", "emoji": "🏗"},
            {"name": "Level 4 - Number Theory",       "xp_required": 300, "color": "#f59e0b", "emoji": "📐"},
            {"name": "Level 5 - Lattice Problems",    "xp_required": 500, "color": "#ec4899", "emoji": "⚡"},
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
var QS=[
    {q:"What is 17 mod 5?",opts:["2","3","4","1"],ans:0,ctx:"17 = 3x5 + 2",fact:"RSA uses mod with huge primes. Kyber uses mod q=3329!"},
    {q:"What is 25 mod 7?",opts:["3","4","2","5"],ans:1,ctx:"25 = 3x7 + 4",fact:"In Kyber all math happens mod q. This keeps numbers small!"},
    {q:"What is (13+9) mod 11?",opts:["1","2","3","0"],ans:0,ctx:"13+9=22, 22=2x11+0",fact:"Hash functions use modular addition inside SHA-3!"},
    {q:"Which number is prime?",opts:["97","91","87","93"],ans:0,ctx:"97 has no factors except 1 and 97",fact:"RSA uses primes with 512+ digits. Shor Algorithm breaks this!"},
    {q:"Prime factors of 15?",opts:["3 and 5","3 and 4","5 and 7","2 and 7"],ans:0,ctx:"15 = 3 x 5",fact:"RSA multiplies two primes. Shor Algorithm factors the product!"},
    {q:"Dot product of [1,2] and [3,4]?",opts:["11","10","12","8"],ans:0,ctx:"1x3 + 2x4 = 11",fact:"Kyber uses matrix-vector dot products for its public key!"},
    {q:"In LWE: b = As + e, what is e?",opts:["Small noise vector","The secret","Public key","The message"],ans:0,ctx:"LWE = Learning With Errors",fact:"The noise e is what makes LWE impossible to solve!"},
    {q:"Euler totient of prime p equals?",opts:["p-1","p","p+1","p/2"],ans:0,ctx:"All numbers 1 to p-1 are coprime to prime p",fact:"RSA uses phi(n)=(p-1)(q-1). Only computable if you know p and q!"},
    {q:"What makes SVP hard in 1000 dimensions?",opts:["No efficient algorithm exists","Computers are too slow","The math is wrong","Quantum helps a lot"],ans:0,ctx:"SVP = Shortest Vector Problem",fact:"SVP hardness is exactly why Kyber is quantum-safe!"},
    {q:"Grover Algorithm gives what speedup on search?",opts:["Square root speedup","Exponential speedup","No speedup","Doubles the speed"],ans:0,ctx:"Grover searches N items in sqrt(N) steps",fact:"Grover gives sqrt speedup only. Not enough to break 256-bit lattice crypto!"},
];
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
