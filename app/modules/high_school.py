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

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📅 NIST Timeline",
        "⚖️ Algorithm Lab",
        "💻 Code It Yourself",
        "🛡️ Threat Modeler",
        "🔬 Research Journal",
        "🎮 Tower Defense",
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