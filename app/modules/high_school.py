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
    st.title("🔴 Cipher Corps - High School Edition")
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
            "    return [random.randint(0, mod-1) for _ in range(n)]\n"
            "\n"
            "def gen_public_key(s, mod):\n"
            "    n = len(s)\n"
            "    A = [[random.randint(0, mod-1) for _ in range(n)] for _ in range(n)]\n"
            "    e = [random.randint(-2, 2) for _ in range(n)]\n"
            "    b = [(sum(A[i][j]*s[j] for j in range(n))+e[i])%mod for i in range(n)]\n"
            "    return A, b\n"
            "\n"
            "def encrypt(A, b, bit, mod):\n"
            "    n = len(b)\n"
            "    r  = [random.randint(0, 1) for _ in range(n)]\n"
            "    e1 = [random.randint(-1, 1) for _ in range(n)]\n"
            "    e2 = random.randint(-1, 1)\n"
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

            def _gen_s(n, mod): return [_r.randint(0, mod-1) for _ in range(n)]
            def _gen_pk(s, mod):
                n = len(s)
                A = [[_r.randint(0, mod-1) for _ in range(n)] for _ in range(n)]
                e = [_r.randint(-2, 2) for _ in range(n)]
                b = [(sum(A[i][j]*s[j] for j in range(n))+e[i])%mod for i in range(n)]
                return A, b, e
            def _enc(A, b, m, mod):
                n = len(b)
                r  = [_r.randint(0,1) for _ in range(n)]
                e1 = [_r.randint(-1,1) for _ in range(n)]
                e2 = _r.randint(-1,1)
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
            sk2 = [_r2.randint(0, MOD_E-1) for _ in range(N_E)]
            A2 = [[_r2.randint(0, MOD_E-1) for _ in range(N_E)] for _ in range(N_E)]
            e2 = [_r2.randint(-noise_level, noise_level) for _ in range(N_E)]
            b2 = [(sum(A2[i][j]*sk2[j] for j in range(N_E))+e2[i])%MOD_E for i in range(N_E)]

            successes = 0
            for _ in range(10):
                bit = _r2.randint(0,1)
                r2 = [_r2.randint(0,1) for _ in range(N_E)]
                e1_2 = [_r2.randint(-noise_level, noise_level) for _ in range(N_E)]
                e2_2 = _r2.randint(-noise_level, noise_level)
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
            st.session_state.hs_prompt_idx = _rp.randint(0, len(PROMPTS)-1)

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
                st.session_state.hs_prompt_idx = _rp2.randint(0, len(PROMPTS)-1)
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
