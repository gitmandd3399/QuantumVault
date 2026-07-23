def render_quiz_board():
    """Middle School: Quantum Quiz Board - 5 categories, 25 questions, plus a final wager round."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("\U0001f9e0 Quantum Quiz Board")
    st.markdown(
        "**Pick a category and a point value!** Answer right and bank the points. "
        "Clear all 25 tiles to unlock the **Final Challenge** \u2014 where you wager your points "
        "on one last question. How high can you score?"
    )

    components.html(r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0b1526;font-family:'Segoe UI',system-ui,sans-serif;color:#e2e8f0;padding:10px;}
.wrap{max-width:760px;margin:0 auto;}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;}
.sbox{background:#1a1500;border:2px solid #fbbf24;border-radius:10px;padding:6px 16px;
font-weight:800;color:#fbbf24;font-size:17px;}
.pbox{color:#94a3b8;font-size:12px;}
.brow{display:grid;grid-template-columns:repeat(5,1fr);gap:5px;margin-bottom:5px;}
.cat{background:#1e1b4b;border:1px solid #4f46e5;border-radius:8px;padding:8px 4px;
text-align:center;font-size:11px;font-weight:800;color:#c7d2fe;min-height:52px;
display:flex;align-items:center;justify-content:center;line-height:1.25;}
.tile{background:#111c30;border:1px solid #334155;border-radius:8px;padding:14px 4px;
font-size:19px;font-weight:800;color:#fbbf24;cursor:pointer;transition:.12s;}
.tile:hover{background:#1e293b;border-color:#fbbf24;transform:scale(1.04);}
.tile.done{background:#0a1120;color:#334155;cursor:default;font-size:15px;}
#modal,#finalwrap{display:none;background:#111c30;border:2px solid #4f46e5;
border-radius:14px;padding:16px;}
#mcat{color:#a5b4fc;font-size:12px;font-weight:800;margin-bottom:8px;}
#mq,#fq{font-size:16px;line-height:1.45;margin-bottom:12px;}
.opt{display:block;width:100%;text-align:left;background:#1e293b;border:2px solid #475569;
border-radius:9px;padding:11px 14px;margin-bottom:7px;color:#e2e8f0;font-size:14px;cursor:pointer;}
.opt:hover:enabled{border-color:#a5b4fc;}
.opt.right{background:#05301f;border-color:#10b981;color:#34d399;font-weight:700;}
.opt.wrong{background:#2d0a0a;border-color:#ef4444;color:#f87171;}
#mwhy,#fwhy{display:none;background:#0c1a30;border-left:3px solid #60a5fa;border-radius:6px;
padding:10px 12px;font-size:13px;line-height:1.5;margin-top:8px;}
.ok{color:#34d399;} .no{color:#f87171;}
#mback,.againb,#startf{display:none;width:100%;margin-top:10px;padding:11px;border:none;
border-radius:9px;background:linear-gradient(135deg,#4f46e5,#7c3aed);color:white;
font-weight:800;font-size:14px;cursor:pointer;}
#startf,.againb{display:block;}
#finalwrap h2{color:#fbbf24;font-size:19px;margin-bottom:6px;text-align:center;}
#wagerbox{text-align:center;}
select{padding:8px 12px;border-radius:8px;background:#1e293b;color:#e2e8f0;
border:2px solid #475569;font-size:14px;font-weight:700;margin:8px 0;}
#fdone{display:none;text-align:center;margin-top:12px;}
.bigscore{font-size:34px;font-weight:800;color:#fbbf24;}
.verdict{font-size:17px;font-weight:800;margin:6px 0;}
.sub{color:#94a3b8;font-size:13px;margin-bottom:10px;}
.confp{position:fixed;top:-10px;width:9px;height:9px;border-radius:2px;pointer-events:none;
animation:cf linear forwards;z-index:999;}
@keyframes cf{to{transform:translateY(105vh) rotate(600deg);opacity:0;}}
</style></head><body><div class="wrap">
<div class="top">
  <div class="sbox">&#11088; <span id="sc">0</span> points</div>
  <div class="pbox">Answered: <span id="prog">0 / 25</span></div>
</div>
<div id="board"></div>
<div id="modal">
  <div id="mcat"></div>
  <div id="mq"></div>
  <div id="mopts"></div>
  <div id="mwhy"></div>
  <button id="mback" onclick="backToBoard()">&#8592; Back to the Board</button>
</div>
<div id="finalwrap">
  <h2>&#127942; FINAL CHALLENGE</h2>
  <div id="wagerbox">
    <p style="font-size:14px;color:#94a3b8">You have <b id="fscore" style="color:#fbbf24">0</b> points.<br>
    How many will you risk on the last question?</p>
    <select id="wagerSel"></select><br>
    <button id="startf" onclick="startFinal()">Lock in my wager!</button>
  </div>
  <div id="finalq" style="display:none">
    <div id="fq"></div>
    <div id="fopts"></div>
    <div id="fwhy"></div>
    <div id="fdone"></div>
  </div>
</div>
</div>
<script>

var DATA = {"cats": [{"name": "\ud83d\udd10 Code Basics", "qs": [[100, "Locking a message so it looks like scrambled nonsense is called this.", ["Encryption", "Compression", "Deletion", "Downloading"], 0, "Encryption! Your message goes in as words and comes out as gibberish."], [200, "This is the secret tool that both locks AND unlocks a message.", ["A key", "A mouse", "A screen", "A cable"], 0, "A key! No key, no reading the message."], [300, "A 'hash' is best described as this.", ["A digital fingerprint for data", "A type of password", "A quantum computer", "A kind of cable"], 0, "A fingerprint! Change one letter of the input and the whole hash changes."], [400, "This word means turning a scrambled message back into readable words.", ["Decryption", "Encryption", "Hashing", "Uploading"], 0, "Decryption \u2014 unlocking the message."], [500, "XOR is famous in cryptography because doing it TWICE with the same key does this.", ["Gives you the original message back", "Deletes the message", "Doubles the message", "Turns it into a hash"], 0, "It gives you the original back! XOR is its own undo button."]]}, {"name": "\u269b\ufe0f Quantum Stuff", "qs": [[100, "A quantum bit has this shorter nickname.", ["Qubit", "Quark", "Qubyte", "Quantumite"], 0, "A qubit! Like a bit, but way weirder."], [200, "A qubit can be in this state that a normal bit cannot.", ["Both 0 and 1 at once", "The number 2", "Upside down", "Invisible"], 0, "Superposition \u2014 0 and 1 at the same time, until you measure it."], [300, "When two qubits are linked so measuring one tells you the other, it's called this.", ["Entanglement", "Tangling", "Twinning", "Magnetism"], 0, "Entanglement! Einstein called it 'spooky action at a distance.'"], [400, "This gate puts a qubit into superposition \u2014 the 'coin flip' gate.", ["Hadamard (H)", "Pauli-X", "CNOT", "Measure"], 0, "The Hadamard gate! It spins the coin into the air."], [500, "Doing this to a qubit forces it to pick 0 or 1 and stop being fuzzy.", ["Measuring it", "Shouting at it", "Cooling it", "Copying it"], 0, "Measuring it! The coin lands and superposition is over."]]}, {"name": "\ud83d\udca5 The Big Threat", "qs": [[100, "The quantum algorithm that could break today's internet encryption is named after this person.", ["Peter Shor", "Alan Turing", "Ada Lovelace", "Alice Bob"], 0, "Peter Shor! He published it in 1994."], [200, "Shor's algorithm is dangerous because it can do this fast.", ["Find the prime factors of huge numbers", "Guess passwords", "Delete files", "Send emails"], 0, "Factoring! And RSA's whole security depends on factoring being slow."], [300, "'Harvest now, decrypt later' means bad guys are doing this today.", ["Stealing encrypted data to unlock in the future", "Farming vegetables", "Deleting old files", "Guessing passwords"], 0, "Stealing data now, waiting for quantum computers to crack it later!"], [400, "Grover's algorithm speeds up searching \u2014 but only by this much.", ["Square root (a lot less scary than Shor)", "A million times", "Not at all", "Infinite"], 0, "Square-root speedup. That's why doubling hash sizes beats Grover."], [500, "This is why bigger hash outputs (like SHA3-256) stay safe from Grover.", ["Doubling the size undoes the speedup", "Grover cannot count", "Hashes are magic", "Grover only breaks RSA"], 0, "Double the bits, and Grover's advantage cancels out."]]}, {"name": "\ud83d\udee1\ufe0f The New Heroes", "qs": [[100, "This lattice-based algorithm is the new standard for exchanging keys safely.", ["ML-KEM (Kyber)", "RSA", "MD5", "WiFi"], 0, "ML-KEM, also called Kyber \u2014 FIPS 203."], [200, "This one creates digital signatures that prove a message is really from you.", ["ML-DSA (Dilithium)", "ML-KEM", "SHA-3", "ECC"], 0, "ML-DSA, also called Dilithium \u2014 FIPS 204."], [300, "Falcon's superpower compared to other signature algorithms is this.", ["Really small signatures", "Really big keys", "It is faster than light", "It never works"], 0, "Tiny signatures \u2014 perfect for smartwatches and small devices."], [400, "SPHINCS+ is different because its security is built entirely from this.", ["Hash functions", "Prime numbers", "Curves", "Passwords"], 0, "Hashes only! No fancy math assumptions, just hashing."], [500, "Lattice problems resist quantum attacks because of this.", ["No quantum algorithm gives a big speedup on them", "They are secret", "Quantum computers are slow", "They use huge passwords"], 0, "Quantum computers just do not have a good shortcut for lattices."]]}, {"name": "\ud83c\udf0d In Real Life", "qs": [[100, "The US agency that ran the contest to pick quantum-safe algorithms is called this.", ["NIST", "NASA", "FBI", "NBA"], 0, "NIST \u2014 the National Institute of Standards and Technology."], [200, "NIST announced its first post-quantum standards in this year.", ["2024", "1999", "2010", "2050"], 0, "August 2024 \u2014 FIPS 203, 204, and 205."], [300, "The little lock icon in your browser bar means this is happening.", ["Your connection is encrypted", "The site is closed", "You are logged out", "The page is loading"], 0, "Encryption in action, every time you browse!"], [400, "Companies need years to switch to new encryption mainly because of this.", ["Crypto is built into millions of devices and systems", "It is expensive to buy", "Nobody knows how", "It is illegal"], 0, "It is everywhere \u2014 phones, cars, banks, browsers, chips."], [500, "A 'cryptographically relevant quantum computer' means one that can do this.", ["Actually break real encryption", "Play games fast", "Store lots of files", "Run cold"], 0, "One powerful enough to break real-world crypto. None exists yet!"]]}], "final": {"cat": "\ud83c\udfc6 FINAL CHALLENGE \u2014 Putting It All Together", "q": "A hospital needs to send your X-ray safely to a specialist, AND prove the file really came from that hospital. Which two tools do they need?", "options": ["ML-KEM to lock it, and ML-DSA to sign it", "Two copies of ML-KEM", "Grover's algorithm and a password", "Shor's algorithm and a firewall"], "answer": 0, "why": "ML-KEM protects the key that locks the file, and ML-DSA signs it so you know the sender is real. Locking and proving are two different jobs!"}};
var score = 0, answered = {}, current = null, finalDone = false, wager = 0, correctCount = 0;

function buildBoard() {
    var b = document.getElementById("board");
    var html = '<div class="brow">';
    for (var c = 0; c < DATA.cats.length; c++) {
        html += '<div class="cat">' + DATA.cats[c].name + "</div>";
    }
    html += "</div>";
    for (var r = 0; r < 5; r++) {
        html += '<div class="brow">';
        for (var c = 0; c < DATA.cats.length; c++) {
            var key = c + "-" + r;
            var val = DATA.cats[c].qs[r][0];
            var done = answered[key];
            html += '<button class="tile' + (done ? " done" : "") + '" ' +
                (done ? "disabled" : 'onclick="openQ(' + c + "," + r + ')"') +
                ">" + (done ? "&#10003;" : val) + "</button>";
        }
        html += "</div>";
    }
    b.innerHTML = html;
    document.getElementById("sc").textContent = score;
    var total = DATA.cats.length * 5;
    var n = Object.keys(answered).length;
    document.getElementById("prog").textContent = n + " / " + total;
    if (n === total && !finalDone) { showFinalPrompt(); }
}

function openQ(c, r) {
    var q = DATA.cats[c].qs[r];
    current = { c: c, r: r, val: q[0], answer: q[3], why: q[4] };
    document.getElementById("board").style.display = "none";
    var m = document.getElementById("modal");
    m.style.display = "block";
    document.getElementById("mcat").textContent = DATA.cats[c].name + " - " + q[0] + " points";
    document.getElementById("mq").textContent = q[1];
    var opts = "";
    for (var i = 0; i < q[2].length; i++) {
        opts += '<button class="opt" onclick="answer(' + i + ',this)">' + q[2][i] + "</button>";
    }
    document.getElementById("mopts").innerHTML = opts;
    document.getElementById("mwhy").style.display = "none";
    document.getElementById("mback").style.display = "none";
}

function answer(i, btn) {
    if (!current || current.locked) return;
    current.locked = true;
    var right = i === current.answer;
    var btns = document.querySelectorAll(".opt");
    for (var k = 0; k < btns.length; k++) {
        btns[k].disabled = true;
        if (k === current.answer) { btns[k].classList.add("right"); }
    }
    if (!right) { btn.classList.add("wrong"); }
    else { score += current.val; correctCount++; confetti(); }
    var w = document.getElementById("mwhy");
    w.style.display = "block";
    w.innerHTML = (right ? "<b class='ok'>&#127881; Correct! +" + current.val + "</b><br>"
                         : "<b class='no'>Not quite!</b><br>") + current.why;
    answered[current.c + "-" + current.r] = true;
    document.getElementById("mback").style.display = "block";
}

function backToBoard() {
    document.getElementById("modal").style.display = "none";
    document.getElementById("board").style.display = "block";
    current = null;
    buildBoard();
}

function showFinalPrompt() {
    document.getElementById("board").style.display = "none";
    document.getElementById("finalwrap").style.display = "block";
    document.getElementById("fscore").textContent = score;
    var sel = document.getElementById("wagerSel");
    sel.innerHTML = "";
    var choices = [0, 100, 250, 500];
    if (score > 500) { choices.push(score); }
    for (var i = 0; i < choices.length; i++) {
        if (choices[i] <= score || choices[i] === 0) {
            sel.innerHTML += '<option value="' + choices[i] + '">' + choices[i] + " points</option>";
        }
    }
    if (!sel.innerHTML) { sel.innerHTML = '<option value="0">0 points</option>'; }
}

function startFinal() {
    wager = parseInt(document.getElementById("wagerSel").value, 10) || 0;
    document.getElementById("wagerbox").style.display = "none";
    document.getElementById("finalq").style.display = "block";
    document.getElementById("fq").textContent = DATA.final.q;
    var opts = "";
    for (var i = 0; i < DATA.final.options.length; i++) {
        opts += '<button class="opt" onclick="finalAnswer(' + i + ',this)">' + DATA.final.options[i] + "</button>";
    }
    document.getElementById("fopts").innerHTML = opts;
}

function finalAnswer(i, btn) {
    if (finalDone) return;
    finalDone = true;
    var right = i === DATA.final.answer;
    var btns = document.querySelectorAll("#fopts .opt");
    for (var k = 0; k < btns.length; k++) {
        btns[k].disabled = true;
        if (k === DATA.final.answer) { btns[k].classList.add("right"); }
    }
    if (!right) { btn.classList.add("wrong"); score -= wager; }
    else { score += wager; confetti(); }
    if (score < 0) { score = 0; }
    var w = document.getElementById("fwhy");
    w.style.display = "block";
    w.innerHTML = (right ? "<b class='ok'>&#127881; Correct! +" + wager + "</b><br>"
                         : "<b class='no'>Not this time! -" + wager + "</b><br>") + DATA.final.why;
    var verdict = score >= 5000 ? "&#127942; QUANTUM CHAMPION!"
        : score >= 3000 ? "&#129352; Quantum Expert!"
        : score >= 1500 ? "&#129353; Solid work, agent!"
        : "&#128218; Good start - play again to level up!";
    document.getElementById("fdone").style.display = "block";
    document.getElementById("fdone").innerHTML =
        "<div class='bigscore'>" + score + " points</div>" +
        "<div class='verdict'>" + verdict + "</div>" +
        "<div class='sub'>You got " + correctCount + " of 25 board questions right.</div>" +
        '<button class="againb" onclick="restart()">&#128260; Play Again</button>';
}

function restart() {
    score = 0; answered = {}; current = null; finalDone = false; wager = 0; correctCount = 0;
    document.getElementById("finalwrap").style.display = "none";
    document.getElementById("wagerbox").style.display = "block";
    document.getElementById("finalq").style.display = "none";
    document.getElementById("fwhy").style.display = "none";
    document.getElementById("fdone").style.display = "none";
    document.getElementById("board").style.display = "block";
    buildBoard();
}

function confetti() {
    var c = ["#fbbf24", "#10b981", "#3b82f6", "#8b5cf6", "#ef4444", "#f97316"];
    for (var i = 0; i < 20; i++) {
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

buildBoard();

</script></body></html>
""", height=820, scrolling=True)

    st.caption(
        "\U0001f4a1 **Teacher tip:** Works great on a projector for whole-class play \u2014 "
        "split into two teams and alternate picks. 25 questions plus a wager round runs about 20 minutes."
    )
