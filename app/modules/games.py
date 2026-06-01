"""
modules/games.py
────────────────
PQC Mini Games — one per grade level.
All games built with HTML/JS embedded via st.components.v1.html()
"""

import streamlit as st
import streamlit.components.v1 as components
from utils.security import sanitize_input


def render_falling_blocks():
    """K-5: Falling Blocks — catch quantum-safe locks, avoid broken ones."""
    st.subheader("🧱 Quantum Lock Drop!")
    st.markdown(
        "Catch the **quantum-safe locks** 🔐 and avoid the **broken locks** 💀 "
        "Use ← → arrow keys or tap the buttons to move your basket!"
    )

    components.html("""
    <style>
        #gameCanvas { border: 2px solid #4f46e5; border-radius: 12px; display: block; margin: 0 auto; background: #0f172a; }
        .game-wrap { text-align: center; font-family: sans-serif; }
        .score-bar { display: flex; justify-content: space-between; max-width: 400px; margin: 8px auto; color: #a5b4fc; font-size: 14px; font-weight: bold; }
        .btn-row { display: flex; justify-content: center; gap: 16px; margin: 10px; }
        .btn { padding: 10px 28px; border-radius: 8px; border: none; cursor: pointer; font-size: 18px; font-weight: bold; background: #4f46e5; color: white; }
        .btn:active { background: #3730a3; }
        #msg { font-size: 15px; color: #34d399; min-height: 22px; margin: 4px; }
    </style>
    <div class="game-wrap">
        <div class="score-bar">
            <span>⭐ Score: <span id="score">0</span></span>
            <span>❤️ Lives: <span id="lives">3</span></span>
            <span>Level: <span id="level">1</span></span>
        </div>
        <canvas id="gameCanvas" width="400" height="480"></canvas>
        <div id="msg"></div>
        <div class="btn-row">
            <button class="btn" onclick="moveLeft()">◀</button>
            <button class="btn" onclick="startGame()" id="startBtn">▶ Start</button>
            <button class="btn" onclick="moveRight()">▶</button>
        </div>
    </div>
    <script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    const SAFE = [
        {label:'Kyber🔐', color:'#10b981', safe:true},
        {label:'Dilithium🛡️', color:'#3b82f6', safe:true},
        {label:'SPHINCS+✅', color:'#8b5cf6', safe:true},
        {label:'Lattice🏗️', color:'#06b6d4', safe:true},
    ];
    const UNSAFE = [
        {label:'RSA💀', color:'#ef4444', safe:false},
        {label:'ECC☠️', color:'#f97316', safe:false},
        {label:'DES⚠️', color:'#eab308', safe:false},
    ];

    let basket = {x: 160, y: 440, w: 80, h: 20, speed: 28};
    let blocks = [];
    let score = 0, lives = 3, level = 1, running = false;
    let frameCount = 0, dropRate = 90;

    function startGame() {
        score = 0; lives = 3; level = 1;
        blocks = []; running = true; frameCount = 0; dropRate = 90;
        basket.x = 160;
        document.getElementById('startBtn').textContent = '🔄 Restart';
        document.getElementById('msg').textContent = '';
        loop();
    }

    function spawnBlock() {
        const pool = Math.random() < 0.55 ? SAFE : UNSAFE;
        const type = pool[Math.floor(Math.random() * pool.length)];
        blocks.push({
            x: Math.floor(Math.random() * 340) + 10,
            y: -30, w: 72, h: 32,
            speed: 2 + level * 0.5,
            label: type.label, color: type.color, safe: type.safe
        });
    }

    function moveLeft()  { basket.x = Math.max(0, basket.x - basket.speed); }
    function moveRight() { basket.x = Math.min(canvas.width - basket.w, basket.x + basket.speed); }

    document.addEventListener('keydown', e => {
        if (e.key === 'ArrowLeft')  moveLeft();
        if (e.key === 'ArrowRight') moveRight();
    });

    function loop() {
        if (!running) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Background grid
        ctx.strokeStyle = 'rgba(79,70,229,0.08)';
        for (let i = 0; i < canvas.width; i += 40) {
            ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke();
        }
        for (let i = 0; i < canvas.height; i += 40) {
            ctx.beginPath(); ctx.moveTo(0,i); ctx.lineTo(canvas.width,i); ctx.stroke();
        }

        frameCount++;
        if (frameCount % dropRate === 0) {
            spawnBlock();
            if (frameCount % (dropRate * 5) === 0 && dropRate > 40) dropRate -= 5;
        }

        // Draw basket
        ctx.fillStyle = '#4f46e5';
        ctx.beginPath();
        ctx.roundRect(basket.x, basket.y, basket.w, basket.h, 6);
        ctx.fill();
        ctx.fillStyle = 'white';
        ctx.font = 'bold 11px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('🧺 AGENT', basket.x + basket.w/2, basket.y + 14);

        // Update and draw blocks
        blocks = blocks.filter(b => {
            b.y += b.speed;

            // Collision with basket
            if (b.y + b.h >= basket.y && b.y <= basket.y + basket.h &&
                b.x + b.w >= basket.x && b.x <= basket.x + basket.w) {
                if (b.safe) {
                    score += 10 * level;
                    level = Math.floor(score / 100) + 1;
                    document.getElementById('msg').textContent = '✅ +' + (10*level) + ' Quantum Safe!';
                } else {
                    lives--;
                    document.getElementById('msg').textContent = '💀 Ouch! ' + b.label + ' is NOT quantum safe!';
                    if (lives <= 0) {
                        running = false;
                        ctx.fillStyle = 'rgba(0,0,0,0.75)';
                        ctx.fillRect(0,0,canvas.width,canvas.height);
                        ctx.fillStyle = '#f87171';
                        ctx.font = 'bold 28px sans-serif';
                        ctx.textAlign = 'center';
                        ctx.fillText('GAME OVER', canvas.width/2, 200);
                        ctx.fillStyle = 'white';
                        ctx.font = '18px sans-serif';
                        ctx.fillText('Score: ' + score, canvas.width/2, 240);
                        ctx.fillText('Kyber & Lattice = Quantum Safe!', canvas.width/2, 280);
                        document.getElementById('startBtn').textContent = '▶ Play Again';
                        return false;
                    }
                }
                return false;
            }

            if (b.y > canvas.height) {
                if (b.safe) {
                    lives--;
                    document.getElementById('msg').textContent = '⚠️ Missed a safe lock!';
                    if (lives <= 0) { running = false; }
                }
                return false;
            }

            // Draw block
            ctx.fillStyle = b.color;
            ctx.beginPath();
            ctx.roundRect(b.x, b.y, b.w, b.h, 6);
            ctx.fill();
            ctx.fillStyle = 'white';
            ctx.font = 'bold 10px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(b.label, b.x + b.w/2, b.y + 21);
            return true;
        });

        document.getElementById('score').textContent = score;
        document.getElementById('lives').textContent = '❤️'.repeat(Math.max(0,lives));
        document.getElementById('level').textContent = level;

        requestAnimationFrame(loop);
    }

    // Draw idle screen
    ctx.fillStyle = '#1e1b4b';
    ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle = '#a5b4fc';
    ctx.font = 'bold 20px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('🔐 Quantum Lock Drop', canvas.width/2, 200);
    ctx.font = '14px sans-serif';
    ctx.fillText('Catch quantum-safe locks!', canvas.width/2, 240);
    ctx.fillText('Press ▶ Start to play', canvas.width/2, 270);
    </script>
    """, height=600)


