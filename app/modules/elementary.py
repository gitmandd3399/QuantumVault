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
    with tab6:
        st.subheader("🔤 PQC Word Search — 12 Levels!")
        st.markdown("Find all the hidden words! Each level gets bigger and harder!")

        if "ws_level" not in st.session_state:
            st.session_state.ws_level = 1

        WS_LEVELS = [
            {"level":1,  "words":["KYBER","HASH","KEY","NIST","SAFE"],                                          "cols":10,"rows":8,  "desc":"Beginner — 5 words"},
            {"level":2,  "words":["KYBER","LATTICE","HASH","NIST","CIPHER"],                                    "cols":10,"rows":8,  "desc":"Easy — 5 words"},
            {"level":3,  "words":["KYBER","LATTICE","QUANTUM","NIST","HASH","FALCON"],                          "cols":12,"rows":9,  "desc":"Easy — 6 words"},
            {"level":4,  "words":["KYBER","LATTICE","QUANTUM","NIST","CIPHER","FALCON","DILITHIUM"],            "cols":12,"rows":9,  "desc":"Medium — 7 words"},
            {"level":5,  "words":["KYBER","LATTICE","QUANTUM","NIST","CIPHER","FALCON","DILITHIUM","HASH"],     "cols":13,"rows":10, "desc":"Medium — 8 words"},
            {"level":6,  "words":["KYBER","LATTICE","QUANTUM","NIST","CIPHER","FALCON","DILITHIUM","ENCRYPT"],  "cols":13,"rows":10, "desc":"Medium — 8 words"},
            {"level":7,  "words":["KYBER","LATTICE","QUANTUM","NIST","CIPHER","FALCON","DILITHIUM","ENCRYPT","SHOR"],"cols":14,"rows":11,"desc":"Hard — 9 words"},
            {"level":8,  "words":["KYBER","LATTICE","QUANTUM","NIST","CIPHER","FALCON","DILITHIUM","ENCRYPT","SHOR","GROVER"],"cols":14,"rows":11,"desc":"Hard — 10 words"},
            {"level":9,  "words":["KYBER","LATTICE","QUANTUM","NIST","CIPHER","FALCON","DILITHIUM","ENCRYPT","SHOR","GROVER","PRIME"],"cols":15,"rows":12,"desc":"Expert — 11 words"},
            {"level":10, "words":["KYBER","LATTICE","QUANTUM","NIST","CIPHER","FALCON","DILITHIUM","ENCRYPT","SHOR","GROVER","PRIME","MODULAR"],"cols":15,"rows":12,"desc":"Expert — 12 words"},
            {"level":11, "words":["KYBER","LATTICE","QUANTUM","NIST","CIPHER","FALCON","DILITHIUM","ENCRYPT","SHOR","GROVER","PRIME","MODULAR","SPHINCS"],"cols":16,"rows":13,"desc":"Master — 13 words"},
            {"level":12, "words":["KYBER","LATTICE","QUANTUM","NIST","CIPHER","FALCON","DILITHIUM","ENCRYPT","SHOR","GROVER","PRIME","MODULAR","SPHINCS","FIPS"],"cols":16,"rows":13,"desc":"Master — 14 words"},
        ]

        WORD_FACTS = {
            "KYBER":"ML-KEM FIPS 203 — quantum-safe key encapsulation!",
            "LATTICE":"Math grid that stumps quantum computers!",
            "QUANTUM":"Quantum computers threaten old crypto!",
            "NIST":"US agency that approved PQC standards!",
            "HASH":"SHA-3 creates unique message fingerprints!",
            "FALCON":"Smallest quantum-safe signature algorithm!",
            "CIPHER":"A method of writing secret messages!",
            "DILITHIUM":"ML-DSA FIPS 204 digital signature standard!",
            "ENCRYPT":"Process of scrambling data to keep it secret!",
            "SHOR":"Shor Algorithm breaks RSA on quantum computers!",
            "GROVER":"Grover Algorithm speeds up quantum search!",
            "PRIME":"Prime numbers are the foundation of RSA!",
            "MODULAR":"Modular arithmetic is the math behind crypto!",
            "SPHINCS":"SLH-DSA FIPS 205 hash-based signature!",
            "FIPS":"Federal Information Processing Standard!",
            "KEY":"Secret information used to lock or unlock data!",
            "SAFE":"Quantum-safe means secure against quantum attacks!",
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

function checkAll() {{
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
</script>
</body>
</html>
""", height=700)

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
