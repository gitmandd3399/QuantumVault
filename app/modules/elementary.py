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
""", height={min(400 + lvl["rows"] * 10, 580)})

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
        st.markdown("Fill in the crossword! Each level adds new PQC vocabulary.")

        if "cw_level" not in st.session_state:
            st.session_state.cw_level = 1

        CW_LEVELS = [
            {"level":1, "desc":"Beginner", "clues_across":[("1","NIST key exchange standard (5)","KYBER"),("4","Keeping messages secret (6)","CIPHER")], "clues_down":[("1","Math grid stumping quantum computers (7)","LATTICE"),("2","Type of computer that breaks RSA (7)","QUANTUM")],"grid_size":8},
            {"level":2, "desc":"Easy",     "clues_across":[("1","NIST key exchange standard (5)","KYBER"),("4","US agency that approved PQC (4)","NIST")],   "clues_down":[("1","Math grid stumping quantum computers (7)","LATTICE"),("2","Digital signature algorithm (9)","DILITHIUM")],"grid_size":9},
            {"level":3, "desc":"Easy",     "clues_across":[("1","ML-KEM standard (5)","KYBER"),("3","Unique message fingerprint (4)","HASH"),("5","NIST approved PQC in 2024 (4)","FIPS")], "clues_down":[("1","Lattice math problem (3)","LWE"),("2","Quantum algorithm breaking RSA (4)","SHOR")],"grid_size":9},
            {"level":4, "desc":"Medium",   "clues_across":[("1","ML-KEM FIPS 203 (5)","KYBER"),("4","Keeps data secret (7)","ENCRYPT"),("6","US PQC standards agency (4)","NIST")], "clues_down":[("1","Quantum-safe math grid (7)","LATTICE"),("2","Hash-based signature (7)","SPHINCS")],"grid_size":10},
            {"level":5, "desc":"Medium",   "clues_across":[("1","Key encapsulation standard (5)","KYBER"),("4","Secret scrambling (7)","ENCRYPT"),("6","Quantum speedup algorithm (6)","GROVER")], "clues_down":[("1","Math grid (7)","LATTICE"),("2","Breaks RSA (4)","SHOR"),("3","Signature size unit (3)","BIT")],"grid_size":10},
            {"level":6, "desc":"Medium",   "clues_across":[("1","FIPS 203 standard (5)","KYBER"),("4","Encryption scrambling (7)","ENCRYPT"),("6","Prime number math (7)","MODULAR")], "clues_down":[("1","LWE math structure (7)","LATTICE"),("2","Quantum computer threat (4)","SHOR"),("3","Signature algorithm (9)","DILITHIUM")],"grid_size":11},
            {"level":7, "desc":"Hard",     "clues_across":[("1","ML-KEM (5)","KYBER"),("4","ML-DSA (9)","DILITHIUM"),("7","Secure standard code (4)","FIPS")], "clues_down":[("1","Quantum-safe grid math (7)","LATTICE"),("2","Hash fingerprint (4)","HASH"),("3","Quantum search speedup (6)","GROVER")],"grid_size":11},
            {"level":8, "desc":"Hard",     "clues_across":[("1","FIPS 203 (5)","KYBER"),("4","FIPS 204 (9)","DILITHIUM"),("7","Learning With Errors (3)","LWE")], "clues_down":[("1","Grid math (7)","LATTICE"),("2","Hash-based FIPS 205 (7)","SPHINCS"),("3","Breaking algorithm (4)","SHOR")],"grid_size":12},
            {"level":9, "desc":"Expert",   "clues_across":[("1","Key encapsulation (5)","KYBER"),("4","Digital signature (9)","DILITHIUM"),("7","Federal standard (4)","FIPS"),("9","Secret number (5)","PRIME")], "clues_down":[("1","Lattice problem (7)","LATTICE"),("2","Hash signature (7)","SPHINCS"),("3","Quantum break (4)","SHOR"),("5","Encryption process (7)","ENCRYPT")],"grid_size":12},
            {"level":10,"desc":"Expert",   "clues_across":[("1","ML-KEM (5)","KYBER"),("4","ML-DSA (9)","DILITHIUM"),("7","FIPS number (4)","FIPS"),("9","Number theory (7)","MODULAR")], "clues_down":[("1","Grid math (7)","LATTICE"),("2","SLH-DSA (7)","SPHINCS"),("3","RSA breaker (4)","SHOR"),("5","Message fingerprint (4)","HASH")],"grid_size":13},
            {"level":11,"desc":"Master",   "clues_across":[("1","FIPS 203 (5)","KYBER"),("4","FIPS 204 (9)","DILITHIUM"),("7","Standard code (4)","FIPS"),("9","Arithmetic type (7)","MODULAR"),("11","FN-DSA (6)","FALCON")], "clues_down":[("1","LWE grid (7)","LATTICE"),("2","FIPS 205 (7)","SPHINCS"),("3","Shor target (4)","SHOR"),("5","Data scramble (7)","ENCRYPT")],"grid_size":13},
            {"level":12,"desc":"Master",   "clues_across":[("1","FIPS 203 (5)","KYBER"),("4","FIPS 204 (9)","DILITHIUM"),("7","Standard (4)","FIPS"),("9","Clock math (7)","MODULAR"),("11","FIPS 206 (6)","FALCON"),("13","Secure hash (4)","HASH")], "clues_down":[("1","Quantum-safe grid (7)","LATTICE"),("2","FIPS 205 (7)","SPHINCS"),("3","RSA breaker (4)","SHOR"),("5","Scramble data (7)","ENCRYPT"),("8","LWE short form (3)","LWE")],"grid_size":14},
        ]

        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            cw_names = [f"Level {l['level']} — {l['desc']}" for l in CW_LEVELS]
            cw_sel = st.selectbox("Choose level:", cw_names, index=st.session_state.cw_level-1, key="cw_lvl_sel")
            st.session_state.cw_level = int(cw_sel.split()[1])
        with col2:
            if st.session_state.cw_level > 1:
                if st.button("← Previous", key="cw_prev"):
                    st.session_state.cw_level -= 1
                    st.rerun()
        with col3:
            if st.session_state.cw_level < 12:
                if st.button("Next →", key="cw_next"):
                    st.session_state.cw_level += 1
                    st.rerun()

        lvl = CW_LEVELS[st.session_state.cw_level - 1]
        across_clues = "\n".join([f"{n}. {c}" for n,c,_ in lvl["clues_across"]])
        down_clues = "\n".join([f"{n}. {c}" for n,c,_ in lvl["clues_down"]])
        all_answers = {n: a for n,c,a in lvl["clues_across"] + lvl["clues_down"]}
        answers_json = str(all_answers).replace("'",'"')

        import streamlit.components.v1 as components
        components.html(f"""
