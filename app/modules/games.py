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
    """K-5: Quantum Lock Drop — UPGRADED 2026 — Fortnite-style catch game with combos and boss waves."""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("🧱 Quantum Lock Drop!")
    st.markdown(
        "Catch **quantum-safe locks** and avoid **broken crypto**! "
        "Build combos, grab power-ups, survive boss waves!"
    )
    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow:hidden;}
#wrap{max-width:420px;margin:0 auto;padding:8px;}
.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-bottom:6px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:5px 3px;
    text-align:center;font-size:9px;color:#60a5fa;}
.hb b{display:block;font-size:14px;color:white;}
#cv{border:2px solid #1d4ed8;border-radius:10px;display:block;
    box-shadow:0 0 20px rgba(29,78,216,0.2);}
#msg{background:#071520;border:1px solid #1a3a5a;border-radius:8px;
    padding:4px 10px;margin-top:5px;font-size:10px;color:#60a5fa;
    text-align:center;min-height:20px;}
.btns{display:flex;gap:4px;margin-top:5px;}
.btn{flex:1;padding:7px;border-radius:8px;border:none;cursor:pointer;
    font-size:11px;font-weight:bold;color:white;}
.btn-start{background:linear-gradient(135deg,#059669,#10b981);}
.btn-reset{background:#334155;}
.cp{position:fixed;pointer-events:none;z-index:999;width:8px;height:8px;
    border-radius:2px;animation:cf linear forwards;}
@keyframes cf{0%{transform:translateY(-20px) rotate(0deg);opacity:1;}
    100%{transform:translateY(500px) rotate(720deg);opacity:0;}}
</style>
</head>
<body>
<div id="wrap">
<div class="hud">
    <div class="hb">⭐ Score<br><b id="h-score">0</b></div>
    <div class="hb">🔥 Combo<br><b id="h-combo">x1</b></div>
    <div class="hb">❤️ Lives<br><b id="h-lives">3</b></div>
    <div class="hb">🌊 Level<br><b id="h-level">1</b></div>
</div>
<canvas id="cv" width="400" height="420"></canvas>
<div id="msg">Press START to catch quantum-safe locks!</div>
<div class="btns">
    <button class="btn btn-start" onclick="startGame()">▶ Start</button>
    <button class="btn btn-reset" onclick="resetGame()">🔄 Reset</button>
</div>
</div>
<script>
var cv=document.getElementById('cv'),cx=cv.getContext('2d');
var W=400,H=420;

// Good items (catch these!)
var GOOD=[
    {emoji:'🔐',name:'ML-KEM',  color:'#10b981',pts:15,fips:'FIPS 203'},
    {emoji:'✍️', name:'ML-DSA',  color:'#3b82f6',pts:20,fips:'FIPS 204'},
    {emoji:'🌲',name:'SPHINCS+',color:'#8b5cf6',pts:25,fips:'FIPS 205'},
    {emoji:'🦅',name:'Falcon',  color:'#f59e0b',pts:30,fips:'FIPS 206'},
    {emoji:'🏗️',name:'Lattice', color:'#06b6d4',pts:10,fips:'Math Core'},
];
// Bad items (avoid these!)
var BAD=[
    {emoji:'💀',name:'RSA',    color:'#ef4444',dmg:1},
    {emoji:'☠️', name:'ECC',    color:'#f97316',dmg:1},
    {emoji:'⚠️', name:'DES',    color:'#dc2626',dmg:1},
    {emoji:'💥',name:'MD5',    color:'#b91c1c',dmg:1},
];
// Power-ups
var POWERUPS=[
    {emoji:'🛡️',name:'Shield',  color:'#10b981',effect:'shield'},
    {emoji:'⏰',name:'Slow',    color:'#60a5fa',effect:'slow'},
    {emoji:'⭐',name:'Double',  color:'#fbbf24',effect:'double'},
    {emoji:'⚡',name:'Zapper',  color:'#a78bfa',effect:'zap'},
];
var FACTS=[
    'ML-KEM (Kyber FIPS 203) uses lattice math — quantum computers cannot crack it!',
    'ML-DSA (Dilithium FIPS 204) creates unforgeable digital signatures!',
    'SPHINCS+ (FIPS 205) uses SHA-3 hash trees — the backup if lattice math breaks!',
    'Falcon (FIPS 206) makes the smallest quantum-safe signatures for IoT!',
    'RSA is broken by Shor Algorithm — quantum computers crack it in seconds!',
    'NIST finalized all 4 PQC standards in August 2024 (FIPS 203-206)!',
];

// State
var items=[],particles=[],floats=[];
var paddle={x:W/2,w:70,y:H-30,h:14};
var score=0,combo=1,comboTimer=0,lives=3,level=1;
var gameActive=false,shielded=false,slowActive=false,doubleActive=false;
var shieldTimer=0,slowTimer=0,doubleTimer=0;
var spawnTimer=0,spawnRate=60,fallSpeed=2;
var boss=null,bossHP=0,bossDir=1;
var bgStars=[];
for(var i=0;i<40;i++) bgStars.push({x:Math.random()*W,y:Math.random()*H*0.7,r:Math.random()*1.2,a:Math.random()*0.6+0.2});

function startGame(){
    items=[];particles=[];floats=[];
    score=0;combo=1;comboTimer=0;lives=3;level=1;
    gameActive=true;shielded=false;slowActive=false;doubleActive=false;
    spawnTimer=0;spawnRate=60;fallSpeed=2;boss=null;
    paddle.x=W/2;
    updateHUD();
    setMsg('Catch the quantum-safe locks! Avoid broken crypto!');
    loop();
}

function resetGame(){gameActive=false;items=[];particles=[];floats=[];boss=null;updateHUD();}

// Mouse / touch paddle control
cv.addEventListener('mousemove',function(e){
    var r=cv.getBoundingClientRect();
    paddle.x=(e.clientX-r.left)*(W/r.width);
});
cv.addEventListener('touchmove',function(e){
    e.preventDefault();
    var r=cv.getBoundingClientRect();
    paddle.x=(e.touches[0].clientX-r.left)*(W/r.width);
},{passive:false});

function spawnItem(){
    var roll=Math.random();
    var item;
    if(roll<0.08){
        var pu=POWERUPS[Math.floor(Math.random()*POWERUPS.length)];
        item={x:20+Math.random()*(W-40),y:-20,vy:fallSpeed*0.7,
              emoji:pu.emoji,name:pu.name,color:pu.color,type:'power',effect:pu.effect,r:18};
    } else if(roll<0.35){
        var b=BAD[Math.floor(Math.random()*BAD.length)];
        item={x:20+Math.random()*(W-40),y:-20,vy:fallSpeed*(0.9+Math.random()*0.4),
              emoji:b.emoji,name:b.name,color:b.color,type:'bad',dmg:b.dmg,r:16};
    } else {
        var g=GOOD[Math.floor(Math.random()*GOOD.length)];
        item={x:20+Math.random()*(W-40),y:-20,vy:fallSpeed*(0.8+Math.random()*0.5),
              emoji:g.emoji,name:g.name,color:g.color,type:'good',pts:g.pts,fips:g.fips,r:16};
    }
    items.push(item);
}

function spawnBoss(){
    boss={x:W/2,y:60,w:60,h:40,hp:5+level,maxHP:5+level,
          emoji:'🤖',color:'#ef4444',dir:1,speed:2+level*0.3,
          shootTimer:0,shootRate:80};
    setMsg('💀 BOSS: Quantum Shor Machine! Dodge its attacks!');
}

function update(){
    if(!gameActive) return;
    // Timers
    if(comboTimer>0){comboTimer--;if(comboTimer===0)combo=1;}
    if(shieldTimer>0){shieldTimer--;if(shieldTimer===0){shielded=false;setMsg('Shield expired!');}}
    if(slowTimer>0){slowTimer--;if(slowTimer===0){slowActive=false;setMsg('Slow expired!');}}
    if(doubleTimer>0){doubleTimer--;if(doubleTimer===0){doubleActive=false;setMsg('Double expired!');}}

    // Spawn
    spawnTimer++;
    if(spawnTimer>=spawnRate){
        spawnTimer=0;
        spawnItem();
        // Boss every 5 levels
        if(score>0&&score%500===0&&!boss) spawnBoss();
    }

    // Level up
    var newLevel=Math.floor(score/200)+1;
    if(newLevel>level){
        level=newLevel;
        fallSpeed=2+level*0.3;
        spawnRate=Math.max(25,60-level*4);
        setMsg('LEVEL '+level+'! Faster drops incoming!');
        confetti();
    }

    // Move items
    var speed=slowActive?0.4:1;
    items.forEach(function(it){it.y+=it.vy*speed;});

    // Boss logic
    if(boss){
        boss.x+=boss.dir*boss.speed;
        if(boss.x<40||boss.x>W-40) boss.dir*=-1;
        boss.shootTimer++;
        if(boss.shootTimer>=boss.shootRate){
            boss.shootTimer=0;
            items.push({x:boss.x,y:boss.y+20,vy:3,emoji:'💥',name:'Boss Shot',
                        color:'#ef4444',type:'bad',dmg:1,r:12});
        }
    }

    // Catch check
    items=items.filter(function(it){
        if(it.y>H+20) return false;
        // Check catch
        if(it.y+it.r>paddle.y&&it.y-it.r<paddle.y+paddle.h&&
           it.x>paddle.x-paddle.w/2-10&&it.x<paddle.x+paddle.w/2+10){
            catch_item(it);
            return false;
        }
        return true;
    });

    // Particles
    particles.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.vy+=0.08;p.alpha-=0.03;p.r*=0.95;});
    particles=particles.filter(function(p){return p.alpha>0;});
    floats.forEach(function(f){f.y-=0.8;f.alpha-=0.02;});
    floats=floats.filter(function(f){return f.alpha>0;});
}

function catch_item(it){
    if(it.type==='good'){
        combo++;comboTimer=90;
        var pts=it.pts*(doubleActive?2:1)*combo;
        score+=pts;
        addFloat(it.x,paddle.y,'+'+pts+(combo>1?' x'+combo:''),it.color);
        spawnParticles(it.x,paddle.y,it.color,8);
        if(combo>=5) confetti();
        if(it.fips) setMsg(it.emoji+' '+it.name+' ('+it.fips+') caught! +'+pts+' pts!');
    } else if(it.type==='bad'){
        if(shielded){
            addFloat(it.x,paddle.y,'BLOCKED!','#10b981');
            spawnParticles(it.x,paddle.y,'#10b981',6);
        } else {
            lives--;combo=1;
            addFloat(it.x,paddle.y,'OUCH!','#ef4444');
            spawnParticles(it.x,paddle.y,'#ef4444',10);
            setMsg('💀 '+it.name+' is quantum-vulnerable! Avoid it!');
            if(lives<=0) gameOver();
        }
    } else if(it.type==='power'){
        spawnParticles(it.x,paddle.y,it.color,10);
        addFloat(it.x,paddle.y,it.name+'!',it.color);
        if(it.effect==='shield'){shielded=true;shieldTimer=300;setMsg('🛡️ Shield active for 5 seconds!');}
        else if(it.effect==='slow'){slowActive=true;slowTimer=300;setMsg('⏰ Slow motion for 5 seconds!');}
        else if(it.effect==='double'){doubleActive=true;doubleTimer=300;setMsg('⭐ Double points for 5 seconds!');}
        else if(it.effect==='zap'){
            items=items.filter(function(i){return i.type!=='bad';});
            setMsg('⚡ Quantum Zapper! All bad crypto destroyed!');
            spawnParticles(W/2,H/2,'#a78bfa',20);
        }
    }
    // Boss hit
    if(it===boss) return;
    updateHUD();
}

function gameOver(){
    gameActive=false;
    setMsg('💀 GAME OVER! Score: '+score+' | Level: '+level+' — Press Start to try again!');
}

function draw(){
    cx.clearRect(0,0,W,H);
    // Background
    cx.fillStyle='#020d14';cx.fillRect(0,0,W,H);
    // Stars
    bgStars.forEach(function(s){
        cx.beginPath();cx.arc(s.x,s.y,s.r,0,6.28);
        cx.fillStyle='rgba(255,255,255,'+s.a+')';cx.fill();
    });
    // Grid
    cx.strokeStyle='#0a1f2e';cx.lineWidth=0.4;
    for(var gx=0;gx<W;gx+=50){cx.beginPath();cx.moveTo(gx,0);cx.lineTo(gx,H);cx.stroke();}
    for(var gy=0;gy<H;gy+=50){cx.beginPath();cx.moveTo(0,gy);cx.lineTo(W,gy);cx.stroke();}

    // Boss
    if(boss){
        cx.shadowColor=boss.color;cx.shadowBlur=15;
        cx.font='36px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(boss.emoji,boss.x,boss.y);cx.shadowBlur=0;
        // HP bar
        cx.fillStyle='#1e293b';cx.fillRect(boss.x-30,boss.y-28,60,8);
        cx.fillStyle='#ef4444';cx.fillRect(boss.x-30,boss.y-28,60*(boss.hp/boss.maxHP),8);
        cx.font='8px sans-serif';cx.fillStyle='#ef4444';
        cx.fillText('BOSS HP',boss.x,boss.y-32);
    }

    // Items
    items.forEach(function(it){
        cx.shadowColor=it.color;cx.shadowBlur=8;
        cx.font='22px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(it.emoji,it.x,it.y);cx.shadowBlur=0;
        // Small label
        cx.font='8px sans-serif';cx.fillStyle=it.color;
        cx.fillText(it.name,it.x,it.y+16);
    });

    // Particles
    particles.forEach(function(p){
        cx.beginPath();cx.arc(p.x,p.y,p.r,0,6.28);
        cx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,'0');cx.fill();
    });

    // Float texts
    floats.forEach(function(f){
        cx.font='bold 13px sans-serif';cx.textAlign='center';
        cx.fillStyle=f.color+Math.floor(f.alpha*255).toString(16).padStart(2,'0');
        cx.fillText(f.text,f.x,f.y);
    });

    // Paddle
    var pw=paddle.w+(shielded?10:0);
    var pg=cx.createLinearGradient(paddle.x-pw/2,0,paddle.x+pw/2,0);
    pg.addColorStop(0,shielded?'#10b981':'#1d4ed8');
    pg.addColorStop(0.5,shielded?'#34d399':'#60a5fa');
    pg.addColorStop(1,shielded?'#10b981':'#1d4ed8');
    cx.fillStyle=pg;
    if(cx.roundRect)cx.roundRect(paddle.x-pw/2,paddle.y,pw,paddle.h,paddle.h/2);
    else cx.rect(paddle.x-pw/2,paddle.y,pw,paddle.h);
    cx.fill();
    if(shielded){cx.shadowColor='#10b981';cx.shadowBlur=20;cx.fill();cx.shadowBlur=0;}

    // Power-up indicators
    var indicators=[];
    if(shielded) indicators.push({emoji:'🛡️',color:'#10b981',t:shieldTimer});
    if(slowActive) indicators.push({emoji:'⏰',color:'#60a5fa',t:slowTimer});
    if(doubleActive) indicators.push({emoji:'⭐',color:'#fbbf24',t:doubleTimer});
    indicators.forEach(function(ind,i){
        cx.font='14px serif';cx.textAlign='left';
        cx.fillText(ind.emoji,W-22,15+i*18);
        cx.fillStyle='#1e293b';cx.fillRect(W-44,10+i*18,18,4);
        cx.fillStyle=ind.color;cx.fillRect(W-44,10+i*18,18*(ind.t/300),4);
    });

    // Combo indicator
    if(combo>1){
        cx.font='bold '+(12+combo)+'px sans-serif';cx.textAlign='left';
        cx.fillStyle='#fbbf24';
        cx.fillText('x'+combo+' COMBO!',5,18);
    }

    // Level progress bar
    var lpct=(score%200)/200;
    cx.fillStyle='#1e293b';cx.fillRect(0,H-3,W,3);
    cx.fillStyle='#3b82f6';cx.fillRect(0,H-3,W*lpct,3);
}

function loop(){if(!gameActive)return;requestAnimationFrame(loop);update();draw();}

function spawnParticles(x,y,color,n){
    for(var i=0;i<n;i++){
        var a=Math.random()*6.28,s=1+Math.random()*4;
        particles.push({x:x,y:y,vx:Math.cos(a)*s,vy:Math.sin(a)*s-1,r:2+Math.random()*3,alpha:1,color:color});
    }
}
function addFloat(x,y,text,color){floats.push({x:x,y:y,text:text,color:color,alpha:1});}
function updateHUD(){
    document.getElementById('h-score').textContent=score;
    document.getElementById('h-combo').textContent='x'+combo;
    document.getElementById('h-lives').textContent='❤️'.repeat(Math.max(0,lives));
    document.getElementById('h-level').textContent=level;
}
function setMsg(m){document.getElementById('msg').textContent=m;}
function confetti(){
    var cols=['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444'];
    for(var i=0;i<20;i++){setTimeout(function(){
        var el=document.createElement('div');el.className='cp';
        el.style.left=Math.random()*100+'vw';
        el.style.background=cols[Math.floor(Math.random()*cols.length)];
        el.style.animationDuration=(1+Math.random()*2)+'s';
        document.body.appendChild(el);setTimeout(function(){el.remove();},3000);
    },i*40);}
}

// Init canvas
cx.fillStyle='#020d14';cx.fillRect(0,0,W,H);
cx.font='bold 16px sans-serif';cx.fillStyle='#60a5fa';cx.textAlign='center';
cx.fillText('🧱 Quantum Lock Drop',W/2,H/2-10);
cx.font='11px sans-serif';cx.fillStyle='#94a3b8';
cx.fillText('Press START to play!',W/2,H/2+15);
</script>
</body>
</html>
""", height=580)

def render_lattice_maze():
    """6-8: Lattice Maze — UPGRADED 2026 — Pac-Man style with enemies, power-ups, boss waves."""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("🌀 Lattice Maze — Operation: Quantum Rescue!")
    st.markdown(
        "🚨 **Collect all 4 NIST crystals** before Shor Bots catch you! "
        "Arrow keys to move. Grab power-ups to fight back!"
    )
    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow:hidden;}
#wrap{display:flex;flex-direction:column;align-items:center;padding:8px;max-width:580px;margin:0 auto;}
.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;width:100%;margin-bottom:6px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:5px 3px;
    text-align:center;font-size:9px;color:#60a5fa;}
.hb b{display:block;font-size:14px;color:white;}
#cv{border:2px solid #1d4ed8;border-radius:8px;display:block;
    box-shadow:0 0 20px rgba(29,78,216,0.2);}
#msg-bar{background:#071520;border:1px solid #1a3a5a;border-radius:8px;
    padding:5px 12px;width:100%;margin-top:5px;font-size:10px;
    color:#60a5fa;text-align:center;min-height:24px;}
#fact-box{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);
    border-radius:8px;padding:6px 10px;margin-top:4px;font-size:10px;
    color:#93c5fd;display:none;line-height:1.5;width:100%;text-align:center;}
.btns{display:flex;gap:5px;margin-top:5px;}
.btn{flex:1;padding:7px;border-radius:8px;border:none;cursor:pointer;
    font-size:11px;font-weight:bold;color:white;transition:all 0.15s;}
.btn:hover{filter:brightness(1.2);}
.btn-start{background:linear-gradient(135deg,#059669,#10b981);}
.btn-reset{background:#334155;}

#overlay{position:absolute;top:0;left:0;width:100%;height:100%;
    background:rgba(0,0,0,0.82);border-radius:8px;display:flex;
    flex-direction:column;align-items:center;justify-content:center;z-index:10;}
#overlay h2{font-size:20px;margin-bottom:6px;}
#overlay p{font-size:11px;color:#94a3b8;margin-bottom:12px;text-align:center;}

@keyframes confettiFall{0%{transform:translateY(-20px) rotate(0deg);opacity:1;}
    100%{transform:translateY(600px) rotate(720deg);opacity:0;}}
.cp{position:fixed;pointer-events:none;z-index:999;width:8px;height:8px;
    border-radius:2px;animation:confettiFall linear forwards;}
</style>
</head>
<body>
<div id="wrap">
<div class="hud">
    <div class="hb">⭐ Score<br><b id="h-score">0</b></div>
    <div class="hb">❤️ Lives<br><b id="h-lives">3</b></div>
    <div class="hb">💎 Crystals<br><b id="h-crystals">0</b>/4</div>
    <div class="hb">🌊 Level<br><b id="h-level">1</b></div>
</div>

<div style="position:relative;width:560px;">
    <canvas id="cv" width="560" height="380"></canvas>
    <div id="overlay">
        <h2 id="ov-title">🌀 Lattice Maze</h2>
        <p id="ov-msg">Collect all 4 NIST crystals!<br>Arrow keys to move.<br>Avoid Shor Bots — grab power-ups to fight back!</p>
        <button class="btn btn-start" onclick="startGame()" style="padding:10px 24px;font-size:13px;">▶ Start Game</button>
    </div>
</div>

<div id="msg-bar">Press START to begin your mission!</div>
<div id="fact-box"></div>

<div class="btns">
    <button class="btn btn-start" onclick="startGame()">▶ Start</button>
    <button class="btn btn-reset" onclick="resetGame()">🔄 Reset</button>
</div>
</div>

<script>
const cv = document.getElementById('cv');
const cx = cv.getContext('2d');
const W = 560, H = 380;

// ── MAZE GRID ─────────────────────────────────────────────────────────────────
// 0=path 1=wall 2=dot 3=crystal 4=powerup
const TS = 28; // tile size
const COLS = Math.floor(W/TS); // 20
const ROWS = Math.floor(H/TS); // 13

// Generate maze using walls around the edges + internal structure
function genMaze(){
    const grid = [];
    for(let r=0;r<ROWS;r++){
        grid[r]=[];
        for(let c=0;c<COLS;c++){
            // Border walls
            if(r===0||r===ROWS-1||c===0||c===COLS-1){ grid[r][c]=1; continue; }
            // Internal wall pattern — lattice grid feel
            if(r%4===0&&c%4===0){ grid[r][c]=1; continue; }
            if(r%4===0&&c%2===0&&Math.random()<0.5){ grid[r][c]=1; continue; }
            if(c%4===0&&r%2===0&&Math.random()<0.5){ grid[r][c]=1; continue; }
            grid[r][c]=2; // default: dot
        }
    }
    // Place crystals in corners (safe spots)
    const crystalSpots=[[2,2],[2,COLS-3],[ROWS-3,2],[ROWS-3,COLS-3]];
    crystalSpots.forEach(([r,c])=>{
        grid[r][c]=3;
        // Clear surrounding area
        for(let dr=-1;dr<=1;dr++) for(let dc=-1;dc<=1;dc++){
            if(grid[r+dr]&&grid[r+dr][c+dc]!==undefined&&grid[r+dr][c+dc]!==1)
                grid[r+dr][c+dc]=2;
        }
    });
    // Place power-ups
    let puCount=0;
    while(puCount<4){
        const r=2+Math.floor(Math.random()*(ROWS-4));
        const c=2+Math.floor(Math.random()*(COLS-4));
        if(grid[r][c]===2){ grid[r][c]=4; puCount++; }
    }
    // Clear player start area
    for(let dr=-1;dr<=1;dr++) for(let dc=-1;dc<=1;dc++){
        if(grid[6+dr]&&grid[6+dr][10+dc]!==undefined&&grid[6+dr][10+dc]!==1)
            grid[6+dr][10+dc]=0;
    }
    return grid;
}

// ── CRYSTAL DATA ─────────────────────────────────────────────────────────────
const CRYSTALS=[
    {name:'ML-KEM',  emoji:'🔐', color:'#10b981', fips:'FIPS 203',
     fact:'ML-KEM (Kyber) uses lattice math to protect key exchange — even quantum computers cannot break it!'},
    {name:'ML-DSA',  emoji:'✍️',  color:'#3b82f6', fips:'FIPS 204',
     fact:'ML-DSA (Dilithium) creates digital signatures that no quantum computer can forge!'},
    {name:'SLH-DSA', emoji:'🌲', color:'#8b5cf6', fips:'FIPS 205',
     fact:'SLH-DSA (SPHINCS+) uses SHA-3 hash trees — safe even if all lattice math breaks!'},
    {name:'FN-DSA',  emoji:'🦅', color:'#f59e0b', fips:'FIPS 206',
     fact:'FN-DSA (Falcon) makes the SMALLEST quantum-safe signatures — perfect for IoT devices!'},
];

const POWERUPS=[
    {emoji:'⚡', name:'Quantum Zapper', color:'#fbbf24', effect:'zap'},
    {emoji:'🛡️', name:'Kyber Shield',  color:'#10b981', effect:'shield'},
    {emoji:'⏰', name:'Time Freeze',    color:'#60a5fa', effect:'freeze'},
    {emoji:'🚀', name:'Speed Boost',    color:'#f97316', effect:'speed'},
];

// ── GAME STATE ────────────────────────────────────────────────────────────────
let grid=[], player={}, enemies=[], particles=[];
let score=0, lives=3, level=1, crystals=0;
let frameId=null, gameActive=false;
let keys={};
let crystalsCollected=[];
let activeEffect=null, effectTimer=0;
let dots=0, totalDots=0;

function startGame(){
    document.getElementById('overlay').style.display='none';
    grid=genMaze();
    // Count dots
    totalDots=0;
    for(let r=0;r<ROWS;r++) for(let c=0;c<COLS;c++) if(grid[r][c]===2) totalDots++;

    player={
        x:10*TS+TS/2, y:6*TS+TS/2,
        vx:0, vy:0, speed:2.2,
        r:10, dir:0, mouthAngle:0, mouthOpen:true,
        invincible:0, mouthTimer:0,
    };
    enemies=[
        makeEnemy(3,3,'👾','#ef4444'),
        makeEnemy(ROWS-4,COLS-4,'🤖','#f97316'),
        makeEnemy(3,COLS-4,'💀','#8b5cf6'),
    ];
    score=0; lives=3; crystals=0; dots=0;
    crystalsCollected=[]; activeEffect=null; effectTimer=0;
    particles=[];
    gameActive=true;
    updateHUD();
    if(frameId) cancelAnimationFrame(frameId);
    loop();
}

function makeEnemy(row,col,emoji,color){
    return {
        x:col*TS+TS/2, y:row*TS+TS/2,
        emoji, color, speed:1.2+level*0.15,
        dir:Math.floor(Math.random()*4),
        moveTimer:0, moveRate:18,
        frozen:false, r:12,
    };
}

function resetGame(){
    if(frameId) cancelAnimationFrame(frameId);
    gameActive=false;
    score=0;lives=3;level=1;crystals=0;dots=0;
    updateHUD();
    document.getElementById('overlay').style.display='flex';
    document.getElementById('ov-title').textContent='🌀 Lattice Maze';
    document.getElementById('ov-msg').textContent='Collect all 4 NIST crystals!\nArrow keys to move.';
    document.getElementById('overlay').querySelector('button').textContent='▶ Start Game';
    document.getElementById('overlay').querySelector('button').onclick=startGame;
    cx.clearRect(0,0,W,H);
}

// ── PHYSICS ───────────────────────────────────────────────────────────────────
function tileAt(x,y){ return grid[Math.floor(y/TS)]?.[Math.floor(x/TS)]??1; }
function canMove(x,y,r){
    const checks=[[x-r,y],[x+r,y],[x,y-r],[x,y+r],[x-r,y-r],[x+r,y-r],[x-r,y+r],[x+r,y+r]];
    return checks.every(([cx,cy])=>tileAt(cx,cy)!==1);
}

const DIRS=[{dx:0,dy:-1},{dx:1,dy:0},{dx:0,dy:1},{dx:-1,dy:0}];
function updatePlayer(){
    const spd = activeEffect==='speed' ? player.speed*1.8 : player.speed;
    let dx=0,dy=0;
    if(keys['ArrowLeft']||keys['a']) dx=-spd;
    else if(keys['ArrowRight']||keys['d']) dx=spd;
    else if(keys['ArrowUp']||keys['w']) dy=-spd;
    else if(keys['ArrowDown']||keys['s']) dy=spd;

    if(dx!==0||dy!==0){
        const nx=player.x+dx, ny=player.y+dy;
        if(canMove(nx,player.y,player.r-2)) player.x=nx;
        if(canMove(player.x,ny,player.r-2)) player.y=ny;
        player.dir=dx>0?1:dx<0?3:dy>0?2:0;
    }

    // Mouth animation
    player.mouthTimer++;
    if(player.mouthTimer>6){ player.mouthTimer=0; player.mouthOpen=!player.mouthOpen; }

    // Collect tile
    const tr=Math.floor(player.y/TS), tc=Math.floor(player.x/TS);
    const tile=grid[tr]?.[tc];
    if(tile===2){ grid[tr][tc]=0; score+=10; dots++; updateHUD(); }
    else if(tile===3){
        const ci=crystalsCollected.length;
        if(ci<CRYSTALS.length){
            grid[tr][tc]=0;
            crystalsCollected.push(ci);
            crystals++;
            score+=500;
            const crys=CRYSTALS[ci];
            showFact('💎 Collected '+crys.emoji+' '+crys.name+' ('+crys.fips+')! '+crys.fact);
            setMsg('💎 '+crys.name+' crystal collected! +500 pts!');
            spawnParticles(player.x,player.y,crys.color,12);
            confetti();
            if(crystals>=4) levelComplete();
            updateHUD();
        }
    }
    else if(tile===4){
        grid[tr][tc]=0;
        const pu=POWERUPS[Math.floor(Math.random()*POWERUPS.length)];
        activeEffect=pu.effect;
        effectTimer=180; // 3 seconds at 60fps
        setMsg(pu.emoji+' '+pu.name+' activated!');
        spawnParticles(player.x,player.y,pu.color,8);
        if(pu.effect==='zap'){
            enemies.forEach(e=>{ e.frozen=true; e.frozenTimer=120; });
            setMsg('⚡ Quantum Zapper! Enemies frozen for 2 seconds!');
        }
        if(pu.effect==='shield'){ player.invincible=300; }
        if(pu.effect==='freeze'){ enemies.forEach(e=>{e.frozen=true;e.frozenTimer=180;}); }
        updateHUD();
    }

    if(player.invincible>0) player.invincible--;
    if(effectTimer>0){ effectTimer--; if(effectTimer===0) activeEffect=null; }
}

function updateEnemies(){
    const DIRS2=[{dx:0,dy:-spd2},{dx:spd2,dy:0},{dx:0,dy:spd2},{dx:-spd2,dy:0}];
    enemies.forEach(e=>{
        if(e.frozen){ e.frozenTimer=Math.max(0,(e.frozenTimer||0)-1); if(e.frozenTimer===0) e.frozen=false; return; }
        const spd2=e.speed;
        e.moveTimer++;
        if(e.moveTimer<e.moveRate) {
            // Move in current direction
            const d=DIRS[e.dir];
            const nx=e.x+d.dx*spd2, ny=e.y+d.dy*spd2;
            if(canMove(nx,e.y,e.r-2)) e.x=nx;
            if(canMove(e.x,ny,e.r-2)) e.y=ny;
        } else {
            // Choose new direction — prefer toward player
            e.moveTimer=0;
            const options=[];
            const dx=player.x-e.x, dy=player.y-e.y;
            // Try player direction first
            const prefDir=Math.abs(dx)>Math.abs(dy)?(dx>0?1:3):(dy>0?2:0);
            [prefDir,(prefDir+1)%4,(prefDir+3)%4,(prefDir+2)%4].forEach(d=>{
                const dir=DIRS[d];
                const nx=e.x+dir.dx*TS*0.5, ny=e.y+dir.dy*TS*0.5;
                if(canMove(nx,ny,e.r-2)) options.push(d);
            });
            if(options.length>0) e.dir=options[0];
        }
    });
}
// fix reference issue in DIRS2 - use outer scope
const spd2=1;

function checkCollision(){
    enemies.forEach(e=>{
        const d=Math.hypot(player.x-e.x,player.y-e.y);
        if(d<player.r+e.r-4){
            if(player.invincible>0) return;
            if(activeEffect==='zap'){ // zap kills enemy
                enemies=enemies.filter(en=>en!==e);
                score+=200;
                spawnParticles(e.x,e.y,'#fbbf24',10);
                setMsg('⚡ Shor Bot destroyed! +200 pts!');
                return;
            }
            lives--;
            player.invincible=120;
            spawnParticles(player.x,player.y,'#ef4444',10);
            setMsg('💀 Caught! '+lives+' lives left!');
            if(lives<=0) gameOver();
            updateHUD();
        }
    });
}

function levelComplete(){
    gameActive=false;
    level++;
    score+=level*1000;
    showOverlay('🎉 Level '+(level-1)+' Complete!',
        'All 4 NIST crystals rescued!\n+'+((level)*1000)+' bonus points!\nGet ready for level '+level+'!',
        '▶ Next Level', ()=>{ startGame(); });
    confetti();
}

function gameOver(){
    gameActive=false;
    showOverlay('💀 Mission Failed!',
        'Score: '+score+'\nCrystals: '+crystals+'/4',
        '🔄 Try Again', startGame);
}

function showOverlay(title,msg,btn,fn){
    const ov=document.getElementById('overlay');
    ov.style.display='flex';
    document.getElementById('ov-title').textContent=title;
    document.getElementById('ov-msg').textContent=msg;
    const b=ov.querySelector('button');
    b.textContent=btn; b.onclick=fn;
}

// ── DRAW ──────────────────────────────────────────────────────────────────────
function draw(){
    cx.clearRect(0,0,W,H);
    cx.fillStyle='#020d14'; cx.fillRect(0,0,W,H);

    for(let r=0;r<ROWS;r++){
        for(let c=0;c<COLS;c++){
            const tile=grid[r]?.[c];
            const x=c*TS, y=r*TS;
            if(tile===1){
                // Wall — lattice pattern
                cx.fillStyle='#0a1f35'; cx.fillRect(x,y,TS,TS);
                cx.strokeStyle='#1d4ed820'; cx.lineWidth=1;
                cx.strokeRect(x,y,TS,TS);
                // Lattice dots in wall corners
                cx.fillStyle='#1d4ed830';
                cx.beginPath();cx.arc(x+2,y+2,2,0,Math.PI*2);cx.fill();
                cx.beginPath();cx.arc(x+TS-2,y+2,2,0,Math.PI*2);cx.fill();
            } else if(tile===2){
                // Dot
                cx.beginPath();cx.arc(x+TS/2,y+TS/2,2.5,0,Math.PI*2);
                cx.fillStyle='#1d4ed860';cx.fill();
            } else if(tile===3){
                // Crystal
                const ci=Math.floor(Math.random()*4); // deterministic by position
                const crys=CRYSTALS[(r+c)%4];
                cx.font='16px serif';cx.textAlign='center';cx.textBaseline='middle';
                // Glow
                cx.shadowColor=crys.color; cx.shadowBlur=12;
                cx.fillText(crys.emoji,x+TS/2,y+TS/2);
                cx.shadowBlur=0;
            } else if(tile===4){
                // Power-up
                const pu=POWERUPS[(r+c)%POWERUPS.length];
                cx.font='16px serif';cx.textAlign='center';cx.textBaseline='middle';
                cx.shadowColor=pu.color; cx.shadowBlur=10;
                cx.fillText(pu.emoji,x+TS/2,y+TS/2);
                cx.shadowBlur=0;
            }
        }
    }

    // Enemies
    enemies.forEach(e=>{
        cx.font='20px serif';cx.textAlign='center';cx.textBaseline='middle';
        if(e.frozen){
            cx.globalAlpha=0.5;
            cx.fillStyle='#60a5fa20';
            cx.beginPath();cx.arc(e.x,e.y,e.r+4,0,Math.PI*2);cx.fill();
        }
        cx.fillText(e.emoji,e.x,e.y);
        cx.globalAlpha=1;
    });

    // Player — Pac-Man style circle with mouth
    cx.save();
    cx.translate(player.x,player.y);
    const angle=[0,Math.PI/2,Math.PI,Math.PI*3/2][player.dir];
    cx.rotate(angle);
    const mouth=player.mouthOpen?0.25:0.05;
    if(player.invincible>0&&Math.floor(Date.now()/100)%2===0){
        cx.globalAlpha=0.4;
    }
    // Shield glow
    if(activeEffect==='shield'||player.invincible>0){
        cx.shadowColor='#10b981'; cx.shadowBlur=15;
    }
    cx.beginPath();
    cx.moveTo(0,0);
    cx.arc(0,0,player.r,Math.PI*mouth,-Math.PI*mouth,false);
    cx.closePath();
    cx.fillStyle='#fbbf24';
    cx.fill();
    cx.shadowBlur=0;
    cx.globalAlpha=1;
    cx.restore();

    // Active effect indicator
    if(activeEffect){
        cx.font='12px serif';cx.textAlign='center';
        const pu=POWERUPS.find(p=>p.effect===activeEffect);
        if(pu){
            cx.fillText(pu.emoji,player.x,player.y-player.r-8);
        }
    }

    // Particles
    particles.forEach(p=>{
        cx.beginPath();cx.arc(p.x,p.y,p.r,0,Math.PI*2);
        cx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,'0');
        cx.fill();
    });

    // Crystal progress bar at top
    CRYSTALS.forEach((cr,i)=>{
        const collected=crystalsCollected.includes(i);
        cx.font='14px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.globalAlpha=collected?1:0.25;
        cx.fillText(cr.emoji,W/2-42+i*28,12);
        cx.globalAlpha=1;
    });
}

function update(){
    if(!gameActive) return;
    updatePlayer();
    updateEnemies();
    checkCollision();
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.alpha-=0.03;p.r*=0.95;});
    particles=particles.filter(p=>p.alpha>0);
}

function loop(){
    frameId=requestAnimationFrame(loop);
    update();
    draw();
}

// ── PARTICLES ─────────────────────────────────────────────────────────────────
function spawnParticles(x,y,color,n){
    for(let i=0;i<n;i++){
        const a=Math.random()*Math.PI*2,s=1+Math.random()*3;
        particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,
            r:2+Math.random()*3,alpha:1,color});
    }
}

// ── HUD ───────────────────────────────────────────────────────────────────────
function updateHUD(){
    document.getElementById('h-score').textContent=score;
    document.getElementById('h-lives').textContent='❤️'.repeat(Math.max(0,lives));
    document.getElementById('h-crystals').textContent=crystals;
    document.getElementById('h-level').textContent=level;
}

function setMsg(m){ document.getElementById('msg-bar').textContent=m; }

let factTimer=null;
function showFact(t){
    const el=document.getElementById('fact-box');
    el.textContent=t; el.style.display='block';
    if(factTimer)clearTimeout(factTimer);
    factTimer=setTimeout(()=>el.style.display='none',6000);
}

function confetti(){
    const cols=['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444'];
    for(let i=0;i<20;i++){
        setTimeout(()=>{
            const el=document.createElement('div');
            el.className='cp';
            el.style.left=Math.random()*100+'vw';
            el.style.background=cols[Math.floor(Math.random()*cols.length)];
            el.style.animationDuration=(1+Math.random()*2)+'s';
            document.body.appendChild(el);
            setTimeout(()=>el.remove(),3000);
        },i*40);
    }
}

// ── INPUT ─────────────────────────────────────────────────────────────────────
document.addEventListener('keydown',e=>{
    keys[e.key]=true;
    if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)) e.preventDefault();
});
document.addEventListener('keyup',e=>keys[e.key]=false);

// Mobile touch controls
let touchStartX=0,touchStartY=0;
cv.addEventListener('touchstart',e=>{
    touchStartX=e.touches[0].clientX;
    touchStartY=e.touches[0].clientY;
    e.preventDefault();
},{passive:false});
cv.addEventListener('touchend',e=>{
    const dx=e.changedTouches[0].clientX-touchStartX;
    const dy=e.changedTouches[0].clientY-touchStartY;
    if(Math.abs(dx)>Math.abs(dy)){
        if(dx>20){keys['ArrowRight']=true;setTimeout(()=>keys['ArrowRight']=false,150);}
        else if(dx<-20){keys['ArrowLeft']=true;setTimeout(()=>keys['ArrowLeft']=false,150);}
    } else {
        if(dy>20){keys['ArrowDown']=true;setTimeout(()=>keys['ArrowDown']=false,150);}
        else if(dy<-20){keys['ArrowUp']=true;setTimeout(()=>keys['ArrowUp']=false,150);}
    }
    e.preventDefault();
},{passive:false});

// ── INIT ─────────────────────────────────────────────────────────────────────
cx.fillStyle='#020d14';cx.fillRect(0,0,W,H);
cx.font='bold 22px sans-serif';cx.fillStyle='#60a5fa';
cx.textAlign='center';cx.fillText('🌀 Lattice Maze',W/2,H/2-20);
cx.font='12px sans-serif';cx.fillStyle='#94a3b8';
cx.fillText('Press START to rescue the NIST crystals!',W/2,H/2+10);
</script>
</body>
</html>
""", height=560)

def render_tower_defense():
    """All grades: Tower Defense — UPGRADED 2026 — place PQC towers, survive 10 waves."""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("🏰 Quantum Tower Defense!")
    st.markdown(
        "**Place PQC towers** to stop Shor Bots from reaching your server! "
        "Each tower uses a real NIST PQC algorithm. Click the grid to place towers!"
    )
    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow:hidden;}
#wrap{display:flex;flex-direction:column;align-items:center;padding:8px;max-width:580px;margin:0 auto;}
.hud{display:grid;grid-template-columns:repeat(5,1fr);gap:3px;width:100%;margin-bottom:6px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:6px;padding:4px 2px;
    text-align:center;font-size:8px;color:#60a5fa;}
.hb b{display:block;font-size:13px;color:white;}
#cv{border:2px solid #1d4ed8;border-radius:8px;display:block;cursor:pointer;
    box-shadow:0 0 20px rgba(29,78,216,0.15);}
#tower-bar{display:flex;gap:4px;justify-content:center;margin-top:5px;flex-wrap:wrap;}
.tower-btn{padding:5px 8px;border-radius:8px;border:2px solid #1a3a5a;
    background:#071520;color:#94a3b8;font-size:10px;cursor:pointer;
    transition:all 0.15s;text-align:center;min-width:70px;}
.tower-btn:hover{border-color:#3b82f6;color:white;}
.tower-btn.active{border-color:#fbbf24;background:#1a1500;color:#fbbf24;}
.tower-btn .tb-emoji{font-size:16px;display:block;margin-bottom:1px;}
.tower-btn .tb-cost{font-size:8px;color:#fbbf24;}
.btns{display:flex;gap:4px;margin-top:5px;width:100%;}
.btn{flex:1;padding:7px;border-radius:8px;border:none;cursor:pointer;
    font-size:11px;font-weight:bold;color:white;transition:all 0.15s;}
.btn:hover{filter:brightness(1.2);}
.btn-start{background:linear-gradient(135deg,#059669,#10b981);}
.btn-reset{background:#334155;}
.btn-speed{background:#1d4ed8;}
#msg-bar{background:#071520;border:1px solid #1a3a5a;border-radius:8px;
    padding:5px 12px;width:100%;margin-top:5px;font-size:10px;
    color:#60a5fa;text-align:center;min-height:22px;}
#fact-box{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);
    border-radius:8px;padding:6px 10px;margin-top:4px;font-size:10px;
    color:#93c5fd;display:none;line-height:1.5;width:100%;text-align:center;}
.cp{position:fixed;pointer-events:none;z-index:999;width:8px;height:8px;
    border-radius:2px;animation:cf linear forwards;}
@keyframes cf{0%{transform:translateY(-20px) rotate(0deg);opacity:1;}
    100%{transform:translateY(600px) rotate(720deg);opacity:0;}}
</style>
</head>
<body>
<div id="wrap">
<div class="hud">
    <div class="hb">💰 Gold<br><b id="h-gold">150</b></div>
    <div class="hb">❤️ Lives<br><b id="h-lives">20</b></div>
    <div class="hb">🌊 Wave<br><b id="h-wave">0</b>/10</div>
    <div class="hb">💀 Kills<br><b id="h-kills">0</b></div>
    <div class="hb">⭐ Score<br><b id="h-score">0</b></div>
</div>

<div style="position:relative;width:560px;">
    <canvas id="cv" width="560" height="360"></canvas>
</div>

<div id="tower-bar">
    <div class="tower-btn active" onclick="selectTower('kyber')" id="tb-kyber">
        <span class="tb-emoji">🔐</span>ML-KEM
        <div class="tb-cost">💰50 | DMG:2 | RNG:80</div>
    </div>
    <div class="tower-btn" onclick="selectTower('dilithium')" id="tb-dilithium">
        <span class="tb-emoji">✍️</span>ML-DSA
        <div class="tb-cost">💰75 | DMG:4 | RNG:65</div>
    </div>
    <div class="tower-btn" onclick="selectTower('sphincs')" id="tb-sphincs">
        <span class="tb-emoji">🌲</span>SPHINCS+
        <div class="tb-cost">💰100 | DMG:1 | RNG:120</div>
    </div>
    <div class="tower-btn" onclick="selectTower('falcon')" id="tb-falcon">
        <span class="tb-emoji">🦅</span>Falcon
        <div class="tb-cost">💰120 | DMG:8 | RNG:55</div>
    </div>
</div>

<div class="btns">
    <button class="btn btn-start" id="start-btn" onclick="startWave()">▶ Start Wave</button>
    <button class="btn btn-speed" onclick="toggleSpeed()" id="speed-btn">⚡ 1x Speed</button>
    <button class="btn btn-reset" onclick="resetGame()">🔄 Reset</button>
</div>

<div id="msg-bar">Click the grid to place towers, then press Start Wave!</div>
<div id="fact-box"></div>
</div>

<script>
const cv = document.getElementById('cv');
const cx = cv.getContext('2d');
const W=560, H=360;
const TS=40; // tile size
const COLS=14, ROWS=9;

// ── PATH ─────────────────────────────────────────────────────────────────────
// Pre-defined enemy path through the grid (column, row pairs)
const PATH=[
    [0,4],[1,4],[2,4],[2,2],[3,2],[4,2],[4,4],[5,4],[6,4],[6,6],
    [7,6],[8,6],[8,4],[9,4],[10,4],[10,2],[11,2],[12,2],[12,6],[13,6],
    [13,4],[13,3],[13,2],[13,1],[13,0]
];
// Convert to pixel coords (center of tiles)
const PATH_PX=PATH.map(([c,r])=>({x:c*TS+TS/2,y:r*TS+TS/2}));
// Set of path tiles (for placement blocking)
const PATH_SET=new Set(PATH.map(([c,r])=>r+','+c));

// ── TOWER TYPES ───────────────────────────────────────────────────────────────
const TOWERS={
    kyber:    {name:'ML-KEM',  emoji:'🔐',color:'#10b981',cost:50, dmg:2, range:80, rate:30, fips:'FIPS 203',
               fact:'ML-KEM (Kyber FIPS 203) fires key encapsulation packets — scrambles enemy crypto instantly!'},
    dilithium:{name:'ML-DSA',  emoji:'✍️', color:'#3b82f6',cost:75, dmg:4, range:65, rate:45, fips:'FIPS 204',
               fact:'ML-DSA (Dilithium FIPS 204) fires signature bursts — enemies cannot forge authentication!'},
    sphincs:  {name:'SPHINCS+',emoji:'🌲',color:'#8b5cf6',cost:100,dmg:1, range:120,rate:20, fips:'FIPS 205',
               fact:'SLH-DSA (SPHINCS+ FIPS 205) fires hash storms — wide range, rapid fire, quantum-proof!'},
    falcon:   {name:'Falcon',  emoji:'🦅',color:'#f59e0b',cost:120,dmg:8, range:55, rate:60, fips:'FIPS 206',
               fact:'FN-DSA (Falcon FIPS 206) fires compact NTRU spikes — high damage, precise strikes!'},
};

// ── WAVE CONFIGS ──────────────────────────────────────────────────────────────
const WAVES=[
    {count:5,  hp:3,  speed:0.8, emoji:'👾', reward:30,  name:'Shor Scout'},
    {count:8,  hp:4,  speed:0.9, emoji:'🤖', reward:35,  name:'RSA Bot'},
    {count:10, hp:5,  speed:1.0, emoji:'💀', reward:40,  name:'Grover Ghost'},
    {count:8,  hp:8,  speed:0.8, emoji:'☠️', reward:50,  name:'Quantum Creeper'},
    {count:12, hp:6,  speed:1.2, emoji:'🌀', reward:55,  name:'Vortex Drone'},
    {count:10, hp:12, speed:0.9, emoji:'👾', reward:65,  name:'Hardened Shor Bot'},
    {count:15, hp:8,  speed:1.1, emoji:'🤖', reward:70,  name:'Shor Swarm'},
    {count:8,  hp:20, speed:0.8, emoji:'💀', reward:80,  name:'Tank Bot'},
    {count:20, hp:10, speed:1.3, emoji:'🌀', reward:90,  name:'Speed Surge'},
    {count:5,  hp:50, speed:0.7, emoji:'👑', reward:200, name:'QUANTUM BOSS'},
];

// ── GAME STATE ────────────────────────────────────────────────────────────────
let towers=[], enemies=[], bullets=[], particles=[];
let gold=150, lives=20, wave=0, kills=0, score=0;
let waveActive=false, selectedType='kyber', speedMult=1;
let frameId=null, spawnTimer=0, spawnCount=0, spawnTotal=0;
let hoverTile=null;

// ── TOWER PLACEMENT ───────────────────────────────────────────────────────────
cv.addEventListener('click',e=>{
    const r=cv.getBoundingClientRect();
    const mx=(e.clientX-r.left)*(W/r.width);
    const my=(e.clientY-r.top)*(H/r.height);
    const tc=Math.floor(mx/TS), tr=Math.floor(my/TS);
    if(tc>=COLS||tr>=ROWS) return;
    if(PATH_SET.has(tr+','+tc)){ setMsg('❌ Cannot place on the path!'); return; }
    if(towers.find(t=>t.tc===tc&&t.tr===tr)){ setMsg('❌ Tower already here!'); return; }
    const type=TOWERS[selectedType];
    if(gold<type.cost){ setMsg('❌ Not enough gold! Need '+type.cost+' 💰'); return; }
    gold-=type.cost;
    towers.push({
        tc,tr,x:tc*TS+TS/2,y:tr*TS+TS/2,
        type:selectedType,...type,
        fireTimer:0,level:1,kills:0,
    });
    showFact(type.fact);
    setMsg('🔐 '+type.name+' tower placed! ('+type.fips+')');
    updateHUD();
});

cv.addEventListener('mousemove',e=>{
    const r=cv.getBoundingClientRect();
    const mx=(e.clientX-r.left)*(W/r.width);
    const my=(e.clientY-r.top)*(H/r.height);
    hoverTile={c:Math.floor(mx/TS),r:Math.floor(my/TS)};
});
cv.addEventListener('mouseleave',()=>hoverTile=null);

// ── WAVE MANAGEMENT ───────────────────────────────────────────────────────────
function startWave(){
    if(waveActive){ setMsg('⚠️ Wave already in progress!'); return; }
    if(wave>=WAVES.length){ setMsg('🏆 All waves defeated! You won!'); return; }
    const cfg=WAVES[wave];
    waveActive=true; spawnTimer=0; spawnCount=0; spawnTotal=cfg.count;
    document.getElementById('start-btn').disabled=true;
    setMsg('🌊 Wave '+(wave+1)+': '+cfg.count+'x '+cfg.name+' incoming!');
    wave++;
    updateHUD();
}

function spawnEnemy(){
    const cfg=WAVES[wave-1];
    const maxHp=cfg.hp*(1+wave*0.1);
    enemies.push({
        pathIdx:0,
        x:PATH_PX[0].x, y:PATH_PX[0].y,
        hp:maxHp, maxHp, speed:cfg.speed,
        emoji:cfg.emoji, progress:0,
        id:Math.random(),
    });
}

// ── UPDATE ────────────────────────────────────────────────────────────────────
function update(){
    const steps=speedMult;
    for(let s=0;s<steps;s++) _update();
}

function _update(){
    // Spawn
    if(waveActive&&spawnCount<spawnTotal){
        spawnTimer++;
        if(spawnTimer>=40){
            spawnTimer=0; spawnCount++;
            spawnEnemy();
        }
    }

    // Move enemies along path
    enemies.forEach(e=>{
        if(e.pathIdx>=PATH_PX.length-1){
            // Reached end — lose a life
            lives--; updateHUD();
            spawnParticles(e.x,e.y,'#ef4444',8);
            e.dead=true;
            setMsg('💀 Shor Bot reached your server! Lives: '+lives);
            if(lives<=0) gameOver();
            return;
        }
        const target=PATH_PX[e.pathIdx+1];
        const dx=target.x-e.x, dy=target.y-e.y;
        const d=Math.sqrt(dx*dx+dy*dy)||1;
        e.x+=dx/d*e.speed; e.y+=dy/d*e.speed;
        if(d<e.speed+1) e.pathIdx++;
    });
    enemies=enemies.filter(e=>!e.dead);

    // Towers fire
    towers.forEach(t=>{
        t.fireTimer++;
        if(t.fireTimer<t.rate) return;
        // Find closest enemy in range
        const target=enemies.filter(e=>{
            const d=Math.hypot(e.x-t.x,e.y-t.y);
            return d<=t.range;
        }).sort((a,b)=>b.pathIdx-a.pathIdx)[0];
        if(!target) return;
        t.fireTimer=0;
        bullets.push({
            x:t.x,y:t.y,tx:target.x,ty:target.y,
            targetId:target.id,speed:6,
            dmg:t.dmg,color:t.color,r:4,
            towerType:t.type,
        });
    });

    // Move bullets
    bullets.forEach(b=>{
        const target=enemies.find(e=>e.id===b.targetId);
        if(target){
            const dx=target.x-b.x,dy=target.y-b.y;
            const d=Math.sqrt(dx*dx+dy*dy)||1;
            b.x+=dx/d*b.speed; b.y+=dy/d*b.speed;
            if(d<b.speed+2){
                target.hp-=b.dmg;
                spawnParticles(target.x,target.y,b.color,4);
                b.dead=true;
                if(target.hp<=0){
                    target.dead=true;
                    kills++; score+=10;
                    const cfg=WAVES[wave-1];
                    gold+=cfg?Math.floor(cfg.reward/cfg.count):5;
                    const t=towers.find(t=>t.type===b.towerType);
                    if(t) t.kills++;
                    updateHUD();
                }
            }
        } else {
            b.dead=true;
        }
    });
    bullets=bullets.filter(b=>!b.dead);
    enemies=enemies.filter(e=>!e.dead);

    // Check wave clear
    if(waveActive&&spawnCount>=spawnTotal&&enemies.length===0){
        waveComplete();
    }

    // Particles
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.alpha-=0.04;p.r*=0.94;});
    particles=particles.filter(p=>p.alpha>0);
}

function waveComplete(){
    waveActive=false;
    const bonus=wave*50;
    gold+=bonus; score+=bonus;
    updateHUD();
    document.getElementById('start-btn').disabled=false;
    setMsg('✅ Wave '+wave+' cleared! +'+bonus+' gold bonus! Place more towers!');
    showFact(['🔐 ML-KEM protects key exchange!','✍️ ML-DSA signs every packet!',
              '🌲 SPHINCS+ uses SHA-3 hash trees!','🦅 Falcon makes tiny signatures!'][wave%4]);
    if(wave>=WAVES.length){
        setMsg('👑 ALL 10 WAVES DEFEATED! You are a Quantum Defense Master!');
        confetti();
    }
}

function gameOver(){
    waveActive=false;
    if(frameId) cancelAnimationFrame(frameId);
    setMsg('💀 GAME OVER! Wave: '+wave+' | Score: '+score+' | Kills: '+kills);
}

function resetGame(){
    if(frameId) cancelAnimationFrame(frameId);
    towers=[]; enemies=[]; bullets=[]; particles=[];
    gold=150; lives=20; wave=0; kills=0; score=0;
    waveActive=false; spawnTimer=0; spawnCount=0;
    document.getElementById('start-btn').disabled=false;
    updateHUD();
    setMsg('Click the grid to place towers, then press Start Wave!');
    document.getElementById('fact-box').style.display='none';
    loop();
}

function toggleSpeed(){
    speedMult=speedMult===1?2:1;
    document.getElementById('speed-btn').textContent=speedMult===1?'⚡ 1x Speed':'⚡ 2x Speed';
}

// ── DRAW ──────────────────────────────────────────────────────────────────────
function draw(){
    cx.clearRect(0,0,W,H);
    cx.fillStyle='#020d14'; cx.fillRect(0,0,W,H);

    // Grid tiles
    for(let r=0;r<ROWS;r++){
        for(let c=0;c<COLS;c++){
            const x=c*TS,y=r*TS;
            const isPath=PATH_SET.has(r+','+c);
            cx.fillStyle=isPath?'#0a1f35':'#050e1a';
            cx.fillRect(x,y,TS,TS);
            cx.strokeStyle='#1a3a5a20';
            cx.lineWidth=0.5;
            cx.strokeRect(x,y,TS,TS);
        }
    }

    // Path highlight
    PATH.forEach(([c,r],i)=>{
        if(i===0||i===PATH.length-1) return;
        cx.fillStyle='#1d4ed815';
        cx.fillRect(c*TS,r*TS,TS,TS);
    });

    // Start/end markers
    cx.font='16px serif';cx.textAlign='center';cx.textBaseline='middle';
    cx.fillText('👾',PATH_PX[0].x,PATH_PX[0].y);
    cx.font='10px sans-serif';cx.fillStyle='#ef4444';
    cx.fillText('SPAWN',PATH_PX[0].x,PATH_PX[0].y+20);
    cx.font='16px serif';
    cx.fillText('🖥️',W-TS/2,TS/2);
    cx.font='10px sans-serif';cx.fillStyle='#10b981';
    cx.fillText('SERVER',W-TS/2,TS*1.5);

    // Hover preview
    if(hoverTile&&hoverTile.c<COLS&&hoverTile.r<ROWS){
        const isPath=PATH_SET.has(hoverTile.r+','+hoverTile.c);
        const hasTower=towers.find(t=>t.tc===hoverTile.c&&t.tr===hoverTile.r);
        if(!isPath&&!hasTower){
            cx.fillStyle='#fbbf2420';
            cx.fillRect(hoverTile.c*TS,hoverTile.r*TS,TS,TS);
            // Show range preview
            const type=TOWERS[selectedType];
            cx.beginPath();
            cx.arc(hoverTile.c*TS+TS/2,hoverTile.r*TS+TS/2,type.range,0,Math.PI*2);
            cx.strokeStyle=type.color+'30';cx.lineWidth=1;cx.stroke();
        }
    }

    // Towers
    towers.forEach(t=>{
        // Range ring on hover
        if(hoverTile&&t.tc===hoverTile.c&&t.tr===hoverTile.r){
            cx.beginPath();
            cx.arc(t.x,t.y,t.range,0,Math.PI*2);
            cx.strokeStyle=t.color+'60';cx.lineWidth=1.5;cx.stroke();
        }
        // Tower body
        cx.fillStyle='#071520';
        cx.fillRect(t.x-12,t.y-12,24,24);
        cx.strokeStyle=t.color;cx.lineWidth=2;
        cx.strokeRect(t.x-12,t.y-12,24,24);
        // Tower emoji
        cx.font='16px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(t.emoji,t.x,t.y);
        // Kill count
        if(t.kills>0){
            cx.font='8px sans-serif';cx.fillStyle=t.color;
            cx.fillText(t.kills+'💀',t.x,t.y+16);
        }
    });

    // Enemies
    enemies.forEach(e=>{
        // HP bar
        const bw=24;
        cx.fillStyle='#1e293b'; cx.fillRect(e.x-bw/2,e.y-18,bw,4);
        cx.fillStyle=e.hp/e.maxHp>0.5?'#10b981':'#ef4444';
        cx.fillRect(e.x-bw/2,e.y-18,bw*Math.max(0,e.hp/e.maxHp),4);
        // Emoji
        cx.font='18px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(e.emoji,e.x,e.y);
    });

    // Bullets
    bullets.forEach(b=>{
        cx.beginPath();cx.arc(b.x,b.y,b.r,0,Math.PI*2);
        cx.fillStyle=b.color;cx.fill();
        cx.shadowColor=b.color;cx.shadowBlur=6;cx.fill();
        cx.shadowBlur=0;
    });

    // Particles
    particles.forEach(p=>{
        cx.beginPath();cx.arc(p.x,p.y,p.r,0,Math.PI*2);
        cx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,'0');
        cx.fill();
    });

    // Wave progress bar
    if(waveActive){
        const pct=spawnCount/spawnTotal;
        cx.fillStyle='#1e293b';cx.fillRect(0,H-4,W,4);
        cx.fillStyle='#10b981';cx.fillRect(0,H-4,W*pct,4);
    }
}

function loop(){frameId=requestAnimationFrame(loop);update();draw();}

// ── HELPERS ───────────────────────────────────────────────────────────────────
function selectTower(type){
    selectedType=type;
    document.querySelectorAll('.tower-btn').forEach(b=>b.classList.remove('active'));
    document.getElementById('tb-'+type).classList.add('active');
    const t=TOWERS[type];
    setMsg('Selected: '+t.emoji+' '+t.name+' ('+t.fips+') — Cost: '+t.cost+' 💰');
}
function spawnParticles(x,y,color,n){
    for(let i=0;i<n;i++){
        const a=Math.random()*Math.PI*2,s=1+Math.random()*3;
        particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,r:2+Math.random()*2,alpha:1,color});
    }
}
function updateHUD(){
    document.getElementById('h-gold').textContent=gold;
    document.getElementById('h-lives').textContent=lives;
    document.getElementById('h-wave').textContent=wave;
    document.getElementById('h-kills').textContent=kills;
    document.getElementById('h-score').textContent=score;
}
function setMsg(m){document.getElementById('msg-bar').textContent=m;}
let factTimer=null;
function showFact(t){
    const el=document.getElementById('fact-box');
    el.textContent=t;el.style.display='block';
    if(factTimer)clearTimeout(factTimer);
    factTimer=setTimeout(()=>el.style.display='none',6000);
}
function confetti(){
    const cols=['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444'];
    for(let i=0;i<25;i++){
        setTimeout(()=>{
            const el=document.createElement('div');
            el.className='cp';el.style.left=Math.random()*100+'vw';
            el.style.background=cols[Math.floor(Math.random()*cols.length)];
            el.style.animationDuration=(1+Math.random()*2)+'s';
            document.body.appendChild(el);
            setTimeout(()=>el.remove(),3000);
        },i*40);
    }
}

updateHUD();
loop();
setMsg('Click any grid tile to place a tower! Avoid the path tiles.');
</script>
</body>
</html>
""", height=600)

def render_zombie_blast(difficulty: str = "easy"):
    """Elementary: Zombie Blast — tap to shoot Shor Zombies, collect PQC shields."""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("🧟 Quantum Zombie Blast!")
    st.markdown(
        "**Shor Zombies are attacking your server!** "
        "Click/tap zombies to blast them! "
        "Spacebar shoots the nearest zombie. Keys 1-4 switch weapons!"
    )
    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow:hidden;}
#wrap{max-width:580px;margin:0 auto;padding:8px;}
.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-bottom:6px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:5px 3px;text-align:center;font-size:9px;color:#60a5fa;}
.hb b{display:block;font-size:14px;color:white;}
#server-hp-wrap{width:100%;background:#071520;border:1px solid #ef444440;border-radius:8px;padding:5px 10px;margin-bottom:6px;display:flex;align-items:center;gap:8px;}
#server-label{font-size:10px;color:#ef4444;white-space:nowrap;}
#server-bar-bg{flex:1;height:10px;background:#1e293b;border-radius:5px;}
#server-bar{height:10px;border-radius:5px;transition:width 0.3s;background:linear-gradient(90deg,#ef4444,#fbbf24,#10b981);}
#server-pct{font-size:10px;color:#10b981;white-space:nowrap;font-weight:bold;}
#cv{border:2px solid #1d4ed8;border-radius:10px;display:block;cursor:crosshair;box-shadow:0 0 20px rgba(29,78,216,0.2);}
#weapon-bar{display:flex;gap:4px;justify-content:center;margin-top:5px;flex-wrap:wrap;}
.wpn-btn{padding:5px 10px;border-radius:8px;border:2px solid #1a3a5a;background:#071520;color:#94a3b8;font-size:10px;cursor:pointer;transition:all 0.15s;}
.wpn-btn.active{border-color:#fbbf24;background:#1a1500;color:#fbbf24;}
.wpn-btn.locked{opacity:0.3;cursor:not-allowed;}
.btns{display:flex;gap:4px;margin-top:5px;}
.btn{flex:1;padding:7px;border-radius:8px;border:none;cursor:pointer;font-size:11px;font-weight:bold;color:white;}
.btn-start{background:linear-gradient(135deg,#059669,#10b981);}
.btn-reset{background:#334155;}
#msg-bar{background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:5px 12px;width:100%;margin-top:5px;font-size:10px;color:#60a5fa;text-align:center;min-height:22px;}
#fact-box{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);border-radius:8px;padding:6px 10px;margin-top:4px;font-size:10px;color:#93c5fd;display:none;line-height:1.5;width:100%;text-align:center;}
.cp{position:fixed;pointer-events:none;z-index:999;width:8px;height:8px;border-radius:2px;animation:cf linear forwards;}
@keyframes cf{0%{transform:translateY(-20px) rotate(0deg);opacity:1;}100%{transform:translateY(600px) rotate(720deg);opacity:0;}}
</style>
</head>
<body>
<div id="wrap">
<div class="hud">
    <div class="hb">⭐ Score<br><b id="h-score">0</b></div>
    <div class="hb">🌊 Wave<br><b id="h-wave">1</b>/10</div>
    <div class="hb">💎 Crystals<br><b id="h-crystals">0</b></div>
    <div class="hb">🔥 Combo<br><b id="h-combo">x1</b></div>
</div>
<div id="server-hp-wrap">
    <span id="server-label">🖥️ Server:</span>
    <div id="server-bar-bg"><div id="server-bar" style="width:100%"></div></div>
    <span id="server-pct">100%</span>
</div>
<canvas id="cv" width="560" height="340"></canvas>
<div id="weapon-bar">
    <div class="wpn-btn active" id="wp-kyber" onclick="selectWeapon('kyber')">🔐 ML-KEM [1]</div>
    <div class="wpn-btn locked" id="wp-dilithium" onclick="selectWeapon('dilithium')">✍️ ML-DSA [2]</div>
    <div class="wpn-btn locked" id="wp-sphincs" onclick="selectWeapon('sphincs')">🌲 SPHINCS+ [3]</div>
    <div class="wpn-btn locked" id="wp-falcon" onclick="selectWeapon('falcon')">🦅 Falcon [4]</div>
</div>
<div class="btns">
    <button class="btn btn-start" id="start-btn" onclick="startGame()">▶ Start!</button>
    <button class="btn btn-reset" onclick="resetGame()">🔄 Reset</button>
</div>
<div id="msg-bar">Click START to defend your server! Spacebar = shoot nearest zombie</div>
<div id="fact-box"></div>
</div>
<script>
var cv = document.getElementById('cv');
var cx = cv.getContext('2d');
var W = 560, H = 340;

var WEAPONS = {
    kyber:     {name:'ML-KEM',   emoji:'🔐', color:'#10b981', dmg:1,  splash:0,  unlockAt:0,    upgrades:['ML-KEM-512','ML-KEM-768','ML-KEM-1024'], baseDmg:1,  fact:'ML-KEM (Kyber FIPS 203) blasts enemies with lattice math!'},
    dilithium: {name:'ML-DSA',   emoji:'✍️',  color:'#3b82f6', dmg:2,  splash:0,  unlockAt:200,  upgrades:['ML-DSA-44','ML-DSA-65','ML-DSA-87'],    baseDmg:2,  fact:'ML-DSA (Dilithium FIPS 204) fires signature bolts!'},
    sphincs:   {name:'SPHINCS+', emoji:'🌲', color:'#8b5cf6', dmg:1,  splash:60, unlockAt:500,  upgrades:['SPHINCS-128s','SPHINCS-192s','SPHINCS-256s'], baseDmg:1, fact:'SLH-DSA (SPHINCS+ FIPS 205) fires a hash storm!'},
    falcon:    {name:'Falcon',   emoji:'🦅', color:'#f59e0b', dmg:5,  splash:0,  unlockAt:1000, upgrades:['Falcon-512','Falcon-1024','Falcon-MAX'],  baseDmg:5,  fact:'FN-DSA (Falcon FIPS 206) fires compact NTRU spikes!'},
};
// Weapon upgrade levels (0=base, 1=mid, 2=max)
var weaponLevels = {kyber:0, dilithium:0, sphincs:0, falcon:0};

function getWeaponDmg(type) {
    var w = WEAPONS[type];
    return w.baseDmg * (1 + weaponLevels[type] * 0.8);
}
function getWeaponSplash(type) {
    var w = WEAPONS[type];
    return w.splash > 0 ? w.splash + weaponLevels[type] * 20 : 0;
}
function upgradeWeapons() {
    // Auto-upgrade weapons every 2 waves
    var lvl = Math.min(Math.floor((wave-1)/3), 2);
    ['kyber','dilithium','sphincs','falcon'].forEach(function(k){
        if (unlockedWeapons.includes(k) && weaponLevels[k] < lvl) {
            weaponLevels[k] = lvl;
            var w = WEAPONS[k];
            addFloat(W/2, H/2-20, w.emoji+' '+w.upgrades[lvl]+' UPGRADED!', w.color);
            showFact(w.emoji+' '+w.name+' upgraded to '+w.upgrades[lvl]+'! Damage: '+getWeaponDmg(k).toFixed(1));
        }
    });
    updateWeaponBar();
}

var ZOMBIE_TYPES = [
    {emoji:'🧟', hp:4,  speed:0.4, pts:10,  color:'#10b981', name:'Baby Shor'},
    {emoji:'👾', hp:6,  speed:0.6, pts:15,  color:'#3b82f6', name:'Shor Bot'},
    {emoji:'🤖', hp:10, speed:0.8, pts:25,  color:'#ef4444', name:'RSA Zombie'},
    {emoji:'💀', hp:16, speed:1.0, pts:40,  color:'#8b5cf6', name:'Grover Ghost'},
    {emoji:'👑', hp:40, speed:0.5, pts:100, color:'#fbbf24', name:'Quantum Boss'},
];

var FACTS = [
    'ML-KEM (Kyber FIPS 203) protects key exchange with lattice math!',
    'ML-DSA (Dilithium FIPS 204) creates unbreakable digital signatures!',
    'SLH-DSA (SPHINCS+ FIPS 205) uses SHA-3 hash trees!',
    'FN-DSA (Falcon FIPS 206) makes tiny quantum-safe signatures!',
];

// Game state
var zombies = [], bullets = [], particles = [], floatTexts = [], crystals = [];
var score = 0, wave = 1, combo = 1, comboTimer = 0, serverHp = 100;
var serverMaxHp = 100;
function getServerMaxHp() { return 100 + (wave-1) * 20; } // +20 HP per wave
var crystalCount = 0, gameActive = false, frameId = null;
var selectedWeapon = 'kyber', unlockedWeapons = ['kyber'];
var spawnTimer = 0, spawnCount = 0, spawnTotal = 0, waveClearing = false;
var mouseX = W/2, mouseY = H/2;
var bgStars = [];
for (var si = 0; si < 60; si++) {
    bgStars.push({x:Math.random()*W, y:Math.random()*H, r:Math.random()*1.5, a:Math.random()*0.5+0.2});
}

function startGame() {
    zombies=[]; bullets=[]; particles=[]; crystals=[]; floatTexts=[];
    score=0; wave=1; combo=1; comboTimer=0; serverHp=100; serverMaxHp=100;
    weaponLevels={kyber:0,dilithium:0,sphincs:0,falcon:0};
    crystalCount=0; waveClearing=false; spawnCount=0; spawnTimer=0;
    unlockedWeapons=['kyber']; selectedWeapon='kyber';
    updateWeaponBar();
    startWave();
    gameActive=true;
    if (frameId) cancelAnimationFrame(frameId);
    frameId = requestAnimationFrame(loop);
    document.getElementById('start-btn').disabled = true;
    updateHUD();
    setMsg('Wave 1 starting! Click zombies or press SPACE to blast them!');
}

function startWave() {
    spawnTotal = 8 + wave * 3;
    spawnCount = 0; spawnTimer = 0; waveClearing = false;
    var zombieType = ZOMBIE_TYPES[Math.min(Math.floor(wave/2), ZOMBIE_TYPES.length-1)];
    setMsg('Wave ' + wave + ': ' + spawnTotal + 'x ' + zombieType.name + ' incoming!');
}

function spawnZombie() {
    var waveIdx = Math.min(Math.floor(wave/2), ZOMBIE_TYPES.length-1);
    var type = ZOMBIE_TYPES[waveIdx];
    var fromLeft = spawnCount % 2 === 0;
    var speed = type.speed * (1 + wave * 0.08);
    zombies.push({
        x: fromLeft ? 10 : W-10,
        y: 80 + Math.random() * (H-160),
        vx: fromLeft ? speed * 0.9 : -speed * 1.8,
        vy: (Math.random()-0.5) * 0.3,
        hp: type.hp * (1 + wave * 0.2),
        maxHp: type.hp * (1 + wave * 0.2),
        emoji: type.emoji, color: type.color,
        pts: type.pts, r: 18,
        wobble: Math.random() * Math.PI * 2,
        id: Math.random(),
    });
}

// Click to shoot
cv.addEventListener('click', function(e) {
    if (!gameActive) return;
    var rect = cv.getBoundingClientRect();
    var mx = (e.clientX-rect.left)*(W/rect.width);
    var my = (e.clientY-rect.top)*(H/rect.height);
    // Check crystal
    for (var ci = crystals.length-1; ci >= 0; ci--) {
        var c = crystals[ci];
        if (Math.hypot(c.x-mx, c.y-my) < 20) {
            crystals.splice(ci, 1);
            crystalCount++;
            score += 100;
            showFact(FACTS[crystalCount%FACTS.length]);
            addFloat(mx, my, '💎+100', '#fbbf24');
            confetti();
            checkUnlocks();
            updateHUD();
            return;
        }
    }
    shoot(mx, my);
});

cv.addEventListener('mousemove', function(e) {
    var rect = cv.getBoundingClientRect();
    mouseX = (e.clientX-rect.left)*(W/rect.width);
    mouseY = (e.clientY-rect.top)*(H/rect.height);
});

cv.addEventListener('touchstart', function(e) {
    if (!gameActive) return;
    e.preventDefault();
    var rect = cv.getBoundingClientRect();
    var t = e.touches[0];
    var mx = (t.clientX-rect.left)*(W/rect.width);
    var my = (t.clientY-rect.top)*(H/rect.height);
    shoot(mx, my);
}, {passive:false});

function shoot(mx, my) {
    var wpn = WEAPONS[selectedWeapon];
    var hit = null;
    for (var zi = 0; zi < zombies.length; zi++) {
        if (Math.hypot(zombies[zi].x-mx, zombies[zi].y-my) < zombies[zi].r+10) {
            hit = zombies[zi]; break;
        }
    }
    if (hit) {
        if (wpn.splash > 0) {
            for (var si2 = zombies.length-1; si2 >= 0; si2--) {
                if (Math.hypot(zombies[si2].x-hit.x, zombies[si2].y-hit.y) < wpn.splash) {
                    damageZombie(zombies[si2], wpn.dmg);
                }
            }
            spawnParticles(hit.x, hit.y, wpn.color, 15);
        } else {
            damageZombie(hit, wpn.dmg);
        }
        combo = Math.min(combo+1, 8);
        comboTimer = 90;
    } else {
        bullets.push({x:W/2, y:H+20, tx:mx, ty:my, speed:8, dmg:wpn.dmg, color:wpn.color, emoji:wpn.emoji, splash:wpn.splash, id:Math.random()});
        combo = Math.max(1, combo-1);
    }
    spawnParticles(mx, my, wpn.color, 4);
    updateHUD();
}

function damageZombie(z, dmg) {
    z.hp -= dmg * combo * (1 + weaponLevels[selectedWeapon]*0.8);
    spawnParticles(z.x, z.y, z.color, 6);
    addFloat(z.x, z.y, '-'+(dmg*combo), z.color);
    if (z.hp <= 0) killZombie(z);
}

function killZombie(z) {
    zombies = zombies.filter(function(zz){return zz!==z;});
    var pts = z.pts * combo;
    score += pts;
    addFloat(z.x, z.y, '+'+pts+'⭐', '#fbbf24');
    spawnParticles(z.x, z.y, '#fbbf24', 10);
    if (Math.random() < 0.3) {
        var ci = crystalCount % 4;
        crystals.push({x:z.x, y:z.y, emoji:['🔐','✍️','🌲','🦅'][ci], color:['#10b981','#3b82f6','#8b5cf6','#f59e0b'][ci], id:Math.random(), timer:180, ci:ci});
    }
    checkUnlocks();
    updateHUD();
}

function checkUnlocks() {
    if (score>=200 && !unlockedWeapons.includes('dilithium')) { unlockedWeapons.push('dilithium'); showFact('✍️ ML-DSA UNLOCKED! Double damage!'); updateWeaponBar(); }
    if (score>=500 && !unlockedWeapons.includes('sphincs'))   { unlockedWeapons.push('sphincs');   showFact('🌲 SPHINCS+ UNLOCKED! Splash damage!'); updateWeaponBar(); }
    if (score>=1000&& !unlockedWeapons.includes('falcon'))    { unlockedWeapons.push('falcon');    showFact('🦅 Falcon UNLOCKED! 5x damage!'); updateWeaponBar(); }
}

function update() {
    if (!gameActive) return;
    if (comboTimer > 0) { comboTimer--; if (comboTimer===0) combo = Math.max(1,combo-1); }
    if (spawnCount < spawnTotal) {
        spawnTimer++;
        if (spawnTimer >= 15) { spawnTimer=0; spawnCount++; spawnZombie(); }
    }
    // Move zombies toward server
    for (var zi = zombies.length-1; zi >= 0; zi--) {
        var z = zombies[zi];
        z.wobble += 0.08;
        var dx = W/2-z.x, dy = H*0.85-z.y;
        var d = Math.sqrt(dx*dx+dy*dy) || 1;
        z.x += (dx/d) * Math.abs(z.vx);
        z.y += (dy/d) * Math.abs(z.vx) * 0.3 + z.vy;
        if (d < 50) {
            serverHp -= 0.5;
            updateServerHp();
            if (serverHp <= 0) { gameOver(); return; }
        }
    }
    // Move bullets
    for (var bi = bullets.length-1; bi >= 0; bi--) {
        var b = bullets[bi];
        var bdx = b.tx-b.x, bdy = b.ty-b.y;
        var bd = Math.sqrt(bdx*bdx+bdy*bdy) || 1;
        b.x += bdx/bd*b.speed; b.y += bdy/bd*b.speed;
        if (bd < b.speed+4) {
            if (b.splash > 0) {
                for (var si3 = zombies.length-1; si3 >= 0; si3--) {
                    if (Math.hypot(zombies[si3].x-b.tx, zombies[si3].y-b.ty) < b.splash) damageZombie(zombies[si3], b.dmg);
                }
            } else {
                var bh = null;
                for (var bzi = 0; bzi < zombies.length; bzi++) {
                    if (Math.hypot(zombies[bzi].x-b.tx, zombies[bzi].y-b.ty) < zombies[bzi].r+10) { bh=zombies[bzi]; break; }
                }
                if (bh) damageZombie(bh, b.dmg);
            }
            bullets.splice(bi, 1);
        } else if (b.y < -20 || b.y > H+20) { bullets.splice(bi, 1); }
    }
    // Crystal timers
    for (var ci2 = crystals.length-1; ci2 >= 0; ci2--) {
        crystals[ci2].timer--;
        if (crystals[ci2].timer <= 0) {
            crystalCount++;
            score += 50;
            addFloat(crystals[ci2].x, crystals[ci2].y, '💎+50', '#fbbf24');
            crystals.splice(ci2, 1);
            updateHUD();
        }
    }
    // Particles
    for (var pi = particles.length-1; pi >= 0; pi--) {
        var p = particles[pi];
        p.x+=p.vx; p.y+=p.vy; p.vy+=0.08; p.alpha-=0.03; p.r*=0.95;
        if (p.alpha <= 0) particles.splice(pi, 1);
    }
    // Float texts
    for (var fi = floatTexts.length-1; fi >= 0; fi--) {
        floatTexts[fi].timer--;
        if (floatTexts[fi].timer <= 0) floatTexts.splice(fi, 1);
    }
    // Wave clear
    if (spawnCount >= spawnTotal && zombies.length === 0 && !waveClearing) {
        waveClearing = true;
        waveComplete();
    }
}

function waveComplete() {
    var bonus = wave * 100;
    score += bonus;
    wave++;
    // Refill server HP to new max
    serverMaxHp = getServerMaxHp();
    serverHp = serverMaxHp;
    updateServerHp();
    // Upgrade weapons
    upgradeWeapons();
    updateHUD();
    addFloat(W/2, H/2, 'Wave Clear! +'+bonus+'⭐', '#fbbf24');
    setMsg('Wave '+(wave-1)+' cleared! +'+bonus+' bonus! Server HP refilled to '+serverMaxHp+'! Wave '+wave+' starting...');
    if (wave > 10) { victory(); return; }
    setTimeout(function() { startWave(); waveClearing=false; }, 1200);
}

function victory() {
    gameActive = false;
    setMsg('👑 ALL 10 WAVES DEFEATED! Score: '+score);
    confetti();
    document.getElementById('start-btn').disabled = false;
}

function gameOver() {
    gameActive = false;
    serverHp = 0; updateServerHp();
    setMsg('💀 SERVER DESTROYED! Wave: '+wave+' | Score: '+score);
    document.getElementById('start-btn').disabled = false;
}

function resetGame() {
    if (frameId) cancelAnimationFrame(frameId);
    gameActive = false;
    zombies=[]; bullets=[]; particles=[]; crystals=[]; floatTexts=[];
    score=0; wave=1; combo=1; comboTimer=0; serverHp=100; serverMaxHp=100;
    weaponLevels={kyber:0,dilithium:0,sphincs:0,falcon:0};
    crystalCount=0; unlockedWeapons=['kyber']; selectedWeapon='kyber';
    document.getElementById('start-btn').disabled = false;
    updateHUD(); updateServerHp(); updateWeaponBar();
    setMsg('Click START to defend your server!');
    document.getElementById('fact-box').style.display='none';
}

function draw() {
    cx.clearRect(0,0,W,H);
    cx.fillStyle='#020d14'; cx.fillRect(0,0,W,H);
    bgStars.forEach(function(s) { cx.beginPath(); cx.arc(s.x,s.y,s.r,0,6.28); cx.fillStyle='rgba(255,255,255,'+s.a+')'; cx.fill(); });
    cx.fillStyle='#0a1f35'; cx.fillRect(0,H*0.85,W,H*0.15);
    cx.strokeStyle='#1d4ed840'; cx.lineWidth=2;
    cx.beginPath(); cx.moveTo(0,H*0.85); cx.lineTo(W,H*0.85); cx.stroke();
    // Server
    cx.font='28px serif'; cx.textAlign='center'; cx.textBaseline='middle';
    cx.shadowColor=serverHp>50?'#10b981':'#ef4444'; cx.shadowBlur=15;
    cx.fillText('🖥️',W/2,H*0.85+20); cx.shadowBlur=0;
    // Crystals
    crystals.forEach(function(c) {
        cx.font='18px serif'; cx.textAlign='center'; cx.textBaseline='middle';
        cx.shadowColor=c.color; cx.shadowBlur=12;
        cx.fillText(c.emoji, c.x, c.y-Math.sin(Date.now()*0.003+c.id*5)*6);
        cx.shadowBlur=0;
    });
    // Zombies
    zombies.forEach(function(z) {
        cx.font='26px serif'; cx.textAlign='center'; cx.textBaseline='middle';
        cx.shadowColor=z.color; cx.shadowBlur=8;
        cx.fillText(z.emoji, z.x+Math.sin(z.wobble)*3, z.y+Math.cos(z.wobble*0.7)*2);
        cx.shadowBlur=0;
        var bw=28;
        cx.fillStyle='#1e293b'; cx.fillRect(z.x-bw/2,z.y-24,bw,4);
        cx.fillStyle=z.hp/z.maxHp>0.5?'#10b981':'#ef4444';
        cx.fillRect(z.x-bw/2,z.y-24,bw*Math.max(0,z.hp/z.maxHp),4);
    });
    // Bullets
    bullets.forEach(function(b) {
        cx.font='16px serif'; cx.textAlign='center'; cx.textBaseline='middle';
        cx.shadowColor=b.color; cx.shadowBlur=10;
        cx.fillText(b.emoji,b.x,b.y); cx.shadowBlur=0;
    });
    // Particles
    particles.forEach(function(p) {
        cx.beginPath(); cx.arc(p.x,p.y,p.r,0,6.28);
        cx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,'0');
        cx.fill();
    });
    // Float texts
    floatTexts.forEach(function(f) {
        var alpha = f.timer/40;
        cx.font='bold 14px sans-serif'; cx.textAlign='center';
        cx.fillStyle=f.color+Math.floor(alpha*255).toString(16).padStart(2,'0');
        cx.fillText(f.text, f.x, f.y-(1-f.timer/40)*30);
    });
    if (combo > 1) {
        cx.font='bold '+(14+combo)+'px sans-serif'; cx.textAlign='left';
        cx.fillStyle='#fbbf24';
        cx.fillText('🔥 x'+combo+' COMBO!',8,20);
    }
    var wpn = WEAPONS[selectedWeapon];
    cx.font='11px sans-serif'; cx.textAlign='right'; cx.fillStyle=wpn.color;
    cx.fillText(wpn.emoji+' '+wpn.name, W-8, 20);
}

function loop() {
    frameId = requestAnimationFrame(loop);
    update();
    draw();
}

function selectWeapon(type) {
    if (!unlockedWeapons.includes(type)) { setMsg('🔒 Score more to unlock '+WEAPONS[type].name+'!'); return; }
    selectedWeapon = type;
    updateWeaponBar();
    setMsg('Selected: '+WEAPONS[type].emoji+' '+WEAPONS[type].name);
}

function updateWeaponBar() {
    ['kyber','dilithium','sphincs','falcon'].forEach(function(k) {
        var el = document.getElementById('wp-'+k);
        if (!el) return;
        el.className = 'wpn-btn' + (k===selectedWeapon?' active':'') + (unlockedWeapons.includes(k)?'':' locked');
        var w = WEAPONS[k];
        var stars = ['','⭐','⭐⭐'][weaponLevels[k]||0];
        var lvlName = w.upgrades ? w.upgrades[weaponLevels[k]||0] : w.name;
        el.innerHTML = w.emoji+' '+w.name+(stars?' '+stars:'')+'<br><span style="font-size:7px;color:#475569">'+(unlockedWeapons.includes(k)?lvlName:'🔒 Score '+w.unlockAt)+'</span>';
    });
}

function spawnParticles(x,y,color,n) {
    for (var i=0;i<n;i++) {
        var a=Math.random()*6.28, s=1+Math.random()*3;
        particles.push({x:x,y:y,vx:Math.cos(a)*s,vy:Math.sin(a)*s-1,r:2+Math.random()*3,alpha:1,color:color});
    }
}

function addFloat(x,y,text,color) { floatTexts.push({x:x,y:y,text:text,color:color,timer:40}); }

function updateHUD() {
    document.getElementById('h-score').textContent=score;
    document.getElementById('h-wave').textContent=wave;
    document.getElementById('h-crystals').textContent=crystalCount;
    document.getElementById('h-combo').textContent='x'+combo;
}

function updateServerHp() {
    var pct=Math.max(0,serverHp/serverMaxHp*100);
    document.getElementById('server-bar').style.width=pct+'%';
    document.getElementById('server-pct').textContent=Math.round(serverHp)+'/'+serverMaxHp;
    document.getElementById('server-pct').style.color=pct>50?'#10b981':pct>25?'#fbbf24':'#ef4444';
    document.getElementById('server-bar').style.background=pct>50?'linear-gradient(90deg,#10b981,#34d399)':pct>25?'linear-gradient(90deg,#fbbf24,#f97316)':'linear-gradient(90deg,#ef4444,#dc2626)';
}

function setMsg(m) { document.getElementById('msg-bar').textContent=m; }

var factTimer=null;
function showFact(t) {
    var el=document.getElementById('fact-box');
    el.textContent=t; el.style.display='block';
    if (factTimer) clearTimeout(factTimer);
    factTimer=setTimeout(function(){el.style.display='none';},6000);
}

function confetti() {
    var cols=['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444'];
    for (var i=0;i<20;i++) {
        setTimeout(function() {
            var el=document.createElement('div'); el.className='cp';
            el.style.left=Math.random()*100+'vw';
            el.style.background=cols[Math.floor(Math.random()*cols.length)];
            el.style.animationDuration=(1+Math.random()*2)+'s';
            document.body.appendChild(el);
            setTimeout(function(){el.remove();},3000);
        },i*40);
    }
}

// Keyboard controls
document.addEventListener('keydown', function(e) {
    if (e.key===' ' && gameActive) {
        e.preventDefault();
        // Shoot toward current mouse position
        shoot(mouseX, mouseY);
    }
    if (e.key==='1') selectWeapon('kyber');
    if (e.key==='2') selectWeapon('dilithium');
    if (e.key==='3') selectWeapon('sphincs');
    if (e.key==='4') selectWeapon('falcon');
});

// Init
updateHUD();
updateServerHp();
cx.fillStyle='#020d14'; cx.fillRect(0,0,W,H);
cx.font='bold 22px sans-serif'; cx.fillStyle='#60a5fa'; cx.textAlign='center';
cx.fillText('🧟 Quantum Zombie Blast',W/2,H/2-20);
cx.font='12px sans-serif'; cx.fillStyle='#94a3b8';
cx.fillText('Click START to defend your server!',W/2,H/2+10);
</script>
</body>
</html>
""", height=580)

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
            <span>Lives:<span id="qlives">❤️❤️❤️</span></span>
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
    let world=[],player,enemies,inventory,score,qhp,level,running,mined,keys={},lives=3;
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
        score=0;qhp=100;level=1;running=true;mined=0;lives=3;
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
                    if(mined>=level*8){
                        level++;
                        document.getElementById('qlevel').textContent=level;
                        document.getElementById('qc-msg').textContent=
                            '🎉 LEVEL '+level+'! More creepers! Mine '+level*8+' blocks to advance!';
                        genWorld();
                        enemies=[];
                        for(let i=0;i<level+2;i++) spawnC();
                        // Speed up creepers each level
                        enemies.forEach(e=>{ e.rate=Math.max(20, 45-level*3); });
                        score+=level*50;
                        updateUI();
                    }
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
        document.getElementById('qmined').textContent=mined;
        document.getElementById('qlevel').textContent=level;
        document.getElementById('slot-kyber').textContent='Kyber:'+inventory.kyber;
        document.getElementById('slot-lattice').textContent='Lattice:'+inventory.lattice;
        document.getElementById('slot-hash').textContent='Hash:'+inventory.hash;
        document.getElementById('slot-key').textContent='Keys:'+inventory.key;
        var lv=document.getElementById('qlives');
        if(lv) lv.textContent='❤️'.repeat(Math.max(0,lives));
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
            // Keep minimum creeper population
            if(enemies.length<2+Math.floor(level/2)) spawnC();
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
                    lives--;
                    enemies.splice(i,1);
                    setTimeout(()=>{if(running) spawnC();}, 2000);
                    document.getElementById('qc-msg').textContent='💀 Lost a life! '+lives+' lives left!';
                    // Flash player red
                    qhp=100;
                    updateUI();
                    if(lives<=0){
                        running=false;
                        qx.fillStyle='rgba(0,0,0,0.85)';qx.fillRect(0,0,480,400);
                        qx.fillStyle='#ef4444';qx.font='bold 26px sans-serif';qx.textAlign='center';
                        qx.fillText('Game Over! Score:'+score,240,185);
                        qx.fillStyle='white';qx.font='16px sans-serif';
                        qx.fillText('Press Start to play again!',240,220);
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
        enemies.forEach(e=>{
            qx.font='22px sans-serif';qx.textAlign='center';
            qx.shadowColor='#ef4444';qx.shadowBlur=8;
            qx.fillText('💀',e.x*CELL+20,e.y*CELL+28);
            qx.shadowBlur=0;
        });
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
    """6-8: QuantumCraft Lattice Mines — UPGRADED 2026 — deeper caves, PQC boss, glow crystals."""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("⛏️ QuantumCraft — Lattice Mines!")
    st.markdown(
        "Dig deep into the **quantum lattice mines**! "
        "Mine PQC crystals, avoid Shor Bots, and find the portal to go deeper. "
        "**WASD** to move, **E** to mine, **F** to place walls."
    )
    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow:hidden;}
#wrap{max-width:560px;margin:0 auto;padding:8px;}
.hud{display:grid;grid-template-columns:repeat(5,1fr);gap:3px;margin-bottom:6px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:6px;padding:4px 2px;
    text-align:center;font-size:8px;color:#60a5fa;}
.hb b{display:block;font-size:13px;color:white;}
#cv{border:2px solid #8b5cf6;border-radius:10px;display:block;}
#inv-bar{display:flex;gap:4px;justify-content:center;margin-top:5px;flex-wrap:wrap;}
.inv-slot{padding:3px 8px;border-radius:6px;border:1px solid #1a3a5a;background:#071520;
    font-size:10px;color:#94a3b8;min-width:70px;text-align:center;}
#msg{background:#071520;border:1px solid #1a3a5a;border-radius:8px;
    padding:4px 10px;margin-top:5px;font-size:10px;color:#60a5fa;text-align:center;}
.btns{display:flex;gap:4px;margin-top:5px;}
.btn{flex:1;padding:7px;border-radius:8px;border:none;cursor:pointer;
    font-size:11px;font-weight:bold;color:white;}
.btn-start{background:linear-gradient(135deg,#7c3aed,#8b5cf6);}
.btn-reset{background:#334155;}
.cp{position:fixed;pointer-events:none;z-index:999;width:8px;height:8px;
    border-radius:2px;animation:cf linear forwards;}
@keyframes cf{0%{transform:translateY(-20px) rotate(0deg);opacity:1;}
    100%{transform:translateY(500px) rotate(720deg);opacity:0;}}
</style>
</head>
<body>
<div id="wrap">
<div class="hud">
    <div class="hb">❤️ HP<br><b id="h-hp">100</b></div>
    <div class="hb">⭐ Score<br><b id="h-score">0</b></div>
    <div class="hb">⛏️ Mined<br><b id="h-mined">0</b></div>
    <div class="hb">🌊 Depth<br><b id="h-depth">1</b></div>
    <div class="hb">🔐 PQC<br><b id="h-pqc">0</b></div>
</div>
<canvas id="cv" width="560" height="360"></canvas>
<div id="inv-bar">
    <div class="inv-slot" id="sl-kyber">🔐 Kyber:0</div>
    <div class="inv-slot" id="sl-dil">✍️ ML-DSA:0</div>
    <div class="inv-slot" id="sl-sph">🌲 SPHINCS:0</div>
    <div class="inv-slot" id="sl-fal">🦅 Falcon:0</div>
</div>
<div id="msg">WASD to move, E to mine, F to place wall. Find the portal to go deeper!</div>
<div class="btns">
    <button class="btn btn-start" onclick="startGame()">⛏️ Start Mining!</button>
    <button class="btn btn-reset" onclick="resetGame()">🔄 Reset</button>
</div>
</div>
<script>
var cv=document.getElementById('cv'),cx=cv.getContext('2d');
var W=560,H=360,TS=28,COLS=20,ROWS=13;

var BLOCKS={
    air:   {color:'',        solid:false,mine:false},
    stone: {color:'#374151', solid:true, mine:true,  drop:'stone',   pts:2,  hard:3, emoji:''},
    dirt:  {color:'#7c4f2a', solid:true, mine:true,  drop:'dirt',    pts:1,  hard:1, emoji:''},
    kyber: {color:'#10b981', solid:true, mine:true,  drop:'kyber',   pts:20, hard:2, emoji:'🔐', glow:'#10b981'},
    dil:   {color:'#3b82f6', solid:true, mine:true,  drop:'dil',     pts:25, hard:3, emoji:'✍️',  glow:'#3b82f6'},
    sph:   {color:'#8b5cf6', solid:true, mine:true,  drop:'sph',     pts:30, hard:4, emoji:'🌲', glow:'#8b5cf6'},
    fal:   {color:'#f59e0b', solid:true, mine:true,  drop:'fal',     pts:35, hard:5, emoji:'🦅', glow:'#f59e0b'},
    wall:  {color:'#1e293b', solid:true, mine:true,  drop:null,      pts:0,  hard:1, emoji:''},
    bedrock:{color:'#0f172a',solid:true, mine:false, drop:null,      pts:0,  hard:99,emoji:''},
    portal:{color:'#a78bfa', solid:false,mine:false, drop:null,      pts:0,  hard:0, emoji:'🌀', glow:'#a78bfa'},
    loot:  {color:'#fbbf24', solid:false,mine:true,  drop:'loot',    pts:50, hard:1, emoji:'📦'},
    enemy_egg:{color:'#ef4444',solid:true,mine:true, drop:null,      pts:10, hard:1, emoji:'🥚'},
};
var FACTS=[
    'You mined Kyber! ML-KEM FIPS 203 uses Module-LWE lattice math to protect key exchange!',
    'Dilithium mined! ML-DSA FIPS 204 signs every message — quantum computers cannot forge it!',
    'SPHINCS+ found! SLH-DSA FIPS 205 uses SHA-3 hash trees — safe even if lattice math breaks!',
    'Falcon collected! FN-DSA FIPS 206 makes the smallest quantum-safe signatures for IoT!',
    'These crystals represent the 4 NIST PQC standards finalized in August 2024!',
];

// State
var world=[],player={},enemies=[],particles=[],mineProgress=null;
var inventory={kyber:0,dil:0,sph:0,fal:0,stone:0,dirt:0};
var score=0,hp=100,depth=1,mined=0,pqcTotal=0;
var keys={},gameActive=false,camera={x:0,y:0};
var frameId=null;
var PQCCOUNT=0;

function genWorld(d){
    world=[];
    for(var r=0;r<ROWS;r++){
        world[r]=[];
        for(var c=0;c<COLS;c++){
            if(r===0||r===ROWS-1||c===0||c===COLS-1){world[r][c]='bedrock';continue;}
            var rng=Math.random();
            var pqcChance=0.02+d*0.01;
            if(r===ROWS-2&&c===Math.floor(COLS/2)){world[r][c]='portal';continue;}
            if(r<3){world[r][c]=rng<0.3?'stone':rng<0.5?'dirt':'air';}
            else if(r<6){
                if(rng<pqcChance) world[r][c]='kyber';
                else if(rng<0.35) world[r][c]='stone';
                else if(rng<0.5) world[r][c]='dirt';
                else world[r][c]='air';
            } else {
                if(rng<pqcChance*0.5) world[r][c]='fal';
                else if(rng<pqcChance) world[r][c]='sph';
                else if(rng<pqcChance*2) world[r][c]='dil';
                else if(rng<pqcChance*3) world[r][c]='kyber';
                else if(rng<0.45) world[r][c]='stone';
                else if(rng<0.55) world[r][c]='dirt';
                else if(rng<0.58) world[r][c]='loot';
                else world[r][c]='air';
            }
        }
    }
    // Clear player spawn
    for(var dr=-1;dr<=1;dr++) for(var dc=-1;dc<=1;dc++) if(world[2+dr]&&world[2+dr][2+dc]) world[2+dr][2+dc]='air';
    // Spawn enemies
    enemies=[];
    for(var i=0;i<2+d;i++){
        var er=3+Math.floor(Math.random()*(ROWS-5));
        var ec=5+Math.floor(Math.random()*(COLS-8));
        if(world[er][ec]==='air') enemies.push({r:ec*TS+TS/2,y:er*TS+TS/2,vx:0,vy:0,speed:0.7+d*0.15,hp:3,face:'👾',onGround:false});
    }
}

function startGame(){
    depth=1;score=0;hp=100;mined=0;pqcTotal=0;PQCCOUNT=0;
    inventory={kyber:0,dil:0,sph:0,fal:0,stone:0,dirt:0};
    genWorld(depth);
    player={x:2*TS+TS/2,y:2*TS,vx:0,vy:0,onGround:false,mineTimer:0,mineTarget:null,facing:1};
    camera={x:0,y:0};mineProgress=null;
    gameActive=true;particles=[];
    updateHUD();updateInv();
    if(frameId) cancelAnimationFrame(frameId);
    loop();
    setMsg('Mine PQC crystals! Find the 🌀 portal to go deeper!');
}

function resetGame(){gameActive=false;if(frameId)cancelAnimationFrame(frameId);}

// Tile helpers
function getTile(c,r){if(c<0||r<0||c>=COLS||r>=ROWS)return 'bedrock';return world[r][c]||'air';}
function setTile(c,r,t){if(c>=0&&r>=0&&c<COLS&&r<ROWS)world[r][c]=t;}
function isSolid(c,r){return BLOCKS[getTile(c,r)].solid;}

// Player physics
var G=0.4,MAXFALL=10,SPEED=2.5,JUMP=-8;
function updatePlayer(){
    if(!gameActive)return;
    // Input
    var dx=0;
    if(keys['a']||keys['ArrowLeft'])dx=-SPEED;
    if(keys['d']||keys['ArrowRight'])dx=SPEED;
    if(dx!==0)player.facing=dx>0?1:-1;
    player.vx=dx;
    if((keys['w']||keys['ArrowUp']||keys[' '])&&player.onGround){player.vy=JUMP;player.onGround=false;}
    player.vy=Math.min(player.vy+G,MAXFALL);
    // X move
    player.x+=player.vx;
    var tx1=Math.floor((player.x-8)/TS),tx2=Math.floor((player.x+8)/TS);
    var ty1=Math.floor(player.y/TS),ty2=Math.floor((player.y+26)/TS);
    if(player.vx>0){if(isSolid(tx2,ty1)||isSolid(tx2,ty2)){player.x=tx2*TS-8;player.vx=0;}}
    else if(player.vx<0){if(isSolid(tx1,ty1)||isSolid(tx1,ty2)){player.x=(tx1+1)*TS+8;player.vx=0;}}
    // Y move
    player.y+=player.vy;player.onGround=false;
    tx1=Math.floor((player.x-7)/TS);tx2=Math.floor((player.x+7)/TS);
    ty1=Math.floor(player.y/TS);ty2=Math.floor((player.y+26)/TS);
    if(player.vy>0){if(isSolid(tx1,ty2)||isSolid(tx2,ty2)){player.y=ty2*TS-26;player.vy=0;player.onGround=true;}}
    else if(player.vy<0){if(isSolid(tx1,ty1)||isSolid(tx2,ty1)){player.y=(ty1+1)*TS;player.vy=0;}}
    // Bounds
    player.x=Math.max(TS,Math.min(COLS*TS-TS,player.x));
    player.y=Math.max(0,Math.min(ROWS*TS-TS,player.y));
    // Camera
    camera.x=Math.max(0,Math.min(COLS*TS-W,player.x-W/2));
    camera.y=Math.max(0,Math.min(ROWS*TS-H,player.y-H/2));
    // Portal check
    var ptc=Math.floor(player.x/TS),ptr=Math.floor((player.y+13)/TS);
    if(getTile(ptc,ptr)==='portal'){nextDepth();}
}

function doMine(){
    var dirs=[{dc:0,dr:-1},{dc:0,dr:1},{dc:-1,dr:0},{dc:1,dr:0}];
    for(var i=0;i<dirs.length;i++){
        var nc=Math.floor(player.x/TS)+dirs[i].dc;
        var nr=Math.floor((player.y+13)/TS)+dirs[i].dr;
        var bt=getTile(nc,nr);
        var bd=BLOCKS[bt];
        if(bd&&bd.mine){
            if(!mineProgress||mineProgress.c!==nc||mineProgress.r!==nr){
                mineProgress={c:nc,r:nr,prog:0,max:bd.hard*6};
            }
            mineProgress.prog++;
            spawnParticles(nc*TS+TS/2-camera.x,nr*TS+TS/2-camera.y,bd.color||'#888',2);
            if(mineProgress.prog>=mineProgress.max){
                setTile(nc,nr,'air');
                if(bd.drop){
                    inventory[bd.drop]=(inventory[bd.drop]||0)+1;
                    score+=bd.pts;mined++;
                    if(['kyber','dil','sph','fal'].includes(bd.drop)){
                        pqcTotal++;PQCCOUNT++;
                        setMsg(bd.emoji+' '+bd.drop.toUpperCase()+' mined! +'+bd.pts+' pts! '+FACTS[Math.floor(Math.random()*FACTS.length)].substring(0,60)+'...');
                        confetti();
                    }
                    if(bd.drop==='loot'){score+=50;setMsg('📦 Loot chest! +50 pts!');}
                }
                mineProgress=null;
                updateHUD();updateInv();
            }
            return;
        }
    }
    mineProgress=null;
}

function doPlace(){
    if((inventory.stone||0)<=0)return;
    var dirs=[{dc:0,dr:-1},{dc:1,dr:0},{dc:-1,dr:0},{dc:0,dr:1}];
    for(var i=0;i<dirs.length;i++){
        var nc=Math.floor(player.x/TS)+dirs[i].dc;
        var nr=Math.floor((player.y+13)/TS)+dirs[i].dr;
        if(getTile(nc,nr)==='air'){
            setTile(nc,nr,'wall');
            inventory.stone--;
            updateInv();return;
        }
    }
}

function updateEnemies(){
    enemies.forEach(function(e,i){
        e.vy=(e.vy||0)+G;e.vy=Math.min(e.vy,MAXFALL);
        var dx=player.x-e.r,dy=player.y-e.y;
        e.vx=dx>0?e.speed:-e.speed;
        e.r+=e.vx;e.y+=e.vy;e.onGround=false;
        var ec=Math.floor(e.r/TS),er2=Math.floor((e.y+12)/TS);
        if(isSolid(ec,er2)){e.y=er2*TS-12;e.vy=0;e.onGround=true;}
        if(isSolid(ec,Math.floor(e.y/TS))){e.y=(Math.floor(e.y/TS)+1)*TS;e.vy=0;}
        var dist=Math.hypot(e.r-player.x,e.y-player.y);
        if(dist<20){hp=Math.max(0,hp-0.5);updateHUD();if(hp<=0)gameOver();}
    });
}

function nextDepth(){
    depth++;
    score+=depth*100;
    setMsg('🌀 Deeper! Depth '+depth+' — More PQC crystals, faster enemies!');
    genWorld(depth);
    player.x=2*TS+TS/2;player.y=2*TS;player.vy=0;
    mineProgress=null;
    updateHUD();confetti();
}

function gameOver(){
    gameActive=false;
    setMsg('💀 GAME OVER! Score:'+score+' | Depth:'+depth+' | PQC:'+pqcTotal+' — Press Start to try again!');
}

function draw(){
    cx.clearRect(0,0,W,H);
    // Sky/cave background
    var bgG=cx.createLinearGradient(0,0,0,H);
    bgG.addColorStop(0,'#0a0a1a');bgG.addColorStop(1,'#050510');
    cx.fillStyle=bgG;cx.fillRect(0,0,W,H);

    var startC=Math.floor(camera.x/TS),startR=Math.floor(camera.y/TS);
    var endC=Math.min(COLS,startC+Math.ceil(W/TS)+2);
    var endR=Math.min(ROWS,startR+Math.ceil(H/TS)+2);

    for(var r=Math.max(0,startR);r<endR;r++){
        for(var c=Math.max(0,startC);c<endC;c++){
            var bt=world[r][c];if(!bt||bt==='air')continue;
            var bd=BLOCKS[bt];if(!bd)continue;
            var sx=c*TS-camera.x,sy=r*TS-camera.y;
            if(bd.color){
                if(bd.glow){cx.shadowColor=bd.glow;cx.shadowBlur=8;}
                cx.fillStyle=bd.color;cx.fillRect(sx,sy,TS,TS);
                cx.shadowBlur=0;
                // Stone texture
                if(bt==='stone'){cx.strokeStyle='#2d3748';cx.lineWidth=0.5;cx.strokeRect(sx,sy,TS,TS);}
            }
            if(bd.emoji){
                cx.font='14px serif';cx.textAlign='center';cx.textBaseline='middle';
                cx.fillText(bd.emoji,sx+TS/2,sy+TS/2);
            }
            // Mine progress overlay
            if(mineProgress&&mineProgress.c===c&&mineProgress.r===r){
                var pct=mineProgress.prog/mineProgress.max;
                cx.fillStyle='rgba(0,0,0,'+(pct*0.7)+')';cx.fillRect(sx,sy,TS,TS);
                cx.strokeStyle='rgba(255,255,255,0.5)';cx.lineWidth=1;
                for(var ci=0;ci<Math.floor(pct*4);ci++){
                    cx.beginPath();cx.moveTo(sx+4+ci*6,sy+4);cx.lineTo(sx+7+ci*6,sy+TS-4);cx.stroke();
                }
            }
        }
    }

    // Enemies
    enemies.forEach(function(e){
        var sx=e.r-camera.x,sy=e.y-camera.y;
        cx.font='18px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(e.face,sx,sy);
        cx.fillStyle='#1e293b';cx.fillRect(sx-12,sy-18,24,4);
        cx.fillStyle='#ef4444';cx.fillRect(sx-12,sy-18,24*(e.hp/3),4);
    });

    // Particles
    particles.forEach(function(p){
        cx.beginPath();cx.arc(p.x,p.y,p.r,0,6.28);
        cx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,'0');cx.fill();
    });

    // Player
    var px=player.x-camera.x,py=player.y-camera.y;
    cx.save();if(player.facing<0){cx.scale(-1,1);px=-px;}
    cx.font='20px serif';cx.textAlign='center';cx.textBaseline='bottom';
    cx.fillText('🧑‍💻',px,py+26);cx.restore();

    // HP bar
    cx.fillStyle='rgba(7,21,32,0.8)';cx.fillRect(5,5,104,14);
    cx.fillStyle='#1e293b';cx.fillRect(5,5,104,14);
    cx.fillStyle=hp>50?'#10b981':hp>25?'#fbbf24':'#ef4444';
    cx.fillRect(5,5,hp*1.04,14);
    cx.font='9px sans-serif';cx.fillStyle='white';cx.textAlign='left';
    cx.fillText('HP: '+Math.round(hp),8,16);

    // Depth indicator
    cx.font='9px sans-serif';cx.fillStyle='#8b5cf6';cx.textAlign='right';
    cx.fillText('Depth '+depth+' | PQC: '+pqcTotal,W-5,15);
}

function loop(){frameId=requestAnimationFrame(loop);
    if(gameActive){
        if(keys['e']||keys['E'])doMine();else mineProgress=null;
        if(keys['f']||keys['F'])doPlace();
        updatePlayer();updateEnemies();
        particles.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.vy+=0.1;p.alpha-=0.03;p.r*=0.96;});
        particles=particles.filter(function(p){return p.alpha>0;});
    }
    draw();
}

function spawnParticles(x,y,color,n){
    for(var i=0;i<n;i++){
        var a=Math.random()*6.28,s=1+Math.random()*3;
        particles.push({x:x,y:y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,r:2+Math.random()*2,alpha:1,color:color||'#888'});
    }
}
function updateHUD(){
    document.getElementById('h-hp').textContent=Math.round(hp);
    document.getElementById('h-hp').style.color=hp>50?'#10b981':hp>25?'#fbbf24':'#ef4444';
    document.getElementById('h-score').textContent=score;
    document.getElementById('h-mined').textContent=mined;
    document.getElementById('h-depth').textContent=depth;
    document.getElementById('h-pqc').textContent=pqcTotal;
}
function updateInv(){
    document.getElementById('sl-kyber').textContent='🔐 ML-KEM:'+(inventory.kyber||0);
    document.getElementById('sl-dil').textContent='✍️ ML-DSA:'+(inventory.dil||0);
    document.getElementById('sl-sph').textContent='🌲 SPHINCS:'+(inventory.sph||0);
    document.getElementById('sl-fal').textContent='🦅 Falcon:'+(inventory.fal||0);
}
function setMsg(m){document.getElementById('msg').textContent=m;}
function confetti(){var c=['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444'];for(var i=0;i<15;i++){setTimeout(function(){var el=document.createElement('div');el.className='cp';el.style.left=Math.random()*100+'vw';el.style.background=c[Math.floor(Math.random()*c.length)];el.style.animationDuration=(1+Math.random()*2)+'s';document.body.appendChild(el);setTimeout(function(){el.remove();},3000);},i*40);}}

document.addEventListener('keydown',function(e){keys[e.key]=true;e.preventDefault();});
document.addEventListener('keyup',function(e){keys[e.key]=false;});

cx.fillStyle='#020d14';cx.fillRect(0,0,W,H);
cx.font='bold 16px sans-serif';cx.fillStyle='#8b5cf6';cx.textAlign='center';
cx.fillText('⛏️ QuantumCraft — Lattice Mines',W/2,H/2-10);
cx.font='11px sans-serif';cx.fillStyle='#94a3b8';cx.fillText('Press Start Mining to begin!',W/2,H/2+15);
</script>
</body>
</html>
""", height=560)

def render_quantumcraft_highschool():
    """9-12: QuantumCraft Cipher Ruins — UPGRADED 2026 — platformer with PQC bosses and lore."""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("🏃 QuantumCraft — Cipher Ruins!")
    st.markdown(
        "Run through **quantum-corrupted ruins**! "
        "Arrow keys/WASD to run and jump. Collect PQC power-ups, defeat cipher bosses! "
        "Each boss teaches a real PQC concept."
    )
    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow:hidden;}
#wrap{max-width:560px;margin:0 auto;padding:8px;}
.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-bottom:6px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:5px 3px;
    text-align:center;font-size:9px;color:#60a5fa;}
.hb b{display:block;font-size:14px;color:white;}
#cv{border:2px solid #7c3aed;border-radius:10px;display:block;}
#msg{background:#071520;border:1px solid #1a3a5a;border-radius:8px;
    padding:4px 10px;margin-top:5px;font-size:10px;color:#a78bfa;text-align:center;}
.btns{display:flex;gap:4px;margin-top:5px;}
.btn{flex:1;padding:7px;border-radius:8px;border:none;cursor:pointer;font-size:11px;font-weight:bold;color:white;}
.btn-start{background:linear-gradient(135deg,#7c3aed,#a78bfa);}
.btn-reset{background:#334155;}
.cp{position:fixed;pointer-events:none;z-index:999;width:8px;height:8px;border-radius:2px;animation:cf linear forwards;}
@keyframes cf{0%{transform:translateY(-20px) rotate(0deg);opacity:1;}100%{transform:translateY(500px) rotate(720deg);opacity:0;}}
</style>
</head>
<body>
<div id="wrap">
<div class="hud">
    <div class="hb">❤️ HP<br><b id="h-hp">5</b></div>
    <div class="hb">⭐ Score<br><b id="h-score">0</b></div>
    <div class="hb">🌊 Level<br><b id="h-level">1</b>/4</div>
    <div class="hb">🏆 Boss<br><b id="h-boss">—</b></div>
</div>
<canvas id="cv" width="560" height="360"></canvas>
<div id="msg">Arrow keys / WASD to move, Space/Up to jump. Collect PQC power-ups!</div>
<div class="btns">
    <button class="btn btn-start" onclick="startGame()">▶ Start!</button>
    <button class="btn btn-reset" onclick="resetGame()">🔄 Reset</button>
</div>
</div>
<script>
var cv=document.getElementById('cv'),cx=cv.getContext('2d');
var W=560,H=360;

// Level configs with boss info
var LEVELS=[
    {name:'RSA Ruins',     bgColor:'#0a0a1a', groundColor:'#1a0a2e', bossName:'RSA Guardian',
     bossEmoji:'💀',bossColor:'#ef4444',
     bossHP:8, bossSpeed:1.2,
     fact:'RSA is broken by Shor Algorithm — quantum computers factor its primes in seconds!',
     platforms:[{x:0,y:320,w:560,h:40},{x:100,y:250,w:100,h:15},{x:300,y:200,w:100,h:15},{x:450,y:260,w:80,h:15}],
     pickups:[{x:150,y:230,type:'kyber'},{x:350,y:180,type:'kyber'},{x:480,y:240,type:'kyber'}]},
    {name:'Lattice Caverns',bgColor:'#071520',groundColor:'#1a2a0a', bossName:'Lattice Wraith',
     bossEmoji:'🌀',bossColor:'#8b5cf6',
     bossHP:10,bossSpeed:1.4,
     fact:'Lattice math (LWE) is the foundation of ML-KEM and ML-DSA — impossible for quantum to solve!',
     platforms:[{x:0,y:320,w:560,h:40},{x:80,y:260,w:80,h:15},{x:220,y:210,w:100,h:15},{x:380,y:250,w:120,h:15}],
     pickups:[{x:120,y:240,type:'dil'},{x:270,y:190,type:'dil'},{x:430,y:230,type:'dil'}]},
    {name:'Hash Fortress',  bgColor:'#0a1520',groundColor:'#1a1a2e', bossName:'Hash Phantom',
     bossEmoji:'#️⃣',bossColor:'#06b6d4',
     bossHP:12,bossSpeed:1.6,
     fact:'SPHINCS+ chains thousands of SHA-3 hashes — Grover Algorithm only gives quadratic speedup!',
     platforms:[{x:0,y:320,w:560,h:40},{x:60,y:270,w:60,h:15},{x:200,y:220,w:80,h:15},{x:380,y:200,w:80,h:15},{x:480,y:260,w:60,h:15}],
     pickups:[{x:100,y:250,type:'sph'},{x:240,y:200,type:'sph'},{x:420,y:180,type:'sph'}]},
    {name:'Falcon Tower',   bgColor:'#1a0a0a',groundColor:'#2a1a0a', bossName:'FINAL: Quantum BOSS',
     bossEmoji:'👑',bossColor:'#fbbf24',
     bossHP:20,bossSpeed:2.0,
     fact:'FN-DSA Falcon uses NTRU lattices — the most compact quantum-safe signature scheme!',
     platforms:[{x:0,y:320,w:560,h:40},{x:80,y:260,w:70,h:15},{x:220,y:200,w:80,h:15},{x:360,y:240,w:70,h:15},{x:460,y:180,w:80,h:15}],
     pickups:[{x:120,y:240,type:'fal'},{x:260,y:180,type:'fal'},{x:490,y:160,type:'fal'}]},
];
var PICKUP_INFO={
    kyber:{emoji:'🔐',color:'#10b981',name:'ML-KEM',pts:30},
    dil:  {emoji:'✍️', color:'#3b82f6',name:'ML-DSA',pts:35},
    sph:  {emoji:'🌲',color:'#8b5cf6',name:'SPHINCS+',pts:40},
    fal:  {emoji:'🦅',color:'#f59e0b',name:'Falcon',pts:50},
};

// State
var player={x:60,y:280,vx:0,vy:0,w:20,h:28,onGround:false,hp:5,maxHp:5,invincible:0,facing:1};
var boss=null,bossActive=false,bossBullets=[];
var pickups=[],particles=[],floats=[];
var score=0,level=0,gameActive=false,keys={};
var bgStars=[];
for(var i=0;i<50;i++) bgStars.push({x:Math.random()*W,y:Math.random()*H*0.7,r:Math.random()*1.5,a:Math.random()*0.5+0.2});
var camera={x:0};
var frameId=null;
var WIN_X=500;

function startGame(){
    level=0;score=0;
    player={x:60,y:280,vx:0,vy:0,w:20,h:28,onGround:false,hp:5,maxHp:5,invincible:0,facing:1};
    loadLevel();
    gameActive=true;
    if(frameId)cancelAnimationFrame(frameId);
    loop();
}

function resetGame(){gameActive=false;if(frameId)cancelAnimationFrame(frameId);}

function loadLevel(){
    var lv=LEVELS[level];
    boss={x:W-80,y:lv.platforms[0].y-50,vx:-lv.bossSpeed,vy:0,
          w:36,h:40,hp:lv.bossHP,maxHp:lv.bossHP,
          emoji:lv.bossEmoji,color:lv.bossColor,
          shootTimer:0,shootRate:90,onGround:false,active:false};
    bossActive=false;bossBullets=[];particles=[];floats=[];
    pickups=lv.pickups.map(function(p){return Object.assign({},p,{alive:true});});
    document.getElementById('h-level').textContent=(level+1)+'/4';
    document.getElementById('h-boss').textContent=lv.bossName;
    setMsg('Level '+(level+1)+': '+lv.name+' — reach the boss!');
    updateHUD();
}

var GRAV=0.45,MAXFALL=12,SPDHZ=3,JUMP=-9;
function updatePlayer(){
    if(player.invincible>0) player.invincible--;
    var dx=0;
    if(keys['ArrowLeft']||keys['a'])dx=-SPDHZ;
    if(keys['ArrowRight']||keys['d'])dx=SPDHZ;
    if(dx!==0)player.facing=dx>0?1:-1;
    player.vx=dx;
    if((keys['ArrowUp']||keys['w']||keys[' '])&&player.onGround){player.vy=JUMP;player.onGround=false;}
    player.vy=Math.min(player.vy+GRAV,MAXFALL);
    player.x+=player.vx;player.y+=player.vy;player.onGround=false;
    // Platform collision
    LEVELS[level].platforms.forEach(function(p){
        if(player.x+player.w>p.x&&player.x<p.x+p.w&&
           player.y+player.h>p.y&&player.y+player.h<p.y+p.h+player.vy+1&&
           player.vy>0){
            player.y=p.y-player.h;player.vy=0;player.onGround=true;
        }
        if(player.x+player.w>p.x&&player.x<p.x+p.w&&
           player.y>p.y&&player.y<p.y+p.h&&player.vy<0){
            player.y=p.y+p.h;player.vy=0;
        }
    });
    player.x=Math.max(0,Math.min(W-player.w,player.x));
    if(player.y>H){player.hp--;player.y=50;player.vy=0;updateHUD();if(player.hp<=0)gameOver();}
    // Pickup
    pickups.forEach(function(pu){
        if(!pu.alive)return;
        if(Math.abs(player.x+10-pu.x)<20&&Math.abs(player.y+14-pu.y)<20){
            pu.alive=false;
            var info=PICKUP_INFO[pu.type];
            score+=info.pts;
            addFloat(pu.x,pu.y,'+'+info.pts+' '+info.name,info.color);
            spawnParts(pu.x,pu.y,info.color,10);
            setMsg(info.emoji+' '+info.name+' collected! '+info.pts+' pts!');
            // Activate boss when all pickups collected
            if(pickups.every(function(p){return !p.alive;})&&!bossActive){
                bossActive=true;
                setMsg('💀 BOSS ACTIVATED: '+LEVELS[level].bossName+'! Defeat it!');
            }
            updateHUD();
        }
    });
    // Boss collision
    if(bossActive&&boss&&player.invincible===0){
        if(Math.abs(player.x+10-boss.x-18)<30&&Math.abs(player.y+14-boss.y-20)<30){
            player.hp--;player.invincible=90;player.vy=-5;
            spawnParts(player.x+10,player.y+14,'#ef4444',8);
            updateHUD();if(player.hp<=0)gameOver();
        }
    }
    // Boss bullets
    bossBullets.forEach(function(b,i){
        b.x+=b.vx;b.y+=b.vy;
        if(Math.abs(player.x+10-b.x)<15&&Math.abs(player.y+14-b.y)<15&&player.invincible===0){
            player.hp--;player.invincible=90;
            bossBullets.splice(i,1);spawnParts(b.x,b.y,'#ef4444',6);
            updateHUD();if(player.hp<=0)gameOver();
        }
        if(b.x<0||b.x>W||b.y>H) bossBullets.splice(i,1);
    });
    // Win check
    if(player.x>WIN_X&&bossActive&&boss.hp<=0) nextLevel();
}

function updateBoss(){
    if(!bossActive||!boss) return;
    boss.vy=Math.min(boss.vy+GRAV,MAXFALL);
    boss.x+=boss.vx;boss.y+=boss.vy;boss.onGround=false;
    LEVELS[level].platforms.forEach(function(p){
        if(boss.x+boss.w>p.x&&boss.x<p.x+p.w&&boss.y+boss.h>p.y&&boss.y+boss.h<p.y+p.h+2&&boss.vy>0){
            boss.y=p.y-boss.h;boss.vy=0;boss.onGround=true;
        }
    });
    if(boss.x<20||boss.x>W-boss.w-20) boss.vx*=-1;
    // Jump occasionally
    if(boss.onGround&&Math.random()<0.015) boss.vy=JUMP*0.7;
    // Shoot
    boss.shootTimer++;
    if(boss.shootTimer>=boss.shootRate){
        boss.shootTimer=0;
        var dx=player.x-boss.x,dy=player.y-boss.y;
        var d=Math.sqrt(dx*dx+dy*dy)||1;
        bossBullets.push({x:boss.x+18,y:boss.y+20,vx:dx/d*4,vy:dy/d*4,color:boss.color});
    }
}

function nextLevel(){
    if(level>=LEVELS.length-1){victory();return;}
    level++;confetti();
    player.x=60;player.y=280;player.vy=0;player.hp=Math.min(player.hp+2,player.maxHp);
    setMsg('✅ Level '+(level)+' cleared! '+LEVELS[level-1].fact);
    showFact(LEVELS[level-1].fact);
    setTimeout(function(){loadLevel();},2000);
    updateHUD();
}

function victory(){
    gameActive=false;
    setMsg('👑 ALL BOSSES DEFEATED! You mastered all 4 NIST PQC standards! Score: '+score);
    confetti();
}
function gameOver(){
    gameActive=false;
    setMsg('💀 Game Over! Score:'+score+' | Level:'+(level+1)+' — Press Start to try again!');
}

function draw(){
    var lv=LEVELS[level];
    cx.clearRect(0,0,W,H);
    cx.fillStyle=lv.bgColor;cx.fillRect(0,0,W,H);
    // Stars
    bgStars.forEach(function(s){
        cx.beginPath();cx.arc(s.x,s.y,s.r,0,6.28);
        cx.fillStyle='rgba(255,255,255,'+s.a+')';cx.fill();
    });
    // Platforms
    lv.platforms.forEach(function(p){
        var g=cx.createLinearGradient(0,p.y,0,p.y+p.h);
        g.addColorStop(0,lv.groundColor);g.addColorStop(1,'#0a0a14');
        cx.fillStyle=g;cx.fillRect(p.x,p.y,p.w,p.h);
        // Edge glow
        cx.strokeStyle='#7c3aed30';cx.lineWidth=1;
        cx.beginPath();cx.moveTo(p.x,p.y);cx.lineTo(p.x+p.w,p.y);cx.stroke();
    });
    // Pickups
    pickups.forEach(function(pu){
        if(!pu.alive)return;
        var info=PICKUP_INFO[pu.type];
        cx.shadowColor=info.color;cx.shadowBlur=12;
        cx.font='18px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(info.emoji,pu.x,pu.y+Math.sin(Date.now()*0.003+pu.x)*4);
        cx.shadowBlur=0;
    });
    // Boss
    if(bossActive&&boss){
        cx.shadowColor=boss.color;cx.shadowBlur=20;
        cx.font='32px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(boss.emoji,boss.x+18,boss.y+20);cx.shadowBlur=0;
        // HP bar
        cx.fillStyle='#1e293b';cx.fillRect(boss.x,boss.y-14,boss.w,8);
        cx.fillStyle=boss.color;cx.fillRect(boss.x,boss.y-14,boss.w*(boss.hp/boss.maxHp),8);
        document.getElementById('h-boss').textContent=boss.hp+'HP';
    }
    // Boss bullets
    bossBullets.forEach(function(b){
        cx.beginPath();cx.arc(b.x,b.y,5,0,6.28);
        cx.fillStyle=b.color;cx.shadowColor=b.color;cx.shadowBlur=8;cx.fill();cx.shadowBlur=0;
    });
    // Particles
    particles.forEach(function(p){
        cx.beginPath();cx.arc(p.x,p.y,p.r,0,6.28);
        cx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,'0');cx.fill();
    });
    // Float texts
    floats.forEach(function(f){
        cx.font='bold 12px sans-serif';cx.textAlign='center';
        cx.fillStyle=f.color+Math.floor(f.alpha*255).toString(16).padStart(2,'0');
        cx.fillText(f.text,f.x,f.y);
    });
    // Player
    cx.save();
    if(player.facing<0){cx.scale(-1,1);}
    var px=player.facing>0?player.x+10:-(player.x+10);
    if(player.invincible>0&&Math.floor(Date.now()/100)%2===0)cx.globalAlpha=0.3;
    cx.font='22px serif';cx.textAlign='center';cx.textBaseline='bottom';
    cx.fillText('🏃',px,player.y+player.h);cx.globalAlpha=1;
    cx.restore();
    // HP bar
    cx.fillStyle='#1e293b';cx.fillRect(5,5,100,10);
    cx.fillStyle=player.hp>3?'#10b981':player.hp>1?'#fbbf24':'#ef4444';
    cx.fillRect(5,5,100*(player.hp/player.maxHp),10);
    // Win arrow
    if(bossActive&&boss&&boss.hp<=0){
        cx.font='bold 12px sans-serif';cx.fillStyle='#fbbf24';cx.textAlign='center';
        cx.fillText('→ Reach the exit! →',W-100,H/2);
    }
}

function loop(){
    frameId=requestAnimationFrame(loop);
    if(gameActive){
        updatePlayer();updateBoss();
        particles.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.vy+=0.1;p.alpha-=0.025;p.r*=0.96;});
        particles=particles.filter(function(p){return p.alpha>0;});
        floats.forEach(function(f){f.y-=0.8;f.alpha-=0.02;});
        floats=floats.filter(function(f){return f.alpha>0;});
    }
    draw();
}

// Boss hit detection (jump on boss head)
function checkBossJump(){
    if(!bossActive||!boss||boss.hp<=0) return;
    if(player.vy>0&&player.y+player.h>boss.y&&player.y<boss.y+10&&
       player.x+player.w>boss.x&&player.x<boss.x+boss.w){
        boss.hp--;player.vy=JUMP*0.7;
        spawnParts(boss.x+18,boss.y,'#fbbf24',12);
        score+=20;updateHUD();
        setMsg('⚡ Boss hit! HP: '+boss.hp+'/'+boss.maxHp);
        if(boss.hp<=0){
            bossActive=false;
            setMsg('🏆 '+LEVELS[level].bossName+' DEFEATED! '+LEVELS[level].fact);
            confetti();score+=200;updateHUD();
        }
    }
}

function spawnParts(x,y,col,n){for(var i=0;i<n;i++){var a=Math.random()*6.28,s=1+Math.random()*4;particles.push({x:x,y:y,vx:Math.cos(a)*s,vy:Math.sin(a)*s-1,r:2+Math.random()*3,alpha:1,color:col});}}
function addFloat(x,y,t,c){floats.push({x:x,y:y,text:t,color:c,alpha:1});}
function updateHUD(){document.getElementById('h-hp').textContent='❤️'.repeat(player.hp);document.getElementById('h-score').textContent=score;}
function setMsg(m){document.getElementById('msg').textContent=m;}
function showFact(t){setMsg('💡 '+t.substring(0,120)+'...');}
function confetti(){var c=['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444'];for(var i=0;i<15;i++){setTimeout(function(){var el=document.createElement('div');el.className='cp';el.style.left=Math.random()*100+'vw';el.style.background=c[Math.floor(Math.random()*c.length)];el.style.animationDuration=(1+Math.random()*2)+'s';document.body.appendChild(el);setTimeout(function(){el.remove();},3000);},i*40);}}

document.addEventListener('keydown',function(e){keys[e.key]=true;checkBossJump();if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' '].includes(e.key))e.preventDefault();});
document.addEventListener('keyup',function(e){keys[e.key]=false;});

cx.fillStyle='#020d14';cx.fillRect(0,0,W,H);
cx.font='bold 16px sans-serif';cx.fillStyle='#a78bfa';cx.textAlign='center';
cx.fillText('🏃 QuantumCraft — Cipher Ruins',W/2,H/2-10);
cx.font='11px sans-serif';cx.fillStyle='#94a3b8';cx.fillText('Press Start to run!',W/2,H/2+15);
</script>
</body>
</html>
""", height=560)

def render_prime_factor_game():
    """Free game: Prime Factor Cracker — UPGRADED 2026 with Shor Bot battle!"""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("🔢 Prime Factor Cracker — Beat the Shor Bot!")
    st.markdown(
        "**RSA encryption** is only as safe as the hardest math problem: factoring huge numbers. "
        "Race the **Shor Bot** quantum computer to find the prime factors first! "
        "Learn why RSA is doomed — and what KYBER does instead!"
    )
    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow-x:hidden;}
#wrap{display:flex;flex-direction:column;align-items:center;padding:10px;
    max-width:560px;margin:0 auto;}

/* HUD */
.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;width:100%;margin-bottom:8px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:5px 3px;
    text-align:center;font-size:9px;color:#60a5fa;}
.hb b{display:block;font-size:15px;color:white;}

/* WAVE BANNER */
#wave-banner{background:linear-gradient(135deg,#0a1f35,#071520);
    border:1px solid #1d4ed8;border-radius:10px;padding:8px 14px;
    width:100%;margin-bottom:8px;display:flex;
    justify-content:space-between;align-items:center;}
#wave-title{font-size:13px;color:#60a5fa;font-weight:bold;}
#wave-sub{font-size:10px;color:#475569;}

/* BATTLE ARENA */
#arena{width:100%;background:#071520;border:2px solid #1a3a5a;
    border-radius:12px;padding:12px;margin-bottom:8px;position:relative;}

/* VS ROW */
#vs-row{display:flex;align-items:center;justify-content:space-between;
    margin-bottom:10px;}
.fighter{text-align:center;flex:1;}
.fighter-emoji{font-size:2.5rem;display:block;margin-bottom:4px;
    transition:transform 0.3s;}
.fighter-name{font-size:10px;color:#94a3b8;margin-bottom:4px;}
.fighter-bar-wrap{height:8px;background:#1e293b;border-radius:4px;overflow:hidden;}
.fighter-bar{height:8px;border-radius:4px;transition:width 0.3s;}
#player-bar{background:linear-gradient(90deg,#10b981,#34d399);}
#shor-bar{background:linear-gradient(90deg,#ef4444,#f97316);}
#vs-text{font-size:20px;font-weight:bold;color:#fbbf24;flex-shrink:0;
    margin:0 10px;}

/* NUMBER DISPLAY */
#number-card{background:#051018;border:2px solid #3b82f6;border-radius:12px;
    padding:14px;text-align:center;margin-bottom:10px;}
#number-label{font-size:10px;color:#60a5fa;margin-bottom:4px;}
#big-number{font-size:28px;font-weight:bold;color:#fbbf24;
    font-family:'Fira Code',monospace;letter-spacing:2px;}
#number-bits{font-size:9px;color:#475569;margin-top:2px;}
#hint-row{display:flex;justify-content:center;gap:10px;margin-top:6px;}
.hint-pill{background:#0a1f35;border:1px solid #1a3a5a;border-radius:20px;
    padding:3px 10px;font-size:9px;color:#60a5fa;}

/* SHOR TIMER */
#shor-section{margin-bottom:10px;}
#shor-label{font-size:10px;color:#ef4444;margin-bottom:4px;
    display:flex;justify-content:space-between;}
#shor-timer-bar{height:10px;background:#1e293b;border-radius:5px;overflow:hidden;}
#shor-fill{height:10px;background:linear-gradient(90deg,#ef4444,#f97316);
    border-radius:5px;width:0%;transition:width 0.1s linear;}
#shor-bot-status{font-size:11px;color:#ef4444;text-align:center;
    margin-top:4px;min-height:16px;}

/* INPUT SECTION */
#input-section{display:flex;gap:6px;margin-bottom:8px;}
#factor-input{flex:1;background:#0a1f35;border:2px solid #3b82f6;
    border-radius:8px;color:white;font-size:16px;padding:8px 12px;
    outline:none;font-family:'Fira Code',monospace;text-align:center;}
#factor-input:focus{border-color:#60a5fa;}
#check-btn{padding:8px 16px;background:#1d4ed8;border:none;border-radius:8px;
    color:white;font-size:13px;font-weight:bold;cursor:pointer;
    transition:all 0.15s;white-space:nowrap;}
#check-btn:hover{background:#2563eb;transform:translateY(-1px);}

/* FACTOR DISPLAY */
#factors-found{display:flex;gap:6px;justify-content:center;
    flex-wrap:wrap;margin-bottom:6px;}
.factor-badge{background:#071520;border:2px solid #10b981;border-radius:8px;
    padding:6px 14px;font-size:14px;color:#10b981;font-family:'Fira Code',monospace;
    font-weight:bold;}

/* RESULT */
#result-area{text-align:center;min-height:40px;margin-bottom:6px;}
#result-msg{font-size:13px;font-weight:bold;min-height:20px;}

/* BUTTONS */
.btn{padding:8px 16px;border-radius:8px;border:none;cursor:pointer;
    font-size:12px;font-weight:bold;color:white;transition:all 0.15s;margin:3px;}
.btn:hover{filter:brightness(1.2);transform:translateY(-1px);}
.btn-blue{background:#1d4ed8;}
.btn-green{background:#059669;}
.btn-red{background:#dc2626;}
.btn-gold{background:linear-gradient(135deg,#b45309,#d97706);}
.btn-row{display:flex;gap:5px;flex-wrap:wrap;justify-content:center;}

/* WAVE COMPLETE */
#wave-complete{display:none;background:linear-gradient(135deg,#071520,#0a1f35);
    border:2px solid #fbbf24;border-radius:12px;padding:16px;
    text-align:center;width:100%;margin-bottom:8px;animation:slideIn 0.3s ease;}

/* FACT BOX */
#fact-box{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);
    border-radius:8px;padding:8px 12px;margin-bottom:8px;font-size:10px;
    color:#93c5fd;display:none;line-height:1.5;width:100%;}

/* LEADERBOARD */
#lb-section{background:#071520;border:1px solid #1a3a5a;border-radius:10px;
    padding:10px;width:100%;margin-bottom:8px;}
#lb-section h4{color:#60a5fa;font-size:11px;margin-bottom:6px;}
.lb-row{display:flex;justify-content:space-between;font-size:10px;
    color:#94a3b8;padding:3px 0;border-bottom:1px solid #0f2030;}
.lb-row:last-child{border:none;}
.lb-rank{color:#fbbf24;font-weight:bold;width:20px;}
.lb-name{flex:1;color:white;}
.lb-score{color:#10b981;font-weight:bold;}

/* ANIMATIONS */
@keyframes slideIn{from{opacity:0;transform:translateY(-10px);}to{opacity:1;transform:translateY(0);}}
@keyframes shake{0%,100%{transform:translateX(0);}25%{transform:translateX(-6px);}75%{transform:translateX(6px);}}
@keyframes pop{0%{transform:scale(1);}50%{transform:scale(1.2);}100%{transform:scale(1);}}
@keyframes victory{0%{transform:scale(1) rotate(0deg);}25%{transform:scale(1.3) rotate(-10deg);}50%{transform:scale(1.3) rotate(10deg);}100%{transform:scale(1) rotate(0deg);}}
@keyframes defeated{0%{transform:scale(1);}100%{transform:scale(0.7) rotate(180deg);opacity:0.3;}}
@keyframes confettiFall{0%{transform:translateY(-20px) rotate(0deg);opacity:1;}100%{transform:translateY(600px) rotate(720deg);opacity:0;}}
.shake{animation:shake 0.4s ease;}
.pop{animation:pop 0.4s ease;}
.victory{animation:victory 0.6s ease;}
.defeated{animation:defeated 0.8s ease forwards;}
.confetti-piece{position:fixed;pointer-events:none;z-index:999;
    width:8px;height:8px;border-radius:2px;animation:confettiFall linear forwards;}

/* TOAST */
#toast{position:fixed;top:16px;left:50%;transform:translateX(-50%);
    background:#071520;border:2px solid #10b981;border-radius:10px;
    padding:8px 16px;font-size:12px;color:#10b981;font-weight:bold;
    z-index:100;opacity:0;transition:opacity 0.3s;pointer-events:none;text-align:center;}
#toast.show{opacity:1;}
</style>
</head>
<body>
<div id="wrap">

<!-- HUD -->
<div class="hud">
    <div class="hb">⭐ Score<br><b id="h-score">0</b></div>
    <div class="hb">🌊 Wave<br><b id="h-wave">1</b>/10</div>
    <div class="hb">🔥 Streak<br><b id="h-streak">0</b></div>
    <div class="hb">⚡ Wins<br><b id="h-wins">0</b></div>
</div>

<!-- WAVE BANNER -->
<div id="wave-banner">
    <div>
        <div id="wave-title">🌊 Wave 1 — Warm Up</div>
        <div id="wave-sub">Small numbers — easy factors!</div>
    </div>
    <button class="btn btn-blue" onclick="startWave()" id="start-btn">▶ Start!</button>
</div>

<!-- ARENA -->
<div id="arena">

    <!-- VS ROW -->
    <div id="vs-row">
        <div class="fighter">
            <span class="fighter-emoji" id="player-emoji">🧑‍💻</span>
            <div class="fighter-name">YOU</div>
            <div class="fighter-bar-wrap" style="width:120px;margin:0 auto;">
                <div class="fighter-bar" id="player-bar" style="width:100%"></div>
            </div>
        </div>
        <div id="vs-text">⚔️</div>
        <div class="fighter">
            <span class="fighter-emoji" id="shor-emoji">🤖</span>
            <div class="fighter-name">SHOR BOT</div>
            <div class="fighter-bar-wrap" style="width:120px;margin:0 auto;">
                <div class="fighter-bar" id="shor-bar" style="width:100%"></div>
            </div>
        </div>
    </div>

    <!-- NUMBER -->
    <div id="number-card">
        <div id="number-label">🔐 Factor this RSA number:</div>
        <div id="big-number">???</div>
        <div id="number-bits">Press Start to begin!</div>
        <div id="hint-row">
            <div class="hint-pill" id="hint-1">💡 Hint 1</div>
            <div class="hint-pill" id="hint-2">💡 Hint 2</div>
        </div>
    </div>

    <!-- SHOR TIMER -->
    <div id="shor-section">
        <div id="shor-label">
            <span>☠️ Shor Bot cracking progress:</span>
            <span id="shor-pct">0%</span>
        </div>
        <div id="shor-timer-bar"><div id="shor-fill"></div></div>
        <div id="shor-bot-status">Press Start to wake up the Shor Bot!</div>
    </div>

    <!-- FACTORS FOUND -->
    <div id="factors-found"></div>

    <!-- INPUT -->
    <div id="input-section">
        <input id="factor-input" type="number" placeholder="Enter a factor..."
               onkeydown="if(event.key==='Enter') checkFactor()"/>
        <button id="check-btn" onclick="checkFactor()">⚡ Check!</button>
    </div>

    <!-- RESULT -->
    <div id="result-area">
        <div id="result-msg"></div>
    </div>

    <!-- BUTTONS -->
    <div class="btn-row">
        <button class="btn btn-gold" onclick="useHint()">💡 Hint (-10 pts)</button>
        <button class="btn" style="background:#334155" onclick="skipNumber()">⏭️ Skip</button>
    </div>

</div>

<!-- WAVE COMPLETE -->
<div id="wave-complete">
    <div style="font-size:2.5rem" id="wc-emoji">🎉</div>
    <h3 style="color:#fbbf24;margin:6px 0" id="wc-title">Wave Complete!</h3>
    <p style="color:#94a3b8;font-size:11px" id="wc-msg"></p>
    <button class="btn btn-gold" style="margin-top:8px" onclick="nextWave()">➡️ Next Wave!</button>
</div>

<!-- FACT BOX -->
<div id="fact-box"></div>

<!-- LOCAL LEADERBOARD -->
<div id="lb-section">
    <h4>🏆 Best Scores This Session</h4>
    <div id="lb-rows">
        <div class="lb-row"><span class="lb-rank">—</span><span class="lb-name">No scores yet</span><span class="lb-score">0</span></div>
    </div>
</div>

</div><!-- end wrap -->
<div id="toast"></div>

<script>
// ── WAVE DEFINITIONS ──────────────────────────────────────────────────────────
// Each wave has: title, subtitle, numbers to factor, time limit
const WAVES = [
    {title:'Wave 1 — Warm Up',      sub:'Small numbers — easy factors!',        nums:[[6,2,3],[10,2,5],[15,3,5],[21,3,7],[14,2,7]],       time:20},
    {title:'Wave 2 — Getting Real', sub:'Slightly bigger — stay focused!',       nums:[[35,5,7],[77,7,11],[91,7,13],[143,11,13],[187,11,17]], time:22},
    {title:'Wave 3 — RSA Basics',   sub:'Two-digit primes — Shor Bot speeds up!',nums:[[221,13,17],[323,17,19],[437,19,23],[667,23,29],[899,29,31]],time:25},
    {title:'Wave 4 — Triple Digits',sub:'Three digits — think carefully!',        nums:[[1147,31,37],[1517,37,41],[1763,41,43],[2021,43,47],[2491,47,53]],time:28},
    {title:'Wave 5 — RSA-64',       sub:'Real RSA territory — Shor Bot angry!',  nums:[[3127,53,59],[3599,59,61],[4rr,61,67],[5183,67,71],[5767,71,73]],time:30},
    {title:'Wave 6 — Speed Round',  sub:'Fast fingers! 15 seconds each!',        nums:[[6557,73,79],[7663,79,97],[9409,97,97],[10403,101,103],[11021,101,109]],time:15},
    {title:'Wave 7 — Boss Level',   sub:'The Shor Bot is ANGRY — hurry!',        nums:[[12319,107,109],[13013,101,113],[15251,107,109],[17081,113,151],[18721,131,143]],time:20},
    {title:'Wave 8 — Elite',        sub:'Only the best cryptographers survive!', nums:[[21277,127,167],[25123,139,181],[28441,151,179],[33511,163,193],[39403,181,211]],time:25},
    {title:'Wave 9 — Legendary',    sub:'Modern RSA uses 2048-bit numbers!',     nums:[[46189,199,233],[54869,211,257],[65183,229,271],[76843,251,307],[91567,271,337]],time:30},
    {title:'Wave 10 — FINAL BOSS',  sub:'QUANTUM THREAT LEVEL: MAXIMUM!',       nums:[[104537,317,311],[121399,347,311],[144169,389,371],[169om,409,421],[196om,439,449]],time:35},
];

// Fix wave 5 and 10 typos
WAVES[4].nums[2] = [4rr,61,67];
// Actually let me use cleaner numbers
const CLEAN_WAVES = [
    {title:'Wave 1 — Warm Up',       sub:'Small numbers — easy factors!',         time:20, nums:[[6,2,3],[10,2,5],[15,3,5],[21,3,7],[14,2,7]]},
    {title:'Wave 2 — Getting Real',  sub:'Slightly bigger — stay focused!',        time:22, nums:[[35,5,7],[77,7,11],[91,7,13],[143,11,13],[187,11,17]]},
    {title:'Wave 3 — RSA Basics',    sub:'Two-digit primes — Shor Bot speeds up!', time:25, nums:[[221,13,17],[323,17,19],[437,19,23],[667,23,29],[899,29,31]]},
    {title:'Wave 4 — Triple Digits', sub:'Three digits — think carefully!',         time:28, nums:[[1147,31,37],[1517,37,41],[1763,41,43],[2021,43,47],[2491,47,53]]},
    {title:'Wave 5 — RSA Territory', sub:'Real RSA territory — Shor Bot angry!',   time:30, nums:[[3127,53,59],[3599,59,61],[4087,61,67],[5183,67,71],[5767,71,73]]},
    {title:'Wave 6 — Speed Round',   sub:'Fast fingers! 15 seconds each!',          time:15, nums:[[6557,73,89],[7921,89,89],[9409,97,97],[10403,101,103],[11021,101,109]]},
    {title:'Wave 7 — Boss Level',    sub:'The Shor Bot is ANGRY — hurry!',          time:20, nums:[[12319,107,109],[13013,101,131],[15251,107,139],[17081,113,151],[18721,131,149]]},
    {title:'Wave 8 — Elite',         sub:'Only the best cryptographers survive!',   time:25, nums:[[21277,127,167],[25123,139,181],[28441,157,179],[33511,163,193],[39403,181,211]]},
    {title:'Wave 9 — Legendary',     sub:'Modern RSA uses 2048-bit numbers!',       time:30, nums:[[46189,199,233],[54869,211,257],[65183,229,281],[76843,251,307],[91567,271,337]]},
    {title:'Wave 10 — FINAL BOSS',   sub:'QUANTUM THREAT LEVEL: MAXIMUM!',         time:35, nums:[[104537,317,331],[121399,347,349],[144169,379,383],[169013,409,421],[196013,441,449]]},
];

// ── PQC FACTS ────────────────────────────────────────────────────────────────
const FACTS = [
    '🔐 RSA uses the product of two huge primes as its public key. Factoring it would break RSA!',
    '☠️ Shor\'s Algorithm runs on a quantum computer and factors huge numbers in SECONDS!',
    '⏱️ A classical computer would take longer than the age of the universe to factor RSA-2048!',
    '🔐 Kyber (ML-KEM FIPS 203) does NOT use prime factoring — it uses lattice math instead!',
    '🌊 Wave '+'— each wave doubles the size of the numbers, just like RSA doubles its key size!',
    '💎 RSA-2048 has a 617-digit number as its key. Shor\'s Algorithm would crack it instantly!',
    '🏆 The record for factoring RSA numbers by hand: RSA-250 (829 bits) took 2700 CPU years!',
    '🤖 Shor\'s Algorithm was invented in 1994 by Peter Shor — it changed cryptography forever!',
    '🔬 Google\'s Willow quantum chip showed quantum advantage in 2024 — PQC is urgent now!',
    '🛡️ NIST finalized 4 PQC standards in 2024 to replace RSA before quantum computers arrive!',
];

// ── SHOR BOT TAUNTS ──────────────────────────────────────────────────────────
const TAUNTS = [
    '🤖 Shor Bot: "My qubits are warming up..."',
    '🤖 Shor Bot: "Superposition engaged! Finding all factors at once!"',
    '🤖 Shor Bot: "Period finding in progress... RSA has no defense!"',
    '🤖 Shor Bot: "Quantum Fourier Transform activated!"',
    '🤖 Shor Bot: "I see the factors! Almost there!"',
    '🤖 Shor Bot: "THIS is why you need Kyber, not RSA!"',
    '🤖 Shor Bot: "Too slow! Quantum computers never sleep!"',
    '🤖 Shor Bot: "Your 2048-bit RSA key is NOTHING to me!"',
];

// ── GAME STATE ────────────────────────────────────────────────────────────────
let score=0, wave=0, streak=0, wins=0, bestScore=0;
let currentWave=null, currentNumIdx=0;
let currentNum=0, factor1=0, factor2=0;
let foundFactors=[], hintsShown=0;
let shorTimer=null, shorPct=0;
let timeLimit=20;
let gameRunning=false;
let sessionScores=[];

// ── INIT WAVE ─────────────────────────────────────────────────────────────────
function startWave(){
    if(wave>=CLEAN_WAVES.length){ showVictory(); return; }
    currentWave=CLEAN_WAVES[wave];
    currentNumIdx=0;
    document.getElementById('start-btn').style.display='none';
    document.getElementById('wave-complete').style.display='none';
    document.getElementById('wave-title').textContent=currentWave.title;
    document.getElementById('wave-sub').textContent=currentWave.sub;
    document.getElementById('h-wave').textContent=(wave+1);
    loadNumber();
}

function loadNumber(){
    if(currentNumIdx>=currentWave.nums.length){
        waveComplete();
        return;
    }
    const [n,p,q]=currentWave.nums[currentNumIdx];
    currentNum=n; factor1=p; factor2=q;
    foundFactors=[];
    hintsShown=0;
    gameRunning=true;
    timeLimit=currentWave.time;

    document.getElementById('big-number').textContent=n.toLocaleString();
    document.getElementById('number-bits').textContent=
        'This '+n.toString().length+'-digit number = '+p+' × '+q+' (you find them!)';
    document.getElementById('factors-found').innerHTML='';
    document.getElementById('result-msg').textContent='';
    document.getElementById('factor-input').value='';
    document.getElementById('factor-input').focus();
    document.getElementById('hint-1').textContent='💡 Hint 1';
    document.getElementById('hint-2').textContent='💡 Hint 2';

    // Start Shor Bot timer
    startShorTimer();
    showFact(FACTS[Math.floor(Math.random()*FACTS.length)]);
}

// ── SHOR BOT TIMER ────────────────────────────────────────────────────────────
let shorInterval=null;
function startShorTimer(){
    shorPct=0;
    clearInterval(shorInterval);
    document.getElementById('shor-fill').style.width='0%';
    document.getElementById('shor-pct').textContent='0%';

    const tauntIdx=Math.floor(Math.random()*TAUNTS.length);
    document.getElementById('shor-bot-status').textContent=TAUNTS[tauntIdx];

    const steps=timeLimit*10; // update every 100ms
    let step=0;
    shorInterval=setInterval(()=>{
        if(!gameRunning){clearInterval(shorInterval);return;}
        step++;
        shorPct=Math.min(100,Math.round((step/steps)*100));
        document.getElementById('shor-fill').style.width=shorPct+'%';
        document.getElementById('shor-pct').textContent=shorPct+'%';

        // Taunt at milestones
        if(shorPct===25) setShorStatus('🤖 "Quantum state initialized... 25% done!"');
        if(shorPct===50) setShorStatus('🤖 "Halfway! Grover search engaged!"');
        if(shorPct===75) setShorStatus('🤖 "Almost cracked! 75% complete!"');
        if(shorPct===90) setShorStatus('🤖 "FINAL CALCULATION — tick tock!"');

        // Shor Bot wins
        if(shorPct>=100){
            clearInterval(shorInterval);
            gameRunning=false;
            shorWins();
        }
    },100);
}

function setShorStatus(msg){
    document.getElementById('shor-bot-status').textContent=msg;
}

// ── CHECK FACTOR ──────────────────────────────────────────────────────────────
function checkFactor(){
    if(!gameRunning) return;
    const val=parseInt(document.getElementById('factor-input').value);
    if(!val||val<2){ shake('factor-input'); return; }

    if(val===factor1||val===factor2){
        // Correct factor!
        if(!foundFactors.includes(val)){
            foundFactors.push(val);
            addFactorBadge(val);
            document.getElementById('factor-input').value='';

            if(foundFactors.length===2||(factor1===factor2&&foundFactors.length===1)){
                // Both factors found!
                playerWins();
            } else {
                setResult('✅ '+val+' is correct! Find the other factor!','#10b981');
                document.getElementById('player-emoji').classList.add('pop');
                setTimeout(()=>document.getElementById('player-emoji').classList.remove('pop'),400);
            }
        }
    } else if(currentNum%val===0){
        // Is a factor but not prime — guide them
        setResult('📎 '+val+' divides '+currentNum+' but keep going — find the PRIME factors!','#fbbf24');
        shake('factor-input');
    } else {
        // Wrong
        streak=0; updateHUD();
        setResult('❌ '+val+' is not a factor of '+currentNum,'#ef4444');
        shake('factor-input');
    }
    document.getElementById('factor-input').value='';
    document.getElementById('factor-input').focus();
}

function addFactorBadge(f){
    const d=document.createElement('div');
    d.className='factor-badge pop';
    d.textContent=f;
    document.getElementById('factors-found').appendChild(d);
}

// ── PLAYER WINS ───────────────────────────────────────────────────────────────
function playerWins(){
    clearInterval(shorInterval);
    gameRunning=false;
    streak++; wins++;
    const timeBonus=Math.round((1-shorPct/100)*50);
    const streakBonus=streak>=3?20:0;
    const pts=100+timeBonus+streakBonus;
    score+=pts; updateHUD();

    setResult('🎉 YOU WIN! +'+pts+' pts'+(streakBonus?' (Streak Bonus!)':''),'#10b981');
    document.getElementById('player-emoji').classList.add('victory');
    document.getElementById('shor-emoji').classList.add('defeated');
    setShorStatus('🤖 "Impossible! No quantum computer is fast enough!"');
    showToast('⚡ Beat the Shor Bot! +'+pts+' pts!');

    if(streak>=3) showToast('🔥 '+streak+' in a row! You\'re on fire!');

    setTimeout(()=>{
        document.getElementById('player-emoji').classList.remove('victory');
        document.getElementById('shor-emoji').classList.remove('defeated');
        currentNumIdx++;
        loadNumber();
    },1800);
}

// ── SHOR BOT WINS ────────────────────────────────────────────────────────────
function shorWins(){
    streak=0; updateHUD();
    setResult('💀 Shor Bot cracked it first! The factors were '+factor1+' × '+factor2,'#ef4444');
    document.getElementById('shor-emoji').classList.add('victory');
    document.getElementById('player-emoji').style.opacity='0.5';
    setShorStatus('🤖 "RSA is DEAD! This is why we need Kyber!"');
    showFact('🔐 The Shor Bot won because RSA relies on factoring — Kyber (FIPS 203) uses lattice math instead, which NO quantum computer can break!');

    setTimeout(()=>{
        document.getElementById('shor-emoji').classList.remove('victory');
        document.getElementById('player-emoji').style.opacity='1';
        currentNumIdx++;
        loadNumber();
    },2500);
}

// ── WAVE COMPLETE ─────────────────────────────────────────────────────────────
function waveComplete(){
    clearInterval(shorInterval);
    gameRunning=false;
    wave++;
    const waveBonus=wave*50;
    score+=waveBonus;
    updateHUD();
    saveScore();

    document.getElementById('wave-complete').style.display='block';
    document.getElementById('wc-emoji').textContent=wave>=10?'👑':'🎉';
    document.getElementById('wc-title').textContent=
        wave>=10?'YOU DEFEATED ALL WAVES!':'Wave '+(wave)+' Complete!';
    document.getElementById('wc-msg').textContent=
        '+'+waveBonus+' wave bonus! Total score: '+score;

    if(wave<CLEAN_WAVES.length){
        confetti();
    } else {
        showVictory();
    }
}

function nextWave(){
    document.getElementById('wave-complete').style.display='none';
    startWave();
}

function showVictory(){
    document.getElementById('arena').innerHTML=
        '<div style="text-align:center;padding:20px;">'+
        '<div style="font-size:3rem">👑</div>'+
        '<h2 style="color:#fbbf24;margin:8px 0">QUANTUM CHAMPION!</h2>'+
        '<p style="color:#94a3b8;font-size:11px">You defeated all 10 waves and beat Shor\'s Algorithm!</p>'+
        '<p style="color:#10b981;font-size:13px;margin:8px 0">Final Score: '+score+'</p>'+
        '<p style="color:#60a5fa;font-size:10px">Now you know why RSA needs to be replaced with Kyber (FIPS 203)!</p>'+
        '<button class="btn btn-gold" style="margin-top:10px" onclick="resetGame()">🔄 Play Again</button>'+
        '</div>';
    confetti();
    showToast('👑 QUANTUM CHAMPION! Final Score: '+score);
}

// ── HINTS ─────────────────────────────────────────────────────────────────────
function useHint(){
    score=Math.max(0,score-10);
    hintsShown++;
    if(hintsShown===1){
        const hint='Hint: Is '+factor1+' a factor? Try dividing '+currentNum+' by small primes!';
        document.getElementById('hint-1').textContent='💡 '+Math.min(factor1,factor2);
        showToast('💡 Hint: Try '+Math.min(factor1,factor2)+'! -10 pts');
    } else {
        document.getElementById('hint-2').textContent='💡 '+Math.max(factor1,factor2);
        showToast('💡 Other factor: '+Math.max(factor1,factor2)+'! -10 pts');
    }
    updateHUD();
}

function skipNumber(){
    clearInterval(shorInterval);
    gameRunning=false;
    streak=0;
    setResult('⏭️ Skipped! Factors were '+factor1+' × '+factor2,'#475569');
    showFact('💡 Remember: '+currentNum+' = '+factor1+' × '+factor2+'. Try to spot the pattern!');
    setTimeout(()=>{ currentNumIdx++; loadNumber(); },1500);
    updateHUD();
}

// ── UI HELPERS ────────────────────────────────────────────────────────────────
function setResult(msg,color){
    const el=document.getElementById('result-msg');
    el.textContent=msg; el.style.color=color||'white';
    el.classList.add('pop');
    setTimeout(()=>el.classList.remove('pop'),400);
}

function shake(id){
    const el=document.getElementById(id);
    el.classList.add('shake');
    setTimeout(()=>el.classList.remove('shake'),400);
}

function updateHUD(){
    document.getElementById('h-score').textContent=score;
    document.getElementById('h-wave').textContent=Math.min(wave+1,10);
    document.getElementById('h-streak').textContent=streak;
    document.getElementById('h-wins').textContent=wins;
}

let factTimer=null;
function showFact(text){
    const el=document.getElementById('fact-box');
    el.textContent=text; el.style.display='block';
    if(factTimer) clearTimeout(factTimer);
    factTimer=setTimeout(()=>el.style.display='none',5000);
}

let toastTimer=null;
function showToast(msg){
    const el=document.getElementById('toast');
    el.textContent=msg; el.classList.add('show');
    if(toastTimer) clearTimeout(toastTimer);
    toastTimer=setTimeout(()=>el.classList.remove('show'),2500);
}

// ── LEADERBOARD ───────────────────────────────────────────────────────────────
function saveScore(){
    sessionScores.push({score,wave,time:new Date().toLocaleTimeString()});
    sessionScores.sort((a,b)=>b.score-a.score);
    const rows=document.getElementById('lb-rows');
    rows.innerHTML='';
    sessionScores.slice(0,5).forEach((s,i)=>{
        const medals=['🥇','🥈','🥉','4️⃣','5️⃣'];
        const d=document.createElement('div');
        d.className='lb-row';
        d.innerHTML='<span class="lb-rank">'+medals[i]+'</span>'+
            '<span class="lb-name">Wave '+s.wave+' | '+s.time+'</span>'+
            '<span class="lb-score">'+s.score+'</span>';
        rows.appendChild(d);
    });
}

// ── CONFETTI ──────────────────────────────────────────────────────────────────
function confetti(){
    const colors=['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444','#f97316'];
    for(let i=0;i<25;i++){
        setTimeout(()=>{
            const el=document.createElement('div');
            el.className='confetti-piece';
            el.style.left=Math.random()*100+'vw';
            el.style.background=colors[Math.floor(Math.random()*colors.length)];
            el.style.animationDuration=(1+Math.random()*2)+'s';
            el.style.animationDelay=Math.random()*0.3+'s';
            document.body.appendChild(el);
            setTimeout(()=>el.remove(),3000);
        },i*40);
    }
}

function resetGame(){
    score=0; wave=0; streak=0; wins=0;
    currentWave=null; currentNumIdx=0;
    clearInterval(shorInterval);
    document.getElementById('start-btn').style.display='block';
    document.getElementById('wave-complete').style.display='none';
    document.getElementById('big-number').textContent='???';
    document.getElementById('number-bits').textContent='Press Start to begin!';
    document.getElementById('shor-bot-status').textContent='Press Start to wake up the Shor Bot!';
    document.getElementById('shor-fill').style.width='0%';
    document.getElementById('shor-pct').textContent='0%';
    document.getElementById('factors-found').innerHTML='';
    document.getElementById('result-msg').textContent='';
    updateHUD();
}

// ── KEYBOARD ──────────────────────────────────────────────────────────────────
document.addEventListener('keydown',e=>{
    if(e.key==='Enter') checkFactor();
});

// ── INIT ─────────────────────────────────────────────────────────────────────
updateHUD();
showFact(FACTS[0]);
</script>
</body>
</html>
""", height=720)

def render_network_defender():
    """Free game: Quantum Fortress — UPGRADED 2026 — Melon-style network defense."""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("🏰 Quantum Fortress — Network Defense!")
    st.markdown(
        "**Protect your network from Shor Bots!** "
        "Click nodes to deploy quantum shields. "
        "Don't let the attackers reach the HUB!"
    )
    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow:hidden;}
#wrap{display:flex;flex-direction:column;align-items:center;padding:8px;max-width:580px;margin:0 auto;}

/* HUD */
.hud{display:grid;grid-template-columns:repeat(5,1fr);gap:3px;width:100%;margin-bottom:6px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:6px;padding:4px 2px;
    text-align:center;font-size:8px;color:#60a5fa;}
.hb b{display:block;font-size:13px;color:white;}

/* WAVE BANNER */
#wave-banner{width:100%;background:#071520;border:1px solid #1d4ed8;
    border-radius:8px;padding:6px 12px;margin-bottom:6px;
    display:flex;justify-content:space-between;align-items:center;font-size:11px;}
#wave-text{color:#60a5fa;font-weight:bold;}
#integrity-bar-wrap{flex:1;height:8px;background:#1e293b;border-radius:4px;margin:0 10px;}
#integrity-bar{height:8px;border-radius:4px;background:linear-gradient(90deg,#10b981,#34d399);
    transition:width 0.3s;}
#integrity-pct{color:#10b981;font-size:10px;font-weight:bold;white-space:nowrap;}

/* CANVAS */
#gc{border:2px solid #1d4ed8;border-radius:10px;display:block;cursor:pointer;
    box-shadow:0 0 20px rgba(29,78,216,0.2);}

/* SHIELD SELECTOR */
#shield-bar{display:flex;gap:4px;justify-content:center;margin:6px 0;flex-wrap:wrap;}
.shield-opt{padding:5px 10px;border-radius:8px;border:2px solid #1a3a5a;
    background:#071520;color:#94a3b8;font-size:10px;cursor:pointer;
    transition:all 0.15s;text-align:center;}
.shield-opt:hover{border-color:#3b82f6;color:white;}
.shield-opt.active{border-color:#fbbf24;background:#1a1500;color:#fbbf24;}
.shield-opt .sh-emoji{font-size:16px;display:block;margin-bottom:2px;}
.shield-opt .sh-count{font-size:9px;color:#475569;}

/* BUTTONS */
.btns{display:flex;gap:4px;justify-content:center;flex-wrap:wrap;margin:4px 0;}
.btn{padding:7px 14px;border-radius:8px;border:none;cursor:pointer;
    font-size:11px;font-weight:bold;color:white;transition:all 0.15s;}
.btn:hover{filter:brightness(1.2);transform:translateY(-1px);}
.btn:disabled{opacity:0.4;cursor:not-allowed;transform:none;}
.btn-start{background:linear-gradient(135deg,#059669,#10b981);}
.btn-blue{background:#1d4ed8;}
.btn-red{background:#dc2626;}

/* FACT / MSG */
#msg{font-size:10px;color:#34d399;text-align:center;min-height:16px;margin:3px 0;}
#fact{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);
    border-radius:8px;padding:6px 10px;font-size:10px;color:#93c5fd;
    width:100%;margin-top:4px;display:none;line-height:1.5;}

/* TOAST */
#toast{position:fixed;top:14px;left:50%;transform:translateX(-50%);
    background:#071520;border:2px solid #10b981;border-radius:10px;
    padding:7px 14px;font-size:11px;color:#10b981;font-weight:bold;
    z-index:100;opacity:0;transition:opacity 0.3s;pointer-events:none;text-align:center;}
#toast.show{opacity:1;}

/* CONFETTI */
.cp{position:fixed;pointer-events:none;z-index:999;width:8px;height:8px;
    border-radius:2px;animation:cf linear forwards;}
@keyframes cf{0%{transform:translateY(-20px) rotate(0deg);opacity:1;}
    100%{transform:translateY(600px) rotate(720deg);opacity:0;}}

/* GAME OVER / WIN SCREEN */
#overlay{position:absolute;top:0;left:0;width:100%;height:100%;
    background:rgba(0,0,0,0.8);border-radius:10px;display:none;
    flex-direction:column;align-items:center;justify-content:center;z-index:10;}
#overlay.show{display:flex;}
#overlay h2{font-size:22px;margin-bottom:8px;}
#overlay p{font-size:12px;color:#94a3b8;margin-bottom:12px;text-align:center;}
</style>
</head>
<body>
<div id="wrap">

<!-- HUD -->
<div class="hud">
    <div class="hb">🌊 Wave<br><b id="h-wave">0</b>/12</div>
    <div class="hb">⭐ Score<br><b id="h-score">0</b></div>
    <div class="hb">🔐 Shields<br><b id="h-shields">5</b></div>
    <div class="hb">💀 Attacks<br><b id="h-attacks">0</b></div>
    <div class="hb">⚡ Blocked<br><b id="h-blocked">0</b></div>
</div>

<!-- WAVE BANNER / INTEGRITY -->
<div id="wave-banner">
    <span id="wave-text">Press START to begin!</span>
    <div id="integrity-bar-wrap"><div id="integrity-bar" style="width:100%"></div></div>
    <span id="integrity-pct">100%</span>
</div>

<!-- CANVAS WRAPPER -->
<div style="position:relative;width:560px;">
    <canvas id="gc" width="560" height="360"></canvas>
    <div id="overlay">
        <h2 id="overlay-title">Game Over</h2>
        <p id="overlay-msg">The network fell!</p>
        <button class="btn btn-start" onclick="resetGame()">🔄 Play Again</button>
    </div>
</div>

<!-- SHIELD SELECTOR -->
<div id="shield-bar">
    <div class="shield-opt active" onclick="selectShield('kyber',this)" id="sh-kyber">
        <span class="sh-emoji">🔐</span>ML-KEM<br>
        <span class="sh-count" id="cnt-kyber">∞</span>
    </div>
    <div class="shield-opt" onclick="selectShield('dilithium',this)" id="sh-dilithium">
        <span class="sh-emoji">✍️</span>ML-DSA<br>
        <span class="sh-count" id="cnt-dilithium">∞</span>
    </div>
    <div class="shield-opt" onclick="selectShield('sphincs',this)" id="sh-sphincs">
        <span class="sh-emoji">🌲</span>SPHINCS+<br>
        <span class="sh-count" id="cnt-sphincs">∞</span>
    </div>
    <div class="shield-opt" onclick="selectShield('falcon',this)" id="sh-falcon">
        <span class="sh-emoji">🦅</span>Falcon<br>
        <span class="sh-count" id="cnt-falcon">∞</span>
    </div>
</div>

<!-- BUTTONS -->
<div class="btns">
    <button class="btn btn-start" id="start-btn" onclick="startGame()">🏰 START GAME</button>
    <button class="btn btn-blue" id="next-btn" onclick="nextWave()" disabled>Next Wave →</button>
    <button class="btn btn-red" onclick="resetGame()">🔄 Reset</button>
</div>

<div id="msg">Click START to defend your network from Shor Bots!</div>
<div id="fact"></div>
</div>

<div id="toast"></div>

<script>
// ── CANVAS SETUP ──────────────────────────────────────────────────────────────
const cv = document.getElementById('gc');
const cx = cv.getContext('2d');
const W = 560, H = 360;

// ── SHIELD TYPES ──────────────────────────────────────────────────────────────
const SHIELDS = {
    kyber:     {name:'ML-KEM',   emoji:'🔐', color:'#10b981', hp:5, fips:'FIPS 203'},
    dilithium: {name:'ML-DSA',   emoji:'✍️',  color:'#3b82f6', hp:4, fips:'FIPS 204'},
    sphincs:   {name:'SPHINCS+', emoji:'🌲', color:'#8b5cf6', hp:6, fips:'FIPS 205'},
    falcon:    {name:'Falcon',   emoji:'🦅', color:'#f59e0b', hp:4, fips:'FIPS 206'},
};

// ── WAVE CONFIGS ─────────────────────────────────────────────────────────────
const WAVES = [
    {name:'Quantum Probe',    nodeCount:5,  attackRate:1800, maxAtk:2,  reward:200, desc:'Basic Shor bots scanning for RSA!'},
    {name:'Shor Scouts',      nodeCount:6,  attackRate:1600, maxAtk:3,  reward:250, desc:'Scouts found weak nodes!'},
    {name:'Lattice Breach',   nodeCount:6,  attackRate:1400, maxAtk:3,  reward:300, desc:'Cascade failure risk!'},
    {name:'Grover Surge',     nodeCount:7,  attackRate:1200, maxAtk:4,  reward:350, desc:'Grover speedup — attacks faster!'},
    {name:'Multi-Vector',     nodeCount:7,  attackRate:1100, maxAtk:5,  reward:400, desc:'Multiple attack vectors!'},
    {name:'RSA Apocalypse',   nodeCount:8,  attackRate:1000, maxAtk:5,  reward:450, desc:'RSA encryption is broken!'},
    {name:'Quantum Storm',    nodeCount:8,  attackRate:900,  maxAtk:6,  reward:500, desc:'Full quantum storm incoming!'},
    {name:'Shor Blitz',       nodeCount:9,  attackRate:800,  maxAtk:7,  reward:550, desc:'Blitz attack — shields are critical!'},
    {name:'Entanglement',     nodeCount:9,  attackRate:700,  maxAtk:8,  reward:600, desc:'Entangled attackers share damage!'},
    {name:'Quantum Supremacy',nodeCount:10, attackRate:600,  maxAtk:8,  reward:700, desc:'Quantum supremacy activated!'},
    {name:'Final Protocol',   nodeCount:10, attackRate:500,  maxAtk:9,  reward:800, desc:'Final defense protocol!'},
    {name:'LAST STAND',       nodeCount:12, attackRate:400,  maxAtk:10, reward:1000,desc:'LAST STAND — all or nothing!'},
];

// ── PQC FACTS ────────────────────────────────────────────────────────────────
const FACTS = [
    '🔐 ML-KEM (Kyber FIPS 203) protects key exchange — the most important step in any connection!',
    '✍️ ML-DSA (Dilithium FIPS 204) signs every packet — Shor Bots cannot forge signatures!',
    '🌲 SPHINCS+ (FIPS 205) uses hash trees — immune even if lattice math is ever broken!',
    '🦅 Falcon (FIPS 206) makes the smallest signatures — perfect for IoT nodes!',
    '💥 Cascade failures happen when nodes share RSA keys — PQC prevents this!',
    '🌐 Every node in a real network needs its own PQC certificate to stay safe!',
    '☠️ Shor\'s Algorithm attacks RSA by factoring the public key — Kyber has no such weakness!',
    '🏆 NIST mandated PQC by 2035 — your network needs it NOW!',
];

// ── GAME STATE ────────────────────────────────────────────────────────────────
let nodes = [], edges = [], attackers = [], particles = [];
let wave = 0, score = 0, shields = 5, blocked = 0, totalAttacks = 0;
let integrity = 100, maxIntegrity = 100;
let gameActive = false, gameOver = false;
let selectedShield = 'kyber';
let spawnTimer = null, frameId = null;
let hoveredNode = null;

// ── GENERATE NETWORK ─────────────────────────────────────────────────────────
function genNetwork(count) {
    nodes = []; edges = [];

    // Hub at center
    nodes.push({
        id: 0, x: W/2, y: H/2,
        isHub: true, hp: 10, maxHp: 10,
        shield: null, shieldHp: 0,
        compromised: false, pulse: 0,
        connections: [], emoji: '🏛️'
    });

    // Ring of nodes
    const emojis = ['🏦','🏥','🏫','⚡','📡','🌍','🔭','🚀','💊','🏗️','🔬'];
    for (let i = 1; i < count; i++) {
        const angle = ((i-1) / (count-1)) * Math.PI * 2 - Math.PI/2;
        const r = 110 + Math.random() * 50;
        nodes.push({
            id: i,
            x: W/2 + r * Math.cos(angle),
            y: H/2 + r * Math.sin(angle),
            isHub: false, hp: 5, maxHp: 5,
            shield: null, shieldHp: 0,
            compromised: false, pulse: Math.random() * Math.PI * 2,
            connections: [], emoji: emojis[(i-1) % emojis.length]
        });
    }

    // Connect hub to all
    for (let i = 1; i < nodes.length; i++) {
        addEdge(0, i);
    }
    // Connect nearby nodes
    for (let i = 1; i < nodes.length; i++) {
        for (let j = i+1; j < nodes.length; j++) {
            const d = dist(nodes[i], nodes[j]);
            if (d < 170 && !edgeExists(i,j)) addEdge(i, j);
        }
    }
}

function addEdge(a, b) {
    edges.push({a, b, stress: 0});
    nodes[a].connections.push(b);
    nodes[b].connections.push(a);
}

function edgeExists(a, b) {
    return edges.some(e => (e.a===a&&e.b===b)||(e.a===b&&e.b===a));
}

function dist(a, b) { return Math.hypot(a.x-b.x, a.y-b.y); }

// ── ATTACKERS ─────────────────────────────────────────────────────────────────
function spawnAttacker() {
    if (!gameActive) return;
    const cfg = WAVES[wave-1];
    if (attackers.length >= cfg.maxAtk) return;

    // Target weakest unshielded node
    const targets = nodes.filter(n => !n.compromised);
    if (!targets.length) return;
    targets.sort((a,b) => (a.shield?1:0) - (b.shield?1:0) || a.hp - b.hp);
    const target = targets[Math.floor(Math.random() * Math.min(3, targets.length))];

    // Spawn from edge of screen
    const angle = Math.random() * Math.PI * 2;
    const r = 320;
    attackers.push({
        x: W/2 + r * Math.cos(angle),
        y: H/2 + r * Math.sin(angle),
        targetId: target.id,
        speed: 0.8 + wave * 0.08,
        size: 14,
        hp: 2 + Math.floor(wave/3),
        maxHp: 2 + Math.floor(wave/3),
        emoji: ['👾','🤖','💀','🌀','☠️'][Math.floor(Math.random()*5)],
        alpha: 1,
    });
    totalAttacks++;
    updateHUD();
}

function updateAttackers() {
    attackers.forEach((a, ai) => {
        const target = nodes[a.targetId];
        if (!target || target.compromised) {
            // Retarget
            const alive = nodes.filter(n => !n.compromised);
            if (alive.length) a.targetId = alive[Math.floor(Math.random()*alive.length)].id;
            return;
        }

        // Move toward target
        const dx = target.x - a.x, dy = target.y - a.y;
        const d = Math.hypot(dx, dy);
        if (d > 5) {
            a.x += (dx/d) * a.speed;
            a.y += (dy/d) * a.speed;
        } else {
            // Reached target — attack!
            if (target.shield) {
                // Shield absorbs hit
                target.shieldHp--;
                blocked++;
                spawnParticles(target.x, target.y, SHIELDS[target.shield].color, 6);
                showToast('🛡️ '+SHIELDS[target.shield].name+' shield blocked attack!');
                if (target.shieldHp <= 0) {
                    target.shield = null;
                    showToast('💥 Shield destroyed!');
                }
                attackers.splice(ai, 1);
                score += 50;
            } else {
                // Direct hit
                target.hp -= 1;
                spawnParticles(target.x, target.y, '#ef4444', 8);
                if (target.hp <= 0) {
                    compromiseNode(target);
                    attackers.splice(ai, 1);
                } else {
                    attackers.splice(ai, 1);
                }
                integrity = Math.max(0, integrity - (target.isHub ? 20 : 8));
                if (integrity <= 0) endGame(false);
            }
            updateHUD();
        }
    });
}

function compromiseNode(node) {
    node.compromised = true;
    node.hp = 0;
    spawnParticles(node.x, node.y, '#ef4444', 15);
    showFact(FACTS[Math.floor(Math.random()*FACTS.length)]);
    // Cascade — weaken connected nodes
    node.connections.forEach(ci => {
        const cn = nodes[ci];
        if (cn && !cn.compromised) {
            cn.hp = Math.max(1, cn.hp - 1);
            spawnParticles(cn.x, cn.y, '#f97316', 4);
        }
    });
    if (node.isHub) { integrity = 0; endGame(false); }
    setMsg('💥 Node compromised! Cascade damage to connected nodes!');
}

// ── SHIELD PLACEMENT ─────────────────────────────────────────────────────────
cv.addEventListener('click', e => {
    if (!gameActive) return;
    const rect = cv.getBoundingClientRect();
    const mx = (e.clientX - rect.left) * (W / rect.width);
    const my = (e.clientY - rect.top) * (H / rect.height);

    const node = nodes.find(n => Math.hypot(n.x-mx, n.y-my) < 26 && !n.compromised);
    if (!node) return;

    if (shields <= 0) { showToast('❌ No shields left! Survive the wave to get more!'); return; }
    if (node.shield) { showToast('🔐 Already shielded! Wait for it to expire.'); return; }

    node.shield = selectedShield;
    node.shieldHp = SHIELDS[selectedShield].hp;
    shields--;
    score += 10;
    spawnParticles(node.x, node.y, SHIELDS[selectedShield].color, 10);
    showToast('🔐 '+SHIELDS[selectedShield].name+' deployed! '+shields+' shields left.');
    showFact('🔐 '+SHIELDS[selectedShield].name+' ('+SHIELDS[selectedShield].fips+') — '+
        SHIELDS[selectedShield].emoji+' Provides '+SHIELDS[selectedShield].hp+' hits of protection!');
    updateHUD();
});

// Mouse hover for highlight
cv.addEventListener('mousemove', e => {
    const rect = cv.getBoundingClientRect();
    const mx = (e.clientX - rect.left) * (W / rect.width);
    const my = (e.clientY - rect.top) * (H / rect.height);
    hoveredNode = nodes.find(n => Math.hypot(n.x-mx, n.y-my) < 26) || null;
    cv.style.cursor = hoveredNode ? 'pointer' : 'default';
});

// ── PARTICLES ─────────────────────────────────────────────────────────────────
function spawnParticles(x, y, color, n) {
    for (let i = 0; i < n; i++) {
        const a = Math.random() * Math.PI * 2;
        const s = 1 + Math.random() * 4;
        particles.push({x, y, vx: Math.cos(a)*s, vy: Math.sin(a)*s,
            r: 2+Math.random()*3, alpha: 1, color});
    }
}

// ── DRAW ──────────────────────────────────────────────────────────────────────
function draw() {
    cx.clearRect(0, 0, W, H);

    // Background
    cx.fillStyle = '#020d14'; cx.fillRect(0, 0, W, H);

    // Grid
    cx.strokeStyle = '#0a1f2e'; cx.lineWidth = 0.4;
    for (let x = 0; x < W; x += 30) { cx.beginPath(); cx.moveTo(x,0); cx.lineTo(x,H); cx.stroke(); }
    for (let y = 0; y < H; y += 30) { cx.beginPath(); cx.moveTo(0,y); cx.lineTo(W,y); cx.stroke(); }

    // Edges
    edges.forEach(e => {
        const na = nodes[e.a], nb = nodes[e.b];
        if (!na || !nb) return;
        cx.beginPath(); cx.moveTo(na.x, na.y); cx.lineTo(nb.x, nb.y);
        const bothShielded = na.shield && nb.shield;
        const eitherComp = na.compromised || nb.compromised;
        cx.strokeStyle = eitherComp ? '#ef444430' : bothShielded ? '#10b98140' : '#1d4ed830';
        cx.lineWidth = eitherComp ? 1 : bothShielded ? 2 : 1.5;
        if (eitherComp) cx.setLineDash([4,4]); else cx.setLineDash([]);
        cx.stroke(); cx.setLineDash([]);
    });

    // Attackers
    attackers.forEach(a => {
        cx.font = '18px serif';
        cx.textAlign = 'center'; cx.textBaseline = 'middle';
        cx.fillText(a.emoji, a.x, a.y);
        // HP bar
        const bw = 24;
        cx.fillStyle = '#1e293b'; cx.fillRect(a.x-bw/2, a.y-16, bw, 3);
        cx.fillStyle = '#ef4444'; cx.fillRect(a.x-bw/2, a.y-16, bw*(a.hp/a.maxHp), 3);
    });

    // Nodes
    nodes.forEach(n => {
        n.pulse += 0.04;
        const sh = n.shield ? SHIELDS[n.shield] : null;
        const isHovered = n === hoveredNode;

        // Compromised
        if (n.compromised) {
            cx.beginPath(); cx.arc(n.x, n.y, 20, 0, Math.PI*2);
            cx.fillStyle = '#1a0505'; cx.fill();
            cx.strokeStyle = '#ef444440'; cx.lineWidth = 1; cx.stroke();
            cx.font = '14px serif'; cx.textAlign = 'center'; cx.textBaseline = 'middle';
            cx.globalAlpha = 0.4; cx.fillText('💀', n.x, n.y); cx.globalAlpha = 1;
            return;
        }

        // Shield glow
        if (sh) {
            cx.shadowColor = sh.color; cx.shadowBlur = 15;
            cx.beginPath(); cx.arc(n.x, n.y, 26+Math.sin(n.pulse)*2, 0, Math.PI*2);
            cx.strokeStyle = sh.color+'50'; cx.lineWidth = 2; cx.stroke();
            cx.shadowBlur = 0;
        }

        // Hover highlight
        if (isHovered) {
            cx.beginPath(); cx.arc(n.x, n.y, 28, 0, Math.PI*2);
            cx.strokeStyle = '#ffffff30'; cx.lineWidth = 2; cx.stroke();
        }

        // Pulse ring
        cx.beginPath(); cx.arc(n.x, n.y, 20+Math.sin(n.pulse)*2, 0, Math.PI*2);
        cx.strokeStyle = (sh ? sh.color : n.isHub ? '#60a5fa' : '#334155')+'30';
        cx.lineWidth = 1; cx.stroke();

        // HP arc
        if (n.hp < n.maxHp) {
            cx.beginPath();
            cx.arc(n.x, n.y, 22, -Math.PI/2, -Math.PI/2 + (n.hp/n.maxHp)*Math.PI*2);
            cx.strokeStyle = n.hp/n.maxHp > 0.5 ? '#10b981' : '#ef4444';
            cx.lineWidth = 3; cx.stroke();
        }

        // Node body
        cx.beginPath(); cx.arc(n.x, n.y, 20, 0, Math.PI*2);
        cx.fillStyle = n.isHub ? '#0d2a4a' : '#071520';
        cx.fill();
        cx.strokeStyle = sh ? sh.color : n.isHub ? '#3b82f6' : '#334155';
        cx.lineWidth = n.isHub ? 3 : 2; cx.stroke();

        // Emoji
        cx.font = (n.isHub ? '16px' : '14px') + ' serif';
        cx.textAlign = 'center'; cx.textBaseline = 'middle';
        cx.fillText(n.emoji, n.x, n.y);

        // Shield indicator
        if (sh) {
            cx.font = '10px serif';
            cx.fillText(sh.emoji, n.x+14, n.y-14);
            // Shield HP bar
            cx.fillStyle = '#1e293b'; cx.fillRect(n.x-12, n.y-28, 24, 3);
            cx.fillStyle = sh.color; cx.fillRect(n.x-12, n.y-28, 24*(n.shieldHp/sh.hp), 3);
        }

        // HUB label
        if (n.isHub) {
            cx.font = '8px sans-serif'; cx.fillStyle = '#60a5fa';
            cx.textAlign = 'center'; cx.textBaseline = 'top';
            cx.fillText('HUB', n.x, n.y+22);
        }
    });

    // Particles
    particles.forEach(p => {
        cx.beginPath(); cx.arc(p.x, p.y, p.r, 0, Math.PI*2);
        cx.fillStyle = p.color + Math.floor(p.alpha*255).toString(16).padStart(2,'0');
        cx.fill();
    });

    // Wave complete check overlay
    const allSafe = attackers.length === 0 && !gameOver;
}

// ── GAME LOOP ─────────────────────────────────────────────────────────────────
function loop() {
    frameId = requestAnimationFrame(loop);
    if (gameActive) {
        updateAttackers();
        particles.forEach(p => {
            p.x+=p.vx; p.y+=p.vy; p.vy+=0.1;
            p.alpha-=0.025; p.r*=0.96;
        });
        particles = particles.filter(p => p.alpha > 0);

        // Check wave clear
        if (attackers.length === 0 && gameActive && waveClearTimer === null) {
            waveClearTimer = setTimeout(checkWaveClear, 1500);
        }
    }
    draw();
}

let waveClearTimer = null;

function checkWaveClear() {
    waveClearTimer = null;
    if (!gameActive) return;
    const allDown = nodes.every(n => n.compromised);
    if (allDown) { endGame(false); return; }
    if (attackers.length === 0) {
        waveComplete();
    }
}

// ── WAVE MANAGEMENT ───────────────────────────────────────────────────────────
function startGame() {
    wave = 0;
    score = 0;
    shields = 5;
    blocked = 0;
    totalAttacks = 0;
    integrity = 100;
    gameOver = false;
    document.getElementById('overlay').classList.remove('show');
    document.getElementById('start-btn').disabled = true;
    document.getElementById('next-btn').disabled = true;
    if (frameId) cancelAnimationFrame(frameId);
    clearInterval(spawnTimer);
    waveClearTimer = null;
    nextWave();
    loop();
}

function nextWave() {
    wave++;
    if (wave > 12) { endGame(true); return; }
    const cfg = WAVES[wave-1];
    genNetwork(cfg.nodeCount);
    attackers = []; particles = [];
    shields += 3;
    waveClearTimer = null;
    gameActive = true;

    document.getElementById('wave-text').textContent =
        '🌊 Wave '+wave+'/12: '+cfg.name+' — '+cfg.desc;
    document.getElementById('next-btn').disabled = true;
    document.getElementById('h-wave').textContent = wave;
    updateHUD();
    showToast('🌊 Wave '+wave+': '+cfg.name+'!');
    showFact(FACTS[Math.floor(Math.random()*FACTS.length)]);

    clearInterval(spawnTimer);
    spawnTimer = setInterval(() => {
        if (gameActive) spawnAttacker();
    }, cfg.attackRate);
}

function waveComplete() {
    clearInterval(spawnTimer);
    gameActive = false;
    const cfg = WAVES[wave-1];
    score += cfg.reward;
    shields += 2;
    updateHUD();
    showToast('🎉 Wave '+wave+' cleared! +'+cfg.reward+' pts!');
    confetti();

    if (wave >= 12) { endGame(true); return; }
    document.getElementById('next-btn').disabled = false;
    setMsg('✅ Wave '+wave+' cleared! Deploy more shields then click Next Wave!');
}

function endGame(won) {
    clearInterval(spawnTimer);
    gameActive = false;
    gameOver = true;
    document.getElementById('start-btn').disabled = false;

    const overlay = document.getElementById('overlay');
    overlay.classList.add('show');
    document.getElementById('overlay-title').textContent = won ? '👑 NETWORK SECURED!' : '💥 NETWORK COMPROMISED!';
    document.getElementById('overlay-msg').textContent =
        (won ? '🎉 You defended all 12 waves! ' : '💀 The Shor Bots broke through! ') +
        'Final Score: ' + score + ' | Blocked: ' + blocked + ' attacks';

    if (won) confetti();
}

function resetGame() {
    clearInterval(spawnTimer);
    if (frameId) cancelAnimationFrame(frameId);
    nodes=[]; edges=[]; attackers=[]; particles=[];
    document.getElementById('overlay').classList.remove('show');
    document.getElementById('start-btn').disabled = false;
    document.getElementById('next-btn').disabled = true;
    gameActive = false; gameOver = false; wave = 0;
    score=0; shields=5; blocked=0; totalAttacks=0; integrity=100;
    updateHUD();
    setMsg('Click START to defend your network from Shor Bots!');
    cx.clearRect(0,0,W,H);
}

// ── SHIELD SELECTION ──────────────────────────────────────────────────────────
function selectShield(type, btn) {
    selectedShield = type;
    document.querySelectorAll('.shield-opt').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    showFact('Selected: '+SHIELDS[type].emoji+' '+SHIELDS[type].name+
        ' ('+SHIELDS[type].fips+') — '+SHIELDS[type].hp+' hits of quantum protection!');
}

// ── HUD ───────────────────────────────────────────────────────────────────────
function updateHUD() {
    document.getElementById('h-wave').textContent = wave+'/12';
    document.getElementById('h-score').textContent = score;
    document.getElementById('h-shields').textContent = shields;
    document.getElementById('h-attacks').textContent = totalAttacks;
    document.getElementById('h-blocked').textContent = blocked;
    const pct = Math.round(integrity);
    document.getElementById('integrity-bar').style.width = pct+'%';
    document.getElementById('integrity-bar').style.background =
        pct>60?'linear-gradient(90deg,#10b981,#34d399)':
        pct>30?'linear-gradient(90deg,#f59e0b,#fbbf24)':
               'linear-gradient(90deg,#ef4444,#f97316)';
    document.getElementById('integrity-pct').textContent = pct+'%';
    document.getElementById('integrity-pct').style.color =
        pct>60?'#10b981':pct>30?'#fbbf24':'#ef4444';
}

function setMsg(m) { document.getElementById('msg').textContent = m; }

let factTimer = null;
function showFact(t) {
    const el = document.getElementById('fact');
    el.textContent = t; el.style.display = 'block';
    if (factTimer) clearTimeout(factTimer);
    factTimer = setTimeout(() => el.style.display='none', 5000);
}

let toastTimer = null;
function showToast(m) {
    const el = document.getElementById('toast');
    el.textContent = m; el.classList.add('show');
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('show'), 2500);
}

function confetti() {
    const colors = ['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444','#f97316'];
    for (let i=0; i<25; i++) {
        setTimeout(() => {
            const el = document.createElement('div');
            el.className = 'cp';
            el.style.left = Math.random()*100+'vw';
            el.style.background = colors[Math.floor(Math.random()*colors.length)];
            el.style.animationDuration = (1+Math.random()*2)+'s';
            document.body.appendChild(el);
            setTimeout(() => el.remove(), 3000);
        }, i*40);
    }
}

// ── INIT ─────────────────────────────────────────────────────────────────────
updateHUD();
setMsg('👆 Click START to defend your network from Shor Bots!');
</script>
</body>
</html>
""", height=680)

def render_secret_message():
    """Free game: Secret Message Maker — K-5 cipher introduction — UPGRADED 2026!"""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("🔤 Secret Message Maker!")
    st.markdown(
        "**Encrypt messages, decode challenges, and become a Cipher Agent!** "
        "Learn why simple ciphers are NOT quantum-safe — and what IS!"
    )
    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow-x:hidden;}
#wrap{display:flex;flex-direction:column;align-items:center;padding:10px;max-width:560px;margin:0 auto;}

/* HUD */
.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;width:100%;margin-bottom:8px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:5px 3px;
    text-align:center;font-size:9px;color:#60a5fa;}
.hb b{display:block;font-size:15px;color:white;}

/* RANK BADGE */
#rank-bar{background:#071520;border:1px solid #fbbf2440;border-radius:10px;
    padding:6px 12px;width:100%;margin-bottom:8px;
    display:flex;align-items:center;justify-content:space-between;}
#rank-name{font-size:12px;color:#fbbf24;font-weight:bold;}
#rank-xp-bar{flex:1;height:6px;background:#1e293b;border-radius:3px;margin:0 10px;}
#rank-xp-fill{height:6px;background:linear-gradient(90deg,#fbbf24,#f97316);
    border-radius:3px;transition:width 0.5s;width:0%;}
#rank-next{font-size:9px;color:#475569;}

/* TABS */
.tabs{display:flex;gap:3px;width:100%;margin-bottom:8px;}
.tab{flex:1;padding:7px 4px;border-radius:8px;border:1px solid #1a3a5a;
    background:#071520;color:#60a5fa;font-size:11px;font-weight:bold;
    cursor:pointer;text-align:center;transition:all 0.15s;}
.tab:hover{border-color:#3b82f6;}
.tab.active{background:#1d4ed8;border-color:#3b82f6;color:white;}

/* CARDS */
.card{background:#071520;border:1px solid #1a3a5a;border-radius:12px;
    padding:12px;width:100%;margin-bottom:8px;}
.card h4{color:#60a5fa;margin-bottom:8px;font-size:12px;font-weight:bold;}

/* INPUTS */
.msg-input{width:100%;background:#0a1f35;border:2px solid #1d4ed8;border-radius:8px;
    color:white;font-size:13px;padding:9px;outline:none;resize:none;
    font-family:'Segoe UI',sans-serif;}
.msg-input:focus{border-color:#60a5fa;}
.msg-output{width:100%;background:#051018;border:1px solid #1a3a5a;border-radius:8px;
    color:#10b981;font-size:13px;padding:9px;min-height:44px;
    font-family:'Fira Code',monospace;word-break:break-all;line-height:1.6;
    letter-spacing:1px;}

/* CIPHER BUTTONS */
.cipher-select{display:flex;gap:4px;flex-wrap:wrap;margin:6px 0;}
.cipher-btn{padding:5px 10px;border-radius:20px;border:1px solid #1a3a5a;
    background:#071520;color:#60a5fa;font-size:10px;cursor:pointer;
    transition:all 0.1s;}
.cipher-btn:hover{border-color:#3b82f6;}
.cipher-btn.active{background:#1d4ed8;border-color:#3b82f6;color:white;}

/* ACTION BUTTONS */
.btn{padding:7px 14px;border-radius:8px;border:none;cursor:pointer;
    font-size:11px;font-weight:bold;color:white;transition:all 0.15s;}
.btn:hover{filter:brightness(1.2);transform:translateY(-1px);}
.btn-blue{background:#1d4ed8;}
.btn-green{background:#059669;}
.btn-purple{background:#7c3aed;}
.btn-gold{background:linear-gradient(135deg,#b45309,#d97706);}
.btn-row{display:flex;gap:5px;flex-wrap:wrap;justify-content:center;margin:6px 0;}

/* CHALLENGE */
.challenge-card{background:#071520;border:2px solid #7c3aed;border-radius:12px;
    padding:12px;width:100%;margin-bottom:8px;}
.level-badge{display:inline-block;
    background:linear-gradient(135deg,#7c3aed,#1d4ed8);
    border-radius:20px;padding:3px 10px;font-size:10px;font-weight:bold;margin-bottom:6px;}
.encrypted-msg{font-family:'Fira Code',monospace;font-size:15px;color:#fbbf24;
    letter-spacing:3px;background:#051018;padding:10px;border-radius:6px;
    word-break:break-all;margin:8px 0;text-align:center;line-height:1.8;}
.decode-input{width:100%;background:#0a1f35;border:2px solid #7c3aed;
    border-radius:8px;color:white;font-size:13px;padding:8px;outline:none;
    margin-bottom:6px;}
.decode-input:focus{border-color:#a78bfa;}

/* PROGRESS DOTS */
#progress{display:flex;gap:5px;justify-content:center;flex-wrap:wrap;margin:8px 0;}
.pdot{width:14px;height:14px;border-radius:50%;background:#1e293b;
    border:2px solid #334155;transition:all 0.3s;cursor:pointer;}
.pdot.done{background:#10b981;border-color:#10b981;}
.pdot.current{background:#3b82f6;border-color:#60a5fa;
    box-shadow:0 0 8px #3b82f6;}
.pdot.failed{background:#ef4444;border-color:#ef4444;}

/* MESSAGES */
#msg{font-size:11px;color:#34d399;min-height:18px;margin:4px;
    text-align:center;font-weight:bold;}

/* KEY MAP */
.key-display{display:flex;gap:3px;flex-wrap:wrap;margin:6px 0;justify-content:center;}
.key-pair{background:#0a1f35;border:1px solid #1a3a5a;border-radius:4px;
    padding:3px 5px;font-size:9px;color:#60a5fa;font-family:monospace;}
.key-pair span{color:#10b981;}

/* LEARN TAB */
.learn-card{background:#071520;border:1px solid #1a3a5a;border-radius:10px;
    padding:10px;margin-bottom:6px;cursor:pointer;transition:all 0.15s;}
.learn-card:hover{border-color:#3b82f6;background:#0a1f35;}
.learn-card h5{color:#60a5fa;font-size:12px;margin-bottom:4px;}
.learn-card p{font-size:10px;color:#94a3b8;line-height:1.5;}
.safe-badge{display:inline-block;padding:2px 8px;border-radius:10px;
    font-size:9px;font-weight:bold;margin-left:6px;}
.safe-yes{background:#05260f;color:#10b981;border:1px solid #10b981;}
.safe-no{background:#300;color:#ef4444;border:1px solid #ef4444;}

/* ANIMATIONS */
@keyframes pop{0%{transform:scale(1);}50%{transform:scale(1.3);}100%{transform:scale(1);}}
@keyframes shake{0%,100%{transform:translateX(0);}25%{transform:translateX(-5px);}75%{transform:translateX(5px);}}
@keyframes glow{0%,100%{box-shadow:0 0 5px #10b981;}50%{box-shadow:0 0 20px #10b981,0 0 40px #10b981;}}
@keyframes slideIn{from{opacity:0;transform:translateY(-10px);}to{opacity:1;transform:translateY(0);}}
.pop{animation:pop 0.3s ease;}
.shake{animation:shake 0.4s ease;}
.glow{animation:glow 1s ease infinite;}

/* CONFETTI */
.confetti-piece{position:fixed;pointer-events:none;z-index:999;
    width:8px;height:8px;border-radius:2px;
    animation:confettiFall linear forwards;}
@keyframes confettiFall{
    0%{transform:translateY(-20px) rotate(0deg);opacity:1;}
    100%{transform:translateY(600px) rotate(720deg);opacity:0;}
}

/* TOAST */
#toast{position:fixed;top:20px;left:50%;transform:translateX(-50%);
    background:#071520;border:2px solid #10b981;border-radius:10px;
    padding:10px 18px;font-size:12px;color:#10b981;font-weight:bold;
    z-index:100;opacity:0;transition:opacity 0.3s;pointer-events:none;
    text-align:center;}
#toast.show{opacity:1;}

/* MORSE REFERENCE */
.morse-ref{display:flex;flex-wrap:wrap;gap:3px;margin-top:6px;}
.morse-char{background:#0a1f35;border:1px solid #1a3a5a;border-radius:4px;
    padding:2px 4px;font-size:8px;font-family:monospace;color:#60a5fa;}
</style>
</head>
<body>
<div id="wrap">

<!-- HUD -->
<div class="hud">
    <div class="hb">⭐ XP<br><b id="h-xp">0</b></div>
    <div class="hb">🏆 Level<br><b id="h-level">1</b>/12</div>
    <div class="hb">🔥 Streak<br><b id="h-streak">0</b></div>
    <div class="hb">✅ Solved<br><b id="h-solved">0</b></div>
</div>

<!-- RANK BAR -->
<div id="rank-bar">
    <span id="rank-name">🔰 Rookie Agent</span>
    <div id="rank-xp-bar"><div id="rank-xp-fill"></div></div>
    <span id="rank-next">0/100 XP</span>
</div>

<!-- TABS -->
<div class="tabs">
    <div class="tab active" onclick="showTab('encrypt')">🔐 Encrypt</div>
    <div class="tab" onclick="showTab('decode')">🕵️ Decode</div>
    <div class="tab" onclick="showTab('daily')">🎯 Daily</div>
    <div class="tab" onclick="showTab('learn')">📚 Learn</div>
</div>

<div id="msg"></div>

<!-- ═══════════════════════════════════════════════════════════ -->
<!-- ENCRYPT TAB -->
<!-- ═══════════════════════════════════════════════════════════ -->
<div id="tab-encrypt">
    <div class="card">
        <h4>Choose your cipher:</h4>
        <div class="cipher-select">
            <button class="cipher-btn active" onclick="setCipher('substitution',this)">🔄 Substitution</button>
            <button class="cipher-btn" onclick="setCipher('caesar',this)">⚔️ Caesar</button>
            <button class="cipher-btn" onclick="setCipher('reverse',this)">↩️ Reverse</button>
            <button class="cipher-btn" onclick="setCipher('morse',this)">📡 Morse</button>
            <button class="cipher-btn" onclick="setCipher('vigenere',this)">🔑 Vigenère</button>
            <button class="cipher-btn" onclick="setCipher('binary',this)">01 Binary</button>
        </div>
        <div id="cipher-info" style="font-size:10px;color:#64748b;"></div>
    </div>

    <div class="card">
        <h4>✏️ Type your message:</h4>
        <textarea class="msg-input" id="plain-input" rows="2"
            placeholder="Type anything here..."
            oninput="encrypt()">Hello World</textarea>
    </div>

    <div class="card" id="output-card">
        <h4>🔐 Encrypted message:</h4>
        <div class="msg-output" id="cipher-output">—</div>
        <div class="btn-row" style="margin-top:8px">
            <button class="btn btn-blue" onclick="copyEncrypted()">📋 Copy</button>
            <button class="btn btn-purple" onclick="toggleKeyMap()">🗝️ Key</button>
            <button class="btn btn-green" onclick="addXP(5);showToast('✨ +5 XP for encrypting!')">⭐ Encrypt!</button>
        </div>
        <div id="key-map" style="display:none;margin-top:6px;animation:slideIn 0.3s ease">
            <div style="font-size:10px;color:#60a5fa;margin-bottom:4px;">Cipher Key:</div>
            <div class="key-display" id="key-display"></div>
        </div>
        <div id="morse-ref" style="display:none;margin-top:6px;">
            <div style="font-size:10px;color:#60a5fa;margin-bottom:4px;">Morse Reference:</div>
            <div class="morse-ref" id="morse-ref-content"></div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════ -->
<!-- DECODE TAB -->
<!-- ═══════════════════════════════════════════════════════════ -->
<div id="tab-decode" style="display:none">
    <div id="progress"></div>

    <div class="challenge-card" id="challenge-area">
        <div class="level-badge" id="challenge-badge">Level 1</div>
        <div style="font-size:11px;color:#a78bfa;margin-bottom:4px;" id="challenge-cipher-label"></div>
        <div style="font-size:10px;color:#64748b;margin-bottom:6px;" id="challenge-hint"></div>
        <div class="encrypted-msg" id="challenge-msg">—</div>
        <input class="decode-input" id="decode-input" type="text"
               placeholder="Type your answer here..."
               onkeydown="if(event.key==='Enter') checkDecode()"/>
        <div class="btn-row">
            <button class="btn btn-purple" onclick="checkDecode()">✅ Check Answer</button>
            <button class="btn btn-blue" onclick="useHint()">💡 Hint (-5 XP)</button>
            <button class="btn" style="background:#334155" onclick="skipChallenge()">⏭️ Skip</button>
        </div>
        <div id="hint-text" style="font-size:10px;color:#fbbf24;margin-top:4px;display:none;"></div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════ -->
<!-- DAILY CHALLENGE TAB -->
<!-- ═══════════════════════════════════════════════════════════ -->
<div id="tab-daily" style="display:none">
    <div class="card">
        <h4>🎯 Today's Cipher Mission</h4>
        <div style="font-size:10px;color:#64748b;margin-bottom:8px;">
            Complete today's special challenge for bonus XP and a badge!
        </div>
        <div style="background:#051018;border:2px solid #fbbf24;border-radius:8px;
            padding:12px;margin-bottom:10px;">
            <div style="font-size:10px;color:#fbbf24;margin-bottom:4px;">
                🌟 BONUS MISSION — <span id="daily-cipher-name"></span></div>
            <div class="encrypted-msg" id="daily-msg" style="font-size:16px;"></div>
        </div>
        <input class="decode-input" id="daily-input" type="text"
               placeholder="Decode the secret message..."
               style="border-color:#fbbf24;"
               onkeydown="if(event.key==='Enter') checkDaily()"/>
        <div class="btn-row" style="margin-top:6px;">
            <button class="btn btn-gold" onclick="checkDaily()">🌟 Submit Answer</button>
            <button class="btn btn-blue" onclick="showDailyHint()">💡 Hint</button>
        </div>
        <div id="daily-hint-text" style="font-size:10px;color:#fbbf24;margin-top:4px;display:none;"></div>
        <div id="daily-result" style="margin-top:8px;"></div>
    </div>
    <div class="card">
        <h4>📊 Your Stats</h4>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:10px;color:#94a3b8;">
            <div>Total XP: <b id="stats-xp" style="color:white">0</b></div>
            <div>Challenges: <b id="stats-solved" style="color:white">0</b></div>
            <div>Best Streak: <b id="stats-streak" style="color:white">0</b></div>
            <div>Rank: <b id="stats-rank" style="color:#fbbf24">Rookie</b></div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════ -->
<!-- LEARN TAB -->
<!-- ═══════════════════════════════════════════════════════════ -->
<div id="tab-learn" style="display:none">
    <div class="card">
        <h4>📚 Cipher History & Quantum Safety</h4>
    </div>
    <div class="learn-card" onclick="expandLearn(this)">
        <h5>⚔️ Caesar Cipher (100 BC) <span class="safe-badge safe-no">❌ NOT Quantum Safe</span></h5>
        <p>Julius Caesar shifted letters by 3. Easy to break — only 25 possible keys!
           A quantum computer breaks this in microseconds.</p>
    </div>
    <div class="learn-card" onclick="expandLearn(this)">
        <h5>🔄 Substitution Cipher <span class="safe-badge safe-no">❌ NOT Quantum Safe</span></h5>
        <p>Each letter maps to another. 400 septillion possible keys but frequency analysis breaks it easily.
           Quantum computers use Grover's algorithm to search all keys instantly.</p>
    </div>
    <div class="learn-card" onclick="expandLearn(this)">
        <h5>🔑 Vigenère Cipher (1553) <span class="safe-badge safe-no">❌ NOT Quantum Safe</span></h5>
        <p>Uses a keyword to shift letters differently. Stronger than Caesar but still breakable
           with the Kasiski test. Quantum computers destroy it.</p>
    </div>
    <div class="learn-card" onclick="expandLearn(this)">
        <h5>📡 Morse Code (1836) <span class="safe-badge safe-no">❌ NOT Quantum Safe</span></h5>
        <p>Dots and dashes — not even a cipher, just an encoding! Anyone with a chart can read it instantly.</p>
    </div>
    <div class="learn-card" onclick="expandLearn(this)" style="border-color:#10b981;">
        <h5>🔐 ML-KEM Kyber (2024) <span class="safe-badge safe-yes">✅ QUANTUM SAFE!</span></h5>
        <p>FIPS 203 — Uses lattice math with billions of dimensions. Not even quantum computers
           using Shor's or Grover's algorithm can break it. This is the future!</p>
    </div>
    <div class="learn-card" onclick="expandLearn(this)" style="border-color:#10b981;">
        <h5>✍️ ML-DSA Dilithium (2024) <span class="safe-badge safe-yes">✅ QUANTUM SAFE!</span></h5>
        <p>FIPS 204 — Creates digital signatures no quantum computer can forge.
           Used to sign software, documents, and certificates.</p>
    </div>
    <div style="background:#051018;border:1px solid #10b981;border-radius:8px;
        padding:10px;margin-top:6px;font-size:10px;color:#34d399;text-align:center;">
        🔐 The ciphers you learned today are for FUN and history.<br>
        Real encryption uses <b>NIST PQC Standards (FIPS 203-206)</b> — unbreakable even by quantum computers!
    </div>
</div>

</div><!-- end wrap -->

<!-- TOAST -->
<div id="toast"></div>

<script>
// ── GAME STATE ────────────────────────────────────────────────────────────────
let xp=0, level=1, streak=0, solved=0, bestStreak=0;
let currentCipher='substitution';
let challengeIdx=0;
let hintsUsed=0;
let dailyDone=false;

// ── RANKS ─────────────────────────────────────────────────────────────────────
const RANKS=[
    {name:'🔰 Rookie Agent',   xp:0},
    {name:'🕵️ Junior Spy',    xp:50},
    {name:'🔐 Cipher Cadet',  xp:120},
    {name:'⚡ Code Breaker',  xp:220},
    {name:'🌟 Crypto Expert', xp:350},
    {name:'🏆 Master Agent',  xp:500},
    {name:'💎 Quantum Guard', xp:700},
];

// ── SUBSTITUTION KEY ──────────────────────────────────────────────────────────
const SUB_KEY = (function(){
    const alpha='ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
    const shuffled=[...alpha].sort(()=>0.5-Math.random());
    const key={};
    alpha.forEach((c,i)=>{ key[c]=shuffled[i]; key[c.toLowerCase()]=shuffled[i].toLowerCase(); });
    return key;
})();

// ── VIGENERE KEY ──────────────────────────────────────────────────────────────
const VIG_KEY='KYBER';

// ── MORSE MAP ─────────────────────────────────────────────────────────────────
const MORSE={
    A:'.-',B:'-...',C:'-.-.',D:'-..', E:'.',F:'..-.',G:'--.',H:'....',
    I:'..',J:'.---',K:'-.-',L:'.-..',M:'--',N:'-.',O:'---',P:'.--.',
    Q:'--.-',R:'.-.',S:'...',T:'-',U:'..-',V:'...-',W:'.--',X:'-..-',
    Y:'-.--',Z:'--..',
    '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-',
    '5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
    ' ':'/'
};

// ── CHALLENGES ────────────────────────────────────────────────────────────────
const CHALLENGES=[
    {cipher:'caesar',  msg:'KHOOR',         answer:'HELLO',      hint:'Shift each letter BACK by 3',       pts:10, label:'Caesar Cipher'},
    {cipher:'reverse', msg:'TERCES',         answer:'SECRET',     hint:'Read the message backwards!',       pts:10, label:'Reverse Cipher'},
    {cipher:'caesar',  msg:'ZRUOG',          answer:'WORLD',      hint:'Caesar shift back 3 letters',       pts:15, label:'Caesar Cipher'},
    {cipher:'morse',   msg:'--. --- ---',    answer:'GOO',        hint:'G=--. O=---',                       pts:20, label:'Morse Code'},
    {cipher:'caesar',  msg:'TXDQWXP',        answer:'QUANTUM',    hint:'Shift back 3 — Q becomes N... wait, forward 3!', pts:20, label:'Caesar Cipher'},
    {cipher:'reverse', msg:'REPEHC',         answer:'CIPHER',     hint:'Reverse the letters!',              pts:20, label:'Reverse Cipher'},
    {cipher:'morse',   msg:'.- -... -.-.', answer:'ABC',        hint:'A=.- B=-... C=-.-.',                pts:25, label:'Morse Code'},
    {cipher:'caesar',  msg:'FUBSWR',         answer:'CRYPTO',     hint:'Caesar shift back 3',               pts:25, label:'Caesar Cipher'},
    {cipher:'binary',  msg:'01001000 01001001', answer:'HI',     hint:'H=72=01001000 I=73=01001001',       pts:30, label:'Binary Code'},
    {cipher:'reverse', msg:'RETAUQ',         answer:'QUATER',     hint:'Backwards!',                        pts:30, label:'Reverse Cipher'},
    {cipher:'caesar',  msg:'ODLOKD',         answer:'LAILE',      hint:'Wait — shift back 3 carefully!',   pts:35, label:'Caesar Cipher'},
    {cipher:'morse',   msg:'.-- --- .--',   answer:'WOW',        hint:'W=.-- O=---',                       pts:40, label:'Morse Code'},
];

// ── DAILY CHALLENGE ───────────────────────────────────────────────────────────
const DAILY={
    cipher:'substitution',
    msg:'QUANTUM VAULT ACADEMY',
    answer:'QUANTUM VAULT ACADEMY',
    hint:'This one is NOT encrypted — some messages are already safe!',
    pts:50,
    label:'Special Mission'
};

// ── CIPHER FUNCTIONS ─────────────────────────────────────────────────────────
function caesarEncrypt(text, shift){
    return text.split('').map(c=>{
        if(c>='A'&&c<='Z') return String.fromCharCode((c.charCodeAt(0)-65+shift)%26+65);
        if(c>='a'&&c<='z') return String.fromCharCode((c.charCodeAt(0)-97+shift)%26+97);
        return c;
    }).join('');
}

function substitutionEncrypt(text){
    return text.split('').map(c=>SUB_KEY[c]||c).join('');
}

function reverseEncrypt(text){ return text.split('').reverse().join(''); }

function morseEncrypt(text){
    return text.toUpperCase().split('').map(c=>MORSE[c]||c).join(' ');
}

function vigenereEncrypt(text){
    let result='', ki=0;
    for(let c of text){
        if(c.match(/[a-zA-Z]/)){
            const shift=VIG_KEY.charCodeAt(ki%VIG_KEY.length)-65;
            const base=c>='a'?97:65;
            result+=String.fromCharCode((c.toUpperCase().charCodeAt(0)-65+shift)%26+65);
            ki++;
        } else result+=c;
    }
    return result;
}

function binaryEncrypt(text){
    return text.split('').map(c=>c.charCodeAt(0).toString(2).padStart(8,'0')).join(' ');
}

function encrypt(){
    const text=document.getElementById('plain-input').value;
    let result='';
    switch(currentCipher){
        case 'caesar':      result=caesarEncrypt(text,3); break;
        case 'substitution':result=substitutionEncrypt(text); break;
        case 'reverse':     result=reverseEncrypt(text); break;
        case 'morse':       result=morseEncrypt(text); break;
        case 'vigenere':    result=vigenereEncrypt(text); break;
        case 'binary':      result=binaryEncrypt(text); break;
    }
    const el=document.getElementById('cipher-output');
    el.textContent=result||'—';
    el.classList.add('pop');
    setTimeout(()=>el.classList.remove('pop'),300);
}

// ── CIPHER SELECTION ─────────────────────────────────────────────────────────
const CIPHER_INFO={
    substitution:'🔄 Each letter swaps to a different letter using a secret key. 400 septillion possibilities!',
    caesar:'⚔️ Shift every letter by 3. Julius Caesar used this in 100 BC!',
    reverse:'↩️ Write your message backwards. Simple but surprising!',
    morse:'📡 Dots and dashes — invented in 1836 for telegraph machines!',
    vigenere:'🔑 Uses the keyword KYBER to shift each letter differently. Stronger than Caesar!',
    binary:'01 Every character becomes 8 bits. How computers actually store text!',
};

function setCipher(c, btn){
    currentCipher=c;
    document.querySelectorAll('.cipher-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('cipher-info').textContent=CIPHER_INFO[c]||'';
    document.getElementById('key-map').style.display='none';
    document.getElementById('morse-ref').style.display='none';
    encrypt();
    addXP(2);
    showToast('🔐 Switched to '+c+' cipher! +2 XP');
}

function toggleKeyMap(){
    if(currentCipher==='morse'){
        const ref=document.getElementById('morse-ref');
        ref.style.display=ref.style.display==='none'?'block':'none';
        // Build morse reference
        const content=document.getElementById('morse-ref-content');
        content.innerHTML='';
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').forEach(c=>{
            const d=document.createElement('div');
            d.className='morse-char';
            d.textContent=c+':'+MORSE[c];
            content.appendChild(d);
        });
    } else {
        const km=document.getElementById('key-map');
        km.style.display=km.style.display==='none'?'block':'none';
        // Build key map
        const kd=document.getElementById('key-display');
        kd.innerHTML='';
        if(currentCipher==='substitution'){
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').forEach(c=>{
                const d=document.createElement('div');
                d.className='key-pair';
                d.innerHTML=c+'→<span>'+SUB_KEY[c]+'</span>';
                kd.appendChild(d);
            });
        } else if(currentCipher==='caesar'){
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').forEach((c,i)=>{
                const shifted=String.fromCharCode((i+3)%26+65);
                const d=document.createElement('div');
                d.className='key-pair';
                d.innerHTML=c+'→<span>'+shifted+'</span>';
                kd.appendChild(d);
            });
        } else if(currentCipher==='vigenere'){
            const d=document.createElement('div');
            d.className='key-pair';
            d.innerHTML='Key: <span>'+VIG_KEY+'</span>';
            kd.appendChild(d);
        }
    }
}

function copyEncrypted(){
    const text=document.getElementById('cipher-output').textContent;
    if(navigator.clipboard) navigator.clipboard.writeText(text);
    showToast('📋 Copied to clipboard!');
    addXP(3);
}

// ── DECODE CHALLENGES ─────────────────────────────────────────────────────────
function loadChallenge(){
    if(challengeIdx>=CHALLENGES.length){
        document.getElementById('challenge-area').innerHTML=
            '<div style="text-align:center;padding:20px;">'+
            '<div style="font-size:3rem">🏆</div>'+
            '<h3 style="color:#fbbf24;margin:8px 0">All Challenges Complete!</h3>'+
            '<p style="color:#94a3b8;font-size:11px">You decoded all '+CHALLENGES.length+' messages!</p>'+
            '<button class="btn btn-gold" style="margin-top:10px" onclick="resetChallenges()">🔄 Play Again</button>'+
            '</div>';
        confetti();
        return;
    }
    const ch=CHALLENGES[challengeIdx];
    document.getElementById('challenge-badge').textContent='Level '+(challengeIdx+1);
    document.getElementById('challenge-cipher-label').textContent='Cipher: '+ch.label;
    document.getElementById('challenge-hint').textContent='';
    document.getElementById('challenge-msg').textContent=ch.msg;
    document.getElementById('decode-input').value='';
    document.getElementById('hint-text').style.display='none';
    document.getElementById('hint-text').textContent='';
    hintsUsed=0;
    buildProgressDots();
}

function buildProgressDots(){
    const p=document.getElementById('progress');
    p.innerHTML='';
    CHALLENGES.forEach((_,i)=>{
        const d=document.createElement('div');
        d.className='pdot'+(i<challengeIdx?' done':i===challengeIdx?' current':'');
        d.title='Level '+(i+1);
        p.appendChild(d);
    });
}

function checkDecode(){
    const input=document.getElementById('decode-input').value.trim().toUpperCase();
    const ch=CHALLENGES[challengeIdx];
    if(input===ch.answer.toUpperCase()){
        // Correct!
        streak++; solved++;
        bestStreak=Math.max(bestStreak,streak);
        const bonus=streak>=3?10:0;
        addXP(ch.pts+bonus);
        showToast('🎉 CORRECT! +'+(ch.pts+bonus)+' XP'+(bonus?' (Streak Bonus!)':''));
        setMsg('🎉 Correct! '+(streak>=3?'🔥 '+streak+' streak! Bonus XP!':''));
        document.getElementById('decode-input').classList.add('glow');
        setTimeout(()=>{
            document.getElementById('decode-input').classList.remove('glow');
            challengeIdx++;
            loadChallenge();
        },1200);
        if(streak===3) showToast('🔥 3 STREAK! Bonus XP unlocked!');
        if(streak===5) confetti();
    } else {
        // Wrong
        streak=0;
        document.getElementById('decode-input').classList.add('shake');
        setTimeout(()=>document.getElementById('decode-input').classList.remove('shake'),400);
        setMsg('❌ Not quite! Try again...');
        updateHUD();
    }
    updateHUD();
}

function useHint(){
    const ch=CHALLENGES[challengeIdx];
    hintsUsed++;
    xp=Math.max(0,xp-5);
    document.getElementById('hint-text').textContent='💡 Hint: '+ch.hint;
    document.getElementById('hint-text').style.display='block';
    showToast('💡 Hint used! -5 XP');
    updateHUD();
}

function skipChallenge(){
    streak=0;
    challengeIdx++;
    loadChallenge();
    updateHUD();
}

function resetChallenges(){
    challengeIdx=0;
    loadChallenge();
}

// ── DAILY CHALLENGE ───────────────────────────────────────────────────────────
function setupDaily(){
    document.getElementById('daily-cipher-name').textContent=DAILY.label;
    document.getElementById('daily-msg').textContent=DAILY.msg;
}

function checkDaily(){
    if(dailyDone){ showToast('✅ Daily challenge already completed!'); return; }
    const input=document.getElementById('daily-input').value.trim().toUpperCase();
    const result=document.getElementById('daily-result');
    if(input===DAILY.answer.toUpperCase()){
        dailyDone=true;
        addXP(DAILY.pts);
        result.innerHTML='<div style="text-align:center;padding:10px;">'+
            '<div style="font-size:2rem">🌟</div>'+
            '<div style="color:#fbbf24;font-weight:bold;font-size:13px">Daily Mission Complete!</div>'+
            '<div style="color:#94a3b8;font-size:10px;margin-top:4px">+'+DAILY.pts+' Bonus XP!</div>'+
            '</div>';
        confetti();
        showToast('🌟 Daily Mission Complete! +'+DAILY.pts+' XP!');
    } else {
        result.innerHTML='<div style="color:#ef4444;font-size:11px;text-align:center">Not quite! Keep trying!</div>';
        streak=0; updateHUD();
    }
}

function showDailyHint(){
    document.getElementById('daily-hint-text').textContent='💡 '+DAILY.hint;
    document.getElementById('daily-hint-text').style.display='block';
}

// ── LEARN TAB ─────────────────────────────────────────────────────────────────
function expandLearn(el){
    const p=el.querySelector('p');
    p.style.display=p.style.display==='none'?'block':'none';
    addXP(1);
}

// ── XP & RANKS ────────────────────────────────────────────────────────────────
function addXP(amount){
    xp+=amount;
    // Check level up
    const newLevel=CHALLENGES.filter((_,i)=>i<challengeIdx).length+1;
    if(newLevel>level){
        level=newLevel;
        showToast('🎉 LEVEL UP! Level '+level+'!');
        confetti();
    }
    updateHUD();
}

function getRank(){
    let rank=RANKS[0];
    for(const r of RANKS){ if(xp>=r.xp) rank=r; }
    return rank;
}

function getNextRank(){
    for(const r of RANKS){ if(r.xp>xp) return r; }
    return null;
}

function updateHUD(){
    document.getElementById('h-xp').textContent=xp;
    document.getElementById('h-level').textContent=Math.min(challengeIdx+1,12);
    document.getElementById('h-streak').textContent=streak;
    document.getElementById('h-solved').textContent=solved;

    const rank=getRank();
    const next=getNextRank();
    document.getElementById('rank-name').textContent=rank.name;
    document.getElementById('stats-rank').textContent=rank.name;
    document.getElementById('stats-xp').textContent=xp;
    document.getElementById('stats-solved').textContent=solved;
    document.getElementById('stats-streak').textContent=bestStreak;

    if(next){
        const pct=Math.min(100,((xp-rank.xp)/(next.xp-rank.xp))*100);
        document.getElementById('rank-xp-fill').style.width=pct+'%';
        document.getElementById('rank-next').textContent=xp+'/'+next.xp+' XP';
    } else {
        document.getElementById('rank-xp-fill').style.width='100%';
        document.getElementById('rank-next').textContent='MAX RANK! 💎';
    }
}

function setMsg(msg){ document.getElementById('msg').textContent=msg; }

// ── TOAST ─────────────────────────────────────────────────────────────────────
let toastTimer=null;
function showToast(msg){
    const el=document.getElementById('toast');
    el.textContent=msg; el.classList.add('show');
    if(toastTimer) clearTimeout(toastTimer);
    toastTimer=setTimeout(()=>el.classList.remove('show'),2500);
}

// ── CONFETTI ──────────────────────────────────────────────────────────────────
function confetti(){
    const colors=['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444','#f97316'];
    for(let i=0;i<30;i++){
        setTimeout(()=>{
            const el=document.createElement('div');
            el.className='confetti-piece';
            el.style.left=Math.random()*100+'vw';
            el.style.background=colors[Math.floor(Math.random()*colors.length)];
            el.style.animationDuration=(1+Math.random()*2)+'s';
            el.style.animationDelay=Math.random()*0.5+'s';
            el.style.borderRadius=Math.random()>0.5?'50%':'2px';
            document.body.appendChild(el);
            setTimeout(()=>el.remove(),3000);
        },i*50);
    }
}

// ── TABS ──────────────────────────────────────────────────────────────────────
function showTab(tab){
    ['encrypt','decode','daily','learn'].forEach(t=>{
        document.getElementById('tab-'+t).style.display=t===tab?'block':'none';
    });
    document.querySelectorAll('.tab').forEach((el,i)=>{
        el.classList.toggle('active',['encrypt','decode','daily','learn'][i]===tab);
    });
    if(tab==='decode') loadChallenge();
    if(tab==='daily') setupDaily();
}

// ── INIT ─────────────────────────────────────────────────────────────────────
setCipher('substitution', document.querySelector('.cipher-btn'));
encrypt();
updateHUD();
buildProgressDots();
setMsg('🔐 Type a message above to encrypt it — or try the Decode tab!');
</script>
</body>
</html>
""", height=720)

def render_ctf_game():
    """Free game: QuantumVault CTF v2 — Hacker terminal UI with dramatic story, animations, real challenges."""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("🚩 Operation Quantum Shield — PQC CTF")
    st.markdown(
        "**You are Agent CIPHER.** A hostile quantum computer is attacking global infrastructure. "
        "Complete 12 hacking missions using real post-quantum cryptography knowledge. "
        "Each mission unlocks the next. Faster = more points."
    )
    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#000;font-family:'Share Tech Mono',monospace;color:#00ff41;overflow-x:hidden;}

/* TERMINAL */
#terminal{width:100%;max-width:560px;margin:0 auto;background:#000;
    border:1px solid #00ff4130;position:relative;}

/* TOP BAR */
#topbar{background:#0a0a0a;border-bottom:1px solid #00ff4120;
    padding:6px 12px;display:flex;justify-content:space-between;align-items:center;}
.tb-title{font-family:'Orbitron',sans-serif;font-size:11px;color:#00ff41;letter-spacing:2px;}
.tb-status{font-size:9px;color:#00ff4160;display:flex;gap:10px;}
.status-dot{width:6px;height:6px;border-radius:50%;background:#00ff41;
    display:inline-block;animation:blink 1s infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}}

/* HUD */
#hud{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
    background:#00ff4110;border-bottom:1px solid #00ff4120;}
.hud-cell{background:#000;padding:6px 4px;text-align:center;font-size:9px;color:#00ff4170;}
.hud-cell b{display:block;font-size:14px;color:#00ff41;font-family:'Orbitron',sans-serif;}

/* MAIN SCREEN */
#screen{padding:12px;min-height:400px;position:relative;}

/* BOOT SEQUENCE */
#boot{display:block;}
.boot-line{font-size:11px;color:#00ff41;margin:2px 0;opacity:0;}
.boot-line.show{animation:fadeIn 0.1s forwards;}
@keyframes fadeIn{to{opacity:1}}
#boot-bar{height:3px;background:#00ff4120;margin:8px 0;border-radius:2px;overflow:hidden;}
#boot-fill{height:100%;width:0%;background:#00ff41;transition:width 0.3s;}

/* MISSION MAP */
#mission-map{display:none;}
.map-title{font-family:'Orbitron',sans-serif;font-size:12px;color:#00ff41;
    text-align:center;margin:8px 0;letter-spacing:3px;}
.map-subtitle{font-size:9px;color:#00ff4150;text-align:center;margin-bottom:10px;}
#mission-list{display:flex;flex-direction:column;gap:4px;}
.mission-item{display:flex;align-items:center;gap:8px;padding:8px 10px;
    border:1px solid #00ff4120;border-radius:4px;cursor:pointer;transition:all 0.2s;
    background:#050505;}
.mission-item:hover:not(.locked){border-color:#00ff41;background:#001a00;}
.mission-item.locked{opacity:0.35;cursor:not-allowed;}
.mission-item.done{border-color:#00ff4160;background:#001a00;}
.mission-item.active-mission{border-color:#ffff00;background:#1a1a00;}
.m-num{font-family:'Orbitron',sans-serif;font-size:14px;color:#00ff41;
    min-width:28px;text-align:center;}
.m-num.done{color:#00ff41;}
.m-num.locked{color:#333;}
.m-info{flex:1;}
.m-name{font-size:11px;color:#00ff41;margin-bottom:1px;}
.m-desc{font-size:9px;color:#00ff4150;}
.m-pts{font-size:9px;color:#00ff4190;text-align:right;min-width:50px;}
.m-status{font-size:14px;min-width:20px;text-align:center;}

/* ACTIVE MISSION */
#active-mission{display:none;}
.mission-header-bar{background:#001a00;border:1px solid #00ff4140;border-radius:4px;
    padding:8px 12px;margin-bottom:10px;}
.mission-codename{font-family:'Orbitron',sans-serif;font-size:10px;color:#00ff41;
    letter-spacing:2px;margin-bottom:3px;}
.mission-objective{font-size:10px;color:#00ff4180;line-height:1.5;}

/* TIMER */
#timer-bar-wrap{margin:6px 0;}
#tbar{height:4px;background:#00ff4115;border-radius:2px;overflow:hidden;}
#tfill{height:100%;background:#00ff41;border-radius:2px;transition:width 1s linear;}
#ttext{font-size:9px;color:#00ff4160;margin-top:2px;text-align:right;}

/* CHALLENGE BOX */
.challenge-box{background:#050505;border:1px solid #00ff4120;border-radius:4px;
    padding:10px;margin:8px 0;font-size:11px;color:#00ff41;line-height:1.7;}
.code-terminal{background:#000;border:1px solid #00ff4140;border-radius:3px;
    padding:8px;font-size:11px;color:#00ff41;margin:6px 0;word-break:break-all;
    letter-spacing:1px;position:relative;}
.code-terminal::before{content:'> ';color:#00ff4160;}

/* MCQ OPTIONS */
.options{display:flex;flex-direction:column;gap:5px;margin:8px 0;}
.opt{padding:8px 10px;border:1px solid #00ff4130;border-radius:3px;
    font-size:10px;color:#00ff41;cursor:pointer;transition:all 0.15s;
    background:#050505;display:flex;gap:8px;align-items:flex-start;}
.opt:hover{border-color:#00ff41;background:#001a00;}
.opt-key{color:#00ff4170;min-width:14px;}
.opt.correct{border-color:#00ff41;background:#001a00;animation:flashGreen 0.5s;}
.opt.wrong{border-color:#ff0040;color:#ff0040;background:#1a0008;}
@keyframes flashGreen{0%{background:#00ff4130}100%{background:#001a00}}

/* INPUT */
.terminal-input-wrap{display:flex;gap:6px;margin:8px 0;align-items:center;}
.prompt{color:#00ff4160;font-size:12px;white-space:nowrap;}
.terminal-input{flex:1;background:#000;border:none;border-bottom:1px solid #00ff41;
    color:#00ff41;font-family:'Share Tech Mono',monospace;font-size:12px;
    padding:4px 6px;outline:none;}
.terminal-input::placeholder{color:#00ff4130;}
.exec-btn{padding:5px 12px;background:#00ff4115;border:1px solid #00ff41;
    color:#00ff41;font-family:'Share Tech Mono',monospace;font-size:11px;
    cursor:pointer;border-radius:2px;}
.exec-btn:hover{background:#00ff4130;}

/* FACTOR */
.factor-display{font-family:'Orbitron',sans-serif;font-size:2.5rem;color:#00ff41;
    text-align:center;margin:10px 0;text-shadow:0 0 20px #00ff41;}
.factor-inputs{display:flex;gap:8px;align-items:center;justify-content:center;margin:8px 0;}
.factor-in{width:100px;background:#000;border:1px solid #00ff41;color:#00ff41;
    font-family:'Share Tech Mono',monospace;font-size:14px;padding:6px;
    text-align:center;outline:none;}
.x-sign{font-size:1.2rem;color:#00ff4160;}

/* HINTS */
.hints-bar{display:flex;gap:4px;margin:6px 0;flex-wrap:wrap;}
.hint-btn{padding:3px 8px;border:1px solid #00ff4130;color:#00ff4170;
    font-family:'Share Tech Mono',monospace;font-size:9px;cursor:pointer;
    background:transparent;}
.hint-btn:hover{border-color:#00ff41;color:#00ff41;}
.hint-btn.used{color:#333;border-color:#111;cursor:default;}
#hint-out{font-size:10px;color:#ffff00;margin:4px 0;display:none;line-height:1.5;
    border-left:2px solid #ffff00;padding-left:8px;}

/* MSG */
#msg-line{font-size:11px;min-height:18px;margin:4px 0;}
#fact-out{font-size:10px;color:#00ff4190;margin:6px 0;display:none;
    border-left:2px solid #00ff41;padding-left:8px;line-height:1.6;}

/* BOTTOM BUTTONS */
.bot-btns{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0;}
.b-btn{padding:6px 14px;border:1px solid #00ff4140;color:#00ff41;
    font-family:'Share Tech Mono',monospace;font-size:10px;cursor:pointer;
    background:transparent;transition:all 0.15s;}
.b-btn:hover{background:#00ff4115;border-color:#00ff41;}

/* FLAG OVERLAY */
#flag-overlay{display:none;position:fixed;inset:0;background:#000e00;z-index:999;
    flex-direction:column;align-items:center;justify-content:center;text-align:center;
    font-family:'Share Tech Mono',monospace;}
#flag-overlay.show{display:flex;}
.flag-ascii{font-size:3rem;animation:flagPop 0.4s ease-out;}
@keyframes flagPop{0%{transform:scale(0);opacity:0}70%{transform:scale(1.3)}100%{transform:scale(1);opacity:1}}
.flag-word{font-family:'Orbitron',sans-serif;font-size:1.3rem;color:#00ff41;
    letter-spacing:4px;margin:8px 0;text-shadow:0 0 20px #00ff41;}
.flag-code{font-size:12px;color:#00ff4180;letter-spacing:2px;margin:4px 0;}
.flag-pts-disp{font-size:14px;color:#ffff00;margin:6px 0;}
.flag-fact{font-size:10px;color:#00ff4170;max-width:320px;line-height:1.6;margin:8px auto;}
.cont-btn{margin-top:14px;padding:8px 24px;border:1px solid #00ff41;color:#00ff41;
    font-family:'Orbitron',sans-serif;font-size:11px;cursor:pointer;background:transparent;
    letter-spacing:2px;}
.cont-btn:hover{background:#00ff4115;}

/* GAME OVER / WIN */
#endscreen{display:none;padding:20px;text-align:center;}
.end-title{font-family:'Orbitron',sans-serif;font-size:1.4rem;letter-spacing:3px;margin:10px 0;}
.end-score{font-size:2rem;color:#00ff41;font-family:'Orbitron',sans-serif;margin:8px 0;}
.end-stats{font-size:10px;color:#00ff4170;line-height:2;margin:8px 0;}

/* SCANLINE */
#screen::after{content:'';position:absolute;inset:0;pointer-events:none;
    background:repeating-linear-gradient(transparent,transparent 2px,rgba(0,255,65,0.015) 2px,rgba(0,255,65,0.015) 4px);}
</style>
</head>
<body>

<!-- FLAG OVERLAY -->
<div id="flag-overlay">
    <div class="flag-ascii">🚩</div>
    <div class="flag-word">FLAG CAPTURED</div>
    <div class="flag-code" id="fo-code">FLAG{...}</div>
    <div class="flag-pts-disp" id="fo-pts">+500 PTS</div>
    <div class="flag-fact" id="fo-fact"></div>
    <button class="cont-btn" onclick="closeFlagOverlay()">[ CONTINUE ]</button>
</div>

<div id="terminal">
    <!-- TOP BAR -->
    <div id="topbar">
        <div class="tb-title">QUANTUMVAULT // OPERATION QUANTUM SHIELD</div>
        <div class="tb-status">
            <span><span class="status-dot"></span> AGENT CIPHER</span>
            <span>SYS:ONLINE</span>
        </div>
    </div>

    <!-- HUD -->
    <div id="hud">
        <div class="hud-cell">SCORE<br><b id="h-score">0</b></div>
        <div class="hud-cell">FLAGS<br><b id="h-flags">0/12</b></div>
        <div class="hud-cell">HINTS<br><b id="h-hints">3</b></div>
        <div class="hud-cell">RANK<br><b id="h-rank">RECRUIT</b></div>
    </div>

    <div id="screen">

        <!-- BOOT SEQUENCE -->
        <div id="boot">
            <div id="boot-lines"></div>
            <div id="boot-bar"><div id="boot-fill"></div></div>
            <div id="boot-status" style="font-size:9px;color:#00ff4150;text-align:center;margin-top:4px;"></div>
            <div style="text-align:center;margin-top:16px;display:none" id="start-wrap">
                <div style="font-family:'Orbitron',sans-serif;font-size:11px;color:#00ff41;letter-spacing:2px;margin-bottom:10px">
                    AUTHENTICATION REQUIRED
                </div>
                <button class="b-btn" style="font-size:12px;padding:10px 24px;border-color:#00ff41"
                    onclick="showMissionMap()">[ INITIATE OPERATION ]</button>
            </div>
        </div>

        <!-- MISSION MAP -->
        <div id="mission-map">
            <div class="map-title">// MISSION SELECT //</div>
            <div class="map-subtitle">12 OBJECTIVES — COMPLETE IN ORDER TO UNLOCK</div>
            <div id="mission-list"></div>
        </div>

        <!-- ACTIVE MISSION -->
        <div id="active-mission">
            <div class="mission-header-bar">
                <div class="mission-codename" id="m-codename">MISSION 01 // THE RSA BREACH</div>
                <div class="mission-objective" id="m-obj">Loading...</div>
            </div>
            <div id="timer-bar-wrap">
                <div id="tbar"><div id="tfill" style="width:100%"></div></div>
                <div id="ttext">60s</div>
            </div>
            <div id="challenge-content"></div>
            <div class="hints-bar">
                <button class="hint-btn" id="hbtn1" onclick="useHint(0)">HINT_1 [-50]</button>
                <button class="hint-btn" id="hbtn2" onclick="useHint(1)">HINT_2 [-50]</button>
                <button class="hint-btn" id="hbtn3" onclick="useHint(2)">HINT_3 [-50]</button>
            </div>
            <div id="hint-out"></div>
            <div id="msg-line"></div>
            <div id="fact-out"></div>
            <div class="bot-btns">
                <button class="b-btn" onclick="backToMap()">[ ABORT MISSION ]</button>
            </div>
        </div>

        <!-- END SCREEN -->
        <div id="endscreen">
            <div id="end-title" class="end-title"></div>
            <div id="end-score" class="end-score"></div>
            <div id="end-stats" class="end-stats"></div>
            <button class="b-btn" onclick="showMissionMap()" style="margin-top:10px">[ MISSION SELECT ]</button>
        </div>

    </div>
</div>

<script>
const MISSIONS=[
    {id:1,code:"RSA_BREACH",name:"The RSA Breach",pts:200,time:90,diff:"EASY",
     obj:"INTEL: A quantum computer just cracked a government server. Identify the vulnerable algorithm.",
     type:"mcq",
     opts:[
         {t:"ML-KEM (Kyber) FIPS 203 — Module-LWE lattice encryption",c:false},
         {t:"RSA-2048 — Large prime factorization encryption [MOST COMMON]",c:true},
         {t:"SLH-DSA SPHINCS+ FIPS 205 — Hash-based signatures",c:false},
         {t:"ML-DSA Dilithium FIPS 204 — Lattice-based signatures",c:false},
     ],
     flag:"FLAG{SH0R_OWNS_RS4}",
     fact:"Shor's Algorithm factors large primes in polynomial time — instantly breaking RSA-2048 which protects 90% of encrypted internet traffic. Migration to Kyber is URGENT.",
     hints:["Which algorithm relies on the difficulty of factoring large prime numbers?","Shor's Algorithm specifically solves integer factorization","RSA = Rivest-Shamir-Adleman — its security IS prime factorization"]},

    {id:2,code:"CAESAR_INTERCEPT",name:"Caesar Intercept",pts:250,time:75,diff:"EASY",
     obj:"DECRYPT: Enemy used ROT13 (Caesar +13). Decode the flag and enter it below.",
     type:"decode",
     encoded:"SYNT{P4RF4E_1F_D34Q}",
     answer:"FLAG{C4ES4R_1S_D34D}",
     flag:"FLAG{C4ES4R_1S_D34D}",
     fact:"Caesar cipher = 25 possible keys. A quantum computer tries all of them in nanoseconds. Kyber has 2^128 possible keys even against quantum — astronomically more secure.",
     hints:["ROT13: shift each LETTER back 13 positions. Numbers and symbols stay the same","A→N, B→O... N→A, O→B. So S→F, Y→L, T→A, N→G","First 4 letters decode to FLAG — continue from there"]},

    {id:3,code:"KYBER_MATH",name:"Kyber Math Core",pts:300,time:80,diff:"EASY",
     obj:"IDENTIFY: What mathematical problem makes ML-KEM (Kyber) resistant to quantum attacks?",
     type:"mcq",
     opts:[
         {t:"Integer Factorization — product of two large primes",c:false},
         {t:"Discrete Logarithm — elliptic curve mathematics",c:false},
         {t:"Module Learning With Errors (M-LWE) — noise in lattice equations",c:true},
         {t:"Subset Sum Problem — NP-complete knapsack variant",c:false},
     ],
     flag:"FLAG{M_LW3_L4TT1C3}",
     fact:"M-LWE: given matrix A and noisy equation b = As + e (s=secret, e=small noise), find s. Even quantum computers using Grover or Shor cannot solve this efficiently — Kyber is safe!",
     hints:["Kyber is a LATTICE-based cryptosystem","LWE = Learning With Errors — finding a secret in noisy linear equations","The key word is 'Module' — it's a structured lattice problem"]},

    {id:4,code:"PRIME_FACTOR",name:"The Prime Trap",pts:400,time:65,diff:"MEDIUM",
     obj:"CRACK IT: Factor this RSA mini-key. Enter both prime factors (p < q). This is child's play vs real RSA — but proves RSA is breakable.",
     type:"factor",
     n:2021, p:43, q:47,
     flag:"FLAG{F4CT0R3D_2021}",
     fact:"2021 = 43 × 47. Real RSA-2048 uses primes with 300+ DIGITS each — classical computers need millions of years. Shor's Algorithm on a quantum computer: seconds. That's the crisis.",
     hints:["Try dividing 2021 by prime numbers: 2, 3, 5, 7, 11, 13... keep going","Try primes in the 40s range","43 is one of the factors — 2021 ÷ 43 = ?"]},

    {id:5,code:"SIG_FORGERY",name:"Signature Forgery",pts:450,time:70,diff:"MEDIUM",
     obj:"CRISIS: Quantum computer forged a software update signature — millions infected. Which NIST standard prevents this?",
     type:"mcq",
     opts:[
         {t:"ECDSA P-384 — Elliptic Curve Digital Signature Algorithm",c:false},
         {t:"RSA-PSS 4096 — Just use bigger RSA keys",c:false},
         {t:"ML-DSA (Dilithium) FIPS 204 — Module Lattice signatures",c:true},
         {t:"HMAC-SHA512 — Keyed hash authentication",c:false},
     ],
     flag:"FLAG{D1L1TH1UM_S1GNS_S4F3}",
     fact:"ML-DSA (Dilithium) FIPS 204 creates unforgeable digital signatures using Module-LWE + Module-SIS lattice hardness. Protects software updates, code signing, TLS certificates — all quantum-safe.",
     hints:["ECDSA is vulnerable to Shor's Algorithm — wrong","Bigger RSA keys only delay the inevitable — Shor breaks any RSA","Look for the NIST PQC signature standard with a FIPS number"]},

    {id:6,code:"HASH_FORTRESS",name:"Hash Fortress",pts:500,time:65,diff:"MEDIUM",
     obj:"ANALYZE: SPHINCS+ uses SHA-3 hash functions. Grover's Algorithm gives quantum computers a speedup. Why is SHA-3 still quantum-safe enough for SPHINCS+?",
     type:"mcq",
     opts:[
         {t:"SHA-3 is completely immune to quantum attacks — Grover has no effect",c:false},
         {t:"Grover halves security bits — SHA3-256 becomes 128-bit — still infeasible to break",c:true},
         {t:"SHA-3 uses prime factorization internally making it quantum-safe",c:false},
         {t:"Grover's Algorithm doesn't work on hash functions at all",c:false},
     ],
     flag:"FLAG{GR0V3R_H4LV3S_B1TS}",
     fact:"Grover's Algorithm gives quadratic speedup: SHA3-256 goes from 2^256 to 2^128 security. 2^128 operations is still astronomically infeasible — even for quantum computers. That's why SPHINCS+ remains safe!",
     hints:["Grover gives a QUADRATIC speedup — square root of the search space","SHA3-256 has 256-bit security classically. What does halving that give?","2^128 is still ~340 undecillion operations — impossible even for quantum computers"]},

    {id:7,code:"FALCON_NTRU",name:"Falcon Files",pts:550,time:60,diff:"MEDIUM",
     obj:"CLASSIFY: IoT devices need tiny signatures. Which NIST PQC standard produces the SMALLEST signatures and what lattice type does it use?",
     type:"mcq",
     opts:[
         {t:"ML-KEM FIPS 203 — Module-LWE (not a signature scheme)",c:false},
         {t:"SLH-DSA SPHINCS+ FIPS 205 — hash-based (largest signatures)",c:false},
         {t:"FN-DSA Falcon FIPS 206 — NTRU lattice (smallest signatures)",c:true},
         {t:"ML-DSA Dilithium FIPS 204 — medium signatures",c:false},
     ],
     flag:"FLAG{F4LC0N_NTRU_T1NY}",
     fact:"Falcon (FN-DSA FIPS 206) uses NTRU lattices — producing signatures 3x smaller than Dilithium. Critical for IoT sensors, smart cards, and embedded systems where storage is measured in kilobytes!",
     hints:["SPHINCS+ has the LARGEST signatures of all four — eliminate it","ML-KEM is a key EXCHANGE scheme, not signatures — eliminate it","FN-DSA = Falcon, uses a specific lattice type called NTRU"]},

    {id:8,code:"NIST_TIMELINE",name:"NIST Timeline",pts:650,time:55,diff:"HARD",
     obj:"INTEL BRIEF: Your handler needs the exact date NIST finalized the PQC standards and the law requiring US agency migration. Enter the year FIPS 203/204/205/206 were finalized:",
     type:"typed",
     answer:"2024",
     flag:"FLAG{N1ST_2024_F1PS}",
     fact:"NIST finalized FIPS 203 (Kyber), 204 (Dilithium), 205 (SPHINCS+), and 206 (Falcon) in AUGUST 2024. National Security Memorandum 10 (NSM-10) requires ALL US federal agencies to migrate by 2035.",
     hints:["This happened very recently — after the year 2023","Think about when these standards were in the news as 'finalized'","The year these 4 FIPS standards were published as final (not draft)"]},

    {id:9,code:"HARVEST_NOW",name:"Harvest Now Decrypt Later",pts:700,time:55,diff:"HARD",
     obj:"THREAT ASSESSMENT: Enemy agents are ALREADY stealing encrypted traffic. They can't decrypt it yet. What attack are they executing and why is it dangerous TODAY?",
     type:"mcq",
     opts:[
         {t:"Zero-day exploit — attacking unpatched software vulnerabilities",c:false},
         {t:"Harvest Now Decrypt Later — storing ciphertext to decrypt when QC arrives",c:true},
         {t:"Man-in-the-Middle — real-time traffic interception and modification",c:false},
         {t:"SQL Injection — database exfiltration through web vulnerabilities",c:false},
     ],
     flag:"FLAG{H4RV3ST_N0W_D3CR1PT}",
     fact:"HNDL is happening RIGHT NOW. Nation-states are archiving encrypted government communications, medical records, and financial data — waiting for quantum computers. Data encrypted TODAY with RSA will be readable in 5-10 years. Migrate to Kyber NOW.",
     hints:["The attack has two phases — one now, one in the future","Think about data being collected TODAY for future use","The attack name literally describes both phases: collect now, decrypt when quantum computers exist"]},

    {id:10,code:"LWE_LAB",name:"The LWE Lab",pts:800,time:50,diff:"HARD",
     obj:"MATH CHALLENGE: Solve this baby LWE equation. In Kyber: secret s=7, modulus q=17. Calculate: (5 × s + noise) mod q where noise=2. Enter the result:",
     type:"typed",
     answer:"2",
     flag:"FLAG{LW3_M4TH_3XP3RT}",
     fact:"(5×7+2) mod 17 = 37 mod 17 = 3... wait: 5×7=35, 35+2=37, 37÷17=2 rem 3. Kyber uses vectors of THOUSANDS of these with unknown noise — even quantum computers can't find 's'. That's post-quantum security!",
     hints:["Step 1: Calculate 5 × 7","Step 2: Add the noise value 2","Step 3: Take mod 17 (remainder when divided by 17). 35+2=37, 37=2×17+3, so answer is 3"],
     answer:"3"},

    {id:11,code:"TLS_HYBRID",name:"TLS 1.3 + Kyber",pts:900,time:45,diff:"HARD",
     obj:"NETWORK INTEL: You intercepted a quantum-safe TLS 1.3 handshake. Chrome and Cloudflare deployed a HYBRID post-quantum key exchange. What combination?",
     type:"mcq",
     opts:[
         {t:"RSA-4096 + ML-DSA Dilithium — hybrid signature scheme",c:false},
         {t:"X25519 + ML-KEM-768 Kyber — hybrid key encapsulation",c:true},
         {t:"ECDH-P521 + FN-DSA Falcon — hybrid key exchange",c:false},
         {t:"DH-8192 + SLH-DSA SPHINCS+ — hash-hybrid approach",c:false},
     ],
     flag:"FLAG{X25519_KYBER_TLS13}",
     fact:"Google Chrome shipped X25519+Kyber (now ML-KEM-768) hybrid TLS in 2023. Combining classical X25519 with Kyber means: secure against classical AND quantum attacks simultaneously during the migration period. Cloudflare serves 20% of the internet with this!",
     hints:["Google Chrome already has this in production — not experimental","Kyber (ML-KEM) is specifically designed for KEY ENCAPSULATION in TLS","X25519 is a modern elliptic curve key exchange — combined with Kyber for hybrid security"]},

    {id:12,code:"FINAL_BOSS",name:"FINAL: Quantum Boss",pts:2000,time:40,diff:"BOSS",
     obj:"🚨 CRQC DETECTED — CRYPTOGRAPHICALLY RELEVANT QUANTUM COMPUTER ONLINE 🚨\nChoose the COMPLETE NIST PQC stack protecting: key exchange + digital signatures + hash backup:",
     type:"mcq",
     opts:[
         {t:"RSA-8192 + ECDSA-521 + SHA-512 — scaled up classical cryptography",c:false},
         {t:"ML-KEM FIPS203 + ML-DSA FIPS204 + SLH-DSA FIPS205 — full PQC stack",c:true},
         {t:"ML-KEM FIPS203 only — Kyber handles all cryptographic needs",c:false},
         {t:"FN-DSA FIPS206 + SHA3-512 — Falcon signatures and hashing only",c:false},
     ],
     flag:"FLAG{C0MPL3T3_PQC_ST4CK}",
     fact:"The complete NIST PQC stack: ML-KEM (Kyber/FIPS203) for key exchange, ML-DSA (Dilithium/FIPS204) for signatures, SLH-DSA (SPHINCS+/FIPS205) as hash-based backup. Together = full quantum-safe internet. You just saved the world.",
     hints:["You need THREE things: key exchange + signatures + hash-based backup","ML-KEM=key exchange. ML-DSA=signatures. SLH-DSA=hash backup","All three have FIPS numbers: 203, 204, 205. Combine them."]},
];

const RANKS=["RECRUIT","CADET","ANALYST","SPECIALIST","AGENT","SR.AGENT",
    "CRYPTOGRAPHER","PQC_EXPERT","GUARDIAN","NIST_SCHOLAR","PQC_CHAMPION","QUANTUM_MASTER"];

let score=0,flags=0,hintsLeft=3;
let status=Array(12).fill("locked");
let cur=null,timer=null,timeLeft=0,hintUsed=[false,false,false],factTmo=null;
status[0]="open";

// BOOT SEQUENCE
const BOOT=[
    "INITIALIZING QUANTUMVAULT SECURE TERMINAL v4.2.1...",
    "LOADING POST-QUANTUM CRYPTOGRAPHY MODULE...",
    "FIPS 203 (ML-KEM/KYBER).............. OK",
    "FIPS 204 (ML-DSA/DILITHIUM).......... OK",
    "FIPS 205 (SLH-DSA/SPHINCS+).......... OK",
    "FIPS 206 (FN-DSA/FALCON)............. OK",
    "THREAT DATABASE LOADING...",
    "SHOR ALGORITHM SIGNATURES............ DETECTED",
    "GROVER SPEEDUP PATTERNS.............. DETECTED",
    "HARVEST-NOW-DECRYPT-LATER ATTACKS.... ACTIVE",
    "ESTABLISHING SECURE CHANNEL...",
    "AGENT CIPHER AUTHENTICATION.......... PENDING",
    "MISSION BRIEFING READY.",
];

function boot(){
    const bl=document.getElementById("boot-lines");
    const bf=document.getElementById("boot-fill");
    const bs=document.getElementById("boot-status");
    let i=0;
    function nextLine(){
        if(i<BOOT.length){
            const d=document.createElement("div");
            d.className="boot-line";
            d.textContent="> "+BOOT[i];
            bl.appendChild(d);
            setTimeout(()=>d.classList.add("show"),50);
            bf.style.width=((i+1)/BOOT.length*100)+"%";
            i++;
            bl.scrollTop=bl.scrollHeight;
            setTimeout(nextLine, i<8?120:i<11?80:200);
        } else {
            bs.textContent="// SYSTEM READY — AUTHENTICATION REQUIRED //";
            document.getElementById("start-wrap").style.display="block";
        }
    }
    nextLine();
}

function showMissionMap(){
    document.getElementById("boot").style.display="none";
    document.getElementById("active-mission").style.display="none";
    document.getElementById("endscreen").style.display="none";
    document.getElementById("mission-map").style.display="block";
    buildMap();
}

function buildMap(){
    const ml=document.getElementById("mission-list");
    ml.innerHTML="";
    MISSIONS.forEach((m,i)=>{
        const s=status[i];
        const div=document.createElement("div");
        div.className="mission-item"+(s==="locked"?" locked":s==="done"?" done":"");
        const diffColors={EASY:"#00ff41",MEDIUM:"#ffff00",HARD:"#ff8800",BOSS:"#ff0040"};
        div.innerHTML=`
            <div class="m-num ${s==="done"?"done":s==="locked"?"locked":""}">${String(m.id).padStart(2,"0")}</div>
            <div class="m-info">
                <div class="m-name" style="color:${s==="locked"?"#333":diffColors[m.diff]||"#00ff41"}">${m.code}</div>
                <div class="m-desc">${m.name} — ${m.diff}</div>
            </div>
            <div class="m-pts">${m.pts}pts</div>
            <div class="m-status">${s==="done"?"✓":s==="locked"?"🔒":"▶"}</div>`;
        if(s!=="locked") div.onclick=()=>startMission(i);
        ml.appendChild(div);
    });
}

function startMission(idx){
    cur=idx;
    const m=MISSIONS[idx];
    hintUsed=[false,false,false];
    document.getElementById("mission-map").style.display="none";
    document.getElementById("active-mission").style.display="block";
    document.getElementById("hint-out").style.display="none";
    document.getElementById("fact-out").style.display="none";
    document.getElementById("msg-line").textContent="";
    document.getElementById("m-codename").textContent=
        "MISSION "+String(m.id).padStart(2,"0")+" // "+m.code;
    document.getElementById("m-obj").textContent=m.obj;
    ["hbtn1","hbtn2","hbtn3"].forEach((id,i)=>{
        const b=document.getElementById(id);
        b.classList.remove("used");
        b.textContent="HINT_"+(i+1)+" [-50]";
    });
    buildChallenge(m);
    startTimer(m.time);
}

function buildChallenge(m){
    const area=document.getElementById("challenge-content");
    let html="";
    if(m.type==="mcq"||m.type==="final"){
        html+=`<div class="options">`;
        const keys=["A","B","C","D"];
        m.opts.forEach((o,i)=>{
            html+=`<div class="opt" id="opt${i}" onclick="pickOpt(${i})">
                <span class="opt-key">[${keys[i]}]</span><span>${o.t}</span></div>`;
        });
        html+=`</div>`;
    } else if(m.type==="decode"){
        html+=`<div class="code-terminal">${m.encoded}</div>`;
        html+=`<div class="terminal-input-wrap">
            <span class="prompt">DECODED_FLAG > </span>
            <input class="terminal-input" id="decode-in" placeholder="FLAG{...}"
                onkeydown="if(event.key==='Enter')checkDecode()"/>
            <button class="exec-btn" onclick="checkDecode()">EXEC</button>
        </div>`;
    } else if(m.type==="factor"){
        html+=`<div class="factor-display">${m.n}</div>`;
        html+=`<div style="font-size:9px;color:#00ff4150;text-align:center;margin-bottom:8px">FACTOR: ${m.n} = p × q (both prime, p &lt; q)</div>`;
        html+=`<div class="factor-inputs">
            <input class="factor-in" id="fp" type="number" placeholder="p"/>
            <span class="x-sign">×</span>
            <input class="factor-in" id="fq" type="number" placeholder="q"/>
            <button class="exec-btn" onclick="checkFactor()" style="margin-left:8px">CRACK</button>
        </div>`;
    } else if(m.type==="typed"){
        html+=`<div class="challenge-box">${m.obj}</div>`;
        html+=`<div class="terminal-input-wrap">
            <span class="prompt">ANSWER > </span>
            <input class="terminal-input" id="typed-in" placeholder="Enter answer..."
                onkeydown="if(event.key==='Enter')checkTyped()"/>
            <button class="exec-btn" onclick="checkTyped()">EXEC</button>
        </div>`;
    }
    area.innerHTML=html;
}

function pickOpt(i){
    const m=MISSIONS[cur];
    document.querySelectorAll(".opt").forEach(o=>{o.onclick=null;o.style.cursor="default";});
    if(m.opts[i].c){
        document.getElementById("opt"+i).classList.add("correct");
        setTimeout(()=>captureFlag(m),400);
    } else {
        document.getElementById("opt"+i).classList.add("wrong");
        m.opts.forEach((o,j)=>{if(o.c)document.getElementById("opt"+j).classList.add("correct");});
        setTimeout(()=>missionFail(m),800);
    }
}

function checkDecode(){
    const m=MISSIONS[cur];
    const v=document.getElementById("decode-in").value.trim().toUpperCase().replace(/\\s/g,"");
    if(v===m.answer){captureFlag(m);}
    else{setMsg("// DECRYPTION FAILED — CHECK YOUR ROT13 //","#ff0040");score=Math.max(0,score-20);updateHUD();}
}

function checkFactor(){
    const m=MISSIONS[cur];
    const p=parseInt(document.getElementById("fp").value)||0;
    const q=parseInt(document.getElementById("fq").value)||0;
    if((p===m.p&&q===m.q)||(p===m.q&&q===m.p)){captureFlag(m);}
    else if(p*q===m.n){setMsg("// FACTORS CORRECT BUT NOT PRIME — FIND PRIME FACTORS //","#ff8800");}
    else{setMsg("// "+p+"×"+q+"="+(p*q)+" ≠ "+m.n+" — RECALCULATE //","#ff0040");score=Math.max(0,score-20);updateHUD();}
}

function checkTyped(){
    const m=MISSIONS[cur];
    const v=document.getElementById("typed-in").value.trim();
    if(v===m.answer){captureFlag(m);}
    else{setMsg("// INCORRECT — ACCESS DENIED //","#ff0040");score=Math.max(0,score-20);updateHUD();}
}

function captureFlag(m){
    clearInterval(timer);
    const timePts=Math.floor((timeLeft/m.time)*300);
    const hintPen=hintUsed.filter(Boolean).length*50;
    const pts=Math.max(50,m.pts+timePts-hintPen);
    score+=pts;flags++;
    status[cur]="done";
    if(cur+1<12) status[cur+1]="open";
    updateHUD();
    document.getElementById("fo-code").textContent=m.flag;
    document.getElementById("fo-pts").textContent="+"+pts+" PTS (base:"+m.pts+" speed:+"+timePts+" hints:-"+hintPen+")";
    document.getElementById("fo-fact").textContent=m.fact;
    document.getElementById("flag-overlay").classList.add("show");
}

function closeFlagOverlay(){
    document.getElementById("flag-overlay").classList.remove("show");
    if(flags>=12){showEndScreen(true);}
    else{backToMap();}
}

function missionFail(m){
    clearInterval(timer);
    status[cur]="open";
    setMsg("// ACCESS DENIED — WRONG ANSWER — -100 PTS //","#ff0040");
    showFact(m.fact);
    score=Math.max(0,score-100);updateHUD();
}

function backToMap(){
    clearInterval(timer);
    cur=null;
    document.getElementById("active-mission").style.display="none";
    document.getElementById("endscreen").style.display="none";
    document.getElementById("mission-map").style.display="block";
    buildMap();
}

function showEndScreen(win){
    document.getElementById("active-mission").style.display="none";
    document.getElementById("mission-map").style.display="none";
    document.getElementById("endscreen").style.display="block";
    const t=document.getElementById("end-title");
    const s=document.getElementById("end-score");
    const st=document.getElementById("end-stats");
    if(win){
        t.textContent="// OPERATION COMPLETE //";t.style.color="#00ff41";
        s.textContent=score+" PTS";
        st.innerHTML="FLAGS: "+flags+"/12<br>RANK: "+RANKS[Math.min(flags,11)]+"<br>CLASSIFICATION: QUANTUM_MASTER<br><br>You mastered all 4 NIST PQC standards.<br>ML-KEM + ML-DSA + SLH-DSA + FN-DSA = Quantum-Safe Internet.";
    } else {
        t.textContent="// MISSION FAILED //";t.style.color="#ff0040";
        s.textContent=score+" PTS";
        st.innerHTML="FLAGS: "+flags+"/12<br>The quantum attackers broke through.<br>Study the PQC standards and try again.";
    }
}

function startTimer(sec){
    timeLeft=sec;
    clearInterval(timer);
    updateTimer();
    timer=setInterval(()=>{
        timeLeft--;
        updateTimer();
        if(timeLeft<=0){
            clearInterval(timer);
            const m=MISSIONS[cur];
            setMsg("// TIME EXPIRED — MISSION FAILED //","#ff0040");
            showFact(m.fact);
            score=Math.max(0,score-50);
            status[cur]="open";
            updateHUD();
        }
    },1000);
}

function updateTimer(){
    const m=cur!==null?MISSIONS[cur]:null;
    const max=m?m.time:60;
    const pct=timeLeft/max*100;
    document.getElementById("tfill").style.width=pct+"%";
    document.getElementById("tfill").style.background=
        pct>60?"#00ff41":pct>30?"#ffff00":"#ff0040";
    document.getElementById("ttext").textContent=
        "⏱ "+timeLeft+"s"+(timeLeft<10?" — CRITICAL":timeLeft<20?" — HURRY":"");
}

function useHint(i){
    const m=cur!==null?MISSIONS[cur]:null;
    if(!m||hintUsed[i]||hintsLeft<=0) return;
    hintUsed[i]=true;hintsLeft--;
    score=Math.max(0,score-50);
    const ho=document.getElementById("hint-out");
    ho.style.display="block";
    ho.textContent="// HINT "+(i+1)+": "+m.hints[i]+" //";
    document.getElementById("hbtn"+(i+1)).classList.add("used");
    document.getElementById("hbtn"+(i+1)).textContent="HINT_"+(i+1)+" [USED]";
    updateHUD();
}

function updateHUD(){
    document.getElementById("h-score").textContent=score;
    document.getElementById("h-flags").textContent=flags+"/12";
    document.getElementById("h-hints").textContent=hintsLeft;
    document.getElementById("h-rank").textContent=RANKS[Math.min(flags,11)];
}

function setMsg(m,c){
    const el=document.getElementById("msg-line");
    el.textContent=m;el.style.color=c||"#00ff41";
}

function showFact(fact){
    const el=document.getElementById("fact-out");
    el.textContent="// INTEL: "+fact+" //";
    el.style.display="block";
    if(factTmo)clearTimeout(factTmo);
    factTmo=setTimeout(()=>el.style.display="none",8000);
}

// BOOT
boot();
</script>
</body>
</html>
""", height=860)


"""
modules/games.py
────────────────
PQC Mini Games — one per grade level.
All games built with HTML/JS embedded via st.components.v1.html()
"""

import streamlit as st
import streamlit.components.v1 as components
from utils.security import sanitize_input


def render_code_shield():
    """K-5: Code the Shield — UPGRADED 2026 — Fortnite-style shield building with incoming attacks!"""
    import streamlit as st
    import streamlit.components.v1 as components
    from modules.trial import trial_gate
    if not trial_gate("code_shield", "Code the Shield"):
        return
    st.subheader("🛡️ Code the Shield!")
    st.markdown(
        "**Shor Bots are attacking!** Click the right blocks to build your "
        "quantum shield before they break through! No typing — just click!"
    )
    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow:hidden;}
#wrap{max-width:560px;margin:0 auto;padding:10px;}

/* HUD */
.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-bottom:8px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;
    padding:5px 3px;text-align:center;font-size:9px;color:#60a5fa;}
.hb b{display:block;font-size:15px;color:white;}

/* ATTACK METER */
#attack-wrap{background:#071520;border:1px solid #ef444440;border-radius:8px;
    padding:6px 10px;margin-bottom:8px;display:flex;align-items:center;gap:8px;}
#attack-label{font-size:10px;color:#ef4444;white-space:nowrap;}
#attack-bar-bg{flex:1;height:10px;background:#1e293b;border-radius:5px;}
#attack-bar{height:10px;border-radius:5px;
    background:linear-gradient(90deg,#10b981,#fbbf24,#ef4444);
    transition:width 0.2s;width:0%;}
#shor-status{font-size:10px;color:#ef4444;white-space:nowrap;}

/* CHALLENGE BOX */
.challenge-box{background:#071520;border:2px solid #fbbf24;border-radius:12px;
    padding:12px;margin-bottom:8px;text-align:center;}
.ch-emoji{font-size:2.5rem;display:block;margin-bottom:4px;
    animation:float 2s ease-in-out infinite;}
@keyframes float{0%,100%{transform:translateY(0);}50%{transform:translateY(-6px);}}
.ch-title{font-size:14px;font-weight:bold;color:#fbbf24;margin-bottom:3px;}
.ch-desc{font-size:11px;color:#94a3b8;line-height:1.5;}

/* PROGRESS */
.progress-dots{display:flex;gap:5px;justify-content:center;margin-bottom:8px;}
.dot{width:14px;height:14px;border-radius:50%;background:#1e293b;
    border:2px solid #334155;transition:all 0.3s;}
.dot.done{background:#10b981;border-color:#10b981;}
.dot.active{background:#3b82f6;border-color:#60a5fa;
    box-shadow:0 0 8px #3b82f6;}
.dot.fail{background:#ef4444;border-color:#ef4444;}

/* BLOCKS GRID */
#blocks-area{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px;}
.block{padding:12px 8px;border-radius:12px;cursor:pointer;text-align:center;
    font-size:11px;font-weight:bold;transition:all 0.15s;border:3px solid transparent;
    line-height:1.4;position:relative;overflow:hidden;}
.block:hover{transform:scale(1.05);filter:brightness(1.2);}
.block:active{transform:scale(0.95);}
.block.selected{transform:scale(0.95);opacity:0.6;}
.block .b-emoji{font-size:22px;display:block;margin-bottom:4px;}
.block .b-name{font-size:10px;font-weight:bold;}
.block .b-desc{font-size:9px;opacity:0.7;margin-top:2px;}

/* BLOCK COLORS */
.block.blue{background:#1d4ed830;border-color:#3b82f6;color:#93c5fd;}
.block.green{background:#05301530;border-color:#10b981;color:#6ee7b7;}
.block.purple{background:#2e1a4030;border-color:#8b5cf6;color:#c4b5fd;}
.block.yellow{background:#1a1a0030;border-color:#fbbf24;color:#fde68a;}
.block.red{background:#2a000030;border-color:#ef4444;color:#fca5a5;}
.block.orange{background:#1a0a0030;border-color:#f97316;color:#fed7aa;}
.block.correct-flash{animation:correctFlash 0.5s ease;}
.block.wrong-flash{animation:wrongFlash 0.4s ease;}
@keyframes correctFlash{0%,100%{transform:scale(1);}50%{transform:scale(1.15);filter:brightness(1.5);}}
@keyframes wrongFlash{0%,25%,75%,100%{transform:translateX(0);}50%{transform:translateX(-8px);}75%{transform:translateX(8px);}}

/* BUILDER */
#builder-area{background:#071520;border:3px dashed #1d4ed8;border-radius:12px;
    min-height:90px;padding:8px;margin-bottom:8px;position:relative;}
#builder-label{font-size:9px;color:#334155;text-align:center;
    position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
    pointer-events:none;}
.placed{padding:8px 12px;border-radius:8px;margin-bottom:4px;
    font-size:11px;font-weight:bold;display:flex;justify-content:space-between;
    align-items:center;cursor:pointer;animation:slideIn 0.2s ease;}
@keyframes slideIn{from{opacity:0;transform:translateX(-10px);}to{opacity:1;transform:translateX(0);}}
.placed .p-num{font-size:9px;color:#475569;margin-right:6px;min-width:16px;}
.placed .p-x{font-size:14px;opacity:0.4;transition:opacity 0.1s;}
.placed .p-x:hover{opacity:1;}

/* BUTTONS */
.btn-row{display:flex;gap:6px;margin-bottom:6px;}
#run-btn{flex:2;padding:12px;background:linear-gradient(135deg,#1d4ed8,#06b6d4);
    border:none;border-radius:10px;color:white;font-size:14px;font-weight:bold;
    cursor:pointer;transition:all 0.15s;}
#run-btn:hover{filter:brightness(1.15);transform:translateY(-1px);}
#clear-btn{flex:1;padding:12px;background:#334155;border:none;border-radius:10px;
    color:white;font-size:12px;cursor:pointer;transition:all 0.15s;}
#clear-btn:hover{filter:brightness(1.2);}
#next-btn{width:100%;padding:12px;background:linear-gradient(135deg,#059669,#10b981);
    border:none;border-radius:10px;color:white;font-size:14px;font-weight:bold;
    cursor:pointer;display:none;animation:pulse 1s infinite;}
@keyframes pulse{0%,100%{transform:scale(1);}50%{transform:scale(1.02);}}

/* OUTPUT */
#output{background:#051018;border:1px solid #1a3a5a;border-radius:8px;
    padding:10px;font-size:11px;min-height:50px;margin-bottom:6px;
    font-family:'Fira Code',monospace;line-height:1.8;}
.out-ok{color:#10b981;}
.out-err{color:#ef4444;}
.out-comment{color:#475569;}
.out-warn{color:#fbbf24;}

/* MESSAGE */
#msg{font-size:12px;min-height:18px;text-align:center;font-weight:bold;
    padding:4px;margin-bottom:4px;}

/* FACT */
#fact{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);
    border-radius:8px;padding:8px 10px;font-size:10px;color:#93c5fd;
    display:none;line-height:1.5;margin-bottom:6px;}

/* STARS */
#stars{font-size:28px;text-align:center;margin:6px 0;display:none;}

/* SHIELD VISUAL */
#shield-visual{text-align:center;font-size:3rem;margin:4px 0;
    transition:all 0.3s;filter:drop-shadow(0 0 0px transparent);}
#shield-visual.built{filter:drop-shadow(0 0 15px #10b981);}
#shield-visual.broken{filter:drop-shadow(0 0 15px #ef4444);
    animation:shieldBreak 0.5s ease;}
@keyframes shieldBreak{0%{transform:scale(1);}50%{transform:scale(1.3) rotate(15deg);}100%{transform:scale(1) rotate(0deg);}}

/* TOAST */
#toast{position:fixed;top:14px;left:50%;transform:translateX(-50%);
    background:#071520;border:2px solid #10b981;border-radius:10px;
    padding:7px 14px;font-size:11px;color:#10b981;font-weight:bold;
    z-index:100;opacity:0;transition:opacity 0.3s;pointer-events:none;text-align:center;}
#toast.show{opacity:1;}

/* CONFETTI */
.cp{position:fixed;pointer-events:none;z-index:999;width:8px;height:8px;
    border-radius:2px;animation:cf linear forwards;}
@keyframes cf{0%{transform:translateY(-20px) rotate(0deg);opacity:1;}
    100%{transform:translateY(600px) rotate(720deg);opacity:0;}}

/* GAME OVER */
#gameover{display:none;text-align:center;padding:20px;}
#gameover h2{color:#ef4444;font-size:20px;margin-bottom:8px;}
#gameover p{color:#94a3b8;font-size:11px;margin-bottom:12px;}
</style>
</head>
<body>
<div id="wrap">

<!-- HUD -->
<div class="hud">
    <div class="hb">⭐ Score<br><b id="h-score">0</b></div>
    <div class="hb">🏆 Level<br><b id="h-level">1</b>/8</div>
    <div class="hb">🔥 Streak<br><b id="h-streak">0</b></div>
    <div class="hb">❤️ Lives<br><b id="h-lives">3</b></div>
</div>

<!-- ATTACK METER -->
<div id="attack-wrap">
    <span id="attack-label">☠️ Shor Bot:</span>
    <div id="attack-bar-bg"><div id="attack-bar"></div></div>
    <span id="shor-status">Waiting...</span>
</div>

<!-- SHIELD VISUAL -->
<div id="shield-visual">🛡️</div>

<!-- CHALLENGE -->
<div class="challenge-box">
    <span class="ch-emoji" id="ch-emoji">🔐</span>
    <div class="ch-title" id="ch-title">Loading...</div>
    <div class="ch-desc" id="ch-desc">Click START to begin!</div>
</div>

<!-- PROGRESS DOTS -->
<div class="progress-dots" id="progress-dots"></div>

<!-- BLOCKS -->
<div id="blocks-area"></div>

<!-- BUILDER -->
<div id="builder-area">
    <div id="builder-label">Click blocks above to add them here →</div>
    <div id="placed-blocks"></div>
</div>

<!-- BUTTONS -->
<div class="btn-row">
    <button id="run-btn" onclick="runCode()">⚡ BUILD SHIELD!</button>
    <button id="clear-btn" onclick="clearBuilder()">🗑️ Clear</button>
</div>
<button id="next-btn" onclick="nextLevel()">➡️ Next Level!</button>

<!-- OUTPUT -->
<div id="output"><span class="out-comment">// Click blocks to build your shield...</span></div>

<!-- MESSAGE -->
<div id="msg"></div>

<!-- FACT -->
<div id="fact"></div>

<!-- STARS -->
<div id="stars"></div>

<!-- GAME OVER -->
<div id="gameover">
    <h2>💀 Network Compromised!</h2>
    <p id="go-msg">The Shor Bots broke through your defenses!</p>
    <button onclick="resetGame()"
        style="padding:10px 20px;background:#1d4ed8;border:none;border-radius:8px;
        color:white;font-size:13px;font-weight:bold;cursor:pointer;">
        🔄 Try Again!
    </button>
</div>

</div>
<div id="toast"></div>

<script>
// ── LEVELS ───────────────────────────────────────────────────────────────────
const LEVELS = [
    {
        emoji:'🔐', title:'Build a Kyber Shield!',
        desc:'Kyber (ML-KEM FIPS 203) protects key exchange. Click the RIGHT blocks to build it!',
        answer:['INIT_KYBER','SET_PARAMS','GENERATE_KEYS','ACTIVATE'],
        blocks:[
            {id:'INIT_KYBER',   emoji:'⚙️', name:'Initialize Kyber', desc:'Start the ML-KEM algorithm', color:'blue'},
            {id:'SET_PARAMS',   emoji:'📐', name:'Set Parameters',   desc:'Configure security level 3', color:'blue'},
            {id:'GENERATE_KEYS',emoji:'🔑', name:'Generate Keys',    desc:'Create public+private key pair', color:'green'},
            {id:'ACTIVATE',     emoji:'✅', name:'Activate Shield',  desc:'Deploy quantum protection!', color:'green'},
            {id:'USE_RSA',      emoji:'💀', name:'Use RSA Instead',  desc:'Old algorithm — quantum vulnerable!', color:'red'},
            {id:'SKIP_KEYS',    emoji:'⚠️', name:'Skip Key Gen',     desc:'Never skip key generation!', color:'red'},
        ],
        fact:'🔐 ML-KEM (Kyber FIPS 203) protects key exchange using Module-LWE lattice math — impossible for quantum computers to break!',
        time:30, pts:100,
    },
    {
        emoji:'✍️', title:'Sign with Dilithium!',
        desc:'Dilithium (ML-DSA FIPS 204) creates digital signatures. Build the signing process!',
        answer:['LOAD_MESSAGE','HASH_SHA3','SIGN_DILITHIUM','VERIFY'],
        blocks:[
            {id:'LOAD_MESSAGE',    emoji:'📄', name:'Load Message',     desc:'Get the document to sign', color:'blue'},
            {id:'HASH_SHA3',       emoji:'#️⃣', name:'Hash with SHA-3', desc:'Create a message fingerprint', color:'purple'},
            {id:'SIGN_DILITHIUM',  emoji:'✍️', name:'Sign with ML-DSA', desc:'Apply Dilithium signature', color:'blue'},
            {id:'VERIFY',          emoji:'✅', name:'Verify Signature', desc:'Confirm the signature is valid', color:'green'},
            {id:'USE_ECDSA',       emoji:'💀', name:'Use ECDSA',        desc:'Quantum vulnerable — Shor breaks it!', color:'red'},
            {id:'SKIP_HASH',       emoji:'⚠️', name:'Skip Hashing',     desc:'Never skip the hash step!', color:'red'},
        ],
        fact:'✍️ ML-DSA (Dilithium FIPS 204) creates digital signatures that NO quantum computer can forge — protecting software updates and certificates!',
        time:28, pts:150,
    },
    {
        emoji:'🌲', title:'Build SPHINCS+ Backup!',
        desc:'SPHINCS+ is the hash-based backup signature. No lattice math needed — just SHA-3!',
        answer:['INIT_SHA3','BUILD_TREE','SIGN_LEAF','PUBLISH'],
        blocks:[
            {id:'INIT_SHA3',   emoji:'#️⃣', name:'Init SHA-3',      desc:'Start the hash function chain', color:'purple'},
            {id:'BUILD_TREE',  emoji:'🌲', name:'Build Hash Tree', desc:'Create Merkle tree structure', color:'green'},
            {id:'SIGN_LEAF',   emoji:'🍃', name:'Sign Leaf Node',  desc:'Sign at tree leaf position', color:'green'},
            {id:'PUBLISH',     emoji:'📡', name:'Publish Root',    desc:'Share the tree root hash', color:'blue'},
            {id:'USE_RSA2',    emoji:'💀', name:'Use RSA',         desc:'Broken by Shor Algorithm!', color:'red'},
            {id:'WRONG_ORDER', emoji:'⚠️', name:'Publish First',   desc:'Must build tree before publishing!', color:'red'},
        ],
        fact:'🌲 SPHINCS+ (FIPS 205) chains thousands of SHA-3 hashes into a Merkle tree — even if ALL lattice math breaks, SPHINCS+ stays safe!',
        time:28, pts:150,
    },
    {
        emoji:'🦅', title:'Deploy Falcon for IoT!',
        desc:'Falcon uses NTRU lattices and makes the SMALLEST signatures — perfect for tiny devices!',
        answer:['DETECT_DEVICE','LOAD_NTRU','COMPRESS_SIG','DEPLOY'],
        blocks:[
            {id:'DETECT_DEVICE', emoji:'📱', name:'Detect Device',   desc:'Check device memory limits', color:'blue'},
            {id:'LOAD_NTRU',     emoji:'🦅', name:'Load NTRU Lattice',desc:'Use Falcon FN-DSA FIPS 206', color:'yellow'},
            {id:'COMPRESS_SIG',  emoji:'🗜️', name:'Compress Sig',    desc:'Falcon sigs are 3x smaller!', color:'yellow'},
            {id:'DEPLOY',        emoji:'🚀', name:'Deploy to IoT',   desc:'Send to smart device', color:'green'},
            {id:'USE_BIG_SIG',   emoji:'💀', name:'Use SPHINCS+',    desc:'Too large for small devices!', color:'red'},
            {id:'SKIP_CHECK',    emoji:'⚠️', name:'Skip Device Check',desc:'Always check device limits!', color:'red'},
        ],
        fact:'🦅 Falcon (FN-DSA FIPS 206) signatures are ~666 bytes vs Dilithium\'s 3293 bytes — 5x smaller, perfect for IoT sensors and smart cards!',
        time:26, pts:200,
    },
    {
        emoji:'🏰', title:'Secure a TLS Connection!',
        desc:'TLS protects websites. Build a quantum-safe HTTPS connection step by step!',
        answer:['CLIENT_HELLO','KYBER_KEM','DILITHIUM_CERT','ENCRYPTED_DATA'],
        blocks:[
            {id:'CLIENT_HELLO',    emoji:'👋', name:'Client Hello',     desc:'Browser greets the server', color:'blue'},
            {id:'KYBER_KEM',       emoji:'🔐', name:'Kyber Key Exchange',desc:'Share secret using ML-KEM', color:'green'},
            {id:'DILITHIUM_CERT',  emoji:'✍️', name:'Verify Certificate',desc:'Check server identity with ML-DSA', color:'blue'},
            {id:'ENCRYPTED_DATA',  emoji:'🔒', name:'Send Encrypted Data',desc:'Data protected by shared secret!', color:'green'},
            {id:'USE_RSA_TLS',     emoji:'💀', name:'Use RSA for TLS',  desc:'Quantum vulnerable key exchange!', color:'red'},
            {id:'SKIP_CERT',       emoji:'⚠️', name:'Skip Certificate', desc:'Never skip identity verification!', color:'red'},
        ],
        fact:'🌐 Google Chrome + Cloudflare already use Kyber (ML-KEM) in TLS — protecting 20% of all internet traffic from future quantum attacks!',
        time:24, pts:200,
    },
    {
        emoji:'💾', title:'Protect a Database!',
        desc:'Databases store sensitive data. Encrypt them with the right PQC algorithm!',
        answer:['SCAN_DATA','KYBER_ENCRYPT','HASH_RECORDS','BACKUP_KEYS'],
        blocks:[
            {id:'SCAN_DATA',     emoji:'🔍', name:'Scan Database',    desc:'Find sensitive records', color:'blue'},
            {id:'KYBER_ENCRYPT', emoji:'🔐', name:'Encrypt with Kyber',desc:'Apply ML-KEM encryption', color:'green'},
            {id:'HASH_RECORDS',  emoji:'#️⃣', name:'Hash Records',     desc:'Create SHA-3 integrity hashes', color:'purple'},
            {id:'BACKUP_KEYS',   emoji:'💾', name:'Backup Keys Safely',desc:'Store keys in HSM', color:'yellow'},
            {id:'USE_AES128',    emoji:'⚠️', name:'Use AES-128',      desc:'Grover halves security to 64 bits!', color:'red'},
            {id:'NO_BACKUP',     emoji:'💀', name:'Skip Key Backup',  desc:'Lost keys = lost data forever!', color:'red'},
        ],
        fact:'💾 AES-256 stays safe against Grover (128-bit quantum security) but RSA/ECC key exchange must be replaced with Kyber — databases need BOTH!',
        time:22, pts:250,
    },
    {
        emoji:'🚀', title:'Launch a Satellite!',
        desc:'Satellites need quantum-safe crypto that works for 20+ years — long after quantum computers arrive!',
        answer:['GENERATE_LONGTERM','FALCON_SIGN','SPHINCS_BACKUP','LAUNCH'],
        blocks:[
            {id:'GENERATE_LONGTERM',emoji:'🔑', name:'Generate Long-term Keys',desc:'Keys that last 20 years', color:'blue'},
            {id:'FALCON_SIGN',      emoji:'🦅', name:'Sign with Falcon',        desc:'Compact FIPS 206 signatures', color:'yellow'},
            {id:'SPHINCS_BACKUP',   emoji:'🌲', name:'SPHINCS+ Backup Sig',     desc:'Hash-based backup protection', color:'green'},
            {id:'LAUNCH',           emoji:'🚀', name:'Launch Satellite',         desc:'Deploy with full PQC protection!', color:'green'},
            {id:'USE_RSA_SAT',      emoji:'💀', name:'Use RSA for 20 Years',    desc:'Quantum will break this in 5 years!', color:'red'},
            {id:'SKIP_BACKUP',      emoji:'⚠️', name:'Skip SPHINCS+ Backup',   desc:'Always have a backup scheme!', color:'red'},
        ],
        fact:'🚀 Real satellites launched today must survive quantum computers — NASA and ESA are already testing PQC standards for space communications!',
        time:20, pts:300,
    },
    {
        emoji:'🌍', title:'Secure the Internet!',
        desc:'FINAL MISSION: Deploy all 4 NIST PQC standards to protect global infrastructure!',
        answer:['DEPLOY_KYBER','DEPLOY_DILITHIUM','DEPLOY_SPHINCS','DEPLOY_FALCON'],
        blocks:[
            {id:'DEPLOY_KYBER',     emoji:'🔐', name:'Deploy ML-KEM',    desc:'FIPS 203 — Key Exchange', color:'green'},
            {id:'DEPLOY_DILITHIUM', emoji:'✍️', name:'Deploy ML-DSA',    desc:'FIPS 204 — Signatures', color:'blue'},
            {id:'DEPLOY_SPHINCS',   emoji:'🌲', name:'Deploy SLH-DSA',   desc:'FIPS 205 — Hash Backup', color:'purple'},
            {id:'DEPLOY_FALCON',    emoji:'🦅', name:'Deploy FN-DSA',    desc:'FIPS 206 — Compact Sigs', color:'yellow'},
            {id:'KEEP_RSA',         emoji:'💀', name:'Keep RSA',         desc:'Quantum destroys RSA!', color:'red'},
            {id:'PARTIAL_DEPLOY',   emoji:'⚠️', name:'Deploy Only 2',    desc:'Need ALL 4 standards!', color:'red'},
        ],
        fact:'🌍 NIST finalized all 4 PQC standards in August 2024. NSM-10 requires all US federal agencies to migrate by 2035. The quantum-safe internet starts NOW!',
        time:18, pts:500,
    },
];

// ── SHOR BOT TAUNTS ──────────────────────────────────────────────────────────
const TAUNTS = [
    '🤖 "Warming up qubits..."',
    '🤖 "Found your RSA key!"',
    '🤖 "Shor Algorithm active!"',
    '🤖 "Your time is running out!"',
    '🤖 "Almost through your defenses!"',
    '🤖 "QUANTUM SUPREMACY!"',
];

// ── GAME STATE ────────────────────────────────────────────────────────────────
let currentLevel = 0;
let placedBlocks = [];
let score = 0, streak = 0, lives = 3;
let attackPct = 0, attackTimer = null;
let levelDone = false;

// ── INIT ─────────────────────────────────────────────────────────────────────
function initLevel() {
    const lv = LEVELS[currentLevel];
    levelDone = false;
    placedBlocks = [];
    attackPct = 0;

    // Update challenge box
    document.getElementById('ch-emoji').textContent = lv.emoji;
    document.getElementById('ch-title').textContent = lv.title;
    document.getElementById('ch-desc').textContent = lv.desc;
    document.getElementById('h-level').textContent = (currentLevel+1)+'/8';

    // Shield visual
    document.getElementById('shield-visual').textContent = lv.emoji;
    document.getElementById('shield-visual').className = '';

    // Build blocks
    const area = document.getElementById('blocks-area');
    area.innerHTML = '';
    // Shuffle blocks
    const shuffled = [...lv.blocks].sort(() => Math.random()-0.5);
    shuffled.forEach(b => {
        const div = document.createElement('div');
        div.className = 'block '+b.color;
        div.id = 'blk-'+b.id;
        div.innerHTML =
            '<span class="b-emoji">'+b.emoji+'</span>'+
            '<div class="b-name">'+b.name+'</div>'+
            '<div class="b-desc">'+b.desc+'</div>';
        div.onclick = () => addBlock(b, div);
        area.appendChild(div);
    });

    // Clear builder
    clearBuilder();
    document.getElementById('output').innerHTML =
        '<span class="out-comment">// '+lv.desc+'</span>';
    document.getElementById('next-btn').style.display = 'none';
    document.getElementById('run-btn').style.display = 'block';
    document.getElementById('fact').style.display = 'none';
    document.getElementById('stars').style.display = 'none';
    document.getElementById('gameover').style.display = 'none';
    document.getElementById('blocks-area').style.display = 'grid';

    // Build progress dots
    const dots = document.getElementById('progress-dots');
    dots.innerHTML = '';
    LEVELS.forEach((_, i) => {
        const d = document.createElement('div');
        d.className = 'dot'+(i<currentLevel?' done':i===currentLevel?' active':'');
        dots.appendChild(d);
    });

    // Start attack timer
    clearInterval(attackTimer);
    attackPct = 0;
    updateAttack();
    const steps = lv.time * 10;
    let step = 0;
    let tauntIdx = 0;
    attackTimer = setInterval(() => {
        if (levelDone) { clearInterval(attackTimer); return; }
        step++;
        attackPct = Math.min(100, (step/steps)*100);
        updateAttack();
        // Taunts
        if (step % Math.floor(steps/5) === 0) {
            document.getElementById('shor-status').textContent =
                TAUNTS[tauntIdx++ % TAUNTS.length];
        }
        if (attackPct >= 100) {
            clearInterval(attackTimer);
            timeUp();
        }
    }, 100);

    setMsg('🛡️ Click blocks in the RIGHT ORDER to build your shield!', '#60a5fa');
    updateHUD();
}

// ── BLOCK INTERACTION ─────────────────────────────────────────────────────────
function addBlock(block, el) {
    if (levelDone) return;
    placedBlocks.push(block);
    el.classList.add('selected');

    // Add to builder
    const pb = document.getElementById('placed-blocks');
    document.getElementById('builder-label').style.display = 'none';
    const div = document.createElement('div');
    div.className = 'placed';
    div.style.background = el.classList.contains('green')?'#05301530':
                            el.classList.contains('blue')?'#1d4ed830':
                            el.classList.contains('purple')?'#2e1a4030':
                            el.classList.contains('yellow')?'#1a1a0030':
                            el.classList.contains('red')?'#2a000030':'#1e293b';
    div.style.borderLeft = '3px solid '+(
        el.classList.contains('green')?'#10b981':
        el.classList.contains('blue')?'#3b82f6':
        el.classList.contains('purple')?'#8b5cf6':
        el.classList.contains('yellow')?'#fbbf24':'#ef4444');
    div.innerHTML =
        '<span class="p-num">'+placedBlocks.length+'.</span>'+
        '<span>'+block.emoji+' '+block.name+'</span>'+
        '<span class="p-x" onclick="removeBlock('+(placedBlocks.length-1)+')">✕</span>';
    pb.appendChild(div);
    updateHUD();
}

function removeBlock(idx) {
    placedBlocks.splice(idx, 1);
    rebuildPlaced();
}

function rebuildPlaced() {
    const pb = document.getElementById('placed-blocks');
    pb.innerHTML = '';
    if (placedBlocks.length === 0) {
        document.getElementById('builder-label').style.display = 'block';
        // Re-enable all blocks
        document.querySelectorAll('.block').forEach(b => b.classList.remove('selected'));
        return;
    }
    placedBlocks.forEach((block, i) => {
        const div = document.createElement('div');
        div.className = 'placed';
        div.style.borderLeft = '3px solid #3b82f6';
        div.innerHTML =
            '<span class="p-num">'+(i+1)+'.</span>'+
            '<span>'+block.emoji+' '+block.name+'</span>'+
            '<span class="p-x" onclick="removeBlock('+i+')">✕</span>';
        pb.appendChild(div);
    });
}

function clearBuilder() {
    placedBlocks = [];
    document.getElementById('placed-blocks').innerHTML = '';
    document.getElementById('builder-label').style.display = 'block';
    document.querySelectorAll('.block').forEach(b => b.classList.remove('selected'));
    updateHUD();
}

// ── RUN CODE ──────────────────────────────────────────────────────────────────
function runCode() {
    if (levelDone) return;
    const lv = LEVELS[currentLevel];
    const out = document.getElementById('output');
    out.innerHTML = '';

    if (placedBlocks.length === 0) {
        out.innerHTML = '<span class="out-err">ERROR: No blocks selected! Click blocks to build your shield.</span>';
        setMsg('❌ Add some blocks first!', '#ef4444');
        return;
    }

    // Check answer
    const userIds = placedBlocks.map(b => b.id);
    const correct = lv.answer;
    let allCorrect = true;
    let firstError = -1;

    // Output each step
    userIds.forEach((id, i) => {
        const block = lv.blocks.find(b => b.id === id);
        const isCorrect = id === correct[i];
        if (!isCorrect && firstError === -1) firstError = i;
        if (!isCorrect) allCorrect = false;

        const line = document.createElement('div');
        if (isCorrect) {
            line.className = 'out-ok';
            line.textContent = '✅ Step '+(i+1)+': '+block.emoji+' '+block.name+' — CORRECT!';
        } else if (id.includes('RSA')||id.includes('ECDSA')||id.includes('KEEP')||id.includes('USE')) {
            line.className = 'out-err';
            line.textContent = '❌ Step '+(i+1)+': '+block.emoji+' '+block.name+' — QUANTUM VULNERABLE!';
        } else {
            line.className = 'out-warn';
            line.textContent = '⚠️ Step '+(i+1)+': '+block.emoji+' '+block.name+' — Wrong order!';
        }
        out.appendChild(line);
    });

    // Check if all 4 required steps are included
    const hasAll = correct.every(id => userIds.includes(id));

    if (allCorrect && userIds.length === correct.length) {
        // Perfect!
        levelWin(true);
    } else if (hasAll && userIds.length === correct.length) {
        // Right blocks wrong order
        const errLine = document.createElement('div');
        errLine.className = 'out-warn';
        errLine.textContent = '⚠️ Right blocks but wrong order! Try rearranging.';
        out.appendChild(errLine);
        setMsg('⚠️ Right blocks, wrong order! Clear and try again.', '#fbbf24');
        streak = 0; updateHUD();
    } else {
        // Wrong blocks
        const errLine = document.createElement('div');
        errLine.className = 'out-err';
        errLine.textContent = '❌ Shield failed! Check for quantum-vulnerable blocks!';
        out.appendChild(errLine);
        setMsg('❌ Shield failed! Remove the wrong blocks!', '#ef4444');
        // Flash wrong blocks
        placedBlocks.forEach(b => {
            if (!correct.includes(b.id)) {
                const el = document.getElementById('blk-'+b.id);
                if (el) { el.classList.add('wrong-flash'); setTimeout(()=>el.classList.remove('wrong-flash'),400); }
            }
        });
        lives--; updateHUD();
        if (lives <= 0) gameOver();
    }
}

function levelWin(perfect) {
    clearInterval(attackTimer);
    levelDone = true;
    const lv = LEVELS[currentLevel];
    streak++;
    const timeBonus = Math.round((1 - attackPct/100) * 50);
    const streakBonus = streak >= 3 ? 30 : 0;
    const pts = lv.pts + timeBonus + streakBonus;
    score += pts;

    document.getElementById('shield-visual').textContent = '🛡️';
    document.getElementById('shield-visual').className = 'built';
    document.getElementById('stars').textContent = streak>=3?'⭐⭐⭐':'⭐⭐';
    document.getElementById('stars').style.display = 'block';

    showFact(lv.fact);
    setMsg('🎉 SHIELD BUILT! +'+pts+' pts'+(streakBonus?' (Streak Bonus!)':''), '#10b981');
    document.getElementById('next-btn').style.display = 'block';
    document.getElementById('run-btn').style.display = 'none';
    document.getElementById('shor-status').textContent = '🤖 "BLOCKED! Retreat!"';
    updateAttack(0);
    updateHUD();
    showToast('🛡️ Shield Built! +'+pts+' pts!');
    if (streak >= 3) confetti();

    // Add success line to output
    const out = document.getElementById('output');
    const line = document.createElement('div');
    line.className = 'out-ok';
    line.textContent = '🛡️ SHIELD ACTIVATED! Shor Bot blocked!';
    out.appendChild(line);
}

function timeUp() {
    if (levelDone) return;
    levelDone = true;
    lives--;
    document.getElementById('shield-visual').className = 'broken';
    document.getElementById('shor-status').textContent = '🤖 "BREACHED! RSA is mine!"';
    setMsg('💀 Too slow! Shor Bot broke through!', '#ef4444');
    streak = 0; updateHUD();
    if (lives <= 0) { setTimeout(gameOver, 1000); return; }
    setTimeout(()=>{
        document.getElementById('next-btn').style.display = 'block';
        document.getElementById('next-btn').textContent = '➡️ Try Next Level';
        document.getElementById('run-btn').style.display = 'none';
    }, 1000);
}

function nextLevel() {
    currentLevel++;
    if (currentLevel >= LEVELS.length) {
        // Victory!
        document.getElementById('blocks-area').style.display = 'none';
        document.getElementById('builder-area').style.display = 'none';
        document.getElementById('btn-row').style.display = 'none';
        document.getElementById('next-btn').style.display = 'none';
        document.getElementById('output').innerHTML =
            '<span class="out-ok">🌍 ALL 4 NIST PQC STANDARDS DEPLOYED!</span><br>'+
            '<span class="out-ok">🏆 Final Score: '+score+'</span><br>'+
            '<span class="out-ok">🎉 The internet is quantum-safe!</span>';
        setMsg('👑 QUANTUM CHAMPION! You protected the internet!', '#fbbf24');
        confetti();
        showToast('👑 All 8 levels complete! Score: '+score);
        return;
    }
    initLevel();
}

function gameOver() {
    clearInterval(attackTimer);
    document.getElementById('gameover').style.display = 'block';
    document.getElementById('go-msg').textContent =
        'Score: '+score+' | Streak: '+streak+' | Level: '+(currentLevel+1)+'/8';
    setMsg('', '');
}

function resetGame() {
    currentLevel = 0; score = 0; streak = 0; lives = 3;
    document.getElementById('gameover').style.display = 'none';
    document.getElementById('builder-area').style.display = 'block';
    document.getElementById('blocks-area').style.display = 'grid';
    document.getElementById('run-btn').style.display = 'block';
    initLevel();
}

// ── UI HELPERS ────────────────────────────────────────────────────────────────
function updateHUD() {
    document.getElementById('h-score').textContent = score;
    document.getElementById('h-streak').textContent = streak;
    document.getElementById('h-lives').textContent = '❤️'.repeat(Math.max(0,lives));
}

function updateAttack(pct) {
    const p = pct !== undefined ? pct : attackPct;
    document.getElementById('attack-bar').style.width = p+'%';
}

function setMsg(m, c) {
    const el = document.getElementById('msg');
    el.textContent = m;
    el.style.color = c || '#60a5fa';
}

let factTimer = null;
function showFact(t) {
    const el = document.getElementById('fact');
    el.textContent = t; el.style.display = 'block';
    if (factTimer) clearTimeout(factTimer);
    factTimer = setTimeout(() => el.style.display='none', 7000);
}

let toastTimer = null;
function showToast(m) {
    const el = document.getElementById('toast');
    el.textContent = m; el.classList.add('show');
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('show'), 2500);
}

function confetti() {
    const colors = ['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444','#f97316'];
    for (let i=0; i<20; i++) {
        setTimeout(() => {
            const el = document.createElement('div');
            el.className = 'cp';
            el.style.left = Math.random()*100+'vw';
            el.style.background = colors[Math.floor(Math.random()*colors.length)];
            el.style.animationDuration = (1+Math.random()*2)+'s';
            document.body.appendChild(el);
            setTimeout(() => el.remove(), 3000);
        }, i*50);
    }
}

// ── START ─────────────────────────────────────────────────────────────────────
initLevel();
</script>
</body>
</html>
""", height=820)

def render_cipher_quest():
    """Middle School 6-8: Cipher Quest — UPGRADED 2026 — RPG quest map, coins, shop, boss fights."""
    import streamlit as st
    import streamlit.components.v1 as components
    from modules.trial import trial_gate
    if not trial_gate("cipher_quest", "Cipher Quest"):
        return
    st.subheader("🎮 Cipher Quest!")
    st.markdown(
        "**You are a Quantum Spy!** Complete cipher missions to earn coins, "
        "unlock power-ups, and defeat the Shor Boss! Fill in ONE blank per challenge."
    )
    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow-x:hidden;}
#wrap{max-width:560px;margin:0 auto;padding:10px;}

/* HUD */
.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-bottom:8px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;
    padding:5px 3px;text-align:center;font-size:9px;color:#60a5fa;}
.hb b{display:block;font-size:14px;color:white;}

/* RANK BAR */
#rank-bar{background:#071520;border:1px solid #fbbf2440;border-radius:10px;
    padding:5px 12px;margin-bottom:8px;display:flex;align-items:center;gap:8px;}
#rank-name{font-size:11px;color:#fbbf24;font-weight:bold;white-space:nowrap;}
#rank-xp-bar{flex:1;height:6px;background:#1e293b;border-radius:3px;}
#rank-xp-fill{height:6px;background:linear-gradient(90deg,#fbbf24,#f97316);
    border-radius:3px;transition:width 0.5s;width:0%;}
#rank-next{font-size:9px;color:#475569;white-space:nowrap;}

/* TABS */
.tabs{display:flex;gap:3px;margin-bottom:8px;}
.tab{flex:1;padding:7px 4px;border-radius:8px;border:1px solid #1a3a5a;
    background:#071520;color:#60a5fa;font-size:11px;font-weight:bold;
    cursor:pointer;text-align:center;transition:all 0.15s;}
.tab.active{background:#1d4ed8;border-color:#3b82f6;color:white;}

/* QUEST MAP */
#quest-map{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px;}
.quest-node{background:#071520;border:2px solid #1a3a5a;border-radius:12px;
    padding:10px;cursor:pointer;transition:all 0.15s;text-align:center;
    position:relative;}
.quest-node:hover:not(.locked){border-color:#3b82f6;background:#0a1f35;}
.quest-node.active{border-color:#fbbf24;background:#1a1500;}
.quest-node.done{border-color:#10b981;background:#051a0f;}
.quest-node.locked{opacity:0.35;cursor:not-allowed;}
.quest-node.boss{border-color:#ef4444;background:#1a0505;}
.quest-node .qn-emoji{font-size:1.8rem;display:block;margin-bottom:3px;}
.quest-node .qn-title{font-size:10px;font-weight:bold;color:#60a5fa;}
.quest-node .qn-coins{font-size:9px;color:#fbbf24;margin-top:2px;}
.quest-node .qn-badge{position:absolute;top:4px;right:4px;font-size:9px;
    padding:1px 5px;border-radius:6px;font-weight:bold;}
.badge-easy{background:#059669;color:white;}
.badge-med{background:#d97706;color:white;}
.badge-hard{background:#dc2626;color:white;}
.badge-boss{background:linear-gradient(135deg,#dc2626,#7c3aed);color:white;}
.badge-done{background:#10b981;color:white;}

/* QUEST CARD */
.quest-card{background:#071520;border:2px solid #1d4ed8;border-radius:14px;
    padding:12px;margin-bottom:8px;}
.quest-header{display:flex;align-items:center;gap:8px;margin-bottom:8px;}
.quest-emoji-big{font-size:2rem;}
.quest-title-wrap{flex:1;}
.quest-title-text{font-size:13px;font-weight:bold;color:#60a5fa;}
.quest-subtitle{font-size:9px;color:#475569;margin-top:2px;}
.quest-desc{font-size:11px;color:#94a3b8;line-height:1.6;margin-bottom:8px;
    background:#050e1a;border-radius:8px;padding:8px;}

/* CODE BLOCK */
.code-block{background:#020d14;border:1px solid #1a3a5a;border-radius:8px;
    padding:10px;font-family:'Fira Code',monospace;font-size:11px;
    line-height:2.2;margin-bottom:8px;}
.code-line{display:block;color:#60a5fa;}
.code-comment{display:block;color:#475569;font-style:italic;}
.code-keyword{color:#a78bfa;}
.blank{background:#0a1f35;border:2px solid #3b82f6;border-radius:6px;
    color:#10b981;font-family:'Fira Code',monospace;font-size:12px;
    padding:3px 8px;width:130px;outline:none;text-align:center;
    transition:border-color 0.2s;}
.blank:focus{border-color:#60a5fa;box-shadow:0 0 8px rgba(59,130,246,0.3);}
.blank.correct{border-color:#10b981;background:#051a0f;}
.blank.wrong{border-color:#ef4444;animation:shake 0.4s ease;}
@keyframes shake{0%,100%{transform:translateX(0);}25%{transform:translateX(-5px);}75%{transform:translateX(5px);}}

/* BUTTONS */
.btn-row{display:flex;gap:5px;margin-bottom:6px;}
.btn{flex:1;padding:10px;border:none;border-radius:8px;color:white;
    font-size:12px;font-weight:bold;cursor:pointer;transition:all 0.15s;}
.btn:hover{filter:brightness(1.15);transform:translateY(-1px);}
.btn-run{background:linear-gradient(135deg,#1d4ed8,#06b6d4);}
.btn-hint{background:#7c3aed;}
.btn-next{width:100%;padding:12px;background:linear-gradient(135deg,#059669,#10b981);
    border:none;border-radius:10px;color:white;font-size:14px;font-weight:bold;
    cursor:pointer;display:none;animation:pulse 1s infinite;}
@keyframes pulse{0%,100%{transform:scale(1);}50%{transform:scale(1.02);}}

/* OUTPUT */
.output{background:#020d14;border:2px solid #00ff4130;border-radius:8px;
    padding:10px;font-family:'Fira Code',monospace;font-size:11px;
    color:#00ff41;min-height:44px;margin-bottom:6px;line-height:1.8;}

/* SHOP */
#shop-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px;}
.shop-item{background:#071520;border:1px solid #1a3a5a;border-radius:10px;
    padding:10px;text-align:center;cursor:pointer;transition:all 0.15s;}
.shop-item:hover{border-color:#fbbf24;background:#1a1500;}
.shop-item.owned{border-color:#10b981;background:#051a0f;}
.shop-item .si-emoji{font-size:1.8rem;display:block;margin-bottom:4px;}
.shop-item .si-name{font-size:11px;font-weight:bold;color:white;}
.shop-item .si-desc{font-size:9px;color:#94a3b8;margin-top:2px;line-height:1.4;}
.shop-item .si-cost{font-size:11px;color:#fbbf24;font-weight:bold;margin-top:4px;}
.shop-item.owned .si-cost{color:#10b981;}

/* BOSS FIGHT */
#boss-fight{background:#1a0505;border:2px solid #ef4444;border-radius:14px;
    padding:12px;margin-bottom:8px;display:none;}
#boss-fight h3{color:#ef4444;font-size:13px;margin-bottom:8px;text-align:center;}
#boss-hp-bar{height:12px;background:#1e293b;border-radius:6px;overflow:hidden;margin-bottom:8px;}
#boss-hp-fill{height:12px;background:linear-gradient(90deg,#dc2626,#ef4444);
    border-radius:6px;transition:width 0.5s;width:100%;}
.boss-emoji{text-align:center;font-size:3rem;display:block;margin-bottom:6px;
    animation:bossFloat 2s ease-in-out infinite;}
@keyframes bossFloat{0%,100%{transform:translateY(0);}50%{transform:translateY(-8px);}}

/* MSG + FACT */
#msg{font-size:11px;min-height:16px;text-align:center;font-weight:bold;padding:4px;margin-bottom:4px;}
#fact{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);
    border-radius:8px;padding:8px 10px;font-size:10px;color:#93c5fd;
    display:none;line-height:1.5;margin-bottom:6px;}

/* TOAST */
#toast{position:fixed;top:14px;left:50%;transform:translateX(-50%);
    background:#071520;border:2px solid #fbbf24;border-radius:10px;
    padding:7px 14px;font-size:11px;color:#fbbf24;font-weight:bold;
    z-index:100;opacity:0;transition:opacity 0.3s;pointer-events:none;text-align:center;}
#toast.show{opacity:1;}

/* CONFETTI */
.cp{position:fixed;pointer-events:none;z-index:999;width:8px;height:8px;
    border-radius:2px;animation:cf linear forwards;}
@keyframes cf{0%{transform:translateY(-20px) rotate(0deg);opacity:1;}
    100%{transform:translateY(600px) rotate(720deg);opacity:0;}}
</style>
</head>
<body>
<div id="wrap">

<!-- HUD -->
<div class="hud">
    <div class="hb">🪙 Coins<br><b id="h-coins">0</b></div>
    <div class="hb">⭐ XP<br><b id="h-xp">0</b></div>
    <div class="hb">🔥 Streak<br><b id="h-streak">0</b></div>
    <div class="hb">✅ Done<br><b id="h-done">0</b>/8</div>
</div>

<!-- RANK BAR -->
<div id="rank-bar">
    <span id="rank-name">🔰 Rookie Spy</span>
    <div id="rank-xp-bar"><div id="rank-xp-fill"></div></div>
    <span id="rank-next">0/100 XP</span>
</div>

<!-- TABS -->
<div class="tabs">
    <div class="tab active" onclick="showTab('map')">🗺️ Quest Map</div>
    <div class="tab" onclick="showTab('active')">🎯 Mission</div>
    <div class="tab" onclick="showTab('shop')">🛒 Shop</div>
</div>

<div id="msg"></div>

<!-- QUEST MAP TAB -->
<div id="tab-map">
    <div id="quest-map"></div>
</div>

<!-- ACTIVE QUEST TAB -->
<div id="tab-active" style="display:none">
    <!-- BOSS FIGHT -->
    <div id="boss-fight">
        <h3>💀 BOSS BATTLE — The Shor Machine!</h3>
        <span class="boss-emoji">🤖</span>
        <div id="boss-hp-bar"><div id="boss-hp-fill"></div></div>
        <div style="font-size:10px;color:#ef4444;text-align:center;margin-bottom:8px"
             id="boss-status">Shor Machine HP: 100%</div>
    </div>

    <div class="quest-card" id="quest-area">
        <div class="quest-header">
            <span class="quest-emoji-big" id="q-emoji">🎯</span>
            <div class="quest-title-wrap">
                <div class="quest-title-text" id="q-title">Select a quest!</div>
                <div class="quest-subtitle" id="q-subtitle"></div>
            </div>
        </div>
        <div class="quest-desc" id="q-desc">Click a quest on the map to begin!</div>
        <div class="code-block" id="q-code"></div>
        <div class="btn-row">
            <button class="btn btn-run" onclick="runQuest()">⚡ Run Code</button>
            <button class="btn btn-hint" onclick="useHint()">💡 Hint (-5 coins)</button>
        </div>
        <button class="btn-next" id="next-btn" onclick="nextQuest()">➡️ Next Quest!</button>
        <div class="output" id="q-output">// Output will appear here...</div>
    </div>

    <div id="fact"></div>
</div>

<!-- SHOP TAB -->
<div id="tab-shop" style="display:none">
    <div style="text-align:center;font-size:12px;color:#94a3b8;margin-bottom:8px;">
        Spend your coins on power-ups to help complete missions!
    </div>
    <div id="shop-grid"></div>
</div>

</div>
<div id="toast"></div>

<script>
// ── QUESTS ───────────────────────────────────────────────────────────────────
const QUESTS = [
    {
        id:0, emoji:'🔐', title:'Kyber Key Exchange',
        subtitle:'EASY — Fill in the algorithm name',
        desc:'ML-KEM (Kyber) is the NIST FIPS 203 standard for key exchange. It replaces RSA by using lattice math. Complete the code to set up a Kyber key exchange!',
        diff:'easy', coins:30, xp:20, bossHit:0,
        code:[
            {t:'comment', text:'# Set up ML-KEM key exchange'},
            {t:'code',    text:'algorithm = "'},
            {t:'blank',   answer:'ML-KEM', placeholder:'algorithm name...'},
            {t:'code',    text:'"'},
            {t:'code',    text:'security_level = 768  # bits'},
            {t:'code',    text:'print(f"Using {algorithm} with {security_level}-bit security")'},
        ],
        output:'Using ML-KEM with 768-bit security\n✅ Kyber key exchange ready! Quantum-safe!',
        hint:'The NIST FIPS 203 standard — also known as Kyber',
        fact:'🔐 ML-KEM (FIPS 203) replaced RSA for key exchange! It uses Module Learning With Errors — math so hard even quantum computers cannot solve it!',
    },
    {
        id:1, emoji:'✍️', title:'Dilithium Signature',
        subtitle:'EASY — Fill in the FIPS number',
        desc:'ML-DSA (Dilithium) creates digital signatures that quantum computers cannot forge. What FIPS number is Dilithium?',
        diff:'easy', coins:35, xp:25, bossHit:0,
        code:[
            {t:'comment', text:'# Digital signature standard'},
            {t:'code',    text:'standard = "ML-DSA"'},
            {t:'code',    text:'fips_number = '},
            {t:'blank',   answer:'204', placeholder:'FIPS number...'},
            {t:'code',    text:'print(f"{standard} is FIPS {fips_number}")'},
            {t:'code',    text:'print("Quantum-safe digital signatures!")'},
        ],
        output:'ML-DSA is FIPS 204\nQuantum-safe digital signatures!',
        hint:'NIST published 4 standards: 203, 204, 205, 206. Dilithium is the second one.',
        fact:'✍️ ML-DSA (FIPS 204) signs software updates, code, and certificates! No quantum computer can forge a Dilithium signature.',
    },
    {
        id:2, emoji:'🏗️', title:'LWE Math Core',
        subtitle:'MEDIUM — Fill in the math answer',
        desc:'Learning With Errors (LWE) is the math behind Kyber. Solve: Given secret s=5, matrix A=3, noise e=2, compute b = (A*s + e) mod 17',
        diff:'medium', coins:50, xp:40, bossHit:15,
        code:[
            {t:'comment', text:'# LWE: b = (A*s + e) mod q'},
            {t:'code',    text:'A, s, e, q = 3, 5, 2, 17'},
            {t:'code',    text:'b = (A*s + e) % q'},
            {t:'comment', text:'# What is b? (3*5+2) mod 17 = ?'},
            {t:'code',    text:'b = '},
            {t:'blank',   answer:'0', placeholder:'calculate b...'},
            {t:'code',    text:'print(f"LWE result: b = {b}")'},
            {t:'code',    text:'print("Even knowing A and b, finding s is HARD!")'},
        ],
        output:'LWE result: b = 0\nEven knowing A and b, finding s is HARD!',
        hint:'3×5=15, 15+2=17, 17 mod 17 = 0',
        fact:'🏗️ Real Kyber uses vectors of thousands of LWE equations! Given only A and b, finding the secret s is computationally impossible — even for quantum computers!',
    },
    {
        id:3, emoji:'🌲', title:'SPHINCS+ Hash Tree',
        subtitle:'MEDIUM — Fill in the hash function',
        desc:'SPHINCS+ (SLH-DSA FIPS 205) uses hash trees for signatures. It only needs ONE type of math — hash functions. Which hash function does FIPS 205 use?',
        diff:'medium', coins:55, xp:45, bossHit:15,
        code:[
            {t:'comment', text:'# SPHINCS+ hash-based signature'},
            {t:'code',    text:'algorithm = "SLH-DSA"'},
            {t:'code',    text:'hash_function = "'},
            {t:'blank',   answer:'SHA-3', placeholder:'hash function...'},
            {t:'code',    text:'"'},
            {t:'code',    text:'print(f"{algorithm} uses {hash_function}")'},
            {t:'code',    text:'print("Safe even if lattice math breaks!")'},
        ],
        output:'SLH-DSA uses SHA-3\nSafe even if lattice math breaks!',
        hint:'It starts with SHA — the third version of Secure Hash Algorithm',
        fact:'🌲 SPHINCS+ chains thousands of SHA-3 hashes into a Merkle tree. Even if ALL lattice math (Kyber, Dilithium, Falcon) is broken, SPHINCS+ stays safe!',
    },
    {
        id:4, emoji:'🦅', title:'Falcon Compact Keys',
        subtitle:'MEDIUM — Fill in the key size',
        desc:'Falcon (FN-DSA FIPS 206) makes the smallest signatures. A Falcon-512 signature is approximately how many bytes? (vs Dilithium\'s 3293 bytes)',
        diff:'medium', coins:60, xp:50, bossHit:20,
        code:[
            {t:'comment', text:'# Falcon compact signatures'},
            {t:'code',    text:'algorithm = "FN-DSA Falcon-512"'},
            {t:'code',    text:'sig_bytes = '},
            {t:'blank',   answer:'666', placeholder:'size in bytes...'},
            {t:'code',    text:'dilithium_bytes = 3293'},
            {t:'code',    text:'print(f"Falcon: {sig_bytes} bytes")'},
            {t:'code',    text:'print(f"Dilithium: {dilithium_bytes} bytes")'},
            {t:'code',    text:'print(f"Falcon is {dilithium_bytes//sig_bytes}x smaller!")'},
        ],
        output:'Falcon: 666 bytes\nDilithium: 3293 bytes\nFalcon is 4x smaller!',
        hint:'Falcon-512 signatures are approximately 666 bytes — about 4-5x smaller than Dilithium',
        fact:'🦅 Falcon (FN-DSA FIPS 206) uses NTRU lattices to create the tiniest quantum-safe signatures — critical for IoT sensors, smart cards, and embedded devices!',
    },
    {
        id:5, emoji:'🌐', title:'TLS Quantum Upgrade',
        subtitle:'HARD — Fill in the hybrid protocol',
        desc:'Google Chrome uses a HYBRID TLS that combines classical X25519 with Kyber. What is the combined protocol called? (format: X25519+ML-KEM-768)',
        diff:'hard', coins:80, xp:70, bossHit:25,
        code:[
            {t:'comment', text:'# Hybrid quantum-safe TLS 1.3'},
            {t:'code',    text:'classical = "X25519"'},
            {t:'code',    text:'quantum_safe = "ML-KEM-768"'},
            {t:'code',    text:'hybrid = "'},
            {t:'blank',   answer:'X25519+ML-KEM-768', placeholder:'hybrid protocol...'},
            {t:'code',    text:'"'},
            {t:'code',    text:'print(f"Chrome uses: {hybrid}")'},
            {t:'code',    text:'print("Secure against classical AND quantum!")'},
        ],
        output:'Chrome uses: X25519+ML-KEM-768\nSecure against classical AND quantum!',
        hint:'Combine them with a + sign: classical_name+quantum_name',
        fact:'🌐 Google Chrome and Cloudflare already deployed this! X25519+ML-KEM-768 protects 20% of all internet traffic from both classical AND future quantum attacks!',
    },
    {
        id:6, emoji:'☠️', title:'Harvest Now Decrypt Later',
        subtitle:'HARD — Fill in the threat name',
        desc:'Nation-states are stealing encrypted data TODAY to decrypt it when quantum computers arrive. What is this attack called? (3 words, abbreviated HNDL)',
        diff:'hard', coins:90, xp:80, bossHit:25,
        code:[
            {t:'comment', text:'# The biggest PQC threat TODAY'},
            {t:'code',    text:'attack_name = "'},
            {t:'blank',   answer:'Harvest Now Decrypt Later', placeholder:'attack name...'},
            {t:'code',    text:'"'},
            {t:'code',    text:'threat_level = "CRITICAL"'},
            {t:'code',    text:'print(f"Threat: {attack_name}")'},
            {t:'code',    text:'print(f"Level: {threat_level} — Migrate to Kyber NOW!")'},
        ],
        output:'Threat: Harvest Now Decrypt Later\nLevel: CRITICAL — Migrate to Kyber NOW!',
        hint:'The 3 words describe the two phases: collect encrypted data NOW, decrypt LATER when quantum computers exist',
        fact:'☠️ HNDL is happening RIGHT NOW! Intelligence agencies are storing encrypted government and medical data — waiting for quantum computers. Data encrypted with RSA TODAY will be readable in 5-10 years!',
    },
    {
        id:7, emoji:'👑', title:'BOSS: Defeat the Shor Machine!',
        subtitle:'BOSS FIGHT — Fill in the migration deadline',
        desc:'🚨 The Shor Machine is attacking! US agencies must migrate to PQC by what year? (NSM-10 executive order)',
        diff:'boss', coins:150, xp:150, bossHit:100,
        code:[
            {t:'comment', text:'# NSM-10: US Federal PQC Migration'},
            {t:'code',    text:'mandate = "NSM-10"'},
            {t:'code',    text:'migration_deadline = '},
            {t:'blank',   answer:'2035', placeholder:'deadline year...'},
            {t:'code',    text:'print(f"All US agencies must use PQC by: {migration_deadline}")'},
            {t:'code',    text:'print("NIST FIPS 203/204/205/206 are the standards!")'},
            {t:'code',    text:'print("Shor Machine DEFEATED! 🏆")'},
        ],
        output:'All US agencies must use PQC by: 2035\nNIST FIPS 203/204/205/206 are the standards!\nShor Machine DEFEATED! 🏆',
        hint:'NSM-10 was signed in 2022. Agencies have about 13 years to migrate. 2022 + 13 = ?',
        fact:'🏆 NSM-10 (National Security Memorandum 10) requires ALL US federal agencies to migrate to post-quantum cryptography by 2035. The countdown has started!',
    },
];

// ── SHOP ITEMS ────────────────────────────────────────────────────────────────
const SHOP_ITEMS = [
    {id:'double_coins', emoji:'💰', name:'Double Coins', desc:'Earn 2x coins for 3 quests', cost:40, owned:false},
    {id:'auto_hint',    emoji:'💡', name:'Free Hint',    desc:'One free hint (no coin cost)', cost:50, owned:false},
    {id:'shield',       emoji:'🛡️', name:'Error Shield', desc:'One wrong answer forgiven', cost:60, owned:false},
    {id:'xp_boost',     emoji:'⚡', name:'XP Boost',     desc:'3x XP for next quest', cost:80, owned:false},
];

// ── RANKS ─────────────────────────────────────────────────────────────────────
const RANKS = [
    {name:'🔰 Rookie Spy',    xp:0},
    {name:'🕵️ Junior Agent', xp:50},
    {name:'🔐 Cipher Expert', xp:130},
    {name:'⚡ Code Breaker',  xp:250},
    {name:'🌟 Crypto Master', xp:400},
    {name:'👑 Quantum Guard', xp:600},
];

// ── STATE ─────────────────────────────────────────────────────────────────────
let coins=0, xp=0, streak=0, done=0;
let currentQuestId=null, hintsUsed=0, questDone=false;
let bossHp=100;
let powerups={double_coins:0, auto_hint:false, shield:false, xp_boost:false};
let questStatus=QUESTS.map(()=>'locked');
questStatus[0]='available'; questStatus[1]='available';

// ── BUILD QUEST MAP ───────────────────────────────────────────────────────────
function buildMap(){
    const grid=document.getElementById('quest-map');
    grid.innerHTML='';
    QUESTS.forEach((q,i)=>{
        const div=document.createElement('div');
        const st=questStatus[i];
        div.className='quest-node'+(st==='locked'?' locked':st==='done'?' done':q.diff==='boss'?' boss':st==='available'?' ':' ');
        if(i===currentQuestId) div.classList.add('active');
        const badgeClass=q.diff==='boss'?'badge-boss':q.diff==='easy'?'badge-easy':q.diff==='medium'?'badge-med':'badge-hard';
        div.innerHTML=
            '<span class="qn-emoji">'+q.emoji+'</span>'+
            '<div class="qn-title">'+q.title+'</div>'+
            '<div class="qn-coins">🪙 '+q.coins+' coins</div>'+
            '<span class="qn-badge '+(st==='done'?'badge-done':badgeClass)+'">'+(st==='done'?'✅':q.diff.toUpperCase())+'</span>';
        if(st!=='locked') div.onclick=()=>selectQuest(i);
        grid.appendChild(div);
    });
}

// ── SELECT QUEST ──────────────────────────────────────────────────────────────
function selectQuest(idx){
    currentQuestId=idx;
    const q=QUESTS[idx];
    questDone=false; hintsUsed=0;

    document.getElementById('q-emoji').textContent=q.emoji;
    document.getElementById('q-title').textContent=q.title;
    document.getElementById('q-subtitle').textContent=q.subtitle;
    document.getElementById('q-desc').textContent=q.desc;
    document.getElementById('q-output').textContent='// Output will appear here...';
    document.getElementById('next-btn').style.display='none';
    document.getElementById('fact').style.display='none';

    // Build code block
    const codeEl=document.getElementById('q-code');
    codeEl.innerHTML='';
    q.code.forEach((line,li)=>{
        if(line.t==='comment'){
            const span=document.createElement('span');
            span.className='code-comment'; span.textContent=line.text; codeEl.appendChild(span);
        } else if(line.t==='blank'){
            const input=document.createElement('input');
            input.type='text'; input.className='blank'; input.id='blank-'+li;
            input.placeholder=line.placeholder;
            input.onkeydown=e=>{if(e.key==='Enter') runQuest();};
            codeEl.appendChild(input);
        } else {
            const span=document.createElement('span');
            span.className='code-line'; span.textContent=line.text; codeEl.appendChild(span);
        }
    });

    // Boss fight UI
    const bossDiv=document.getElementById('boss-fight');
    if(q.diff==='boss'){
        bossDiv.style.display='block';
        bossHp=100;
        updateBossHp();
    } else {
        bossDiv.style.display='none';
    }

    buildMap();
    showTab('active');
    setMsg('💡 Fill in the blank and click Run Code!','#60a5fa');
    // Focus the blank
    setTimeout(()=>{
        const b=document.querySelector('.blank');
        if(b) b.focus();
    },100);
}

// ── RUN QUEST ─────────────────────────────────────────────────────────────────
function runQuest(){
    if(!currentQuestId&&currentQuestId!==0){setMsg('Select a quest from the map first!','#fbbf24');return;}
    if(questDone){setMsg('Quest already complete! Click Next Quest.','#10b981');return;}
    const q=QUESTS[currentQuestId];

    // Find the blank and check answer
    let blankIdx=-1, blankEl=null, userAnswer='';
    q.code.forEach((line,li)=>{
        if(line.t==='blank'){
            blankIdx=li;
            blankEl=document.getElementById('blank-'+li);
            userAnswer=(blankEl?blankEl.value.trim():'');
        }
    });

    const correct=q.code.find(l=>l.t==='blank')?.answer||'';
    const isCorrect=userAnswer.toLowerCase()===correct.toLowerCase();

    if(isCorrect){
        // Success!
        if(blankEl){ blankEl.classList.add('correct'); blankEl.classList.remove('wrong'); }
        questDone=true;
        questStatus[currentQuestId]='done';
        done++;
        streak++;

        // Calculate rewards
        let earnedCoins=q.coins*(powerups.double_coins>0?2:1);
        let earnedXP=q.xp*(powerups.xp_boost?3:1);
        if(powerups.double_coins>0) powerups.double_coins--;
        if(powerups.xp_boost) powerups.xp_boost=false;

        coins+=earnedCoins; xp+=earnedXP;

        // Boss fight
        if(q.diff==='boss'){
            bossHp=0; updateBossHp();
            confetti();
            showToast('👑 SHOR MACHINE DEFEATED! +'+earnedCoins+' coins!');
        } else {
            if(streak>=3) showToast('🔥 '+streak+' streak! +'+earnedCoins+' coins!');
            else showToast('✅ Correct! +'+earnedCoins+' coins +'+earnedXP+' XP!');
        }

        // Unlock next quests
        if(currentQuestId<QUESTS.length-1 && questStatus[currentQuestId+1]==='locked')
            questStatus[currentQuestId+1]='available';
        if(currentQuestId<QUESTS.length-2 && questStatus[currentQuestId+2]==='locked')
            questStatus[currentQuestId+2]='available';

        document.getElementById('q-output').textContent=q.output;
        document.getElementById('next-btn').style.display='block';
        showFact(q.fact);
        setMsg('🎉 Correct! Quest Complete! +'+earnedCoins+' coins!','#10b981');
        updateHUD();
        buildMap();
        if(streak>=3) confetti();

        // Boss damage animation
        if(q.bossHit>0 && q.diff!=='boss'){
            bossHp=Math.max(0,bossHp-q.bossHit);
            updateBossHp();
        }
    } else {
        // Wrong answer
        if(blankEl){ blankEl.classList.add('wrong'); blankEl.classList.remove('correct'); }
        streak=0;

        // Shield power-up
        if(powerups.shield){
            powerups.shield=false;
            setMsg('🛡️ Shield used! Try again — this one is free!','#fbbf24');
            setTimeout(()=>blankEl.classList.remove('wrong'),400);
        } else {
            setMsg('❌ Not quite! Try again or use a hint.','#ef4444');
        }
        updateHUD();
        setTimeout(()=>blankEl?.classList.remove('wrong'),400);
    }
}

// ── NEXT QUEST ────────────────────────────────────────────────────────────────
function nextQuest(){
    const next=QUESTS.findIndex((q,i)=>questStatus[i]==='available'&&i>currentQuestId);
    if(next!==-1) selectQuest(next);
    else { showTab('map'); setMsg('All available quests done! More unlock as you progress.','#10b981'); }
}

// ── HINT ──────────────────────────────────────────────────────────────────────
function useHint(){
    if(!currentQuestId&&currentQuestId!==0) return;
    const q=QUESTS[currentQuestId];
    if(powerups.auto_hint){ powerups.auto_hint=false; }
    else if(coins>=5){ coins-=5; updateHUD(); }
    else { showToast('❌ Not enough coins for a hint!'); return; }
    showFact('💡 Hint: '+q.hint);
    setMsg('💡 Hint used!','#fbbf24');
}

// ── SHOP ──────────────────────────────────────────────────────────────────────
function buildShop(){
    const grid=document.getElementById('shop-grid');
    grid.innerHTML='';
    SHOP_ITEMS.forEach(item=>{
        const div=document.createElement('div');
        const isOwned=powerups[item.id]&&powerups[item.id]!==false&&powerups[item.id]!==0;
        div.className='shop-item'+(isOwned?' owned':'');
        div.innerHTML=
            '<span class="si-emoji">'+item.emoji+'</span>'+
            '<div class="si-name">'+item.name+'</div>'+
            '<div class="si-desc">'+item.desc+'</div>'+
            '<div class="si-cost">'+(isOwned?'✅ Active':'🪙 '+item.cost+' coins')+'</div>';
        if(!isOwned) div.onclick=()=>buyItem(item);
        grid.appendChild(div);
    });
}

function buyItem(item){
    if(coins<item.cost){ showToast('❌ Need '+item.cost+' coins! Complete more quests.'); return; }
    coins-=item.cost;
    if(item.id==='double_coins') powerups.double_coins=3;
    else if(item.id==='auto_hint') powerups.auto_hint=true;
    else if(item.id==='shield') powerups.shield=true;
    else if(item.id==='xp_boost') powerups.xp_boost=true;
    showToast('✅ '+item.name+' purchased!');
    updateHUD();
    buildShop();
}

// ── BOSS HP ───────────────────────────────────────────────────────────────────
function updateBossHp(){
    document.getElementById('boss-hp-fill').style.width=bossHp+'%';
    document.getElementById('boss-status').textContent='Shor Machine HP: '+bossHp+'%';
    if(bossHp<=0){
        document.getElementById('boss-status').textContent='💀 DEFEATED! The internet is quantum-safe!';
    }
}

// ── TABS ──────────────────────────────────────────────────────────────────────
function showTab(tab){
    ['map','active','shop'].forEach(t=>{
        document.getElementById('tab-'+t).style.display=t===tab?'block':'none';
    });
    document.querySelectorAll('.tab').forEach((el,i)=>{
        el.classList.toggle('active',['map','active','shop'][i]===tab);
    });
    if(tab==='shop') buildShop();
    if(tab==='map') buildMap();
}

// ── HUD ───────────────────────────────────────────────────────────────────────
function updateHUD(){
    document.getElementById('h-coins').textContent=coins;
    document.getElementById('h-xp').textContent=xp;
    document.getElementById('h-streak').textContent=streak;
    document.getElementById('h-done').textContent=done;
    const rank=RANKS.filter(r=>xp>=r.xp).pop();
    const next=RANKS.find(r=>r.xp>xp);
    document.getElementById('rank-name').textContent=rank.name;
    if(next){
        const pct=Math.min(100,((xp-rank.xp)/(next.xp-rank.xp))*100);
        document.getElementById('rank-xp-fill').style.width=pct+'%';
        document.getElementById('rank-next').textContent=xp+'/'+next.xp;
    } else {
        document.getElementById('rank-xp-fill').style.width='100%';
        document.getElementById('rank-next').textContent='MAX!';
    }
}

function setMsg(m,c){ const el=document.getElementById('msg'); el.textContent=m; el.style.color=c||'#60a5fa'; }

let factTimer=null;
function showFact(t){ const el=document.getElementById('fact'); el.textContent=t; el.style.display='block'; if(factTimer)clearTimeout(factTimer); factTimer=setTimeout(()=>el.style.display='none',7000); }

let toastTimer=null;
function showToast(m){ const el=document.getElementById('toast'); el.textContent=m; el.classList.add('show'); if(toastTimer)clearTimeout(toastTimer); toastTimer=setTimeout(()=>el.classList.remove('show'),2500); }

function confetti(){ const cols=['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444']; for(let i=0;i<25;i++){ setTimeout(()=>{ const el=document.createElement('div'); el.className='cp'; el.style.left=Math.random()*100+'vw'; el.style.background=cols[Math.floor(Math.random()*cols.length)]; el.style.animationDuration=(1+Math.random()*2)+'s'; document.body.appendChild(el); setTimeout(()=>el.remove(),3000); },i*40); } }

// ── INIT ─────────────────────────────────────────────────────────────────────
buildMap();
updateHUD();
setMsg('🗺️ Pick a quest from the map to start your mission!','#60a5fa');
</script>
</body>
</html>
""", height=720)

def render_pqc_python_lab():
    """High School 9-12: PQC Python Lab — UPGRADED 2026 — AI reviewer, speed bonus, certificates."""
    import streamlit as st
    import streamlit.components.v1 as components
    from modules.trial import trial_gate
    if not trial_gate("pqc_python_lab", "PQC Python Lab"):
        return
    st.subheader("🐍 PQC Python Lab")
    st.markdown(
        "**Write real Python code** to master post-quantum cryptography! "
        "Earn XP, unlock challenges, and get an AI code review on completion!"
    )

    challenges = [
        {
            "id": 1, "title": "Caesar Cipher Decoder", "difficulty": "🟢 Beginner",
            "concept": "Why simple ciphers fail",
            "xp": 50, "coins": 30,
            "desc": "Decode a Caesar cipher by brute force. This shows why old ciphers are weak — then we'll see what makes Kyber unbreakable.",
            "starter": """# CHALLENGE 1: Crack a Caesar Cipher
# Caesar only has 25 possible keys — easy to brute force!
ciphertext = 'Khoor Zruog'

# Loop through all 25 possible shifts
for shift in range(1, 26):
    decoded = ''
    for c in ciphertext:
        if c.isalpha():
            base = 65 if c.isupper() else 97
            decoded += chr((ord(c) - base - shift) % 26 + base)
        else:
            decoded += c
    print(f'Shift {shift:2d}: {decoded}')

print('\\nKyber has 2^256 keys — NOT 25!')
print('Even quantum computers cannot brute force Kyber!')""",
            "hint": "Run it as-is! Look for the shift that produces a real English phrase.",
            "check_word": "Hello World",
            "fact": "Caesar: 25 keys, cracked in milliseconds. Kyber: 2^256 keys — a number larger than atoms in the observable universe!",
        },
        {
            "id": 2, "title": "LWE Math Core", "difficulty": "🟢 Beginner",
            "concept": "The math inside Kyber",
            "xp": 75, "coins": 50,
            "desc": "Implement Learning With Errors (LWE) — the actual mathematical foundation of Kyber! This is what makes it quantum-safe.",
            "starter": """# CHALLENGE 2: Learning With Errors (LWE)
# This is the REAL math inside Kyber (ML-KEM FIPS 203)!

import random

# Parameters (tiny version for learning)
q = 17      # modulus (real Kyber uses q=3329)
n = 4       # dimension (real Kyber uses n=256)

# Secret key (what we want to hide)
secret = [3, 1, 4, 1]  # short secret vector

# Public matrix A (known to everyone)
A = [[2,3,1,4],[1,2,3,1],[4,1,2,3],[3,4,1,2]]

# Add noise (this is what makes LWE hard to reverse!)
noise = [random.randint(0,2) for _ in range(n)]

# Compute b = A*s + e (mod q)
b = []
for row in A:
    val = sum(row[i]*secret[i] for i in range(n))
    val = (val + noise[b.__len__()]) % q
    b.append(val)

print(f'Secret s = {secret}')
print(f'Public b = {b}')
print(f'Noise e  = {noise}')
print('\\nEven knowing A and b, finding s requires')
print('solving billions of equations — impossible for quantum computers!')""",
            "hint": "The noise variable is auto-generated. Just run the code and observe how b looks random even though s is simple.",
            "check_word": "impossible for quantum",
            "fact": "Real Kyber uses 256-dimensional vectors with modulus q=3329. The noise makes it computationally infeasible to recover the secret — even with Shor's Algorithm!",
        },
        {
            "id": 3, "title": "Hash Avalanche Effect", "difficulty": "🟡 Intermediate",
            "concept": "SHA-3 inside SPHINCS+",
            "xp": 100, "coins": 70,
            "desc": "Demonstrate SHA-3's avalanche effect — the core of SPHINCS+ (FIPS 205). Change ONE character and see how 50% of the hash changes!",
            "starter": """# CHALLENGE 3: SHA-3 Avalanche Effect
# SHA-3 is used inside SPHINCS+ (SLH-DSA FIPS 205)

import hashlib

msg1 = "QuantumVault Academy"
msg2 = "QuantumVault academy"  # Only 'A' changed to 'a'!

# Hash both messages with SHA-3
h1 = hashlib.sha3_256(msg1.encode()).hexdigest()
h2 = hashlib.sha3_256(msg2.encode()).hexdigest()

print(f'Message 1: {msg1}')
print(f'Hash 1:    {h1}')
print()
print(f'Message 2: {msg2}')
print(f'Hash 2:    {h2}')

# Count different characters
diff = sum(1 for a, b in zip(h1, h2) if a != b)
pct = round(diff / len(h1) * 100)
print(f'\\nDifferent: {diff}/64 characters ({pct}% changed!)')
print('ONE letter change = HALF the hash changed!')
print('This is the AVALANCHE EFFECT — SHA-3 is quantum-resistant!')""",
            "hint": "Run it as-is! The avalanche effect is built into SHA-3. Observe how much of the hash changes.",
            "check_word": "AVALANCHE EFFECT",
            "fact": "SHA-3's avalanche effect means every output bit depends on every input bit. Grover's Algorithm halves SHA-3's security — but SHA3-256 with 128-bit quantum security is still unbreakable!",
        },
        {
            "id": 4, "title": "Kyber Key Exchange Simulation", "difficulty": "🟡 Intermediate",
            "concept": "How ML-KEM works",
            "xp": 150, "coins": 100,
            "desc": "Simulate a simplified Kyber key exchange between Alice and Bob! See how they create a shared secret without ever sending it.",
            "starter": """# CHALLENGE 4: Kyber Key Exchange (Simplified)
# This simulates ML-KEM (FIPS 203) key encapsulation

import random

q = 17  # modulus

def keygen():
    '''Alice generates her key pair'''
    secret = [random.randint(0,3) for _ in range(4)]
    public = [(3*s + random.randint(0,1)) % q for s in secret]
    return secret, public

def encapsulate(public_key):
    '''Bob creates ciphertext and shared secret'''
    r = [random.randint(0,3) for _ in range(4)]
    ciphertext = [(pk + ri) % q for pk, ri in zip(public_key, r)]
    shared_secret = sum(r) % q
    return ciphertext, shared_secret

def decapsulate(secret_key, ciphertext):
    '''Alice recovers shared secret'''
    recovered = sum((ct - 3*sk) % q for ct, sk in zip(ciphertext, secret_key)) % q
    return recovered

# Run the key exchange!
alice_secret, alice_public = keygen()
ciphertext, bob_secret = encapsulate(alice_public)
alice_recovered = decapsulate(alice_secret, ciphertext)

print(f'Alice public key: {alice_public}')
print(f'Bob ciphertext:   {ciphertext}')
print(f'Bob shared secret:   {bob_secret}')
print(f'Alice recovered:     {alice_recovered}')
print()
print('Real Kyber uses 768-dimensional vectors')
print('and modulus q=3329 for 128-bit quantum security!')""",
            "hint": "Run as-is to see the key exchange! Notice Bob and Alice never directly share the secret.",
            "check_word": "128-bit quantum security",
            "fact": "Real ML-KEM-768 uses 768-dimensional vectors. The public key is 1184 bytes, ciphertext 1088 bytes. Even with a quantum computer running Grover's Algorithm, it would take longer than the age of the universe to crack!",
        },
        {
            "id": 5, "title": "Digital Signature Verify", "difficulty": "🔴 Advanced",
            "concept": "ML-DSA (Dilithium) signatures",
            "xp": 200, "coins": 150,
            "desc": "Implement a simplified Dilithium-style signature scheme! Sign a message and verify it — then try to forge a signature and see why it fails.",
            "starter": """# CHALLENGE 5: Dilithium-Style Digital Signatures
# Simulating ML-DSA (FIPS 204) signature scheme

import hashlib, random

q = 257  # prime modulus

def keygen():
    '''Generate signing/verification key pair'''
    private_key = [random.randint(1, q-1) for _ in range(4)]
    public_key = [(3*pk) % q for pk in private_key]
    return private_key, public_key

def sign(message, private_key):
    '''Sign a message with private key'''
    msg_hash = int(hashlib.sha3_256(message.encode()).hexdigest()[:8], 16)
    signature = [(pk * msg_hash) % q for pk in private_key]
    return signature

def verify(message, signature, public_key):
    '''Verify signature with public key'''
    msg_hash = int(hashlib.sha3_256(message.encode()).hexdigest()[:8], 16)
    expected = [(pub * msg_hash) % q for pub in public_key]
    check = [(sig * 3) % q for sig in signature]
    return check == expected

# Test the signature
private_key, public_key = keygen()
message = "QuantumVault Academy - Quantum Safe!"
signature = sign(message, private_key)
valid = verify(message, signature, public_key)

print(f'Message:   {message}')
print(f'Signature: {signature[:2]}... (truncated)')
print(f'Valid:     {valid}')

# Try to forge a signature
fake_sig = [random.randint(0, q-1) for _ in range(4)]
forged = verify(message, fake_sig, public_key)
print(f'\\nForged signature valid: {forged}')
print('Impossible to forge without the private key!')
print('Real ML-DSA uses Module-LWE + SIS — quantum computers cannot crack it!')""",
            "hint": "Run as-is! The key insight is that fake_sig will ALWAYS fail verification — that's what makes digital signatures secure.",
            "check_word": "Impossible to forge",
            "fact": "Real ML-DSA (Dilithium FIPS 204) has a 3293-byte signature and 1952-byte public key. Forging it requires solving Module-SIS — a hard lattice problem that quantum computers cannot solve!",
        },
    ]

    # Session state
    if "pqc_lab_idx" not in st.session_state:
        st.session_state.pqc_lab_idx = 0
    if "pqc_lab_xp" not in st.session_state:
        st.session_state.pqc_lab_xp = 0
    if "pqc_lab_coins" not in st.session_state:
        st.session_state.pqc_lab_coins = 0
    if "pqc_lab_done" not in st.session_state:
        st.session_state.pqc_lab_done = []

    idx = st.session_state.pqc_lab_idx
    total_xp = st.session_state.pqc_lab_xp
    coins = st.session_state.pqc_lab_coins
    done_list = st.session_state.pqc_lab_done

    # HUD
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⭐ XP", total_xp)
    col2.metric("🪙 Coins", coins)
    col3.metric("✅ Done", f"{len(done_list)}/{len(challenges)}")
    col4.metric("🏆 Challenge", f"{idx+1}/{len(challenges)}")

    # Progress bar
    prog_cols = st.columns(len(challenges))
    for i, ch in enumerate(challenges):
        with prog_cols[i]:
            if i in done_list:
                st.success(f"✅ {i+1}")
            elif i == idx:
                st.info(f"▶ {i+1}")
            else:
                st.markdown(f"<div style='text-align:center;color:#334155;padding:4px'>🔒 {i+1}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Current challenge
    if idx >= len(challenges):
        st.balloons()
        st.success("🏆 **ALL 5 CHALLENGES COMPLETE!** You are a PQC Python expert!")
        st.markdown(f"""
<div style='background:linear-gradient(135deg,#071520,#0a1f35);border:3px solid #fbbf24;
border-radius:16px;padding:24px;text-align:center;'>
<div style='font-size:3rem'>🏆</div>
<h2 style='color:#fbbf24'>PQC Python Lab Certificate</h2>
<p style='color:#94a3b8'>This certifies mastery of</p>
<h3 style='color:#60a5fa'>Post-Quantum Cryptography Programming</h3>
<p style='color:#94a3b8'>Caesar Cipher · LWE Math · SHA-3 · Kyber KEM · Dilithium Signatures</p>
<p style='color:#10b981;font-size:14px'>Total XP: {total_xp} | Coins: {coins}</p>
<p style='color:#fbbf24;font-size:11px'>QuantumVault Academy · FIPS 203/204/205/206</p>
</div>
""", unsafe_allow_html=True)
        if st.button("🔄 Restart Lab"):
            st.session_state.pqc_lab_idx = 0
            st.session_state.pqc_lab_xp = 0
            st.session_state.pqc_lab_coins = 0
            st.session_state.pqc_lab_done = []
            st.rerun()
        return

    ch = challenges[idx]

    # Challenge header
    st.markdown(f"### {ch['difficulty']} — {ch['title']}")
    st.markdown(f"**Concept:** {ch['concept']} | 🪙 {ch['coins']} coins | ⭐ {ch['xp']} XP")
    st.info(ch["desc"])

    # Code editor
    code = st.text_area(
        "✏️ Your Python code:",
        value=ch["starter"],
        height=280,
        key=f"code_{idx}"
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        run = st.button("▶️ Run Code", type="primary", use_container_width=True, key=f"run_{idx}")
    with col2:
        hint = st.button("💡 Hint", use_container_width=True, key=f"hint_{idx}")

    if hint:
        st.warning(f"💡 **Hint:** {ch['hint']}")

    if run:
        import io, sys, traceback, time
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        start_time = time.time()
        error = None
        try:
            exec(compile(code, "<lab>", "exec"), {})
        except Exception:
            error = traceback.format_exc()
        elapsed = time.time() - start_time
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        if error:
            st.error(f"❌ Python Error:\n```\n{error}\n```")
            st.markdown("🔧 Check your syntax and try again!")
        else:
            st.code(output, language="text")

            # Check for key output
            if ch["check_word"].lower() in output.lower():
                if idx not in done_list:
                    done_list.append(idx)
                    st.session_state.pqc_lab_done = done_list

                    # Speed bonus
                    speed_bonus = 20 if elapsed < 5 else 0
                    earned_xp = ch["xp"] + speed_bonus
                    earned_coins = ch["coins"]
                    st.session_state.pqc_lab_xp = total_xp + earned_xp
                    st.session_state.pqc_lab_coins = coins + earned_coins

                    st.success(f"🎉 **Challenge Complete!** +{earned_xp} XP +{earned_coins} coins!" +
                               (f" ⚡ Speed bonus +{speed_bonus} XP!" if speed_bonus else ""))
                    st.balloons()
                else:
                    st.success("✅ Challenge already completed! Experimenting — great habit!")

                st.info(f"💡 **PQC Fact:** {ch['fact']}")

                # AI Review button
                if st.button("🤖 Get AI Code Review", key=f"ai_{idx}"):
                    try:
                        import anthropic
                        client = anthropic.Anthropic(api_key=st.secrets.get("ANTHROPIC_API_KEY",""))
                        with st.spinner("🤖 AI reviewing your code..."):
                            response = client.messages.create(
                                model="claude-sonnet-4-6",
                                max_tokens=400,
                                messages=[{"role":"user","content":
                                    f"Review this Python code from a high school student learning PQC cryptography. "
                                    f"Be encouraging, specific, and educational. Max 150 words. "
                                    f"Code:\n{code}\n\nOutput:\n{output}"}]
                            )
                        st.success("🤖 **AI Code Review:**\n\n" + response.content[0].text)
                    except Exception:
                        st.info("🤖 AI review unavailable — your code is great!")

                if idx + 1 < len(challenges):
                    if st.button("➡️ Next Challenge!", type="primary", key=f"next_{idx}"):
                        st.session_state.pqc_lab_idx = idx + 1
                        st.rerun()
                else:
                    if st.button("🏆 Complete the Lab!", type="primary", key=f"complete_{idx}"):
                        st.session_state.pqc_lab_idx = len(challenges)
                        st.rerun()
            else:
                st.warning("⚠️ Code ran but the output doesn't match. Check your logic and try again!")
                st.info(f"💡 Look for: *{ch['check_word']}* in your output")

