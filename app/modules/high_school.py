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
        st.subheader("🧮 QuantumMath Challenge — Unlock All 5 Levels!")
        st.markdown(
            "Master the math behind post-quantum cryptography! "
            "Each level unlocks new concepts. Earn XP to unlock harder levels!"
        )

        xp = st.session_state.xp

        LEVELS = [
            {"name": "Level 1 — Modular Arithmetic", "xp_required": 0,   "color": "#10b981", "emoji": "🔢"},
            {"name": "Level 2 — Prime Numbers",       "xp_required": 50,  "color": "#3b82f6", "emoji": "🔑"},
            {"name": "Level 3 — Matrix Math",         "xp_required": 150, "color": "#8b5cf6", "emoji": "🏗️"},
            {"name": "Level 4 — Number Theory",       "xp_required": 300, "color": "#f59e0b", "emoji": "📐"},
            {"name": "Level 5 — Lattice Problems",    "xp_required": 500, "color": "#ec4899", "emoji": "⚡"},
        ]

        # Show level unlock status
        st.markdown("### 🔓 Your Progress")
        level_cols = st.columns(5)
        for i, (col, lvl) in enumerate(zip(level_cols, LEVELS)):
            with col:
                unlocked = xp >= lvl["xp_required"]
                st.markdown(
                    f"<div style='background:{lvl['color']}{'20' if unlocked else '08'};"
                    f"border:1px solid {lvl['color']}{'60' if unlocked else '20'};"
                    f"border-radius:8px;padding:8px;text-align:center;'>"
                    f"<div style='font-size:1.5rem'>{lvl['emoji']}</div>"
                    f"<div style='font-size:0.7rem;color:{'#ccc' if unlocked else '#555'};margin-top:4px'>"
                    f"{'✅ Unlocked' if unlocked else '🔒 '+str(lvl['xp_required'])+' XP'}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        st.markdown("---")

        # Level selector
        available = [l for l in LEVELS if xp >= l["xp_required"]]
        if not available:
            st.warning("Earn XP in other modules to unlock math challenges!")
        else:
            selected_level = st.selectbox(
                "Choose a level:",
                [l["name"] for l in available],
                key="math_level_select"
            )
            level_idx = next(i for i, l in enumerate(LEVELS) if l["name"] == selected_level)

            import streamlit.components.v1 as components_math
            components_math.html("""
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0f172a;font-family:sans-serif;color:white;padding:12px;}
.math-wrap{max-width:560px;margin:0 auto;}
.math-hud{display:flex;justify-content:space-between;margin-bottom:12px;gap:8px;}
.hud-box{background:#1e293b;border:1px solid #334155;border-radius:8px;
padding:8px 12px;font-size:12px;font-weight:bold;color:#a5b4fc;flex:1;text-align:center;}
.question-box{background:#1e293b;border:1px solid #334155;border-radius:12px;
padding:20px;margin:10px 0;text-align:center;}
.q-text{font-size:1.4rem;font-weight:bold;color:white;margin-bottom:8px;}
.q-context{font-size:0.85rem;color:#888;margin-bottom:16px;}
.options{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0;}
.opt-btn{padding:12px;border-radius:8px;border:2px solid #334155;
cursor:pointer;font-size:14px;font-weight:bold;background:#1e293b;
color:#a5b4fc;transition:all 0.15s;text-align:center;}
.opt-btn:hover{border-color:#4f46e5;background:rgba(79,70,229,0.1);}
.opt-btn.correct{border-color:#10b981;background:rgba(16,185,129,0.2);color:#10b981;}
.opt-btn.wrong{border-color:#ef4444;background:rgba(239,68,68,0.2);color:#ef4444;}
.feedback{padding:12px;border-radius:8px;margin:8px 0;font-size:13px;
text-align:center;display:none;}
.feedback.correct{background:rgba(16,185,129,0.15);border:1px solid #10b981;color:#10b981;}
.feedback.wrong{background:rgba(239,68,68,0.15);border:1px solid #ef4444;color:#ef4444;}
.pqc-fact{background:rgba(79,70,229,0.15);border:1px solid rgba(79,70,229,0.4);
border-radius:8px;padding:10px;margin:8px 0;font-size:12px;color:#a5b4fc;
text-align:center;display:none;}
.next-btn{width:100%;padding:12px;border-radius:8px;border:none;
cursor:pointer;font-size:14px;font-weight:bold;background:#4f46e5;
color:white;margin-top:8px;display:none;}
.next-btn:hover{background:#6d60ff;}
.timer-bar{height:6px;background:#334155;border-radius:3px;margin:8px 0;overflow:hidden;}
.timer-fill{height:100%;border-radius:3px;background:#10b981;transition:width 0.1s linear;}
.complete-box{background:rgba(16,185,129,0.1);border:1px solid #10b981;
border-radius:12px;padding:24px;text-align:center;display:none;}
</style>
</head>
<body>
<div class="math-wrap">
    <div class="math-hud">
        <div class="hud-box">⭐ Score<br><span id="score">0</span></div>
        <div class="hud-box">✅ Correct<br><span id="correct">0</span></div>
        <div class="hud-box">❌ Wrong<br><span id="wrong">0</span></div>
        <div class="hud-box">⏱️ Time<br><span id="timer">30</span>s</div>
        <div class="hud-box">📊 Q<br><span id="qnum">1</span>/10</div>
    </div>
    <div class="timer-bar"><div class="timer-fill" id="timer-fill" style="width:100%"></div></div>
    <div id="start-screen" style="background:#1e293b;border:1px solid #334155;
        border-radius:12px;padding:24px;margin:10px 0;">

        <!-- Level header -->
        <div style="text-align:center;margin-bottom:16px;">
            <div style="font-size:3rem;margin-bottom:8px" id="level-emoji">🧮</div>
            <h2 style="color:#a5b4fc;margin-bottom:4px" id="level-title">QuantumMath Challenge</h2>
            <p style="color:#888;font-size:12px;">10 questions · 30 seconds each · Time bonus points!</p>
        </div>

        <!-- Level intro explanation -->
        <div id="level-intro" style="background:rgba(79,70,229,0.1);border:1px solid rgba(79,70,229,0.3);
            border-radius:10px;padding:16px;margin-bottom:16px;">
        </div>

        <!-- Key concepts -->
        <div id="level-concepts" style="margin-bottom:16px;"></div>

        <!-- PQC connection -->
        <div id="level-pqc" style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);
            border-radius:10px;padding:12px;margin-bottom:20px;font-size:12px;color:#6ee7b7;">
        </div>

        <div style="text-align:center;">
            <button onclick="startChallenge()" style="padding:12px 32px;border-radius:8px;border:none;cursor:pointer;background:#4f46e5;color:white;font-size:15px;font-weight:bold;">▶ Start Challenge</button>
        </div>
    </div>
    <div class="question-box" id="qbox">
        <div class="q-text" id="q-text">Loading...</div>
        <div class="q-context" id="q-context"></div>
        <div class="options" id="options"></div>
        <div class="feedback" id="feedback"></div>
        <div class="pqc-fact" id="pqc-fact"></div>
        <button class="next-btn" id="next-btn" onclick="nextQuestion()">Next Question →</button>
    </div>
    <div class="complete-box" id="complete-box">
        <div style="font-size:3rem;margin-bottom:12px">🏆</div>
        <h2 style="color:#10b981;margin-bottom:8px">Level Complete!</h2>
        <p id="complete-msg" style="color:#888;margin-bottom:16px"></p>
        <button onclick="restartLevel()" style="padding:10px 24px;border-radius:8px;border:none;
            cursor:pointer;background:#4f46e5;color:white;font-size:14px;font-weight:bold;">
            Play Again
        </button>
    </div>
</div>
<script>
const LEVEL = 0; // Will be set dynamically

const LEVEL_INTROS = [
    {
        emoji: "🔢",
        title: "Level 1 — Modular Arithmetic",
        color: "#10b981",
        intro: `<h3 style="color:#a5b4fc;margin:0 0 10px;font-size:1rem;">What is Modular Arithmetic?</h3>
            <p style="color:#ccc;font-size:13px;line-height:1.7;margin-bottom:10px;">
                Modular arithmetic is like clock math. On a 12-hour clock, if it is 10 o'clock and you add 5 hours,
                you get 3 o'clock — not 15! That is because 15 mod 12 = 3.
            </p>
            <p style="color:#ccc;font-size:13px;line-height:1.7;margin-bottom:10px;">
                <strong style="color:#a5b4fc;">The formula:</strong> a mod b = the remainder when a is divided by b<br>
                <strong style="color:#10b981;">Example:</strong> 17 mod 5 = 2 (because 17 = 3×5 + 2)
            </p>
            <p style="color:#ccc;font-size:13px;line-height:1.7;">
                <strong style="color:#a5b4fc;">Key idea:</strong> Numbers wrap around! After reaching b, they start over at 0.
                Think of it like a number line that forms a circle.
            </p>`,
        concepts: [
            {icon:"🔄", text:"Numbers wrap around at a fixed value (the modulus)"},
            {icon:"➗", text:"a mod b = remainder of a ÷ b"},
            {icon:"⏰", text:"Clock arithmetic: 10 + 5 = 3 (mod 12)"},
            {icon:"🔑", text:"Modular inverse: find x where a×x ≡ 1 (mod n)"},
        ],
        pqc: "🔐 PQC Connection: ALL cryptography uses modular arithmetic! RSA encrypts using m^e mod n. Kyber does lattice math mod q=3329. Even SHA-3 hashing uses modular operations internally!",
    },
    {
        emoji: "🔑",
        title: "Level 2 — Prime Numbers",
        color: "#3b82f6",
        intro: `<h3 style="color:#a5b4fc;margin:0 0 10px;font-size:1rem;">What are Prime Numbers?</h3>
            <p style="color:#ccc;font-size:13px;line-height:1.7;margin-bottom:10px;">
                A prime number has exactly two factors: 1 and itself. Examples: 2, 3, 5, 7, 11, 13, 17...
                The number 4 is NOT prime because 4 = 2×2 (it has factors 1, 2, and 4).
            </p>
            <p style="color:#ccc;font-size:13px;line-height:1.7;margin-bottom:10px;">
                <strong style="color:#a5b4fc;">Prime factorization:</strong> Every number can be broken into prime factors.<br>
                <strong style="color:#3b82f6;">Example:</strong> 60 = 2 × 2 × 3 × 5
            </p>
            <p style="color:#ccc;font-size:13px;line-height:1.7;">
                <strong style="color:#a5b4fc;">The big idea:</strong> Multiplying two primes is easy. Finding which primes
                were multiplied together (factoring) is incredibly hard for large numbers!
            </p>`,
        concepts: [
            {icon:"🎯", text:"Prime: exactly 2 factors (1 and itself)"},
            {icon:"🔨", text:"Composite: more than 2 factors (can be broken down)"},
            {icon:"📊", text:"Every number has a unique prime factorization"},
            {icon:"💥", text:"Factoring large numbers is computationally hard"},
        ],
        pqc: "🔐 PQC Connection: RSA security depends on prime factoring being hard! RSA uses n=p×q where p and q are secret 512-digit primes. A quantum computer running Shor's Algorithm factors n and breaks RSA in hours. Kyber avoids primes entirely — it uses lattice math instead!",
    },
    {
        emoji: "🏗️",
        title: "Level 3 — Matrix Math",
        color: "#8b5cf6",
        intro: `<h3 style="color:#a5b4fc;margin:0 0 10px;font-size:1rem;">What are Matrices?</h3>
            <p style="color:#ccc;font-size:13px;line-height:1.7;margin-bottom:10px;">
                A matrix is a rectangular grid of numbers arranged in rows and columns.
                A vector is a single row or column of numbers. Matrix math lets us work with
                many equations at once — incredibly powerful!
            </p>
            <p style="color:#ccc;font-size:13px;line-height:1.7;margin-bottom:10px;">
                <strong style="color:#a5b4fc;">Dot product:</strong> [1,2] · [3,4] = 1×3 + 2×4 = 11<br>
                <strong style="color:#8b5cf6;">Matrix multiply:</strong> Each output cell = dot product of a row and column
            </p>
            <p style="color:#ccc;font-size:13px;line-height:1.7;">
                <strong style="color:#a5b4fc;">Key idea:</strong> In LWE (Learning With Errors), the equation is
                b = A·s + e where A is a matrix, s is the secret vector, and e is small noise.
            </p>`,
        concepts: [
            {icon:"📐", text:"Matrix: grid of numbers with rows and columns"},
            {icon:"➕", text:"Dot product: multiply matching elements and sum"},
            {icon:"🔄", text:"Transpose: flip rows and columns"},
            {icon:"🏗️", text:"Lattice = set of all integer combinations of basis vectors"},
        ],
        pqc: "🔐 PQC Connection: Kyber's public key is literally a matrix! The key generation computes b = A·s + e mod q where A is a public matrix, s is the secret, and e is small noise. The Learning With Errors (LWE) problem asks: given A and b, find s. In 1000+ dimensions this is impossible even for quantum computers!",
    },
    {
        emoji: "📐",
        title: "Level 4 — Number Theory",
        color: "#f59e0b",
        intro: `<h3 style="color:#a5b4fc;margin:0 0 10px;font-size:1rem;">What is Number Theory?</h3>
            <p style="color:#ccc;font-size:13px;line-height:1.7;margin-bottom:10px;">
                Number theory is the study of integers and their properties. It asks deep questions:
                How many primes are there? What patterns do remainders follow? How do numbers
                behave in groups and rings?
            </p>
            <p style="color:#ccc;font-size:13px;line-height:1.7;margin-bottom:10px;">
                <strong style="color:#a5b4fc;">Euler's totient φ(n):</strong> Count of numbers less than n that share no factors with n.<br>
                <strong style="color:#f59e0b;">Example:</strong> φ(8) = 4 (the numbers 1, 3, 5, 7 are coprime to 8)
            </p>
            <p style="color:#ccc;font-size:13px;line-height:1.7;">
                <strong style="color:#a5b4fc;">Abstract algebra:</strong> Groups, rings, and fields give us the
                mathematical structures that ALL modern cryptography is built on.
            </p>`,
        concepts: [
            {icon:"φ", text:"Euler's totient: count of coprime integers less than n"},
            {icon:"🔁", text:"Groups: sets with an operation following specific rules"},
            {icon:"💍", text:"Rings: sets with + and × (like polynomial rings in Kyber!)"},
            {icon:"🎯", text:"Hardness assumptions: problems believed impossible to solve fast"},
        ],
        pqc: "🔐 PQC Connection: Kyber works inside a polynomial ring Zq[x]/(x^n+1). This ring structure makes computations fast while keeping the lattice problem hard. RSA uses Euler's totient φ(n)=(p-1)(q-1) for key generation — computable only if you know p and q!",
    },
    {
        emoji: "⚡",
        title: "Level 5 — Lattice Problems",
        color: "#ec4899",
        intro: `<h3 style="color:#a5b4fc;margin:0 0 10px;font-size:1rem;">What are Lattice Problems?</h3>
            <p style="color:#ccc;font-size:13px;line-height:1.7;margin-bottom:10px;">
                A lattice is an infinite grid of points in multi-dimensional space. Lattice problems
                ask: given this grid, can you find the shortest vector? Or the closest point to a
                target? In 2D this is easy. In 1000 dimensions it is computationally impossible!
            </p>
            <p style="color:#ccc;font-size:13px;line-height:1.7;margin-bottom:10px;">
                <strong style="color:#a5b4fc;">SVP (Shortest Vector Problem):</strong> Find the shortest nonzero vector in a lattice.<br>
                <strong style="color:#ec4899;">LWE:</strong> Given noisy equations A·s + e = b, find secret s.
                The noise e makes this impossible to reverse!
            </p>
            <p style="color:#ccc;font-size:13px;line-height:1.7;">
                <strong style="color:#a5b4fc;">Why quantum-safe?</strong> No quantum algorithm gives significant speedup
                on SVP or LWE. Grover gives at most a square root speedup — not enough to break it!
            </p>`,
        concepts: [
            {icon:"🏗️", text:"SVP: find shortest nonzero vector — NP-hard in general"},
            {icon:"🎯", text:"CVP: find closest lattice point to a target"},
            {icon:"🧮", text:"LWE: solve A·s + e = b with small noise e"},
            {icon:"🔐", text:"MLWE: Module LWE — used in Kyber for efficiency"},
        ],
        pqc: "🔐 PQC Connection: This IS the math behind Kyber (ML-KEM), Dilithium (ML-DSA), and Falcon! NIST chose lattice-based crypto because SVP and LWE have no known quantum speedup. Shor's Algorithm does not help here. Grover's Algorithm gives only square root speedup — not enough to break 256-bit lattice security!",
    },
];

const intro = LEVEL_INTROS[Math.min(LEVEL, LEVEL_INTROS.length-1)];
document.getElementById("level-emoji").textContent = intro.emoji;
document.getElementById("level-title").textContent = intro.title;
document.getElementById("level-title").style.color = intro.color;
document.getElementById("level-intro").innerHTML = intro.intro;
document.getElementById("level-pqc").textContent = intro.pqc;

// Render key concepts
const conceptsEl = document.getElementById("level-concepts");
conceptsEl.innerHTML = intro.concepts.map(c =>
    `<div style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.06);">
        <span style="font-size:1rem;min-width:24px;text-align:center;">${c.icon}</span>
        <span style="font-size:12px;color:#ccc;line-height:1.5;">${c.text}</span>
    </div>`
).join("");

const ALL_QUESTIONS = [
    // Level 0 — Modular Arithmetic
    [
        {q:"What is 17 mod 5?", opts:["2","3","4","1"], ans:0,
          ctx:"Modular arithmetic is the foundation of all cryptography!",
          fact:"RSA uses mod arithmetic with huge primes. Kyber uses mod q in lattice equations!"},
        {q:"What is 25 mod 7?", opts:["3","4","2","5"], ans:1,
          ctx:"a mod b = remainder when a is divided by b",
          fact:"In Kyber, all calculations happen mod q (usually 3329). This keeps numbers small!"},
        {q:"If 3 × x ≡ 1 (mod 7), what is x?", opts:["5","3","4","2"], ans:0,
          ctx:"Finding the modular inverse — crucial for RSA decryption!",
          fact:"RSA decryption uses modular inverses. Kyber avoids this with lattice math instead!"},
        {q:"What is (13 + 9) mod 11?", opts:["1","2","3","0"], ans:0,
          ctx:"Modular addition wraps around like a clock",
          fact:"Hash functions use modular addition internally. SHA-3 uses mod 2^64 operations!"},
        {q:"What is 2^10 mod 1000?", opts:["24","124","24","1024"], ans:0,
          ctx:"Modular exponentiation powers RSA encryption",
          fact:"RSA encryption computes m^e mod n. Quantum computers can crack this with Shor's Algorithm!"},
        {q:"What is 100 mod 13?", opts:["9","10","8","11"], ans:0,
          ctx:"100 = 7 × 13 + 9",
          fact:"Modular arithmetic creates groups — the mathematical structure behind all public key crypto!"},
        {q:"Which is true: 15 ≡ ? (mod 4)", opts:["3","1","2","0"], ans:0,
          ctx:"15 = 3×4 + 3, so 15 mod 4 = 3",
          fact:"Congruence notation (≡) is used throughout the Kyber specification FIPS 203!"},
        {q:"What is the additive inverse of 3 mod 7?", opts:["4","3","5","2"], ans:0,
          ctx:"Additive inverse: what number adds to 3 to get 0 mod 7?",
          fact:"Lattice crypto uses additive inverses constantly in its polynomial ring operations!"},
        {q:"If p = 11, what is (p-1)/2?", opts:["5","6","4","10"], ans:0,
          ctx:"This is a key value in number theory for prime p",
          fact:"The value (p-1)/2 appears in quadratic residue checks used in lattice-based crypto!"},
        {q:"What is 7^2 mod 11?", opts:["5","6","4","3"], ans:0,
          ctx:"49 mod 11 = ?",
          fact:"Squaring mod p is used in zero-knowledge proofs and commitment schemes in PQC!"},
    ],
    // Level 1 — Prime Numbers
    [
        {q:"Which is a prime number?", opts:["97","91","87","93"], ans:0,
          ctx:"A prime has exactly 2 factors: 1 and itself",
          fact:"RSA security depends on factoring large primes. A quantum computer breaks this in hours!"},
        {q:"What are the prime factors of 15?", opts:["3 and 5","3 and 4","5 and 7","2 and 7"], ans:0,
          ctx:"Prime factorization is the basis of RSA",
          fact:"RSA multiplies two primes p×q. Shor's Algorithm factors this product on a quantum computer!"},
        {q:"How many primes are less than 10?", opts:["4","3","5","2"], ans:0,
          ctx:"List them: 2, 3, 5, 7...",
          fact:"There are infinitely many primes — the Prime Number Theorem tells us their distribution!"},
        {q:"Which theorem says every number has unique prime factorization?", opts:["Fundamental Theorem of Arithmetic","Fermat's Last Theorem","Euler's Theorem","Pythagorean Theorem"], ans:0,
          ctx:"This is the foundation of RSA's security assumption",
          fact:"Post-quantum crypto avoids prime factoring entirely! Kyber uses lattice problems instead!"},
        {q:"If p and q are prime, is p×q always prime?", opts:["No","Yes","Sometimes","Always"], ans:0,
          ctx:"A product of two primes has 4 factors: 1, p, q, and p×q",
          fact:"RSA public key n = p×q where p,q are secret primes. Finding p and q from n is the hard problem!"},
        {q:"Fermat's Little Theorem: a^(p-1) ≡ ? (mod p) for prime p", opts:["1","0","p","a"], ans:0,
          ctx:"This works when gcd(a,p)=1",
          fact:"Fermat's Little Theorem is used in RSA key generation and primality testing!"},
        {q:"What is the smallest prime greater than 100?", opts:["101","103","107","109"], ans:0,
          ctx:"Check: is 101 divisible by 2,3,5,7?",
          fact:"RSA uses primes with 1024+ digits. Finding such primes requires probabilistic tests!"},
        {q:"Which of these is NOT prime?", opts:["51","53","59","61"], ans:0,
          ctx:"51 = 3 × 17",
          fact:"Testing if large numbers are prime uses the Miller-Rabin test — a key algorithm in crypto!"},
        {q:"What does 'relatively prime' mean?", opts:["gcd(a,b)=1","Both are prime","a<b","a divides b"], ans:0,
          ctx:"Also called 'coprime'",
          fact:"The RSA public exponent e must be relatively prime to φ(n). This ensures decryption works!"},
        {q:"In RSA, if n=35, what are p and q?", opts:["5 and 7","3 and 11","7 and 9","5 and 9"], ans:0,
          ctx:"Factor 35 into two primes",
          fact:"Real RSA uses primes with 512+ digits each. Kyber replaces this with lattice math!"},
    ],
    // Level 2 — Matrix Math
    [
        {q:"What is [1,2] · [3,4] (dot product)?", opts:["11","10","12","8"], ans:0,
          ctx:"1×3 + 2×4 = ?",
          fact:"Kyber uses matrix-vector products over polynomial rings! The public key is a matrix A times secret s!"},
        {q:"For matrix A = [[1,2],[3,4]], what is A[0][1]?", opts:["2","1","3","4"], ans:0,
          ctx:"Row 0, Column 1 of the matrix",
          fact:"Kyber's public key matrix A is generated from a random seed using SHA-3 — impossible to reverse!"},
        {q:"What is the transpose of [[1,2],[3,4]]?", opts:["[[1,3],[2,4]]","[[4,3],[2,1]]","[[2,1],[4,3]]","[[1,2],[3,4]]"], ans:0,
          ctx:"Swap rows and columns",
          fact:"Dilithium uses matrix transposes in its signature verification algorithm!"},
        {q:"Matrix multiplication: [[1,0],[0,1]] × [[5,6],[7,8]] = ?", opts:["[[5,6],[7,8]]","[[1,0],[0,1]]","[[6,5],[8,7]]","[[12,14],[16,18]]"], ans:0,
          ctx:"The identity matrix times any matrix = that matrix",
          fact:"Identity matrices appear in lattice proofs. The hard lattice problem is NOT like the identity!"},
        {q:"If A is 2×3 and B is 3×4, what size is A×B?", opts:["2×4","3×3","2×3","3×4"], ans:0,
          ctx:"(m×n) × (n×p) = m×p",
          fact:"Kyber uses matrix dimensions that balance security and efficiency. Kyber-768 uses 3×3 matrices!"},
        {q:"What does det([[2,1],[1,2]]) equal?", opts:["3","4","2","1"], ans:0,
          ctx:"det = ad - bc for 2×2 matrix",
          fact:"Determinants determine if a matrix is invertible — crucial in lattice math security proofs!"},
        {q:"In LWE, we compute A·s + e. What is e?", opts:["Small noise vector","The secret","The public key","The message"], ans:0,
          ctx:"LWE = Learning With Errors",
          fact:"The noise e is what makes LWE hard! Without noise, solving A·s = b is easy linear algebra!"},
        {q:"What is a vector in n dimensions?", opts:["A list of n numbers","An n×n grid","A single number","A direction only"], ans:0,
          ctx:"Lattices are built from vectors",
          fact:"Kyber-768 secret key s is a vector of 256 polynomial coefficients! Huge but quantum-safe!"},
        {q:"What does 'linearly independent' mean for vectors?", opts:["No vector is a combination of others","All vectors are parallel","All vectors have length 1","Vectors are perpendicular"], ans:0,
          ctx:"Key concept for lattice bases",
          fact:"Lattice basis vectors must be linearly independent. The security comes from finding short vectors!"},
        {q:"What is the Gram-Schmidt process used for?", opts:["Orthogonalizing vectors","Multiplying matrices","Finding eigenvalues","Solving equations"], ans:0,
          ctx:"Used in lattice reduction algorithms",
          fact:"The LLL algorithm uses Gram-Schmidt to find short lattice vectors — but fails in high dimensions!"},
    ],
    // Level 3 — Number Theory
    [
        {q:"What is Euler's totient φ(12)?", opts:["4","6","8","3"], ans:0,
          ctx:"Count integers 1-12 that are coprime to 12",
          fact:"RSA uses φ(n) = (p-1)(q-1). Computing this requires knowing p and q — which is secret!"},
        {q:"Chinese Remainder Theorem: solve x≡1(mod 3), x≡2(mod 5)", opts:["7","11","4","2"], ans:0,
          ctx:"Find the smallest positive x satisfying both",
          fact:"Kyber uses Number Theoretic Transform (NTT) based on CRT for fast polynomial multiplication!"},
        {q:"What is gcd(48, 18)?", opts:["6","3","9","12"], ans:0,
          ctx:"Use Euclidean algorithm: 48=2×18+12, 18=1×12+6, 12=2×6+0",
          fact:"Extended Euclidean Algorithm computes modular inverses used in RSA key generation!"},
        {q:"For RSA with p=5, q=11, what is n?", opts:["55","56","50","60"], ans:0,
          ctx:"n = p × q",
          fact:"Real RSA n is 2048+ bits. A 2048-bit quantum computer running Shor breaks it in hours!"},
        {q:"What is the discrete logarithm problem?", opts:["Find x given g^x mod p = y","Multiply two primes","Factor a large number","Find square roots"], ans:0,
          ctx:"Basis of Diffie-Hellman and ECDH",
          fact:"Discrete log is also broken by Shor's Algorithm! Kyber solves a completely different problem!"},
        {q:"Lagrange's theorem: order of subgroup divides order of group. If group order=12, which can be subgroup order?", opts:["4","5","7","8"], ans:0,
          ctx:"4 divides 12 evenly",
          fact:"Group theory underlies all of abstract algebra including the ring structure in lattice crypto!"},
        {q:"What is a ring in abstract algebra?", opts:["Set with + and × following specific rules","A circular number","Only integers","A prime number set"], ans:0,
          ctx:"Polynomial rings are key in post-quantum crypto",
          fact:"Kyber works in the polynomial ring Zq[x]/(x^n+1). This ring structure enables fast computation!"},
        {q:"If φ(p) = p-1 for prime p, what is φ(7)?", opts:["6","5","7","4"], ans:0,
          ctx:"All numbers 1 to p-1 are coprime to prime p",
          fact:"Euler's totient function is central to RSA but NOT used in post-quantum algorithms like Kyber!"},
        {q:"What is a quadratic residue mod p?", opts:["A perfect square mod p","A prime mod p","An even number","A negative number"], ans:0,
          ctx:"x is QR mod p if x ≡ a² mod p for some a",
          fact:"Quadratic residuosity is used in some PQC schemes and zero-knowledge proof systems!"},
        {q:"What does 'hardness assumption' mean in crypto?", opts:["A problem believed computationally infeasible","A difficult exam","Physical hardness","Memory requirements"], ans:0,
          ctx:"Security relies on unproven but widely believed assumptions",
          fact:"Kyber's hardness assumption is MLWE — Module Learning With Errors. No quantum speedup known!"},
    ],
    // Level 4 — Lattice Problems
    [
        {q:"What is the Shortest Vector Problem (SVP)?", opts:["Find shortest nonzero vector in lattice","Sort a list","Find primes","Matrix multiplication"], ans:0,
          ctx:"NP-hard in general — basis of lattice security",
          fact:"SVP hardness is what makes lattice crypto quantum-safe! No quantum algorithm solves SVP efficiently!"},
        {q:"In LWE: given (A, b=As+e), what is the secret?", opts:["s","A","b","e"], ans:0,
          ctx:"A is public, b is public, e is small noise",
          fact:"Finding s from (A, As+e) is computationally infeasible — this is what Kyber relies on!"},
        {q:"What makes MLWE harder than plain LWE?", opts:["Uses polynomial rings instead of integers","Uses bigger numbers","Has more noise","Has fewer equations"], ans:0,
          ctx:"M stands for Module",
          fact:"Kyber uses MLWE (Module LWE) for better efficiency. Same hardness, smaller key sizes!"},
        {q:"What is a lattice basis?", opts:["Set of linearly independent vectors spanning the lattice","The bottom row of a matrix","A fundamental constant","The lattice boundary"], ans:0,
          ctx:"Many different bases can generate the same lattice",
          fact:"The hard problem: given a bad basis, find a good one (short vectors). This is what crypto uses!"},
        {q:"Kyber-512 has security level equivalent to AES-?", opts:["128","256","192","64"], ans:0,
          ctx:"NIST security level 1",
          fact:"Kyber-512: 128-bit security. Kyber-768: 192-bit. Kyber-1024: 256-bit. Choose based on need!"},
        {q:"What is the noise distribution in Kyber?", opts:["Centered binomial distribution","Uniform random","Gaussian","Binary"], ans:0,
          ctx:"Small errors sampled from a specific distribution",
          fact:"Kyber uses centered binomial distribution η for noise — efficient to sample and provably secure!"},
        {q:"How does Kyber key encapsulation work (simplified)?", opts:["Encrypt random seed with recipient public key","Sign a message","Hash a password","Generate prime numbers"], ans:0,
          ctx:"Kyber = ML-KEM = key encapsulation mechanism",
          fact:"Kyber: Alice encrypts random seed r using Bob's public key → shared secret = Hash(r). Quantum safe!"},
        {q:"What is the rejection sampling technique used for in Dilithium?", opts:["Make signatures independent of secret key","Speed up computation","Reduce key size","Generate primes"], ans:0,
          ctx:"Critical security feature in Dilithium signing",
          fact:"Without rejection sampling, Dilithium signatures would leak the secret key over multiple uses!"},
        {q:"What is NTRU? (used by Falcon)", opts:["Nth degree TRUncated polynomial ring","A network protocol","A hash function","A prime number type"], ans:0,
          ctx:"Falcon uses NTRU lattices for compact signatures",
          fact:"Falcon uses NTRU lattices — produces signatures 5x smaller than Dilithium for same security!"},
        {q:"If Grover's algorithm gives quadratic speedup, a 256-bit hash has effective security of?", opts:["128 bits","256 bits","64 bits","512 bits"], ans:0,
          ctx:"Square root speedup: 2^256 operations becomes 2^128",
          fact:"SHA-256 gives 128-bit post-quantum security. SHA-3-256 is NIST recommended for PQC systems!"},
    ],
];

const questions = ALL_QUESTIONS[Math.min(LEVEL, ALL_QUESTIONS.length-1)];
let qIdx=0, score=0, correct=0, wrong=0, answered=false;
let timeLeft=30, timerInterval;

function startTimer() {
    clearInterval(timerInterval);
    timeLeft=30;
    timerInterval=setInterval(()=>{
        timeLeft--;
        document.getElementById("timer").textContent=timeLeft;
        const pct=(timeLeft/30)*100;
        const fill=document.getElementById("timer-fill");
        fill.style.width=pct+"%";
        fill.style.background=timeLeft>15?"#10b981":timeLeft>8?"#f59e0b":"#ef4444";
        if(timeLeft<=0){
            clearInterval(timerInterval);
            if(!answered) timeUp();
        }
    },1000);
}

function timeUp() {
    answered=true;
    const q=questions[qIdx];
    document.querySelectorAll(".opt-btn").forEach((b,i)=>{
        if(i===q.ans) b.className="opt-btn correct";
    });
    showFeedback(false,"⏰ Time's up! The answer was: "+q.opts[q.ans]);
    wrong++;
    document.getElementById("wrong").textContent=wrong;
    document.getElementById("next-btn").style.display="block";
}

function loadQuestion() {
    answered=false;
    const q=questions[qIdx];
    document.getElementById("q-text").textContent=q.q;
    document.getElementById("q-context").textContent=q.ctx;
    document.getElementById("qnum").textContent=(qIdx+1);
    document.getElementById("feedback").style.display="none";
    document.getElementById("pqc-fact").style.display="none";
    document.getElementById("next-btn").style.display="none";

    const opts=document.getElementById("options");
    opts.innerHTML="";
    q.opts.forEach((opt,i)=>{
        const btn=document.createElement("button");
        btn.className="opt-btn";
        btn.textContent=opt;
        btn.onclick=()=>answer(i);
        opts.appendChild(btn);
    });

    startTimer();
}

function answer(i) {
    if(answered) return;
    answered=true;
    clearInterval(timerInterval);
    const q=questions[qIdx];
    const btns=document.querySelectorAll(".opt-btn");
    btns[q.ans].className="opt-btn correct";
    if(i!==q.ans) btns[i].className="opt-btn wrong";

    const isCorrect=i===q.ans;
    const timeBonus=Math.floor(timeLeft/3);
    const pts=isCorrect?100+timeBonus:0;
    score+=pts;
    if(isCorrect){correct++;}else{wrong++;}

    document.getElementById("score").textContent=score;
    document.getElementById("correct").textContent=correct;
    document.getElementById("wrong").textContent=wrong;

    showFeedback(isCorrect,
        isCorrect?"✅ Correct! +"+(pts)+" points (+"+(timeBonus)+" time bonus!)":
        "❌ Wrong! Correct answer: "+q.opts[q.ans]);

    // Show PQC fact
    const fact=document.getElementById("pqc-fact");
    fact.textContent="🔐 PQC Connection: "+q.fact;
    fact.style.display="block";

    document.getElementById("next-btn").style.display="block";
}

function showFeedback(isCorrect,msg) {
    const fb=document.getElementById("feedback");
    fb.textContent=msg;
    fb.className="feedback "+(isCorrect?"correct":"wrong");
    fb.style.display="block";
}

function nextQuestion() {
    qIdx++;
    if(qIdx>=questions.length){
        // Level complete!
        clearInterval(timerInterval);
        document.getElementById("qbox").style.display="none";
        const cb=document.getElementById("complete-box");
        cb.style.display="block";
        const pct=Math.round(correct/questions.length*100);
        document.getElementById("complete-msg").textContent=
            "Score: "+score+" | Accuracy: "+pct+"% | "+correct+"/"+questions.length+" correct";
    } else {
        loadQuestion();
    }
}

function restartLevel() {
    qIdx=0;score=0;correct=0;wrong=0;
    document.getElementById("score").textContent=0;
    document.getElementById("correct").textContent=0;
    document.getElementById("wrong").textContent=0;
    document.getElementById("qbox").style.display="none";
    document.getElementById("complete-box").style.display="none";
    document.getElementById("start-screen").style.display="block";
}

// Show start screen first
document.getElementById("qbox").style.display="none";
document.getElementById("start-screen").style.display="block";

function startChallenge() {
    document.getElementById("start-screen").style.display="none";
    document.getElementById("qbox").style.display="block";
    loadQuestion();
}
document.getElementById("start-btn").onclick = startChallenge;
</script>
</body>
</html>
""", height=620)