def render_lattice_maze():
    """6-8: Lattice Maze — navigate grid avoiding quantum attackers."""
    st.subheader("🌀 Lattice Maze Escape!")
    st.markdown(
        "Navigate the **lattice grid** to reach the 🔐 Kyber Key! "
        "Avoid the ☠️ quantum attackers. Use arrow keys or WASD to move."
    )

    components.html("""
    <style>
        #mazeCanvas { border: 2px solid #4f46e5; border-radius: 12px; display: block; margin: 0 auto; background: #0f172a; }
        .maze-wrap { text-align: center; font-family: sans-serif; }
        .maze-score { display: flex; justify-content: space-between; max-width: 420px; margin: 8px auto; color: #a5b4fc; font-size: 13px; font-weight: bold; }
        #maze-msg { font-size: 14px; color: #34d399; min-height: 20px; margin: 4px; }
        .maze-btn { padding: 8px 20px; border-radius: 8px; border: none; cursor: pointer; font-size: 14px; font-weight: bold; background: #4f46e5; color: white; margin: 4px; }
    </style>
    <div class="maze-wrap">
        <div class="maze-score">
            <span>⭐ Score: <span id="mscore">0</span></span>
            <span>❤️ Lives: <span id="mlives">3</span></span>
            <span>🔑 Keys: <span id="mkeys">0</span>/3</span>
        </div>
        <canvas id="mazeCanvas" width="420" height="420"></canvas>
        <div id="maze-msg">Press Start to play!</div>
        <button class="maze-btn" onclick="startMaze()">▶ Start</button>
        <button class="maze-btn" onclick="mazeUp()">▲</button>
        <button class="maze-btn" onclick="mazeDown()">▼</button>
        <button class="maze-btn" onclick="mazeLeft()">◀</button>
        <button class="maze-btn" onclick="mazeRight()">▶</button>
    </div>
    <script>
    const mc = document.getElementById('mazeCanvas');
    const mx = mc.getContext('2d');
    const CELL = 42, COLS = 10, ROWS = 10;

    let player, enemies, keys, score, lives, running, collected;

    // Simple maze walls — 1 = wall, 0 = open
    const MAZE = [
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,0,0,0,0,1],
        [1,0,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,1,0,1],
        [1,0,1,1,1,1,0,1,0,1],
        [1,0,0,0,0,1,0,0,0,1],
        [1,1,1,0,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,1,1,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1],
    ];

    function startMaze() {
        player = {x:1, y:1};
        enemies = [{x:8,y:1,dx:0,dy:1},{x:1,y:7,dx:1,dy:0}];
        keys = [{x:3,y:3,collected:false},{x:7,y:5,collected:false},{x:5,y:8,collected:false}];
        score = 0; lives = 3; running = true; collected = 0;
        document.getElementById('maze-msg').textContent = 'Collect all 3 Kyber Keys!';
        drawMaze();
        setInterval(moveEnemies, 700);
    }

    function canMove(x, y) {
        return x >= 0 && y >= 0 && x < COLS && y < ROWS && MAZE[y][x] === 0;
    }

    function mazeUp()    { if(running && canMove(player.x, player.y-1)) { player.y--; checkCollect(); checkEnemy(); drawMaze(); }}
    function mazeDown()  { if(running && canMove(player.x, player.y+1)) { player.y++; checkCollect(); checkEnemy(); drawMaze(); }}
    function mazeLeft()  { if(running && canMove(player.x-1, player.y)) { player.x--; checkCollect(); checkEnemy(); drawMaze(); }}
    function mazeRight() { if(running && canMove(player.x+1, player.y)) { player.x++; checkCollect(); checkEnemy(); drawMaze(); }}

    document.addEventListener('keydown', e => {
        if (e.key==='ArrowUp'||e.key==='w')    mazeUp();
        if (e.key==='ArrowDown'||e.key==='s')  mazeDown();
        if (e.key==='ArrowLeft'||e.key==='a')  mazeLeft();
        if (e.key==='ArrowRight'||e.key==='d') mazeRight();
    });

    function checkCollect() {
        keys.forEach(k => {
            if (!k.collected && k.x === player.x && k.y === player.y) {
                k.collected = true; collected++; score += 50;
                document.getElementById('maze-msg').textContent = '🔑 Kyber Key collected! +50 XP';
                document.getElementById('mkeys').textContent = collected;
                document.getElementById('mscore').textContent = score;
                if (collected === 3) {
                    running = false;
                    document.getElementById('maze-msg').textContent = '🎉 You escaped! All keys collected!';
                }
            }
        });
    }

    function checkEnemy() {
        enemies.forEach(e => {
            if (e.x === player.x && e.y === player.y) {
                lives--;
                document.getElementById('mlives').textContent = '❤️'.repeat(Math.max(0,lives));
                document.getElementById('maze-msg').textContent = '💀 Caught by quantum attacker! -1 life';
                player = {x:1, y:1};
                if (lives <= 0) {
                    running = false;
                    document.getElementById('maze-msg').textContent = '☠️ Game Over! Quantum won this round.';
                }
            }
        });
    }

    function moveEnemies() {
        if (!running) return;
        enemies.forEach(e => {
            const dirs = [{dx:0,dy:-1},{dx:0,dy:1},{dx:-1,dy:0},{dx:1,dy:0}];
            const valid = dirs.filter(d => canMove(e.x+d.dx, e.y+d.dy));
            if (valid.length > 0) {
                // Prefer moving toward player
                valid.sort((a,b) => {
                    const da = Math.abs((e.x+a.dx)-player.x) + Math.abs((e.y+a.dy)-player.y);
                    const db = Math.abs((e.x+b.dx)-player.x) + Math.abs((e.y+b.dy)-player.y);
                    return da - db;
                });
                const move = Math.random() < 0.6 ? valid[0] : valid[Math.floor(Math.random()*valid.length)];
                e.x += move.dx; e.y += move.dy;
            }
        });
        checkEnemy();
        drawMaze();
    }

    function drawMaze() {
        mx.clearRect(0,0,mc.width,mc.height);
        for (let r=0; r<ROWS; r++) {
            for (let c=0; c<COLS; c++) {
                if (MAZE[r][c]===1) {
                    mx.fillStyle='#1e1b4b';
                    mx.fillRect(c*CELL, r*CELL, CELL, CELL);
                    mx.strokeStyle='#4f46e5';
                    mx.strokeRect(c*CELL, r*CELL, CELL, CELL);
                } else {
                    mx.fillStyle='#0f172a';
                    mx.fillRect(c*CELL, r*CELL, CELL, CELL);
                    mx.strokeStyle='rgba(79,70,229,0.15)';
                    mx.strokeRect(c*CELL, r*CELL, CELL, CELL);
                }
            }
        }
        // Draw keys
        keys.forEach(k => {
            if (!k.collected) {
                mx.font='22px sans-serif';
                mx.textAlign='center';
                mx.fillText('🔑', k.x*CELL+CELL/2, k.y*CELL+CELL/1.4);
            }
        });
        // Draw enemies
        enemies.forEach(e => {
            mx.font='22px sans-serif';
            mx.textAlign='center';
            mx.fillText('☠️', e.x*CELL+CELL/2, e.y*CELL+CELL/1.4);
        });
        // Draw player
        mx.font='22px sans-serif';
        mx.textAlign='center';
        mx.fillText('🕵️', player.x*CELL+CELL/2, player.y*CELL+CELL/1.4);
    }

    // Idle screen
    mx.fillStyle='#0f172a';
    mx.fillRect(0,0,mc.width,mc.height);
    mx.fillStyle='#a5b4fc';
    mx.font='bold 18px sans-serif';
    mx.textAlign='center';
    mx.fillText('🌀 Lattice Maze Escape', mc.width/2, 180);
    mx.font='13px sans-serif';
    mx.fillText('Collect Kyber Keys, avoid quantum attackers', mc.width/2, 215);
    mx.fillText('Press ▶ Start to play', mc.width/2, 245);
    </script>
    """, height=560)


