"""
modules/elementary.py
─────────────────────
K-5 learning module: "Secret Keepers"

Concepts taught:
  - What is a secret? Why do we hide messages?
  - Old locks (classical crypto) vs. quantum-proof locks
  - Color-mixing key exchange analogy
  - Meet the Quantum Monster
"""

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

def render_elementary():
    st.title("🟢 Secret Keepers — Elementary Edition")
    st.markdown(
        "Welcome, young agent! Your mission: learn how to send secret messages "
        "that even the scariest quantum monsters can't crack. 🐉🔐"
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📖 Story Time", "🎨 Color Mixing Keys", "🔒 Lock Puzzle", "📝 Vocab Cards"]
    )

    # ── Tab 1: Story Mode ──────────────────────────────────────────────────────
    with tab1:
        st.subheader("🌟 Help Agent Pixel!")
        st.markdown(
            """
            Agent Pixel needs to send a secret message to her friend Byte across town.
            But the evil **Quantum Monster** can break ALL the old locks!

            > *"Don't worry,"* says her teacher. *"We have NEW locks — lattice locks —
            that even quantum monsters can't pick!"*

            **Lattice locks** use a special math puzzle: imagine a giant tangled grid.
            Even a super-fast quantum computer gets lost in it!
            """
        )
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Lattice_torsion_points.svg/320px-Lattice_torsion_points.svg.png",
            caption="A lattice — like a giant tangled grid of dots 🔵",
            width=300,
        )
        st.markdown("### 🐉 Meet the Quantum Monster")
        col1, col2 = st.columns(2)
        with col1:
            st.error(
                "🐉 **Old Lock (RSA)**\n\n"
                "The Quantum Monster can pick this lock in seconds. ❌"
            )
        with col2:
            st.success(
                "🔐 **Lattice Lock (Kyber)**\n\n"
                "The Quantum Monster is totally stumped! ✅"
            )

        if st.button("✅ I finished the story!", key="story_done"):
            award_badge("📖 Story Reader", xp=5)

    # ── Tab 2: Color Mixing Key Exchange ──────────────────────────────────────
    with tab2:
        st.subheader("🎨 Secret Color Mixing")
        st.markdown(
            """
            Here's a fun way to understand how two friends can agree on a secret
            without anyone else figuring it out — using **colors**!

            1. Everyone can see a **public color** (yellow).
            2. Each friend picks a **secret color** nobody else knows.
            3. They mix their secret color with the public color and swap.
            4. Both friends end up with the **same final color** — their shared secret!
            """
        )

        col1, col2 = st.columns(2)
        with col1:
            alice_color = st.color_picker("🧑 Alice's secret color", "#FF6B6B")
        with col2:
            bob_color = st.color_picker("👦 Bob's secret color", "#4ECDC4")

        public_color = "#FFD700"  # Gold — "public"
        st.markdown(f"🌍 **Public color (everyone sees this):** `{public_color}` 🟡")

        # Simple hex blending for visual effect
        def blend_hex(c1: str, c2: str) -> str:
            c1, c2 = c1.lstrip("#"), c2.lstrip("#")
            r = (int(c1[0:2], 16) + int(c2[0:2], 16)) // 2
            g = (int(c1[2:4], 16) + int(c2[2:4], 16)) // 2
            b = (int(c1[4:6], 16) + int(c2[4:6], 16)) // 2
            return f"#{r:02X}{g:02X}{b:02X}"

        alice_mix = blend_hex(alice_color, public_color)
        bob_mix = blend_hex(bob_color, public_color)
        shared_secret = blend_hex(alice_mix, bob_mix)

        st.markdown("---")
        st.markdown(f"Alice sends Bob: `{alice_mix}` &nbsp; Bob sends Alice: `{bob_mix}`")
        st.markdown(
            f"<div style='background:{shared_secret};padding:20px;border-radius:12px;"
            f"text-align:center;color:white;font-weight:bold;font-size:1.2em'>"
            f"🎉 Shared Secret Color: {shared_secret}</div>",
            unsafe_allow_html=True,
        )
        st.caption("An eavesdropper who only sees the mixed colors can't figure out the secret!")

        if st.button("🎨 I learned about color keys!", key="color_done"):
            award_badge("🎨 Color Cryptographer", xp=10)

    # ── Tab 3: Lock Puzzle ────────────────────────────────────────────────────
    
    with tab3:
        st.subheader("🔒 Which Lock is Quantum-Safe?")
        st.markdown("Help Agent Pixel choose the right lock! Tap the quantum-safe one:")

        # ── Timer setup ───────────────────────────────────────────────────
        import time
        if "quiz_start" not in st.session_state:
            st.session_state.quiz_start = time.time()

        elapsed = int(time.time() - st.session_state.quiz_start)
        remaining = max(0, 30 - elapsed)

        if remaining > 0:
            st.info(f"⏱️ Time remaining: **{remaining} seconds**")
        else:
            st.warning("⏰ Time's up! Try again.")
            st.session_state.quiz_start = time.time()

        options = {
            "🔑 RSA Lock — math with big numbers": False,
            "🌐 Lattice Lock — tangled grid math": True,
            "🔓 Padlock — just a key": False,
            "🧮 ECC Lock — elliptic curves": False,
        }

        options = {
            "🔑 RSA Lock — math with big numbers": False,
            "🌐 Lattice Lock — tangled grid math": True,
            "🔓 Padlock — just a key": False,
            "🧮 ECC Lock — elliptic curves": False,
        }

        if "lock_answered" not in st.session_state:
            st.session_state.lock_answered = False

        for label, is_correct in options.items():
            if st.button(label, key=f"lock_{label}"):
                if not check_rate_limit("lock_puzzle", st.session_state):
                    st.warning("Slow down, agent! Try again in a moment.")
                else:
                    st.session_state.lock_answered = True
                    if is_correct:
                        st.success("✅ Correct! The Lattice Lock stumps quantum monsters!")
                        if elapsed < 10:
                            st.balloons()
                            st.success("⚡ Speed bonus! +15 XP")
                            st.session_state.xp += 15
                        award_badge("🔒 Lock Expert", xp=15)
                        st.session_state.quiz_start = time.time()
                    else:
                        st.error(
                            "❌ Not quite. Hint: quantum computers are great at number "
                            "problems. What kind of math is hardest for them?"
                        )

    # ── Tab 4: Vocabulary Cards ───────────────────────────────────────────────
    with tab4:
        st.subheader("📝 Vocabulary Flashcards")
        vocab = {
            "Cryptography": "The science of writing secret messages so only the right person can read them.",
            "Quantum Computer": "A super-powerful computer that uses tiny particles to solve some math problems VERY fast.",
            "Lattice": "A tangled grid of dots — used in new, quantum-safe math puzzles.",
            "Key": "A secret piece of information used to lock or unlock a message.",
            "Encryption": "Scrambling a message so only someone with the key can unscramble it.",
            "Post-Quantum Cryptography": "New types of secret codes that even quantum computers can't break!",
        }

        word = st.selectbox("Pick a vocab word:", list(vocab.keys()))
        st.info(f"**{word}:** {vocab[word]}")

        answer = st.text_input("Try to explain it in your own words:", key="vocab_answer")
        if st.button("Submit my explanation", key="vocab_submit"):
            if not check_rate_limit("vocab_submit", st.session_state):
                st.warning("Take a breath — try again in a moment!")
            else:
                clean = sanitize_input(answer)
                if len(clean) > 10:
                    st.success(f"Great job! You wrote: *\"{clean}\"* 🌟")
                    award_badge("📚 Vocab Vault", xp=5)
                else:
                    st.warning("Tell me a little more — you've got this!")
