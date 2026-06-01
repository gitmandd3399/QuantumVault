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
        st.subheader("🔤 PQC Word Search")
        st.markdown("Find all the PQC words! Click letters in order to spell each word.")
        components.html("""
<style>
.ws-wrap{text-align:center;font-family:sans-serif;padding:10px;}
.ws-grid{display:inline-grid;grid-template-columns:repeat(12,30px);gap:2px;margin:10px auto;}
.ws-cell{width:30px;height:30px;display:flex;align-items:center;justify-content:center;
font-size:13px;font-weight:bold;border-radius:4px;cursor:pointer;
background:#1e293b;color:#a5b4fc;border:1px solid #334155;user-select:none;}
.ws-cell.selected{background:#4f46e5;color:white;}
.ws-cell.found{background:#10b981;color:white;}
.ws-words{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:8px;}
.ws-word{padding:3px 8px;border-radius:6px;font-size:11px;font-weight:bold;
background:#1e293b;color:#a5b4fc;border:1px solid #334155;}
.ws-word.found{background:#10b981;color:white;text-decoration:line-through;}
#ws-msg{font-size:12px;color:#34d399;min-height:18px;margin:4px;}
.ws-btn{padding:5px 12px;border-radius:6px;border:none;cursor:pointer;
background:#4f46e5;color:white;font-size:11px;font-weight:bold;margin:3px;}
</style>
<div class="ws-wrap">
<div id="ws-msg">Click letters to spell a word!</div>
<div class="ws-grid" id="wgrid"></div>
<div class="ws-words" id="wlist"></div>
<button class="ws-btn" onclick="resetWS()">New Game</button>
<div id="ws-score" style="font-size:12px;color:#a5b4fc;margin-top:6px;">Found: 0 / 7</div>
</div>
<script>
const WDS=[
{word:"KYBER",fact:"NIST ML-KEM — quantum-safe key exchange!"},
{word:"LATTICE",fact:"Math grid that stumps quantum computers!"},
{word:"QUANTUM",fact:"Quantum computers can break old locks!"},
{word:"NIST",fact:"US agency that approved PQC standards!"},
{word:"HASH",fact:"SHA-3 creates unique message fingerprints!"},
{word:"CIPHER",fact:"A method of writing secret messages!"},
{word:"FALCON",fact:"Smallest quantum-safe signature algorithm!"},
];
const R=9,C=12;
let gr=[],pl=[],sel=[],fd=[];
function resetWS(){
gr=Array.from({length:R},()=>Array(C).fill(""));
pl=[];sel=[];fd=[];placeW();fillW();renderW();renderWL();
document.getElementById("ws-msg").textContent="Click letters to spell a word!";
document.getElementById("ws-score").textContent="Found: 0 / 7";
}
function placeW(){
const dirs=[{dr:0,dc:1},{dr:1,dc:0},{dr:1,dc:1}];
WDS.forEach(({word})=>{
let t=0;
while(t<200){t++;
const d=dirs[Math.floor(Math.random()*dirs.length)];
const mr=R-d.dr*(word.length-1),mc=C-d.dc*(word.length-1);
if(mr<=0||mc<=0)continue;
const r=Math.floor(Math.random()*mr),c=Math.floor(Math.random()*mc);
let ok=true;const cs=[];
for(let i=0;i<word.length;i++){
const nr=r+d.dr*i,nc=c+d.dc*i;
if(gr[nr][nc]!==""&&gr[nr][nc]!==word[i]){ok=false;break;}
cs.push([nr,nc]);}
if(ok){cs.forEach(([nr,nc],i)=>{gr[nr][nc]=word[i];});pl.push({word,cells:cs});break;}}});
}
function fillW(){
const L="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
for(let r=0;r<R;r++)for(let c=0;c<C;c++)
if(!gr[r][c])gr[r][c]=L[Math.floor(Math.random()*26)];
}
function renderW(){
const el=document.getElementById("wgrid");el.innerHTML="";
for(let r=0;r<R;r++)for(let c=0;c<C;c++){
const cell=document.createElement("div");
cell.className="ws-cell";cell.textContent=gr[r][c];
cell.dataset.r=r;cell.dataset.c=c;
cell.onclick=()=>selC(r,c);el.appendChild(cell);}
updCS();}
function selC(r,c){
const idx=sel.findIndex(s=>s[0]===r&&s[1]===c);
if(idx>=0){sel=[];}else{sel.push([r,c]);chkW();}
updCS();}
function chkW(){
const s=sel.map(([r,c])=>gr[r][c]).join("");
const m=pl.find(p=>p.word===s&&!fd.includes(p.word));
if(m){fd.push(m.word);
m.cells.forEach(([r,c])=>{
const cell=document.querySelector("[data-r='"+r+"'][data-c='"+c+"']");
if(cell)cell.classList.add("found");});
sel=[];
document.getElementById("ws-msg").textContent="Found "+m.word+"! "+m.fact;
document.getElementById("ws-score").textContent="Found: "+fd.length+" / 7";
renderWL();
if(fd.length===WDS.length)document.getElementById("ws-msg").textContent="All found! PQC expert!";}
else if(sel.length>=9){sel=[];}
updCS();}
function updCS(){
document.querySelectorAll(".ws-cell").forEach(cell=>{
const r=parseInt(cell.dataset.r),c=parseInt(cell.dataset.c);
const isSel=sel.some(([sr,sc])=>sr===r&&sc===c);
const isF=pl.some(p=>fd.includes(p.word)&&p.cells.some(([pr,pc])=>pr===r&&pc===c));
cell.className="ws-cell"+(isF?" found":isSel?" selected":"");});}
function renderWL(){
document.getElementById("wlist").innerHTML=
WDS.map(({word})=>"<div class='ws-word"+(fd.includes(word)?" found":"")+"'>"+word+"</div>").join("");}
resetWS();
</script>
""", height=520)

    with tab7:
        st.subheader("✏️ PQC Crossword Puzzle")
        st.markdown("Fill in the crossword using your PQC knowledge!")
        components.html("""
<style>
.cw-wrap{text-align:center;font-family:sans-serif;padding:10px;}
.cw-grid{display:inline-grid;gap:2px;margin:8px auto;
grid-template-columns:repeat(9,34px);grid-template-rows:repeat(8,34px);}
.black{background:#0f172a;width:34px;height:34px;}
.white{background:#1e293b;border:1px solid #334155;width:34px;height:34px;
position:relative;display:flex;align-items:center;justify-content:center;}
.white input{width:26px;height:26px;background:transparent;border:none;
text-align:center;font-size:13px;font-weight:bold;color:#a5b4fc;
text-transform:uppercase;outline:none;}
.white input.ok{color:#10b981;}
.cnum{position:absolute;top:1px;left:2px;font-size:8px;color:#6b7280;line-height:1;}
.cw-clues{display:grid;grid-template-columns:1fr 1fr;gap:12px;
max-width:480px;margin:8px auto;text-align:left;}
.clue{font-size:11px;color:#888;margin-bottom:4px;line-height:1.4;}
.clue strong{color:#a5b4fc;}
.cw-btn{padding:5px 12px;border-radius:6px;border:none;cursor:pointer;
background:#4f46e5;color:white;font-size:11px;font-weight:bold;margin:3px;}
#cw-msg{font-size:12px;color:#34d399;min-height:18px;margin:4px;}
h4{color:#a5b4fc;font-size:12px;margin:0 0 6px;}
</style>
<div class="cw-wrap">
<div id="cw-msg">Type letters in the white boxes!</div>
<div class="cw-grid" id="cwg"></div>
<button class="cw-btn" onclick="chkCW()">Check Answers</button>
<button class="cw-btn" onclick="revCW()">Reveal All</button>
<div class="cw-clues">
<div><h4>ACROSS</h4>
<div class="clue"><strong>1.</strong> NIST key exchange standard (5)</div>
<div class="clue"><strong>4.</strong> Keeping messages secret (6)</div>
<div class="clue"><strong>6.</strong> US agency that approved PQC (4)</div>
</div>
<div><h4>DOWN</h4>
<div class="clue"><strong>1.</strong> Math grid that stumps quantum computers (7)</div>
<div class="clue"><strong>2.</strong> Type of computer that breaks RSA (7)</div>
<div class="clue"><strong>3.</strong> ML-DSA signature algorithm (9)</div>
</div>
</div>
</div>
<script>
const ANS=[
[-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,"K","Y","B","E","R",-1,-1,-1],
[-1,"A",-1,-1,-1,-1,-1,-1,-1],
[-1,"T",-1,"D",-1,-1,-1,-1,-1],
["C","I","P","I","E","R",-1,-1,-1],
[-1,"C",-1,"L",-1,-1,-1,-1,-1],
[-1,"E",-1,"I","N","I","S","T",-1],
[-1,-1,-1,"T",-1,-1,-1,-1,-1],
];
const NMS={"1,1":"1","4,0":"4","6,4":"6"};
let ug=Array.from({length:8},(_,r)=>Array.from({length:9},(_,c)=>ANS[r][c]===-1?-1:""));
function buildCW(){
const el=document.getElementById("cwg");el.innerHTML="";
for(let r=0;r<8;r++)for(let c=0;c<9;c++){
const div=document.createElement("div");
if(ANS[r][c]===-1){div.className="black";}
else{div.className="white";
const k=r+","+c;
if(NMS[k]){const n=document.createElement("div");n.className="cnum";n.textContent=NMS[k];div.appendChild(n);}
const inp=document.createElement("input");inp.maxLength=1;
inp.dataset.r=r;inp.dataset.c=c;inp.value=ug[r][c];
inp.oninput=e=>{ug[r][c]=e.target.value.toUpperCase();e.target.value=e.target.value.toUpperCase();};
div.appendChild(inp);}
el.appendChild(div);}
}
function chkCW(){
let ok=0,tot=0;
for(let r=0;r<8;r++)for(let c=0;c<9;c++){
if(ANS[r][c]!==-1){tot++;
const inp=document.querySelector("input[data-r='"+r+"'][data-c='"+c+"']");
if(inp){if(ug[r][c]===ANS[r][c]){ok++;inp.classList.add("ok");}else inp.classList.remove("ok");}}}
const p=Math.round(ok/tot*100);
document.getElementById("cw-msg").textContent=p===100?"Perfect! You know PQC!":ok+"/"+tot+" correct ("+p+"%)";
}
function revCW(){
for(let r=0;r<8;r++)for(let c=0;c<9;c++){
if(ANS[r][c]!==-1){ug[r][c]=ANS[r][c];
const inp=document.querySelector("input[data-r='"+r+"'][data-c='"+c+"']");
if(inp){inp.value=ANS[r][c];inp.classList.add("ok");}}}
document.getElementById("cw-msg").textContent="Answers revealed!";}
buildCW();
</script>
""", height=580)