def render_tower_defense():
    """9-12: Improved PQC Tower Defense with more towers, enemies, bosses and education."""
    st.subheader("🛡️ PQC Tower Defense — Advanced!")
    st.markdown(
        "Deploy **post-quantum algorithms** to stop quantum attack waves! "
        "Place towers on the grid, then hit **Start Wave**. "
        "Earn bits by defeating enemies to buy more towers. **Boss enemies appear every 3 waves!**"
    )

    with st.expander("📚 Tower Guide — PQC Algorithms", expanded=False):
        cols = st.columns(3)
        with cols[0]:
            st.success("🔐 **Kyber (ML-KEM)** — Fast, cheap, good range. FIPS 203 key encapsulation.")
            st.success("✍️ **Dilithium (ML-DSA)** — Heavy damage, medium range. FIPS 204 signatures.")
        with cols[1]:
            st.success("🌲 **SPHINCS+ (SLH-DSA)** — Slow but massive damage. FIPS 205 hash-based.")
            st.success("🦅 **Falcon (FN-DSA)** — Fast rate, small range. FIPS 206 compact signature.")
        with cols[2]:
            st.success("⚡ **LWE Cannon** — Area damage, hits all enemies nearby. Ultimate weapon!")
            st.info("🌊 **Enemy Types:** Shor attacks key exchange. Grover attacks hashes. Boss = full quantum computer!")

    import streamlit.components.v1 as components_td
    components_td.html("""
<!DOCTYPE html>
<html>
<head>
<style>
body{margin:0;background:#0f172a;font-family:sans-serif;color:white;}
#gameArea{display:flex;flex-direction:column;align-items:center;padding:8px;}
.topbar{display:flex;justify-content:space-between;width:520px;margin-bottom:6px;
font-size:12px;font-weight:bold;color:#a5b4fc;}
.stat{background:#1e293b;padding:4px 10px;border-radius:6px;border:1px solid #334155;}
#tdCanvas{border:2px solid #4f46e5;border-radius:10px;cursor:pointer;}
.tower-panel{display:flex;gap:6px;margin:6px 0;flex-wrap:wrap;justify-content:center;}
.tbtn{padding:6px 10px;border-radius:8px;border:2px solid transparent;
cursor:pointer;font-size:11px;font-weight:bold;color:white;transition:all 0.15s;}
.tbtn.sel{border-color:white;transform:scale(1.05);}
.msg-box{font-size:12px;color:#34d399;min-height:18px;margin:4px;text-align:center;}
.wave-btn{padding:8px 24px;border-radius:8px;border:none;cursor:pointer;
background:#4f46e5;color:white;font-size:13px;font-weight:bold;margin:4px;}
.wave-btn:hover{background:#6d60ff;}
#fact-box{background:rgba(79,70,229,0.15);border:1px solid rgba(79,70,229,0.4);
border-radius:8px;padding:8px 12px;margin:4px;font-size:11px;color:#a5b4fc;
max-width:520px;display:none;text-align:center;}
</style>
</head>
<body>
<div id="gameArea">
<div class="topbar">
    <div class="stat">💾 HP: <span id="hp">100</span></div>
    <div class="stat">⭐ Score: <span id="tdscore">0</span></div>
    <div class="stat">💎 Bits: <span id="bits">200</span></div>
    <div class="stat">🌊 Wave: <span id="wave">0</span></div>
    <div class="stat">👾 Left: <span id="eleft">0</span></div>
</div>
<canvas id="tdCanvas" width="520" height="400"></canvas>
<div class="msg-box" id="td-msg">Select a tower and click the grid to place it!</div>
<div id="fact-box"></div>
<div class="tower-panel">
    <button class="tbtn sel" id="btn-kyber" style="background:#10b981"
        onclick="selT('kyber')">🔐 Kyber 40💎</button>
    <button class="tbtn" id="btn-dilithium" style="background:#3b82f6"
        onclick="selT('dilithium')">✍️ Dilithium 70💎</button>
    <button class="tbtn" id="btn-sphincs" style="background:#8b5cf6"
        onclick="selT('sphincs')">🌲 SPHINCS 100💎</button>
    <button class="tbtn" id="btn-falcon" style="background:#f59e0b"
        onclick="selT('falcon')">🦅 Falcon 60💎</button>
    <button class="tbtn" id="btn-lwe" style="background:#ec4899"
        onclick="selT('lwe')">⚡ LWE 150💎</button>
    <button class="wave-btn" onclick="startWave()">▶ Start Wave</button>
    <button class="wave-btn" style="background:#374151" onclick="resetGame()">🔄 Reset</button>
</div>
</div>
<script>
const tc = document.getElementById("tdCanvas");
const tx = tc.getContext("2d");
const CELL=40, COLS=13, ROWS=10;

const TOWERS = {
    kyber:     {cost:40,  color:"#10b981", dmg:20,  range:80,  rate:30,  emoji:"🔐", name:"Kyber",     area:false, fact:"ML-KEM FIPS 203 — Lattice key encapsulation! Quantum safe!"},
    dilithium: {cost:70,  color:"#3b82f6", dmg:45,  range:100, rate:50,  emoji:"✍️", name:"Dilithium",  area:false, fact:"ML-DSA FIPS 204 — Lattice digital signature! Cannot be forged!"},
    sphincs:   {cost:100, color:"#8b5cf6", dmg:80,  range:120, rate:90,  emoji:"🌲", name:"SPHINCS+",   area:false, fact:"SLH-DSA FIPS 205 — Hash-based! Works even if lattices break!"},
    falcon:    {cost:60,  color:"#f59e0b", dmg:25,  range:70,  rate:20,  emoji:"🦅", name:"Falcon",     area:false, fact:"FN-DSA FIPS 206 — Smallest quantum-safe signature ever!"},
    lwe:       {cost:150, color:"#ec4899", dmg:120, range:110, rate:80,  emoji:"⚡", name:"LWE Cannon", area:true,  fact:"Learning With Errors — The hardest quantum math problem exists!"},
};

const ENEMY_TYPES = [
    {name:"Shor",    emoji:"⚛️",  hp:60,   spd:1.2, pts:15, color:"#ef4444", fact:"Shor Algorithm breaks RSA and ECC!", boss:false},
    {name:"Grover",  emoji:"🌀",  hp:40,   spd:1.8, pts:12, color:"#f97316", fact:"Grover Algorithm speeds up brute force!", boss:false},
    {name:"Harrow",  emoji:"👾",  hp:100,  spd:0.9, pts:20, color:"#eab308", fact:"HHL Algorithm attacks linear systems!", boss:false},
    {name:"QAOA",    emoji:"🔮",  hp:80,   spd:1.5, pts:18, color:"#a855f7", fact:"QAOA finds optimal solutions faster!", boss:false},
    {name:"Q-BOSS",  emoji:"💀",  hp:800,  spd:0.7, pts:100,color:"#dc2626", fact:"Full quantum computer — the ultimate threat!", boss:true},
];

const PATH = [
    {x:0,y:2},{x:1,y:2},{x:2,y:2},{x:3,y:2},{x:3,y:5},
    {x:4,y:5},{x:5,y:5},{x:6,y:5},{x:6,y:1},{x:7,y:1},
    {x:8,y:1},{x:9,y:1},{x:9,y:7},{x:10,y:7},{x:11,y:7},{x:12,y:7}
];
const PATH_SET = new Set(PATH.map(p=>p.x+","+p.y));

let towers=[], enemies=[], bullets=[], particles=[];
let selTower="kyber", hp=100, score=0, bits=200, wave=0;
let waveRunning=false, frameId, spawnQ=[], spawnTimer=0;

function selT(t) {
    selTower=t;
    document.querySelectorAll(".tbtn").forEach(b=>b.classList.remove("sel"));
    document.getElementById("btn-"+t).classList.add("sel");
    const td = TOWERS[t];
    showMsg(td.emoji+" "+td.name+" selected — "+td.fact);
}

function showMsg(msg) {
    document.getElementById("td-msg").textContent=msg;
}

function showFact(fact) {
    const fb = document.getElementById("fact-box");
    fb.textContent = "📚 " + fact;
    fb.style.display = "block";
    clearTimeout(window._factTimer);
    window._factTimer = setTimeout(()=>{fb.style.display="none";}, 4000);
}

tc.addEventListener("click", e=>{
    const rect = tc.getBoundingClientRect();
    const cx = Math.floor((e.clientX-rect.left)/CELL);
    const cy = Math.floor((e.clientY-rect.top)/CELL);
    const key = cx+","+cy;
    const td = TOWERS[selTower];
    if (!PATH_SET.has(key) && !towers.find(t=>t.x===cx&&t.y===cy) && bits>=td.cost) {
        towers.push({x:cx,y:cy,type:selTower,timer:0,...td});
        bits-=td.cost;
        updateUI();
        showMsg(td.emoji+" "+td.name+" placed! "+td.fact);
        draw();
    } else if (bits<td.cost) {
        showMsg("💎 Need "+td.cost+" bits! Defeat more enemies to earn bits.");
    }
});

function startWave() {
    if (waveRunning) return;
    wave++;
    waveRunning=true;
    spawnQ=[];
    const isBoss = wave%3===0;
    const count = isBoss ? 1 : 4+wave*2;

    if (isBoss) {
        showMsg("💀 BOSS WAVE "+wave+"! The full quantum computer attacks!");
        spawnQ.push({...ENEMY_TYPES[4], delay:0});
    } else {
        for(let i=0;i<count;i++){
            const eType = ENEMY_TYPES[Math.floor(Math.random()*(ENEMY_TYPES.length-1))];
            const hpBoost = 1+(wave-1)*0.25;
            spawnQ.push({...eType, hp:Math.floor(eType.hp*hpBoost), maxHp:Math.floor(eType.hp*hpBoost), delay:i*60});
        }
    }
    document.getElementById("wave").textContent=wave;
    updateUI();
    if (!frameId) gameLoop();
}

function resetGame() {
    towers=[]; enemies=[]; bullets=[]; particles=[];
    hp=100; score=0; bits=200; wave=0; waveRunning=false;
    spawnQ=[]; spawnTimer=0;
    cancelAnimationFrame(frameId); frameId=null;
    updateUI();
    showMsg("Game reset! Select towers and start a new wave.");
    draw();
}

function updateUI() {
    document.getElementById("hp").textContent=Math.max(0,hp);
    document.getElementById("tdscore").textContent=score;
    document.getElementById("bits").textContent=bits;
    document.getElementById("eleft").textContent=enemies.length+spawnQ.length;
}

function gameLoop() {
    frameId=requestAnimationFrame(gameLoop);
    update();
    draw();
}

function update() {
    // Spawn enemies from queue
    spawnTimer++;
    if (spawnQ.length>0 && spawnQ[0].delay<=spawnTimer) {
        const e = spawnQ.shift();
        const hpVal = e.hp || e.maxHp || 60;
        enemies.push({
            pathIdx:0,
            x:PATH[0].x*CELL+CELL/2,
            y:PATH[0].y*CELL+CELL/2,
            hp:hpVal, maxHp:hpVal,
            speed:e.spd||1.2,
            name:e.name, emoji:e.emoji,
            color:e.color, pts:e.pts,
            fact:e.fact, boss:e.boss||false,
        });
    }

    // Move enemies
    enemies.forEach(e=>{
        if(e.pathIdx>=PATH.length-1){
            hp-= e.boss?30:10;
            document.getElementById("hp").textContent=Math.max(0,hp);
            showMsg("💥 "+e.name+" breached! "+(e.boss?"-30":"-10")+" HP");
            e.pathIdx=-1;
            if(hp<=0){
                cancelAnimationFrame(frameId); frameId=null;
                waveRunning=false;
                showMsg("☠️ Data corrupted! Quantum won. Score: "+score);
            }
            return;
        }
        const tgt=PATH[e.pathIdx+1];
        const tx2=tgt.x*CELL+CELL/2, ty2=tgt.y*CELL+CELL/2;
        const dx=tx2-e.x, dy=ty2-e.y;
        const dist=Math.sqrt(dx*dx+dy*dy);
        if(dist<e.speed+1){e.pathIdx++;}
        else{e.x+=dx/dist*e.speed; e.y+=dy/dist*e.speed;}
    });

    // Tower shooting
    towers.forEach(tower=>{
        tower.timer++;
        if(tower.timer<tower.rate) return;
        tower.timer=0;
        const cx=tower.x*CELL+CELL/2, cy=tower.y*CELL+CELL/2;
        if(tower.area){
            // LWE area damage
            const hit=enemies.filter(e=>e.pathIdx>=0&&Math.hypot(e.x-cx,e.y-cy)<=tower.range);
            if(hit.length>0){
                hit.forEach(e=>{e.hp-=tower.dmg;});
                particles.push({x:cx,y:cy,r:5,maxR:tower.range,alpha:0.8,color:tower.color});
                showFact(tower.fact);
            }
        } else {
            const inR=enemies.filter(e=>e.pathIdx>=0&&Math.hypot(e.x-cx,e.y-cy)<=tower.range);
            if(inR.length>0){
                bullets.push({x:cx,y:cy,tx:inR[0].x,ty:inR[0].y,
                    target:inR[0],dmg:tower.dmg,color:tower.color,
                    emoji:tower.emoji,speed:6,fact:tower.fact});
            }
        }
    });

    // Move bullets
    bullets=bullets.filter(b=>{
        const dx=b.tx-b.x, dy=b.ty-b.y;
        const dist=Math.sqrt(dx*dx+dy*dy);
        if(dist<b.speed+2){
            b.target.hp-=b.dmg;
            showFact(b.fact);
            return false;
        }
        b.x+=dx/dist*b.speed; b.y+=dy/dist*b.speed;
        b.tx=b.target.x; b.ty=b.target.y;
        return true;
    });

    // Remove dead enemies
    enemies=enemies.filter(e=>{
        if(e.pathIdx<0) return false;
        if(e.hp<=0){
            score+=e.pts*(e.boss?5:1);
            bits+=e.boss?80:20;
            // Death particles
            for(let i=0;i<6;i++){
                particles.push({
                    x:e.x, y:e.y,
                    vx:(Math.random()-0.5)*4,
                    vy:(Math.random()-0.5)*4,
                    r:4, alpha:1, color:e.color, type:"spark"
                });
            }
            showMsg("💥 "+e.name+" destroyed! +"+(e.pts*(e.boss?5:1))+" score +"+(e.boss?80:20)+" bits");
            updateUI();
            return false;
        }
        return true;
    });

    // Update particles
    particles=particles.filter(p=>{
        p.alpha-=p.type==="spark"?0.06:0.04;
        if(p.type==="spark"){p.x+=p.vx;p.y+=p.vy;}
        else{p.r+=3;}
        return p.alpha>0;
    });

    // Check wave complete
    if(waveRunning && enemies.length===0 && spawnQ.length===0){
        waveRunning=false;
        const bonus=50+wave*20;
        bits+=bonus;
        updateUI();
        showMsg("✅ Wave "+wave+" cleared! +"+bonus+" bits bonus. Ready for wave "+(wave+1)+"?");
        cancelAnimationFrame(frameId); frameId=null;
    }
}

function draw() {
    tx.clearRect(0,0,tc.width,tc.height);

    // Background
    tx.fillStyle="#0f172a";
    tx.fillRect(0,0,tc.width,tc.height);

    // Grid
    for(let r=0;r<ROWS;r++){
        for(let c=0;c<COLS;c++){
            const key=c+","+r;
            tx.fillStyle=PATH_SET.has(key)?"#1e293b":"#0f172a";
            tx.fillRect(c*CELL,r*CELL,CELL,CELL);
            tx.strokeStyle="rgba(79,70,229,0.15)";
            tx.strokeRect(c*CELL,r*CELL,CELL,CELL);
        }
    }

    // Path arrows
    for(let i=0;i<PATH.length-1;i++){
        const p=PATH[i], n=PATH[i+1];
        tx.fillStyle="rgba(165,180,252,0.3)";
        tx.font="14px sans-serif";
        tx.textAlign="center";
        const arrow = n.x>p.x?"→":n.x<p.x?"←":n.y>p.y?"↓":"↑";
        tx.fillText(arrow,p.x*CELL+CELL/2,p.y*CELL+CELL/1.5);
    }

    // Goal
    tx.font="22px sans-serif";
    tx.textAlign="center";
    tx.fillText("💾",PATH[PATH.length-1].x*CELL+CELL/2,PATH[PATH.length-1].y*CELL+CELL/1.4);

    // Particles
    particles.forEach(p=>{
        tx.beginPath();
        if(p.type==="spark"){
            tx.arc(p.x,p.y,p.r,0,Math.PI*2);
            tx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,"0");
            tx.fill();
        } else {
            tx.arc(p.x,p.y,p.r,0,Math.PI*2);
            tx.strokeStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,"0");
            tx.lineWidth=2;
            tx.stroke();
        }
    });

    // Tower ranges (on hover - always show for selected)
    towers.forEach(t=>{
        tx.beginPath();
        tx.arc(t.x*CELL+CELL/2,t.y*CELL+CELL/2,t.range,0,Math.PI*2);
        tx.fillStyle=t.color+"15";
        tx.fill();
        tx.font="22px sans-serif";
        tx.textAlign="center";
        tx.fillText(t.emoji,t.x*CELL+CELL/2,t.y*CELL+CELL/1.4);
    });

    // Bullets
    bullets.forEach(b=>{
        tx.font="14px sans-serif";
        tx.textAlign="center";
        tx.fillText(b.emoji,b.x,b.y+5);
    });

    // Enemies
    enemies.forEach(e=>{
        if(e.pathIdx<0) return;
        const size = e.boss?32:22;
        tx.font=size+"px sans-serif";
        tx.textAlign="center";
        tx.fillText(e.emoji,e.x,e.y+size/2);

        // HP bar
        const bw=e.boss?50:36, bh=e.boss?7:4;
        tx.fillStyle="#374151";
        tx.fillRect(e.x-bw/2,e.y-size/2-10,bw,bh);
        const pct=Math.max(0,e.hp/e.maxHp);
        tx.fillStyle=pct>0.6?"#10b981":pct>0.3?"#f59e0b":"#ef4444";
        tx.fillRect(e.x-bw/2,e.y-size/2-10,bw*pct,bh);

        // Boss label
        if(e.boss){
            tx.fillStyle="#dc2626";
            tx.font="bold 9px sans-serif";
            tx.textAlign="center";
            tx.fillText("BOSS: "+e.hp+"/"+e.maxHp,e.x,e.y-size/2-14);
        }
    });

    // HP warning overlay
    if(hp<=30){
        tx.fillStyle="rgba(239,68,68,0.08)";
        tx.fillRect(0,0,tc.width,tc.height);
    }
}

draw();
updateUI();
</script>
</body>
</html>
""", height=680)

