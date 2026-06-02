"""
modules/explainers.py
──────────────────────
Animated explainer videos for PQC concepts.
Built with HTML/CSS/JS animations — no external video needed.
"""

import streamlit as st
import streamlit.components.v1 as components


EXPLAINERS = [
    {
        "id": "quantum_threat",
        "title": "🔥 Why Quantum Computers Are a Threat",
        "grade": "All grades",
        "duration": "60 sec",
        "color": "#ef4444",
        "description": "See how a quantum computer breaks RSA encryption using Shor's Algorithm.",
    },
    {
        "id": "kyber_explained",
        "title": "🔐 How Kyber Encryption Works",
        "grade": "Middle + High School",
        "duration": "90 sec",
        "color": "#10b981",
        "description": "Step-by-step animation of Kyber key encapsulation using lattice math.",
    },
    {
        "id": "lattice_math",
        "title": "🏗️ What is Lattice Mathematics?",
        "grade": "All grades",
        "duration": "60 sec",
        "color": "#7c6dfa",
        "description": "Visual explanation of the lattice problem and why quantum computers fail.",
    },
    {
        "id": "hash_functions",
        "title": "🔢 How Hash Functions Work",
        "grade": "Middle + High School",
        "duration": "60 sec",
        "color": "#3b82f6",
        "description": "Watch SHA-3 transform any message into a unique fingerprint.",
    },
]


def render_quantum_threat():
    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0;padding:0;box-sizing:border-box; }
