from modules.progress_tracker import mark_complete, is_complete
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

def render_middle_school():
    st.title("🟡 Code Cadets — Middle School Edition")
    st.markdown(
        "Welcome, Cadet! You're now ready to dig into the real math behind "
        "post-quantum cryptography. Let's go! 🚀"
    )

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
        ["📖 Story Time", "🏗️ Lattice Explorer", "🏭 Hash Factory", "⚡ Quantum Race", "🔑 Key Workshop", "🌀 Mini Game", "🎨 Hash Visualizer", "🔬 Key Size Lab"]
    )

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
                    from modules.elementary import award_badge
                    award_badge("📖 Code Cadet Story", xp=10)

    with tab2:
        st.subheader("🏗️ Lattice Maze Explorer")
        st.markdown(
            """
            A **lattice** is a regular grid of points in space.
            The hard problem: given a messy point near the grid, find the CLOSEST grid point.
            Sounds easy? Try it with hundreds of dimensions — even quantum computers sweat! 😅

            **The Learning Problem (LWE)** — the math behind CRYSTALS-Kyber:
            - Pick a secret number `s`
            - Add intentional "noise" (small random errors) to equations about `s`
            - An attacker has to find `s` — nearly impossible with lattice noise!
            """
        )

# ── Live Lattice Visualizer ───────────────────────────────────────
        import plotly.graph_objects as go
        import numpy as np

        grid_range = range(-5, 6)
        x_points = [x for x in grid_range for _ in grid_range]
        y_points = [y for _ in grid_range for y in grid_range]

        if "target_x" not in st.session_state:
            st.session_state.target_x = round(random.uniform(-4, 4), 2)
            st.session_state.target_y = round(random.uniform(-4, 4), 2)

        tx = st.session_state.target_x
        ty = st.session_state.target_y
        closest_x = round(tx)
        closest_y = round(ty)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_points, y=y_points,
            mode="markers",
            marker=dict(size=8, color="#4f46e5"),
            name="Lattice points"
        ))
        fig.add_trace(go.Scatter(
            x=[tx], y=[ty],
            mode="markers",
            marker=dict(size=14, color="#ef4444", symbol="star"),
            name="Mystery point"
        ))
        fig.add_trace(go.Scatter(
            x=[closest_x], y=[closest_y],
            mode="markers",
            marker=dict(size=14, color="#10b981", symbol="circle"),
            name="Closest lattice point"
        ))
        fig.add_trace(go.Scatter(
            x=[tx, closest_x], y=[ty, closest_y],
            mode="lines",
            line=dict(color="#f59e0b", width=2, dash="dash"),
            name="Distance"
        ))
        fig.update_layout(
            height=400,
            showlegend=True,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            margin=dict(l=20, r=20, t=20, b=20),
        )

        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            f"⭐ Mystery point: ({tx}, {ty}) — "
            f"Closest lattice point: ({closest_x}, {closest_y})"
        )
        if st.button("🎲 New mystery point", key="new_target"):
            st.session_state.target_x = round(random.uniform(-4, 4), 2)
            st.session_state.target_y = round(random.uniform(-4, 4), 2)
            st.rerun()

        st.markdown("### 🎮 Mini Lattice Challenge")

        st.markdown("### 🎮 Mini Lattice Challenge")
        st.markdown(
            "The secret vector is hidden by noise. "
            "Can you guess what **s** is from these noisy equations?"
        )

        if "lattice_s" not in st.session_state:
            st.session_state.lattice_s = random.randint(2, 9)
            st.session_state.lattice_attempts = 0

        s = st.session_state.lattice_s
        # Generate 3 noisy equations:  a*s + e ≡ b (mod 11)
        mod = 11
        equations = []
        for _ in range(3):
            a = random.randint(1, 10)
            e = random.choice([-1, 0, 1])          # small noise
            b = (a * s + e) % mod
            equations.append((a, b))

        for i, (a, b) in enumerate(equations):
            st.code(f"Equation {i+1}: {a} × s + (small noise) ≡ {b}  (mod {mod})")

        guess = st.number_input("Your guess for s:", min_value=0, max_value=10, step=1, key="lattice_guess")
        if st.button("🔍 Check my guess", key="lattice_check"):
            if not check_rate_limit("lattice_check", st.session_state):
                st.warning("Hold on, Cadet! Try again in a moment.")
            else:
                st.session_state.lattice_attempts += 1
                if int(guess) == s:
                    st.success(f"✅ Correct! s = {s}. Imagine this with 1000 variables — impossible to guess!")
                    mark_complete("lattice_challenge")
                    award_badge("🏗️ Lattice Navigator", xp=20)
                    st.session_state.lattice_s = random.randint(2, 9)
                else:
                    st.error(
                        f"❌ Not quite! You've tried {st.session_state.lattice_attempts} time(s). "
                        "The noise makes it tricky, right? That's the whole point!"
                    )

    # ── Tab 3: Hash Factory ───────────────────────────────────────────────────
    with tab3:
        st.subheader("🏭 Hash Function Factory")
        st.markdown(
            """
            A **hash function** takes ANY input and produces a fixed-size fingerprint.
            It's a **one-way** function — you can't reverse it.
            PQC schemes rely on hashes like **SHA-3** internally.

            Key properties:
            - Same input → ALWAYS same output
            - Change one letter → completely different output (**avalanche effect** 🌊)
            - Can't reverse the hash to get the original input
            """
        )

        user_msg = st.text_input(
            "Type a message to hash:",
            value="Hello Quantum World",
            max_chars=200,
            key="hash_input",
        )
        clean_msg = sanitize_input(user_msg)

        algo = st.radio("Pick a hash algorithm:", ["SHA-256", "SHA3-256", "SHA-512"], horizontal=True)

        hash_map = {
            "SHA-256": hashlib.sha256,
            "SHA3-256": hashlib.sha3_256,
            "SHA-512": hashlib.sha512,
        }
        digest = hash_map[algo](clean_msg.encode()).hexdigest()

        st.markdown("### 🔢 Hash Output")
        st.code(digest, language="text")
        st.caption(f"Input length: {len(clean_msg)} chars → Output: always {len(digest)} hex chars")

        # Avalanche effect demo
        st.markdown("### 🌊 Avalanche Effect")
        st.markdown("Change just ONE character and watch the hash completely change:")
        if clean_msg:
            tweaked = clean_msg[:-1] + ("X" if clean_msg[-1] != "X" else "Y")
            tweaked_digest = hash_map[algo](tweaked.encode()).hexdigest()
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Original:** `{clean_msg[:30]}...`")
                st.code(digest[:32] + "...", language="text")
            with col2:
                st.markdown(f"**Tweaked:** `{tweaked[:30]}...`")
                st.code(tweaked_digest[:32] + "...", language="text")
            diff = sum(a != b for a, b in zip(digest, tweaked_digest))
            st.metric("Hex characters different", f"{diff} / {len(digest)}", delta=f"{diff/len(digest)*100:.0f}%")

        if st.button("🏭 I understand hash functions!", key="hash_done"):
            award_badge("🏭 Hash Factory Worker", xp=15)

    # ── Tab 4: Quantum vs Classical Race ─────────────────────────────────────
    with tab4:
        st.subheader("⚡ Quantum Computer vs Classical Computer — Head to Head!")
        st.markdown(
            """
            Quantum computers use **qubits** that can be 0 AND 1 at the same time (superposition).
            This gives them superpowers on SOME problems — but not all!
            """
        )

        problems = {
            "Factor a 2048-bit number (RSA)": ("🐢 Classical: millions of years", "⚡ Quantum: hours! (Shor's Algorithm)"),
            "Find a shortest lattice vector (Kyber)": ("🐢 Classical: still hard", "🐢 Quantum: still hard! 🎉"),
            "Search an unsorted database": ("🐢 Classical: check every item", "⚡ Quantum: √N steps (Grover's Algorithm)"),
            "Hash collision (SHA-3)": ("🐢 Classical: 2^128 tries", "⚡ Quantum: 2^64 tries — but still huge!"),
        }

        chosen = st.selectbox("Pick a problem:", list(problems.keys()))
        classical, quantum = problems[chosen]
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"🖥️ **Classical Computer**\n\n{classical}")
        with col2:
            if "Quantum: still hard" in quantum:
                st.success(f"⚛️ **Quantum Computer**\n\n{quantum}")
            else:
                st.error(f"⚛️ **Quantum Computer**\n\n{quantum}")

        if st.button("⚡ Got it — I understand the threat!", key="race_done"):
            award_badge("⚡ Quantum Racer", xp=20)

    # ── Tab 5: Key Workshop ───────────────────────────────────────────────────
    with tab5:
        st.subheader("🔑 Build-a-Key Workshop (Simplified Kyber)")
        st.markdown(
            """
            CRYSTALS-Kyber generates keys using lattice math.
            Here's a VERY simplified version to see the idea:

            1. **Key Generation:** Pick a secret `s`, a public matrix `A`, and small noise `e`
            2. **Public Key:** `b = A·s + e` (shared with everyone)
            3. **Encryption:** Combine message with public key and more noise
            4. **Decryption:** Use secret `s` to cancel the noise and recover the message
            """
        )

        mod = 17  # tiny prime for demo
        if st.button("🎲 Generate new keys", key="keygen"):
            s = random.randint(1, mod - 1)
            A = random.randint(2, mod - 1)
            e = random.choice([-1, 0, 1])
            b = (A * s + e) % mod
            st.session_state.kyber_keys = {"s": s, "A": A, "e": e, "b": b, "mod": mod}

        if "kyber_keys" in st.session_state:
            k = st.session_state.kyber_keys
            st.markdown("### 🔓 Your Keys (mod {mod})".format(**k))
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"🔑 **Secret Key:** s = {k['s']}")
                st.caption("(Only YOU know this!)")
            with col2:
                st.info(f"📢 **Public Key:** A={k['A']}, b={k['b']}")
                st.caption("(Safe to share)")

            st.markdown(f"*The noise was e = {k['e']} — hidden inside b, making it hard to reverse!*")
            st.markdown(
                f"Verify: {k['A']} × {k['s']} + {k['e']} = "
                f"{k['A'] * k['s'] + k['e']} ≡ **{k['b']}** (mod {mod}) ✅"
            )
            award_badge("🔑 Key Crafter", xp=25)

    with tab6:
        from modules.games import render_lattice_maze, render_zombie_blast, render_quantumcraft_middle
        game_choice = st.radio("Pick a game:", ["🌀 Lattice Maze", "🧟 Zombie Blast", "⛏️ QuantumCraft Mines"], horizontal=True)
        if game_choice == "🌀 Lattice Maze":
            render_lattice_maze()
        elif game_choice == "🧟 Zombie Blast":
            render_zombie_blast(difficulty="medium")
        else:
            render_quantumcraft_middle()
    with tab7:
        st.subheader("🎨 Live Hash Visualizer")
        st.markdown(
            "Type any message below and watch the **SHA-3 hash change in real time**! "
            "Change even one letter and the entire hash changes completely — "
            "that is the **avalanche effect**!"
        )
        import streamlit.components.v1 as components_ms
        components_ms.html("""
<style>
.hv-wrap{font-family:sans-serif;padding:12px;max-width:600px;margin:0 auto;}
.hv-input{width:100%;padding:10px;background:#1e293b;border:1px solid #334155;
border-radius:8px;color:#a5b4fc;font-size:14px;outline:none;box-sizing:border-box;}
.hv-hash{font-family:monospace;font-size:11px;word-break:break-all;
padding:12px;background:#0f172a;border:1px solid #334155;border-radius:8px;
color:#10b981;margin:8px 0;min-height:40px;line-height:1.6;}
.hv-label{font-size:12px;color:#888;margin:6px 0 3px;}
.hv-diff{font-size:12px;color:#f59e0b;margin:6px 0;}
.hv-algo{display:flex;gap:8px;margin:8px 0;}
.algo-btn{padding:5px 12px;border-radius:6px;border:none;cursor:pointer;
font-size:11px;font-weight:bold;background:#1e293b;color:#a5b4fc;
border:1px solid #334155;}
.algo-btn.active{background:#4f46e5;color:white;border-color:#4f46e5;}
</style>
<div class="hv-wrap">
    <div class="hv-algo">
        <button class="algo-btn active" onclick="setAlgo('SHA-256')">SHA-256</button>
        <button class="algo-btn" onclick="setAlgo('SHA-512')">SHA-512</button>
    </div>
    <div class="hv-label">Type your message:</div>
    <input class="hv-input" id="msg1" placeholder="Type anything here..." oninput="updateHash()">
    <div class="hv-label">Hash output:</div>
    <div class="hv-hash" id="hash1">Your hash will appear here...</div>
    <div class="hv-label">Try a slightly different message:</div>
    <input class="hv-input" id="msg2" placeholder="Change one letter..." oninput="updateHash()">
    <div class="hv-label">Hash output:</div>
    <div class="hv-hash" id="hash2">Your hash will appear here...</div>
    <div class="hv-diff" id="diff-msg"></div>
</div>
<script>
let currentAlgo = 'SHA-256';

function setAlgo(algo) {
    currentAlgo = algo;
    document.querySelectorAll('.algo-btn').forEach(b => {
        b.className = 'algo-btn' + (b.textContent === algo ? ' active' : '');
    });
    updateHash();
}

async function hashMessage(message) {
    if (!message) return '';
    const encoder = new TextEncoder();
    const data = encoder.encode(message);
    const algoMap = {'SHA-256': 'SHA-256', 'SHA-512': 'SHA-512'};
    const hashBuffer = await crypto.subtle.digest(algoMap[currentAlgo], data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

async function updateHash() {
    const msg1 = document.getElementById('msg1').value;
    const msg2 = document.getElementById('msg2').value;
    const h1 = await hashMessage(msg1);
    const h2 = await hashMessage(msg2);
    document.getElementById('hash1').textContent = h1 || 'Your hash will appear here...';
    document.getElementById('hash2').textContent = h2 || 'Your hash will appear here...';
    if (h1 && h2) {
        let diff = 0;
        for (let i = 0; i < Math.max(h1.length, h2.length); i++) {
            if (h1[i] !== h2[i]) diff++;
        }
        const pct = Math.round(diff / h1.length * 100);
        document.getElementById('diff-msg').textContent =
            diff === 0 ? '✅ Identical messages — identical hashes!' :
            '🌊 Avalanche effect! ' + diff + ' of ' + h1.length + ' characters changed (' + pct + '%) — from just one letter difference!';
    } else {
        document.getElementById('diff-msg').textContent = '';
    }
}
</script>
""", height=480)

    with tab8:
        st.subheader("🔬 Key Size Lab — How Big Are Crypto Keys?")
        st.markdown(
            "A **key** is like a password that locks your secret messages. "
            "Crypto keys are HUGE compared to regular passwords! "
            "Let us explore how big they are and which ones are quantum-safe."
        )
        st.markdown("---")
        st.markdown("### What Even Is a Crypto Key?")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("Your house key\n\nAbout 5cm long\nVery simple\nEasy to copy!")
        with col2:
            st.warning("RSA key\n\nMade of 2048 ones and zeros\nClassical computers cannot crack it\nBut quantum computers can!")
        with col3:
            st.success("Kyber key\n\nSmaller than RSA\nBased on lattice math\nEven quantum computers cannot crack it!")
        st.markdown("---")
        st.markdown("### Pick an Algorithm to Learn About It!")

        ALGOS = [
            {"name":"RSA-2048",    "type":"Classical",    "safe":False, "key_kb":256, "emoji":"💀", "color":"#ef4444", "nist":"No standard",
             "analogy":"Like a lock with 2048 tumblers. Classical computers cannot pick it. But a quantum computer using Shor Algorithm cracks it in hours!",
             "fact":"RSA was invented in 1977 and has protected the internet for 45 years. But quantum computers will break it.",
             "size":"256 KB — about the size of a small photo"},
            {"name":"RSA-4096",    "type":"Classical",    "safe":False, "key_kb":512, "emoji":"💀", "color":"#ef4444", "nist":"No standard",
             "analogy":"Double the tumblers of RSA-2048. Still cracked by quantum computers just takes a bit longer!",
             "fact":"Some people use RSA-4096 thinking it is safer. Against quantum computers bigger RSA keys just delay the inevitable.",
             "size":"512 KB — twice as big but still quantum-vulnerable"},
            {"name":"ECC-256",     "type":"Classical",    "safe":False, "key_kb":64,  "emoji":"⚠️", "color":"#f97316", "nist":"No PQC standard",
             "analogy":"ECC uses elliptic curves — fancy math that makes smaller keys than RSA. But Shor Algorithm breaks elliptic curves too!",
             "fact":"Your phone uses ECC right now for HTTPS connections. All of it becomes vulnerable to quantum computers.",
             "size":"64 KB — much smaller than RSA but still quantum-vulnerable"},
            {"name":"Kyber-512",   "type":"Post-Quantum", "safe":True,  "key_kb":0.8, "emoji":"🔐", "color":"#10b981", "nist":"FIPS 203 ML-KEM",
             "analogy":"Uses lattice math — finding the closest point in a 256-dimensional grid with noise added. Quantum computers cannot solve this!",
             "fact":"Kyber was selected by NIST in 2022 after 6 years of global competition beating 69 other algorithms. Now it is FIPS 203.",
             "size":"800 bytes — smaller than most profile pictures!"},
            {"name":"Kyber-768",   "type":"Post-Quantum", "safe":True,  "key_kb":1.2, "emoji":"🔐", "color":"#10b981", "nist":"FIPS 203 ML-KEM",
             "analogy":"Stronger version of Kyber-512. Uses a larger lattice grid making it even harder to crack. Recommended for most uses!",
             "fact":"Kyber-768 gives 192-bit security. A quantum computer would need 2^192 operations to crack it. The universe is only 2^60 seconds old!",
             "size":"1.2 KB — still tiny! Fits in a text message"},
            {"name":"Dilithium-2", "type":"Post-Quantum", "safe":True,  "key_kb":1.3, "emoji":"✍️", "color":"#3b82f6", "nist":"FIPS 204 ML-DSA",
             "analogy":"Dilithium creates digital signatures — like a wax seal on a royal letter. It proves a message really came from you. Quantum-safe!",
             "fact":"Dilithium is named after a crystal from Star Trek! It was chosen by NIST for signing documents and software updates.",
             "size":"1.3 KB — about the size of a short text message"},
            {"name":"Falcon-512",  "type":"Post-Quantum", "safe":True,  "key_kb":0.9, "emoji":"🦅", "color":"#8b5cf6", "nist":"FIPS 206 FN-DSA",
             "analogy":"Falcon makes the SMALLEST quantum-safe signatures! It uses NTRU lattices — a special lattice math that produces tiny signatures.",
             "fact":"Falcon signatures are 5 times smaller than Dilithium! Perfect for smart cards and IoT sensors with limited storage.",
             "size":"897 bytes — the most compact quantum-safe signature algorithm!"},
        ]

        selected = st.selectbox("Choose an algorithm:", [a["name"] for a in ALGOS], key="keylab_sel")
        algo = next(a for a in ALGOS if a["name"] == selected)
        color = algo["color"]
        safe_label = "Quantum Safe" if algo["safe"] else "NOT Quantum Safe"
        safe_color = "#10b981" if algo["safe"] else "#ef4444"
        safe_emoji = "✅" if algo["safe"] else "❌"

        st.markdown(
            "<div style='background:" + color + "15;border:2px solid " + color + "40;"
            "border-radius:12px;padding:1.25rem;margin:0.75rem 0;'>"
            "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;'>"
            "<h3 style='margin:0;color:" + color + "'>" + algo["emoji"] + " " + algo["name"] + "</h3>"
            "<span style='background:" + safe_color + "20;border:1px solid " + safe_color + ";color:" + safe_color + ";"
            "padding:3px 10px;border-radius:100px;font-size:0.78rem;font-weight:bold;'>"
            + safe_emoji + " " + safe_label + "</span>"
            "</div>"
            "<p style='color:#aaa;font-size:0.82rem;margin:0;'>"
            "Type: " + algo["type"] + "  |  NIST Standard: " + algo["nist"] + "</p>"
            "</div>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**How it works (simple version):**")
            st.info(algo["analogy"])
        with col2:
            st.markdown("**Fun Fact:**")
            st.success(algo["fact"])
        st.markdown("**Key Size:** " + algo["size"])

        st.markdown("---")
        st.markdown("### How Does It Compare to Others?")

        import plotly.graph_objects as go
        names = [a["name"] for a in ALGOS]
        sizes = [a["key_kb"] for a in ALGOS]
        colors_list = [a["color"] for a in ALGOS]
        sel_idx = next(i for i, a in enumerate(ALGOS) if a["name"] == selected)
        bar_colors = [c + "ff" if i == sel_idx else c + "66" for i, c in enumerate(colors_list)]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=names, y=sizes,
            marker_color=bar_colors,
            text=[str(s) + " KB" for s in sizes],
            textposition="outside",
        ))
        fig.update_layout(
            height=320,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color="#888", tickangle=-30),
            yaxis=dict(title="Key Size (KB)", color="#888"),
            font=dict(color="#ccc", size=11),
            margin=dict(l=20, r=20, t=20, b=80),
        )
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Key Size", algo["size"].split("—")[0].strip())
        with col2:
            st.metric("Quantum Safe", safe_emoji + " " + safe_label)

        st.markdown("---")
        st.markdown("### Quick Quiz!")
        quiz = st.radio(
            "Which algorithm is BOTH quantum-safe AND has a small key?",
            ["RSA-4096 — big key, quantum safe",
             "Kyber-512 — small key, quantum safe",
             "ECC-256 — small key, not quantum safe",
             "RSA-2048 — small key, quantum safe"],
            key="keylab_quiz"
        )
        if st.button("Check My Answer!", key="keylab_check"):
            if "Kyber-512" in quiz:
                st.success("Correct! Kyber-512 has an 800-byte public key AND is quantum-safe! That is why NIST made it FIPS 203.")
                award_badge("🔬 Key Lab Expert", xp=15)
                from modules.progress_tracker import mark_complete
                mark_complete("key_size_lab")
            else:
                st.error("Not quite! RSA keys are huge and NOT quantum-safe. ECC is small but also NOT quantum-safe. Kyber wins on both!")

        st.markdown("---")
        st.info(
            "The winner: Kyber (ML-KEM) gives us keys that are SMALLER than RSA "
            "AND completely quantum-safe. That is why the US government chose it as FIPS 203 in 2024. "
            "Every internet connection will eventually switch to Kyber!"
        )