def render_zombie_blast(difficulty: str = "easy"):
    """
    Quantum Zombie Blast — shoot quantum zombies with PQC weapons.
    difficulty: 'easy' | 'medium' | 'hard'
    """
    st.subheader("🧟 Quantum Zombie Blast!")
    st.markdown(
        "Quantum zombies are attacking your server! "
        "Blast them with **post-quantum cryptography weapons** before they reach you! "
        "Move with ← → keys and shoot with **SPACE**."
    )

    diff_settings = {
        "easy":   {"speed": "1.2", "rate": "120", "hp": "30",  "label": "🟢 Agent Recruit"},
        "medium": {"speed": "2.0", "rate": "80",  "hp": "50",  "label": "🟡 Code Cadet"},
        "hard":   {"speed": "3.0", "rate": "50",  "hp": "80",  "label": "🔴 Cipher Corps"},
    }
    d = diff_settings.get(difficulty, diff_settings["easy"])

    components.html(f"""
    <style>
        #zbCanvas {{ border: 2px solid #4f46e5; border-radius: 12px; display: block; margin: 0 auto; background: #0f172a; }}
        .zb-wrap {{ text-align: center; font-family: sans-serif; }}
        .zb-bar {{ display: flex; justify-content: space-between; max-width: 480px; margin: 6px auto; color: #a5b4fc; font-size: 13px; font-weight: bold; }}
        .weapon-row {{ display: flex; justify-content: center; gap: 8px; margin: 8px; flex-wrap: wrap; }}
        .wbtn {{ padding: 6px 12px; border-radius: 8px; border: 2px solid transparent; cursor: pointer; font-size: 11px; font-weight: bold; color: white; }}
        .wbtn.active {{ border-color: white; transform: scale(1.1); }}
        #zb-msg {{ font-size: 13px; color: #34d399; min-height: 18px; margin: 4px; }}
    </style>
    <div class="zb-wrap">
        <div class="zb-bar">
            <span>❤️ HP: <span id="zhp">100</span></span>
            <span>⭐ Score: <span id="zscore">0</span></span>
            <span>🌊 Wave: <span id="zwave">1</span></span>
            <span>🎯 Difficulty: {d['label']}</span>
        </div>
        <canvas id="zbCanvas" width="480" height="460"></canvas>
        <div id="zb-msg">Press SPACE or tap Fire to shoot!</div>
        <div class="weapon-row">
            <button class="wbtn active" id="w0" style="background:#10b981" onclick="selectWeapon(0)">🔐 Kyber</button>
            <button class="wbtn" id="w1" style="background:#3b82f6" onclick="selectWeapon(1)">✍️ Dilithium</button>
            <button class="wbtn" id="w2" style="background:#8b5cf6" onclick="selectWeapon(2)">🌲 SPHINCS+</button>
            <button class="wbtn" id="w3" style="background:#ef4444" onclick="selectWeapon(3)">⚡ Lattice Bomb</button>
            <button class="wbtn" style="background:#4f46e5" onclick="startZombies()">▶ Start</button>
            <button class="wbtn" style="background:#374151" onclick="fireWeapon()">🔫 Fire</button>
        </div>
    </div>
    <script>
    const zc = document.getElementById('zbCanvas');
    const zx = zc.getContext('2d');
    const W = 480, H = 460;

    const WEAPONS = [
        {{name:'Kyber Blaster',   emoji:'🔐', color:'#10b981', dmg:25,  speed:8,  spread:0,  ammo:999, desc:'Fast single shot'}},
        {{name:'Dilithium Cannon',emoji:'✍️', color:'#3b82f6', dmg:60,  speed:5,  spread:0,  ammo:999, desc:'Heavy slow shot'}},
        {{name:'SPHINCS Shotgun', emoji:'🌲', color:'#8b5cf6', dmg:20,  speed:7,  spread:3,  ammo:999, desc:'3-way spread'}},
        {{name:'Lattice Bomb',    emoji:'⚡', color:'#ef4444', dmg:100, speed:4,  spread:0,  ammo:999, desc:'Huge area blast'}},
    ];

    const ZOMBIE_TYPES = [
        {{label:'RSA☠️',   color:'#ef4444', emoji:'🧟', hp:{d['hp']},   pts:10, fact:'RSA broken by Shor Algorithm!'}},
        {{label:'ECC💀',   color:'#f97316', emoji:'🧟‍♀️', hp:{int(d['hp'])//2}, pts:15, fact:'ECC vulnerable to quantum!'}},
        {{label:'DES⚠️',  color:'#eab308', emoji:'🧟‍♂️', hp:{int(d['hp'])//3}, pts:20, fact:'DES is classically broken!'}},
        {{label:'MD5💥',   color:'#ec4899', emoji:'🧟', hp:{int(d['hp'])//2}, pts:25, fact:'MD5 has collision attacks!'}},
    ];

    let player = {{x: W/2, y: H-50, w: 44, h: 44, speed: 6}};
    let bullets = [], zombies = [], explosions = [];
    let selectedWeapon = 0, score = 0, zhp = 100, wave = 1;
    let running = false, frameId, spawnTimer = 0;
    let keys = {{}};
    const ZOMBIE_SPEED = {d['speed']};
    const SPAWN_RATE   = {d['rate']};

    function selectWeapon(i) {{
        selectedWeapon = i;
        document.querySelectorAll('.wbtn').forEach((b,j) => {{
            b.classList.toggle('active', j===i);
        }});
        const w = WEAPONS[i];
        document.getElementById('zb-msg').textContent = w.emoji+' '+w.name+' selected — '+w.desc;
    }}

    function startZombies() {{
        bullets=[]; zombies=[]; explosions=[];
        score=0; zhp=100; wave=1; running=true; spawnTimer=0;
        document.getElementById('zscore').textContent=0;
        document.getElementById('zhp').textContent=100;
        document.getElementById('zwave').textContent=1;
        document.getElementById('zb-msg').textContent='🧟 Quantum zombies incoming!';
        player.x = W/2;
        cancelAnimationFrame(frameId);
        gameLoop();
    }}

    function fireWeapon() {{
        if (!running) return;
        const w = WEAPONS[selectedWeapon];
        if (w.spread > 0) {{
            for (let i=-1; i<=1; i++) {{
                bullets.push({{
                    x: player.x, y: player.y-20,
                    dx: i*2.5, dy: -w.speed,
                    dmg: w.dmg, color: w.color,
                    emoji: w.emoji, r: 8,
                    bomb: w.dmg >= 100
                }});
            }}
        }} else {{
            bullets.push({{
                x: player.x, y: player.y-20,
                dx: 0, dy: -w.speed,
                dmg: w.dmg, color: w.color,
                emoji: w.emoji, r: w.dmg>=100 ? 14 : 8,
                bomb: w.dmg >= 100
            }});
        }}
    }}

    document.addEventListener('keydown', e => {{
        keys[e.key] = true;
        if (e.key===' ') {{ e.preventDefault(); fireWeapon(); }}
    }});
    document.addEventListener('keyup', e => {{ keys[e.key] = false; }});

    function spawnZombie() {{
        const type = ZOMBIE_TYPES[Math.floor(Math.random()*ZOMBIE_TYPES.length)];
        const waveHpBoost = 1 + (wave-1)*0.3;
        zombies.push({{
            x: Math.random()*(W-60)+30,
            y: -40,
            w: 40, h: 40,
            hp: Math.floor(type.hp * waveHpBoost),
            maxHp: Math.floor(type.hp * waveHpBoost),
            speed: ZOMBIE_SPEED + (wave-1)*0.15,
            label: type.label,
            color: type.color,
            emoji: type.emoji,
            pts: type.pts * wave,
            fact: type.fact,
            wobble: Math.random()*Math.PI*2,
        }});
    }}

    function gameLoop() {{
        frameId = requestAnimationFrame(gameLoop);
        update();
        draw();
    }}

    function update() {{
        // Player movement
        if (keys['ArrowLeft']  || keys['a']) player.x = Math.max(22, player.x-player.speed);
        if (keys['ArrowRight'] || keys['d']) player.x = Math.min(W-22, player.x+player.speed);

        // Spawn zombies
        spawnTimer++;
        const effectiveRate = Math.max(25, SPAWN_RATE - (wave-1)*8);
        if (spawnTimer >= effectiveRate) {{ spawnZombie(); spawnTimer=0; }}

        // Move bullets
        bullets = bullets.filter(b => {{
            b.x += b.dx; b.y += b.dy;
            return b.y > -20 && b.x > -20 && b.x < W+20;
        }});

        // Move zombies
        zombies.forEach(z => {{
            z.wobble += 0.08;
            z.y += z.speed;
            z.x += Math.sin(z.wobble)*0.8;
        }});

        // Bullet-zombie collisions
        bullets.forEach((b,bi) => {{
            zombies.forEach((z,zi) => {{
                const dist = Math.hypot(b.x-z.x-z.w/2, b.y-z.y-z.h/2);
                const hitR = b.bomb ? 60 : 22;
                if (dist < hitR) {{
                    if (b.bomb) {{
                        // Area damage to ALL zombies in range
                        zombies.forEach(oz => {{
                            if (Math.hypot(b.x-oz.x-oz.w/2, b.y-oz.y-oz.h/2) < 60) {{
                                oz.hp -= b.dmg;
                            }}
                        }});
                        explosions.push({{x:b.x, y:b.y, r:10, maxR:65, alpha:1}});
                        bullets[bi] = null;
                    }} else {{
                        z.hp -= b.dmg;
                        bullets[bi] = null;
                    }}
                    if (z.hp <= 0) {{
                        score += z.pts;
                        document.getElementById('zscore').textContent = score;
                        document.getElementById('zb-msg').textContent = '💥 '+z.label+' destroyed! '+z.fact;
                        zombies[zi] = null;
                        if (score >= wave * 200) {{
                            wave++;
                            document.getElementById('zwave').textContent = wave;
                            document.getElementById('zb-msg').textContent = '🌊 Wave '+wave+'! Quantum zombies getting stronger!';
                        }}
                    }}
                }}
            }});
        }});

        bullets  = bullets.filter(Boolean);
        zombies  = zombies.filter(Boolean);

        // Zombie reaches player
        zombies.forEach((z,zi) => {{
            if (z.y + z.h >= player.y && z.y <= player.y+player.h &&
                z.x + z.w >= player.x-22 && z.x <= player.x+22) {{
                zhp -= 8;
                document.getElementById('zhp').textContent = Math.max(0,zhp);
                document.getElementById('zb-msg').textContent = '💀 '+z.label+' hit you! -8 HP';
                zombies[zi] = null;
                if (zhp <= 0) {{
                    running = false;
                    cancelAnimationFrame(frameId);
                    zx.fillStyle='rgba(0,0,0,0.8)';
                    zx.fillRect(0,0,W,H);
                    zx.fillStyle='#ef4444';
                    zx.font='bold 32px sans-serif';
                    zx.textAlign='center';
                    zx.fillText('💀 SERVER BREACHED!', W/2, H/2-40);
                    zx.fillStyle='white';
                    zx.font='18px sans-serif';
                    zx.fillText('Final Score: '+score, W/2, H/2+5);
                    zx.fillText('Wave Reached: '+wave, W/2, H/2+35);
                    zx.fillStyle='#a5b4fc';
                    zx.font='14px sans-serif';
                    zx.fillText('Kyber & Dilithium would have protected you!', W/2, H/2+70);
                    document.getElementById('zb-msg').textContent='☠️ Game Over! Press Start to try again.';
                }}
            }}
        }});

        zombies = zombies.filter(Boolean);

        // Update explosions
        explosions = explosions.filter(e => {{
            e.r += 4; e.alpha -= 0.07;
            return e.alpha > 0;
        }});
    }}

    function draw() {{
        zx.clearRect(0,0,W,H);

        // Starfield background
        zx.fillStyle='#0f172a';
        zx.fillRect(0,0,W,H);
        for (let i=0; i<40; i++) {{
            zx.fillStyle='rgba(165,180,252,0.3)';
            zx.fillRect((i*67)%W, (i*43+Date.now()*0.02)%H, 1.5, 1.5);
        }}

        // Ground line
        zx.strokeStyle='#4f46e5';
        zx.lineWidth=2;
        zx.beginPath();
        zx.moveTo(0, H-30);
        zx.lineTo(W, H-30);
        zx.stroke();

        // Draw explosions
        explosions.forEach(e => {{
            zx.beginPath();
            zx.arc(e.x, e.y, e.r, 0, Math.PI*2);
            zx.fillStyle=`rgba(239,68,68,${{e.alpha*0.4}})`;
            zx.fill();
            zx.strokeStyle=`rgba(251,191,36,${{e.alpha}})`;
            zx.lineWidth=3;
            zx.stroke();
        }});

        // Draw zombies
        zombies.forEach(z => {{
            zx.font='30px sans-serif';
            zx.textAlign='center';
            zx.fillText(z.emoji, z.x+z.w/2, z.y+z.h);

            // Label
            zx.fillStyle=z.color;
            zx.font='bold 9px sans-serif';
            zx.fillText(z.label, z.x+z.w/2, z.y-2);

            // HP bar
            const bw=38, bh=4;
            zx.fillStyle='#374151';
            zx.fillRect(z.x+z.w/2-bw/2, z.y-10, bw, bh);
            zx.fillStyle=z.hp/z.maxHp > 0.5 ? '#10b981' : '#ef4444';
            zx.fillRect(z.x+z.w/2-bw/2, z.y-10, bw*(z.hp/z.maxHp), bh);
        }});

        // Draw bullets
        bullets.forEach(b => {{
            zx.font=(b.bomb?'22':'14')+'px sans-serif';
            zx.textAlign='center';
            zx.fillText(b.emoji, b.x, b.y);
        }});

        // Draw player
        zx.font='36px sans-serif';
        zx.textAlign='center';
        zx.fillText('🧑‍💻', player.x, player.y+10);

        // Player HP bar
        const pw=60;
        zx.fillStyle='#374151';
        zx.fillRect(player.x-pw/2, player.y+16, pw, 5);
        zx.fillStyle = zhp > 50 ? '#10b981' : zhp > 25 ? '#f59e0b' : '#ef4444';
        zx.fillRect(player.x-pw/2, player.y+16, pw*(zhp/100), 5);

        // Weapon indicator
        const w = WEAPONS[selectedWeapon];
        zx.fillStyle='rgba(79,70,229,0.3)';
        zx.beginPath();
        zx.roundRect(10, H-28, 160, 20, 4);
        zx.fill();
        zx.fillStyle='white';
        zx.font='11px sans-serif';
        zx.textAlign='left';
        zx.fillText(w.emoji+' '+w.name, 16, H-14);
    }}

    // Idle screen
    zx.fillStyle='#0f172a';
    zx.fillRect(0,0,W,H);
    zx.fillStyle='#a5b4fc';
    zx.font='bold 22px sans-serif';
    zx.textAlign='center';
    zx.fillText('🧟 Quantum Zombie Blast!', W/2, H/2-60);
    zx.font='14px sans-serif';
    zx.fillStyle='#6b7280';
    zx.fillText('Blast RSA, ECC and DES zombies', W/2, H/2-25);
    zx.fillText('with Kyber, Dilithium & SPHINCS+!', W/2, H/2+5);
    zx.fillStyle='#4f46e5';
    zx.font='bold 16px sans-serif';
    zx.fillText('Press ▶ Start to play', W/2, H/2+45);
    </script>
    """, height=600)

