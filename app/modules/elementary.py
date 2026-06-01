from modules.progress_tracker import mark_complete, is_complete
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

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        ["📖 Story Time", "🎨 Color Mixing Keys", "🔒 Lock Puzzle", "📝 Vocab Cards", "🧱 Mini Game", "🔤 Word Search", "✏️ Crossword"]
    )

    # ── Tab 1: Story Mode ──────────────────────────────────────────────────────
    with tab1:
        st.subheader("📖 Agent Pixel and the Quantum Monster")

        if "story_page" not in st.session_state:
            st.session_state.story_page = 0

        pages = [
            {
                "title": "Chapter 1 — The Sneaky Quantum Monster",
                "emoji": "👾",
                "color": "#4f46e5",
                "text": (
                    "Meet **Agent Pixel** — the world's coolest cryptographer.\n\n"
                    "She has purple hair, a jetpack, and a pet robot named **Byte** who only speaks in beeps.\n\n"
                    "One day Agent Pixel gets an emergency message:\n\n"
                    "> *ALERT! The Quantum Monster escaped from the math dimension! "
                    "It is eating all the world's secret codes for BREAKFAST!* 🍳\n\n"
                    "Agent Pixel looks at Byte. Byte looks at Agent Pixel.\n\n"
                    "**Uh oh** says Byte. *(Beep boop.)*\n\n"
                    "**The Quantum Monster can break every old lock in the world. "
                    "RSA locks, ECC locks, even the lock on my lunch box!**\n\n"
                    "**BEEP!** says Byte, very alarmed.\n\n"
                    "**We need quantum-safe locks. FAST!** 🔐"
                ),
                "quiz": None,
            },
            {
                "title": "Chapter 2 — Old Locks Are No Good",
                "emoji": "💀",
                "color": "#ef4444",
                "text": (
                    "The Quantum Monster is HUGE. It has seventeen eyes, six arms, "
                    "and it smells like old math homework.\n\n"
                    "**NOM!** There goes the bank's password. 🏦\n\n"
                    "**CHOMP!** There goes the school's homework files. 📚\n\n"
                    "**BURP!** Excuse you, Quantum Monster. 🫢\n\n"
                    "Agent Pixel explains: **The old locks use RSA — big numbers multiplied together. "
                    "Normal computers take a million years to crack them.**\n\n"
                    "**Beep?** asks Byte. *(So what's the problem?)*\n\n"
                    "**The Quantum Monster uses Shor's Algorithm — it tries ALL the answers at the same time!**\n\n"
                    "Byte's eyes go very wide. **BEEEEEP.**\n\n"
                    "**Yep. We need NEW locks. Quantum-safe ones.** 🔒"
                ),
                "quiz": {
                    "question": "Why is the Quantum Monster dangerous to RSA locks?",
                    "options": [
                        "It is very smelly",
                        "It uses Shor's Algorithm to try all answers at once",
                        "It has seventeen eyes",
                        "It ate the keys"
                    ],
                    "answer": 1,
                    "xp": 10,
                    "key": "story_q1"
                }
            },
            {
                "title": "Chapter 3 — The Magic Lattice",
                "emoji": "🏗️",
                "color": "#10b981",
                "text": (
                    "Agent Pixel pulls out her secret weapon — a glowing blue crystal called **KYBER**. ✨\n\n"
                    "**What does it do?** beeps Byte.\n\n"
                    "**It uses LATTICE math** — imagine a dot-to-dot puzzle with a TRILLION dots "
                    "across a THOUSAND dimensions.\n\n"
                    "Byte tries to imagine this. Byte's brain overheats. 🤯\n\n"
                    "**Even the Quantum Monster cannot solve that puzzle!**\n\n"
                    "She installs Kyber locks on everything. The Quantum Monster runs up and tries to eat one.\n\n"
                    "It bounces off. 💥 Tries again. Bounces off again. Sits down and cries a little. 😢\n\n"
                    "**QUANTUM SAFE!** cheers Byte. 🎉"
                ),
                "quiz": {
                    "question": "What is Kyber based on?",
                    "options": [
                        "Lattice math — a giant dot grid across thousands of dimensions!",
                        "RSA prime numbers",
                        "Byte's brain",
                        "Homework"
                    ],
                    "answer": 0,
                    "xp": 10,
                    "key": "story_q2"
                }
            },
            {
                "title": "Chapter 4 — Three Heroes Save the Day",
                "emoji": "🦸",
                "color": "#8b5cf6",
                "text": (
                    "But the Quantum Monster has PLAN B — a giant hammer labelled **Grover's Algorithm**. 🔨\n\n"
                    "**Uh oh** beeps Byte. *(Again.)*\n\n"
                    "Agent Pixel calls in backup:\n\n"
                    "🛡️ **DILITHIUM** — big and strong, signs documents so you know they are real.\n\n"
                    "🌲 **SPHINCS+** — speedy, uses fingerprint math as a backup plan.\n\n"
                    "**KYBER! DILITHIUM! SPHINCS+!** The wall holds.\n\n"
                    "The Quantum Monster sits down and eats its own tail in frustration. 🤦\n\n"
                    "**Should we help it?** beeps Byte.\n\n"
                    "**Absolutely not** says Agent Pixel. 😄"
                ),
                "quiz": {
                    "question": "Which three algorithms saved the world?",
                    "options": [
                        "RSA, ECC, and DES",
                        "Kyber, Dilithium, and SPHINCS+",
                        "Byte, Pixel, and Grover",
                        "SHA, MD5, and AES"
                    ],
                    "answer": 1,
                    "xp": 25,
                    "key": "story_q3"
                }
            },
            {
                "title": "Chapter 5 — The Happy Ending 🎉",
                "emoji": "🎉",
                "color": "#f59e0b",
                "text": (
                    "The Quantum Monster shuffled away, grumbling about lattice math.\n\n"
                    "Agent Pixel high-fived Byte. 🙏 Every lock was now quantum-safe. "
                    "Banks. Hospitals. Schools. Even Agent Pixel's lunch box.\n\n"
                    "**Will it ever come back?** asked Byte.\n\n"
                    "**Maybe. That is why we keep learning!** smiled Agent Pixel.\n\n"
                    "Byte beeped happily. 🤖\n\n"
                    "**THE END!**\n\n"
                    "*(The Quantum Monster eventually got a job teaching math. It was not very good at it.)*\n\n"
                    "---\n🏅 **You finished the story! You are now an official Secret Keeper!**"
                ),
                "quiz": None,
            },
        ]

        page = pages[st.session_state.story_page]
        total_pages = len(pages)
        current = st.session_state.story_page

        st.progress(current / total_pages)
        st.caption(f"Chapter {current + 1} of {total_pages}")
        color = page["color"]
        emoji = page["emoji"]
        title = page["title"]

        st.markdown(
            f"<div style='background:{color}15;border-left:4px solid "
            f"{color};border-radius:0 10px 10px 0;"
            f"padding:1rem 1.5rem;margin-bottom:1rem;'>"
            f"<div style='font-size:2rem;margin-bottom:0.5rem'>{emoji}</div>"
            f"<h3 style='color:{color};margin:0'>{title}</h3>"
            f"</div>",
            unsafe_allow_html=True
        )

        st.markdown(page["text"])

        if page["quiz"]:
            quiz = page["quiz"]
            st.markdown("---")
            st.markdown(f"**🧠 Quick Check:** {quiz['question']}")
            key = quiz["key"]
            if f"answered_{key}" not in st.session_state:
                st.session_state[f"answered_{key}"] = False
            if not st.session_state[f"answered_{key}"]:
                for i, option in enumerate(quiz["options"]):
                    if st.button(option, key=f"quiz_{key}_{i}"):
                        if i == quiz["answer"]:
                            st.session_state[f"answered_{key}"] = True
                            st.session_state.xp += quiz["xp"]
                            st.success(f"✅ Correct! +{quiz['xp']} XP")
                            st.balloons()
                        else:
                            st.error("❌ Not quite! Read the chapter again!")
            else:
                st.success("✅ Already answered!")

        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if current > 0:
                if st.button("← Previous", key="story_prev"):
                    st.session_state.story_page -= 1
                    st.rerun()
        with col2:
            st.caption(f"Page {current + 1} / {total_pages}")
        with col3:
            if current < total_pages - 1:
                if st.button("Next →", key="story_next"):
                    st.session_state.story_page += 1
                    st.rerun()
            else:
                st.success("🎉 Story Complete!")
                if st.button("✅ Claim Story Badge!", key="story_badge"):
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
                        mark_complete("lock_puzzle")
                        from utils import play_sound
                        st.markdown(play_sound("correct"), unsafe_allow_html=True)
                        st.markdown(
                            '<div class="flash-correct">✅ Correct! '
                            'The Lattice Lock stumps quantum monsters!</div>',
                            unsafe_allow_html=True
                        )
                        if elapsed < 10:
                            st.balloons()
                            st.success("⚡ Speed bonus! +15 XP")
                            st.session_state.xp += 15
                        award_badge("🔒 Lock Expert", xp=15)
                        st.session_state.quiz_start = time.time()
                    else:
                        from utils import play_sound
                        st.markdown(play_sound("wrong"), unsafe_allow_html=True)
                        st.markdown(
                            '<div class="flash-wrong">❌ Not quite! '
                            f"You've tried {st.session_state.lattice_attempts} time(s). "
                            'The noise makes it tricky, right? That\'s the whole point!</div>',
                            unsafe_allow_html=True
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

    with tab5:
        from modules.games import render_falling_blocks, render_zombie_blast, render_quantumcraft_elementary
        game_choice = st.radio("Pick a game:", ["🧱 Falling Blocks", "🧟 Zombie Blast", "⛏️ QuantumCraft"], horizontal=True)
        if game_choice == "🧱 Falling Blocks":
            render_falling_blocks()
        elif game_choice == "🧟 Zombie Blast":
            render_zombie_blast(difficulty="easy")
        else:
            render_quantumcraft_elementary()