<style>
body{{margin:0;background:#0f172a;font-family:sans-serif;color:white;padding:8px;}}
.cw-wrap{{max-width:560px;margin:0 auto;text-align:center;}}
.cw-clues{{display:grid;grid-template-columns:1fr 1fr;gap:12px;max-width:520px;margin:8px auto;text-align:left;}}
.clue-section h4{{color:#a5b4fc;font-size:12px;margin:0 0 6px;}}
.clue{{font-size:11px;color:#888;margin-bottom:4px;line-height:1.4;}}
.clue strong{{color:#a5b4fc;}}
.input-area{{max-width:520px;margin:8px auto;}}
.ans-row{{display:flex;align-items:center;gap:8px;margin:5px 0;}}
.ans-label{{font-size:11px;color:#a5b4fc;font-weight:bold;min-width:60px;}}
.ans-input{{flex:1;background:#1e293b;border:1px solid #334155;border-radius:6px;
color:#a5b4fc;font-size:12px;padding:5px 8px;text-transform:uppercase;outline:none;}}
.ans-input.correct{{border-color:#10b981;color:#10b981;}}
.ans-input.wrong{{border-color:#ef4444;color:#ef4444;}}
.cw-btn{{padding:6px 14px;border-radius:6px;border:none;cursor:pointer;
background:#4f46e5;color:white;font-size:11px;font-weight:bold;margin:3px;}}
#cw-msg{{font-size:12px;color:#34d399;min-height:18px;margin:5px;}}
</style>
<div class="cw-wrap">
<div style="font-size:13px;font-weight:bold;color:#a5b4fc;margin-bottom:6px;">
Level {lvl["level"]} — {lvl["desc"]}</div>
<div id="cw-msg">Type your answers below!</div>
<div class="input-area" id="inputs"></div>
<button class="cw-btn" onclick="checkAll()">Check Answers</button>
<button class="cw-btn" onclick="revealAll()">Reveal All</button>
<div class="cw-clues">
<div class="clue-section">
<h4>ACROSS</h4>
{"".join(f'<div class="clue"><strong>{n}.</strong> {c}</div>' for n,c,_ in lvl["clues_across"])}
</div>
<div class="clue-section">
<h4>DOWN</h4>
{"".join(f'<div class="clue"><strong>{n}.</strong> {c}</div>' for n,c,_ in lvl["clues_down"])}
</div>
</div>
</div>
<script>
const ANSWERS = {answers_json};
const ALL_CLUES = [
{"".join(f'{{num:"{n}",dir:"Across",clue:"{c}",ans:"{a}"}},' for n,c,a in lvl["clues_across"])}
{"".join(f'{{num:"{n}",dir:"Down",clue:"{c}",ans:"{a}"}},' for n,c,a in lvl["clues_down"])}
];
const inputs = document.getElementById("inputs");
ALL_CLUES.forEach(item=>{{
const row=document.createElement("div");row.className="ans-row";
const label=document.createElement("div");label.className="ans-label";
label.textContent=item.num+". "+item.dir+":";
const inp=document.createElement("input");inp.className="ans-input";
inp.maxLength=item.ans.length+2;inp.placeholder=item.ans.length+" letters";
inp.dataset.ans=item.ans;inp.dataset.num=item.num;
row.appendChild(label);row.appendChild(inp);inputs.appendChild(row);
}});
function checkAll(){{
let ok=0,tot=ALL_CLUES.length;
document.querySelectorAll(".ans-input").forEach(inp=>{{
const val=inp.value.toUpperCase().trim();
if(val===inp.dataset.ans){{inp.className="ans-input correct";ok++;}}
else if(val){{inp.className="ans-input wrong";}}
}});
const pct=Math.round(ok/tot*100);
document.getElementById("cw-msg").textContent=
ok===tot?"Perfect! You know your PQC!":ok+"/"+tot+" correct ("+pct+"%) — keep trying!";
}}
function revealAll(){{
document.querySelectorAll(".ans-input").forEach(inp=>{{
inp.value=inp.dataset.ans;inp.className="ans-input correct";
}});
document.getElementById("cw-msg").textContent="Answers revealed — study them for next time!";
}}
</script>
""", height=580)

        if f"cw_complete_{lvl['level']}" not in st.session_state:
            if st.button(f"Mark Level {lvl['level']} Complete! +{lvl['level']*8} XP", key=f"cw_done_{lvl['level']}"):
                st.session_state[f"cw_complete_{lvl['level']}"] = True
                st.session_state.xp += lvl['level'] * 8
                st.success(f"Level {lvl['level']} complete! +{lvl['level']*8} XP earned!")
                if st.session_state.cw_level < 12:
                    st.session_state.cw_level += 1
                    st.rerun()
        else:
            st.success(f"Level {lvl['level']} already completed!")

