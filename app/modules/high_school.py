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

from modules.quantum_composer import render_quantum_composer
def render_high_school():
    st.title("🔴 Cipher Corps - High School Edition")
    st.markdown(
        "Welcome to the advanced division. You'll work with real algorithms, "
        "real standards, and real Python code. Let's build the future of security. 🛡️"
    )

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📅 NIST Timeline",
        "⚖️ Algorithm Lab",
        "💻 Code It Yourself",
        "🛡️ Threat Modeler",
        "🔬 Research Journal",
        "🎮 Tower Defense",
        "🧮 Math Challenge",
        "⚛️ Quantum Composer",
    ])

    # ── Tab 1: NIST PQC Timeline ──────────────────────────────────────────────
    with tab1:
        import streamlit.components.v1 as _hs1
        st.subheader("📅 The Road to Post-Quantum Standards")
        st.markdown(
            "🏛️ **NIST ran the biggest cryptography competition in history.** "
            "69 algorithms from teams worldwide competed for 6 years. "
            "Only 4 survived. Here is the complete story."
        )

        # Interactive timeline
        timeline_events = [
            {"year": "2016", "emoji": "🚀", "color": "#3b82f6",
             "title": "Competition Launches",
             "detail": "NIST announces Post-Quantum Cryptography competition. 82 teams worldwide submit algorithms. The goal: find math that quantum computers cannot break.",
             "stat": "82 submissions"},
            {"year": "2017", "emoji": "🔍", "color": "#8b5cf6",
             "title": "Round 1 - First Cut",
             "detail": "69 algorithms pass initial screening. Teams of cryptographers worldwide begin analyzing every submission for weaknesses. Many algorithms are broken almost immediately.",
             "stat": "69 candidates"},
            {"year": "2019", "emoji": "⚙️", "color": "#f59e0b",
             "title": "Round 2 - Deep Analysis",
             "detail": "26 algorithms advance. Years of intense mathematical analysis. Several promising algorithms are cryptanalyzed and eliminated. Lattice-based schemes prove strongest.",
             "stat": "26 candidates"},
            {"year": "2020", "emoji": "🎯", "color": "#ec4899",
             "title": "Round 3 - Final Seven",
             "detail": "7 finalists selected: Kyber, Dilithium, FALCON, SPHINCS+, Classic McEliece, BIKE, HQC. Plus 8 alternates for backup. Intense final scrutiny begins.",
             "stat": "7 finalists"},
            {"year": "2022", "emoji": "🏆", "color": "#10b981",
             "title": "Winners Announced",
             "detail": "NIST selects Kyber (key exchange), Dilithium, FALCON, SPHINCS+ (signatures) for standardization. Classic McEliece, BIKE, HQC continue as alternates.",
             "stat": "4 selected"},
            {"year": "2024", "emoji": "✅", "color": "#10b981",
             "title": "Standards Published",
             "detail": "FIPS 203 (ML-KEM/Kyber), FIPS 204 (ML-DSA/Dilithium), FIPS 205 (SLH-DSA/SPHINCS+), FIPS 206 (FN-DSA/Falcon) officially published. History made.",
             "stat": "FIPS 203-206"},
            {"year": "2025+", "emoji": "🌐", "color": "#4f46e5",
             "title": "Global Migration",
             "detail": "NSM-10 requires federal agencies to migrate by 2035. Google, Cloudflare, Apple all begin TLS integration. The biggest cryptographic migration in internet history.",
             "stat": "Migration begins"},
        ]

        if "hs_timeline_idx" not in st.session_state:
            st.session_state.hs_timeline_idx = 0

        # Show timeline as clickable cards
        cols = st.columns(len(timeline_events))
        for i, (col, evt) in enumerate(zip(cols, timeline_events)):
            with col:
                active = i == st.session_state.hs_timeline_idx
                st.markdown(
                    f"<div style='background:{'%s20' % evt['color'] if active else '#1e293b'};"
                    f"border:{'2px solid ' + evt['color'] if active else '1px solid #334155'};"
                    f"border-radius:10px;padding:8px 4px;text-align:center;cursor:pointer;"
                    f"margin:2px;'>"
                    f"<div style='font-size:1.3rem'>{evt['emoji']}</div>"
                    f"<div style='font-size:0.68rem;font-weight:bold;color:{'%s' % evt['color']}'>{evt['year']}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                if st.button("", key=f"tl_{i}", help=evt["title"]):
                    st.session_state.hs_timeline_idx = i
                    st.rerun()

        evt = timeline_events[st.session_state.hs_timeline_idx]
        st.markdown(
            f"<div style='background:{evt['color']}15;border:2px solid {evt['color']}50;"
            f"border-radius:14px;padding:20px;margin:10px 0'>"
            f"<div style='display:flex;justify-content:space-between;align-items:flex-start'>"
            f"<div>"
            f"<div style='font-size:2rem;margin-bottom:6px'>{evt['emoji']}</div>"
            f"<h3 style='color:{evt['color']};margin:0 0 4px'>{evt['year']} - {evt['title']}</h3>"
            f"<p style='color:#ccc;font-size:0.9rem;line-height:1.6;margin:0'>{evt['detail']}</p>"
            f"</div>"
            f"<div style='text-align:center;min-width:80px'>"
            f"<div style='font-size:1.4rem;font-weight:bold;color:{evt['color']}'>{evt['stat']}</div>"
            f"</div>"
            f"</div></div>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Previous", key="tl_prev", use_container_width=True):
                st.session_state.hs_timeline_idx = max(0, st.session_state.hs_timeline_idx - 1)
                st.rerun()
        with col2:
            if st.button("Next ➡️", key="tl_next", use_container_width=True, type="primary"):
                if st.session_state.hs_timeline_idx < len(timeline_events)-1:
                    st.session_state.hs_timeline_idx += 1
                    st.rerun()

        st.markdown("---")
        st.markdown("### 🏆 The Four NIST PQC Standards")

        winners = [
            {"name": "ML-KEM", "fips": "FIPS 203", "old": "Kyber", "type": "Key Encapsulation",
             "basis": "Module-LWE", "color": "#10b981", "emoji": "🔐",
             "use": "TLS handshakes, encrypted messaging, VPNs"},
            {"name": "ML-DSA", "fips": "FIPS 204", "old": "Dilithium", "type": "Digital Signature",
             "basis": "Module-LWE + SIS", "color": "#3b82f6", "emoji": "✍️",
             "use": "Code signing, document authentication, PKI"},
            {"name": "SLH-DSA", "fips": "FIPS 205", "old": "SPHINCS+", "type": "Hash Signature",
             "basis": "SHA-3 hash functions", "color": "#8b5cf6", "emoji": "🌲",
             "use": "CA certificates, long-term signatures, backup"},
            {"name": "FN-DSA", "fips": "FIPS 206", "old": "Falcon", "type": "Compact Signature",
             "basis": "NTRU lattices", "color": "#f59e0b", "emoji": "🦅",
             "use": "IoT devices, embedded systems, TLS certificates"},
        ]

        w_cols = st.columns(4)
        for col, w in zip(w_cols, winners):
            with col:
                st.markdown(
                    f"<div style='background:{w['color']}12;border:2px solid {w['color']}50;"
                    f"border-radius:12px;padding:12px;text-align:center;height:220px'>"
                    f"<div style='font-size:2rem;margin-bottom:4px'>{w['emoji']}</div>"
                    f"<div style='font-weight:bold;color:{w['color']};font-size:0.9rem'>{w['name']}</div>"
                    f"<div style='font-size:0.72rem;color:#888;margin:2px 0'>{w['fips']}</div>"
                    f"<div style='font-size:0.72rem;color:#a5b4fc;margin:4px 0'>{w['type']}</div>"
                    f"<div style='font-size:0.68rem;color:#888;margin-top:6px;line-height:1.4'>{w['use']}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        st.markdown("---")
        st.markdown("### 🧠 NIST Timeline Quiz")
        quiz_qs = [
            ("Which NIST standard is used for KEY EXCHANGE (KEM)?",
             ["ML-DSA (FIPS 204)", "SLH-DSA (FIPS 205)", "ML-KEM (FIPS 203)", "FN-DSA (FIPS 206)"], 2),
            ("How many years did the NIST PQC competition run?",
             ["2 years", "4 years", "6 years", "10 years"], 2),
            ("Which algorithm has the SMALLEST signatures (good for IoT)?",
             ["ML-KEM", "SLH-DSA", "ML-DSA", "FN-DSA (Falcon)"], 3),
            ("What math problem does ML-KEM (Kyber) rely on?",
             ["Prime factorization", "Discrete logarithm", "Module-LWE lattice", "Elliptic curves"], 2),
        ]

        if "nist_q" not in st.session_state:
            st.session_state.nist_q = 0
        if "nist_score" not in st.session_state:
            st.session_state.nist_score = 0

        if st.session_state.nist_q < len(quiz_qs):
            q, opts, ans = quiz_qs[st.session_state.nist_q]
            st.markdown(f"**Q{st.session_state.nist_q+1}/{len(quiz_qs)}:** {q}")
            for i, opt in enumerate(opts):
                if st.button(opt, key=f"nq_{st.session_state.nist_q}_{i}", use_container_width=True):
                    if i == ans:
                        st.success("✅ Correct! +10 XP")
                        st.session_state.xp = st.session_state.get("xp", 0) + 10
                        st.session_state.nist_score += 1
                    else:
                        st.error(f"❌ The answer was: {opts[ans]}")
                    st.session_state.nist_q += 1
                    if st.session_state.nist_q >= len(quiz_qs):
                        mark_complete("nist_timeline")
                        award_badge("📅 NIST Scholar", xp=25)
                    st.rerun()
        else:
            score = st.session_state.nist_score
            color = "#10b981" if score >= 3 else "#f59e0b"
            st.markdown(
                f"<div style='background:{color}15;border:2px solid {color};border-radius:12px;"
                f"padding:14px;text-align:center'>"
                f"<h3 style='color:{color};margin:0'>Score: {score}/{len(quiz_qs)} 🏆</h3>"
                f"<p style='color:#888;font-size:0.85rem'>{'NIST Expert! Badge unlocked!' if score>=3 else 'Review the timeline and try again!'}</p>"
                f"</div>",
                unsafe_allow_html=True
            )
            if st.button("🔄 Retry Quiz", key="nist_retry"):
                st.session_state.nist_q = 0
                st.session_state.nist_score = 0
                st.rerun()

    with tab2:
        import plotly.graph_objects as go
        import plotly.express as px
        st.subheader("⚖️ Algorithm Comparison Lab")
        st.markdown(
            "🔬 **You are the cryptographer.** Compare all algorithms across security, "
            "key size, speed, and quantum resistance. Then run the live quantum attack race!"
        )

        algo_data = {
            "Algorithm":               ["RSA-2048", "RSA-4096", "ECC-256", "ML-KEM-512", "ML-KEM-768", "ML-KEM-1024", "ML-DSA-2", "Falcon-512", "SPHINCS+"],
            "Type":                    ["Classical","Classical","Classical","Post-Quantum","Post-Quantum","Post-Quantum","Post-Quantum","Post-Quantum","Post-Quantum"],
            "Security (bits)":         [112,        128,        128,        128,          192,           256,           128,          128,           128],
            "Public Key (bytes)":      [256,        512,        64,         800,          1184,          1568,          1312,         897,           32],
            "Ciphertext/Sig (bytes)":  [256,        512,        96,         768,          1088,          1568,          2420,         666,           8080],
            "Quantum Safe":            [False,      False,      False,      True,         True,          True,          True,         True,          True],
            "Color":                   ["#ef4444","#ef4444","#f97316","#10b981","#3b82f6","#8b5cf6","#06b6d4","#f59e0b","#ec4899"],
        }

        view_tab1, view_tab2, view_tab3 = st.tabs(["📊 Full Comparison", "📏 Key Sizes", "⚡ Quantum Attack Race"])

        with view_tab1:
            # Color coded table
            st.markdown("**Algorithm Comparison - Red = Quantum Vulnerable, Green = Quantum Safe**")
            for i, algo in enumerate(algo_data["Algorithm"]):
                color = algo_data["Color"][i]
                qsafe = algo_data["Quantum Safe"][i]
                sec = algo_data["Security (bits)"][i]
                pk = algo_data["Public Key (bytes)"][i]
                sig = algo_data["Ciphertext/Sig (bytes)"][i]
                atype = algo_data["Type"][i]
                st.markdown(
                    f"<div style='background:{color}12;border-left:4px solid {color};"
                    f"border-radius:0 10px 10px 0;padding:10px 14px;margin:4px 0;"
                    f"display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr 1fr 0.8fr;gap:8px;align-items:center'>"
                    f"<div style='font-weight:bold;color:{color}'>{algo}</div>"
                    f"<div style='font-size:0.78rem;color:#888'>{atype}</div>"
                    f"<div style='font-size:0.82rem;color:#ccc'>{sec}-bit</div>"
                    f"<div style='font-size:0.82rem;color:#ccc'>{pk}B pubkey</div>"
                    f"<div style='font-size:0.82rem;color:#ccc'>{sig}B sig</div>"
                    f"<div style='font-size:0.82rem;color:{'#10b981' if qsafe else '#ef4444'};font-weight:bold'>"
                    f"{'✅ Safe' if qsafe else '❌ Broken'}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        with view_tab2:
            fig = go.Figure()
            for i, algo in enumerate(algo_data["Algorithm"]):
                fig.add_trace(go.Bar(
                    name=algo, x=[algo],
                    y=[algo_data["Public Key (bytes)"][i]],
                    marker_color=algo_data["Color"][i],
                    text=[f"{algo_data['Public Key (bytes)'][i]}B"],
                    textposition='outside',
                ))
            fig.update_layout(
                showlegend=False, height=320,
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=10),
                xaxis=dict(gridcolor='#334155', tickangle=-30),
                yaxis=dict(gridcolor='#334155', title="Public Key Size (bytes)"),
                margin=dict(t=20, b=60, l=40, r=20),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.info("💡 Kyber-512 (800B) is only 3x larger than ECC-256 (64B) but QUANTUM SAFE! RSA-2048 (256B) is smaller but completely broken by Shor's Algorithm.")

        with view_tab3:
            st.markdown("### ⚡ Quantum Computer Attack Simulation")
            st.markdown(
                "Watch a cryptographically-relevant quantum computer (CRQC) attack "
                "RSA-2048 vs ML-KEM-768 in real time!"
            )
            if st.button("🚀 Start Attack Simulation!", key="start_race", type="primary"):
                import time as _time
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(
                        "<div style='background:#ef444420;border:2px solid #ef4444;"
                        "border-radius:10px;padding:10px;text-align:center;margin-bottom:8px'>"
                        "<b style='color:#ef4444'>🔑 RSA-2048 (Classical)</b>"
                        "</div>", unsafe_allow_html=True
                    )
                    rsa_bar = st.progress(0)
                    rsa_status = st.empty()
                with col2:
                    st.markdown(
                        "<div style='background:#10b98120;border:2px solid #10b981;"
                        "border-radius:10px;padding:10px;text-align:center;margin-bottom:8px'>"
                        "<b style='color:#10b981'>🔐 ML-KEM-768 (Post-Quantum)</b>"
                        "</div>", unsafe_allow_html=True
                    )
                    kyber_bar = st.progress(0)
                    kyber_status = st.empty()

                for step in range(101):
                    rsa_prog = min(100, step * 4)
                    kyber_prog = min(12, step * 0.12)
                    rsa_bar.progress(int(rsa_prog))
                    kyber_bar.progress(int(kyber_prog))
                    if rsa_prog < 100:
                        rsa_status.markdown(f"💥 Shor's Algorithm cracking... **{int(rsa_prog)}%**")
                    else:
                        rsa_status.markdown("💀 **RSA BROKEN** - private key exposed!")
                    kyber_status.markdown(f"🛡️ Quantum computer lost in lattice... **{int(kyber_prog):.0f}%** (stuck!)")
                    _time.sleep(0.04)

                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.error("❌ **RSA-2048 Result:** Broken in ~hours by Shor's Algorithm. All data encrypted with RSA is now readable.")
                with col2:
                    st.success("✅ **ML-KEM-768 Result:** Quantum computer made <15% progress. Module-LWE problem remains unsolved.")
                st.balloons()
                mark_complete("algorithm_lab")
                award_badge("⚖️ Algorithm Analyst", xp=30)
                st.session_state.xp = st.session_state.get("xp", 0) + 30

            st.markdown("---")
            st.markdown("### 🎯 Algorithm Selection Challenge")
            st.markdown("You are securing a hospital's patient records for 30 years. Which combo do you choose?")

            col1, col2 = st.columns(2)
            with col1:
                choice_key = st.selectbox("Key Exchange:", ["RSA-2048", "ECDH-256", "ML-KEM-1024"], key="algo_choice_key")
            with col2:
                choice_sig = st.selectbox("Digital Signatures:", ["RSA-PSS", "ECDSA-256", "ML-DSA-87"], key="algo_choice_sig")

            if st.button("📋 Evaluate My Choice", key="algo_eval"):
                key_safe = "ML-KEM" in choice_key
                sig_safe = "ML-DSA" in choice_sig
                if key_safe and sig_safe:
                    st.success("🏥 EXCELLENT! Hospital records will be safe for 30+ years against quantum computers. Both algorithms are NIST approved PQC standards!")
                    award_badge("⚖️ Security Architect", xp=20)
                elif key_safe or sig_safe:
                    st.warning("⚠️ Partially secure! One algorithm is vulnerable. In 2035 when quantum computers arrive, some data could be decrypted. Use ML-KEM + ML-DSA for full protection.")
                else:
                    st.error("🚨 VULNERABLE! By 2035 a quantum computer could decrypt all 30 years of patient records. Harvest-now-decrypt-later attacks start TODAY!")

    with tab3:
        st.subheader("💻 Code It Yourself - Real LWE in Python")
        st.markdown(
            "🧑‍💻 **This is actual cryptographic code.** The Learning With Errors problem "
            "implemented in Python - the same math inside CRYSTALS-Kyber. "
            "Run it, modify it, break it, understand it!"
        )

        lwe_code = (
            "\"\"\"\"\"\"\n"
            "Simplified LWE Demo\n"
            "===================\n"
            "import random\n"
            "MOD = 97  # Kyber uses 3329\n"
            "N   = 4   # Kyber uses 256\n"
            "\n"
            "def gen_secret(n, mod):\n"
            "    return [random.randint(0, mod-1) for _ in range(n)]\n"  # nosec B311
            "\n"
            "def gen_public_key(s, mod):\n"
            "    n = len(s)\n"
            "    A = [[random.randint(0, mod-1) for _ in range(n)] for _ in range(n)]\n"  # nosec B311
            "    e = [random.randint(-2, 2) for _ in range(n)]\n"  # nosec B311
            "    b = [(sum(A[i][j]*s[j] for j in range(n))+e[i])%mod for i in range(n)]\n"
            "    return A, b\n"
            "\n"
            "def encrypt(A, b, bit, mod):\n"
            "    n = len(b)\n"
            "    r  = [random.randint(0, 1) for _ in range(n)]\n"  # nosec B311
            "    e1 = [random.randint(-1, 1) for _ in range(n)]\n"  # nosec B311
            "    e2 = random.randint(-1, 1)\n"  # nosec B311
            "    u = [(sum(A[j][i]*r[j] for j in range(n))+e1[i])%mod for i in range(n)]\n"
            "    v = (sum(b[i]*r[i] for i in range(n))+e2+(mod//2)*bit)%mod\n"
            "    return u, v\n"
            "\n"
            "def decrypt(s, u, v, mod):\n"
            "    noisy = (v - sum(s[i]*u[i] for i in range(len(s))))%mod\n"
            "    return 1 if abs(noisy-mod//2) < mod//4 else 0\n"
            "\n"
            "secret = gen_secret(N, MOD)\n"
            "A, b   = gen_public_key(secret, MOD)\n"
            "for bit in [0, 1]:\n"
            "    u, v = encrypt(A, b, bit, MOD)\n"
            "    rec  = decrypt(secret, u, v, MOD)\n"
            "    print(f\"Sent: {bit} | Got: {rec} | OK\")"
            "\n\"\"\"\n"
        )

        st.code(lwe_code, language="python")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "<div style='background:#0c2e1e;border:2px solid #10b981;border-radius:10px;padding:12px'>"
                "<h4 style='color:#34d399;margin:0 0 8px'>🔑 What each step does</h4>"
                "<ul style='color:#ccc;font-size:0.82rem;line-height:1.8;margin:0;padding-left:16px'>"
                "<li><b style='color:#10b981'>gen_secret</b>: picks private key s</li>"
                "<li><b style='color:#10b981'>gen_public_key</b>: computes t=As+e</li>"
                "<li><b style='color:#10b981'>encrypt</b>: wraps bit using public key</li>"
                "<li><b style='color:#10b981'>decrypt</b>: uses s to cancel noise</li>"
                "</ul></div>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                "<div style='background:#1a0f2e;border:2px solid #8b5cf6;border-radius:10px;padding:12px'>"
                "<h4 style='color:#a5b4fc;margin:0 0 8px'>⚛️ Real Kyber differences</h4>"
                "<ul style='color:#ccc;font-size:0.82rem;line-height:1.8;margin:0;padding-left:16px'>"
                "<li>n=256 (not 4)</li>"
                "<li>q=3329 (not 97)</li>"
                "<li>Polynomial rings (not integers)</li>"
                "<li>NTT for fast multiplication</li>"
                "<li>Key = 800 bytes (Kyber-512)</li>"
                "</ul></div>",
                unsafe_allow_html=True
            )

        st.markdown("---")
        if st.button("▶️ Run Demo Live!", key="run_lwe", type="primary"):
            MOD_L, N_L = 97, 4
            import random as _r

            def _gen_s(n, mod): return [_r.randint(0, mod-1) for _ in range(n)]  # nosec B311
            def _gen_pk(s, mod):
                n = len(s)
                A = [[_r.randint(0, mod-1) for _ in range(n)] for _ in range(n)]  # nosec B311
                e = [_r.randint(-2, 2) for _ in range(n)]  # nosec B311
                b = [(sum(A[i][j]*s[j] for j in range(n))+e[i])%mod for i in range(n)]
                return A, b, e
            def _enc(A, b, m, mod):
                n = len(b)
                r  = [_r.randint(0,1) for _ in range(n)]  # nosec B311
                e1 = [_r.randint(-1,1) for _ in range(n)]  # nosec B311
                e2 = _r.randint(-1,1)  # nosec B311
                u = [(sum(A[j][i]*r[j] for j in range(n))+e1[i])%mod for i in range(n)]
                v = (sum(b[i]*r[i] for i in range(n))+e2+(mod//2)*m)%mod
                return u, v
            def _dec(s, u, v, mod):
                noisy = (v - sum(s[i]*u[i] for i in range(len(s))))%mod
                return 1 if abs(noisy-mod//2) < mod//4 else 0

            sk = _gen_s(N_L, MOD_L)
            A_m, b_m, e_m = _gen_pk(sk, MOD_L)

            st.markdown("**🔐 Key Generation:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    f"<div style='background:#10b98120;border:1px solid #10b981;border-radius:8px;"
                    f"padding:10px;text-align:center'>"
                    f"<div style='font-size:0.72rem;color:#888'>🔒 Secret Key</div>"
                    f"<code style='color:#10b981;font-size:0.78rem'>{sk}</code>"
                    f"</div>", unsafe_allow_html=True
                )
            with col2:
                st.markdown(
                    f"<div style='background:#3b82f620;border:1px solid #3b82f6;border-radius:8px;"
                    f"padding:10px;text-align:center'>"
                    f"<div style='font-size:0.72rem;color:#888'>🌐 Public Key b</div>"
                    f"<code style='color:#3b82f6;font-size:0.78rem'>{b_m}</code>"
                    f"</div>", unsafe_allow_html=True
                )
            with col3:
                st.markdown(
                    f"<div style='background:#f59e0b20;border:1px solid #f59e0b;border-radius:8px;"
                    f"padding:10px;text-align:center'>"
                    f"<div style='font-size:0.72rem;color:#888'>🌊 Noise e</div>"
                    f"<code style='color:#f59e0b;font-size:0.78rem'>{e_m}</code>"
                    f"</div>", unsafe_allow_html=True
                )

            st.markdown("**📡 Encrypt & Decrypt:**")
            all_ok = True
            for bit in [0, 1]:
                u_r, v_r = _enc(A_m, b_m, bit, MOD_L)
                rec = _dec(sk, u_r, v_r, MOD_L)
                ok = rec == bit
                if not ok: all_ok = False
                color = "#10b981" if ok else "#ef4444"
                st.markdown(
                    f"<div style='background:{color}12;border:1px solid {color}40;"
                    f"border-radius:8px;padding:10px;margin:4px 0'>"
                    f"{'✅' if ok else '❌'} Sent: <b style='color:#a5b4fc'>{bit}</b> → "
                    f"Encrypted → Decrypted: <b style='color:{color}'>{rec}</b> "
                    f"{'(noise cancelled out!)' if ok else '(decryption failed!)'}"
                    f"</div>", unsafe_allow_html=True
                )

            if all_ok:
                st.success("🎉 LWE encryption/decryption works! The noise cancels perfectly because s is known. Without s, even a quantum computer can't recover the message!")
                award_badge("💻 LWE Coder", xp=35)
                mark_complete("lwe_code_lab")
                st.session_state.xp = st.session_state.get("xp", 0) + 35

        st.markdown("---")
        st.markdown("### 🧪 Experiment: What Happens With More Noise?")
        st.markdown("Increase the noise level and watch decryption start failing!")
        noise_level = st.slider("Noise level:", 1, 20, 2, key="noise_exp")
        if st.button("🔬 Run Experiment", key="noise_run"):
            import random as _r2
            MOD_E, N_E = 97, 4
            sk2 = [_r2.randint(0, MOD_E-1) for _ in range(N_E)]  # nosec B311
            A2 = [[_r2.randint(0, MOD_E-1) for _ in range(N_E)] for _ in range(N_E)]  # nosec B311
            e2 = [_r2.randint(-noise_level, noise_level) for _ in range(N_E)]  # nosec B311
            b2 = [(sum(A2[i][j]*sk2[j] for j in range(N_E))+e2[i])%MOD_E for i in range(N_E)]

            successes = 0
            for _ in range(10):
                bit = _r2.randint(0,1)  # nosec B311
                r2 = [_r2.randint(0,1) for _ in range(N_E)]  # nosec B311
                e1_2 = [_r2.randint(-noise_level, noise_level) for _ in range(N_E)]  # nosec B311
                e2_2 = _r2.randint(-noise_level, noise_level)  # nosec B311
                u2 = [(sum(A2[j][i]*r2[j] for j in range(N_E))+e1_2[i])%MOD_E for i in range(N_E)]
                v2 = (sum(b2[i]*r2[i] for i in range(N_E))+e2_2+(MOD_E//2)*bit)%MOD_E
                noisy2 = (v2 - sum(sk2[i]*u2[i] for i in range(N_E)))%MOD_E
                rec2 = 1 if abs(noisy2-MOD_E//2) < MOD_E//4 else 0
                if rec2 == bit: successes += 1

            pct = successes * 10
            color = "#10b981" if pct >= 90 else "#f59e0b" if pct >= 60 else "#ef4444"
            st.markdown(
                f"<div style='background:{color}15;border:2px solid {color};border-radius:10px;"
                f"padding:12px;text-align:center'>"
                f"<b style='color:{color}'>Decryption success rate with noise={noise_level}: {pct}%</b><br>"
                f"<span style='color:#888;font-size:0.82rem'>"
                f"{'✅ Noise level OK - decryption works!' if pct>=90 else '⚠️ High noise causing errors!' if pct>=60 else '❌ Too much noise - decryption failing!'}"
                f"</span></div>",
                unsafe_allow_html=True
            )
            st.caption(f"Real Kyber uses noise in range [-2,2] with q=3329 to keep error probability below 2^-139!")

    with tab4:
        st.subheader("🛡️ Threat Modeling Simulator - Design a Secure System")
        st.markdown(
            "🏗️ **You are the security architect.** Choose algorithms to protect a real-world system, "
            "then face a simulated attacker. Can your design survive?"
        )

        SYSTEMS = {
            "🏥 Hospital Patient Records": {"years": 30, "sensitivity": "Critical"},
            "🏦 Banking Transaction System": {"years": 15, "sensitivity": "Critical"},
            "🏫 School Grade Database": {"years": 10, "sensitivity": "Medium"},
            "🌐 Public Website (HTTPS)": {"years": 2, "sensitivity": "Low"},
            "🔐 Government Classified Comms": {"years": 50, "sensitivity": "Top Secret"},
        }

        col1, col2 = st.columns([1,1])
        with col1:
            system = st.selectbox("System to protect:", list(SYSTEMS.keys()), key="tm_system")
            sys_info = SYSTEMS[system]
            st.markdown(
                f"<div style='background:#1e293b;border-radius:10px;padding:12px;margin-top:8px'>"
                f"<div style='font-size:0.8rem;color:#888'>Protection needed:</div>"
                f"<div style='color:#a5b4fc;font-weight:bold'>{sys_info['years']} years</div>"
                f"<div style='font-size:0.8rem;color:#888;margin-top:4px'>Sensitivity:</div>"
                f"<div style='color:{'#ef4444' if sys_info['sensitivity']=='Top Secret' else '#f59e0b' if sys_info['sensitivity']=='Critical' else '#10b981'};font-weight:bold'>{sys_info['sensitivity']}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

        with col2:
            attacker = st.selectbox("Threat model:", [
                "😈 Script kiddie (today)",
                "🕵️ Nation-state classical HPC (today)",
                "⚛️ Cryptographically Relevant Quantum Computer (CRQC)",
                "🔮 CRQC + harvest-now-decrypt-later (worst case)",
            ], key="tm_attacker")

        st.markdown("---")
        st.markdown("### 🔧 Choose Your Algorithms")
        col1, col2, col3 = st.columns(3)
        with col1:
            key_algo = st.selectbox("Key Exchange:", [
                "RSA-2048", "ECDH-256", "ML-KEM-512", "ML-KEM-768", "ML-KEM-1024"
            ], key="tm_key")
        with col2:
            sig_algo = st.selectbox("Digital Signatures:", [
                "RSA-PSS", "ECDSA-256", "ML-DSA-44", "ML-DSA-65", "ML-DSA-87", "FN-DSA-512"
            ], key="tm_sig")
        with col3:
            hash_algo = st.selectbox("Hash Function:", [
                "SHA-256", "SHA3-256", "SHA3-384", "SHA3-512", "SHAKE-256"
            ], key="tm_hash")

        if st.button("🎯 Run Threat Assessment!", key="threat_run", type="primary"):
            if not check_rate_limit("threat_run", st.session_state):
                st.warning("Rate limit reached. Try again shortly.")
            else:
                crqc = "CRQC" in attacker or "quantum" in attacker.lower()
                harvest = "harvest" in attacker.lower()
                years = sys_info["years"]

                key_safe  = "ML-KEM" in key_algo
                sig_safe  = "ML-DSA" in sig_algo or "FN-DSA" in sig_algo
                hash_safe = "SHA3" in hash_algo or "SHAKE" in hash_algo

                # More nuanced scoring
                issues = []
                score = 100

                if not key_safe:
                    if crqc:
                        issues.append(("❌ CRITICAL", f"{key_algo} is broken by Shor's Algorithm. All key exchanges exposed.", "#ef4444"))
                        score -= 40
                    elif harvest and years > 10:
                        issues.append(("⚠️ HIGH RISK", f"{key_algo} data collected today will be decrypted when quantum computers arrive.", "#f59e0b"))
                        score -= 25
                    else:
                        issues.append(("⚠️ FUTURE RISK", f"{key_algo} will become vulnerable as quantum computers advance.", "#f59e0b"))
                        score -= 10
                else:
                    issues.append(("✅ SECURE", f"{key_algo} is quantum-safe. Module-LWE problem resists all known attacks.", "#10b981"))

                if not sig_safe:
                    if crqc:
                        issues.append(("❌ CRITICAL", f"{sig_algo} signatures are forgeable by quantum Shor's Algorithm.", "#ef4444"))
                        score -= 35
                    else:
                        issues.append(("⚠️ FUTURE RISK", f"{sig_algo} will become vulnerable to quantum signature forgery.", "#f59e0b"))
                        score -= 10
                else:
                    issues.append(("✅ SECURE", f"{sig_algo} is NIST approved quantum-safe signature scheme.", "#10b981"))

                if not hash_safe:
                    if crqc:
                        issues.append(("⚠️ REDUCED", f"SHA-256 provides only 64-bit quantum security via Grover. Use SHA3-256 minimum.", "#f59e0b"))
                        score -= 15
                    else:
                        issues.append(("ℹ️ OK", f"{hash_algo} is currently safe but consider upgrading to SHA3-256.", "#3b82f6"))
                else:
                    issues.append(("✅ SECURE", f"{hash_algo} is quantum-resistant. Grover provides only quadratic speedup.", "#10b981"))

                score = max(0, score)
                color = "#10b981" if score >= 80 else "#f59e0b" if score >= 50 else "#ef4444"
                grade = "A" if score>=90 else "B" if score>=80 else "C" if score>=60 else "D" if score>=40 else "F"

                st.markdown(
                    f"<div style='background:{color}15;border:3px solid {color};border-radius:14px;"
                    f"padding:20px;margin:10px 0'>"
                    f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                    f"<h3 style='color:{color};margin:0'>Security Assessment: Grade {grade}</h3>"
                    f"<div style='font-size:2.5rem;font-weight:bold;color:{color}'>{score}/100</div>"
                    f"</div></div>",
                    unsafe_allow_html=True
                )

                for status, detail, c in issues:
                    st.markdown(
                        f"<div style='background:{c}10;border-left:4px solid {c};"
                        f"border-radius:0 8px 8px 0;padding:10px 14px;margin:5px 0'>"
                        f"<b style='color:{c}'>{status}</b> - {detail}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                if score >= 80:
                    st.balloons()
                    st.success(f"🏆 Excellent security design for {system}!")
                    award_badge("🛡️ Threat Modeler", xp=40)
                    mark_complete("threat_modeler")
                elif score < 50:
                    st.error(f"🚨 {system} would be compromised! Switch to ML-KEM + ML-DSA + SHA3 for full quantum protection.")
                else:
                    st.warning("⚠️ Partially secure - consider upgrading to full PQC stack before quantum computers arrive.")

    with tab5:
        st.subheader("🔬 Research Journal - Your PQC Notebook")
        st.markdown(
            "📝 **Document your journey into post-quantum cryptography.** "
            "Write research entries, record what you learned, and export your journal. "
            "AI feedback available on your entries!"
        )

        import datetime as _dt

        PROMPTS = [
            "Explain in your own words why RSA is vulnerable to quantum computers but Kyber is not.",
            "Describe the Learning With Errors problem and why adding noise makes it secure.",
            "Compare Dilithium and Falcon - when would you use each one?",
            "What would happen to the internet if a cryptographically relevant quantum computer existed today?",
            "Explain the NIST PQC competition - why was it necessary and what did it achieve?",
            "Describe the harvest-now-decrypt-later threat and why it makes PQC migration urgent.",
            "What is the avalanche effect in SHA-3 and why does it matter for security?",
            "Design a post-quantum secure system for protecting medical records for 30 years.",
        ]

        if "hs_journal" not in st.session_state:
            st.session_state.hs_journal = []
        if "hs_prompt_idx" not in st.session_state:
            import random as _rp
            st.session_state.hs_prompt_idx = _rp.randint(0, len(PROMPTS)-1)  # nosec B311

        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown(
                f"<div style='background:#4f46e515;border:1px solid #4f46e550;"
                f"border-radius:10px;padding:12px;margin-bottom:8px'>"
                f"<div style='font-size:0.75rem;color:#888;margin-bottom:4px'>💡 TODAY'S PROMPT</div>"
                f"<div style='color:#a5b4fc;font-size:0.9rem'>{PROMPTS[st.session_state.hs_prompt_idx]}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🎲 New Prompt", key="new_prompt_hs"):
                import random as _rp2
                st.session_state.hs_prompt_idx = _rp2.randint(0, len(PROMPTS)-1)  # nosec B311
                st.rerun()

        topic = st.text_input("Entry title:", placeholder="e.g. Why Kyber resists Shor's Algorithm", max_chars=80, key="hs_journal_topic")
        entry = st.text_area(
            "Your research entry:",
            placeholder="Write your analysis, insights, or reflections here...",
            max_chars=3000, height=180, key="hs_journal_entry"
        )

        word_count = len(entry.split()) if entry else 0
        wc_color = "#10b981" if word_count >= 50 else "#f59e0b" if word_count >= 20 else "#ef4444"
        st.markdown(
            f"<span style='color:{wc_color};font-size:0.82rem'>"
            f"📝 {word_count} words "
            f"{'- Great depth!' if word_count>=50 else '- Add more detail!' if word_count>=20 else '- Too short'}"
            f"</span>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Entry", key="hs_journal_save", type="primary"):
                if not check_rate_limit("journal_save", st.session_state):
                    st.warning("Save rate-limited. Wait a moment!")
                else:
                    clean_entry = sanitize_input(entry, max_length=3000)
                    clean_topic = sanitize_input(topic or "Untitled", max_length=80)
                    if len(clean_entry) < 30:
                        st.warning("Write at least a few sentences!")
                    else:
                        xp_earned = min(15 + word_count//10, 35)
                        st.session_state.hs_journal.append({
                            "topic": clean_topic,
                            "entry": clean_entry,
                            "timestamp": _dt.datetime.now().strftime("%b %d, %Y %H:%M"),
                            "words": word_count,
                            "prompt": PROMPTS[st.session_state.hs_prompt_idx],
                        })
                        st.session_state.xp = st.session_state.get("xp", 0) + xp_earned
                        award_badge("🔬 PQC Researcher", xp=xp_earned)
                        mark_complete("research_journal")
                        st.success(f"✅ Entry saved! +{xp_earned} XP")
                        st.balloons()

        with col2:
            if st.session_state.hs_journal:
                all_text = "QuantumVault Academy - Research Journal\n" + "="*40 + "\n\n"
                for j in st.session_state.hs_journal:
                    all_text += f"Title: {j['topic']}\nDate: {j['timestamp']}\n\n{j['entry']}\n\n" + "-"*30 + "\n\n"
                st.download_button("📥 Export Journal", all_text, "PQC_Research_Journal.txt", "text/plain", key="export_hs_journal")

        if st.session_state.hs_journal:
            st.markdown("---")
            st.markdown(f"### 📚 Your Entries ({len(st.session_state.hs_journal)} total)")
            for j in reversed(st.session_state.hs_journal):
                with st.expander(f"📝 {j['topic']} - {j['timestamp']} ({j['words']} words)"):
                    st.markdown(f"*Prompt: {j['prompt']}*")
                    st.markdown("---")
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
        import streamlit.components.v1 as _math_comp
        import json as _json

        st.subheader("🧮 QuantumMath Challenge — 12 Levels!")
        st.markdown(
            "🔥 **120 unique questions across 12 levels.** "
            "Start at Beginner and work up to Grandmaster PQC. "
            "Speed bonuses, streak multipliers, and letter grades!"
        )

        xp = st.session_state.get("xp", 0)

        LEVELS = [
            {"name":"Level 1", "topic":"Modular Arithmetic", "xp_req":0,   "color":"#10b981","emoji":"🔢","grade":"Beginner"},
            {"name":"Level 2", "topic":"Prime Numbers",       "xp_req":0,   "color":"#10b981","emoji":"🔑","grade":"Beginner"},
            {"name":"Level 3", "topic":"Matrix Math",         "xp_req":0,   "color":"#3b82f6","emoji":"🏗️","grade":"Intermediate"},
            {"name":"Level 4", "topic":"Number Theory",       "xp_req":50,  "color":"#3b82f6","emoji":"📐","grade":"Intermediate"},
            {"name":"Level 5", "topic":"Lattice Problems",    "xp_req":100, "color":"#8b5cf6","emoji":"⚡","grade":"Advanced"},
            {"name":"Level 6", "topic":"Hash Functions",      "xp_req":150, "color":"#8b5cf6","emoji":"🌊","grade":"Advanced"},
            {"name":"Level 7", "topic":"Digital Signatures",  "xp_req":200, "color":"#f59e0b","emoji":"✍️","grade":"Expert"},
            {"name":"Level 8", "topic":"Kyber Internals",     "xp_req":250, "color":"#f59e0b","emoji":"🔐","grade":"Expert"},
            {"name":"Level 9", "topic":"Quantum Algorithms",  "xp_req":300, "color":"#ef4444","emoji":"⚛️","grade":"Master"},
            {"name":"Level 10","topic":"Advanced LWE",        "xp_req":400, "color":"#ef4444","emoji":"🧮","grade":"Master"},
            {"name":"Level 11","topic":"NIST Standards",      "xp_req":500, "color":"#4f46e5","emoji":"🏛️","grade":"Grandmaster"},
            {"name":"Level 12","topic":"Grandmaster PQC",     "xp_req":600, "color":"#4f46e5","emoji":"🛡️","grade":"Grandmaster"},
        ]

        ALL_QS = [
            [
                {"q":"17 mod 5 = ?","opts":["2","3","4","1"],"ans":0,"f":"RSA uses mod with huge primes. Kyber uses mod q=3329!"},
                {"q":"25 mod 7 = ?","opts":["3","4","2","5"],"ans":1,"f":"In Kyber all polynomial math happens mod q=3329!"},
                {"q":"(13+9) mod 11 = ?","opts":["0","2","3","1"],"ans":0,"f":"Modular addition wraps around just like a clock!"},
                {"q":"100 mod 13 = ?","opts":["9","10","11","8"],"ans":0,"f":"100 = 7x13 + 9. Modular reduction keeps numbers small!"},
                {"q":"(7x8) mod 5 = ?","opts":["1","2","3","4"],"ans":0,"f":"56 mod 5 = 1. Kyber multiplies polynomials mod 3329!"},
                {"q":"15 mod 15 = ?","opts":["0","1","15","5"],"ans":0,"f":"Any number mod itself = 0. Important for Kyber!"},
                {"q":"2^10 mod 7 = ?","opts":["2","3","4","1"],"ans":0,"f":"1024 mod 7 = 2. Modular exponentiation powers RSA!"},
                {"q":"(-3) mod 7 = ?","opts":["4","3","1","5"],"ans":0,"f":"Add modulus until positive: -3+7=4. Used in lattice math!"},
                {"q":"Kyber modulus q equals?","opts":["3329","3999","4096","2048"],"ans":0,"f":"q=3329 is prime and NTT-friendly — perfect for Kyber!"},
                {"q":"(5x6) mod 11 = ?","opts":["8","7","9","6"],"ans":0,"f":"30 mod 11 = 8. Modular multiplication is in every crypto op!"},
            ],
            [
                {"q":"Which is prime?","opts":["97","91","87","93"],"ans":0,"f":"97 has no factors except 1 and 97!"},
                {"q":"Prime factors of 15?","opts":["3 and 5","3 and 4","5 and 7","2 and 7"],"ans":0,"f":"15=3x5. RSA multiplies primes — Shor factors them back!"},
                {"q":"gcd(12,8) = ?","opts":["4","3","2","6"],"ans":0,"f":"gcd is used in RSA key generation!"},
                {"q":"Which is NOT prime?","opts":["51","53","59","61"],"ans":0,"f":"51=3x17. Composite numbers break prime security!"},
                {"q":"a^p mod p = ? (p prime, Fermat)","opts":["a","1","0","p"],"ans":0,"f":"Fermat Little Theorem: a^p ≡ a mod p. Foundation of RSA!"},
                {"q":"Primes less than 10?","opts":["4","3","5","6"],"ans":0,"f":"2, 3, 5, 7 — four primes below 10!"},
                {"q":"Largest prime factor of 84?","opts":["7","6","4","3"],"ans":0,"f":"84=2x2x3x7. Factoring IS the RSA hard problem!"},
                {"q":"p=11, q=13, n=p*q = ?","opts":["143","134","141","131"],"ans":0,"f":"In RSA n=p*q is the public modulus. Shor factors n!"},
                {"q":"Euler phi(7) = ?","opts":["6","7","5","4"],"ans":0,"f":"phi(p)=p-1. RSA private key uses phi(n)!"},
                {"q":"Which breaks RSA by factoring?","opts":["Shor","Grover","Kyber","Dilithium"],"ans":0,"f":"Shor Algorithm factors n in polynomial quantum time!"},
            ],
            [
                {"q":"[1,2].[3,4] = ?","opts":["11","10","12","8"],"ans":0,"f":"1x3+2x4=11. Kyber uses matrix-vector products!"},
                {"q":"[[1,2],[3,4]] x [1,1] = ?","opts":["[3,7]","[1,4]","[2,6]","[4,8]"],"ans":0,"f":"[1+2,3+4]=[3,7]. This IS Kyber key generation: t=As+e!"},
                {"q":"Transpose of [[1,2],[3,4]]?","opts":["[[1,3],[2,4]]","[[4,3],[2,1]]","[[2,1],[4,3]]","[[1,2],[3,4]]"],"ans":0,"f":"Transpose swaps rows/cols. Kyber encapsulation uses A^T!"},
                {"q":"Kyber-512 matrix A dimension?","opts":["2x2","3x3","4x4","1x1"],"ans":0,"f":"Kyber-512 uses k=2, so A is 2x2 matrix of polynomials!"},
                {"q":"A=[[2,1],[1,3]], s=[1,2], As=?","opts":["[4,7]","[3,6]","[5,8]","[2,4]"],"ans":0,"f":"[2+2,1+6]=[4,7]. Kyber key gen: b=As+e mod q!"},
                {"q":"NTT speeds up what in Kyber?","opts":["Polynomial mult","Matrix inversion","Hash computation","Key storage"],"ans":0,"f":"NTT: O(n^2) to O(n log n). Makes Kyber 100x faster!"},
                {"q":"Norm of vector [3,4] = ?","opts":["5","7","12","25"],"ans":0,"f":"sqrt(9+16)=5. Short vector norms are central to SVP!"},
                {"q":"(x+1)(x+2) = ?","opts":["x^2+3x+2","x^2+2x+2","x^2+3x+1","x^2+x+2"],"ans":0,"f":"Kyber works with polynomial ring Rq=Zq[x]/(x^n+1)!"},
                {"q":"Kyber polynomial degree n = ?","opts":["256","128","512","1024"],"ans":0,"f":"All Kyber variants use n=256 coefficient polynomials!"},
                {"q":"Matrix mult AB: A is 2x3, B must start with?","opts":["3","2","1","4"],"ans":0,"f":"Inner dimensions must match: (2x3)(3xN)=2xN!"},
            ],
            [
                {"q":"Euler phi(prime p) = ?","opts":["p-1","p","p+1","p/2"],"ans":0,"f":"phi(p)=p-1. RSA uses phi(n)=(p-1)(q-1)!"},
                {"q":"gcd(35,14) = ?","opts":["7","5","14","2"],"ans":0,"f":"35=5x7, 14=2x7, gcd=7. Euclidean algorithm!"},
                {"q":"Modular inverse of 3 mod 7?","opts":["5","4","6","2"],"ans":0,"f":"3x5=15=2x7+1, so 3^(-1)=5 mod 7!"},
                {"q":"CRT solves?","opts":["Simultaneous modular equations","Prime factorization","Matrix inversion","Hash collisions"],"ans":0,"f":"Chinese Remainder Theorem — used in NTT for Kyber!"},
                {"q":"Euler phi(15) = ?","opts":["8","6","10","4"],"ans":0,"f":"phi(15)=phi(3)xphi(5)=2x4=8!"},
                {"q":"Extended Euclidean computes?","opts":["gcd and Bezout coefficients","Only gcd","Modular inverse only","Prime factors"],"ans":0,"f":"Bezout: gcd(a,b)=ax+by. Used for RSA private keys!"},
                {"q":"Multiplicative order of 2 mod 7?","opts":["3","6","7","2"],"ans":0,"f":"2^3=8 mod 7=1. Order relates to Shor period-finding!"},
                {"q":"DLP: given g^x mod p, find x. Hard because?","opts":["No efficient classical algorithm","Computers too slow","Numbers too big","Wrong math"],"ans":0,"f":"DLP is basis of Diffie-Hellman — broken by Shor!"},
                {"q":"phi(n) for RSA n=p*q equals?","opts":["(p-1)(q-1)","p*q-1","p+q","(p+q)/2"],"ans":0,"f":"RSA private key d = e^(-1) mod (p-1)(q-1)!"},
                {"q":"Modular inverse exists when?","opts":["gcd(a,n)=1","a is prime","n is prime","a<n"],"ans":0,"f":"a has inverse mod n only if gcd(a,n)=1 (coprime)!"},
            ],
            [
                {"q":"SVP stands for?","opts":["Shortest Vector Problem","Secure Vault Protocol","Symmetric Vector Product","Signature Verification Process"],"ans":0,"f":"SVP is NP-hard — foundation of lattice crypto security!"},
                {"q":"LWE: b=As+e. What is e?","opts":["Small noise vector","The secret","Public key","The message"],"ans":0,"f":"Noise e hides secret s — impossible to remove without s!"},
                {"q":"Kyber security reduces to?","opts":["Module-LWE","RSA factoring","Discrete log","SAT problem"],"ans":0,"f":"Breaking Kyber requires solving the hardest lattice problems!"},
                {"q":"CVP stands for?","opts":["Closest Vector Problem","Cipher Vault Protocol","Compressed Vector Product","Cryptographic Validation Process"],"ans":0,"f":"CVP: find closest lattice point to target. NP-hard!"},
                {"q":"Grover speedup on lattice SVP?","opts":["Minimal — still exponential","Square root","Exponential","Polynomial"],"ans":0,"f":"No quantum speedup on SVP! That is why lattice crypto is safe!"},
                {"q":"LWE noise distribution in Kyber?","opts":["Centered binomial","Uniform random","Gaussian","Binary"],"ans":0,"f":"CBD(eta) gives small coefficients — allows correct decryption!"},
                {"q":"Module-LWE uses what structure?","opts":["Polynomial rings","Integer matrices","Binary fields","Complex numbers"],"ans":0,"f":"MLWE uses ring Rq=Zq[x]/(x^256+1) for efficiency!"},
                {"q":"BKZ algorithm does what?","opts":["Lattice basis reduction","Hash computation","Key derivation","Polynomial mult"],"ans":0,"f":"BKZ is best known SVP approximation — Kyber params resist it!"},
                {"q":"SIS stands for?","opts":["Short Integer Solution","Secure Integer Scheme","Symmetric Integer System","Standard Integer Signature"],"ans":0,"f":"SIS hardness underlies Dilithium signature security!"},
                {"q":"Dimension of Kyber-768 lattice?","opts":["768","256","512","1024"],"ans":0,"f":"k=3, n=256, total 768-dimensional lattice!"},
            ],
            [
                {"q":"SHA-3 based on which construction?","opts":["Keccak sponge","Merkle-Damgard","Davies-Meyer","Matyas-Meyer"],"ans":0,"f":"Keccak won NIST hash competition in 2012!"},
                {"q":"Changing 1 bit changes ~what% of SHA-3 output?","opts":["50%","1%","100%","25%"],"ans":0,"f":"Avalanche effect: ~50% bits flip from one input bit!"},
                {"q":"SHA3-256 output size?","opts":["256 bits","512 bits","128 bits","384 bits"],"ans":0,"f":"The number in the name tells you the output size!"},
                {"q":"Hash collision means?","opts":["Two inputs same hash","Hash runs slowly","Hash is reversible","Output all zeros"],"ans":0,"f":"SHA-3 is collision resistant — no known practical collisions!"},
                {"q":"SHA-3 internal state size?","opts":["1600 bits","512 bits","256 bits","1024 bits"],"ans":0,"f":"5x5x64 bit state = 1600 bits total!"},
                {"q":"SPHINCS+ uses hash functions because?","opts":["Security does not depend on lattices","Hashes are faster","Default quantum safe","Smaller signatures"],"ans":0,"f":"If lattices are broken, SPHINCS+ backup is pure hash-based!"},
                {"q":"Grover reduces SHA3-256 security to?","opts":["128 bits","64 bits","256 bits","32 bits"],"ans":0,"f":"2^256 to 2^128 quantum. 128-bit still secure for 30+ years!"},
                {"q":"Which FIPS uses only hash functions?","opts":["FIPS 205 (SPHINCS+)","FIPS 203 (Kyber)","FIPS 204 (Dilithium)","FIPS 206 (Falcon)"],"ans":0,"f":"SPHINCS+ relies only on SHA-3 — no lattice math needed!"},
                {"q":"Merkle tree root proves?","opts":["Integrity of all leaves","Single file correct","Hash is correct","Key is valid"],"ans":0,"f":"SPHINCS+ uses Merkle trees internally for its signature!"},
                {"q":"SHA-3 absorption phase does?","opts":["XORs input into state","Outputs hash","Generates keys","Computes modular inverse"],"ans":0,"f":"Keccak absorbs input blocks via XOR then permutes 24 rounds!"},
            ],
            [
                {"q":"Digital signature proves?","opts":["Authenticity and integrity","Only authenticity","Only integrity","File size"],"ans":0,"f":"Signatures prove WHO sent it AND it was not modified!"},
                {"q":"Dilithium based on?","opts":["Module-LWE","RSA factoring","SHA-3 preimage","Discrete log"],"ans":0,"f":"ML-DSA (Dilithium) = Module Lattice Digital Signature!"},
                {"q":"Rejection sampling in Dilithium prevents?","opts":["Secret key leakage","Slow signing","Large signatures","Quantum attacks"],"ans":0,"f":"Without rejection sampling each signature leaks bits of key s!"},
                {"q":"Falcon signatures vs Dilithium: Falcon is?","opts":["Much smaller","Much larger","Same size","Faster to verify"],"ans":0,"f":"Falcon-512: 666 bytes vs Dilithium2: 2420 bytes!"},
                {"q":"Which NIST standard for IoT signatures?","opts":["FIPS 206 (Falcon)","FIPS 204 (Dilithium)","FIPS 205 (SPHINCS+)","FIPS 203 (Kyber)"],"ans":0,"f":"Smallest signatures = Falcon = best for constrained devices!"},
                {"q":"Fiat-Shamir transform converts?","opts":["Interactive proof to signature","Hash to key","Lattice to matrix","Prime to polynomial"],"ans":0,"f":"Dilithium uses Fiat-Shamir with Aborts (FSwA)!"},
                {"q":"To verify Dilithium signature you need?","opts":["Public key and message","Private key only","Hash of message","Secret noise"],"ans":0,"f":"Anyone can verify but only private key holder can sign!"},
                {"q":"SPHINCS+ backup standard because?","opts":["Very large signatures","Lower security","Slower keygen","Less tested"],"ans":0,"f":"8-50KB signatures are fine for infrequent CA certs!"},
                {"q":"Kyber is NOT a signature scheme because?","opts":["It is a KEM not signature","Too slow","Wrong math","NIST rejected it"],"ans":0,"f":"Use Kyber for key exchange AND Dilithium for signatures!"},
                {"q":"SLH-DSA in FIPS 205 stands for?","opts":["Stateless Hash-based Digital Signature","Symmetric Lattice Hash DSA","Secure Lightweight Hash DSA","Standard LWE Hash DSA"],"ans":0,"f":"SPHINCS+ = Stateless Hash-based Digital Signature Algorithm!"},
            ],
            [
                {"q":"Kyber-768 security level?","opts":["192 bits","128 bits","256 bits","512 bits"],"ans":0,"f":"Kyber-512=128, Kyber-768=192, Kyber-1024=256 bit security!"},
                {"q":"NTT reduces polynomial mult from?","opts":["O(n^2) to O(n log n)","O(n) to O(log n)","O(n^3) to O(n^2)","O(2^n) to O(n)"],"ans":0,"f":"NTT makes Kyber 100x faster than naive polynomial mult!"},
                {"q":"Kyber public key t = ?","opts":["As + e","A + s","A * e","s + e mod q"],"ans":0,"f":"t=As+e: matrix times secret plus noise mod q=3329!"},
                {"q":"Kyber secret s coefficients from?","opts":["Centered binomial CBD","Uniform [0,q)","Gaussian","Binary {0,1}"],"ans":0,"f":"Small CBD coefficients allow correct decryption after noise!"},
                {"q":"In Kyber encapsulation, client sends?","opts":["Ciphertext (u,v)","Private key","Random seed","Hash of message"],"ans":0,"f":"Ciphertext c=(u,v) encapsulates the shared secret!"},
                {"q":"Kyber is IND-CCA2 secure meaning?","opts":["Secure vs adaptive chosen ciphertext","Only vs passive attacks","Timing attack secure","Post-quantum only"],"ans":0,"f":"IND-CCA2 is required for real protocols like TLS!"},
                {"q":"Compress function in Kyber does?","opts":["Reduces ciphertext size","Increases security","Speeds NTT","Generates randomness"],"ans":0,"f":"Compression trades tiny security margin for smaller ciphertext!"},
                {"q":"Kyber polynomial ring is?","opts":["Zq[x]/(x^256+1)","Z[x]/(x^256-1)","Zq[x]/x^256","Z2[x]/(x^256+1)"],"ans":0,"f":"x^256+1 is chosen for efficient NTT computation!"},
                {"q":"Decapsulation uses which key?","opts":["Kyber private key s","Alice public key","Random seed","Matrix A"],"ans":0,"f":"Only the private key s can recover the shared secret!"},
                {"q":"CBD(eta=2) produces values in range?","opts":["[-2,2]","[0,q)","[-q/2,q/2]","{0,1}"],"ans":0,"f":"CBD(2) gives very small noise — essential for Kyber correctness!"},
            ],
            [
                {"q":"Shor solves what in polynomial time?","opts":["Integer factorization","SVP","SHA-3 preimage","LWE"],"ans":0,"f":"RSA-2048 falls in hours to Shor on a large quantum computer!"},
                {"q":"Grover speedup is?","opts":["Quadratic sqrt(N)","Exponential","Linear","Logarithmic"],"ans":0,"f":"sqrt speedup is not enough to break 256-bit keys!"},
                {"q":"Qubit can be?","opts":["0 and 1 simultaneously","Only 0","Only 1","0 or 1 sequentially"],"ans":0,"f":"Superposition: qubit = alpha|0> + beta|1>!"},
                {"q":"Shor uses QFT to find?","opts":["Period of modular exponentiation","Shortest lattice vector","Hash preimage","Prime factors directly"],"ans":0,"f":"Period r of f(x)=a^x mod n then GCD gives factors!"},
                {"q":"Logical qubits to break RSA-2048?","opts":["~4000","~100","~1 million","~20"],"ans":0,"f":"~4000 error-corrected logical qubits needed — not yet!"},
                {"q":"Harvest-now-decrypt-later means?","opts":["Collect encrypted data now, decrypt later with quantum","Decrypt in real time with AI","Store quantum states","Break encryption immediately"],"ans":0,"f":"Nation states may already be collecting encrypted data TODAY!"},
                {"q":"Which NIST algo is immune to Shor?","opts":["Kyber (ML-KEM)","RSA-4096","ECDH-521","Diffie-Hellman"],"ans":0,"f":"Shor only attacks factoring and discrete log — not lattices!"},
                {"q":"Quantum entanglement enables?","opts":["Correlated qubit measurements","Independent operations","Classical speedup","Parallel memory"],"ans":0,"f":"Entanglement is essential for quantum error correction!"},
                {"q":"Post-quantum crypto protects against?","opts":["Both classical and quantum","Only quantum","Only classical","Side channel only"],"ans":0,"f":"NIST standards must be secure against ALL computers!"},
                {"q":"Grover reduces AES-256 security to?","opts":["128 bits","64 bits","256 bits","32 bits"],"ans":0,"f":"2^256 to 2^128 quantum. AES-256 remains safe!"},
            ],
            [
                {"q":"MLWE vs LWE: MLWE is?","opts":["More efficient same security","Less secure but faster","Harder to implement","NIST only"],"ans":0,"f":"MLWE gives O(n) key sizes vs O(n^2) for LWE!"},
                {"q":"LWR differs from LWE by?","opts":["Rounding replaces random noise","Using matrices not vectors","Adding more noise","Removing secret"],"ans":0,"f":"LWR: b=round(As/p) mod q — deterministic noise!"},
                {"q":"LWE worst-case to average-case proved by?","opts":["Regev 2005","Shor 1994","Diffie-Hellman","NIST"],"ans":0,"f":"Regev proved LWE hardness reduces to worst-case SVP!"},
                {"q":"MLWE security increases when?","opts":["k (matrix dimension) increases","Noise decreases","q decreases","n decreases"],"ans":0,"f":"Kyber-1024 uses k=4 vs Kyber-512 k=2 for more security!"},
                {"q":"x^n+1 chosen for?","opts":["NTT efficiency","Better security","Smaller keys","NIST requirement"],"ans":0,"f":"x^256+1 makes NTT maximally efficient for Kyber!"},
                {"q":"LWE decryption fails when?","opts":["Noise too large to round off","Key gen fails","Matrix A wrong","Ciphertext corrupted"],"ans":0,"f":"Kyber params ensure failure probability below 2^-139!"},
                {"q":"Module-SIS underlies security of?","opts":["Dilithium","Kyber","SPHINCS+","Falcon"],"ans":0,"f":"SIS: find short vector in lattice kernel — Dilithium uses it!"},
                {"q":"Converting LWE to RLWE gains?","opts":["Smaller keys faster ops","Higher security","Simpler implementation","Quantum resistance"],"ans":0,"f":"RLWE keys are O(n) vs LWE O(n^2) — massive efficiency gain!"},
                {"q":"Higher CBD eta means?","opts":["Larger noise harder to invert","Smaller noise","Same noise","Better correctness"],"ans":0,"f":"Higher eta = larger noise = harder LWE = more security!"},
                {"q":"Kyber q=3329 chosen because?","opts":["Prime and NTT-friendly","Largest prime below 4096","NIST random choice","Easy to compute"],"ans":0,"f":"3329 = 2^8 * 13 + 1, allowing efficient NTT in Z_3329!"},
            ],
            [
                {"q":"NIST PQC final standards published?","opts":["August 2024","June 2022","January 2023","December 2025"],"ans":0,"f":"FIPS 203/204/205/206 published August 2024 — history!"},
                {"q":"How many algorithms initially evaluated?","opts":["69","44","12","100"],"ans":0,"f":"69 submitted 2017, reduced through 3 rounds to 4 standards!"},
                {"q":"FIPS 203 is for?","opts":["ML-KEM (Kyber)","ML-DSA (Dilithium)","SLH-DSA (SPHINCS+)","FN-DSA (Falcon)"],"ans":0,"f":"FIPS 203 = ML-KEM = Kyber = key encapsulation!"},
                {"q":"NSM-10 requires migration by?","opts":["2035","2030","2040","2028"],"ans":0,"f":"National Security Memorandum 10 sets 2035 federal deadline!"},
                {"q":"Best standard for CA certificates?","opts":["FIPS 205 (SPHINCS+)","FIPS 203 (Kyber)","FIPS 204 (Dilithium)","FIPS 206 (Falcon)"],"ans":0,"f":"SPHINCS+ large signatures fine for infrequent CA certs!"},
                {"q":"Crypto-agility means?","opts":["Systems can swap algorithms easily","Use multiple algos simultaneously","Avoid standardization","Test continuously"],"ans":0,"f":"Crypto-agile systems can adopt future PQC updates easily!"},
                {"q":"FIPS 206 (Falcon) based on?","opts":["NTRU lattices","Module-LWE","Hash chains","Ring-SIS"],"ans":0,"f":"FN-DSA = Fast-Fourier lattice-based compact signature from NTRU!"},
                {"q":"Hybrid PQC combines classical + PQC to?","opts":["Maintain security if either breaks","Double speed","Reduce key size","Simplify impl"],"ans":0,"f":"NIST recommends hybrid during transition period!"},
                {"q":"Dilithium-2 signature size?","opts":["2420 bytes","666 bytes","8080 bytes","512 bytes"],"ans":0,"f":"Dilithium-2: 2420B sig, 1312B pubkey, 2528B privkey!"},
                {"q":"Which algo NOT selected as NIST primary?","opts":["NTRU","Kyber","Dilithium","SPHINCS+"],"ans":0,"f":"NTRU was finalist but NIST preferred Kyber for KEM!"},
            ],
            [
                {"q":"Kyber security reduction chain?","opts":["MLWE to SVP","RSA to factoring","DLP to Shor","Hash to collision"],"ans":0,"f":"Breaking Kyber requires solving worst-case SVP — provably!"},
                {"q":"Dilithium rejection threshold uses?","opts":["Infinity norm of z","Euclidean norm of s","SHA-3 of message","Matrix A norm"],"ans":0,"f":"If |z|_inf >= gamma1-beta, reject — prevents key leakage!"},
                {"q":"Falcon requires float precision because?","opts":["Gaussian sampling over NTRU lattice","NTT computation","Hash computation","Key compression"],"ans":0,"f":"Gaussian sampling needs 64-bit floats — hard to implement safely!"},
                {"q":"Kyber-768 claims 180-bit not 192-bit security why?","opts":["BKZ attacks reduce below theory","Grover reduces it","Shor partially applies","Parameter error"],"ans":0,"f":"BKZ provides asymptotic advantage — always slightly below theoretical!"},
                {"q":"FSwA ensures?","opts":["Zero-knowledge without s leakage","Faster signing","Smaller keys","RSA compatibility"],"ans":0,"f":"Zero-knowledge: attackers learn NOTHING about s from signatures!"},
                {"q":"SPHINCS+ hypertree structure?","opts":["Tree of XMSS trees signing WOTS+ keys","Single Merkle tree","Binary hash tree","Lattice tree"],"ans":0,"f":"Hypertree allows stateless signing unlike plain XMSS!"},
                {"q":"PQC TLS 1.3 handshake with Kyber?","opts":["1 encapsulation + 1 decapsulation","2 encapsulations","1 encapsulation only","4 total ops"],"ans":0,"f":"Client encapsulates, server decapsulates — one KEM op!"},
                {"q":"CRYSTALS stands for?","opts":["Cryptographic Suite for Algebraic Lattices","Compressed Reactive Algebra TLS System","Cross-Ring Algorithmic Torsion Lattice Solution","Nothing"],"ans":0,"f":"Kyber and Dilithium are both CRYSTALS family algorithms!"},
                {"q":"Quantum with 1M logical qubits breaks RSA-2048 in?","opts":["Hours","Centuries","Milliseconds","Years"],"ans":0,"f":"Shor runs in polynomial time — just needs enough stable qubits!"},
                {"q":"Module-SIS + Module-LWE together underlie?","opts":["Dilithium (FIPS 204)","Kyber (FIPS 203)","SPHINCS+ (FIPS 205)","Falcon (FIPS 206)"],"ans":0,"f":"Dilithium uses both MLWE for keys AND MSIS for signatures!"},
            ],
        ]

        st.markdown("---")
        level_cols = st.columns(6)
        for i, lvl in enumerate(LEVELS):
            with level_cols[i % 6]:
                unlocked = xp >= lvl["xp_req"]
                completed = st.session_state.get(f"math_done_{i}", False)
                c = lvl["color"]
                bg = c + "20" if completed else "#1e293b"
                border = "2px solid " + c if unlocked else "1px solid #334155"
                emoji = lvl["emoji"] if unlocked else "🔒"
                name_color = c if unlocked else "#888"
                grade_txt = "✅" if completed else lvl["grade"]
                st.markdown(
                    f"<div style='background:{bg};border:{border};"
                    f"border-radius:10px;padding:8px 4px;text-align:center;margin:3px'>"
                    f"<div style='font-size:1.2rem'>{emoji}</div>"
                    f"<div style='font-size:0.65rem;font-weight:bold;color:{name_color}'>{lvl['name']}</div>"
                    f"<div style='font-size:0.6rem;color:#888'>{grade_txt}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        st.markdown("---")

        level_names = []
        for i, lvl in enumerate(LEVELS):
            unlocked = xp >= lvl["xp_req"]
            if unlocked:
                level_names.append(lvl["emoji"] + " " + lvl["name"] + ": " + lvl["topic"])
            else:
                level_names.append("🔒 " + lvl["name"] + " — needs " + str(lvl["xp_req"]) + " XP (you have " + str(xp) + ")")

        sel = st.selectbox("Choose your level:", level_names, key="math_sel")
        sel_idx = level_names.index(sel)
        sel_lvl = LEVELS[sel_idx]
        color = sel_lvl["color"]

        if xp < sel_lvl["xp_req"]:
            st.warning(f"🔒 Need {sel_lvl['xp_req']} XP to unlock {sel_lvl['name']}!")
        else:
            st.markdown(
                f"<div style='background:{color}15;border:2px solid {color}50;"
                f"border-radius:12px;padding:14px;margin:8px 0'>"
                f"<h3 style='color:{color};margin:0'>{sel_lvl['emoji']} {sel_lvl['name']}: {sel_lvl['topic']}</h3>"
                f"<span style='background:{color}25;color:{color};font-size:0.75rem;"
                f"padding:2px 8px;border-radius:100px'>{sel_lvl['grade']} · 10 questions · 30s timer · speed bonuses</span>"
                f"</div>",
                unsafe_allow_html=True
            )

            if st.button("▶ Start " + sel_lvl["name"] + "!", key="math_start_btn", type="primary"):
                st.session_state.math_game_active = True
                st.session_state.math_level = sel_idx
                st.rerun()

            if st.session_state.get("math_game_active") and st.session_state.get("math_level") == sel_idx:
                qs = ALL_QS[sel_idx]
                qs_json = _json.dumps(qs)

                _math_comp.html(f"""
<style>
body{{margin:0;background:#0f172a;font-family:sans-serif;color:white;padding:10px;}}
.wrap{{max-width:540px;margin:0 auto;}}
.hud{{display:flex;gap:5px;margin-bottom:8px;}}
.hb{{background:#1e293b;border:1px solid #334155;border-radius:8px;padding:5px 8px;font-size:11px;font-weight:bold;color:#a5b4fc;flex:1;text-align:center;}}
.qbox{{background:#1e293b;border:1px solid {color}40;border-radius:12px;padding:16px;margin:6px 0;}}
.qt{{font-size:1.1rem;font-weight:bold;color:white;margin-bottom:10px;}}
.opts{{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:8px 0;}}
.opt{{padding:10px;border-radius:8px;border:2px solid #334155;cursor:pointer;font-size:12px;font-weight:bold;background:#0f172a;color:#a5b4fc;text-align:center;transition:all 0.15s;}}
.opt:hover{{border-color:{color};background:{color}15;}}
.opt.correct{{border-color:#10b981;background:rgba(16,185,129,0.2);color:#10b981;}}
.opt.wrong{{border-color:#ef4444;background:rgba(239,68,68,0.15);color:#ef4444;}}
.fb{{padding:9px;border-radius:8px;margin:5px 0;font-size:12px;text-align:center;display:none;}}
.fb.ok{{background:rgba(16,185,129,0.15);border:1px solid #10b981;color:#10b981;}}
.fb.bad{{background:rgba(239,68,68,0.12);border:1px solid #ef4444;color:#ef4444;}}
.fc{{background:rgba(79,70,229,0.12);border:1px solid rgba(79,70,229,0.35);border-radius:8px;padding:7px;margin:5px 0;font-size:11px;color:#a5b4fc;text-align:center;display:none;}}
.nb{{width:100%;padding:10px;border-radius:8px;border:none;cursor:pointer;font-size:13px;font-weight:bold;background:{color};color:white;margin-top:7px;display:none;}}
.tb{{height:6px;background:#334155;border-radius:3px;margin:5px 0;overflow:hidden;}}
.tf{{height:100%;border-radius:3px;transition:width 0.1s;}}
.done{{background:rgba(16,185,129,0.08);border:2px solid #10b981;border-radius:12px;padding:20px;text-align:center;display:none;}}
</style>
<div class="wrap">
<div class="hud">
    <div class="hb">Score<br><b id="sc">0</b></div>
    <div class="hb">Correct<br><b id="ok">0</b></div>
    <div class="hb">Wrong<br><b id="wr">0</b></div>
    <div class="hb">Time<br><b id="tm">30</b>s</div>
    <div class="hb">Q<br><b id="qn">1</b>/10</div>
    <div class="hb">Streak<br><b id="streak">0</b>🔥</div>
</div>
<div class="tb"><div class="tf" id="tf" style="width:100%;background:{color}"></div></div>
<div class="qbox" id="qbox">
    <div class="qt" id="qt"></div>
    <div class="opts" id="opts"></div>
    <div class="fb" id="fb"></div>
    <div class="fc" id="fc"></div>
    <button class="nb" id="nb" onclick="nextQ()">Next ➡️</button>
</div>
<div class="done" id="done">
    <div style="font-size:2.5rem" id="done-emoji">🏆</div>
    <h2 style="color:{color};margin:8px 0" id="done-title">Level Complete!</h2>
    <p id="dm" style="color:#888;margin:8px 0"></p>
    <button onclick="restart()" style="padding:9px 22px;border-radius:8px;border:none;cursor:pointer;background:{color};color:white;font-size:13px;font-weight:bold;">🔄 Play Again</button>
</div>
</div>
<script>
var QS={qs_json};
var qi=0,sc=0,ok=0,wr=0,answered=false,tl=30,ti,streak=0;
function loadQ(){{
    if(qi>=QS.length){{showDone();return;}}
    answered=false;
    var q=QS[qi];
    document.getElementById("qt").textContent=q.q;
    document.getElementById("qn").textContent=(qi+1);
    ["fb","fc"].forEach(function(id){{document.getElementById(id).style.display="none";}});
    document.getElementById("nb").style.display="none";
    var od=document.getElementById("opts");od.innerHTML="";
    for(var i=0;i<q.opts.length;i++){{
        var b=document.createElement("button");b.className="opt";
        b.textContent=q.opts[i];b.setAttribute("data-i",i);
        b.onclick=function(){{answer(parseInt(this.getAttribute("data-i")));}}
        od.appendChild(b);
    }}
    clearInterval(ti);tl=30;
    ti=setInterval(function(){{
        tl--;document.getElementById("tm").textContent=tl;
        var pct=(tl/30)*100;var f=document.getElementById("tf");
        f.style.width=pct+"%";f.style.background=tl>15?"{color}":tl>8?"#f59e0b":"#ef4444";
        if(tl<=0){{clearInterval(ti);if(!answered)timeUp();}}
    }},1000);
}}
function answer(i){{
    if(answered)return;answered=true;clearInterval(ti);
    var q=QS[qi];var correct=(i===q.ans);
    document.querySelectorAll(".opt").forEach(function(b,j){{
        if(j===q.ans)b.classList.add("correct");
        else if(j===i&&!correct)b.classList.add("wrong");
        b.onclick=null;
    }});
    if(correct){{ok++;streak++;var bonus=Math.floor(tl/5);var pts=10+bonus+(streak>=3?5:0);sc+=pts;
        var fb=document.getElementById("fb");fb.className="fb ok";
        fb.textContent="✅ Correct! +"+pts+"pts"+(streak>=3?" 🔥x"+streak+" streak!":"");
        fb.style.display="block";
    }}else{{wr++;streak=0;sc=Math.max(0,sc-5);
        var fb=document.getElementById("fb");fb.className="fb bad";
        fb.textContent="❌ Wrong! Answer: "+q.opts[q.ans];fb.style.display="block";
    }}
    document.getElementById("fc").textContent="💡 "+q.f;document.getElementById("fc").style.display="block";
    document.getElementById("nb").style.display="block";
    document.getElementById("sc").textContent=sc;document.getElementById("ok").textContent=ok;
    document.getElementById("wr").textContent=wr;document.getElementById("streak").textContent=streak;
}}
function timeUp(){{
    answered=true;streak=0;var q=QS[qi];
    document.querySelectorAll(".opt").forEach(function(b,j){{if(j===q.ans)b.classList.add("correct");b.onclick=null;}});
    var fb=document.getElementById("fb");fb.className="fb bad";
    fb.textContent="⏰ Time up! Answer: "+q.opts[q.ans];fb.style.display="block";
    document.getElementById("fc").textContent="💡 "+q.f;document.getElementById("fc").style.display="block";
    document.getElementById("nb").style.display="block";document.getElementById("streak").textContent=0;
}}
function nextQ(){{qi++;loadQ();}}
function showDone(){{
    document.getElementById("qbox").style.display="none";document.getElementById("done").style.display="block";
    var pct=Math.round(ok/QS.length*100);var grade=pct>=90?"A":pct>=80?"B":pct>=70?"C":pct>=60?"D":"F";
    document.getElementById("done-emoji").textContent=pct>=90?"🏆":pct>=80?"⭐":"👍";
    document.getElementById("done-title").textContent="Grade "+grade+" — "+ok+"/"+QS.length+" correct";
    document.getElementById("dm").textContent="Score: "+sc+" | "+pct+"% correct";
}}
function restart(){{
    qi=0;sc=0;ok=0;wr=0;streak=0;answered=false;
    document.getElementById("qbox").style.display="block";document.getElementById("done").style.display="none";
    ["sc","ok","wr","streak"].forEach(function(id){{document.getElementById(id).textContent=0;}});
    loadQ();
}}
loadQ();
</script>
""", height=520)

                done_key = f"math_done_{sel_idx}"
                xp_reward = (sel_idx + 1) * 15
                if not st.session_state.get(done_key):
                    if st.button(f"✅ Mark Complete! +{xp_reward} XP", key=f"math_done_btn_{sel_idx}"):
                        st.session_state[done_key] = True
                        st.session_state.xp = st.session_state.get("xp", 0) + xp_reward
                        if sel_idx == 11:
                            st.session_state.badges = st.session_state.get("badges", []) + ["🧮 Math Grandmaster"]
                            st.balloons()
                            st.success(f"🏆 GRANDMASTER! +{xp_reward} XP + Math Grandmaster badge!")
                        else:
                            st.success(f"Level {sel_idx+1} complete! +{xp_reward} XP!")
                        st.rerun()
                else:
                    st.success(f"✅ Level {sel_idx+1} completed! +{xp_reward} XP earned")

    with tab8:
        render_quantum_composer()