def render_quantumcraft_elementary():
    """K-5: QuantumCraft — Crypto Kingdom top-down block world."""
    st.subheader("⛏️ QuantumCraft — Crypto Kingdom!")
    st.markdown(
        "Mine **crypto blocks** and build your quantum-safe fortress! "
        "WASD or arrow keys to move. Press **E** to mine, **F** to place blocks. "
        "Avoid the 💀 quantum creepers!"
    )
    components.html("""
    <style>
        #qcCanvas{border:2px solid #10b981;border-radius:12px;display:block;margin:0 auto;}
        .qc-wrap{text-align:center;font-family:sans-serif;}
        .qc-bar{display:flex;justify-content:space-between;max-width:480px;margin:6px auto;color:#a5b4fc;font-size:12px;font-weight:bold;}
        .qc-inv{display:flex;justify-content:center;gap:6px;margin:6px;flex-wrap:wrap;}
        .inv-slot{background:#1e293b;border:2px solid #4f46e5;border-radius:6px;padding:4px 8px;font-size:11px;color:white;min-width:60px;}
        #qc-msg{font-size:12px;color:#34d399;min-height:18px;margin:3px;}
        .qc-btn{padding:7px 14px;border-radius:8px;border:none;cursor:pointer;font-size:12px;font-weight:bold;background:#10b981;color:white;margin:3px;}
    </style>
    <div class="qc-wrap">
        <div class="qc-bar">
            <span>HP:<span id="qhp">100</span></span>
            <span>Score:<span id="qscore">0</span></span>
            <span>Mined:<span id="qmined">0</span></span>
            <span>Level:<span id="qlevel">1</span></span>
        </div>
        <canvas id="qcCanvas" width="480" height="400"></canvas>
        <div id="qc-msg">WASD to move, E to mine, F to place!</div>
        <div class="qc-inv">
            <div class="inv-slot" id="slot-kyber">Kyber:0</div>
            <div class="inv-slot" id="slot-lattice">Lattice:0</div>
            <div class="inv-slot" id="slot-hash">Hash:0</div>
            <div class="inv-slot" id="slot-key">Keys:0</div>
        </div>
        <button class="qc-btn" onclick="startQC()">Start</button>
        <button class="qc-btn" onclick="mineBlock()">Mine(E)</button>
        <button class="qc-btn" onclick="placeBlock()">Place(F)</button>
    </div>
    <script>
    const qc=document.getElementById('qcCanvas');
    const qx=qc.getContext('2d');
    const CELL=40,COLS=12,ROWS=10;
    const BLOCKS={
        empty:{color:'#0f172a',emoji:'',solid:false,mineable:false},
        grass:{color:'#166534',emoji:'🌿',solid:true,mineable:false},
        kyber:{color:'#10b981',emoji:'🔐',solid:true,mineable:true,item:'kyber',pts:10},
        lattice:{color:'#3b82f6',emoji:'🏗',solid:true,mineable:true,item:'lattice',pts:15},
        hash:{color:'#8b5cf6',emoji:'#',solid:true,mineable:true,item:'hash',pts:20},
        key:{color:'#f59e0b',emoji:'K',solid:true,mineable:true,item:'key',pts:30},
        wall:{color:'#1e293b',emoji:'',solid:true,mineable:false},
        chest:{color:'#b45309',emoji:'C',solid:true,mineable:true,item:'chest',pts:50},
        placed:{color:'#4f46e5',emoji:'',solid:true,mineable:false},
    };
    let world=[],player,enemies,inventory,score,qhp,level,running,mined,keys={};
    function genWorld(){
        world=[];
        for(let r=0;r<ROWS;r++){world[r]=[];for(let c=0;c<COLS;c++){
            if(r===0||r===ROWS-1||c===0||c===COLS-1){world[r][c]='wall';continue;}
            const rn=Math.random();
            if(rn<0.10)world[r][c]='kyber';
            else if(rn<0.18)world[r][c]='lattice';
            else if(rn<0.24)world[r][c]='hash';
            else if(rn<0.27)world[r][c]='key';
            else if(rn<0.29)world[r][c]='chest';
            else if(rn<0.40)world[r][c]='grass';
            else world[r][c]='empty';
        }}
        world[5][1]='empty';world[5][2]='empty';world[4][1]='empty';world[4][2]='empty';
    }
    function startQC(){
        genWorld();player={x:1,y:4};enemies=[];
        inventory={kyber:0,lattice:0,hash:0,key:0,chest:0};
        score=0;qhp=100;level=1;running=true;mined=0;
        for(let i=0;i<4;i++)spawnC();
        document.getElementById('qc-msg').textContent='Mine the glowing crypto blocks!';
        updateUI();cancelAnimationFrame(window._qcF);gLoop();
    }
    function spawnC(){
        const x=Math.floor(Math.random()*(COLS-4))+COLS-5;
        const y=Math.floor(Math.random()*(ROWS-2))+1;
        if(world[y]&&world[y][x]==='empty')enemies.push({x,y,timer:0,rate:45});
    }
    function canWalk(x,y){
        if(x<0||y<0||x>=COLS||y>=ROWS)return false;
        const b=BLOCKS[world[y][x]];return b&&!b.solid;
    }
    function mineBlock(){
        if(!running)return;
        const dirs=[{dx:0,dy:-1},{dx:0,dy:1},{dx:-1,dy:0},{dx:1,dy:0}];
        for(const d of dirs){
            const nx=player.x+d.dx,ny=player.y+d.dy;
            if(nx>=0&&ny>=0&&nx<COLS&&ny<ROWS){
                const bt=world[ny][nx],b=BLOCKS[bt];
                if(b&&b.mineable){
                    if(b.item)inventory[b.item]=(inventory[b.item]||0)+1;
                    score+=b.pts;mined++;world[ny][nx]='empty';
                    document.getElementById('qc-msg').textContent='Mined '+bt+'! +'+b.pts+' pts';
                    updateUI();
                    if(mined>=level*8){level++;document.getElementById('qlevel').textContent=level;genWorld();for(let i=0;i<level+2;i++)spawnC();}
                    return;
                }
            }
        }
    }
    function placeBlock(){
        if(!running||inventory.kyber<=0)return;
        const dirs=[{dx:0,dy:-1},{dx:1,dy:0},{dx:-1,dy:0},{dx:0,dy:1}];
        for(const d of dirs){
            const nx=player.x+d.dx,ny=player.y+d.dy;
            if(nx>=0&&ny>=0&&nx<COLS&&ny<ROWS&&world[ny][nx]==='empty'){
                inventory.kyber--;world[ny][nx]='placed';
                document.getElementById('qc-msg').textContent='Kyber wall placed!';
                updateUI();return;
            }
        }
    }
    function updateUI(){
        document.getElementById('qscore').textContent=score;
        document.getElementById('qhp').textContent=Math.max(0,qhp);
        document.getElementById('qmined').textContent=mined;
        document.getElementById('slot-kyber').textContent='Kyber:'+inventory.kyber;
        document.getElementById('slot-lattice').textContent='Lattice:'+inventory.lattice;
        document.getElementById('slot-hash').textContent='Hash:'+inventory.hash;
        document.getElementById('slot-key').textContent='Keys:'+inventory.key;
    }
    document.addEventListener('keydown',e=>{
        keys[e.key]=true;
        if(e.key==='e'||e.key==='E')mineBlock();
        if(e.key==='f'||e.key==='F')placeBlock();
    });
    document.addEventListener('keyup',e=>{keys[e.key]=false;});
    let mt=0;
    function gLoop(){
        window._qcF=requestAnimationFrame(gLoop);mt++;
        if(mt>=8){mt=0;if(!running)return;
            let nx=player.x,ny=player.y;
            if(keys['ArrowUp']||keys['w'])ny--;
            if(keys['ArrowDown']||keys['s'])ny++;
            if(keys['ArrowLeft']||keys['a'])nx--;
            if(keys['ArrowRight']||keys['d'])nx++;
            if(canWalk(nx,ny)){player.x=nx;player.y=ny;}
            enemies.forEach((e,i)=>{
                e.timer++;if(e.timer<e.rate)return;e.timer=0;
                const dx=player.x-e.x,dy=player.y-e.y;
                const moves=[];
                if(dx>0&&canWalk(e.x+1,e.y))moves.push({x:e.x+1,y:e.y});
                if(dx<0&&canWalk(e.x-1,e.y))moves.push({x:e.x-1,y:e.y});
                if(dy>0&&canWalk(e.x,e.y+1))moves.push({x:e.x,y:e.y+1});
                if(dy<0&&canWalk(e.x,e.y-1))moves.push({x:e.x,y:e.y-1});
                if(moves.length>0){const m=moves[0];e.x=m.x;e.y=m.y;}
                if(e.x===player.x&&e.y===player.y){
                    qhp-=15;updateUI();enemies.splice(i,1);
                    if(qhp<=0){running=false;
                        qx.fillStyle='rgba(0,0,0,0.85)';qx.fillRect(0,0,480,400);
                        qx.fillStyle='#ef4444';qx.font='bold 26px sans-serif';qx.textAlign='center';
                        qx.fillText('Quantum Won! Score:'+score,240,200);
                    }
                }
            });
        }
        draw();
    }
    function draw(){
        qx.clearRect(0,0,480,400);
        for(let r=0;r<ROWS;r++)for(let c=0;c<COLS;c++){
            const b=BLOCKS[world[r][c]];if(!b)continue;
            qx.fillStyle=b.color;qx.fillRect(c*CELL,r*CELL,CELL,CELL);
            qx.strokeStyle='rgba(255,255,255,0.05)';qx.strokeRect(c*CELL,r*CELL,CELL,CELL);
            if(b.emoji){qx.font='20px sans-serif';qx.textAlign='center';qx.fillText(b.emoji,c*CELL+20,r*CELL+28);}
            if(b.mineable){qx.strokeStyle='rgba(255,255,255,0.3)';qx.lineWidth=1.5;qx.strokeRect(c*CELL+2,r*CELL+2,CELL-4,CELL-4);}
        }
        enemies.forEach(e=>{qx.font='22px sans-serif';qx.textAlign='center';qx.fillText('X',e.x*CELL+20,e.y*CELL+28);});
        qx.font='24px sans-serif';qx.textAlign='center';qx.fillText('P',player.x*CELL+20,player.y*CELL+28);
        qx.strokeStyle='#10b981';qx.lineWidth=2;qx.strokeRect(player.x*CELL+2,player.y*CELL+2,CELL-4,CELL-4);
    }
    qx.fillStyle='#0f172a';qx.fillRect(0,0,480,400);
    qx.fillStyle='#10b981';qx.font='bold 18px sans-serif';qx.textAlign='center';
    qx.fillText('QuantumCraft - Crypto Kingdom',240,180);
    qx.fillStyle='white';qx.font='14px sans-serif';qx.fillText('Press Start to play!',240,220);
    </script>
    """, height=620)


