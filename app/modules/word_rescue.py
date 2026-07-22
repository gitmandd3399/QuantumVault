def render_word_rescue():
    """Elementary: Quantum Monster Word Rescue - kid-safe word guessing game with 131 PQC words."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("🦸 Quantum Monster Word Rescue!")
    st.markdown(
        "🚨 **The Quantum Monster is walking to the vault!** "
        "Guess the secret word before it gets there. Pick letters to fill in the blanks. "
        "Every wrong letter lets the monster take one step closer!"
    )

    components.html(r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0b1526;font-family:'Segoe UI',system-ui,sans-serif;color:#e2e8f0;padding:10px;}
.wrap{max-width:640px;margin:0 auto;}
.hud{display:flex;gap:8px;justify-content:center;margin-bottom:10px;flex-wrap:wrap;}
.hb{background:#111c30;border:1px solid #334155;border-radius:10px;padding:6px 14px;font-size:13px;}
.hb b{color:#fbbf24;font-size:16px;}
.tiers{display:flex;gap:6px;justify-content:center;margin-bottom:10px;flex-wrap:wrap;}
.tierb{padding:7px 14px;border-radius:14px;border:2px solid #475569;background:#1e293b;
color:#e2e8f0;font-weight:700;font-size:13px;cursor:pointer;}
.tierb.on{border-color:#fbbf24;background:#1a1500;color:#fbbf24;}
#trackwrap{background:#0a1120;border:1px solid #334155;border-radius:12px;padding:10px;
text-align:center;margin-bottom:8px;}
#track{font-size:26px;letter-spacing:6px;line-height:1.2;}
.step{opacity:.35;}
.vault{opacity:1;}
.mon{animation:wob .6s infinite;display:inline-block;}
@keyframes wob{0%,100%{transform:translateX(0)}50%{transform:translateX(3px)}}
#steps{font-size:12px;color:#f87171;font-weight:700;margin-top:4px;}
#slots{text-align:center;margin:14px 0 8px;line-height:2;}
.slot{display:inline-block;width:30px;height:40px;margin:0 3px;border-bottom:4px solid #475569;
font-size:26px;font-weight:800;color:#a5b4fc;vertical-align:bottom;}
.slot.filled{border-bottom-color:#10b981;color:#34d399;}
#hint{text-align:center;color:#94a3b8;font-size:14px;margin-bottom:10px;font-style:italic;}
#msg{text-align:center;font-size:15px;font-weight:700;color:#fbbf24;min-height:22px;margin-bottom:8px;}
#keys{margin-top:6px;}
.krow{display:flex;justify-content:center;gap:5px;margin-bottom:5px;flex-wrap:wrap;}
.kb{width:40px;height:44px;border-radius:8px;border:2px solid #475569;background:#1e293b;
color:#e2e8f0;font-size:18px;font-weight:800;cursor:pointer;}
.kb:hover{border-color:#a5b4fc;}
.kb.good{background:#05301f;border-color:#10b981;color:#34d399;}
.kb.bad{background:#2d0a0a;border-color:#ef4444;color:#f87171;opacity:.5;}
#nextb{display:none;width:100%;margin-top:12px;padding:12px;border:none;border-radius:10px;
background:linear-gradient(135deg,#4f46e5,#7c3aed);color:white;font-weight:800;font-size:15px;cursor:pointer;}
.confp{position:fixed;top:-10px;width:9px;height:9px;border-radius:2px;pointer-events:none;
animation:cf linear forwards;z-index:999;}
@keyframes cf{to{transform:translateY(105vh) rotate(600deg);opacity:0;}}
</style></head><body><div class="wrap">
<div class="hud">
  <div class="hb">&#11088; Score <b id="sc">0</b></div>
  <div class="hb">&#128293; Streak <b id="st">0</b></div>
  <div class="hb">&#9989; Saved <b id="sv">0</b></div>
</div>
<div class="tiers">
  <button class="tierb on" onclick="setTier(1,this)">&#127793; Easy</button>
  <button class="tierb" onclick="setTier(2,this)">&#127774; Medium</button>
  <button class="tierb" onclick="setTier(3,this)">&#128293; Tricky</button>
</div>
<div id="trackwrap">
  <div id="track"></div>
  <div id="steps"></div>
</div>
<div id="slots"></div>
<div id="hint"></div>
<div id="msg"></div>
<div id="keys"></div>
<button id="nextb" onclick="nextWord()">&#10145;&#65039; Next Word!</button>
</div>
<script>

var WORDS = [{"w": "KEY", "t": 1, "h": "It opens a lock!"}, {"w": "LOCK", "t": 1, "h": "It keeps your stuff safe."}, {"w": "CODE", "t": 1, "h": "Secret writing only friends can read."}, {"w": "SAFE", "t": 1, "h": "Not in any danger."}, {"w": "BIT", "t": 1, "h": "The tiniest piece of computer info."}, {"w": "HASH", "t": 1, "h": "A scrambled fingerprint for data."}, {"w": "DATA", "t": 1, "h": "Info that a computer keeps."}, {"w": "SPY", "t": 1, "h": "Someone who sneaks and watches."}, {"w": "HIDE", "t": 1, "h": "To put something out of sight."}, {"w": "WORD", "t": 1, "h": "Letters that go together."}, {"w": "SEED", "t": 1, "h": "The start of a random number."}, {"w": "GRID", "t": 1, "h": "Rows and rows of dots."}, {"w": "DOTS", "t": 1, "h": "Lots of little round marks."}, {"w": "MATH", "t": 1, "h": "Numbers and number puzzles."}, {"w": "BYTE", "t": 1, "h": "Eight bits stuck together!"}, {"w": "CHIP", "t": 1, "h": "The little brain inside a computer."}, {"w": "FILE", "t": 1, "h": "Where a computer saves your stuff."}, {"w": "HACK", "t": 1, "h": "Sneaking into a computer."}, {"w": "NOTE", "t": 1, "h": "A short little message."}, {"w": "PASS", "t": 1, "h": "Short word for password."}, {"w": "RISK", "t": 1, "h": "A chance something bad happens."}, {"w": "RULE", "t": 1, "h": "Something you must follow."}, {"w": "SEND", "t": 1, "h": "To give it to someone far away."}, {"w": "SIGN", "t": 1, "h": "Your own special mark."}, {"w": "TEST", "t": 1, "h": "A way to check if it works."}, {"w": "TRUE", "t": 1, "h": "Not false!"}, {"w": "WALL", "t": 1, "h": "It blocks things from coming in."}, {"w": "WIFI", "t": 1, "h": "How you go online with no wires."}, {"w": "ZERO", "t": 1, "h": "The number 0."}, {"w": "MASK", "t": 1, "h": "It covers something up."}, {"w": "SWAP", "t": 1, "h": "To trade places."}, {"w": "TRAP", "t": 1, "h": "Something that catches you."}, {"w": "BUGS", "t": 1, "h": "Little problems in a program."}, {"w": "GAME", "t": 1, "h": "Something fun to play!"}, {"w": "KEYS", "t": 1, "h": "More than one key."}, {"w": "MAZE", "t": 1, "h": "A puzzle with twisty paths."}, {"w": "PATH", "t": 1, "h": "The way you go."}, {"w": "SCAN", "t": 1, "h": "To look at something closely."}, {"w": "TEAM", "t": 1, "h": "A group that works together."}, {"w": "WINS", "t": 1, "h": "What you do when you beat the game!"}, {"w": "CIPHER", "t": 2, "h": "Another word for a secret code."}, {"w": "SECRET", "t": 2, "h": "Something only you know."}, {"w": "KYBER", "t": 2, "h": "The new super-lock nobody can break!"}, {"w": "QUBIT", "t": 2, "h": "A quantum bit that can be 0 and 1!"}, {"w": "LOGIN", "t": 2, "h": "How you get into your account."}, {"w": "GUARD", "t": 2, "h": "Someone who keeps things safe."}, {"w": "PROOF", "t": 2, "h": "It shows something is true."}, {"w": "TOKEN", "t": 2, "h": "A special pass to get in."}, {"w": "VAULT", "t": 2, "h": "A super-safe room for treasure."}, {"w": "VIRUS", "t": 2, "h": "A bad computer bug."}, {"w": "NONCE", "t": 2, "h": "A number you use only one time."}, {"w": "NOISE", "t": 2, "h": "Fuzzy static that hides a secret."}, {"w": "PRIME", "t": 2, "h": "A number only 1 and itself divide."}, {"w": "ROBOT", "t": 2, "h": "A machine helper like Byte!"}, {"w": "ROUND", "t": 2, "h": "One turn of mixing things up."}, {"w": "SHIFT", "t": 2, "h": "To slide letters over."}, {"w": "SPACE", "t": 2, "h": "Where all the lattice dots live."}, {"w": "TRUST", "t": 2, "h": "Believing something is safe."}, {"w": "BLOCK", "t": 2, "h": "A chunk of data."}, {"w": "CLOUD", "t": 2, "h": "Computers far, far away."}, {"w": "CRACK", "t": 2, "h": "To break open a secret code."}, {"w": "DIGIT", "t": 2, "h": "One single number."}, {"w": "ENTRY", "t": 2, "h": "Getting inside."}, {"w": "ERROR", "t": 2, "h": "A little mistake."}, {"w": "FALCON", "t": 2, "h": "A tiny signature for tiny gadgets!"}, {"w": "HACKER", "t": 2, "h": "Someone who sneaks into computers."}, {"w": "HIDDEN", "t": 2, "h": "Tucked away where nobody sees."}, {"w": "LOCKED", "t": 2, "h": "Shut tight and safe."}, {"w": "PUZZLE", "t": 2, "h": "A brain teaser to solve."}, {"w": "RANDOM", "t": 2, "h": "Mixed up with no pattern."}, {"w": "SAFETY", "t": 2, "h": "Being kept out of danger."}, {"w": "SECURE", "t": 2, "h": "Locked up nice and safe."}, {"w": "SERVER", "t": 2, "h": "A big computer that saves things."}, {"w": "SIGNAL", "t": 2, "h": "A message sent through the air."}, {"w": "SYSTEM", "t": 2, "h": "All the parts working together."}, {"w": "VECTOR", "t": 2, "h": "An arrow that points somewhere."}, {"w": "BINARY", "t": 2, "h": "Counting with just 0 and 1."}, {"w": "DECODE", "t": 2, "h": "To turn a secret back into words."}, {"w": "ENCODE", "t": 2, "h": "To turn words into a secret."}, {"w": "MODULE", "t": 2, "h": "One piece of a bigger thing."}, {"w": "SHIELD", "t": 2, "h": "It blocks attacks!"}, {"w": "ATTACK", "t": 2, "h": "When a bad guy tries to break in."}, {"w": "DEFEND", "t": 2, "h": "To keep something safe."}, {"w": "PUBLIC", "t": 2, "h": "Everybody can see it."}, {"w": "SEARCH", "t": 2, "h": "To look and look for something."}, {"w": "SECRETS", "t": 2, "h": "More than one secret!"}, {"w": "QUANTUM", "t": 3, "h": "A super-fast new kind of computer."}, {"w": "ENCRYPT", "t": 3, "h": "To lock up a message."}, {"w": "DECRYPT", "t": 3, "h": "To unlock a message and read it."}, {"w": "LATTICE", "t": 3, "h": "A giant grid of dots with a secret inside."}, {"w": "NETWORK", "t": 3, "h": "Computers all connected together."}, {"w": "PRIVACY", "t": 3, "h": "Keeping your own stuff to yourself."}, {"w": "PROTECT", "t": 3, "h": "To keep something safe from harm."}, {"w": "SECURITY", "t": 3, "h": "Everything that keeps you safe."}, {"w": "PASSWORD", "t": 3, "h": "The secret word that lets you in."}, {"w": "FIREWALL", "t": 3, "h": "A computer guard at the door."}, {"w": "DILITHIUM", "t": 3, "h": "A strong lock that signs your name!"}, {"w": "SPHINCS", "t": 3, "h": "A safe lock built from math trees."}, {"w": "ALGORITHM", "t": 3, "h": "A recipe of steps for a computer."}, {"w": "COMPUTER", "t": 3, "h": "A machine that does math super fast."}, {"w": "INTERNET", "t": 3, "h": "How all the computers talk."}, {"w": "MESSAGE", "t": 3, "h": "Something you send to a friend."}, {"w": "SIGNATURE", "t": 3, "h": "Your special mark that proves it's you."}, {"w": "KEYPAIR", "t": 3, "h": "Two keys that work together."}, {"w": "SCRAMBLE", "t": 3, "h": "To mix it all up."}, {"w": "DIGITAL", "t": 3, "h": "Made of 0s and 1s."}, {"w": "MACHINE", "t": 3, "h": "A thing built to do a job."}, {"w": "PATTERN", "t": 3, "h": "Something that repeats."}, {"w": "PROBLEM", "t": 3, "h": "A puzzle that needs solving."}, {"w": "PROGRAM", "t": 3, "h": "A list of steps for a computer."}, {"w": "PROTOCOL", "t": 3, "h": "The rules for talking safely."}, {"w": "SHUFFLE", "t": 3, "h": "To mix up the order."}, {"w": "SOLUTION", "t": 3, "h": "The answer to a puzzle."}, {"w": "STANDARD", "t": 3, "h": "The rule everyone agrees to use."}, {"w": "STRENGTH", "t": 3, "h": "How strong something is."}, {"w": "TRAPDOOR", "t": 3, "h": "Easy one way, super hard the other!"}, {"w": "UNLOCKED", "t": 3, "h": "Opened up, not locked."}, {"w": "SCIENTIST", "t": 3, "h": "A person who studies and discovers."}, {"w": "CHALLENGE", "t": 3, "h": "A hard task to try!"}, {"w": "ENCRYPTED", "t": 3, "h": "All locked up and safe."}, {"w": "PLAINTEXT", "t": 3, "h": "A message before it gets locked."}, {"w": "CIPHERTEXT", "t": 3, "h": "A message after it gets locked."}, {"w": "CRYPTOGRAPHY", "t": 3, "h": "The science of secret codes!"}, {"w": "HARDWARE", "t": 3, "h": "The parts you can touch."}, {"w": "SOFTWARE", "t": 3, "h": "The programs inside a computer."}, {"w": "PARTICLE", "t": 3, "h": "A teeny tiny bit of stuff."}, {"w": "DISCOVER", "t": 3, "h": "To find something new."}, {"w": "EXPLORER", "t": 3, "h": "Someone who goes and finds things."}, {"w": "QUANTUMSAFE", "t": 3, "h": "Safe even from a quantum computer!"}, {"w": "SUPERLOCK", "t": 3, "h": "A lock nobody can ever break."}, {"w": "CODEBREAKER", "t": 3, "h": "Someone who cracks secret codes."}];
var tier = 1, word = "", hint = "", guessed = [], wrong = 0, score = 0, streak = 0, solved = 0;
var MAX_WRONG = 6;
var used = {};

function pool() {
    var p = WORDS.filter(function(x) { return x.t === tier; });
    var fresh = p.filter(function(x) { return !used[x.w]; });
    if (fresh.length === 0) { p.forEach(function(x) { delete used[x.w]; }); fresh = p; }
    return fresh;
}

function newWord() {
    var p = pool();
    var pick = p[Math.floor(Math.random() * p.length)];
    word = pick.w; hint = pick.h; used[word] = true;
    guessed = []; wrong = 0;
    render();
    setMsg("Pick a letter to start!");
}

function setTier(t, el) {
    tier = t;
    var btns = document.querySelectorAll(".tierb");
    for (var i = 0; i < btns.length; i++) { btns[i].classList.remove("on"); }
    el.classList.add("on");
    newWord();
}

function setMsg(m) { document.getElementById("msg").textContent = m; }

function guess(letter, btn) {
    if (guessed.indexOf(letter) !== -1) return;
    if (wrong >= MAX_WRONG) return;
    if (isWon()) return;
    guessed.push(letter);
    if (word.indexOf(letter) === -1) {
        wrong++;
        btn.classList.add("bad");
        setMsg("Nope! The monster steps closer.");
    } else {
        btn.classList.add("good");
        setMsg("Yes! Keep going!");
    }
    render();
    if (isWon()) { win(); }
    else if (wrong >= MAX_WRONG) { lose(); }
}

function isWon() {
    if (!word) return false;
    for (var i = 0; i < word.length; i++) {
        if (guessed.indexOf(word[i]) === -1) return false;
    }
    return true;
}

function win() {
    solved++;
    streak++;
    var pts = 10 + (MAX_WRONG - wrong) * 5 + (streak - 1) * 5;
    score += pts;
    setMsg("YOU SAVED THE VAULT! +" + pts + " points");
    confetti();
    document.getElementById("nextb").style.display = "block";
    render();
}

function lose() {
    streak = 0;
    setMsg("The monster reached the vault! The word was: " + word);
    document.getElementById("nextb").style.display = "block";
    render();
}

function render() {
    // word slots
    var slots = "";
    for (var i = 0; i < word.length; i++) {
        var ch = word[i];
        var show = guessed.indexOf(ch) !== -1 || wrong >= MAX_WRONG;
        slots += '<span class="slot' + (show ? " filled" : "") + '">' + (show ? ch : "") + "</span>";
    }
    document.getElementById("slots").innerHTML = slots;
    document.getElementById("hint").textContent = "Clue: " + hint;
    document.getElementById("sc").textContent = score;
    document.getElementById("st").textContent = streak;
    document.getElementById("sv").textContent = solved;
    // monster track: 7 positions, monster starts far left
    var track = "";
    for (var p = 0; p <= MAX_WRONG; p++) {
        if (p === wrong) { track += '<span class="mon">&#128126;</span>'; }
        else if (p === MAX_WRONG) { track += '<span class="step vault">&#128274;</span>'; }
        else { track += '<span class="step">&#183;</span>'; }
    }
    if (wrong < MAX_WRONG) { track += '<span class="step vault">&#128274;</span>'; }
    document.getElementById("track").innerHTML = track;
    var left = MAX_WRONG - wrong;
    document.getElementById("steps").textContent = left + " step" + (left === 1 ? "" : "s") + " away!";
}

function buildKeys() {
    var kb = document.getElementById("keys");
    var rows = ["ABCDEFGHI", "JKLMNOPQR", "STUVWXYZ"];
    var html = "";
    for (var r = 0; r < rows.length; r++) {
        html += '<div class="krow">';
        for (var i = 0; i < rows[r].length; i++) {
            var L = rows[r][i];
            html += '<button class="kb" id="k-' + L + '" onclick="guess(\'' + L + '\',this)">' + L + "</button>";
        }
        html += "</div>";
    }
    kb.innerHTML = html;
}

function nextWord() {
    document.getElementById("nextb").style.display = "none";
    var ks = document.querySelectorAll(".kb");
    for (var i = 0; i < ks.length; i++) { ks[i].classList.remove("good", "bad"); }
    newWord();
}

function confetti() {
    var c = ["#fbbf24", "#10b981", "#3b82f6", "#8b5cf6", "#ef4444", "#f97316"];
    for (var i = 0; i < 24; i++) {
        (function(n) {
            setTimeout(function() {
                var el = document.createElement("div");
                el.className = "confp";
                el.style.left = Math.random() * 100 + "vw";
                el.style.background = c[Math.floor(Math.random() * c.length)];
                el.style.animationDuration = (1 + Math.random() * 2) + "s";
                document.body.appendChild(el);
                setTimeout(function() { el.remove(); }, 3000);
            }, n * 40);
        })(i);
    }
}

buildKeys();
newWord();

</script></body></html>
""", height=760, scrolling=True)

    st.caption(
        "💡 **Tip for grown-ups:** Start on Easy (short words) for K-2, "
        "Medium for 2nd-3rd, and Tricky for 4th-5th. There are 131 words in all!"
    )
