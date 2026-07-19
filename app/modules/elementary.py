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
import streamlit.components.v1 as components
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
        import streamlit.components.v1 as _tab2_comp

        st.subheader("🎨 Secret Color Mixing Adventure!")
        st.markdown(
            "🕵️ **Agent Pixel needs your help!** She and her friend Byte want to share a "
            "secret color — but the Quantum Monster is watching! Can you help them?"
        )

        # Step by step story reveal
        if "color_step" not in st.session_state:
            st.session_state.color_step = 1

        steps = [
            ("🌍 Step 1 — The Public Color", "Everyone in the world can see this color — even the Quantum Monster! That's OK because it's just the START."),
            ("🔴 Step 2 — Alice's Secret Color", "Alice picks a SECRET color that ONLY SHE knows. She mixes it with the public color and sends the result to Byte!"),
            ("🔵 Step 3 — Byte's Secret Color", "Byte picks HIS own secret color. He mixes it with the public color and sends it back to Alice!"),
            ("🎉 Step 4 — The Shared Secret!", "Now BOTH Alice and Byte mix the OTHER person's result with their OWN secret color. They get THE SAME COLOR! The Quantum Monster never figured it out! 🛡️"),
        ]

        step = st.session_state.color_step
        for i, (title, desc) in enumerate(steps):
            done = i + 1 <= step
            st.markdown(
                f"<div style='background:{'#1e293b' if done else '#0f172a'};"
                f"border:{'2px solid #10b981' if done else '1px solid #334155'};"
                f"border-radius:12px;padding:12px 16px;margin:6px 0;opacity:{'1' if done else '0.4'}'>"
                f"<div style='font-weight:bold;color:{'#10b981' if done else '#888'}'>{title}</div>"
                f"<div style='font-size:0.85rem;color:#ccc;margin-top:4px'>{desc if done else '???'}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

        st.markdown("---")

        def blend_hex(c1: str, c2: str) -> str:
            c1, c2 = c1.lstrip("#"), c2.lstrip("#")
            r = (int(c1[0:2], 16) + int(c2[0:2], 16)) // 2
            g = (int(c1[2:4], 16) + int(c2[2:4], 16)) // 2
            b = (int(c1[4:6], 16) + int(c2[4:6], 16)) // 2
            return f"#{r:02X}{g:02X}{b:02X}"

        public_color = "#FFD700"

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f"<div style='background:{public_color};border-radius:10px;padding:14px;"
                f"text-align:center;color:#333;font-weight:bold;font-size:0.9rem'>"
                f"🌍 Public Color<br>(Everyone sees!)</div>",
                unsafe_allow_html=True
            )
        with col2:
            alice_color = st.color_picker("🧑 Alice's secret:", "#FF6B6B", key="alice_clr")
            st.markdown(
                f"<div style='background:{alice_color};border-radius:8px;padding:8px;"
                f"text-align:center;color:white;font-size:0.8rem'>Alice's Secret 🔒</div>",
                unsafe_allow_html=True
            )
        with col3:
            bob_color = st.color_picker("🤖 Byte's secret:", "#4ECDC4", key="bob_clr")
            st.markdown(
                f"<div style='background:{bob_color};border-radius:8px;padding:8px;"
                f"text-align:center;color:white;font-size:0.8rem'>Byte's Secret 🔒</div>",
                unsafe_allow_html=True
            )

        alice_mix = blend_hex(alice_color, public_color)
        bob_mix = blend_hex(bob_color, public_color)
        shared_secret = blend_hex(alice_mix, bob_mix)
        shared_from_bob = blend_hex(bob_mix, alice_color)

        st.markdown("### 📬 What they share:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"<div style='background:{alice_mix};border-radius:10px;padding:12px;"
                f"text-align:center;color:white;font-weight:bold'>"
                f"📨 Alice sends Byte<br><small>(public + Alice's secret)</small></div>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"<div style='background:{bob_mix};border-radius:10px;padding:12px;"
                f"text-align:center;color:white;font-weight:bold'>"
                f"📨 Byte sends Alice<br><small>(public + Byte's secret)</small></div>",
                unsafe_allow_html=True
            )

        st.markdown("### 🎉 The Shared Secret!")
        st.markdown(
            f"<div style='background:{shared_secret};border:3px solid #10b981;"
            f"border-radius:16px;padding:24px;text-align:center;"
            f"color:white;font-weight:bold;font-size:1.3rem;margin:10px 0'>"
            f"🔐 Both Alice AND Byte get this SAME color!<br>"
            f"<small style='font-size:0.8rem;opacity:0.8'>The Quantum Monster only saw mixed colors — "
            f"it can NEVER figure out the secret! 🛡️</small>"
            f"</div>",
            unsafe_allow_html=True
        )

        # Fun quiz
        st.markdown("### 🧠 Quick Check!")
        q_ans = st.radio(
            "Why can't the Quantum Monster figure out the secret?",
            [
                "Because it doesn't have eyes 👀",
                "Because it only sees the MIXED colors, not the secret colors! 🎨",
                "Because the colors disappear 💨",
                "Because Alice runs away 🏃",
            ],
            key="color_quiz"
        )
        if st.button("Check my answer! 🎯", key="color_check"):
            if "MIXED colors" in q_ans:
                st.balloons()
                st.success("🎉 CORRECT! The Quantum Monster only sees Alice+Public and Byte+Public — never the secret colors alone!")
                award_badge("🎨 Color Cryptographer", xp=15)
                st.session_state.color_step = 4
            else:
                st.error("Not quite! Think about what the Quantum Monster actually gets to see... 🤔")
                st.session_state.color_step = max(st.session_state.color_step, 2)

    # ── Tab 3: Lock Puzzle ────────────────────────────────────────────────────

    with tab3:
        import time
        import streamlit.components.v1 as _lock_comp

        st.subheader("🔒 Agent Pixel's Lock Challenge!")
        st.markdown(
            "🚨 **EMERGENCY!** The Quantum Monster is trying to break into the Secret Vault! "
            "Agent Pixel needs the RIGHT lock — one that even a quantum computer can't crack! "
            "**Help her choose!**"
        )

        _lock_comp.html("""
<style>
body{margin:0;background:#0f172a;font-family:sans-serif;padding:8px;text-align:center;}
.monster{font-size:3rem;animation:shake 0.4s infinite;}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
.pixel{font-size:2.5rem;animation:bounce 0.8s infinite;}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.label{font-size:0.75rem;font-weight:bold;margin:3px 0;}
.row{display:flex;justify-content:center;align-items:center;gap:20px;margin:6px 0;}
</style>
<div>
<div class="monster">👾</div>
<div style="color:#ef4444;font-size:0.75rem;font-weight:bold">QUANTUM MONSTER ATTACKING!</div>
<div style="font-size:2.5rem;margin:4px 0">⚡ ➡️ 🔐 ⬅️ 🕵️</div>
<div class="label" style="color:#a5b4fc">Quantum Monster &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Secret Vault &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Agent Pixel</div>
<div style="color:#f59e0b;font-size:0.8rem;margin-top:6px;font-weight:bold">Pick the right lock to stop the monster! 🛡️</div>
</div>
""", height=160)

        st.markdown("### 🔑 Choose Agent Pixel's Lock:")
        st.caption("Only ONE lock can stop a quantum computer — read the clues carefully!")

        if "quiz_start" not in st.session_state:
            st.session_state.quiz_start = time.time()
        if "lock_attempts" not in st.session_state:
            st.session_state.lock_attempts = 0
        if "lock_solved" not in st.session_state:
            st.session_state.lock_solved = False

        elapsed = int(time.time() - st.session_state.quiz_start)

        if not st.session_state.lock_solved:
            time_color = "#10b981" if elapsed < 10 else "#f59e0b" if elapsed < 20 else "#ef4444"
            st.markdown(
                f"<div style='background:{time_color}20;border:1px solid {time_color};"
                f"border-radius:8px;padding:6px 12px;text-align:center;"
                f"font-size:0.85rem;font-weight:bold;color:{time_color};margin-bottom:10px'>"
                f"⏱️ {elapsed} seconds {' — ⚡ Speed bonus if you solve it!' if elapsed < 10 else ''}"
                f"</div>",
                unsafe_allow_html=True
            )

        LOCKS = [
            {"emoji": "🔑", "name": "RSA Lock", "color": "#ef4444",
             "clue": "Uses BIG numbers — hard to split apart... unless you have a quantum computer! 😬",
             "correct": False, "wrong_msg": "❌ Uh oh! The Quantum Monster knows Shor's trick to break RSA!"},
            {"emoji": "🏗️", "name": "Lattice Lock", "color": "#10b981",
             "clue": "Uses a SUPER tangled grid of dots. Finding the secret path is IMPOSSIBLE — even for quantum computers!",
             "correct": True, "wrong_msg": ""},
            {"emoji": "🔓", "name": "Old Padlock", "color": "#6b7280",
             "clue": "Just a plain metal lock. A toddler could figure this one out! 😂",
             "correct": False, "wrong_msg": "❌ Even a regular computer breaks this in seconds!"},
            {"emoji": "🌀", "name": "ECC Lock", "color": "#f59e0b",
             "clue": "Uses squiggly curve math. Smart... but the Quantum Monster has a trick for this too!",
             "correct": False, "wrong_msg": "❌ Shor Algorithm breaks ECC too — not safe from quantum!"},
        ]

        cols = st.columns(2)
        for i, lock in enumerate(LOCKS):
            with cols[i % 2]:
                st.markdown(
                    f"<div style='background:{lock['color']}12;border:2px solid {lock['color']}50;"
                    f"border-radius:14px;padding:14px;margin:6px 0;text-align:center;min-height:120px'>"
                    f"<div style='font-size:2.5rem;margin-bottom:4px'>{lock['emoji']}</div>"
                    f"<div style='font-weight:bold;color:{lock['color']};font-size:0.95rem'>{lock['name']}</div>"
                    f"<div style='font-size:0.78rem;color:#aaa;margin:6px 0;line-height:1.4'>{lock['clue']}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                if not st.session_state.lock_solved:
                    if st.button(f"{lock['emoji']} Use {lock['name']}!", key=f"lock_{i}", use_container_width=True):
                        if not check_rate_limit("lock_puzzle", st.session_state):
                            st.warning("Slow down, agent! Try again in a moment.")
                        else:
                            st.session_state.lock_attempts += 1
                            if lock["correct"]:
                                st.session_state.lock_solved = True
                                mark_complete("lock_puzzle")
                                xp_bonus = 25 if elapsed < 10 else 20 if elapsed < 20 else 15
                                st.session_state.xp += xp_bonus
                                award_badge("🔒 Lock Expert", xp=xp_bonus)
                            else:
                                st.error(lock["wrong_msg"] + " Try again! 🤔")

        if st.session_state.lock_solved:
            st.balloons()
            elapsed_final = int(time.time() - st.session_state.quiz_start)
            xp_earned = 25 if elapsed_final < 10 else 20 if elapsed_final < 20 else 15
            st.markdown(
                f"<div style='background:#10b98120;border:3px solid #10b981;"
                f"border-radius:16px;padding:20px;text-align:center;margin:10px 0'>"
                f"<div style='font-size:3rem'>🎉</div>"
                f"<h2 style='color:#10b981;margin:8px 0'>VAULT SAVED! YOU DID IT!</h2>"
                f"<p style='color:#ccc'>The Lattice Lock stopped the Quantum Monster cold! "
                f"The tangled grid is impossible to solve — even for quantum computers!</p>"
                f"<div style='font-size:1.2rem;font-weight:bold;color:#f59e0b;margin:8px 0'>"
                f"+{xp_earned} XP {'⚡ Speed Bonus!' if elapsed_final < 10 else '🌟 Great job!'}</div>"
                f"<p style='font-size:0.8rem;color:#888'>"
                f"Solved in {elapsed_final}s with {st.session_state.lock_attempts} attempt(s)</p>"
                f"</div>",
                unsafe_allow_html=True
            )
            if st.button("🔄 Play Again!", key="lock_reset"):
                st.session_state.lock_solved = False
                st.session_state.lock_attempts = 0
                st.session_state.quiz_start = time.time()
                st.rerun()

        st.markdown("---")
        st.info(
            "💡 **Why the Lattice Lock wins:** Imagine hiding a needle in a grid of "
            "one TRILLION dots spread across 1000 dimensions. That's what the lattice math does! "
            "Even the fastest quantum computer gets completely lost. That's why NIST chose "
            "**Kyber (the Lattice Lock)** to protect the internet! 🏗️🔐"
        )

    # ── Tab 4: Vocabulary Cards ───────────────────────────────────────────────
    with tab4:
        import streamlit.components.v1 as _vocab_comp

        st.subheader("📝 PQC Vocabulary Adventure!")
        st.markdown(
            "🕵️ **Agent Pixel's Secret Dictionary!** Learn the words that keep the world safe. "
            "Click a word to flip the card, then test yourself!"
        )

        VOCAB = [
            {"word": "Cryptography", "emoji": "🔐",
             "simple": "Writing secret messages so only YOUR friend can read them!",
             "full": "The science of creating codes and ciphers to protect information from people who should not see it.",
             "example": "When you pass a secret note in class — that is cryptography!",
             "color": "#10b981"},
            {"word": "Quantum Computer", "emoji": "⚛️",
             "simple": "A SUPER powerful computer that uses magic tiny particles!",
             "full": "A computer that uses quantum mechanics — qubits that can be 0 AND 1 at the same time — to solve some problems exponentially faster.",
             "example": "Like having a million calculators all working at the same time!",
             "color": "#8b5cf6"},
            {"word": "Lattice", "emoji": "🏗️",
             "simple": "A giant grid of dots with a secret hidden inside!",
             "full": "A mathematical structure — a regular grid of points in space. In 1000 dimensions, finding the secret dot is impossible even for quantum computers.",
             "example": "Like a huge 3D puzzle where pieces are spread across 1000 dimensions!",
             "color": "#3b82f6"},
            {"word": "Encryption", "emoji": "🔒",
             "simple": "Scrambling a message so it looks like nonsense!",
             "full": "The process of encoding information so only the person with the correct key can understand it. Used for emails, texts, and websites.",
             "example": "Hello → #$@!kX9 (only your friend with the key can turn it back!)",
             "color": "#f59e0b"},
            {"word": "Kyber", "emoji": "💎",
             "simple": "The new super-lock that quantum computers CANNOT break!",
             "full": "ML-KEM FIPS 203 — the NIST approved post-quantum key exchange algorithm. Uses lattice math based on the Module-LWE problem.",
             "example": "Kyber is like a lock with a trillion trillion trillion possible combinations!",
             "color": "#10b981"},
            {"word": "Shor's Algorithm", "emoji": "💥",
             "simple": "The quantum monster's secret weapon against old locks!",
             "full": "A quantum algorithm created by Peter Shor in 1994 that can factor large numbers exponentially faster than classical computers, breaking RSA.",
             "example": "Like having a cheat code that instantly solves the old RSA math puzzle!",
             "color": "#ef4444"},
            {"word": "Post-Quantum Cryptography", "emoji": "🛡️",
             "simple": "NEW secret codes that EVEN quantum computers cannot crack!",
             "full": "Cryptographic algorithms designed to be secure against both classical and quantum computers. NIST approved 4 standards in 2024.",
             "example": "Kyber, Dilithium, SPHINCS+, and Falcon are the four new quantum-safe heroes!",
             "color": "#4f46e5"},
            {"word": "NIST", "emoji": "🏛️",
             "simple": "The US government team that picks the BEST secret codes!",
             "full": "National Institute of Standards and Technology — a US federal agency that runs competitions to find the best cryptographic algorithms.",
             "example": "NIST tested 69 algorithms for 6 years and picked 4 winners in 2024!",
             "color": "#f97316"},
        ]

        if "vocab_card_idx" not in st.session_state:
            st.session_state.vocab_card_idx = 0
        if "vocab_flipped" not in st.session_state:
            st.session_state.vocab_flipped = False
        if "vocab_mastered" not in st.session_state:
            st.session_state.vocab_mastered = set()
        if "vocab_quiz_mode" not in st.session_state:
            st.session_state.vocab_quiz_mode = False

        # Progress bar
        mastered = len(st.session_state.vocab_mastered)
        st.progress(mastered / len(VOCAB))
        st.caption(f"🌟 {mastered}/{len(VOCAB)} words mastered!")

        mode_col1, mode_col2 = st.columns(2)
        with mode_col1:
            if st.button("📖 Flashcard Mode" if st.session_state.vocab_quiz_mode else "✅ Flashcard Mode (Active)", use_container_width=True):
                st.session_state.vocab_quiz_mode = False
                st.rerun()
        with mode_col2:
            if st.button("🎯 Quiz Mode" if not st.session_state.vocab_quiz_mode else "✅ Quiz Mode (Active)", use_container_width=True):
                st.session_state.vocab_quiz_mode = True
                st.rerun()

        st.markdown("---")

        if not st.session_state.vocab_quiz_mode:
            # Flashcard mode
            card = VOCAB[st.session_state.vocab_card_idx]
            color = card["color"]

            _vocab_comp.html(f"""
<style>
body{{margin:0;background:#0f172a;font-family:sans-serif;}}
.card-container{{perspective:800px;width:100%;max-width:420px;margin:0 auto;height:220px;cursor:pointer;}}
.card{{width:100%;height:100%;position:relative;transform-style:preserve-3d;transition:transform 0.6s;}}
.card.flipped{{transform:rotateY(180deg);}}
.face{{position:absolute;width:100%;height:100%;backface-visibility:hidden;border-radius:16px;
    display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px;box-sizing:border-box;}}
.front{{background:linear-gradient(135deg,{color}30,{color}10);border:2px solid {color}60;}}
.back{{background:linear-gradient(135deg,#1e293b,#0f172a);border:2px solid {color};transform:rotateY(180deg);}}
.emoji{{font-size:3.5rem;margin-bottom:8px;}}
.word{{font-size:1.4rem;font-weight:bold;color:white;text-align:center;}}
.hint{{font-size:0.78rem;color:#888;margin-top:8px;}}
.simple{{font-size:0.95rem;color:{color};font-weight:bold;text-align:center;line-height:1.4;}}
.example{{font-size:0.78rem;color:#888;text-align:center;margin-top:8px;font-style:italic;}}
</style>
<div class="card-container" onclick="this.querySelector('.card').classList.toggle('flipped')">
<div class="card" id="card">
<div class="face front">
    <div class="emoji">{card['emoji']}</div>
    <div class="word">{card['word']}</div>
    <div class="hint">👆 Click to see what it means!</div>
</div>
<div class="face back">
    <div class="simple">"{card['simple']}"</div>
    <div class="example">💡 {card['example']}</div>
</div>
</div>
</div>
""", height=240)

            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("⬅️ Prev", key="vocab_prev", use_container_width=True):
                    st.session_state.vocab_card_idx = (st.session_state.vocab_card_idx - 1) % len(VOCAB)
                    st.session_state.vocab_flipped = False
                    st.rerun()
            with col2:
                if st.button(f"{'✅ Already Mastered!' if st.session_state.vocab_card_idx in st.session_state.vocab_mastered else '⭐ I Got It! Mark Mastered'}", key="vocab_master", use_container_width=True, type="primary"):
                    st.session_state.vocab_mastered.add(st.session_state.vocab_card_idx)
                    st.session_state.xp = st.session_state.get("xp", 0) + 5
                    if len(st.session_state.vocab_mastered) == len(VOCAB):
                        award_badge("📚 Vocab Master", xp=20)
                        st.balloons()
                    st.session_state.vocab_card_idx = (st.session_state.vocab_card_idx + 1) % len(VOCAB)
                    st.rerun()
            with col3:
                if st.button("Next ➡️", key="vocab_next", use_container_width=True):
                    st.session_state.vocab_card_idx = (st.session_state.vocab_card_idx + 1) % len(VOCAB)
                    st.session_state.vocab_flipped = False
                    st.rerun()

            st.caption(f"Card {st.session_state.vocab_card_idx + 1} of {len(VOCAB)} — {card['word']}")

            # Full definition
            with st.expander("📖 See the full definition"):
                st.markdown(f"**{card['word']}** {card['emoji']}")
                st.markdown(f"*Simple:* {card['simple']}")
                st.markdown(f"*Full:* {card['full']}")
                st.markdown(f"*Example:* {card['example']}")

        else:
            # Quiz mode
            import random
            if "vocab_q" not in st.session_state:
                st.session_state.vocab_q = random.randint(0, len(VOCAB)-1)  # nosec B311
                st.session_state.vocab_q_answered = False

            card = VOCAB[st.session_state.vocab_q]
            color = card["color"]

            st.markdown(
                f"<div style='background:{color}15;border:2px solid {color}50;"
                f"border-radius:14px;padding:16px;text-align:center;margin:8px 0'>"
                f"<div style='font-size:3rem;margin-bottom:6px'>{card['emoji']}</div>"
                f"<div style='font-size:1.1rem;color:#888;margin-bottom:4px'>What does this mean?</div>"
                f"<div style='font-size:1.5rem;font-weight:bold;color:white'>{card['word']}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

            # Generate wrong answers
            wrong_pool = [v["simple"] for v in VOCAB if v["word"] != card["word"]]
            random.shuffle(wrong_pool)
            options = [card["simple"]] + wrong_pool[:3]
            random.shuffle(options)

            if not st.session_state.vocab_q_answered:
                for opt in options:
                    if st.button(opt[:80] + "..." if len(opt) > 80 else opt, key=f"vq_{opt[:20]}", use_container_width=True):
                        if opt == card["simple"]:
                            st.success(f"🎉 CORRECT! {card['emoji']} {card['word']} = {card['simple']}")
                            st.session_state.vocab_mastered.add(st.session_state.vocab_q)
                            st.session_state.xp = st.session_state.get("xp", 0) + 10
                            st.session_state.vocab_q_answered = True
                            award_badge("📚 Vocab Vault", xp=10)
                        else:
                            st.error(f"❌ Not quite! The answer was: **{card['simple']}**")
                            st.session_state.vocab_q_answered = True
            else:
                if st.button("➡️ Next Question! +10 XP", key="vocab_next_q", type="primary", use_container_width=True):
                    st.session_state.vocab_q = random.randint(0, len(VOCAB)-1)  # nosec B311
                    st.session_state.vocab_q_answered = False
                    st.rerun()

        st.markdown("---")
        st.markdown("### 🌟 All Vocab Words")
        cols = st.columns(4)
        for i, v in enumerate(VOCAB):
            with cols[i % 4]:
                mastered_this = i in st.session_state.vocab_mastered
                st.markdown(
                    f"<div style='text-align:center;padding:8px;border-radius:8px;"
                    f"background:{'#10b98120' if mastered_this else '#1e293b'};"
                    f"border:1px solid {'#10b981' if mastered_this else '#334155'};margin:3px'>"
                    f"<div>{v['emoji']}</div>"
                    f"<div style='font-size:0.7rem;color:{'#10b981' if mastered_this else '#888'}'>"
                    f"{'✅ ' if mastered_this else ''}{v['word'][:10]}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

    with tab5:
        from modules.games import render_falling_blocks, render_zombie_blast
        game_choice = st.radio("Pick a game:", ["🧱 Falling Blocks", "🧟 Zombie Blast", "🧪 Quantum Sandbox"], horizontal=True)
        if game_choice == "🧱 Falling Blocks":
            render_falling_blocks()
        elif game_choice == "🧟 Zombie Blast":
            render_zombie_blast(difficulty="easy")
        elif "Sandbox" in game_choice:
            from modules.quantum_sandbox import render_quantum_sandbox
            render_quantum_sandbox()
    with tab6:
        st.subheader("🔤 PQC Word Search — 12 Levels!")
        st.markdown("Find all the hidden words! Each level gets bigger and harder!")

        if "ws_level" not in st.session_state:
            st.session_state.ws_level = 1

        WS_LEVELS = [
            {"level":1,  "words":["KYBER","HASH","KEY","NIST","SAFE"],                                                    "cols":10,"rows":8,  "desc":"Beginner — 5 words"},
            {"level":2,  "words":["FALCON","CIPHER","QUBIT","NOISE","LOCK"],                                              "cols":10,"rows":8,  "desc":"Beginner — 5 words"},
            {"level":3,  "words":["LATTICE","SHOR","PRIME","FIPS","RING","BIT"],                                          "cols":12,"rows":9,  "desc":"Easy — 6 words"},
            {"level":4,  "words":["DILITHIUM","GROVER","VECTOR","MATRIX","MODULAR","SECURE"],                             "cols":12,"rows":9,  "desc":"Easy — 6 words"},
            {"level":5,  "words":["SPHINCS","ENCRYPT","DECRYPT","DIGITAL","SIGN","PUBLIC","PRIVATE"],                     "cols":13,"rows":10, "desc":"Medium — 7 words"},
            {"level":6,  "words":["QUANTUM","RANDOM","SAMPLE","ATTACK","DEFEND","BLOCK","STREAM"],                        "cols":13,"rows":10, "desc":"Medium — 7 words"},
            {"level":7,  "words":["HARDNESS","PROBLEM","CLASSIC","HYBRID","PROTOCOL","HANDSHAKE","VERIFY"],               "cols":14,"rows":11, "desc":"Hard — 7 words"},
            {"level":8,  "words":["ALGORITHM","STANDARD","SECURITY","ENTROPY","PERMUTE","ABSORB","SQUEEZE","HASH"],       "cols":14,"rows":11, "desc":"Hard — 8 words"},
            {"level":9,  "words":["POLYNOMIAL","COEFFICIENT","REDUCTION","COMPRESS","EXPAND","MODULE","DEGREE","RING"],   "cols":15,"rows":12, "desc":"Expert — 8 words"},
            {"level":10, "words":["ENCAPSULATE","DECAPSULATE","KEYPAIR","CIPHERTEXT","PLAINTEXT","NONCE","SEED","RANDOM","HASH"],"cols":15,"rows":12,"desc":"Expert — 9 words"},
            {"level":11, "words":["SIGNATURE","VERIFICATION","REJECTION","SAMPLING","COMMITMENT","CHALLENGE","RESPONSE","TRANSCRIPT","BINDING"],"cols":16,"rows":13,"desc":"Master — 9 words"},
            {"level":12, "words":["POSTQUANTUM","MIGRATION","CRYPTOAGILE","HYBRID","TRANSITION","TIMELINE","STANDARD","APPROVED","FEDERAL","SECURE"],"cols":16,"rows":13,"desc":"Master — 10 words"},
        ]

        WORD_FACTS = {
            "KYBER":"ML-KEM FIPS 203 — NIST standard for quantum-safe key exchange!",
            "HASH":"SHA-3 creates a unique fingerprint of any message!",
            "KEY":"Secret information used to lock or unlock encrypted data!",
            "NIST":"The US agency that approved all four PQC standards in 2024!",
            "SAFE":"Quantum-safe means secure even against quantum computers!",
            "FALCON":"FN-DSA FIPS 206 — the smallest quantum-safe signature!",
            "CIPHER":"A method of scrambling messages so only the key owner can read them!",
            "QUBIT":"The quantum version of a bit — can be 0 AND 1 at the same time!",
            "NOISE":"Small random errors added to LWE equations to hide the secret!",
            "LOCK":"A cryptographic lock protects your data from attackers!",
            "LATTICE":"A multi-dimensional grid of dots — the math behind Kyber!",
            "SHOR":"Shor Algorithm breaks RSA and ECC on quantum computers!",
            "PRIME":"Prime numbers like 7 and 13 are the foundation of RSA!",
            "FIPS":"Federal Information Processing Standard — official NIST label!",
            "RING":"A polynomial ring is the math structure inside Kyber!",
            "BIT":"The smallest unit of data — a 0 or a 1!",
            "DILITHIUM":"ML-DSA FIPS 204 — quantum-safe digital signature standard!",
            "GROVER":"Grover Algorithm gives quantum computers a search speedup!",
            "VECTOR":"A list of numbers used in lattice math calculations!",
            "MATRIX":"A grid of numbers — Kyber uses matrix multiplication!",
            "MODULAR":"Modular arithmetic is clock math — numbers wrap around!",
            "SECURE":"Cryptographically secure means attackers cannot break it!",
            "SPHINCS":"SLH-DSA FIPS 205 — hash-based backup signature standard!",
            "ENCRYPT":"Scrambling plaintext into ciphertext using a key!",
            "DECRYPT":"Unscrambling ciphertext back to plaintext using a key!",
            "DIGITAL":"A digital signature proves a message is authentic!",
            "SIGN":"To cryptographically sign is to prove authenticity!",
            "PUBLIC":"The public key can be shared with anyone safely!",
            "PRIVATE":"The private key must never be shared with anyone!",
            "QUANTUM":"A quantum computer uses qubits to solve problems differently!",
            "RANDOM":"True randomness is essential for secure key generation!",
            "SAMPLE":"Sampling noise from a distribution is key to LWE security!",
            "ATTACK":"A cryptographic attack tries to break encryption!",
            "DEFEND":"Post-quantum crypto defends against quantum attacks!",
            "BLOCK":"A block cipher encrypts fixed-size chunks of data!",
            "STREAM":"A stream cipher encrypts data one bit at a time!",
            "HARDNESS":"Security is based on the hardness of math problems!",
            "PROBLEM":"The hard problem in PQC is finding short lattice vectors!",
            "CLASSIC":"Classical computers use bits — quantum computers use qubits!",
            "HYBRID":"Hybrid cryptography uses both classical and PQC algorithms!",
            "PROTOCOL":"A cryptographic protocol defines the rules for secure communication!",
            "HANDSHAKE":"A TLS handshake establishes a secure connection!",
            "VERIFY":"Verification checks that a digital signature is authentic!",
            "ALGORITHM":"A step-by-step procedure for solving a math problem!",
            "STANDARD":"NIST standards define which algorithms are officially approved!",
            "SECURITY":"Cryptographic security means attackers cannot feasibly break it!",
            "ENTROPY":"Entropy measures randomness — high entropy means more secure!",
            "PERMUTE":"Permutation rearranges data — used inside SHA-3!",
            "ABSORB":"SHA-3 absorbs input data in chunks during hashing!",
            "SQUEEZE":"SHA-3 squeezes out the final hash output!",
            "POLYNOMIAL":"Kyber works with polynomials — math expressions with variables!",
            "COEFFICIENT":"Each number in a polynomial is a coefficient!",
            "REDUCTION":"NTT reduction makes polynomial math fast in Kyber!",
            "COMPRESS":"Kyber compresses keys to make them smaller!",
            "EXPAND":"Kyber expands a seed into a full random matrix!",
            "MODULE":"Module LWE uses polynomial rings for better efficiency!",
            "DEGREE":"Polynomial degree determines the security level!",
            "ENCAPSULATE":"Key encapsulation wraps a shared secret securely!",
            "DECAPSULATE":"Decapsulation unwraps the shared secret using the private key!",
            "KEYPAIR":"A keypair is a public key plus a matching private key!",
            "CIPHERTEXT":"Ciphertext is the encrypted scrambled version of data!",
            "PLAINTEXT":"Plaintext is the original unencrypted message!",
            "NONCE":"A nonce is a number used only once in crypto operations!",
            "SEED":"A random seed generates the entire key pair in Kyber!",
            "SIGNATURE":"A digital signature proves who sent a message!",
            "VERIFICATION":"Signature verification checks if the signature is genuine!",
            "REJECTION":"Rejection sampling makes Dilithium signatures safe!",
            "SAMPLING":"Sampling from a distribution generates the LWE noise!",
            "COMMITMENT":"A cryptographic commitment hides a value until revealed!",
            "CHALLENGE":"In a proof system a challenge tests the prover!",
            "RESPONSE":"The response proves knowledge without revealing the secret!",
            "TRANSCRIPT":"A proof transcript records the entire proof conversation!",
            "BINDING":"Binding means a commitment cannot be changed after the fact!",
            "POSTQUANTUM":"Post-quantum cryptography is secure against quantum computers!",
            "MIGRATION":"PQC migration means switching from old to quantum-safe crypto!",
            "CRYPTOAGILE":"Crypto-agile systems can switch algorithms quickly!",
            "TRANSITION":"The PQC transition is happening now — NIST approved in 2024!",
            "TIMELINE":"NIST worked from 2016 to 2024 to standardize PQC!",
            "APPROVED":"NIST approved Kyber Dilithium SPHINCS+ and Falcon in 2024!",
            "FEDERAL":"Federal agencies must migrate to PQC by 2035 per NSM-10!",
        }

        # Level selector
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            lvl_names = [f"Level {l['level']} — {l['desc']}" for l in WS_LEVELS]
            sel = st.selectbox("Choose level:", lvl_names, index=st.session_state.ws_level-1, key="ws_lvl_sel")
            st.session_state.ws_level = int(sel.split()[1])
        with col2:
            if st.session_state.ws_level > 1:
                if st.button("← Previous", key="ws_prev"):
                    st.session_state.ws_level -= 1
                    st.rerun()
        with col3:
            if st.session_state.ws_level < 12:
                if st.button("Next →", key="ws_next"):
                    st.session_state.ws_level += 1
                    st.rerun()

        lvl = WS_LEVELS[st.session_state.ws_level - 1]
        words_json = str(lvl["words"]).replace("'", '"')
        facts_entries = ", ".join([f'"{w}": "{WORD_FACTS.get(w, w)}"' for w in lvl["words"]])

        import streamlit.components.v1 as components
        components.html(f"""
<style>
.ws-wrap{{text-align:center;font-family:sans-serif;padding:10px;}}
.ws-grid{{display:inline-grid;grid-template-columns:repeat({lvl["cols"]},28px);gap:2px;margin:8px auto;}}
.ws-cell{{width:28px;height:28px;display:flex;align-items:center;justify-content:center;
font-size:12px;font-weight:bold;border-radius:4px;cursor:pointer;
background:#1e293b;color:#a5b4fc;border:1px solid #334155;user-select:none;}}
.ws-cell.selected{{background:#4f46e5;color:white;}}
.ws-cell.found{{background:#10b981;color:white;}}
.ws-words{{display:flex;flex-wrap:wrap;gap:5px;justify-content:center;margin:6px;}}
.ws-word{{padding:3px 7px;border-radius:5px;font-size:10px;font-weight:bold;
background:#1e293b;color:#a5b4fc;border:1px solid #334155;}}
.ws-word.found{{background:#10b981;color:white;text-decoration:line-through;}}
#ws-msg{{font-size:11px;color:#34d399;min-height:16px;margin:3px;}}
.ws-btn{{padding:5px 10px;border-radius:6px;border:none;cursor:pointer;
background:#4f46e5;color:white;font-size:11px;font-weight:bold;margin:2px;}}
</style>
<div class="ws-wrap">
<div style="font-size:13px;font-weight:bold;color:#a5b4fc;margin-bottom:4px;">
Level {lvl["level"]} — {lvl["desc"]}</div>
<div id="ws-msg">Click letters to spell a word!</div>
<div class="ws-grid" id="wgrid"></div>
<div class="ws-words" id="wlist"></div>
<button class="ws-btn" onclick="resetWS()">New Game</button>
<div id="ws-score" style="font-size:11px;color:#a5b4fc;margin-top:4px;">Found: 0 / {len(lvl["words"])}</div>
</div>
<script>
const WDS = {words_json};
const FACTS = {{{facts_entries}}};
const R={lvl["rows"]},C={lvl["cols"]};
let gr=[],pl=[],sel=[],fd=[];
function resetWS(){{
gr=Array.from({{length:R}},()=>Array(C).fill(""));
pl=[];sel=[];fd=[];placeW();fillW();renderW();renderWL();
document.getElementById("ws-msg").textContent="Click letters to spell a word!";
document.getElementById("ws-score").textContent="Found: 0 / "+WDS.length;
}}
function placeW(){{
const dirs=[{{dr:0,dc:1}},{{dr:1,dc:0}},{{dr:1,dc:1}},{{dr:0,dc:-1}},{{dr:-1,dc:0}}];
WDS.forEach(word=>{{
let t=0;
while(t<300){{t++;
const d=dirs[Math.floor(Math.random()*dirs.length)];
const mr=R-d.dr*(word.length-1),mc=C-d.dc*(word.length-1);
if(mr<=0||mc<=0||mr>R||mc>C)continue;
const r=Math.floor(Math.random()*mr),c=Math.floor(Math.random()*mc);
if(r<0||c<0)continue;
let ok=true;const cs=[];
for(let i=0;i<word.length;i++){{
const nr=r+d.dr*i,nc=c+d.dc*i;
if(nr<0||nc<0||nr>=R||nc>=C){{ok=false;break;}}
if(gr[nr][nc]!==""&&gr[nr][nc]!==word[i]){{ok=false;break;}}
cs.push([nr,nc]);}}
if(ok){{cs.forEach(([nr,nc],i)=>{{gr[nr][nc]=word[i];}});pl.push({{word,cells:cs}});break;}}}}
}});
}}
function fillW(){{
const L="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
for(let r=0;r<R;r++)for(let c=0;c<C;c++)
if(!gr[r][c])gr[r][c]=L[Math.floor(Math.random()*26)];
}}
function renderW(){{
const el=document.getElementById("wgrid");el.innerHTML="";
for(let r=0;r<R;r++)for(let c=0;c<C;c++){{
const cell=document.createElement("div");
cell.className="ws-cell";cell.textContent=gr[r][c];
cell.dataset.r=r;cell.dataset.c=c;
cell.onclick=()=>selC(r,c);el.appendChild(cell);}}
updCS();}}
function selC(r,c){{
const idx=sel.findIndex(s=>s[0]===r&&s[1]===c);
if(idx>=0){{sel=[];}}else{{sel.push([r,c]);chkW();}}
updCS();}}
function chkW(){{
const s=sel.map(([r,c])=>gr[r][c]).join("");
const sr=sel.map(([r,c])=>gr[r][c]).reverse().join("");
const m=pl.find(p=>(p.word===s||p.word===sr)&&!fd.includes(p.word));
if(m){{fd.push(m.word);
m.cells.forEach(([r,c])=>{{
const cell=document.querySelector("[data-r='"+r+"'][data-c='"+c+"']");
if(cell)cell.classList.add("found");}});
sel=[];
const fact=FACTS[m.word]||m.word;
document.getElementById("ws-msg").textContent="Found "+m.word+"! "+fact;
document.getElementById("ws-score").textContent="Found: "+fd.length+" / "+WDS.length;
renderWL();
if(fd.length===WDS.length)document.getElementById("ws-msg").textContent="All words found! PQC expert!";
}}else if(sel.length>=12){{sel=[];}}
updCS();}}
function updCS(){{
document.querySelectorAll(".ws-cell").forEach(cell=>{{
const r=parseInt(cell.dataset.r),c=parseInt(cell.dataset.c);
const isSel=sel.some(([sr,sc])=>sr===r&&sc===c);
const isF=pl.some(p=>fd.includes(p.word)&&p.cells.some(([pr,pc])=>pr===r&&pc===c));
cell.className="ws-cell"+(isF?" found":isSel?" selected":"");
}});}}
function renderWL(){{
document.getElementById("wlist").innerHTML=
WDS.map(w=>"<div class='ws-word"+(fd.includes(w)?" found":"")+"'>"+w+"</div>").join("");}}
resetWS();
</script>
""", height=560)

        # XP reward for completing levels
        if f"ws_complete_{lvl['level']}" not in st.session_state:
            if st.button(f"Mark Level {lvl['level']} Complete! +{lvl['level']*5} XP", key=f"ws_done_{lvl['level']}"):
                st.session_state[f"ws_complete_{lvl['level']}"] = True
                st.session_state.xp += lvl['level'] * 5
                st.success(f"Level {lvl['level']} complete! +{lvl['level']*5} XP earned!")
                if st.session_state.ws_level < 12:
                    st.session_state.ws_level += 1
                    st.rerun()
        else:
            st.success(f"Level {lvl['level']} already completed! +{lvl['level']*5} XP")

    with tab7:
        st.subheader("✏️ PQC Crossword Puzzle — 12 Levels!")
        st.markdown("Fill in the crossword grid! Click a white square and type your answer.")

        if "cw_level" not in st.session_state:
            st.session_state.cw_level = 1

        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            cw_names = [
                "Level 1 — Beginner (4 words)",
                "Level 2 — Beginner (5 words)",
                "Level 3 — Easy (5 words)",
                "Level 4 — Easy (6 words)",
                "Level 5 — Medium (6 words)",
                "Level 6 — Medium (7 words)",
                "Level 7 — Hard (7 words)",
                "Level 8 — Hard (8 words)",
                "Level 9 — Expert (8 words)",
                "Level 10 — Expert (9 words)",
                "Level 11 — Master (9 words)",
                "Level 12 — Master (10 words)",
            ]
            cw_sel = st.selectbox("Choose level:", cw_names, index=st.session_state.cw_level-1, key="cw_lvl_sel")
            st.session_state.cw_level = int(cw_sel.split()[1])
        with col2:
            if st.session_state.cw_level > 1:
                if st.button("← Prev", key="cw_prev"):
                    st.session_state.cw_level -= 1
                    st.rerun()
        with col3:
            if st.session_state.cw_level < 12:
                if st.button("Next →", key="cw_next"):
                    st.session_state.cw_level += 1
                    st.rerun()

        level = st.session_state.cw_level

        import streamlit.components.v1 as components
        # Grid sizes per level (mirrors the JS LEVELS dict)
        _CW_SIZES = {1:7, 2:8, 3:9, 4:10, 5:10, 6:11, 7:12, 8:12, 9:13, 10:13, 11:14, 12:14}
        _sz = _CW_SIZES.get(st.session_state.cw_level, 14)
        _cw_height = 340 + _sz * 36
        components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
body{{margin:0;background:#0f172a;font-family:sans-serif;color:white;padding:8px;}}
.wrap{{max-width:560px;margin:0 auto;}}
.cw-grid{{display:inline-grid;gap:2px;margin:8px auto;}}
.black{{background:#0f172a;}}
.white{{background:#1e293b;border:1px solid #334155;position:relative;
display:flex;align-items:center;justify-content:center;}}
.white input{{width:100%;height:100%;background:transparent;border:none;
text-align:center;font-size:14px;font-weight:bold;color:#a5b4fc;
text-transform:uppercase;outline:none;cursor:pointer;}}
.white input.ok{{color:#10b981;}}
.white input.bad{{color:#ef4444;}}
.cnum{{position:absolute;top:1px;left:2px;font-size:7px;color:#6b7280;line-height:1;}}
.clues{{display:grid;grid-template-columns:1fr 1fr;gap:10px;max-width:540px;
margin:8px auto;text-align:left;}}
.clue-sec h4{{color:#a5b4fc;font-size:12px;margin:0 0 5px;}}
.clue{{font-size:11px;color:#888;margin-bottom:3px;line-height:1.4;}}
.clue strong{{color:#a5b4fc;}}
.btn{{padding:6px 12px;border-radius:6px;border:none;cursor:pointer;
background:#4f46e5;color:white;font-size:11px;font-weight:bold;margin:3px;}}
#msg{{font-size:12px;color:#34d399;min-height:18px;margin:5px;text-align:center;}}
</style>
</head>
<body>
<div class="wrap">
<div id="msg">Click a white square and type your answer!</div>
<div style="text-align:center;background:#111c30;border:1px solid #334155;border-radius:10px;
padding:8px 10px;margin:6px auto;max-width:540px;">
<div style="font-size:11px;color:#a5b4fc;font-weight:bold;margin-bottom:6px;">📋 WORD BANK — find these words!</div>
<div id="word-bank" style="display:flex;flex-wrap:wrap;gap:6px;justify-content:center;"></div>
</div>
<div style="text-align:center">
<div class="cw-grid" id="grid"></div>
</div>
<div style="text-align:center;margin:6px;">
<button class="btn" onclick="checkAll()">Check Answers</button>
<button class="btn" onclick="revealAll()">Reveal All</button>
<button class="btn" onclick="clearAll()">Clear</button>
</div>
<div class="clues" id="clues"></div>
</div>
<script>
const LEVEL = {level};

// Each level: grid layout where each cell is [row,col,letter,clue_num,is_across_start,is_down_start]
// ANS[r][c] = letter or null for black
// NUMS[r+","+c] = clue number

const LEVELS = {{
  1: {{
    size: 7,
    ans: [
      [null,null,null,null,null,null,null],
      [null,"K","Y","B","E","R",null],
      [null,"A",null,null,null,null,null],
      [null,"T",null,null,null,null,null],
      ["C","I","P","H","E","R",null],
      [null,"C",null,null,null,null,null],
      [null,"E",null,null,null,null,null],
    ],
    nums: {{"1,1":"1","4,0":"2"}},
    across: [{{"n":"2","clue":"Keeping messages secret (6)","ans":"CIPHER"}}],
    down:   [{{"n":"1","clue":"NIST key exchange standard ML-KEM (5)","ans":"KYBER"}},{{"n":"1a","clue":"Math grid that stumps quantum computers (7)","ans":"LATTICE","num":"1","col":1}}],
    acrossClues: [{{"n":"2","clue":"Keeping messages secret (6)"}}],
    downClues:   [{{"n":"1","clue":"ML-KEM key standard (5)"}},{{"n":"1","clue":"Quantum-safe math grid (7)","num":"1b"}}],
  }},
  2: {{
    size: 8,
    ans: [
      [null,null,null,null,null,null,null,null],
      [null,"K","Y","B","E","R",null,null],
      [null,"A",null,null,null,null,null,null],
      [null,"T",null,null,null,null,null,null],
      ["C","I","P","H","E","R",null,null],
      [null,"C",null,null,null,null,null,null],
      [null,"E","N","I","S","T",null,null],
      [null,null,null,null,null,null,null,null],
    ],
    nums: {{"1,1":"1","4,0":"4","6,1":"6"}},
    acrossClues: [{{"n":"4","clue":"Keeping messages secret (6)"}},{{"n":"6","clue":"US agency that approved PQC 2024 (4)"}}],
    downClues:   [{{"n":"1","clue":"ML-KEM key standard (5)"}},{{"n":"1","clue":"Quantum-safe math grid (7)","num":"1b"}}],
  }},
  3: {{
    size: 9,
    ans: [
      [null,null,null,null,null,null,null,null,null],
      [null,"K","Y","B","E","R",null,null,null],
      [null,"A",null,null,null,null,null,null,null],
      [null,"T",null,"S","H","O","R",null,null],
      ["C","I","P","H","E","R",null,null,null],
      [null,"C",null,null,null,null,null,null,null],
      [null,"E","N","I","S","T",null,null,null],
      [null,null,null,"H",null,null,null,null,null],
      [null,null,null,"A",null,null,null,null,null],
    ],
    nums: {{"1,1":"1","3,3":"3","4,0":"4","6,1":"6"}},
    acrossClues: [{{"n":"3","clue":"Algorithm that breaks RSA (4)"}},{{"n":"4","clue":"Keeping messages secret (6)"}},{{"n":"6","clue":"US PQC standards agency (4)"}}],
    downClues:   [{{"n":"1","clue":"ML-KEM standard (5)"}},{{"n":"1","clue":"Quantum-safe math grid (7)","num":"1b"}},{{"n":"3","clue":"Creates unique fingerprints (4)","num":"3b"}}],
  }},
  4: {{
    size: 10,
    ans: [
      [null,null,null,null,null,null,null,null,null,null],
      [null,"K","Y","B","E","R",null,null,null,null],
      [null,"A",null,null,null,null,null,null,null,null],
      [null,"T",null,"S","H","O","R",null,null,null],
      ["C","I","P","H","E","R",null,null,null,null],
      [null,"C",null,"A",null,null,null,null,null,null],
      [null,"E","N","I","S","T",null,null,null,null],
      [null,null,null,"S",null,null,null,null,null,null],
      ["H","A","S","H",null,null,null,null,null,null],
      [null,null,null,null,null,null,null,null,null,null],
    ],
    nums: {{"1,1":"1","3,3":"3","4,0":"4","6,1":"6","8,0":"8"}},
    acrossClues: [{{"n":"3","clue":"Quantum algorithm breaking RSA (4)"}},{{"n":"4","clue":"Secret scrambling method (6)"}},{{"n":"6","clue":"US PQC agency (4)"}},{{"n":"8","clue":"Message fingerprint (4)"}}],
    downClues:   [{{"n":"1","clue":"FIPS 203 key standard (5)"}},{{"n":"1","clue":"Quantum-safe grid math (7)","num":"1b"}},{{"n":"3","clue":"FIPS 205 hash signature (6)","num":"3b"}}],
  }},
  5: {{
    size: 10,
    ans: [
      [null,null,null,null,null,null,null,null,null,null],
      [null,"K","Y","B","E","R",null,null,null,null],
      [null,"A",null,null,null,null,null,null,null,null],
      [null,"T",null,"S","H","O","R",null,null,null],
      ["C","I","P","H","E","R",null,null,null,null],
      [null,"C",null,"A",null,null,null,null,null,null],
      [null,"E","N","I","S","T",null,null,null,null],
      ["F","A","L","C","O","N",null,null,null,null],
      ["H","A","S","H",null,null,null,null,null,null],
      [null,null,null,null,null,null,null,null,null,null],
    ],
    nums: {{"1,1":"1","3,3":"3","4,0":"4","6,1":"6","7,0":"7","8,0":"8"}},
    acrossClues: [{{"n":"3","clue":"Quantum RSA breaker (4)"}},{{"n":"4","clue":"Secret scrambling (6)"}},{{"n":"6","clue":"US PQC agency (4)"}},{{"n":"7","clue":"FN-DSA FIPS 206 (6)"}},{{"n":"8","clue":"SHA-3 fingerprint (4)"}}],
    downClues:   [{{"n":"1","clue":"FIPS 203 standard (5)"}},{{"n":"1","clue":"Grid math (7)","num":"1b"}},{{"n":"3","clue":"Hash signature FIPS 205 (6)","num":"3b"}}],
  }},
  6: {{
    size: 11,
    ans: [
      [null,null,null,null,null,null,null,null,null,null,null],
      [null,"K","Y","B","E","R",null,null,null,null,null],
      [null,"A",null,null,null,null,null,null,null,null,null],
      [null,"T",null,"S","H","O","R",null,null,null,null],
      ["C","I","P","H","E","R",null,null,null,null,null],
      [null,"C",null,"A",null,null,null,null,null,null,null],
      [null,"E","N","I","S","T",null,null,null,null,null],
      ["F","A","L","C","O","N",null,null,null,null,null],
      ["H","A","S","H",null,null,null,null,null,null,null],
      [null,null,null,"E",null,null,null,null,null,null,null],
      [null,null,null,"S",null,null,null,null,null,null,null],
    ],
    nums: {{"1,1":"1","3,3":"3","4,0":"4","6,1":"6","7,0":"7","8,0":"8"}},
    acrossClues: [{{"n":"3","clue":"Breaks RSA on quantum (4)"}},{{"n":"4","clue":"Secret scrambling (6)"}},{{"n":"6","clue":"US PQC standards body (4)"}},{{"n":"7","clue":"Smallest quantum-safe signature (6)"}},{{"n":"8","clue":"Message fingerprint (4)"}}],
    downClues:   [{{"n":"1","clue":"FIPS 203 key standard (5)"}},{{"n":"1","clue":"Quantum-safe math grid (7)","num":"1b"}},{{"n":"3","clue":"Hash-based FIPS 205 signature (7)","num":"3b"}}],
  }},
  7: {{
    size: 12,
    ans: [
      [null,null,null,null,null,null,null,null,null,null,null,null],
      [null,"K","Y","B","E","R",null,null,null,null,null,null],
      [null,"A",null,null,null,null,null,null,null,null,null,null],
      [null,"T",null,"S","H","O","R",null,null,null,null,null],
      ["C","I","P","H","E","R",null,null,null,null,null,null],
      [null,"C",null,"A",null,null,null,null,null,null,null,null],
      [null,"E","N","I","S","T",null,null,null,null,null,null],
      ["F","A","L","C","O","N",null,null,null,null,null,null],
      ["H","A","S","H",null,null,null,null,null,null,null,null],
      [null,null,null,"E",null,null,null,null,null,null,null,null],
      ["E","N","C","R","Y","P","T",null,null,null,null,null],
      [null,null,null,"S",null,null,null,null,null,null,null,null],
    ],
    nums: {{"1,1":"1","3,3":"3","4,0":"4","6,1":"6","7,0":"7","8,0":"8","10,0":"10"}},
    acrossClues: [{{"n":"3","clue":"RSA quantum breaker (4)"}},{{"n":"4","clue":"Secret scrambling (6)"}},{{"n":"6","clue":"US PQC agency 2024 (4)"}},{{"n":"7","clue":"FN-DSA compact signature (6)"}},{{"n":"8","clue":"SHA-3 fingerprint (4)"}},{{"n":"10","clue":"Process of scrambling data (7)"}}],
    downClues:   [{{"n":"1","clue":"FIPS 203 (5)"}},{{"n":"1","clue":"LWE grid math (7)","num":"1b"}},{{"n":"3","clue":"SLH-DSA FIPS 205 (7)","num":"3b"}}],
  }},
  8: {{
    size: 12,
    ans: [
      [null,null,null,null,null,null,null,null,null,null,null,null],
      [null,"K","Y","B","E","R",null,null,null,null,null,null],
      [null,"A",null,null,null,null,null,null,null,null,null,null],
      [null,"T",null,"S","H","O","R",null,null,null,null,null],
      ["C","I","P","H","E","R",null,null,null,null,null,null],
      [null,"C",null,"A",null,null,null,null,null,null,null,null],
      [null,"E","N","I","S","T",null,null,null,null,null,null],
      ["F","A","L","C","O","N",null,null,null,null,null,null],
      ["H","A","S","H",null,null,null,null,null,null,null,null],
      [null,null,null,"E",null,null,null,null,null,null,null,null],
      ["E","N","C","R","Y","P","T",null,null,null,null,null],
      ["P","R","I","M","E",null,null,null,null,null,null,null],
    ],
    nums: {{"1,1":"1","3,3":"3","4,0":"4","6,1":"6","7,0":"7","8,0":"8","10,0":"10","11,0":"11"}},
    acrossClues: [{{"n":"3","clue":"RSA quantum breaker (4)"}},{{"n":"4","clue":"Scramble data (6)"}},{{"n":"6","clue":"PQC standards body (4)"}},{{"n":"7","clue":"FIPS 206 compact (6)"}},{{"n":"8","clue":"SHA-3 output (4)"}},{{"n":"10","clue":"Data scrambling process (7)"}},{{"n":"11","clue":"RSA uses these numbers (5)"}}],
    downClues:   [{{"n":"1","clue":"FIPS 203 (5)"}},{{"n":"1","clue":"LWE math grid (7)","num":"1b"}},{{"n":"3","clue":"FIPS 205 hash sig (7)","num":"3b"}}],
  }},
  9: {{
    size: 13,
    ans: [
      [null,null,null,null,null,null,null,null,null,null,null,null,null],
      [null,"K","Y","B","E","R",null,null,null,null,null,null,null],
      [null,"A",null,null,null,null,null,null,null,null,null,null,null],
      [null,"T",null,"S","H","O","R",null,null,null,null,null,null],
      ["C","I","P","H","E","R",null,null,null,null,null,null,null],
      [null,"C",null,"A",null,null,null,null,null,null,null,null,null],
      [null,"E","N","I","S","T",null,null,null,null,null,null,null],
      ["F","A","L","C","O","N",null,null,null,null,null,null,null],
      ["H","A","S","H",null,null,null,null,null,null,null,null,null],
      [null,null,null,"E",null,null,null,null,null,null,null,null,null],
      ["E","N","C","R","Y","P","T",null,null,null,null,null,null],
      ["P","R","I","M","E",null,null,null,null,null,null,null,null],
      ["M","O","D","U","L","A","R",null,null,null,null,null,null],
    ],
    nums: {{"1,1":"1","3,3":"3","4,0":"4","6,1":"6","7,0":"7","8,0":"8","10,0":"10","11,0":"11","12,0":"12"}},
    acrossClues: [{{"n":"3","clue":"RSA quantum breaker (4)"}},{{"n":"4","clue":"Scramble secret data (6)"}},{{"n":"6","clue":"US PQC agency (4)"}},{{"n":"7","clue":"Smallest PQC signature (6)"}},{{"n":"8","clue":"SHA-3 fingerprint (4)"}},{{"n":"10","clue":"Scrambling process (7)"}},{{"n":"11","clue":"RSA foundation numbers (5)"}},{{"n":"12","clue":"Clock math in crypto (7)"}}],
    downClues:   [{{"n":"1","clue":"FIPS 203 (5)"}},{{"n":"1","clue":"LWE grid (7)","num":"1b"}},{{"n":"3","clue":"FIPS 205 hash sig (7)","num":"3b"}}],
  }},
  10: {{
    size: 13,
    ans: [
      [null,null,null,null,null,null,null,null,null,null,null,null,null],
      [null,"K","Y","B","E","R",null,null,null,null,null,null,null],
      [null,"A",null,"F",null,null,null,null,null,null,null,null,null],
      [null,"T",null,"I","P","S",null,null,null,null,null,null,null],
      ["C","I","P","H","E","R",null,null,null,null,null,null,null],
      [null,"C",null,"A",null,null,null,null,null,null,null,null,null],
      [null,"E","N","I","S","T",null,null,null,null,null,null,null],
      ["F","A","L","C","O","N",null,null,null,null,null,null,null],
      ["H","A","S","H",null,null,null,null,null,null,null,null,null],
      [null,null,null,"E",null,null,null,null,null,null,null,null,null],
      ["E","N","C","R","Y","P","T",null,null,null,null,null,null],
      ["P","R","I","M","E",null,null,null,null,null,null,null,null],
      ["M","O","D","U","L","A","R",null,null,null,null,null,null],
    ],
    nums: {{"1,1":"1","3,1":"3f","3,2":"3","4,0":"4","6,1":"6","7,0":"7","8,0":"8","10,0":"10","11,0":"11","12,0":"12"}},
    acrossClues: [{{"n":"3","clue":"Federal standard code (4)"}},{{"n":"4","clue":"Scramble secret data (6)"}},{{"n":"6","clue":"US PQC agency (4)"}},{{"n":"7","clue":"Smallest PQC sig FIPS 206 (6)"}},{{"n":"8","clue":"SHA-3 fingerprint (4)"}},{{"n":"10","clue":"Scrambling process (7)"}},{{"n":"11","clue":"RSA foundation (5)"}},{{"n":"12","clue":"Clock math (7)"}}],
    downClues:   [{{"n":"1","clue":"FIPS 203 (5)"}},{{"n":"1","clue":"LWE grid (7)","num":"1b"}},{{"n":"3","clue":"FIPS 205 hash sig (7)","num":"3b"}}],
  }},
  11: {{
    size: 14,
    ans: [
      [null,null,null,null,null,null,null,null,null,null,null,null,null,null],
      [null,"K","Y","B","E","R",null,null,null,null,null,null,null,null],
      [null,"A",null,"F",null,null,null,null,null,null,null,null,null,null],
      [null,"T",null,"I","P","S",null,null,null,null,null,null,null,null],
      ["C","I","P","H","E","R",null,null,null,null,null,null,null,null],
      [null,"C",null,"A",null,null,null,null,null,null,null,null,null,null],
      [null,"E","N","I","S","T",null,null,null,null,null,null,null,null],
      ["F","A","L","C","O","N",null,null,null,null,null,null,null,null],
      ["H","A","S","H",null,null,null,null,null,null,null,null,null,null],
      [null,null,"L","E",null,null,null,null,null,null,null,null,null,null],
      ["E","N","C","R","Y","P","T",null,null,null,null,null,null,null],
      ["P","R","I","M","E",null,null,null,null,null,null,null,null,null],
      ["M","O","D","U","L","A","R",null,null,null,null,null,null,null],
      [null,null,null,null,null,null,null,null,null,null,null,null,null,null],
    ],
    nums: {{"1,1":"1","3,2":"3","3,3":"3f","4,0":"4","6,1":"6","7,0":"7","8,0":"8","9,2":"9","10,0":"10","11,0":"11","12,0":"12"}},
    acrossClues: [{{"n":"3f","clue":"Federal standard code (4)"}},{{"n":"4","clue":"Scramble secret data (6)"}},{{"n":"6","clue":"US PQC agency (4)"}},{{"n":"7","clue":"Compact FIPS 206 sig (6)"}},{{"n":"8","clue":"SHA-3 fingerprint (4)"}},{{"n":"9","clue":"Learning With Errors short (3)"}},{{"n":"10","clue":"Scrambling process (7)"}},{{"n":"11","clue":"RSA foundation (5)"}},{{"n":"12","clue":"Clock math (7)"}}],
    downClues:   [{{"n":"1","clue":"FIPS 203 (5)"}},{{"n":"1","clue":"LWE grid (7)","num":"1b"}},{{"n":"3","clue":"FIPS 205 hash sig (7)"}},{{"n":"3f","clue":"SHA-3 fingerprint (4)","num":"3fb"}}],
  }},
  12: {{
    size: 14,
    ans: [
      [null,null,null,null,null,null,null,null,null,null,null,null,null,null],
      [null,"K","Y","B","E","R",null,null,null,null,null,null,null,null],
      [null,"A",null,"F",null,"H",null,null,null,null,null,null,null,null],
      [null,"T",null,"I","P","S",null,null,null,null,null,null,null,null],
      ["C","I","P","H","E","R",null,null,null,null,null,null,null,null],
      [null,"C",null,"A",null,"C",null,null,null,null,null,null,null,null],
      [null,"E","N","I","S","T",null,null,null,null,null,null,null,null],
      ["F","A","L","C","O","N",null,null,null,null,null,null,null,null],
      ["H","A","S","H",null,"S",null,null,null,null,null,null,null,null],
      ["G","R","O","V","E","R",null,null,null,null,null,null,null,null],
      ["E","N","C","R","Y","P","T",null,null,null,null,null,null,null],
      ["P","R","I","M","E",null,null,null,null,null,null,null,null,null],
      ["M","O","D","U","L","A","R",null,null,null,null,null,null,null],
      [null,null,null,null,null,null,null,null,null,null,null,null,null,null],
    ],
    nums: {{"1,1":"1","3,2":"3f","3,3":"3","4,0":"4","6,1":"6","7,0":"7","8,0":"8","9,0":"9","10,0":"10","11,0":"11","12,0":"12"}},
    acrossClues: [{{"n":"3","clue":"Federal standard code (4)"}},{{"n":"4","clue":"Scramble secret data (6)"}},{{"n":"6","clue":"US PQC agency (4)"}},{{"n":"7","clue":"FN-DSA FIPS 206 (6)"}},{{"n":"8","clue":"SHA-3 fingerprint (4)"}},{{"n":"9","clue":"Quantum search speedup (6)"}},{{"n":"10","clue":"Scrambling process (7)"}},{{"n":"11","clue":"RSA foundation numbers (5)"}},{{"n":"12","clue":"Clock math in crypto (7)"}}],
    downClues:   [{{"n":"1","clue":"FIPS 203 key standard (5)"}},{{"n":"1","clue":"LWE quantum-safe grid (7)","num":"1b"}},{{"n":"3","clue":"FIPS 205 hash signature (7)"}},{{"n":"3f","clue":"SHA-3 fingerprint (4)"}}],
  }},
}};

const ldata = LEVELS[LEVEL];
// ── Word bank: derive answer words from the grid itself ──
function extractWords() {{
    const words = [], seen = {{}};
    const g = ldata.ans, S = ldata.size;
    // horizontal runs
    for (let r = 0; r < S; r++) {{
        let run = [];
        for (let col = 0; col <= S; col++) {{
            const ch = col < S ? g[r][col] : null;
            if (ch) {{ run.push({{r: r, c: col, ch: ch}}); }}
            else {{
                if (run.length >= 2) {{
                    const w = run.map(x => x.ch).join('');
                    if (!seen[w]) {{ seen[w] = true; words.push({{word: w, cells: run.slice()}}); }}
                }}
                run = [];
            }}
        }}
    }}
    // vertical runs
    for (let col = 0; col < S; col++) {{
        let run = [];
        for (let r = 0; r <= S; r++) {{
            const ch = r < S ? g[r][col] : null;
            if (ch) {{ run.push({{r: r, c: col, ch: ch}}); }}
            else {{
                if (run.length >= 2) {{
                    const w = run.map(x => x.ch).join('');
                    if (!seen[w]) {{ seen[w] = true; words.push({{word: w, cells: run.slice()}}); }}
                }}
                run = [];
            }}
        }}
    }}
    words.sort((a, b) => a.word.localeCompare(b.word));
    return words;
}}
const BANK_WORDS = extractWords();
function renderBank() {{
    const el = document.getElementById('word-bank');
    if (!el) return;
    el.innerHTML = BANK_WORDS.map(function(w, i) {{
        const solved = isWordSolved(w);
        return '<span id="bw-' + i + '" style="padding:5px 12px;border-radius:14px;font-size:14px;' +
            'font-weight:bold;letter-spacing:1px;' +
            (solved
                ? 'background:#05301f;color:#34d399;border:1px solid #10b981;text-decoration:line-through;'
                : 'background:#1e293b;color:#e2e8f0;border:1px solid #475569;') +
            '">' + (solved ? '✓ ' : '') + w.word + '</span>';
    }}).join('');
}}
function isWordSolved(w) {{
    return w.cells.every(function(cell) {{
        const inp = document.querySelector('input[data-r="' + cell.r + '"][data-c="' + cell.c + '"]');
        return inp && inp.value.toUpperCase() === cell.ch;
    }});
}}
const SIZE = ldata.size;
const ANS = ldata.ans;
const NUMS = ldata.nums;

function buildGrid() {{
    const el = document.getElementById("grid");
    el.style.gridTemplateColumns = "repeat("+SIZE+", 34px)";
    el.style.gridTemplateRows = "repeat("+SIZE+", 34px)";
    el.innerHTML = "";
    for(let r=0;r<SIZE;r++) {{
        for(let c=0;c<SIZE;c++) {{
            const div = document.createElement("div");
            if(!ANS[r] || ANS[r][c]===null || ANS[r][c]===undefined) {{
                div.className="black";
                div.style.width="34px";div.style.height="34px";
            }} else {{
                div.className="white";
                div.style.width="34px";div.style.height="34px";
                const key = r+","+c;
                if(NUMS[key]) {{
                    const n=document.createElement("div");
                    n.className="cnum";n.textContent=NUMS[key];
                    div.appendChild(n);
                }}
                const inp=document.createElement("input");
                inp.maxLength=1;inp.dataset.r=r;inp.dataset.c=c;
                inp.dataset.ans=ANS[r][c];
                inp.oninput=e=>{{
                    e.target.value=e.target.value.toUpperCase();
                    e.target.className="";
                }};
                div.appendChild(inp);
            }}
            el.appendChild(div);
        }}
    }}
    buildClues();
}}

function buildClues() {{
    const el = document.getElementById("clues");
    const across = ldata.acrossClues.map(c=>"<div class='clue'><strong>"+c.n+".</strong> "+c.clue+"</div>").join("");
    const down = ldata.downClues.map(c=>"<div class='clue'><strong>"+c.n+".</strong> "+c.clue+"</div>").join("");
    el.innerHTML = "<div class='clue-sec'><h4>ACROSS</h4>"+across+"</div>"+
                   "<div class='clue-sec'><h4>DOWN</h4>"+down+"</div>";
}}

function refreshBank() {{ renderBank(); }}
function checkAll() {{
    refreshBank();
    let ok=0,tot=0;
    document.querySelectorAll(".white input").forEach(inp=>{{
        tot++;
        const val=inp.value.toUpperCase();
        if(val===inp.dataset.ans){{ok++;inp.className="ok";}}
        else if(val){{inp.className="bad";}}
    }});
    const pct=tot>0?Math.round(ok/tot*100):0;
    document.getElementById("msg").textContent=
        ok===tot&&tot>0?"Perfect score! You know your PQC!":ok+"/"+tot+" correct ("+pct+"%)";
}}

function revealAll() {{
    document.querySelectorAll(".white input").forEach(inp=>{{
        inp.value=inp.dataset.ans;inp.className="ok";
    }});
    document.getElementById("msg").textContent="Answers revealed — study them!";
}}

function clearAll() {{
    document.querySelectorAll(".white input").forEach(inp=>{{
        inp.value="";inp.className="";
    }});
    document.getElementById("msg").textContent="Cleared! Try again!";
}}

buildGrid();
renderBank();
document.addEventListener("input",function(e){{if(e.target&&e.target.tagName==="INPUT")renderBank();}});
</script>
</body>
</html>
""", height=_cw_height)

        if f"cw_complete_{level}" not in st.session_state:
            if st.button(f"Mark Level {level} Complete! +{level*8} XP", key=f"cw_done_{level}"):
                st.session_state[f"cw_complete_{level}"] = True
                st.session_state.xp += level * 8
                st.success(f"Level {level} complete! +{level*8} XP earned!")
                if st.session_state.cw_level < 12:
                    st.session_state.cw_level += 1
                    st.rerun()
        else:
            st.success(f"Level {level} already completed! +{level*8} XP")