def render_quantumcraft_middle():
    """6-8: QuantumCraft — Lattice Mines."""
    st.subheader("⛏️ QuantumCraft — Lattice Mines!")
    st.markdown(
        "Dig deep into the **lattice mines** to find rare Kyber ore! "
        "WASD to move, E to mine, F to place. Go deeper for rarer algorithms!"
    )
    components.html("""
    <style>
        #qmCanvas{border:2px solid #3b82f6;border-radius:12px;display:block;margin:0 auto;}
        .qm-wrap{text-align:center;font-family:sans-serif;}
        .qm-bar{display:flex;justify-content:space-between;max-width:520px;margin:6px auto;color:#a5b4fc;font-size:12px;font-weight:bold;}
        .qm-inv{display:flex;justify-content:center;gap:5px;margin:5px;flex-wrap:wrap;}
        .qm-slot{background:#1e293b;border:2px solid #3b82f6;border-radius:6px;padding:3px 7px;font-size:11px;color:white;}
        #qm-msg{font-size:12px;color:#60a5fa;min-height:18px;margin:3px;}
        .qm-btn{padding:6px 12px;border-radius:8px;border:none;cursor:pointer;font-size:12px;font-weight:bold;background:#3b82f6;color:white;margin:3px;}
    </style>
    <div class="qm-wrap">
        <div class="qm-bar">
            <span>HP:<span id="mhp">120</span></span>
            <span>Score:<span id="mscore2">0</span></span>
            <span>Depth:<span id="mdepth">1</span></span>
            <span>Rare:<span id="mrare">0</span></span>
        </div>
        <canvas id="qmCanvas" width="520" height="420"></canvas>
        <div id="qm-msg">Mine deeper to find rarer crypto ore!</div>
        <div class="qm-inv">
            <div class="qm-slot" id="m-kyber">Kyber:0</div>
            <div class="qm-slot" id="m-dilithium">Dilithium:0</div>
            <div class="qm-slot" id="m-sphincs">SPHINCS:0</div>
            <div class="qm-slot" id="m-falcon">Falcon:0</div>
            <div class="qm-slot" id="m-lwe">LWE:0</div>
        </div>
        <button class="qm-btn" onclick="startMines()">Start</button>
        <button class="qm-btn" onclick="mineMid()">Mine(E)</button>
        <button class="qm-btn" onclick="placeMid()">Place(F)</button>
        <button class="qm-btn" onclick="goDeeper()">Deeper</button>
    </div>
    <script>
    const mc2=document.getElementById('qmCanvas');
    const mx2=mc2.getContext('2d');
    const CELL2=40,COLS2=13,ROWS2=10;
    const MB={
        empty:{color:'#0f172a',emoji:'',solid:false,mineable:false},
        stone:{color:'#374151',emoji:'',solid:true,mineable:true,item:null,pts:2},
        kyber:{color:'#10b981',emoji:'K',solid:true,mineable:true,item:'kyber',pts:20},
        dilithium:{color:'#3b82f6',emoji:'D',solid:true,mineable:true,item:'dilithium',pts:30},
        sphincs:{color:'#8b5cf6',emoji:'S',solid:true,mineable:true,item:'sphincs',pts:35},
        falcon:{color:'#f59e0b',emoji:'F',solid:true,mineable:true,item:'falcon',pts:50},
        lwe:{color:'#ec4899',emoji:'L',solid:true,mineable:true,item:'lwe',pts:60},
        wall:{color:'#111827',emoji:'',solid:true,mineable:false},
        ladder:{color:'#78350f',emoji:'^',solid:false,mineable:false},
        placed:{color:'#1d4ed8',emoji:'',solid:true,mineable:false},
    };
    let mw=[],mp,me2,mi,ms2=0,mh=120,md=1,mr=0,mrun=false,mk={},mmt=0;
    function genMines(depth){
        mw=[];
        const rc=Math.min(0.05+depth*0.03,0.25);
        for(let r=0;r<ROWS2;r++){mw[r]=[];for(let c=0;c<COLS2;c++){
            if(r===0||r===ROWS2-1||c===0||c===COLS2-1){mw[r][c]='wall';continue;}
            const rn=Math.random();
            if(rn<rc*0.3)mw[r][c]='lwe';
            else if(rn<rc*0.6)mw[r][c]='falcon';
            else if(rn<rc*0.9)mw[r][c]='sphincs';
            else if(rn<rc*1.5)mw[r][c]='dilithium';
            else if(rn<rc*2.5)mw[r][c]='kyber';
            else if(rn<0.40)mw[r][c]='stone';
            else mw[r][c]='empty';
        }}
        mw[1][1]='empty';mw[1][2]='empty';mw[2][1]='empty';
        mw[ROWS2-2][COLS2-2]='ladder';
    }
    function startMines(){
        md=1;ms2=0;mh=120;mr=0;mi={kyber:0,dilithium:0,sphincs:0,falcon:0,lwe:0};
        genMines(1);mp={x:1,y:1};me2=[];
        for(let i=0;i<2;i++)spawnME();
        mrun=true;updateMUI();cancelAnimationFrame(window._mF);mLoop();
    }
    function spawnME(){
        const x=Math.floor(Math.random()*(COLS2-4))+COLS2-5;
        const y=Math.floor(Math.random()*(ROWS2-3))+2;
        if(mw[y]&&mw[y][x]==='empty')me2.push({x,y,timer:0,rate:35});
    }
    function mCW(x,y){
        if(x<0||y<0||x>=COLS2||y>=ROWS2)return false;
        const b=MB[mw[y][x]];return b&&!b.solid;
    }
    function mineMid(){
        if(!mrun)return;
        const dirs=[{dx:0,dy:-1},{dx:0,dy:1},{dx:-1,dy:0},{dx:1,dy:0}];
        for(const d of dirs){
            const nx=mp.x+d.dx,ny=mp.y+d.dy;
            if(nx>=0&&ny>=0&&nx<COLS2&&ny<ROWS2){
                const bt=mw[ny][nx],b=MB[bt];
                if(b&&b.mineable){
                    if(b.item){mi[b.item]=(mi[b.item]||0)+1;if(['falcon','lwe','sphincs'].includes(b.item))mr++;}
                    ms2+=b.pts;mw[ny][nx]='empty';
                    document.getElementById('qm-msg').textContent='Mined '+bt+'! +'+b.pts;
                    updateMUI();return;
                }
            }
        }
    }
    function placeMid(){
        if(!mrun||mi.kyber<=0){document.getElementById('qm-msg').textContent='Need Kyber!';return;}
        const dirs=[{dx:0,dy:-1},{dx:1,dy:0},{dx:-1,dy:0},{dx:0,dy:1}];
        for(const d of dirs){
            const nx=mp.x+d.dx,ny=mp.y+d.dy;
            if(nx>=0&&ny>=0&&nx<COLS2&&ny<ROWS2&&mw[ny][nx]==='empty'){
                mi.kyber--;mw[ny][nx]='placed';
                document.getElementById('qm-msg').textContent='Kyber wall placed!';
                updateMUI();return;
            }
        }
    }
    function goDeeper(){
        if(!mrun)return;
        if(mp.x>=COLS2-3&&mp.y>=ROWS2-3){
            md++;genMines(md);mp={x:1,y:1};me2=[];
            for(let i=0;i<Math.min(md+1,6);i++)spawnME();
            document.getElementById('mdepth').textContent=md;
            document.getElementById('qm-msg').textContent='Depth '+md+'! Rarer ore ahead!';
        } else {
            document.getElementById('qm-msg').textContent='Find the ladder ^ in bottom-right!';
        }
    }
    function updateMUI(){
        document.getElementById('mscore2').textContent=ms2;
        document.getElementById('mhp').textContent=Math.max(0,mh);
        document.getElementById('mrare').textContent=mr;
        document.getElementById('m-kyber').textContent='Kyber:'+mi.kyber;
        document.getElementById('m-dilithium').textContent='Dilithium:'+mi.dilithium;
        document.getElementById('m-sphincs').textContent='SPHINCS:'+mi.sphincs;
        document.getElementById('m-falcon').textContent='Falcon:'+mi.falcon;
        document.getElementById('m-lwe').textContent='LWE:'+mi.lwe;
    }
    document.addEventListener('keydown',e=>{mk[e.key]=true;if(e.key==='e'||e.key==='E')mineMid();if(e.key==='f'||e.key==='F')placeMid();});
    document.addEventListener('keyup',e=>{mk[e.key]=false;});
    function mLoop(){
        window._mF=requestAnimationFrame(mLoop);mmt++;
        if(mmt>=8){mmt=0;if(!mrun)return;
            let nx=mp.x,ny=mp.y;
            if(mk['ArrowUp']||mk['w'])ny--;if(mk['ArrowDown']||mk['s'])ny++;
            if(mk['ArrowLeft']||mk['a'])nx--;if(mk['ArrowRight']||mk['d'])nx++;
            if(mCW(nx,ny)||mw[ny]&&mw[ny][nx]==='ladder'){mp.x=nx;mp.y=ny;}
            me2.forEach((e,i)=>{
                e.timer++;if(e.timer<e.rate)return;e.timer=0;
                const dx=mp.x-e.x,dy=mp.y-e.y;const moves=[];
                if(dx>0&&mCW(e.x+1,e.y))moves.push({x:e.x+1,y:e.y});
                if(dx<0&&mCW(e.x-1,e.y))moves.push({x:e.x-1,y:e.y});
                if(dy>0&&mCW(e.x,e.y+1))moves.push({x:e.x,y:e.y+1});
                if(dy<0&&mCW(e.x,e.y-1))moves.push({x:e.x,y:e.y-1});
                if(moves.length>0){const m=moves[0];e.x=m.x;e.y=m.y;}
                if(e.x===mp.x&&e.y===mp.y){
                    mh-=20;updateMUI();me2.splice(i,1);
                    if(mh<=0){mrun=false;mx2.fillStyle='rgba(0,0,0,0.85)';mx2.fillRect(0,0,520,420);mx2.fillStyle='#ef4444';mx2.font='bold 24px sans-serif';mx2.textAlign='center';mx2.fillText('Mine Collapsed! Score:'+ms2,260,210);}
                }
            });
        }
        mDraw();
    }
    function mDraw(){
        mx2.clearRect(0,0,520,420);
        for(let r=0;r<ROWS2;r++)for(let c=0;c<COLS2;c++){
            const b=MB[mw[r][c]];if(!b)continue;
            mx2.fillStyle=b.color;mx2.fillRect(c*CELL2,r*CELL2,CELL2,CELL2);
            mx2.strokeStyle='rgba(255,255,255,0.04)';mx2.strokeRect(c*CELL2,r*CELL2,CELL2,CELL2);
            if(b.emoji){mx2.font='16px sans-serif';mx2.textAlign='center';mx2.fillStyle='white';mx2.fillText(b.emoji,c*CELL2+20,r*CELL2+26);}
            if(b.mineable&&b.item){mx2.strokeStyle='rgba(255,255,255,0.25)';mx2.lineWidth=1;mx2.strokeRect(c*CELL2+2,r*CELL2+2,CELL2-4,CELL2-4);}
        }
        me2.forEach(e=>{mx2.font='18px sans-serif';mx2.textAlign='center';mx2.fillStyle='#ef4444';mx2.fillText('Q',e.x*CELL2+20,e.y*CELL2+26);});
        mx2.font='20px sans-serif';mx2.textAlign='center';mx2.fillStyle='white';mx2.fillText('P',mp.x*CELL2+20,mp.y*CELL2+26);
        mx2.strokeStyle='#3b82f6';mx2.lineWidth=2;mx2.strokeRect(mp.x*CELL2+2,mp.y*CELL2+2,CELL2-4,CELL2-4);
    }
    mx2.fillStyle='#0f172a';mx2.fillRect(0,0,520,420);
    mx2.fillStyle='#3b82f6';mx2.font='bold 18px sans-serif';mx2.textAlign='center';
    mx2.fillText('QuantumCraft - Lattice Mines',260,190);
    mx2.fillStyle='white';mx2.font='14px sans-serif';mx2.fillText('Press Start to play!',260,230);
    </script>
    """, height=620)


