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

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📖 Story Time", "🎨 Color Mixing Keys", "🔒 Lock Puzzle", "📝 Vocab Cards", "🧱 Mini Game"]
    )

    # ── Tab 1: Lattice Explorer ───────────────────────────────────────────────
    with tab1:
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
                    award_badge("🏗️ Lattice Navigator", xp=20)
                    st.session_state.lattice_s = random.randint(2, 9)
                else:
                    st.error(
                        f"❌ Not quite! You've tried {st.session_state.lattice_attempts} time(s). "
                        "The noise makes it tricky, right? That's the whole point!"
                    )

    # ── Tab 2: Hash Factory ───────────────────────────────────────────────────
    with tab2:
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

    # ── Tab 3: Quantum vs Classical Race ─────────────────────────────────────
    with tab3:
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

    # ── Tab 4: Key Workshop ───────────────────────────────────────────────────
    with tab4:
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

    with tab5:
        from modules.games import render_lattice_maze
        render_lattice_maze()