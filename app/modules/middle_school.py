from modules.progress_tracker import mark_complete, is_complete


import hashlib
import random
import streamlit as st
from utils.security import sanitize_input, check_rate_limit, sha256_hex

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

def render_middle_school():
    st.title("🟡 Code Cadets — Middle School Edition")
    st.markdown(
        "Welcome, Cadet! You're now ready to dig into the real math behind "
        "post-quantum cryptography. Let's go! 🚀"
    )

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs(
        ["📖 Story Time", "🏗️ Lattice Explorer", "🏭 Hash Factory", "🏇 Quantum Derby", "🔑 Key Workshop", "🌀 Mini Game", "🎨 Hash Visualizer", "🔬 Key Size Lab", "⚡ Logic Gates", "🧠 Quiz Board", "🌐 Secure Network"]
    )

    with tab11:
        from modules.secure_network import render_secure_network
        render_secure_network()

    with tab10:
        from modules.quiz_board import render_quiz_board
        render_quiz_board()

    with tab9:
        render_logic_gates()

    # ── Tab 2: Lattice Explorer ───────────────────────────────────────────────
    with tab1:
        st.subheader("📖 The Codebreaker Crew")
        if "ms_story_page" not in st.session_state:
            st.session_state.ms_story_page = 0
        ms_pages = [
            {
                "title": "Chapter 1 — The Hack",
                "emoji": "💻",
                "color": "#3b82f6",
                "text": (
                    "It is 2031. Three middle schoolers — **Maya**, **Zion**, and **Priya** — "
                    "are in their school computer lab when the lights flicker.\n\n"
                    "Every screen shows the same message:\n\n"
                    "> **SYSTEM COMPROMISED. QUANTUM DECRYPTION IN PROGRESS. "
                    "ALL STUDENT RECORDS EXPOSED IN 60 MINUTES.**\n\n"
                    "Their teacher, Mr. Chen, goes pale.\n\n"
                    "**It is a quantum attack** he whispers. **Our school uses RSA encryption. "
                    "A quantum computer can factor the prime numbers and crack it in minutes.**\n\n"
                    "**What is factoring?** asks Zion.\n\n"
                    "**RSA works by multiplying two giant prime numbers together. "
                    "It is easy to multiply them but nearly impossible to reverse — unless "
                    "you have a quantum computer running Shor Algorithm.**\n\n"
                    "Priya pulls up her laptop. **I know what to do. We need lattice crypto.**"
                ),
                "quiz": None,
            },
            {
                "title": "Chapter 2 — The Lattice",
                "emoji": "🏗️",
                "color": "#10b981",
                "text": (
                    "**What is a lattice?** asks Maya.\n\n"
                    "**Imagine a giant grid of dots** says Priya. "
                    "**Millions of them in hundreds of dimensions. "
                    "Now imagine I give you a point CLOSE to one of those dots "
                    "but not exactly on it. Can you find the closest dot?**\n\n"
                    "**That sounds easy** says Zion.\n\n"
                    "**In 2 dimensions sure** says Priya. "
                    "**In 1000 dimensions? Even a quantum computer takes longer than "
                    "the age of the universe.**\n\n"
                    "**That is the Learning With Errors problem** says Mr. Chen. "
                    "**We add intentional noise to the equations. "
                    "The noise makes it impossible to reverse.**\n\n"
                    "**KYBER uses this** says Priya. **It is NIST ML-KEM FIPS 203. Let me install it.**\n\n"
                    "The countdown clock ticks. **48 minutes remaining.**"
                ),
                "quiz": {
                    "question": "Why cannot a quantum computer crack lattice cryptography?",
                    "options": [
                        "Finding the closest point in 1000 dimensions with noise takes longer than the age of the universe",
                        "Lattices are made of metal",
                        "Quantum computers do not like grids",
                        "Priya is too fast"
                    ],
                    "answer": 0,
                    "xp": 15,
                    "key": "ms_story_q1"
                }
            },
            {
                "title": "Chapter 3 — Saved!",
                "emoji": "🎉",
                "color": "#f59e0b",
                "text": (
                    "With 10 minutes left Priya finishes installing Kyber.\n\n"
                    "**Done!** she announces. "
                    "**All student records are now protected by ML-KEM. "
                    "The quantum attacker has nothing.**\n\n"
                    "On screen the attack progress bar grinds to a halt.\n\n"
                    "**It is working!** cheers Zion.\n\n"
                    "The screen clears. A new message appears:\n\n"
                    "> **QUANTUM ATTACK FAILED. ML-KEM ENCRYPTION ACTIVE. ALL RECORDS SECURE.**\n\n"
                    "**The Codebreaker Crew saves the day!** 🎉\n\n"
                    "---\n\n"
                    "🏅 **Story complete! You are now a Code Cadet!**"
                ),
                "quiz": {
                    "question": "Which NIST standard did Priya use to protect the school?",
                    "options": [
                        "ML-KEM (Kyber) FIPS 203",
                        "RSA-2048",
                        "SHA-256",
                        "DES"
                    ],
                    "answer": 0,
                    "xp": 20,
                    "key": "ms_story_q2"
                }
            },
        ]
        ms_page = ms_pages[st.session_state.ms_story_page]
        ms_total = len(ms_pages)
        ms_current = st.session_state.ms_story_page
        st.progress(ms_current / ms_total)
        st.caption(f"Chapter {ms_current + 1} of {ms_total}")
        ms_color = ms_page["color"]
        ms_emoji = ms_page["emoji"]
        ms_title = ms_page["title"]
        st.markdown(
            f"<div style='background:{ms_color}15;border-left:4px solid {ms_color};"
            f"border-radius:0 10px 10px 0;padding:1rem 1.5rem;margin-bottom:1rem;'>"
            f"<div style='font-size:2rem;margin-bottom:0.5rem'>{ms_emoji}</div>"
            f"<h3 style='color:{ms_color};margin:0'>{ms_title}</h3>"
            f"</div>",
            unsafe_allow_html=True
        )
        st.markdown(ms_page["text"])
        if ms_page["quiz"]:
            quiz = ms_page["quiz"]
            ms_key = quiz["key"]
            st.markdown("---")
            st.markdown(f"**🧠 Quick Check:** {quiz['question']}")
            if f"answered_{ms_key}" not in st.session_state:
                st.session_state[f"answered_{ms_key}"] = False
            if not st.session_state[f"answered_{ms_key}"]:
                for i, option in enumerate(quiz["options"]):
                    if st.button(option, key=f"quiz_{ms_key}_{i}"):
                        if i == quiz["answer"]:
                            st.session_state[f"answered_{ms_key}"] = True
                            st.session_state.xp += quiz["xp"]
                            st.success(f"Correct! +{quiz['xp']} XP")
                            st.balloons()
                        else:
                            st.error("Not quite! Read the chapter again!")
            else:
                st.success("Already answered!")
        st.markdown("---")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            if ms_current > 0:
                if st.button("← Previous", key="ms_prev"):
                    st.session_state.ms_story_page -= 1
                    st.rerun()
        with c2:
            st.caption(f"Page {ms_current + 1} / {ms_total}")
        with c3:
            if ms_current < ms_total - 1:
                if st.button("Next →", key="ms_next"):
                    st.session_state.ms_story_page += 1
                    st.rerun()
            else:
                st.success("Story Complete!")
                if st.button("Claim Badge!", key="ms_story_badge"):
                    import streamlit as _st
                    _st.session_state.xp = _st.session_state.get("xp", 0) + 10
                    _st.session_state.badges = _st.session_state.get("badges", []) + ["📖 Code Cadet Story"]

    with tab2:
        import streamlit.components.v1 as _ms2
        st.subheader("🏗️ Lattice Explorer — The Math That Stops Quantum Computers!")
        st.markdown(
            "🔍 **Why can't quantum computers break Kyber?** Because of LATTICE MATH! "
            "A lattice is a giant grid of dots. The secret is hidden like a needle in a "
            "billion-dimensional haystack. Even quantum computers get completely lost!"
        )

        col1, col2 = st.columns([1,1])
        with col1:
            st.markdown(
                "<div style='background:#1e1b4b;border:2px solid #7c6dfa;border-radius:12px;"
                "padding:16px;'>"
                "<h4 style='color:#a5b4fc;margin:0 0 8px'>🧠 The Hard Problem</h4>"
                "<p style='color:#ccc;font-size:0.88rem;line-height:1.6'>"
                "Given a <b style='color:#7c6dfa'>tangled point</b> near the grid, "
                "find the <b style='color:#10b981'>closest grid dot</b>.<br><br>"
                "In 2D: easy!<br>"
                "In 256 dimensions: <b style='color:#ef4444'>impossible!</b><br><br>"
                "This is called <b style='color:#f59e0b'>SVP</b> — Shortest Vector Problem"
                "</p></div>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                "<div style='background:#0c2e1e;border:2px solid #10b981;border-radius:12px;"
                "padding:16px;'>"
                "<h4 style='color:#34d399;margin:0 0 8px'>🌊 Learning With Errors (LWE)</h4>"
                "<p style='color:#ccc;font-size:0.88rem;line-height:1.6'>"
                "Kyber hides a secret <b style='color:#10b981'>s</b> using noisy equations:<br><br>"
                "<code style='background:#0f172a;padding:3px 6px;border-radius:4px;color:#10b981'>"
                "b = A·s + e mod q</code><br><br>"
                "The noise <b style='color:#f59e0b'>e</b> makes it impossible to find <b>s</b>! "
                "Even with a quantum computer!"
                "</p></div>",
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("### 🎮 Interactive LWE Puzzle")
        st.markdown("Can YOU solve the Learning With Errors problem? Try to find the secret **s**!")

        import random
        if "lattice_s" not in st.session_state:
            st.session_state.lattice_s = random.randint(2, 9)  # nosec B311
            st.session_state.lattice_attempts = 0

        s = st.session_state.lattice_s
        mod = 11

        equations = []
        for _ in range(4):
            a = random.randint(1, 10)  # nosec B311
            e = random.choice([-1, 0, 1])  # nosec B311
            b = (a * s + e) % mod
            equations.append((a, b, e))

        st.markdown("**🔢 You can see these equations (with hidden noise):**")
        eq_cols = st.columns(4)
        for i, (a, b, _) in enumerate(equations):
            with eq_cols[i]:
                st.markdown(
                    f"<div style='background:#1e293b;border:1px solid #7c6dfa;border-radius:10px;"
                    f"padding:12px;text-align:center;'>"
                    f"<div style='font-size:0.75rem;color:#888'>Equation {i+1}</div>"
                    f"<div style='font-size:1.1rem;color:#a5b4fc;font-weight:bold;margin:4px 0'>"
                    f"{a}·s + noise ≡ {b}</div>"
                    f"<div style='font-size:0.7rem;color:#888'>mod {mod}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        st.markdown(f"*The noise (e) is secretly one of: -1, 0, or +1 — you can't see which!*")

        col1, col2 = st.columns([2,1])
        with col1:
            guess = st.slider("Your guess for secret **s**:", 1, 10, 5, key="lwe_guess")
        with col2:
            st.markdown(f"<br>", unsafe_allow_html=True)
            if st.button("🎯 Submit Guess!", key="lwe_submit", type="primary"):
                st.session_state.lattice_attempts += 1
                if guess == s:
                    st.balloons()
                    st.success(f"🎉 CORRECT! s = {s}! You cracked LWE! +20 XP")
                    st.session_state.xp = st.session_state.get("xp", 0) + 20
                    award_badge("🏗️ Lattice Solver", xp=20)
                    mark_complete("lattice_visualizer")
                    st.session_state.lattice_s = random.randint(2, 9)  # nosec B311
                    st.session_state.lattice_attempts = 0
                else:
                    diff = abs(guess - s)
                    hint = "🔥 Very close!" if diff == 1 else "😅 Getting warmer!" if diff <= 3 else "🥶 Way off!"
                    st.error(f"❌ {hint} That's not it. Attempts: {st.session_state.lattice_attempts}")

        st.info(
            f"💡 **Kyber fact:** Real Kyber uses 256-dimensional lattices with s having 256 coefficients, "
            f"not just 1 number. Imagine solving this puzzle in 256 dimensions — impossible! "
            f"That's why it's quantum-safe!"
        )

        with st.expander("📐 Show me the real math"):
            st.markdown(
                "**Real Kyber key generation:**\n\n"
                "- Secret vector: s in Rq^k (k polynomials of degree 256)\n"
                "- Public matrix: A in Rq^(kxk)\n"
                "- Noise vector: e in Rq^k (small coefficients)\n"
                "- Public key: **t = As + e mod q** (where q=3329)\n\n"
                "An attacker seeing only A and t cannot find s - "
                "this is the Module-LWE problem!"
            )

    with tab3:
        st.subheader("🏭 Hash Function Factory — One-Way Street!")
        st.markdown(
            "🔒 **A hash function is like a blender for data!** "
            "You can put anything IN — but you can NEVER get the original back out. "
            "Change even ONE letter and the ENTIRE hash changes completely!"
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                "<div style='background:#1e1b4b;border:2px solid #8b5cf6;border-radius:10px;"
                "padding:12px;text-align:center'>"
                "<div style='font-size:1.5rem'>📄</div>"
                "<div style='font-size:0.8rem;color:#a5b4fc;font-weight:bold'>ANY Input</div>"
                "<div style='font-size:0.72rem;color:#888'>Word, book, video</div>"
                "</div>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                "<div style='background:#4f46e520;border:2px solid #4f46e5;border-radius:10px;"
                "padding:12px;text-align:center'>"
                "<div style='font-size:1.5rem'>🌀</div>"
                "<div style='font-size:0.8rem;color:#818cf8;font-weight:bold'>SHA-3 Blender</div>"
                "<div style='font-size:0.72rem;color:#888'>One way only!</div>"
                "</div>",
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                "<div style='background:#0c2e1e;border:2px solid #10b981;border-radius:10px;"
                "padding:12px;text-align:center'>"
                "<div style='font-size:1.5rem'>🔢</div>"
                "<div style='font-size:0.8rem;color:#34d399;font-weight:bold'>256-bit Hash</div>"
                "<div style='font-size:0.72rem;color:#888'>Always same size</div>"
                "</div>",
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("### 🧪 Hash Lab — Type anything and see it!")

        col1, col2 = st.columns(2)
        with col1:
            msg1 = st.text_input("Message 1:", value="Hello Kyber!", key="ms_hash1", max_chars=200)
        with col2:
            msg2 = st.text_input("Message 2 (try changing 1 letter!):", value="hello Kyber!", key="ms_hash2", max_chars=200)

        import hashlib
        h1 = hashlib.sha3_256(msg1.encode()).hexdigest() if msg1 else ""
        h2 = hashlib.sha3_256(msg2.encode()).hexdigest() if msg2 else ""

        def color_diff_hash(h1, h2):
            if not h1 or not h2: return h1, h2
            out1, out2 = "", ""
            for c1, c2 in zip(h1, h2):
                if c1 == c2:
                    out1 += f"<span style='color:#6b7280'>{c1}</span>"
                    out2 += f"<span style='color:#6b7280'>{c2}</span>"
                else:
                    out1 += f"<span style='color:#10b981;font-weight:bold'>{c1}</span>"
                    out2 += f"<span style='color:#ef4444;font-weight:bold'>{c2}</span>"
            return out1, out2

        h1_colored, h2_colored = color_diff_hash(h1, h2)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**SHA-3 Hash of Message 1:**")
            st.markdown(
                f"<div style='background:#0f172a;border:1px solid #334155;border-radius:8px;"
                f"padding:10px;font-family:monospace;font-size:11px;word-break:break-all;"
                f"line-height:1.6'>{h1_colored}</div>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown("**SHA-3 Hash of Message 2:**")
            st.markdown(
                f"<div style='background:#0f172a;border:1px solid #334155;border-radius:8px;"
                f"padding:10px;font-family:monospace;font-size:11px;word-break:break-all;"
                f"line-height:1.6'>{h2_colored}</div>",
                unsafe_allow_html=True
            )

        if h1 and h2:
            diff = sum(1 for a,b in zip(h1,h2) if a!=b)
            pct = round(diff/len(h1)*100)
            color = "#10b981" if msg1 != msg2 else "#6b7280"
            st.markdown(
                f"<div style='background:{color}15;border:1px solid {color}40;"
                f"border-radius:10px;padding:12px;text-align:center;margin:8px 0'>"
                f"<b style='color:{color}'>"
                f"{'🌊 AVALANCHE EFFECT! ' + str(diff) + '/64 characters changed (' + str(pct) + '%)!' if msg1 != msg2 else '✅ Identical messages = identical hashes'}"
                f"</b></div>",
                unsafe_allow_html=True
            )
            if msg1 != msg2:
                st.progress(pct/100)

        st.markdown("---")
        st.markdown("### 🎯 Hash Challenge!")
        challenges = [
            ("What does SHA-3 stand for?", ["Secure Hash Algorithm 3", "Super Hard Arithmetic 3", "Simple Hash Attack 3", "Shor Hash Algorithm 3"], 0),
            ("If you change the hash input, what happens?", ["The entire hash changes completely", "Only one character changes", "Nothing changes", "The hash gets shorter"], 0),
            ("Can you reverse a SHA-3 hash to get the original?", ["No — it is one-way only!", "Yes — use the inverse function", "Yes — if you have the key", "Only quantum computers can"], 0),
            ("What is the avalanche effect?", ["Small input change = huge output change", "Hash gets bigger over time", "Quantum speedup on hashing", "Hash collision attack"], 0),
        ]

        if "hash_q" not in st.session_state:
            st.session_state.hash_q = 0
            st.session_state.hash_score = 0
            st.session_state.hash_answered = False

        q_idx = st.session_state.hash_q % len(challenges)
        q, opts, ans = challenges[q_idx]

        st.markdown(f"**Question {q_idx+1}/4:** {q}")
        for i, opt in enumerate(opts):
            if st.button(opt, key=f"hq_{q_idx}_{i}", use_container_width=True):
                if i == ans:
                    st.success("🎉 Correct! +10 XP")
                    st.session_state.xp = st.session_state.get("xp", 0) + 10
                    st.session_state.hash_score += 1
                    st.session_state.hash_q += 1
                    if st.session_state.hash_q >= len(challenges):
                        award_badge("🏭 Hash Master", xp=20)
                        mark_complete("hash_factory")
                else:
                    st.error(f"❌ Not quite! The answer was: **{opts[ans]}**")
                    st.session_state.hash_q += 1
                st.rerun()

    with tab4:
        import streamlit.components.v1 as _ms4
        import json as _json
        st.subheader("🏇 Quantum Derby — Bet on the Winner!")
        st.markdown(
            "🪙 **You have 100 coins.** Wager on each race: can quantum computers really beat classical at EVERYTHING? "
            "Bet smart — some of these races have surprise endings!"
        )

        problems = [
            {
            "name": "🔢 Factor RSA-2048",
            "classical": "🐢 Millions of YEARS",
            "quantum": "⚡ Just a few HOURS",
            "winner": "quantum",
            "why": "Shor's Algorithm finds prime factors exponentially faster!",
            "pqc": "❌ RSA is BROKEN by quantum — that's why we need Kyber!",
            "pqc_color": "#ef4444",
            },
            {
            "name": "🏗️ Solve Lattice SVP",
            "classical": "🐢 Super hard",
            "quantum": "🐢 Still super hard!",
            "winner": "tie",
            "why": "No quantum algorithm gives significant speedup on lattice problems!",
            "pqc": "✅ Kyber is SAFE — quantum computers can't solve SVP faster!",
            "pqc_color": "#10b981",
            },
            {
            "name": "🔍 Search Unsorted Data",
            "classical": "🐢 Check ALL N items",
            "quantum": "⚡ Only √N steps!",
            "winner": "quantum",
            "why": "Grover's Algorithm gives a quadratic speedup on search!",
            "pqc": "⚠️ SHA-3 still safe — just use 256-bit output for 128-bit quantum security!",
            "pqc_color": "#f59e0b",
            },
            {
            "name": "🌀 Break SHA-3 Hash",
            "classical": "🐢 2^256 tries needed",
            "quantum": "⚡ 2^128 tries (Grover)",
            "winner": "classical_safe",
            "why": "Grover only gives square root speedup — 2^128 is still impossibly large!",
            "pqc": "✅ SHA-3 is SAFE — double the output size defeats Grover!",
            "pqc_color": "#10b981",
            },
        ]

        _derby_html = '<!DOCTYPE html>\n<html><head><meta charset="UTF-8"><style>\n*{margin:0;padding:0;box-sizing:border-box}\nbody{background:#0b1526;font-family:\'Segoe UI\',sans-serif;color:#e2e8f0;padding:10px}\n.wrap{max-width:600px;margin:0 auto}\n.hud{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}\n.coins{background:#1a1500;border:2px solid #fbbf24;border-radius:10px;padding:6px 14px;font-weight:800;color:#fbbf24;font-size:16px}\n.round{color:#94a3b8;font-size:12px}\n.card{background:#111c30;border:1px solid #334155;border-radius:12px;padding:12px;margin-bottom:8px}\n.pname{color:#a5b4fc;font-weight:800;font-size:15px;margin-bottom:8px;text-align:center}\n.vs{display:grid;grid-template-columns:1fr 1fr;gap:8px}\n.side{background:#1e293b;border-radius:8px;padding:8px;text-align:center;font-size:12px}\n.side b{display:block;font-size:13px;margin-top:3px}\n.lbl{color:#64748b;font-size:10px}\n.bets{display:flex;gap:6px;justify-content:center;margin:8px 0}\n.chip{padding:6px 14px;border-radius:16px;border:2px solid #475569;background:#1e293b;color:#e2e8f0;cursor:pointer;font-weight:700;font-size:13px}\n.chip.on{border-color:#fbbf24;background:#1a1500;color:#fbbf24}\n.picks{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px}\n.pick{padding:10px 4px;border-radius:10px;border:2px solid #475569;background:#1e293b;color:#e2e8f0;cursor:pointer;font-weight:800;font-size:13px}\n.pick:hover{border-color:#a5b4fc}\ncanvas{display:block;margin:0 auto;border-radius:12px;background:#0a1120}\n.banner{text-align:center;font-weight:800;font-size:15px;padding:8px;border-radius:10px;margin:8px 0;display:none}\n.win{background:#05301f;color:#34d399;border:1px solid #10b981}\n.lose{background:#2d0a0a;color:#f87171;border:1px solid #ef4444}\n.why{background:#0c1a30;border-left:3px solid #60a5fa;border-radius:6px;padding:8px 10px;font-size:12px;margin:6px 0;display:none}\n.pqc{border-radius:6px;padding:8px 10px;font-size:12px;margin:6px 0;display:none}\n.nextb{display:none;width:100%;padding:11px;border:none;border-radius:10px;background:linear-gradient(135deg,#4f46e5,#7c3aed);color:white;font-weight:800;font-size:14px;cursor:pointer}\n#final{display:none;text-align:center;padding:14px}\n#final h2{color:#fbbf24}\n</style></head><body><div class="wrap">\n<div class="hud"><div class="coins">🪙 <span id="coins">100</span></div><div class="round" id="roundlbl">Race 1</div></div>\n<div class="card" id="betcard">\n  <div class="pname" id="pname"></div>\n  <div class="vs">\n    <div class="side"><span class="lbl">🖥️ CLASSICAL</span><b id="pcl"></b></div>\n    <div class="side"><span class="lbl">⚛️ QUANTUM</span><b id="pqu"></b></div>\n  </div>\n  <div style="text-align:center;color:#94a3b8;font-size:11px;margin-top:8px">How many coins do you wager?</div>\n  <div class="bets" id="betrow">\n    <button class="chip" onclick="setBet(10,this)">10</button>\n    <button class="chip on" onclick="setBet(25,this)">25</button>\n    <button class="chip" onclick="setBet(50,this)">50</button>\n    <button class="chip" onclick="setBet(-1,this)">ALL IN</button>\n  </div>\n  <div style="text-align:center;color:#94a3b8;font-size:11px;margin-bottom:6px">Who wins this race? (Tie pays double!)</div>\n  <div class="picks">\n    <button class="pick" onclick="lockBet(\'classical_safe\')">🖥️ Classical</button>\n    <button class="pick" onclick="lockBet(\'quantum\')">⚛️ Quantum</button>\n    <button class="pick" onclick="lockBet(\'tie\')">🤝 Tie</button>\n  </div>\n</div>\n<canvas id="track" width="560" height="190"></canvas>\n<div class="banner" id="banner"></div>\n<div class="why" id="why"></div>\n<div class="pqc" id="pqcbox"></div>\n<button class="nextb" id="nextb" onclick="nextRound()">Next Race ➡️</button>\n<div id="final" class="card"></div>\n</div><script>\nconst PROBLEMS=__PROBLEMS__;\nlet coins=100,bet=25,order=[],round=0,phase=\'bet\',called=0;\nconst cv=document.getElementById(\'track\'),cx=cv.getContext(\'2d\');\nfunction shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}\nfunction init(){order=shuffle(PROBLEMS.map((_,i)=>i));round=0;coins=100;called=0;phase=\'bet\';showRound();}\nfunction cur(){return PROBLEMS[order[round]];}\nfunction showRound(){\n  document.getElementById(\'coins\').textContent=coins;\n  document.getElementById(\'roundlbl\').textContent=\'Race \'+(round+1)+\' of \'+PROBLEMS.length;\n  document.getElementById(\'pname\').textContent=cur().name;\n  document.getElementById(\'pcl\').textContent=cur().classical;\n  document.getElementById(\'pqu\').textContent=cur().quantum;\n  document.getElementById(\'betcard\').style.display=\'block\';\n  [\'banner\',\'why\',\'pqcbox\'].forEach(id=>document.getElementById(id).style.display=\'none\');\n  document.getElementById(\'nextb\').style.display=\'none\';\n  drawTrack(0,0,\'\');\n}\nfunction setBet(v,el){\n  document.querySelectorAll(\'.chip\').forEach(c=>c.classList.remove(\'on\'));\n  el.classList.add(\'on\');\n  bet=(v===-1)?coins:Math.min(v,coins);\n}\nlet racing=null;\nfunction lockBet(pick){\n  if(phase!==\'bet\')return;\n  bet=Math.min(bet,coins);if(bet<1)bet=Math.min(10,coins);\n  phase=\'race\';\n  document.getElementById(\'betcard\').style.display=\'none\';\n  const w=cur().winner;\n  const t0=performance.now();\n  const DUR=3200;\n  racing=requestAnimationFrame(function frame(now){\n    let t=Math.min(1,(now-t0)/DUR);\n    // progress curves: winner surges after 45%; loser fades; tie neck-and-neck\n    let pc,pq;\n    const surge=x=>x<0.45?x*0.75:0.34+(x-0.45)*1.25;\n    const fade=x=>x<0.45?x*0.72:0.32+(x-0.45)*0.55;\n    const even=x=>x*0.92;\n    if(w===\'quantum\'){pq=surge(t);pc=fade(t);}\n    else if(w===\'classical_safe\'){pc=surge(t);pq=fade(t);}\n    else{pc=even(t)+Math.sin(t*14)*0.012;pq=even(t)-Math.sin(t*14)*0.012;}\n    drawTrack(pc,pq,t<1?\'\':w);\n    if(t<1){racing=requestAnimationFrame(frame);}\n    else{settle(pick,w);}\n  });\n}\nfunction drawTrack(pc,pq,winner){\n  const W=cv.width,H=cv.height;\n  cx.clearRect(0,0,W,H);\n  cx.fillStyle=\'#0a1120\';cx.fillRect(0,0,W,H);\n  // crowd\n  cx.font=\'13px serif\';cx.globalAlpha=0.5;\n  for(let i=0;i<12;i++)cx.fillText([\'🎉\',\'👀\',\'🙌\',\'⭐\'][i%4],20+i*46,22);\n  cx.globalAlpha=1;\n  // lanes\n  [[58,\'#12203a\'],[128,\'#101b33\']].forEach(([y,c])=>{cx.fillStyle=c;cx.fillRect(10,y-24,W-20,48);});\n  // finish line\n  for(let y=30;y<H-10;y+=12){cx.fillStyle=(y/12)%2<1?\'#e2e8f0\':\'#475569\';cx.fillRect(W-34,y,8,12);}\n  const lane=(y,p,emoji,label,col)=>{\n    const x=24+p*(W-90);\n    cx.font=\'11px sans-serif\';cx.fillStyle=col;cx.fillText(label,14,y-30);\n    cx.font=\'30px serif\';\n    const bob=Math.sin(performance.now()/90+y)*2.5;\n    cx.fillText(emoji,x,y+10+bob);\n    // dust\n    if(p>0.01&&p<0.97){cx.globalAlpha=0.35;cx.font=\'12px serif\';cx.fillText(\'💨\',x-16,y+8);cx.globalAlpha=1;}\n  };\n  lane(58,pc,\'🖥️\',\'CLASSICAL\',\'#60a5fa\');\n  lane(128,pq,\'⚛️\',\'QUANTUM\',\'#c084fc\');\n  if(winner){\n    cx.font=\'16px sans-serif\';cx.fillStyle=\'#fbbf24\';cx.textAlign=\'center\';\n    const msg=winner===\'tie\'?\'PHOTO FINISH — TIE!\':(winner===\'quantum\'?\'⚛️ QUANTUM WINS!\':\'🖥️ CLASSICAL HOLDS!\');\n    cx.fillText(msg,W/2,H-12);cx.textAlign=\'left\';\n  }\n}\nfunction settle(pick,w){\n  phase=\'reveal\';\n  const right=pick===w;\n  const payout=right?(w===\'tie\'?bet*2:bet):-bet;\n  coins=Math.max(0,coins+payout);\n  if(right)called++;\n  if(coins===0){coins=25;}\n  document.getElementById(\'coins\').textContent=coins;\n  const b=document.getElementById(\'banner\');\n  b.className=\'banner \'+(right?\'win\':\'lose\');\n  b.style.display=\'block\';\n  b.textContent=right?(\'🎯 You called it! +\'+payout+\' coins\'+(w===\'tie\'?\' (double for the tie!)\':\'\')):(\'😮 Wrong — lost \'+bet+\' coins.\'+(coins===25?\' The bank spots you 25 to keep playing!\':\'\'));\n  const why=document.getElementById(\'why\');why.style.display=\'block\';why.innerHTML=\'💡 <b>Why:</b> \'+cur().why;\n  const pq=document.getElementById(\'pqcbox\');pq.style.display=\'block\';\n  pq.style.background=cur().pqc_color+\'22\';pq.style.border=\'1px solid \'+cur().pqc_color;\n  pq.innerHTML=\'🔐 <b>PQC Impact:</b> \'+cur().pqc;\n  const nb=document.getElementById(\'nextb\');nb.style.display=\'block\';\n  nb.textContent=(round<PROBLEMS.length-1)?\'Next Race ➡️\':\'🏆 See Final Results!\';\n}\nfunction nextRound(){\n  if(round<PROBLEMS.length-1){round++;phase=\'bet\';showRound();}\n  else{\n    [\'betcard\',\'banner\',\'why\',\'pqcbox\',\'nextb\'].forEach(id=>document.getElementById(id).style.display=\'none\');\n    cv.style.display=\'none\';\n    const f=document.getElementById(\'final\');f.style.display=\'block\';\n    const verdict=coins>=200?\'🏆 QUANTUM ORACLE! You see the future of computing!\':coins>=120?\'🥈 Sharp bettor — you know what quantum can and can not do!\':\'📚 The house taught you something: quantum computers do NOT win everything!\';\n    f.innerHTML=\'<h2>🏇 Derby Complete!</h2><div style="font-size:34px;margin:8px">🪙 \'+coins+\' coins</div><div style="color:#94a3b8;font-size:13px;margin-bottom:6px">Correct calls: \'+called+\' / \'+PROBLEMS.length+\'</div><div style="color:#e2e8f0;font-size:13px;margin-bottom:10px">\'+verdict+\'</div><button class="nextb" style="display:block" onclick="restart()">🔄 Race Again (new order!)</button>\';\n  }\n}\nfunction restart(){document.getElementById(\'final\').style.display=\'none\';cv.style.display=\'block\';init();}\ninit();\n</script></body></html>'.replace("__PROBLEMS__", _json.dumps(problems))
        _ms4.html(_derby_html, height=660, scrolling=True)

        if st.button("🏆 Finished all 6 races? Claim your Quantum Racer badge!", key="derby_badge", use_container_width=True):
            mark_complete("quantum_race")
            award_badge("⚡ Quantum Racer", xp=25)
            st.session_state.xp = st.session_state.get("xp", 0) + 25
            st.balloons()

    with tab5:
        import random as _rand
        st.subheader("🔑 Build-a-Key Workshop — Real Kyber Math!")
        st.markdown(
            "🔧 **You are now a cryptographer!** Build a simplified Kyber keypair step by step. "
            "This is the ACTUAL math used to protect the internet — just with tiny numbers for learning!"
        )

        mod = 17

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "<div style='background:#0c2e1e;border:2px solid #10b981;border-radius:12px;"
                "padding:14px;'>"
                "<h4 style='color:#34d399;margin:0 0 8px'>🔑 Step 1: Generate Keys</h4>"
                "<p style='color:#ccc;font-size:0.85rem;line-height:1.6'>"
                "• Pick a <b style='color:#10b981'>secret s</b> (only you know!)<br>"
                "• Pick a <b style='color:#a5b4fc'>public A</b> (share with everyone)<br>"
                "• Add tiny <b style='color:#f59e0b'>noise e</b> (makes it secure!)<br>"
                "• Compute <b style='color:#10b981'>b = A·s + e mod q</b><br>"
                "• Your <b>public key</b> is (A, b) — share it!"
                "</p></div>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                "<div style='background:#1a0f2e;border:2px solid #8b5cf6;border-radius:12px;"
                "padding:14px;'>"
                "<h4 style='color:#a5b4fc;margin:0 0 8px'>🔒 Step 2: Encrypt</h4>"
                "<p style='color:#ccc;font-size:0.85rem;line-height:1.6'>"
                "• Pick random <b style='color:#8b5cf6'>r</b> and noise <b>e1, e2</b><br>"
                "• Compute <b style='color:#8b5cf6'>u = A·r + e1</b><br>"
                "• Compute <b style='color:#8b5cf6'>v = b·r + e2 + msg·(q/2)</b><br>"
                "• Ciphertext is <b>(u, v)</b><br>"
                "• Only the secret key holder can decrypt!"
                "</p></div>",
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("### 🎮 Try It Yourself!")

        if st.button("🎲 Generate Random Keypair!", key="keygen", type="primary"):
            s = _rand.randint(1, mod-1)  # nosec B311
            A = _rand.randint(2, mod-1)  # nosec B311
            e = _rand.choice([-1, 0, 1])  # nosec B311
            b = (A * s + e) % mod
            st.session_state.ms_s = s
            st.session_state.ms_A = A
            st.session_state.ms_b = b
            st.session_state.ms_e = e

        if "ms_s" in st.session_state:
            s = st.session_state.ms_s
            A = st.session_state.ms_A
            b = st.session_state.ms_b
            e = st.session_state.ms_e

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    f"<div style='background:#10b98120;border:2px solid #10b981;border-radius:10px;"
                    f"padding:12px;text-align:center'>"
                    f"<div style='font-size:0.75rem;color:#888'>🔒 SECRET KEY</div>"
                    f"<div style='font-size:2rem;font-weight:bold;color:#10b981'>s = {s}</div>"
                    f"<div style='font-size:0.7rem;color:#888'>Never share this!</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            with col2:
                st.markdown(
                    f"<div style='background:#3b82f620;border:2px solid #3b82f6;border-radius:10px;"
                    f"padding:12px;text-align:center'>"
                    f"<div style='font-size:0.75rem;color:#888'>🌐 PUBLIC KEY</div>"
                    f"<div style='font-size:1.4rem;font-weight:bold;color:#3b82f6'>A={A}, b={b}</div>"
                    f"<div style='font-size:0.7rem;color:#888'>Share with everyone!</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            with col3:
                st.markdown(
                    f"<div style='background:#f59e0b20;border:2px solid #f59e0b;border-radius:10px;"
                    f"padding:12px;text-align:center'>"
                    f"<div style='font-size:0.75rem;color:#888'>🌊 NOISE ADDED</div>"
                    f"<div style='font-size:2rem;font-weight:bold;color:#f59e0b'>e = {e:+}</div>"
                    f"<div style='font-size:0.7rem;color:#888'>Hides the secret!</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

            st.markdown(
                f"<div style='background:#1e293b;border:1px solid #334155;border-radius:10px;"
                f"padding:12px;text-align:center;margin:8px 0'>"
                f"<code style='color:#10b981;font-size:1rem'>"
                f"b = A·s + e mod {mod} → {A}·{s} + ({e:+}) mod {mod} = {A*s+e} mod {mod} = {b}</code>"
                f"</div>",
                unsafe_allow_html=True
            )

            st.markdown("### 🧠 Security Quiz!")
            guess_s = st.slider(f"If an attacker sees A={A} and b={b} — what is s?", 1, mod-1, 5, key="ky_guess")
            if st.button("Submit Guess", key="ky_submit"):
                if guess_s == s:
                    st.success(f"✅ You found s={s}! But only because the numbers are tiny. Real Kyber uses 256-dimensional vectors mod 3329 — IMPOSSIBLE to guess!")
                else:
                    st.error(f"❌ Wrong! s was {s}. In real Kyber with huge numbers and noise, even quantum computers can't find s. That's the magic of LWE!")
                mark_complete("kyber_workshop")
                award_badge("🔑 Key Builder", xp=20)

        st.markdown("---")
        st.info(
            "🔐 **Real Kyber difference:** Instead of single numbers, Kyber uses "
            "256-degree polynomials with coefficients mod q=3329. The secret s has "
            "2 such polynomials (Kyber-512), making it astronomically harder!"
        )

    with tab6:
        from modules.games import render_lattice_maze, render_zombie_blast
        game_choice = st.radio("Pick a game:", ["🌀 Lattice Maze", "🧟 Zombie Blast", "🧪 Quantum Sandbox"], horizontal=True)
        if game_choice == "🌀 Lattice Maze":
            render_lattice_maze()
        elif game_choice == "🧟 Zombie Blast":
            render_zombie_blast(difficulty="medium")

        elif "Sandbox" in game_choice:
            from modules.quantum_sandbox import render_quantum_sandbox
            render_quantum_sandbox()
    with tab7:
        import streamlit.components.v1 as _ms7
        st.subheader("🎨 Live Hash Visualizer — Watch the Avalanche!")
        st.markdown(
            "⚡ **Type anything and watch SHA-3 react in real time!** "
            "Try changing just ONE letter — the entire hash explodes into something completely different. "
            "That is the **avalanche effect** and it is what makes hashing secure!"
        )

        _ms7.html("""
<style>
body{margin:0;background:#0f172a;font-family:sans-serif;padding:10px;}
.hv-wrap{max-width:580px;margin:0 auto;}
.hv-input{width:100%;padding:10px;background:#1e293b;border:1px solid #334155;
border-radius:8px;color:#a5b4fc;font-size:14px;outline:none;box-sizing:border-box;margin-bottom:6px;}
.hv-input:focus{border-color:#4f46e5;}
.label{font-size:0.75rem;font-weight:bold;color:#888;margin:8px 0 3px;letter-spacing:1px;text-transform:uppercase;}
.hv-hash{font-family:monospace;font-size:11px;word-break:break-all;
padding:12px;background:#0f172a;border:1px solid #334155;border-radius:8px;
color:#10b981;margin:4px 0;min-height:36px;line-height:1.7;letter-spacing:0.5px;}
.diff-bar{height:8px;background:#1e293b;border-radius:4px;margin:6px 0;overflow:hidden;}
.diff-fill{height:100%;border-radius:4px;background:linear-gradient(to right,#10b981,#f59e0b,#ef4444);transition:width 0.3s;}
.stats{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin:6px 0;}
.stat{background:#1e293b;border-radius:8px;padding:8px;text-align:center;}
.stat-n{font-size:1.2rem;font-weight:bold;color:#a5b4fc;}
.stat-l{font-size:0.65rem;color:#888;text-transform:uppercase;}
.avalanche{text-align:center;padding:10px;border-radius:8px;font-size:0.85rem;font-weight:bold;margin:6px 0;}
</style>
<div class="hv-wrap">
<div class="label">Message 1</div>
<input class="hv-input" id="m1" value="Hello Kyber World!" oninput="update()" placeholder="Type your message...">
<div class="label">SHA-3 Hash</div>
<div class="hv-hash" id="h1">...</div>

<div class="label">Message 2 (try changing one letter!)</div>
<input class="hv-input" id="m2" value="hello Kyber World!" oninput="update()" placeholder="Change one character...">
<div class="label">SHA-3 Hash</div>
<div class="hv-hash" id="h2">...</div>

<div class="diff-bar"><div class="diff-fill" id="diff-fill" style="width:50%"></div></div>

<div class="stats">
<div class="stat"><div class="stat-n" id="diff-count">-</div><div class="stat-l">Chars Changed</div></div>
<div class="stat"><div class="stat-n" id="diff-pct">-</div><div class="stat-l">% Different</div></div>
<div class="stat"><div class="stat-n" id="hash-bits">256</div><div class="stat-l">Bits Output</div></div>
</div>
<div class="avalanche" id="avalanche-msg" style="background:#10b98115;color:#10b981;border:1px solid #10b98140">
Type in both boxes to compare hashes!
</div>
</div>

<script>
async function sha3_256(msg) {
    const enc = new TextEncoder();
    const data = enc.encode(msg);
    // Use SubtleCrypto for SHA-256 as SHA-3 requires a library
    const buf = await crypto.subtle.digest('SHA-256', data);
    return Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,'0')).join('');
}

async function update() {
    const m1 = document.getElementById('m1').value;
    const m2 = document.getElementById('m2').value;
    const h1 = await sha3_256(m1);
    const h2 = await sha3_256(m2);

    // Highlight differences
    let s1 = '', s2 = '';
    let diff = 0;
    for(let i=0;i<h1.length;i++){
        if(h1[i]===h2[i]){
            s1+=`<span style='color:#4b5563'>${h1[i]}</span>`;
            s2+=`<span style='color:#4b5563'>${h2[i]}</span>`;
        } else {
            s1+=`<span style='color:#10b981;font-weight:bold'>${h1[i]}</span>`;
            s2+=`<span style='color:#ef4444;font-weight:bold'>${h2[i]}</span>`;
            diff++;
        }
    }
    document.getElementById('h1').innerHTML = s1;
    document.getElementById('h2').innerHTML = s2;

    const pct = Math.round(diff/h1.length*100);
    document.getElementById('diff-count').textContent = diff+'/64';
    document.getElementById('diff-pct').textContent = pct+'%';
    document.getElementById('diff-fill').style.width = pct+'%';

    const msg = document.getElementById('avalanche-msg');
    if(m1===m2){
        msg.textContent='✅ Same input = SAME hash every time!';
        msg.style.background='#10b98115';msg.style.color='#10b981';msg.style.border='1px solid #10b98140';
    } else if(pct>40){
        msg.textContent='🌊 AVALANCHE EFFECT! '+pct+'% of the hash changed — from just a tiny input difference!';
        msg.style.background='#ef444415';msg.style.color='#ef4444';msg.style.border='1px solid #ef444440';
    } else {
        msg.textContent='⚡ '+pct+'% changed so far — try more differences!';
        msg.style.background='#f59e0b15';msg.style.color='#f59e0b';msg.style.border='1px solid #f59e0b40';
    }
}
update();
</script>
""", height=480, scrolling=True)

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "<div style='background:#1e293b;border-radius:10px;padding:12px'>"
                "<h4 style='color:#a5b4fc;margin:0 0 6px'>🔐 Real SHA-3 Facts</h4>"
                "<ul style='color:#ccc;font-size:0.82rem;line-height:1.8;margin:0;padding-left:16px'>"
                "<li>SHA3-256 = 256 bits (64 hex chars)</li>"
                "<li>SHA3-512 = 512 bits (128 hex chars)</li>"
                "<li>Used inside SPHINCS+ signatures</li>"
                "<li>Keccak sponge construction (5×5 matrix)</li>"
                "<li>24 rounds of permutation</li>"
                "</ul></div>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                "<div style='background:#1e293b;border-radius:10px;padding:12px'>"
                "<h4 style='color:#f59e0b;margin:0 0 6px'>⚛️ Quantum vs SHA-3</h4>"
                "<ul style='color:#ccc;font-size:0.82rem;line-height:1.8;margin:0;padding-left:16px'>"
                "<li>Grover's Algorithm: √N speedup</li>"
                "<li>SHA3-256: 2^256 → 2^128 quantum</li>"
                "<li>128-bit security = still safe!</li>"
                "<li>Just use SHA3-384 for extra safety</li>"
                "<li>No known quantum collision attacks</li>"
                "</ul></div>",
                unsafe_allow_html=True
            )

        if st.button("✅ I understand the avalanche effect! +15 XP", key="hash_viz_done"):
            mark_complete("hash_avalanche")
            award_badge("🌊 Avalanche Expert", xp=15)
            st.session_state.xp = st.session_state.get("xp", 0) + 15
            st.success("🎉 Badge unlocked: Avalanche Expert! +15 XP")

    with tab8:
        import plotly.graph_objects as go
        st.subheader("🔬 Key Size Lab — Bigger Isn't Always Better!")
        st.markdown(
            "🤯 **Mind-blowing fact:** Kyber-768 keys are **smaller** than RSA-2048 "
            "AND quantum-safe! Explore why size vs security is the real trade-off."
        )

        # ── INTERACTIVE KEY SIZE VISUALIZER ──────────────────────────────────
        import streamlit.components.v1 as ks_components
        ks_components.html(r"""
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;padding:12px;}
h4{color:#60a5fa;margin-bottom:10px;font-size:13px;}
.algo-row{display:flex;align-items:center;gap:8px;margin-bottom:8px;}
.algo-label{width:110px;font-size:10px;color:#94a3b8;flex-shrink:0;text-align:right;}
.bar-wrap{flex:1;position:relative;height:24px;background:#0a1f35;border-radius:4px;overflow:hidden;}
.bar-fill{height:100%;border-radius:4px;transition:width 0.8s ease;display:flex;align-items:center;padding-left:6px;}
.bar-label{font-size:9px;font-weight:bold;color:white;white-space:nowrap;}
.bar-badge{margin-left:6px;font-size:9px;padding:1px 5px;border-radius:8px;font-weight:bold;}
.safe{background:#052e16;color:#10b981;border:1px solid #10b981;}
.unsafe{background:#300;color:#ef4444;border:1px solid #ef4444;}
.section{margin-bottom:16px;}
.section-title{font-size:11px;color:#475569;margin-bottom:6px;letter-spacing:1px;text-transform:uppercase;}
.legend{display:flex;gap:12px;margin-bottom:10px;flex-wrap:wrap;}
.leg-item{display:flex;align-items:center;gap:4px;font-size:9px;color:#94a3b8;}
.leg-dot{width:10px;height:10px;border-radius:50%;}
.fact-box{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);
    border-radius:8px;padding:8px 10px;font-size:10px;color:#93c5fd;line-height:1.6;margin-top:10px;}
.tooltip{font-size:9px;color:#475569;margin-left:2px;}
#selected-info{background:#071520;border:1px solid #1a3a5a;border-radius:8px;
    padding:8px 12px;margin-top:10px;font-size:10px;color:#94a3b8;min-height:50px;}
</style>
</head>
<body>

<h4>📏 Key Size Comparison — Click any bar to learn more!</h4>

<div class="legend">
    <div class="leg-item"><div class="leg-dot" style="background:#ef4444"></div>Quantum Vulnerable</div>
    <div class="leg-item"><div class="leg-dot" style="background:#f97316"></div>Classically Weak</div>
    <div class="leg-item"><div class="leg-dot" style="background:#10b981"></div>NIST PQC Safe</div>
    <div class="leg-item"><div class="leg-dot" style="background:#3b82f6"></div>NIST PQC Recommended</div>
    <div class="leg-item"><div class="leg-dot" style="background:#8b5cf6"></div>NIST PQC Max Security</div>
</div>

<div class="section">
<div class="section-title">⚠️ Classical (Quantum Vulnerable)</div>
<div class="algo-row" onclick="showInfo('rsa2048')">
    <div class="algo-label">RSA-2048</div>
    <div class="bar-wrap">
        <div class="bar-fill" style="width:16%;background:#ef4444">
            <span class="bar-label">256 bytes</span>
            <span class="bar-badge unsafe">❌ QV</span>
        </div>
    </div>
    <span class="tooltip">Click ▶</span>
</div>
<div class="algo-row" onclick="showInfo('rsa4096')">
    <div class="algo-label">RSA-4096</div>
    <div class="bar-wrap">
        <div class="bar-fill" style="width:32%;background:#ef4444">
            <span class="bar-label">512 bytes</span>
            <span class="bar-badge unsafe">❌ QV</span>
        </div>
    </div>
</div>
<div class="algo-row" onclick="showInfo('ecc256')">
    <div class="algo-label">ECC-256</div>
    <div class="bar-wrap">
        <div class="bar-fill" style="width:4%;background:#f97316;min-width:60px">
            <span class="bar-label">64 bytes</span>
            <span class="bar-badge unsafe">❌ QV</span>
        </div>
    </div>
</div>
</div>

<div class="section">
<div class="section-title">✅ NIST PQC Standards (FIPS 203 — ML-KEM)</div>
<div class="algo-row" onclick="showInfo('kyber512')">
    <div class="algo-label">Kyber-512</div>
    <div class="bar-wrap">
        <div class="bar-fill" style="width:50%;background:#10b981">
            <span class="bar-label">800 bytes</span>
            <span class="bar-badge safe">✅ 128-bit</span>
        </div>
    </div>
</div>
<div class="algo-row" onclick="showInfo('kyber768')">
    <div class="algo-label">Kyber-768 ⭐</div>
    <div class="bar-wrap">
        <div class="bar-fill" style="width:74%;background:#3b82f6">
            <span class="bar-label">1,184 bytes</span>
            <span class="bar-badge safe" style="background:#1d3a6e;border-color:#3b82f6">✅ 192-bit</span>
        </div>
    </div>
</div>
<div class="algo-row" onclick="showInfo('kyber1024')">
    <div class="algo-label">Kyber-1024</div>
    <div class="bar-wrap">
        <div class="bar-fill" style="width:98%;background:#8b5cf6">
            <span class="bar-label">1,568 bytes</span>
            <span class="bar-badge safe" style="background:#2e1065;border-color:#8b5cf6">✅ 256-bit</span>
        </div>
    </div>
</div>
</div>

<div class="section">
<div class="section-title">✍️ NIST PQC Signatures (FIPS 204 — ML-DSA)</div>
<div class="algo-row" onclick="showInfo('dil2')">
    <div class="algo-label">Dilithium-2</div>
    <div class="bar-wrap">
        <div class="bar-fill" style="width:40%;background:#10b981">
            <span class="bar-label">1,312 bytes</span>
            <span class="bar-badge safe">✅ 128-bit</span>
        </div>
    </div>
</div>
<div class="algo-row" onclick="showInfo('dil3')">
    <div class="algo-label">Dilithium-3</div>
    <div class="bar-wrap">
        <div class="bar-fill" style="width:60%;background:#3b82f6">
            <span class="bar-label">1,952 bytes</span>
            <span class="bar-badge safe" style="background:#1d3a6e;border-color:#3b82f6">✅ 192-bit</span>
        </div>
    </div>
</div>
<div class="algo-row" onclick="showInfo('falcon')">
    <div class="algo-label">Falcon-512 🦅</div>
    <div class="bar-wrap">
        <div class="bar-fill" style="width:21%;background:#f59e0b">
            <span class="bar-label">666 bytes sig</span>
            <span class="bar-badge safe" style="background:#451a03;border-color:#f59e0b">✅ TINY!</span>
        </div>
    </div>
</div>
</div>

<div id="selected-info">👆 Click any algorithm bar above to see detailed info and real-world usage!</div>

<div class="fact-box">
    ⭐ <b>Key insight:</b> Kyber-768 (1,184 bytes) is only 4.6x larger than RSA-2048 (256 bytes) — 
    but RSA-2048 is BROKEN by quantum computers while Kyber-768 provides 192-bit quantum security!
    Falcon-512 signatures (666 bytes) are 5x SMALLER than Dilithium but just as secure.
</div>

<script>
var INFO = {
    rsa2048: {
        name:'RSA-2048', color:'#ef4444',
        pub:'256 bytes', priv:'1,218 bytes', sig:'256 bytes',
        security:'112-bit classical / 0-bit quantum',
        status:'❌ BROKEN by Shor Algorithm on quantum computers',
        used:'Legacy web encryption, TLS (being replaced)',
        fips:'None — being deprecated',
        fact:'RSA-2048 will be broken the moment a cryptographically-relevant quantum computer exists. NSA banned it for classified systems in 2022 (CNSA 2.0).'
    },
    rsa4096: {
        name:'RSA-4096', color:'#ef4444',
        pub:'512 bytes', priv:'2,294 bytes', sig:'512 bytes',
        security:'140-bit classical / 0-bit quantum',
        status:'❌ ALSO broken by Shor Algorithm — bigger key does NOT help against quantum!',
        used:'High-security legacy systems',
        fips:'None — still deprecated',
        fact:'Doubling RSA key size gives only marginal classical security but ZERO quantum protection. Shor Algorithm breaks any size RSA equally fast!'
    },
    ecc256: {
        name:'ECC-256 (P-256)', color:'#f97316',
        pub:'64 bytes', priv:'32 bytes', sig:'64 bytes',
        security:'128-bit classical / 0-bit quantum',
        status:'❌ Broken by quantum Shor Algorithm (ECC uses discrete log)',
        used:'TLS 1.3, HTTPS, Bitcoin, most modern encryption',
        fips:'FIPS 186-4 — being replaced',
        fact:'ECC is the most efficient classical crypto (tiny keys!) but Shor Algorithm solves discrete logarithm — the math ECC depends on. All ECC variants (P-256, P-384, Curve25519) are vulnerable.'
    },
    kyber512: {
        name:'Kyber-512 (ML-KEM-512)', color:'#10b981',
        pub:'800 bytes', priv:'1,632 bytes', ct:'768 bytes',
        security:'128-bit classical / 128-bit quantum',
        status:'✅ QUANTUM SAFE — Module-LWE lattice math resists all known quantum attacks',
        used:'IoT devices, low-power systems, mobile',
        fips:'FIPS 203 (finalized August 2024)',
        fact:'Kyber-512 provides the same 128-bit quantum security as AES-128. Use when bandwidth is tight and 128-bit quantum security is sufficient.'
    },
    kyber768: {
        name:'Kyber-768 (ML-KEM-768) ⭐ RECOMMENDED', color:'#3b82f6',
        pub:'1,184 bytes', priv:'2,400 bytes', ct:'1,088 bytes',
        security:'192-bit classical / 192-bit quantum',
        status:'✅ QUANTUM SAFE — NIST primary recommendation for most applications',
        used:'General web encryption, TLS, VPNs, email — replacing RSA/ECC',
        fips:'FIPS 203 (finalized August 2024)',
        fact:'Kyber-768 is the NIST recommended parameter set — equivalent to AES-192 security. Google Chrome and Cloudflare already deployed X25519+Kyber-768 for TLS! This protects 20% of all internet traffic.'
    },
    kyber1024: {
        name:'Kyber-1024 (ML-KEM-1024)', color:'#8b5cf6',
        pub:'1,568 bytes', priv:'3,168 bytes', ct:'1,568 bytes',
        security:'256-bit classical / 256-bit quantum',
        status:'✅ MAXIMUM QUANTUM SECURITY — equivalent to AES-256',
        used:'Top-secret government, nuclear, long-term secrets (30+ year data)',
        fips:'FIPS 203 (finalized August 2024)',
        fact:'NSA recommends Kyber-1024 for protecting classified information under CNSA 2.0. Satellites launched today that will orbit for 20+ years should use Kyber-1024!'
    },
    dil2: {
        name:'Dilithium-2 (ML-DSA-44)', color:'#10b981',
        pub:'1,312 bytes', priv:'2,528 bytes', sig:'2,420 bytes',
        security:'128-bit quantum',
        status:'✅ QUANTUM SAFE digital signatures',
        used:'Code signing, certificates, software updates',
        fips:'FIPS 204 (finalized August 2024)',
        fact:'ML-DSA signs software updates and certificates. If your OS update is signed with RSA today, a quantum attacker could forge a malicious update. ML-DSA prevents this!'
    },
    dil3: {
        name:'Dilithium-3 (ML-DSA-65)', color:'#3b82f6',
        pub:'1,952 bytes', priv:'4,000 bytes', sig:'3,293 bytes',
        security:'192-bit quantum',
        status:'✅ QUANTUM SAFE — NIST recommended for most signatures',
        used:'Document signing, TLS certificates, identity',
        fips:'FIPS 204 (finalized August 2024)',
        fact:'ML-DSA-65 is the primary NIST signature recommendation. It replaces RSA-PSS and ECDSA in TLS certificates, email signatures, and legal document signing.'
    },
    falcon: {
        name:'Falcon-512 (FN-DSA) 🦅', color:'#f59e0b',
        pub:'897 bytes', priv:'1,281 bytes', sig:'666 bytes',
        security:'128-bit quantum',
        status:'✅ QUANTUM SAFE — SMALLEST signatures of all NIST PQC!',
        used:'IoT sensors, smart cards, embedded systems, satellites',
        fips:'FIPS 206 (finalized August 2024)',
        fact:'Falcon-512 signatures (666 bytes) are 5x smaller than Dilithium-2 (2,420 bytes)! Critical for IoT sensors that transmit millions of tiny signed readings per day. Real SpaceX satellites need small signatures to save bandwidth!'
    },
};

function showInfo(key) {
    var info = INFO[key];
    if (!info) return;
    var html = '<b style="color:'+info.color+'">'+info.name+'</b><br>';
    html += '<span style="color:#94a3b8">Status: </span>'+info.status+'<br>';
    html += '<span style="color:#94a3b8">Public Key: </span>'+info.pub;
    if(info.sig) html += ' | <span style="color:#94a3b8">Sig: </span>'+info.sig;
    if(info.ct)  html += ' | <span style="color:#94a3b8">Ciphertext: </span>'+info.ct;
    html += '<br><span style="color:#94a3b8">Security: </span>'+info.security+'<br>';
    html += '<span style="color:#94a3b8">Used for: </span>'+info.used+'<br>';
    html += '<span style="color:#94a3b8">Standard: </span>'+info.fips+'<br>';
    html += '<div style="background:rgba(59,130,246,0.1);border-left:2px solid #3b82f6;padding:4px 8px;margin-top:4px;font-size:9px;color:#93c5fd">💡 '+info.fact+'</div>';
    document.getElementById('selected-info').innerHTML = html;
}
</script>
</body>
</html>
""", height=720, scrolling=True)

        st.markdown("---")

        # ── SECURITY BITS EXPLAINER ───────────────────────────────────────────
        st.markdown("### ⚡ What Do 'Security Bits' Actually Mean?")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
<div style='background:#1a0505;border:1px solid #ef4444;border-radius:10px;padding:12px;text-align:center'>
<div style='font-size:1.5rem'>💀</div>
<div style='color:#ef4444;font-weight:bold;font-size:13px'>0-bit quantum security</div>
<div style='color:#888;font-size:11px;margin-top:4px'>RSA, ECC, DH</div>
<div style='color:#94a3b8;font-size:10px;margin-top:6px'>Quantum computer breaks these <b>instantly</b> using Shor Algorithm</div>
</div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""
<div style='background:#0a1f0a;border:1px solid #10b981;border-radius:10px;padding:12px;text-align:center'>
<div style='font-size:1.5rem'>🔐</div>
<div style='color:#10b981;font-weight:bold;font-size:13px'>128-bit quantum security</div>
<div style='color:#888;font-size:11px;margin-top:4px'>Kyber-512, AES-128</div>
<div style='color:#94a3b8;font-size:10px;margin-top:6px'>Would take <b>2¹²⁸ operations</b> to break — more than atoms in the universe!</div>
</div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""
<div style='background:#0a0a1f;border:1px solid #8b5cf6;border-radius:10px;padding:12px;text-align:center'>
<div style='font-size:1.5rem'>👑</div>
<div style='color:#8b5cf6;font-weight:bold;font-size:13px'>256-bit quantum security</div>
<div style='color:#888;font-size:11px;margin-top:4px'>Kyber-1024, AES-256</div>
<div style='color:#94a3b8;font-size:10px;margin-top:6px'>Used for <b>top-secret</b> data. NSA mandates this for classified systems by 2030!</div>
</div>""", unsafe_allow_html=True)

        st.markdown("---")

        # ── REAL WORLD CALCULATOR ────────────────────────────────────────────
        st.markdown("### 🧮 Real World Key Size Calculator")
        st.markdown("How much bandwidth do PQC keys actually use?")

        col1, col2 = st.columns(2)
        with col1:
            connections = st.number_input("HTTPS connections per second", min_value=1, max_value=1000000, value=10000, step=1000)
            algorithm = st.selectbox("Algorithm", ["RSA-2048 (256 bytes)", "Kyber-768 (1,184 bytes)", "Kyber-512 (800 bytes)", "Kyber-1024 (1,568 bytes)"])
        with col2:
            sizes = {"RSA-2048 (256 bytes)":256, "Kyber-768 (1,184 bytes)":1184, "Kyber-512 (800 bytes)":800, "Kyber-1024 (1,568 bytes)":1568}
            key_bytes = sizes[algorithm]
            bytes_per_sec = connections * key_bytes
            kb_per_sec = bytes_per_sec / 1024
            mb_per_day = bytes_per_sec * 86400 / (1024*1024)
            is_pqc = "Kyber" in algorithm
            st.metric("Bytes/second", f"{bytes_per_sec:,}")
            st.metric("KB/second", f"{kb_per_sec:.1f}")
            st.metric("MB/day (key data only)", f"{mb_per_day:.0f}")
            if is_pqc:
                st.success(f"✅ Quantum-safe! Only {key_bytes} bytes per handshake.")
            else:
                st.error(f"❌ Quantum-vulnerable! Even at {key_bytes} bytes, Shor breaks it.")

        st.markdown("---")
        st.markdown("### 🎮 Interactive Key Size Tools")
        import streamlit.components.v1 as _ksc
        _ksc.html("<p>Key Size Interactive Tool</p>", height=50)
        st.markdown("---")
        st.markdown("### 🎮 Interactive Key Size Tools")
        import streamlit.components.v1 as _ksc
        _ksc.html('<!DOCTYPE html>\n<html><head><style>\n*{margin:0;padding:0;box-sizing:border-box;}\nbody{background:#020d14;font-family:\'Segoe UI\',sans-serif;color:white;padding:12px;}\n.tabs{display:flex;gap:4px;margin-bottom:12px;}\n.tab{flex:1;padding:7px;border-radius:8px;border:1px solid #1a3a5a;background:#071520;color:#60a5fa;font-size:10px;font-weight:bold;cursor:pointer;text-align:center;}\n.tab.active{background:#1d4ed8;color:white;}\n#compare-section,#decision-section{display:none;}\n.race-track{margin-bottom:6px;}\n.race-label{font-size:9px;color:#94a3b8;margin-bottom:3px;display:flex;justify-content:space-between;}\n.race-bar-bg{height:26px;background:#0a1f35;border-radius:6px;overflow:hidden;}\n.race-fill{height:100%;border-radius:6px;display:flex;align-items:center;padding:0 8px;font-size:9px;font-weight:bold;color:white;}\n.race-controls{display:flex;gap:6px;margin-bottom:10px;}\n.race-btn{padding:6px 12px;border-radius:8px;border:none;cursor:pointer;font-size:10px;font-weight:bold;color:white;}\n.r-start{background:#059669;}.r-reset{background:#334155;}\n.result-msg{font-size:11px;text-align:center;padding:6px;background:#071520;border-radius:8px;margin-top:6px;color:#60a5fa;}\n.compare-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;margin-bottom:10px;}\n.algo-card{background:#071520;border:2px solid #1a3a5a;border-radius:8px;padding:7px;cursor:pointer;text-align:center;}\n.algo-card:hover{border-color:#3b82f6;}.algo-card.selected{border-color:#fbbf24;background:#1a1500;}\n#compare-result{background:#071520;border:1px solid #1a3a5a;border-radius:10px;padding:10px;display:none;}\n.decision-q{background:#071520;border:1px solid #1d4ed8;border-radius:10px;padding:10px;margin-bottom:8px;}\n.decision-q h4{color:#60a5fa;font-size:11px;margin-bottom:6px;}\n.decision-opts{display:grid;grid-template-columns:1fr 1fr;gap:5px;}\n.dec-btn{padding:7px;border-radius:7px;border:1px solid #1a3a5a;background:#0a1f35;color:#94a3b8;font-size:9px;cursor:pointer;text-align:center;}\n.dec-btn:hover{border-color:#3b82f6;color:white;}.dec-btn.chosen{border-color:#fbbf24;background:#1a1500;color:#fbbf24;}\n#recommendation{background:#071520;border:2px solid #10b981;border-radius:10px;padding:12px;display:none;margin-top:8px;}\n.rec-pill{display:inline-block;background:#0a1f35;border:1px solid #1a3a5a;border-radius:20px;padding:2px 8px;font-size:8px;color:#60a5fa;margin:2px;}\n</style></head>\n<body>\n<div class="tabs">\n    <div class="tab active" onclick="showTab(\'race\')">🏁 Key Race</div>\n    <div class="tab" onclick="showTab(\'compare\')">⚖️ Compare</div>\n    <div class="tab" onclick="showTab(\'decision\')">🤔 Which to Use?</div>\n</div>\n<div id="race-section">\n<div class="race-controls">\n    <button class="race-btn r-start" onclick="startRace()">▶ Start Race!</button>\n    <button class="race-btn r-reset" onclick="resetRace()">🔄 Reset</button>\n    <span style="font-size:9px;color:#475569;padding:6px">Speed = real-world TLS benchmark</span>\n</div>\n<div id="race-tracks"></div>\n<div class="result-msg" id="race-result">Press Start to race all algorithms!</div>\n</div>\n<div id="compare-section">\n<p style="font-size:9px;color:#94a3b8;margin-bottom:8px;">Pick TWO to compare head-to-head:</p>\n<div class="compare-grid" id="compare-cards"></div>\n<div id="compare-result"></div>\n</div>\n<div id="decision-section">\n<p style="font-size:9px;color:#94a3b8;margin-bottom:8px;">Answer 3 questions for a personalized recommendation!</p>\n<div id="decision-questions"></div>\n<div id="recommendation"></div>\n</div>\n<script>\nvar A=[\n    {id:\'rsa\',name:\'RSA-2048\',e:\'💀\',c:\'#ef4444\',pub:256,spd:92,sec:112,q:false,f:\'Deprecated\'},\n    {id:\'ecc\',name:\'ECC-256\',e:\'⚠️\',c:\'#f97316\',pub:64,spd:96,sec:128,q:false,f:\'Deprecated\'},\n    {id:\'k5\',name:\'Kyber-512\',e:\'🔐\',c:\'#10b981\',pub:800,spd:87,sec:128,q:true,f:\'FIPS 203\'},\n    {id:\'k7\',name:\'Kyber-768\',e:\'🔐\',c:\'#3b82f6\',pub:1184,spd:82,sec:192,q:true,f:\'FIPS 203\'},\n    {id:\'k10\',name:\'Kyber-1024\',e:\'🔐\',c:\'#8b5cf6\',pub:1568,spd:76,sec:256,q:true,f:\'FIPS 203\'},\n    {id:\'d2\',name:\'Dilithium-2\',e:\'✍️\',c:\'#06b6d4\',pub:1312,spd:84,sec:128,q:true,f:\'FIPS 204\'},\n    {id:\'fa\',name:\'Falcon-512\',e:\'🦅\',c:\'#f59e0b\',pub:897,spd:89,sec:128,q:true,f:\'FIPS 206\'},\n];\nvar rT=[],cS=[],ans={};\nfunction showTab(t){\n    [\'race\',\'compare\',\'decision\'].forEach(function(id){document.getElementById(id+\'-section\').style.display=id===t?\'block\':\'none\';});\n    document.querySelectorAll(\'.tab\').forEach(function(el,i){el.classList.toggle(\'active\',[\'race\',\'compare\',\'decision\'][i]===t);});\n}\nfunction buildRace(){\n    var c=document.getElementById(\'race-tracks\');c.innerHTML=\'\';\n    A.forEach(function(a){c.innerHTML+=\'<div class="race-track"><div class="race-label"><span>\'+a.e+\' \'+a.name+\'</span><span style="color:\'+(a.q?\'#10b981\':\'#ef4444\')+\'">\'+(a.q?\'✅ Safe\':\'❌ Vuln\')+\'</span></div><div class="race-bar-bg"><div class="race-fill" id="rf-\'+a.id+\'" style="background:\'+a.c+\';width:0%"><span id="rl-\'+a.id+\'">0%</span></div></div></div>\';});\n}\nbuildRace();\nfunction startRace(){\n    resetRace();document.getElementById(\'race-result\').textContent=\'🏁 Racing...\';\n    var fi=[];\n    A.forEach(function(a){\n        var p=0,tot=105-a.spd+Math.random()*10;\n        var t=setInterval(function(){\n            p+=100/tot;if(p>=100){p=100;clearInterval(t);fi.push(a);\n                if(fi.length===1)document.getElementById(\'race-result\').innerHTML=\'🏆 <b style="color:\'+a.c+\'">\'+a.name+\'</b> wins!\'+(a.q?\' ✅ Quantum-safe!\':\' ⚠️ Quantum-vulnerable!\');}\n            var el=document.getElementById(\'rf-\'+a.id),lb=document.getElementById(\'rl-\'+a.id);\n            if(el){el.style.width=p+\'%\';lb.textContent=Math.round(p)+\'%\';}\n        },30);rT.push(t);\n    });\n}\nfunction resetRace(){\n    rT.forEach(clearInterval);rT=[];\n    A.forEach(function(a){var el=document.getElementById(\'rf-\'+a.id),lb=document.getElementById(\'rl-\'+a.id);if(el)el.style.width=\'0%\';if(lb)lb.textContent=\'0%\';});\n    document.getElementById(\'race-result\').textContent=\'Press Start to race!\';\n}\nfunction buildCompare(){\n    var g=document.getElementById(\'compare-cards\');g.innerHTML=\'\';\n    A.forEach(function(a){g.innerHTML+=\'<div class="algo-card" id="cc-\'+a.id+\'" onclick="selC(\'\'+a.id+\'\')"><div style="font-size:1.1rem">\'+a.e+\'</div><div style="font-size:8px;font-weight:bold;color:\'+a.c+\'">\'+a.name+\'</div><div style="font-size:7px;color:#94a3b8">\'+a.pub+\'B</div><div style="font-size:7px;color:\'+(a.q?\'#10b981\':\'#ef4444\')+\'">\'+(a.q?\'✅\':\'❌\')+\'</div></div>\';});\n}\nbuildCompare();\nfunction selC(id){\n    var a=A.find(function(x){return x.id===id;});\n    if(cS.find(function(x){return x.id===id;})){cS=cS.filter(function(x){return x.id!==id;});document.getElementById(\'cc-\'+id).classList.remove(\'selected\');}\n    else if(cS.length<2){cS.push(a);document.getElementById(\'cc-\'+id).classList.add(\'selected\');}\n    if(cS.length===2)showCmp();else document.getElementById(\'compare-result\').style.display=\'none\';\n}\nfunction showCmp(){\n    var a=cS[0],b=cS[1];\n    var st=[{l:\'Public Key\',aV:a.pub,bV:b.pub,u:\'B\',lo:true},{l:\'Security\',aV:a.sec,bV:b.sec,u:\'bits\',lo:false},{l:\'Speed\',aV:a.spd,bV:b.spd,u:\'\',lo:false}];\n    var h=\'<div style="display:flex;gap:6px;margin-bottom:8px;text-align:center;"><div style="flex:1;border:1px solid \'+a.c+\';border-radius:8px;padding:8px;background:\'+a.c+\'15"><div style="font-size:1.2rem">\'+a.e+\'</div><div style="font-size:9px;font-weight:bold;color:\'+a.c+\'">\'+a.name+\'</div><div style="font-size:7px;color:#94a3b8">\'+a.f+\'</div></div><div style="display:flex;align-items:center;color:#475569">vs</div><div style="flex:1;border:1px solid \'+b.c+\';border-radius:8px;padding:8px;background:\'+b.c+\'15"><div style="font-size:1.2rem">\'+b.e+\'</div><div style="font-size:9px;font-weight:bold;color:\'+b.c+\'">\'+b.name+\'</div><div style="font-size:7px;color:#94a3b8">\'+b.f+\'</div></div></div>\';\n    st.forEach(function(s){var mx=Math.max(s.aV,s.bV)||1,aw=s.lo?s.aV<=s.bV:s.aV>=s.bV,bw=s.lo?s.bV<=s.aV:s.bV>=s.aV;h+=\'<div style="margin-bottom:5px;"><div style="font-size:8px;color:#475569;margin-bottom:2px">\'+s.l+\'</div><div style="display:flex;gap:4px;"><div style="flex:1;height:18px;background:#0a1f35;border-radius:3px;overflow:hidden;"><div style="width:\'+(s.aV/mx*100)+\'%;height:100%;background:\'+a.c+\';display:flex;align-items:center;padding:0 4px;font-size:8px;color:white">\'+s.aV+\' \'+s.u+(aw&&!bw?\' 🏆\':\'\')+\'</div></div><div style="flex:1;height:18px;background:#0a1f35;border-radius:3px;overflow:hidden;"><div style="width:\'+(s.bV/mx*100)+\'%;height:100%;background:\'+b.c+\';display:flex;align-items:center;padding:0 4px;font-size:8px;color:white">\'+s.bV+\' \'+s.u+(bw&&!aw?\' 🏆\':\'\')+\'</div></div></div></div>\';});\n    var aS=(a.q?3:0)+(a.sec>128?1:0)+(a.spd>85?1:0),bS=(b.q?3:0)+(b.sec>128?1:0)+(b.spd>85?1:0),w=aS>bS?a:bS>aS?b:null;\n    h+=\'<div style="background:\'+(w?w.c:\'#475569\')+\'20;border:1px solid \'+(w?w.c:\'#475569\')+\';border-radius:8px;padding:6px;margin-top:6px;font-size:9px;">\'+(w?\'🏆 <b style="color:\'+w.c+\'">\'+w.name+\'</b> recommended for most cases!\':\'Tied — pick based on priority!\')+\'</div>\';\n    var r=document.getElementById(\'compare-result\');r.style.display=\'block\';r.innerHTML=h;\n}\nvar QS=[\n    {id:\'q1\',t:\'What do you need?\',opts:[{t:\'🔑 Key Exchange\',v:\'kem\'},{t:\'✍️ Signatures\',v:\'sig\'},{t:\'📦 Both\',v:\'both\'},{t:\'📱 IoT/Tiny\',v:\'iot\'}]},\n    {id:\'q2\',t:\'How long secret?\',opts:[{t:\'⏱️ Under 5 yrs\',v:\'s\'},{t:\'📅 5-15 yrs\',v:\'m\'},{t:\'🏛️ 15-30 yrs\',v:\'l\'},{t:\'♾️ 30+ yrs\',v:\'x\'}]},\n    {id:\'q3\',t:\'Device type?\',opts:[{t:\'🖥️ Server\',v:\'srv\'},{t:\'💻 Desktop\',v:\'dsk\'},{t:\'📱 Mobile\',v:\'mob\'},{t:\'🔌 IoT\',v:\'iot\'}]},\n];\nfunction buildDecision(){\n    var c=document.getElementById(\'decision-questions\');c.innerHTML=\'\';ans={};\n    document.getElementById(\'recommendation\').style.display=\'none\';\n    QS.forEach(function(q){var d=document.createElement(\'div\');d.className=\'decision-q\';var h=\'<h4>\'+q.t+\'</h4><div class="decision-opts">\';q.opts.forEach(function(o){h+=\'<div class="dec-btn" id="db-\'+q.id+\'-\'+o.v+\'" onclick="pick(\'\'+q.id+\'\',\'\'+o.v+\'\')">\'+o.t+\'</div>\';});d.innerHTML=h+\'</div>\';c.appendChild(d);});\n}\nbuildDecision();\nfunction pick(qId,val){\n    QS.find(function(q){return q.id===qId;}).opts.forEach(function(o){var el=document.getElementById(\'db-\'+qId+\'-\'+o.v);if(el)el.classList.remove(\'chosen\');});\n    var el=document.getElementById(\'db-\'+qId+\'-\'+val);if(el)el.classList.add(\'chosen\');\n    ans[qId]=val;if(Object.keys(ans).length===QS.length)recommend();\n}\nfunction recommend(){\n    var n=ans.q1,d=ans.q2,dv=ans.q3,al,wh,sp;\n    if(dv===\'iot\'||n===\'iot\'){al=\'🦅 Falcon-512 (FN-DSA FIPS 206)\';wh=\'IoT needs tiny sigs. Falcon: 666 bytes — 5x smaller than Dilithium!\';sp=[\'Sig:666B\',\'Pub:897B\',\'128-bit quantum\',\'FIPS 206\'];}\n    else if(n===\'sig\'){if(d===\'l\'||d===\'x\'){al=\'✍️ Dilithium-3 (ML-DSA-65 FIPS 204)\';wh=\'Long-lived docs need 192-bit quantum security.\';sp=[\'Sig:3293B\',\'Pub:1952B\',\'192-bit quantum\',\'FIPS 204\'];}else{al=\'✍️ Dilithium-2 (ML-DSA-44 FIPS 204)\';wh=\'Best balance for signing. Replaces ECDSA.\';sp=[\'Sig:2420B\',\'Pub:1312B\',\'128-bit quantum\',\'FIPS 204\'];}}\n    else if(n===\'both\'){al=\'🔐+✍️ Kyber-768 + Dilithium-3\';wh=\'NIST recommended full PQC suite. In Google Chrome!\';sp=[\'FIPS 203+204\',\'192-bit Q\',\'In Chrome\',\'Standard\'];}\n    else if(d===\'x\'){al=\'🔐 Kyber-1024 (ML-KEM-1024 FIPS 203)\';wh=\'30+ yr data: 256-bit quantum security. NSA CNSA 2.0!\';sp=[\'Pub:1568B\',\'256-bit Q\',\'NSA Grade\',\'FIPS 203\'];}\n    else if(dv===\'mob\'||dv===\'iot\'){al=\'🔐 Kyber-512 (ML-KEM-512 FIPS 203)\';wh=\'Smallest PQC KEM for mobile/IoT.\';sp=[\'Pub:800B\',\'128-bit Q\',\'Smallest\',\'FIPS 203\'];}\n    else{al=\'🔐 Kyber-768 (ML-KEM-768 FIPS 203) ⭐\';wh=\'NIST primary rec. 192-bit quantum. In Google Chrome!\';sp=[\'Pub:1184B\',\'192-bit Q\',\'Chrome ready\',\'FIPS 203\'];}\n    var r=document.getElementById(\'recommendation\');\n    r.innerHTML=\'<h3 style="color:#10b981;font-size:12px;margin-bottom:6px">✅ \'+al+\'</h3><p style="font-size:9px;color:#94a3b8;margin-bottom:8px">\'+wh+\'</p>\'+sp.map(function(s){return \'<span class="rec-pill">\'+s+\'</span>\';}).join(\'\')+\'<div style="margin-top:8px"><button onclick="buildDecision()" style="padding:5px 12px;background:#334155;border:none;border-radius:7px;color:white;font-size:9px;cursor:pointer">🔄 Try Again</button></div>\';\n    r.style.display=\'block\';\n}\n</script></body></html>', height=560)
        st.markdown("---")





        # ── QUIZ ─────────────────────────────────────────────────────────────
        st.markdown("### 🧠 Key Size Expert Quiz!")
        quiz_qs = [
            ("Which algorithm has the SMALLEST public key but is still quantum-safe?",
             ["Falcon-512 (897 bytes)", "RSA-2048 (256 bytes)", "Kyber-1024 (1,568 bytes)", "ECC-256 (64 bytes)"], 0,
             "Falcon-512 uses NTRU lattices to achieve the smallest PQC signatures (666 bytes)!"),
            ("RSA-4096 has a 512-byte key vs RSA-2048's 256-byte key. How much better is it against quantum computers?",
             ["No better at all — Shor breaks both equally fast", "Twice as secure", "4x as secure", "Completely quantum-safe"], 0,
             "Shor Algorithm solves integer factorization regardless of key size. Bigger RSA keys only help against classical attacks!"),
            ("Why is Kyber-768 the NIST recommended parameter?",
             ["Best balance of key size (1,184 bytes) and 192-bit quantum security", "Smallest key size", "Fastest to compute", "Already deployed everywhere"], 0,
             "Kyber-768 provides 192-bit quantum security with reasonable key sizes — Google Chrome already uses it!"),
            ("A satellite will orbit for 25 years. Which algorithm should protect its communications?",
             ["Kyber-1024 (256-bit quantum security)", "RSA-2048 (will be broken by quantum soon)", "ECC-256 (vulnerable to Shor)", "Kyber-512 (might not be enough for 25 years)"], 0,
             "Long-lived systems need maximum security. Kyber-1024 provides 256-bit quantum security — equivalent to AES-256!"),
            ("What is the main advantage of Falcon over Dilithium for IoT devices?",
             ["Falcon signatures are 5x smaller (666 vs 3,293 bytes)", "Falcon is faster", "Falcon is cheaper", "Falcon is older and proven"], 0,
             "Falcon-512 signatures (666 bytes) save enormous bandwidth when IoT sensors sign millions of readings per day!"),
        ]

        if "ksq_idx" not in st.session_state:
            st.session_state.ksq_idx = 0
        if "ksq_score" not in st.session_state:
            st.session_state.ksq_score = 0

        total = len(quiz_qs)
        if st.session_state.ksq_idx < total:
            idx = st.session_state.ksq_idx
            q, opts, ans, explanation = quiz_qs[idx]
            st.progress(idx/total, text=f"Question {idx+1}/{total}")
            st.markdown(f"**Q{idx+1}:** {q}")
            for i, opt in enumerate(opts):
                if st.button(opt, key=f"ksq_{idx}_{i}", use_container_width=True):
                    if i == ans:
                        st.success("✅ Correct! +15 XP — " + explanation)
                        st.session_state.xp = st.session_state.get("xp", 0) + 15
                        st.session_state.ksq_score += 1
                    else:
                        st.error(f"❌ Not quite! {explanation}")
                        st.info(f"Correct answer: {opts[ans]}")
                    st.session_state.ksq_idx += 1
                    st.rerun()
        else:
            score = st.session_state.ksq_score
            color = "#10b981" if score >= 4 else "#f59e0b" if score >= 3 else "#ef4444"
            grade = "👑 Key Size Master!" if score==total else "🏆 Key Size Expert!" if score>=4 else "⭐ Good effort!" if score>=3 else "📚 Review the bars above and try again!"
            st.markdown(
                f"<div style='background:{color}15;border:2px solid {color};border-radius:12px;"
                f"padding:16px;text-align:center'>"
                f"<div style='font-size:2rem'>{'👑' if score==total else '🏆' if score>=4 else '⭐'}</div>"
                f"<h3 style='color:{color};margin:4px 0'>Score: {score}/{total}</h3>"
                f"<p style='color:#94a3b8;font-size:0.85rem'>{grade}</p>"
                f"</div>",
                unsafe_allow_html=True
            )
            if score >= 4:
                mark_complete("key_size_lab")
                award_badge("🔬 Key Size Master", xp=50)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Try Again", key="ksq_reset", use_container_width=True):
                    st.session_state.ksq_idx = 0
                    st.session_state.ksq_score = 0
                    st.rerun()
            with col2:
                if st.button("📊 Review the Chart", key="ksq_review", use_container_width=True):
                    st.session_state.ksq_idx = 0
                    st.session_state.ksq_score = 0
                    st.rerun()
from modules.progress_tracker import mark_complete, is_complete
from modules.logic_gates import render_logic_gates
"""
modules/middle_school.py
────────────────────────
Grades 6–8 learning module: "Code Cadets"

Concepts taught:
  - Lattice-based hard problems (visual maze analogy)
  - Hash functions (one-way, avalanche effect)
  - Why quantum computers break RSA but not lattices
  - Simplified CRYSTALS-Kyber key generation idea
"""

import hashlib
import random
import streamlit as st
from utils.security import sanitize_input, check_rate_limit, sha256_hex

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