def render_quantumcraft_highschool():
    """9-12: QuantumCraft — Cipher Ruins side-scrolling platformer."""
    st.subheader("🏃 QuantumCraft — Cipher Ruins!")
    st.markdown(
        "Run through the **quantum-corrupted ruins**! "
        "Arrow keys to run, SPACE to jump. Collect PQC power-ups, avoid broken crypto!"
    )
    components.html("""
    <style>
        #crCanvas{border:2px solid #8b5cf6;border-radius:12px;display:block;margin:0 auto;}
        .cr-wrap{text-align:center;font-family:sans-serif;}
        .cr-bar{display:flex;justify-content:space-between;max-width:520px;margin:6px auto;color:#a5b4fc;font-size:12px;font-weight:bold;}
        #cr-msg{font-size:12px;color:#a78bfa;min-height:18px;margin:3px;}
        .cr-btn{padding:7px 16px;border-radius:8px;border:none;cursor:pointer;font-size:13px;font-weight:bold;background:#8b5cf6;color:white;margin:3px;}
    </style>
    <div class="cr-wrap">
        <div class="cr-bar">
            <span>HP:<span id="crhp">100</span></span>
            <span>Score:<span id="crscore">0</span></span>
            <span>PQC:<span id="crpqc">0</span></span>
            <span>Zone:<span id="crzone">1</span></span>
        </div>
        <canvas id="crCanvas" width="520" height="380"></canvas>
        <div id="cr-msg">Arrow keys to run, SPACE to jump!</div>
        <button class="cr-btn" onclick="startRunner()">Start</button>
        <button class="cr-btn" onclick="jumpPlayer()">Jump</button>
        <button class="cr-btn" onclick="if(crrunning&&player)player.vx=-4">Left</button>
        <button class="cr-btn" onclick="if(crrunning&&player)player.vx=4">Right</button>
    </div>
    <script>
    const cr=document.getElementById('crCanvas');
    const cx2=cr.getContext('2d');
    const CW=520,CH=380,GROUND=CH-60,GRAV=0.5,JUMP=-12;
    const PU=[
        {emoji:'K',name:'Kyber',color:'#10b981',pts:30,fact:'ML-KEM!'},
        {emoji:'D',name:'Dilithium',color:'#3b82f6',pts:40,fact:'ML-DSA!'},
        {emoji:'S',name:'SPHINCS',color:'#8b5cf6',pts:50,fact:'Hash-based!'},
        {emoji:'F',name:'Falcon',color:'#f59e0b',pts:60,fact:'Compact Lattice!'},
        {emoji:'L',name:'LWE',color:'#ec4899',pts:70,fact:'Learning With Errors!'},
    ];
    const OB=[
        {emoji:'R',name:'RSA',color:'#ef4444',dmg:20},
        {emoji:'E',name:'ECC',color:'#f97316',dmg:15},
        {emoji:'D2',name:'DES',color:'#eab308',dmg:10},
    ];
    let player,items,particles,crscore=0,crhp=100,crpqc=0,crzone=1;
    let crrunning=false,crkeys={},scrollX=0,spawnT=0,frameId2;
    function startRunner(){
        player={x:80,y:GROUND-40,w:36,h:36,vx:0,vy:0,onGround:false};
        items=[];particles=[];crscore=0;crhp=100;crpqc=0;crzone=1;scrollX=0;spawnT=0;
        crrunning=true;
        document.getElementById('crscore').textContent=0;
        document.getElementById('crhp').textContent=100;
        document.getElementById('crpqc').textContent=0;
        document.getElementById('crzone').textContent=1;
        document.getElementById('cr-msg').textContent='Run through the Cipher Ruins!';
        cancelAnimationFrame(frameId2);rLoop();
    }
    function jumpPlayer(){if(player&&player.onGround&&crrunning){player.vy=JUMP;player.onGround=false;}}
    document.addEventListener('keydown',e=>{
        crkeys[e.key]=true;
        if((e.key===' '||e.key==='ArrowUp')&&player&&player.onGround&&crrunning){e.preventDefault();jumpPlayer();}
    });
    document.addEventListener('keyup',e=>{crkeys[e.key]=false;});
    function rLoop(){
        frameId2=requestAnimationFrame(rLoop);if(!crrunning)return;
        if(crkeys['ArrowLeft']||crkeys['a'])player.vx=-4;
        else if(crkeys['ArrowRight']||crkeys['d'])player.vx=4;
        scrollX+=2+crzone*0.3;
        player.x+=player.vx;player.vy+=GRAV;player.y+=player.vy;
        if(player.y>=GROUND-player.h){player.y=GROUND-player.h;player.vy=0;player.onGround=true;}
        else player.onGround=false;
        player.x=Math.max(20,Math.min(CW-60,player.x));
        spawnT++;
        const rate=Math.max(60,120-crzone*10);
        if(spawnT%rate===0){
            const x=CW+scrollX+Math.random()*200+100;
            if(Math.random()<0.55){
                const p=PU[Math.floor(Math.random()*PU.length)];
                items.push({x,y:GROUND-50-Math.random()*80,w:28,h:28,...p,type:'powerup'});
            } else {
                const o=OB[Math.floor(Math.random()*OB.length)];
                const h=30+Math.random()*40;
                items.push({x,y:GROUND-h,w:32,h,...o,type:'obstacle'});
            }
        }
        items=items.filter(item=>{
            const ix=item.x-scrollX;if(ix<-60)return false;
            const hit=player.x<ix+item.w&&player.x+player.w>ix&&player.y<item.y+item.h&&player.y+player.h>item.y;
            if(hit){
                if(item.type==='powerup'){
                    crscore+=item.pts;crpqc++;
                    document.getElementById('crscore').textContent=crscore;
                    document.getElementById('crpqc').textContent=crpqc;
                    document.getElementById('cr-msg').textContent=item.name+' collected! '+item.fact;
                    if(crpqc>=crzone*5){crzone++;document.getElementById('crzone').textContent=crzone;}
                } else {
                    crhp-=item.dmg;document.getElementById('crhp').textContent=Math.max(0,crhp);
                    document.getElementById('cr-msg').textContent=item.name+' hit! NOT quantum safe!';
                    if(crhp<=0){crrunning=false;cx2.fillStyle='rgba(0,0,0,0.85)';cx2.fillRect(0,0,CW,CH);cx2.fillStyle='#8b5cf6';cx2.font='bold 24px sans-serif';cx2.textAlign='center';cx2.fillText('Ruins Collapsed! Score:'+crscore,CW/2,CH/2);}
                }
                return false;
            }
            return true;
        });
        particles=particles.filter(p=>{p.x+=p.vx;p.y+=p.vy;p.vy+=0.2;p.alpha-=0.05;return p.alpha>0;});
        rDraw();
    }
    function rDraw(){
        cx2.clearRect(0,0,CW,CH);
        const g=cx2.createLinearGradient(0,0,0,CH);g.addColorStop(0,'#0f0c29');g.addColorStop(1,'#302b63');
        cx2.fillStyle=g;cx2.fillRect(0,0,CW,CH);
        cx2.fillStyle='#1e1b4b';cx2.fillRect(0,GROUND,CW,CH-GROUND);
        cx2.fillStyle='#4f46e5';cx2.fillRect(0,GROUND,CW,3);
        items.forEach(item=>{
            const ix=item.x-scrollX;
            if(item.type==='obstacle'){
                cx2.fillStyle=item.color+'55';cx2.fillRect(ix,item.y,item.w,item.h);
                cx2.strokeStyle=item.color;cx2.lineWidth=2;cx2.strokeRect(ix,item.y,item.w,item.h);
                cx2.fillStyle=item.color;cx2.font='bold 11px sans-serif';cx2.textAlign='center';
                cx2.fillText(item.emoji,ix+item.w/2,item.y+item.h/2+4);
            } else {
                cx2.font='20px sans-serif';cx2.textAlign='center';
                cx2.fillText(item.emoji,ix+item.w/2,item.y+item.h/1.3);
                cx2.beginPath();cx2.arc(ix+item.w/2,item.y+item.h/2,16,0,Math.PI*2);
                cx2.fillStyle=item.color+'22';cx2.fill();
            }
        });
        cx2.font='26px sans-serif';cx2.textAlign='center';cx2.fillText('P',player.x+player.w/2,player.y+player.h);
        const pw=50;cx2.fillStyle='#374151';cx2.fillRect(player.x,player.y-10,pw,5);
        cx2.fillStyle=crhp>60?'#10b981':crhp>30?'#f59e0b':'#ef4444';
        cx2.fillRect(player.x,player.y-10,pw*(crhp/100),5);
    }
    cx2.fillStyle='#0f0c29';cx2.fillRect(0,0,CW,CH);
    cx2.fillStyle='#8b5cf6';cx2.font='bold 18px sans-serif';cx2.textAlign='center';
    cx2.fillText('QuantumCraft - Cipher Ruins',CW/2,CH/2-40);
    cx2.fillStyle='white';cx2.font='13px sans-serif';
    cx2.fillText('Collect PQC, avoid RSA/ECC/DES',CW/2,CH/2);
    cx2.fillText('Press Start to play!',CW/2,CH/2+35);
    </script>
    """, height=580)
