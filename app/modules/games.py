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
    """9-12: Tower Defense — deploy PQC algorithms to block quantum attacks."""
    st.subheader("🛡️ PQC Tower Defense!")
    st.markdown(
        "Deploy **post-quantum algorithms** to stop the quantum attack waves! "
        "Click a tower type then click the grid to place it. "
        "Stop the quantum computers from reaching your data! 💾"
    )

    components.html("""
    <style>
        #tdCanvas { border: 2px solid #4f46e5; border-radius: 12px; display: block; margin: 0 auto; }
        .td-wrap { text-align: center; font-family: sans-serif; background: #0f172a; padding: 10px; border-radius: 12px; }
        .td-bar { display: flex; justify-content: space-between; max-width: 500px; margin: 6px auto; color: #a5b4fc; font-size: 13px; font-weight: bold; }
        .tower-btns { display: flex; justify-content: center; gap: 8px; margin: 8px; flex-wrap: wrap; }
        .tbtn { padding: 7px 14px; border-radius: 8px; border: 2px solid transparent; cursor: pointer; font-size: 12px; font-weight: bold; color: white; }
        .tbtn.selected { border-color: white; }
        #td-msg { font-size: 13px; color: #34d399; min-height: 18px; }
    </style>
    <div class="td-wrap">
        <div class="td-bar">
            <span>💾 Data HP: <span id="hp">100</span></span>
            <span>⭐ Score: <span id="tdscore">0</span></span>
            <span>💎 Bits: <span id="bits">150</span></span>
            <span>🌊 Wave: <span id="wave">1</span></span>
        </div>
        <canvas id="tdCanvas" width="500" height="400"></canvas>
        <div id="td-msg">Select a tower and click the grid to place it!</div>
        <div class="tower-btns">
            <button class="tbtn selected" id="btn-kyber" style="background:#10b981" onclick="selectTower('kyber')">🔐 Kyber (50💎)</button>
            <button class="tbtn" id="btn-dilithium" style="background:#3b82f6" onclick="selectTower('dilithium')">✍️ Dilithium (75💎)</button>
            <button class="tbtn" id="btn-sphincs" style="background:#8b5cf6" onclick="selectTower('sphincs')">🌲 SPHINCS+ (100💎)</button>
            <button class="tbtn" style="background:#4f46e5" onclick="startWave()">▶ Start Wave</button>
        </div>
    </div>
    <script>
    const tc = document.getElementById('tdCanvas');
    const tx = tc.getContext('2d');
    const CELL=50, COLS=10, ROWS=8;

    const TOWERS = {
        kyber:     {cost:50,  color:'#10b981', dmg:15, range:90,  rate:40,  emoji:'🔐', name:'Kyber'},
        dilithium: {cost:75,  color:'#3b82f6', dmg:25, range:110, rate:60,  emoji:'✍️', name:'Dilithium'},
        sphincs:   {cost:100, color:'#8b5cf6', dmg:40, range:130, rate:80,  emoji:'🌲', name:'SPHINCS+'},
    };

    // Path for enemies to follow (column indices)
    const PATH = [{x:0,y:3},{x:1,y:3},{x:2,y:3},{x:2,y:5},{x:3,y:5},
                {x:4,y:5},{x:4,y:2},{x:5,y:2},{x:6,y:2},{x:6,y:6},
                {x:7,y:6},{x:8,y:6},{x:9,y:6}];

    const PATH_SET = new Set(PATH.map(p => p.x+','+p.y));

    let towers=[], enemies=[], selectedTower='kyber';
    let hp=100, score=0, bits=150, wave=1, waveRunning=false, frameId;

    function selectTower(t) {
        selectedTower = t;
        document.querySelectorAll('.tbtn').forEach(b => b.classList.remove('selected'));
        document.getElementById('btn-'+t).classList.add('selected');
    }

    tc.addEventListener('click', e => {
        const rect = tc.getBoundingClientRect();
        const cx = Math.floor((e.clientX - rect.left) / CELL);
        const cy = Math.floor((e.clientY - rect.top)  / CELL);
        const key = cx+','+cy;
        const tDef = TOWERS[selectedTower];
        if (!PATH_SET.has(key) && !towers.find(t=>t.x===cx&&t.y===cy) && bits >= tDef.cost) {
            towers.push({x:cx, y:cy, type:selectedTower, timer:0, ...tDef});
            bits -= tDef.cost;
            document.getElementById('bits').textContent = bits;
            document.getElementById('td-msg').textContent = tDef.emoji+' '+tDef.name+' placed!';
            draw();
        } else if (bits < tDef.cost) {
            document.getElementById('td-msg').textContent = '💎 Not enough bits!';
        }
    });

    function startWave() {
        if (waveRunning) return;
        waveRunning = true;
        const count = 5 + wave * 2;
        for (let i=0; i<count; i++) {
            setTimeout(() => {
                enemies.push({
                    pathIdx:0,
                    x: PATH[0].x*CELL+CELL/2,
                    y: PATH[0].y*CELL+CELL/2,
                    hp: 50 + wave*20,
                    maxHp: 50 + wave*20,
                    speed: 1 + wave*0.2,
                    type: Math.random()<0.5 ? 'shor' : 'grover',
                });
            }, i * 800);
        }
        document.getElementById('td-msg').textContent = '🌊 Wave '+wave+' incoming! '+count+' quantum attackers!';
        gameLoop();
    }

    function gameLoop() {
        frameId = requestAnimationFrame(gameLoop);
        update();
        draw();
    }

    function update() {
        // Move enemies along path
        enemies.forEach(e => {
            if (e.pathIdx >= PATH.length-1) {
                hp -= 10;
                document.getElementById('hp').textContent = Math.max(0,hp);
                e.pathIdx = -1; // Mark for removal
                document.getElementById('td-msg').textContent = '💥 Quantum attacker breached! -10 HP';
                return;
            }
            const target = PATH[e.pathIdx+1];
            const tx2 = target.x*CELL+CELL/2;
            const ty2 = target.y*CELL+CELL/2;
            const dx = tx2-e.x, dy = ty2-e.y;
            const dist = Math.sqrt(dx*dx+dy*dy);
            if (dist < e.speed+1) { e.pathIdx++; }
            else { e.x += (dx/dist)*e.speed; e.y += (dy/dist)*e.speed; }
        });

        // Tower shooting
        towers.forEach(tower => {
            tower.timer++;
            if (tower.timer >= tower.rate) {
                tower.timer = 0;
                const inRange = enemies.filter(e => e.pathIdx >= 0 &&
                    Math.hypot(e.x - tower.x*CELL-CELL/2, e.y - tower.y*CELL-CELL/2) <= tower.range);
                if (inRange.length > 0) {
                    inRange[0].hp -= tower.dmg;
                    if (inRange[0].hp <= 0) {
                        score += 10 * wave;
                        bits  += 15;
                        document.getElementById('tdscore').textContent = score;
                        document.getElementById('bits').textContent   = bits;
                        inRange[0].pathIdx = -1;
                    }
                }
            }
        });

        enemies = enemies.filter(e => e.pathIdx >= 0);

        if (hp <= 0) {
            cancelAnimationFrame(frameId);
            waveRunning = false;
            document.getElementById('td-msg').textContent = '☠️ Data corrupted! Quantum won. Score: '+score;
            return;
        }

        if (waveRunning && enemies.length === 0) {
            waveRunning = false;
            wave++;
            bits += 50;
            document.getElementById('wave').textContent = wave;
            document.getElementById('bits').textContent = bits;
            document.getElementById('td-msg').textContent = '✅ Wave cleared! +50 bits. Ready for wave '+wave+'?';
            cancelAnimationFrame(frameId);
        }
    }

    function draw() {
        tx.clearRect(0,0,tc.width,tc.height);

        // Grid
        for (let r=0; r<ROWS; r++) {
            for (let c=0; c<COLS; c++) {
                const key = c+','+r;
                if (PATH_SET.has(key)) {
                    tx.fillStyle='#1e293b';
                } else {
                    tx.fillStyle='#0f172a';
                }
                tx.fillRect(c*CELL, r*CELL, CELL, CELL);
                tx.strokeStyle='rgba(79,70,229,0.2)';
                tx.strokeRect(c*CELL, r*CELL, CELL, CELL);
            }
        }

        // Path arrows
        tx.fillStyle='rgba(100,116,139,0.4)';
        for (let i=0; i<PATH.length-1; i++) {
            const p=PATH[i];
            tx.font='16px sans-serif';
            tx.textAlign='center';
            tx.fillText('→', p.x*CELL+CELL/2, p.y*CELL+CELL/1.5);
        }

        // Goal
        tx.font='22px sans-serif';
        tx.textAlign='center';
        tx.fillText('💾', PATH[PATH.length-1].x*CELL+CELL/2, PATH[PATH.length-1].y*CELL+CELL/1.4);

        // Towers
        towers.forEach(t => {
            tx.fillStyle=t.color+'33';
            tx.beginPath();
            tx.arc(t.x*CELL+CELL/2, t.y*CELL+CELL/2, t.range, 0, Math.PI*2);
            tx.fill();
            tx.font='22px sans-serif';
            tx.textAlign='center';
            tx.fillText(t.emoji, t.x*CELL+CELL/2, t.y*CELL+CELL/1.4);
        });

        // Enemies
        enemies.forEach(e => {
            if (e.pathIdx < 0) return;
            const emoji = e.type==='shor' ? '⚛️' : '🌀';
            tx.font='20px sans-serif';
            tx.textAlign='center';
            tx.fillText(emoji, e.x, e.y+6);
            // HP bar
            const bw=34, bh=5;
            tx.fillStyle='#ef4444';
            tx.fillRect(e.x-bw/2, e.y-18, bw, bh);
            tx.fillStyle='#10b981';
            tx.fillRect(e.x-bw/2, e.y-18, bw*(e.hp/e.maxHp), bh);
        });
    }

    draw();
    </script>
    """, height=560)

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