body { background:#0f172a;font-family:sans-serif;color:white;overflow:hidden; }
#stage { width:640px;height:380px;position:relative;margin:0 auto;
    background:linear-gradient(135deg,#0f172a,#1e1b4b);
    border:2px solid #ef4444;border-radius:16px;overflow:hidden; }
.scene { position:absolute;top:0;left:0;width:100%;height:100%;
    display:none;padding:20px; }
.scene.active { display:flex;flex-direction:column;align-items:center;justify-content:center; }
h2 { font-size:1.3rem;color:#f87171;margin-bottom:12px;text-align:center; }
p  { font-size:0.9rem;color:#ccc;text-align:center;line-height:1.6;max-width:500px; }
.emoji-big { font-size:4rem;margin:12px 0; }
.progress { position:absolute;bottom:8px;left:50%;transform:translateX(-50%);
    display:flex;gap:6px; }
.dot { width:8px;height:8px;border-radius:50%;background:#334155;transition:background 0.3s; }
.dot.active { background:#ef4444; }
.nav { position:absolute;bottom:12px;display:flex;gap:10px; }
.nav-btn { padding:6px 14px;border-radius:6px;border:none;cursor:pointer;
    background:#4f46e5;color:white;font-size:12px;font-weight:bold; }

/* RSA animation */
.rsa-demo { display:flex;align-items:center;gap:20px;margin:16px 0; }
.key-box { background:#1e293b;border:2px solid #10b981;border-radius:10px;
    padding:12px 20px;font-size:0.85rem;text-align:center;transition:all 0.5s; }
.key-box.broken { border-color:#ef4444;background:rgba(239,68,68,0.1); }
.arrow { font-size:1.5rem;color:#6b7280; }

/* Qubit animation */
.qubit { width:50px;height:50px;border-radius:50%;border:3px solid #a855f7;
    display:flex;align-items:center;justify-content:center;font-size:1.2rem;
    animation:spin 2s linear infinite; }
@keyframes spin { to { transform:rotate(360deg); } }

/* Number rain */
.num-rain { font-family:monospace;font-size:0.75rem;color:#10b981;
    animation:rain 1s linear infinite; }
@keyframes rain { 0%{opacity:1;transform:translateY(0)} 100%{opacity:0;transform:translateY(40px)} }
</style>
</head>
<body>
<div id="stage">

<!-- Scene 1 -->
<div class="scene active" id="s1">
    <h2>🔐 How RSA Protects Data Today</h2>
    <div class="emoji-big">🏦</div>
    <p>Banks, hospitals, and governments use RSA encryption. It works by multiplying two giant prime numbers together. Even the fastest classical computer would take <strong>millions of years</strong> to crack it.</p>
</div>

<!-- Scene 2 -->
<div class="scene" id="s2">
    <h2>⚛️ Enter the Quantum Computer</h2>
    <div style="display:flex;gap:20px;margin:12px 0;">
        <div class="qubit" style="border-color:#a855f7">0</div>
        <div class="qubit" style="border-color:#3b82f6;animation-delay:0.3s">1</div>
        <div class="qubit" style="border-color:#10b981;animation-delay:0.6s">?</div>
        <div class="qubit" style="border-color:#f59e0b;animation-delay:0.9s">?</div>
    </div>
    <p>A quantum computer uses <strong>qubits</strong> that can be 0 AND 1 at the same time. This lets it try ALL possible answers simultaneously — something classical computers cannot do.</p>
</div>

<!-- Scene 3 -->
<div class="scene" id="s3">
    <h2>💥 Shor's Algorithm Breaks RSA</h2>
    <div class="rsa-demo">
        <div class="key-box" id="rsa-key">RSA-2048<br>🔐 Secure</div>
        <div class="arrow">⚡</div>
        <div style="text-align:center;font-size:0.8rem;color:#a855f7;">Shor's<br>Algorithm</div>
        <div class="arrow">→</div>
        <div class="key-box broken">RSA-2048<br>💀 BROKEN</div>
    </div>
    <p>Shor's Algorithm can factor the large RSA number in <strong>hours</strong> — not millions of years. Every RSA-protected system becomes vulnerable.</p>
</div>

<!-- Scene 4 -->
<div class="scene" id="s4">
    <h2>🛡️ The Solution: Post-Quantum Crypto</h2>
    <div class="emoji-big">🔐</div>
    <p>NIST selected <strong>Kyber, Dilithium, SPHINCS+, and Falcon</strong> as quantum-safe standards in 2024. These use lattice mathematics — a problem quantum computers CANNOT solve efficiently. <br><br>The world is switching now!</p>
</div>

<div class="progress">
    <div class="dot active" id="d1"></div>
    <div class="dot" id="d2"></div>
    <div class="dot" id="d3"></div>
    <div class="dot" id="d4"></div>
</div>

<div class="nav" style="left:12px;">
    <button class="nav-btn" onclick="prevScene()">← Back</button>
</div>
<div class="nav" style="right:12px;">
    <button class="nav-btn" onclick="nextScene()">Next →</button>
</div>

</div>
<script>
let current = 1;
const total = 4;

function showScene(n) {
    document.querySelectorAll('.scene').forEach((s,i) => {
        s.classList.toggle('active', i+1===n);
    });
    document.querySelectorAll('.dot').forEach((d,i) => {
        d.classList.toggle('active', i+1===n);
    });
    current = n;
}

function nextScene() {
    if (current < total) showScene(current+1);
}

function prevScene() {
    if (current > 1) showScene(current-1);
}

// Auto advance every 5 seconds
setInterval(() => {
    if (current < total) nextScene();
}, 5000);
</script>
</body>
</html>
""", height=420)


def render_kyber_explained():
    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0;padding:0;box-sizing:border-box; }
body { background:#0f172a;font-family:sans-serif;color:white; }
#stage { width:640px;height:380px;position:relative;margin:0 auto;
    background:linear-gradient(135deg,#0c2e1e,#0f172a);
    border:2px solid #10b981;border-radius:16px;overflow:hidden; }
.scene { position:absolute;top:0;left:0;width:100%;height:100%;
    display:none;padding:24px; }
.scene.active { display:flex;flex-direction:column;align-items:center;justify-content:center; }
h2 { font-size:1.2rem;color:#34d399;margin-bottom:10px;text-align:center; }
p  { font-size:0.88rem;color:#ccc;text-align:center;line-height:1.6;max-width:520px; }
.emoji-big { font-size:3.5rem;margin:10px 0; }
.step-row { display:flex;align-items:center;gap:12px;margin:10px 0;flex-wrap:wrap;justify-content:center; }
.step-box { background:#1e293b;border:1px solid #10b981;border-radius:8px;
    padding:8px 14px;font-size:0.8rem;text-align:center;min-width:90px; }
.arrow { color:#10b981;font-size:1.2rem; }
.dot-active { background:#10b981; }
.progress { position:absolute;bottom:8px;left:50%;transform:translateX(-50%);display:flex;gap:6px; }
.dot { width:8px;height:8px;border-radius:50%;background:#334155;transition:background 0.3s; }
.nav { position:absolute;bottom:12px;display:flex;gap:10px; }
.nav-btn { padding:6px 14px;border-radius:6px;border:none;cursor:pointer;
    background:#10b981;color:white;font-size:12px;font-weight:bold; }
</style>
</head>
<body>
<div id="stage">

<div class="scene active" id="s1">
    <h2>🔐 What is Key Encapsulation?</h2>
    <div class="emoji-big">🤝</div>
    <p>Alice and Bob want to communicate secretly. They need to agree on a <strong>shared secret key</strong> without anyone listening in being able to figure it out. Kyber does this using lattice math!</p>
</div>

<div class="scene" id="s2">
    <h2>📋 Step 1 — Key Generation</h2>
    <div class="step-row">
        <div class="step-box">Random<br>Seed 🎲</div>
        <div class="arrow">→</div>
        <div class="step-box">Matrix A<br>🏗️</div>
        <div class="arrow">+</div>
        <div class="step-box">Secret s<br>🔒</div>
        <div class="arrow">+</div>
        <div class="step-box">Noise e<br>~</div>
    </div>
    <div class="step-row">
        <div class="arrow" style="font-size:1.5rem">↓</div>
    </div>
    <div class="step-box" style="background:rgba(16,185,129,0.1);border-color:#10b981;min-width:200px;">
        Public Key: b = As + e<br>Private Key: s
    </div>
    <p style="margin-top:10px;font-size:0.82rem;">Bob generates a public and private key pair. The noise <strong>e</strong> hides the secret!</p>
</div>

<div class="scene" id="s3">
    <h2>📦 Step 2 — Encapsulation</h2>
    <div class="step-row">
        <div class="step-box">Bob's<br>Public Key</div>
        <div class="arrow">+</div>
        <div class="step-box">Random<br>Message m</div>
    </div>
    <div class="arrow" style="font-size:1.5rem;margin:6px 0">↓ Kyber Encrypt ↓</div>
    <div class="step-row">
        <div class="step-box" style="background:rgba(16,185,129,0.1)">Ciphertext c<br>📦</div>
        <div class="arrow">+</div>
        <div class="step-box" style="background:rgba(16,185,129,0.1)">Shared Secret K<br>🔑</div>
    </div>
    <p style="margin-top:10px;font-size:0.82rem;">Alice uses Bob's public key to wrap a random message into a ciphertext and derive the shared secret K.</p>
</div>

<div class="scene" id="s4">
    <h2>🔓 Step 3 — Decapsulation</h2>
    <div class="step-row">
        <div class="step-box">Ciphertext c<br>📦</div>
        <div class="arrow">+</div>
        <div class="step-box">Bob's<br>Private Key s</div>
    </div>
    <div class="arrow" style="font-size:1.5rem;margin:6px 0">↓ Kyber Decrypt ↓</div>
    <div class="step-box" style="background:rgba(16,185,129,0.1);min-width:200px;">
        Shared Secret K 🔑 ✅
    </div>
    <p style="margin-top:10px;font-size:0.82rem;">Bob uses his private key to recover the same shared secret K. Now both can encrypt their conversation — quantum safe!</p>
</div>

<div class="progress">
    <div class="dot active" id="d1"></div>
    <div class="dot" id="d2"></div>
    <div class="dot" id="d3"></div>
    <div class="dot" id="d4"></div>
</div>
<div class="nav" style="left:12px;"><button class="nav-btn" onclick="prevScene()">← Back</button></div>
<div class="nav" style="right:12px;"><button class="nav-btn" onclick="nextScene()">Next →</button></div>
</div>
<script>
let current=1;const total=4;
function showScene(n){
    document.querySelectorAll('.scene').forEach((s,i)=>s.classList.toggle('active',i+1===n));
    document.querySelectorAll('.dot').forEach((d,i)=>d.classList.toggle('active',i+1===n));
    current=n;
}
function nextScene(){if(current<total)showScene(current+1);}
function prevScene(){if(current>1)showScene(current-1);}
setInterval(()=>{if(current<total)nextScene();},5000);
</script>
</body>
</html>
""", height=420)


def render_lattice_math():
    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0;padding:0;box-sizing:border-box; }
body { background:#0f172a;font-family:sans-serif;color:white; }
#stage { width:640px;height:380px;position:relative;margin:0 auto;
    background:linear-gradient(135deg,#1a0f2e,#0f172a);
    border:2px solid #7c6dfa;border-radius:16px;overflow:hidden; }
.scene { position:absolute;top:0;left:0;width:100%;height:100%;
    display:none;padding:20px; }
.scene.active { display:flex;flex-direction:column;align-items:center;justify-content:center; }
h2 { font-size:1.2rem;color:#a5b4fc;margin-bottom:10px;text-align:center; }
p  { font-size:0.88rem;color:#ccc;text-align:center;line-height:1.6;max-width:520px; }
canvas { border-radius:8px;margin:10px 0; }
.progress { position:absolute;bottom:8px;left:50%;transform:translateX(-50%);display:flex;gap:6px; }
.dot { width:8px;height:8px;border-radius:50%;background:#334155;transition:background 0.3s; }
.nav { position:absolute;bottom:12px;display:flex;gap:10px; }
.nav-btn { padding:6px 14px;border-radius:6px;border:none;cursor:pointer;
    background:#7c6dfa;color:white;font-size:12px;font-weight:bold; }
</style>
</head>
<body>
<div id="stage">

<div class="scene active" id="s1">
    <h2>🏗️ What is a Lattice?</h2>
    <canvas id="c1" width="300" height="180"></canvas>
    <p>A lattice is a regular grid of points in space. In 2D it looks like graph paper dots. In cryptography we work with lattices in <strong>hundreds or thousands of dimensions!</strong></p>
</div>

<div class="scene" id="s2">
    <h2>🎯 The Closest Vector Problem</h2>
    <canvas id="c2" width="300" height="180"></canvas>
    <p>Given a <strong>target point</strong> (red star) that is NOT on the lattice, find the CLOSEST lattice dot. In 2D this is easy. In 1000 dimensions — even quantum computers fail!</p>
</div>

<div class="scene" id="s3">
    <h2>🌊 Adding Noise — The LWE Problem</h2>
    <canvas id="c3" width="300" height="180"></canvas>
    <p>Learning With Errors adds intentional <strong>noise</strong> to hide a secret. Given noisy equations, find the secret. The noise makes it impossible to reverse — even with a quantum computer!</p>
</div>

<div class="scene" id="s4">
    <h2>🔐 Why Kyber is Quantum-Safe</h2>
    <div style="font-size:3rem;margin:10px 0">🏗️ + 🌊 = 🔐</div>
    <p>Kyber combines the lattice structure with the LWE noise problem. To break Kyber you need to find the secret in a 256-dimensional lattice with noise added. <br><br>Quantum computers have <strong>no known advantage</strong> over classical computers for this problem!</p>
</div>

<div class="progress">
    <div class="dot active" id="d1"></div>
    <div class="dot" id="d2"></div>
    <div class="dot" id="d3"></div>
    <div class="dot" id="d4"></div>
</div>
<div class="nav" style="left:12px;"><button class="nav-btn" onclick="prevScene()">← Back</button></div>
<div class="nav" style="right:12px;"><button class="nav-btn" onclick="nextScene()">Next →</button></div>
</div>
<script>
let current=1;const total=4;
function showScene(n){
    document.querySelectorAll('.scene').forEach((s,i)=>s.classList.toggle('active',i+1===n));
    document.querySelectorAll('.dot').forEach((d,i)=>d.classList.toggle('active',i+1===n));
    current=n;
    drawCanvas(n);
}
function nextScene(){if(current<total)showScene(current+1);}
function prevScene(){if(current>1)showScene(current-1);}

function drawLattice(ctx, w, h, noise=false, target=false) {
    ctx.clearRect(0,0,w,h);
    ctx.fillStyle='#0f172a';
    ctx.fillRect(0,0,w,h);
    const spacing=30;
    const ox=15, oy=15;
    // Draw dots
    for(let x=ox;x<w;x+=spacing){
        for(let y=oy;y<h;y+=spacing){
            let dx=0,dy=0;
            if(noise){dx=(Math.random()-0.5)*8;dy=(Math.random()-0.5)*8;}
            ctx.beginPath();
            ctx.arc(x+dx,y+dy,3,0,Math.PI*2);
            ctx.fillStyle='#7c6dfa';
            ctx.fill();
        }
    }
    if(target){
        // Draw target point
        const tx=w/2+22, ty=h/2-15;
        ctx.beginPath();
        ctx.arc(tx,ty,6,0,Math.PI*2);
        ctx.fillStyle='#ef4444';
        ctx.fill();
        ctx.fillStyle='white';
        ctx.font='14px sans-serif';
        ctx.fillText('★',tx-6,ty+5);
        // Draw line to closest
        const cx2=Math.round(tx/30)*30+ox%30, cy2=Math.round(ty/30)*30+oy%30;
        ctx.beginPath();
        ctx.moveTo(tx,ty);
        ctx.lineTo(cx2,cy2);
        ctx.strokeStyle='#f59e0b';
        ctx.lineWidth=2;
        ctx.setLineDash([4,3]);
        ctx.stroke();
        ctx.setLineDash([]);
    }
}

function drawCanvas(n) {
    if(n===1){const c=document.getElementById('c1');if(c){const x=c.getContext('2d');drawLattice(x,300,180,false,false);}}
    if(n===2){const c=document.getElementById('c2');if(c){const x=c.getContext('2d');drawLattice(x,300,180,false,true);}}
    if(n===3){const c=document.getElementById('c3');if(c){const x=c.getContext('2d');drawLattice(x,300,180,true,false);}}
}

drawCanvas(1);
setInterval(()=>{if(current<total)nextScene();},5000);
</script>
</body>
</html>
""", height=420)


def render_hash_functions():
    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0;padding:0;box-sizing:border-box; }
body { background:#0f172a;font-family:sans-serif;color:white; }
#stage { width:640px;height:380px;position:relative;margin:0 auto;
    background:linear-gradient(135deg,#0c1a2e,#0f172a);
    border:2px solid #3b82f6;border-radius:16px;overflow:hidden; }
.scene { position:absolute;top:0;left:0;width:100%;height:100%;
    display:none;padding:20px; }
.scene.active { display:flex;flex-direction:column;align-items:center;justify-content:center; }
h2 { font-size:1.2rem;color:#60a5fa;margin-bottom:10px;text-align:center; }
p  { font-size:0.88rem;color:#ccc;text-align:center;line-height:1.6;max-width:520px; }
.hash-demo { background:#1e293b;border:1px solid #334155;border-radius:10px;
    padding:12px 16px;font-family:monospace;font-size:0.78rem;color:#10b981;
    word-break:break-all;margin:8px 0;max-width:520px; }
.input-msg { background:#1e1b4b;border:1px solid #4f46e5;border-radius:8px;
    padding:8px 14px;font-size:0.9rem;color:#a5b4fc;margin:6px 0; }
.progress { position:absolute;bottom:8px;left:50%;transform:translateX(-50%);display:flex;gap:6px; }
.dot { width:8px;height:8px;border-radius:50%;background:#334155;transition:background 0.3s; }
.nav { position:absolute;bottom:12px;display:flex;gap:10px; }
.nav-btn { padding:6px 14px;border-radius:6px;border:none;cursor:pointer;
    background:#3b82f6;color:white;font-size:12px;font-weight:bold; }
.changed { color:#ef4444 !important; }
</style>
</head>
<body>
<div id="stage">

<div class="scene active" id="s1">
    <h2>🔢 What is a Hash Function?</h2>
    <div style="font-size:3.5rem;margin:8px 0">📄→🔢</div>
    <p>A hash function takes ANY input — a word, a book, a video — and produces a fixed-size <strong>fingerprint</strong>. SHA-3 always produces exactly 256 bits regardless of input size.</p>
</div>

<div class="scene" id="s2">
    <h2>🔐 One-Way Street</h2>
    <div class="input-msg">Hello World</div>
    <div style="font-size:1.5rem;color:#3b82f6;margin:4px">↓ SHA-3 ↓</div>
    <div class="hash-demo">3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392</div>
    <p>You can compute the hash from the message — but you <strong>cannot reverse it</strong> to get the message from the hash. It is a one-way street!</p>
</div>

<div class="scene" id="s3">
    <h2>🌊 The Avalanche Effect</h2>
    <div class="input-msg">Hello World → <span style="color:#10b981">3338be69...</span></div>
    <div style="margin:6px 0;font-size:0.85rem;color:#888">Change just one letter...</div>
    <div class="input-msg">hello World → <span style="color:#ef4444">7e52c53f...</span></div>
    <p>Changing even <strong>one character</strong> completely changes the entire hash output. This is the <strong>avalanche effect</strong> — essential for cryptographic security!</p>
</div>

<div class="scene" id="s4">
    <h2>🛡️ Why SHA-3 is Quantum Resistant</h2>
    <div style="display:flex;gap:20px;margin:12px 0;align-items:center;">
        <div style="text-align:center;">
            <div style="font-size:2rem">🖥️</div>
            <div style="font-size:0.8rem;color:#888">Classical<br>2^256 tries</div>
        </div>
        <div style="font-size:1.5rem;color:#6b7280">vs</div>
        <div style="text-align:center;">
            <div style="font-size:2rem">⚛️</div>
            <div style="font-size:0.8rem;color:#888">Quantum<br>2^128 tries</div>
        </div>
        <div style="font-size:1.5rem;color:#10b981">→</div>
        <div style="text-align:center;">
            <div style="font-size:2rem">✅</div>
            <div style="font-size:0.8rem;color:#10b981">Still<br>Safe!</div>
        </div>
    </div>
    <p>Grover's Algorithm gives quantum computers a square root speedup against hash functions. SHA-3's 256-bit output drops to 128-bit quantum security — still strong enough! Just use SHA-3-384 or SHA-3-512 for extra safety.</p>
</div>

<div class="progress">
    <div class="dot active" id="d1"></div>
    <div class="dot" id="d2"></div>
    <div class="dot" id="d3"></div>
    <div class="dot" id="d4"></div>
</div>
<div class="nav" style="left:12px;"><button class="nav-btn" onclick="prevScene()">← Back</button></div>
<div class="nav" style="right:12px;"><button class="nav-btn" onclick="nextScene()">Next →</button></div>
</div>
<script>
let current=1;const total=4;
function showScene(n){
    document.querySelectorAll('.scene').forEach((s,i)=>s.classList.toggle('active',i+1===n));
    document.querySelectorAll('.dot').forEach((d,i)=>d.classList.toggle('active',i+1===n));
    current=n;
}
function nextScene(){if(current<total)showScene(current+1);}
function prevScene(){if(current>1)showScene(current-1);}
setInterval(()=>{if(current<total)nextScene();},5000);
</script>
</body>
</html>
""", height=420)


def render_explainers_page():
    st.title("📺 Animated Explainers")
    st.markdown(
        "Watch short animated explainers for every major PQC concept. "
        "Use the arrows to navigate each slide or let it auto-advance!"
    )

    st.markdown("---")

    selected = st.selectbox(
        "Choose an explainer:",
        [e["title"] for e in EXPLAINERS],
        key="explainer_select"
    )

    explainer = next(e for e in EXPLAINERS if e["title"] == selected)
    color = explainer["color"]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"<div style='background:{color}15;border:1px solid {color}40;"
            f"border-radius:8px;padding:6px 12px;text-align:center;"
            f"font-size:0.8rem;color:{color};'>🎓 {explainer['grade']}</div>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"<div style='background:#1e293b;border:1px solid #334155;"
            f"border-radius:8px;padding:6px 12px;text-align:center;"
            f"font-size:0.8rem;color:#888;'>⏱️ {explainer['duration']}</div>",
            unsafe_allow_html=True
        )
    with col3:
        if st.button("✅ Mark Watched! +15 XP", key="mark_watched"):
            watch_key = f"watched_{explainer['id']}"
            if not st.session_state.get(watch_key):
                st.session_state[watch_key] = True
                st.session_state.xp = st.session_state.get("xp", 0) + 15
                st.success("+15 XP!")
                st.rerun()
            else:
                st.info("Already watched!")

    st.markdown(f"*{explainer['description']}*")
    st.markdown("---")

    if explainer["id"] == "quantum_threat":
        render_quantum_threat()
    elif explainer["id"] == "kyber_explained":
        render_kyber_explained()
    elif explainer["id"] == "lattice_math":
        render_lattice_math()
    elif explainer["id"] == "hash_functions":
        render_hash_functions()

    st.markdown("---")
    st.markdown("### 📚 All Explainers")
    for e in EXPLAINERS:
        watched = st.session_state.get(f"watched_{e['id']}", False)
        st.markdown(
            f"{'✅' if watched else '⬜'} **{e['title']}** — {e['description']}"
        )
