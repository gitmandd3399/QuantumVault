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
    """K-5: Enhanced Falling Blocks with better graphics, power-ups, boss waves, PQC education."""
    st.subheader("🧱 Quantum Lock Drop — Enhanced!")
    st.markdown(
        "Catch **quantum-safe locks** and avoid **broken crypto**! "
        "Collect power-ups for special abilities. Boss waves every 5 levels!"
    )

    with st.expander("📚 What to catch vs avoid!", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.success("✅ **CATCH THESE — Quantum Safe!**")
            st.info("🔐 Kyber — ML-KEM FIPS 203\n✍️ Dilithium — ML-DSA FIPS 204\n🌲 SPHINCS+ — SLH-DSA FIPS 205\n🦅 Falcon — FN-DSA FIPS 206\n🏗️ Lattice — Foundation of PQC")
        with col2:
            st.error("❌ **AVOID THESE — Quantum Vulnerable!**")
            st.info("💀 RSA — Broken by Shor Algorithm\n☠️ ECC — Also broken by Shor\n⚠️ DES — Classically broken 1999\n💥 MD5 — Collision attacks\n🔓 RC4 — Stream cipher broken")
        st.warning("⚡ **POWER-UPS** — Catch these for special abilities!\n🛡️ Shield — Protect from one bad block\n⏰ Slow — Slow down all falling blocks\n💎 Double — Double points for 10 seconds")

    import streamlit.components.v1 as components_fb
    components_fb.html("""
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0f172a;font-family:sans-serif;color:white;}
#fb-wrap{display:flex;flex-direction:column;align-items:center;padding:10px;}
.fb-hud{display:flex;justify-content:space-between;width:420px;margin-bottom:8px;gap:5px;}
.hud-box{background:#1e293b;border:1px solid #334155;border-radius:8px;
padding:5px 8px;font-size:11px;font-weight:bold;color:#a5b4fc;flex:1;text-align:center;}
#fbCanvas{border:2px solid #4f46e5;border-radius:12px;display:block;}
.fb-btns{display:flex;gap:6px;margin:8px 0;justify-content:center;}
.fb-btn{padding:8px 18px;border-radius:8px;border:none;cursor:pointer;
font-size:13px;font-weight:bold;color:white;}
.fb-btn:active{opacity:0.8;}
#fb-msg{font-size:12px;color:#34d399;min-height:18px;margin:4px;text-align:center;}
#fb-fact{background:rgba(79,70,229,0.15);border:1px solid rgba(79,70,229,0.4);
border-radius:8px;padding:6px 12px;margin:4px;font-size:11px;color:#a5b4fc;
max-width:420px;display:none;text-align:center;}
.power-bar{display:flex;gap:6px;justify-content:center;margin:4px;}
.power-slot{width:36px;height:36px;background:#1e293b;border:1px solid #334155;
border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:18px;}
.power-slot.active{border-color:#f59e0b;background:rgba(245,158,11,0.2);}
</style>
</head>
<body>
<div id="fb-wrap">
    <div class="fb-hud">
        <div class="hud-box">⭐ Score<br><span id="score">0</span></div>
        <div class="hud-box">❤️ Lives<br><span id="lives">3</span></div>
        <div class="hud-box">📊 Level<br><span id="level">1</span></div>
        <div class="hud-box">🎯 Caught<br><span id="caught">0</span></div>
        <div class="hud-box">🌊 Wave<br><span id="wave">Normal</span></div>
    </div>
    <canvas id="fbCanvas" width="420" height="480"></canvas>
    <div id="fb-msg">Press Start to play!</div>
    <div id="fb-fact"></div>
    <div class="power-bar">
        <div class="power-slot" id="pw-shield" title="Shield">🛡️</div>
        <div class="power-slot" id="pw-slow" title="Slow">⏰</div>
        <div class="power-slot" id="pw-double" title="Double Points">💎</div>
    </div>
    <div class="fb-btns">
        <button class="fb-btn" style="background:#4f46e5" onclick="moveLeft()">◀</button>
        <button class="fb-btn" style="background:#10b981" onclick="startGame()">▶ Start</button>
        <button class="fb-btn" style="background:#4f46e5" onclick="moveRight()">▶</button>
    </div>
</div>
<script>
const canvas = document.getElementById("fbCanvas");
const ctx = canvas.getContext("2d");
const W=420, H=480;

const SAFE_BLOCKS = [
    {label:"Kyber 🔐",   color:"#10b981", safe:true,  pts:15, fact:"ML-KEM FIPS 203 — NIST standard key encapsulation!"},
    {label:"Dilithium ✍️",color:"#3b82f6", safe:true,  pts:20, fact:"ML-DSA FIPS 204 — Quantum-safe digital signatures!"},
    {label:"SPHINCS+ 🌲", color:"#8b5cf6", safe:true,  pts:25, fact:"SLH-DSA FIPS 205 — Hash-based backup signature!"},
    {label:"Falcon 🦅",   color:"#f59e0b", safe:true,  pts:30, fact:"FN-DSA FIPS 206 — Smallest quantum-safe signature!"},
    {label:"Lattice 🏗️",  color:"#06b6d4", safe:true,  pts:20, fact:"Lattice math stumps quantum computers!"},
];

const UNSAFE_BLOCKS = [
    {label:"RSA 💀",  color:"#ef4444", safe:false, pts:-1, fact:"RSA broken by Shor Algorithm on quantum computers!"},
    {label:"ECC ☠️",  color:"#f97316", safe:false, pts:-1, fact:"ECC also broken by Shor Algorithm!"},
    {label:"DES ⚠️",  color:"#eab308", safe:false, pts:-1, fact:"DES was classically broken back in 1999!"},
    {label:"MD5 💥",  color:"#ec4899", safe:false, pts:-1, fact:"MD5 has dangerous collision attacks!"},
    {label:"RC4 🔓",  color:"#a855f7", safe:false, pts:-1, fact:"RC4 stream cipher is completely broken!"},
];

const POWERUPS = [
    {label:"SHIELD 🛡️", color:"#fbbf24", type:"shield", fact:"Shield protects you from one bad block!"},
    {label:"SLOW ⏰",    color:"#60a5fa", type:"slow",   fact:"Slow motion — more time to react!"},
    {label:"2x 💎",     color:"#34d399", type:"double", fact:"Double points — catch quantum-safe blocks fast!"},
];

const BOSS_BLOCKS = [
    {label:"QUANTUM 💻", color:"#dc2626", safe:false, pts:-1, boss:true, fact:"Full quantum computer — the ultimate threat to RSA!"},
];

let basket = {x:W/2-50, y:H-40, w:100, h:22, speed:30};
let blocks=[], particles=[], stars=[];
let score=0, lives=3, level=1, caught=0, running=false;
let frameCount=0, dropRate=80;
let shield=false, slowActive=false, doubleActive=false;
let shieldTimer=0, slowTimer=0, doubleTimer=0;
let bossWave=false;

// Generate stars
for(let i=0;i<50;i++) stars.push({x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.5+0.3,twinkle:Math.random()*Math.PI*2});

function showFact(fact){
    const f=document.getElementById("fb-fact");
    f.textContent="📚 "+fact;f.style.display="block";
    clearTimeout(window._ft);
    window._ft=setTimeout(()=>{f.style.display="none";},3500);
}

function showMsg(msg){document.getElementById("fb-msg").textContent=msg;}

function updateHUD(){
    document.getElementById("score").textContent=score;
    document.getElementById("lives").textContent="❤️".repeat(Math.max(0,lives));
    document.getElementById("level").textContent=level+"/12";
    document.getElementById("caught").textContent=caught;
    document.getElementById("wave").textContent=bossWave?"👾 BOSS!":"Normal";

    // Power-up indicators
    document.getElementById("pw-shield").className="power-slot"+(shield?" active":"");
    document.getElementById("pw-slow").className="power-slot"+(slowActive?" active":"");
    document.getElementById("pw-double").className="power-slot"+(doubleActive?" active":"");
}

function startGame(){
    blocks=[];particles=[];
    score=0;lives=LEVEL_CONFIG[0].lives;level=1;caught=0;running=true;
    frameCount=0;dropRate=LEVEL_CONFIG[0].dropRate;bossWave=false;
    shield=false;slowActive=false;doubleActive=false;
    basket.x=W/2-basket.w/2;
    updateHUD();
    showMsg("Catch quantum-safe blocks! Avoid broken crypto!");
    cancelAnimationFrame(window._fbFrame);
    gameLoop();
}

function moveLeft(){basket.x=Math.max(0,basket.x-basket.speed);}
function moveRight(){basket.x=Math.min(W-basket.w,basket.x+basket.speed);}

document.addEventListener("keydown",e=>{
    if(e.key==="ArrowLeft")moveLeft();
    if(e.key==="ArrowRight")moveRight();
});

function spawnBlock(){
    const isBoss = bossWave;
    let blockType;
    const r=Math.random();
    if(isBoss){
        blockType={...BOSS_BLOCKS[0]};
    } else if(r<0.08){
        blockType={...POWERUPS[Math.floor(Math.random()*POWERUPS.length)],isPowerup:true};
    } else if(r<0.55){
        blockType={...SAFE_BLOCKS[Math.floor(Math.random()*SAFE_BLOCKS.length)]};
    } else {
        blockType={...UNSAFE_BLOCKS[Math.floor(Math.random()*UNSAFE_BLOCKS.length)]};
    }

    blocks.push({
        x:Math.floor(Math.random()*(W-80))+10,
        y:-40, w:80, h:34,
        speed:getLevelConfig().speed*(slowActive?0.4:1)*(isBoss?1.5:1),
        ...blockType
    });
}

function gameLoop(){
    window._fbFrame=requestAnimationFrame(gameLoop);
    if(!running)return;

    // Power-up timers
    if(shield&&shieldTimer-->0===false){shield=false;}
    if(slowActive&&--slowTimer<=0){slowActive=false;}
    if(doubleActive&&--doubleTimer<=0){doubleActive=false;}

    frameCount++;
    const effectiveRate=Math.max(25,dropRate-(level-1)*5);
    if(frameCount%effectiveRate===0) spawnBlock();

    // Boss wave check using level config
    const cfg = getLevelConfig();
    const bossEvery = cfg.bossEvery;
    if(bossEvery>0 && level%bossEvery===0&&!bossWave){
        bossWave=true;
        showMsg("👾 BOSS WAVE " + cfg.name + "! Quantum computers attacking!");
        document.getElementById("wave").textContent="👾 BOSS!";
    } else if(!(bossEvery>0&&level%bossEvery===0)&&bossWave){
        bossWave=false;
    }

    // Update blocks
    blocks=blocks.filter(b=>{
        b.y+=b.speed*(slowActive?0.4:1);

        // Collision with basket
        if(b.y+b.h>=basket.y&&b.y<=basket.y+basket.h&&
           b.x+b.w>=basket.x&&b.x<=basket.x+basket.w){

            if(b.isPowerup){
                // Collect power-up
                if(b.type==="shield"){shield=true;shieldTimer=300;}
                if(b.type==="slow"){slowActive=true;slowTimer=300;}
                if(b.type==="double"){doubleActive=true;doubleTimer=300;}
                showMsg("⚡ Power-up: "+b.label+"!");
                showFact(b.fact);
                // Sparkle
                for(let i=0;i<12;i++) particles.push({
                    x:b.x+b.w/2,y:b.y,
                    vx:(Math.random()-0.5)*6,vy:-Math.random()*5,
                    color:b.color,alpha:1,r:4
                });
                return false;
            }

            if(b.safe){
                const pts=(b.pts||15)*(doubleActive?2:1)*Math.ceil(level/2);
                score+=pts;caught++;
                showMsg("✅ Caught "+b.label+"! +"+pts+(doubleActive?" (2x!)":""));
                showFact(b.fact);
                // Level up every 8 catches
                if(caught%8===0 && level<12){
                    level++;
                    const newCfg = getLevelConfig();
                    dropRate = newCfg.dropRate;
                    showMsg("🎉 Level "+level+": "+newCfg.name+"! "+newCfg.desc);
                } else if(level>=12 && caught%8===0){
                    showMsg("🏆 MAX LEVEL! Quantum Guardian achieved! Score: "+score);
                }
                // Green sparkle
                for(let i=0;i<8;i++) particles.push({
                    x:b.x+b.w/2,y:b.y,
                    vx:(Math.random()-0.5)*5,vy:-Math.random()*4,
                    color:"#10b981",alpha:1,r:3
                });
            } else {
                if(shield){
                    shield=false;
                    showMsg("🛡️ Shield blocked "+b.label+"!");
                    showFact(b.fact);
                } else {
                    lives--;
                    showMsg("💀 "+b.label+" hit! "+b.fact);
                    showFact(b.fact);
                    // Red flash particles
                    for(let i=0;i<10;i++) particles.push({
                        x:b.x+b.w/2,y:b.y,
                        vx:(Math.random()-0.5)*6,vy:-Math.random()*4,
                        color:"#ef4444",alpha:1,r:4
                    });
                    if(lives<=0){
                        running=false;
                        showMsg("☠️ Game Over! Score: "+score+" | Level: "+level);
                    }
                }
            }
            updateHUD();
            return false;
        }

        // Missed safe block
        if(b.y>H){
            if(b.safe&&!b.isPowerup){
                lives--;
                showMsg("⚠️ Missed "+b.label+"! It was quantum-safe!");
                updateHUD();
                if(lives<=0){running=false;showMsg("☠️ Game Over! Score: "+score);}
            }
            return false;
        }
        return true;
    });

    // Update particles
    particles=particles.filter(p=>{
        p.x+=p.vx;p.y+=p.vy;p.vy+=0.2;p.alpha-=0.04;
        return p.alpha>0;
    });

    updateHUD();
    render();
}

function render(){
    ctx.clearRect(0,0,W,H);

    // Starfield background
    const bg=ctx.createLinearGradient(0,0,0,H);
    bg.addColorStop(0,"#0f0c29");
    bg.addColorStop(1,"#1e1b4b");
    ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

    // Twinkling stars
    stars.forEach(s=>{
        s.twinkle+=0.02;
        const alpha=0.3+Math.sin(s.twinkle)*0.3;
        ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
        ctx.fillStyle="rgba(255,255,255,"+alpha+")";ctx.fill();
    });

    // Grid lines
    ctx.strokeStyle="rgba(79,70,229,0.06)";
    for(let i=0;i<W;i+=42){ctx.beginPath();ctx.moveTo(i,0);ctx.lineTo(i,H);ctx.stroke();}
    for(let i=0;i<H;i+=42){ctx.beginPath();ctx.moveTo(0,i);ctx.lineTo(W,i);ctx.stroke();}

    // Particles
    particles.forEach(p=>{
        ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
        ctx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,"0");
        ctx.fill();
    });

    // Blocks
    blocks.forEach(b=>{
        // Shadow
        ctx.fillStyle="rgba(0,0,0,0.3)";
        ctx.beginPath();ctx.roundRect(b.x+4,b.y+4,b.w,b.h,8);ctx.fill();

        // Block body
        const grad=ctx.createLinearGradient(b.x,b.y,b.x,b.y+b.h);
        grad.addColorStop(0,b.color+"ee");
        grad.addColorStop(1,b.color+"88");
        ctx.fillStyle=grad;
        ctx.beginPath();ctx.roundRect(b.x,b.y,b.w,b.h,8);ctx.fill();

        // Border
        ctx.strokeStyle=b.safe||b.isPowerup?"rgba(255,255,255,0.4)":"rgba(255,0,0,0.4)";
        ctx.lineWidth=b.boss?3:1.5;
        ctx.beginPath();ctx.roundRect(b.x,b.y,b.w,b.h,8);ctx.stroke();

        // Boss pulse
        if(b.boss){
            ctx.beginPath();ctx.roundRect(b.x-3,b.y-3,b.w+6,b.h+6,10);
            ctx.strokeStyle="rgba(220,38,38,"+(0.3+Math.sin(Date.now()*0.01)*0.3)+")";
            ctx.lineWidth=2;ctx.stroke();
        }

        // Label
        ctx.fillStyle="white";
        ctx.font="bold 11px sans-serif";
        ctx.textAlign="center";
        ctx.fillText(b.label,b.x+b.w/2,b.y+b.h/2+4);
    });

    // Basket
    const bgrad=ctx.createLinearGradient(basket.x,basket.y,basket.x,basket.y+basket.h);
    bgrad.addColorStop(0,shield?"#fbbf24":"#4f46e5");
    bgrad.addColorStop(1,shield?"#d97706":"#3730a3");
    ctx.fillStyle=bgrad;
    ctx.beginPath();ctx.roundRect(basket.x,basket.y,basket.w,basket.h,8);ctx.fill();

    // Shield glow
    if(shield){
        ctx.beginPath();ctx.roundRect(basket.x-4,basket.y-4,basket.w+8,basket.h+8,10);
        ctx.strokeStyle="rgba(251,191,36,0.5)";ctx.lineWidth=3;ctx.stroke();
    }

    // Basket label
    ctx.fillStyle="white";ctx.font="bold 11px sans-serif";ctx.textAlign="center";
    ctx.fillText(shield?"🛡️ AGENT":"🧺 AGENT",basket.x+basket.w/2,basket.y+15);

    // Power-up timers overlay
    if(slowActive){
        ctx.fillStyle="rgba(96,165,250,0.08)";ctx.fillRect(0,0,W,H);
        ctx.fillStyle="rgba(96,165,250,0.6)";ctx.font="bold 12px sans-serif";
        ctx.textAlign="center";ctx.fillText("⏰ SLOW MOTION",W/2,20);
    }
    if(doubleActive){
        ctx.fillStyle="rgba(52,211,153,0.5)";ctx.font="bold 12px sans-serif";
        ctx.textAlign="center";ctx.fillText("💎 2x POINTS",W/2,doubleActive&&slowActive?36:20);
    }

    // Game over
    if(!running&&lives<=0){
        ctx.fillStyle="rgba(0,0,0,0.8)";ctx.fillRect(0,0,W,H);
        ctx.fillStyle="#ef4444";ctx.font="bold 30px sans-serif";ctx.textAlign="center";
        ctx.fillText("💀 GAME OVER",W/2,H/2-50);
        ctx.fillStyle="white";ctx.font="18px sans-serif";
        ctx.fillText("Score: "+score,W/2,H/2-10);
        ctx.fillText("Level: "+level+" | Caught: "+caught,W/2,H/2+25);
        ctx.fillStyle="#a5b4fc";ctx.font="13px sans-serif";
        ctx.fillText("Kyber & Dilithium = Quantum Safe!",W/2,H/2+60);
    }
}

// Idle screen
const ibg=ctx.createLinearGradient(0,0,0,H);
ibg.addColorStop(0,"#0f0c29");ibg.addColorStop(1,"#1e1b4b");
ctx.fillStyle=ibg;ctx.fillRect(0,0,W,H);
stars.forEach(s=>{ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fillStyle="rgba(255,255,255,0.4)";ctx.fill();});
ctx.fillStyle="#a5b4fc";ctx.font="bold 22px sans-serif";ctx.textAlign="center";
ctx.fillText("🧱 Quantum Lock Drop",W/2,H/2-70);
ctx.fillStyle="#6b7280";ctx.font="13px sans-serif";
ctx.fillText("Catch quantum-safe blocks!",W/2,H/2-35);
ctx.fillText("Avoid broken crypto!",W/2,H/2-10);
ctx.fillText("Grab power-ups for shields and slow motion!",W/2,H/2+20);
ctx.fillStyle="#4f46e5";ctx.font="bold 15px sans-serif";
ctx.fillText("Press ▶ Start to play!",W/2,H/2+60);
</script>
</body>
</html>
""", height=700)

def render_lattice_maze():
    """6-8: Enhanced Lattice Maze with better graphics, enemies, levels and PQC content."""
    st.subheader("🌀 Lattice Maze Escape — Enhanced!")
    st.markdown(
        "Navigate the **quantum lattice grid** to collect all Kyber Keys! "
        "Avoid quantum attackers. Arrow keys or WASD to move. "
        "Each level gets harder — boss enemies appear on level 3+!"
    )

    with st.expander("📚 Why Lattice Math?", expanded=False):
        st.info(
            "A lattice is a regular grid of points in space. "
            "The hard problem: given a noisy point near the grid, find the CLOSEST grid point. "
            "In 1000 dimensions this stumps quantum computers — that is why Kyber is safe! "
            "This maze represents navigating a 2D lattice to find the Kyber keys (solutions)."
        )

    import streamlit.components.v1 as components_lm
    components_lm.html("""
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0f172a;font-family:sans-serif;color:white;}
#lm-wrap{display:flex;flex-direction:column;align-items:center;padding:10px;}
.lm-hud{display:flex;justify-content:space-between;width:460px;margin-bottom:8px;gap:5px;}
.hud-box{background:#1e293b;border:1px solid #334155;border-radius:8px;
padding:5px 8px;font-size:12px;font-weight:bold;color:#a5b4fc;flex:1;text-align:center;}
#mazeCanvas{border:2px solid #4f46e5;border-radius:12px;display:block;}
.lm-btns{display:flex;gap:6px;margin:8px 0;flex-wrap:wrap;justify-content:center;}
.lm-btn{padding:8px 16px;border-radius:8px;border:none;cursor:pointer;
font-size:13px;font-weight:bold;background:#4f46e5;color:white;}
.lm-btn:active{background:#3730a3;}
#lm-msg{font-size:12px;color:#34d399;min-height:18px;margin:4px;text-align:center;}
#lm-fact{background:rgba(79,70,229,0.15);border:1px solid rgba(79,70,229,0.4);
border-radius:8px;padding:6px 12px;margin:4px;font-size:11px;color:#a5b4fc;
max-width:460px;display:none;text-align:center;}
.dir-pad{display:grid;grid-template-columns:repeat(3,40px);gap:4px;margin:4px;}
.dir-btn{width:40px;height:40px;border-radius:8px;border:none;cursor:pointer;
background:#1e293b;color:#a5b4fc;font-size:16px;font-weight:bold;
border:1px solid #334155;}
.dir-btn:active{background:#4f46e5;color:white;}
</style>
</head>
<body>
<div id="lm-wrap">
    <div class="lm-hud">
        <div class="hud-box">❤️ Lives<br><span id="mlives">3</span></div>
        <div class="hud-box">🔑 Keys<br><span id="mkeys">0</span>/<span id="mtotal">3</span></div>
        <div class="hud-box">⭐ Score<br><span id="mscore">0</span></div>
        <div class="hud-box">🌊 Level<br><span id="mlevel">1</span></div>
        <div class="hud-box">👾 Enemies<br><span id="menemies">0</span></div>
    </div>
    <canvas id="mazeCanvas" width="460" height="420"></canvas>
    <div id="lm-msg">Press Start to play!</div>
    <div id="lm-fact"></div>
    <div class="lm-btns">
        <button class="lm-btn" style="background:#10b981" onclick="startMaze()">▶ Start</button>
        <button class="lm-btn" style="background:#4f46e5" onclick="nextLevel()" id="next-btn" disabled>Next Level →</button>
    </div>
    <div class="dir-pad">
        <div></div>
        <button class="dir-btn" onclick="move(0,-1)">▲</button>
        <div></div>
        <button class="dir-btn" onclick="move(-1,0)">◀</button>
        <button class="dir-btn" onclick="startMaze()">⟳</button>
        <button class="dir-btn" onclick="move(1,0)">▶</button>
        <div></div>
        <button class="dir-btn" onclick="move(0,1)">▼</button>
        <div></div>
    </div>
</div>
<script>
const mc = document.getElementById("mazeCanvas");
const mx = mc.getContext("2d");
const CELL = 40, COLS = 11, ROWS = 10;

const KEY_FACTS = [
    {item:"🔐", name:"Kyber Key",    fact:"ML-KEM FIPS 203 — Quantum-safe key encapsulation!",     color:"#10b981", pts:50},
    {item:"✍️", name:"Dilithium",    fact:"ML-DSA FIPS 204 — Quantum-safe digital signatures!",    color:"#3b82f6", pts:75},
    {item:"🌲", name:"SPHINCS+",     fact:"SLH-DSA FIPS 205 — Hash-based backup signature!",       color:"#8b5cf6", pts:100},
    {item:"🦅", name:"Falcon",       fact:"FN-DSA FIPS 206 — Smallest quantum-safe signature!",    color:"#f59e0b", pts:125},
    {item:"🧮", name:"LWE Crystal",  fact:"Learning With Errors — The hardest PQC math problem!",  color:"#ec4899", pts:150},
];

const ENEMY_TYPES = [
    {emoji:"☠️", name:"Shor",   spd:1, color:"#ef4444", fact:"Shor Algorithm breaks RSA!",      boss:false},
    {emoji:"🌀", name:"Grover", spd:2, color:"#f97316", fact:"Grover speeds up brute force!",    boss:false},
    {emoji:"👾", name:"HHL",    spd:1, color:"#a855f7", fact:"HHL attacks linear algebra!",      boss:false},
    {emoji:"💀", name:"Q-BOSS", spd:1, color:"#dc2626", fact:"Full quantum computer attack!",    boss:true},
];

const MAZES = [
    // Level 1 - Very Simple
    [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,0,1,1,1,0,1],
        [1,0,1,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,0,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,1,1,0,1],
        [1,1,1,1,1,1,1,1,1,1,1],
    ],
    // Level 2 - Simple
    [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,0,0,0,0,0,1],
        [1,0,1,0,1,0,1,1,1,0,1],
        [1,0,1,0,0,0,0,0,1,0,1],
        [1,0,1,1,1,1,1,0,1,0,1],
        [1,0,0,0,0,0,1,0,0,0,1],
        [1,1,1,1,0,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,1,1,0,1],
        [1,1,1,1,1,1,1,1,1,1,1],
    ],
    // Level 3 - Easy with 2 enemies
    [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1,0,0,0,1],
        [1,0,1,1,1,0,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,1,1,1,0,1],
        [1,0,0,0,1,0,0,0,0,0,1],
        [1,1,1,0,1,0,1,1,1,1,1],
        [1,0,0,0,0,0,1,0,0,0,1],
        [1,0,1,1,1,1,1,0,1,0,1],
        [1,1,1,1,1,1,1,1,1,1,1],
    ],
    // Level 4 - Medium
    [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,0,0,0,1,0,1],
        [1,1,1,0,1,0,1,0,1,0,1],
        [1,0,0,0,0,0,1,0,0,0,1],
        [1,0,1,1,1,0,1,1,1,0,1],
        [1,0,0,0,1,0,0,0,1,0,1],
        [1,1,1,0,1,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,1,1,0,1],
        [1,1,1,1,1,1,1,1,1,1,1],
    ],
    // Level 5 - Medium with boss
    [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,0,0,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,0,0,1,0,0,0,1],
        [1,0,1,1,1,0,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,1,0,1],
        [1,1,1,1,0,1,0,0,1,0,1],
        [1,0,0,0,0,1,0,1,0,0,1],
        [1,0,1,1,0,0,0,1,1,0,1],
        [1,1,1,1,1,1,1,1,1,1,1],
    ],
    // Level 6 - Hard
    [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,1,0,0,0,1,0,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,1],
        [1,0,0,0,1,0,0,0,1,0,1],
        [1,1,1,0,1,1,1,0,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,0,1,1,1,0,1],
        [1,0,0,0,1,0,0,0,1,0,1],
        [1,1,1,0,1,1,1,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1],
    ],
    // Level 7 - Hard with 3 enemies
    [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,0,1,0,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,1,0,1],
        [1,0,1,1,1,1,1,0,1,0,1],
        [1,0,0,0,0,0,1,0,0,0,1],
        [1,1,0,1,0,0,1,1,1,0,1],
        [1,0,0,1,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,0,1],
        [1,1,1,1,1,1,1,1,1,1,1],
    ],
    // Level 8 - Expert
    [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,1,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,1,0,1,0,1],
        [1,0,0,0,1,0,0,0,0,0,1],
        [1,1,1,0,1,0,1,1,1,1,1],
        [1,0,0,0,0,0,1,0,0,0,1],
        [1,0,1,1,1,0,1,0,1,0,1],
        [1,0,0,0,1,0,0,0,1,0,1],
        [1,1,1,0,1,1,1,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1],
    ],
    // Level 9 - Expert with boss
    [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,0,0,0,0,0,1],
        [1,1,1,0,1,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,1,1,1,0,1,0,1],
        [1,0,1,0,0,0,1,0,0,0,1],
        [1,0,1,0,1,0,1,1,1,0,1],
        [1,0,0,0,1,0,0,0,0,0,1],
        [1,1,1,0,1,1,1,1,1,0,1],
        [1,1,1,1,1,1,1,1,1,1,1],
    ],
    // Level 10 - Master
    [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,0,1,0,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,0,1],
        [1,0,0,1,0,0,0,1,0,0,1],
        [1,1,0,1,1,1,0,1,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1],
    ],
    // Level 11 - Master with 4 enemies
    [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,1,0,1,0,1],
        [1,0,0,0,1,0,1,0,0,0,1],
        [1,1,0,0,1,0,1,0,0,1,1],
        [1,0,0,1,0,0,0,1,0,0,1],
        [1,0,0,1,1,1,0,1,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1],
    ],
    // Level 12 - Grandmaster boss
    [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,1,0,0,0,1,0,0,1],
        [1,0,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,0,1,1,1,0,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1],
    ],
];

let player, enemies, keys, score, lives, level, running, collected, maze, animFrame;
let particles = [];

function showFact(fact, color) {
    const f = document.getElementById("lm-fact");
    f.textContent = "📚 " + fact;
    f.style.display = "block";
    f.style.borderColor = color + "60";
    clearTimeout(window._ft);
    window._ft = setTimeout(()=>{f.style.display="none";}, 4000);
}

function showMsg(msg) { document.getElementById("lm-msg").textContent = msg; }

function updateHUD() {
    document.getElementById("mlives").textContent = "❤️".repeat(Math.max(0,lives));
    document.getElementById("mkeys").textContent = collected;
    document.getElementById("mtotal").textContent = keys.length;
    document.getElementById("mscore").textContent = score;
    document.getElementById("mlevel").textContent = level;
    document.getElementById("menemies").textContent = enemies.length;
}

function startMaze() {
    level = 1;
    score = 0;
    lives = 3;
    document.getElementById("next-btn").disabled = true;
    loadLevel();
}

function loadLevel() {
    const mIdx = Math.min(level-1, MAZES.length-1);
    maze = MAZES[mIdx].map(r=>[...r]);
    player = {x:1, y:1};
    enemies = [];
    particles = [];
    collected = 0;

    // Place keys based on level — more keys at higher levels
    const keyCount = Math.min(3 + Math.floor(level/2), 7);
    keys = [];
    const keyTypes = KEY_FACTS.slice(0, Math.min(level+1, KEY_FACTS.length));
    const positions = [{x:8,y:1},{x:5,y:3},{x:8,y:7},{x:3,y:7},{x:9,y:5}];
    for(let i=0;i<Math.min(keyCount,positions.length);i++){
        const kType = keyTypes[i % keyTypes.length];
        keys.push({...positions[i], collected:false, ...kType});
    }

    // Spawn enemies based on level (more per level)
    const enemyCount = Math.min(1 + Math.floor(level/2), 5);
    const hasBoss = level >= 3 && level % 2 === 1;
    for(let i=0;i<enemyCount;i++){
        const eType = i===0 && hasBoss ? ENEMY_TYPES[3] : ENEMY_TYPES[Math.floor(Math.random()*3)];
        enemies.push({
            x: 9, y: 7-i*2,
            type: eType,
            timer: 0,
            rate: eType.boss ? 60 : 30+Math.floor(Math.random()*30),
            stunned: 0,
        });
    }

    running = true;
    updateHUD();
    showMsg("Level " + level + "! Collect all " + keys.length + " keys!");
    cancelAnimationFrame(animFrame);
    gameLoop();
}

function nextLevel() {
    level++;
    document.getElementById("next-btn").disabled = true;
    loadLevel();
}

function canMove(x, y) {
    if(x<0||y<0||x>=COLS||y>=ROWS) return false;
    return maze[y][x] === 0;
}

function move(dx, dy) {
    if(!running) return;
    const nx = player.x+dx, ny = player.y+dy;
    if(canMove(nx,ny)) {
        player.x=nx; player.y=ny;
        checkCollect();
        checkEnemy();
    }
}

document.addEventListener("keydown", e=>{
    if(e.key==="ArrowUp"||e.key==="w")    {e.preventDefault();move(0,-1);}
    if(e.key==="ArrowDown"||e.key==="s")  {e.preventDefault();move(0,1);}
    if(e.key==="ArrowLeft"||e.key==="a")  move(-1,0);
    if(e.key==="ArrowRight"||e.key==="d") move(1,0);
});

function checkCollect() {
    keys.forEach(k=>{
        if(!k.collected && k.x===player.x && k.y===player.y) {
            k.collected=true; collected++; score+=k.pts;
            showFact(k.fact, k.color);
            showMsg("Collected " + k.name + "! +" + k.pts + " pts");
            // Sparkle particles
            for(let i=0;i<10;i++) particles.push({
                x:k.x*CELL+CELL/2, y:k.y*CELL+CELL/2,
                vx:(Math.random()-0.5)*5, vy:(Math.random()-0.5)*5,
                color:k.color, alpha:1, r:3
            });
            updateHUD();
            if(collected===keys.length) {
                running=false;
                showMsg("🎉 Level " + level + " complete! Score: " + score);
                document.getElementById("next-btn").disabled = level >= 12;
                if(level>=12) showMsg("🏆 GRANDMASTER! All 12 levels complete! Score: " + score);
                else if(level>=9) showMsg("🔥 Expert level! Score: " + score);
            }
        }
    });
}

function checkEnemy() {
    enemies.forEach((e,i)=>{
        if(e.x===player.x&&e.y===player.y) {
            lives--;
            player={x:1,y:1};
            showMsg("💀 " + e.type.name + " caught you! " + e.type.fact);
            showFact(e.type.fact, e.type.color);
            updateHUD();
            if(lives<=0){running=false;showMsg("☠️ Game Over! Score: "+score);}
        }
    });
}

function moveEnemies() {
    if(!running) return;
    enemies.forEach(e=>{
        e.timer++;
        if(e.timer < e.rate) return;
        e.timer=0;
        if(e.stunned>0){e.stunned--;return;}

        const dirs=[{dx:0,dy:-1},{dx:0,dy:1},{dx:-1,dy:0},{dx:1,dy:0}];
        const valid=dirs.filter(d=>canMove(e.x+d.dx,e.y+d.dy));
        if(valid.length===0) return;

        // Smart pathfinding toward player
        valid.sort((a,b)=>{
            const da=Math.abs((e.x+a.dx)-player.x)+Math.abs((e.y+a.dy)-player.y);
            const db=Math.abs((e.x+b.dx)-player.x)+Math.abs((e.y+b.dy)-player.y);
            return da-db;
        });

        // Boss always goes toward player, others sometimes random
        const move2 = e.type.boss||Math.random()<0.7 ? valid[0] : valid[Math.floor(Math.random()*valid.length)];
        e.x+=move2.dx; e.y+=move2.dy;
        checkEnemy();
    });
}

function gameLoop() {
    animFrame=requestAnimationFrame(gameLoop);

    // Move enemies periodically
    moveEnemies();

    // Update particles
    particles=particles.filter(p=>{
        p.x+=p.vx; p.y+=p.vy; p.alpha-=0.04;
        p.vx*=0.95; p.vy*=0.95;
        return p.alpha>0;
    });

    draw();
}

function draw() {
    mx.clearRect(0,0,mc.width,mc.height);

    // Background gradient
    const bg=mx.createLinearGradient(0,0,0,mc.height);
    bg.addColorStop(0,"#0f0c29");
    bg.addColorStop(1,"#1e1b4b");
    mx.fillStyle=bg;
    mx.fillRect(0,0,mc.width,mc.height);

    // Draw maze
    for(let r=0;r<ROWS;r++){
        for(let c=0;c<COLS;c++){
            if(maze[r][c]===1){
                // Wall with gradient
                const wg=mx.createLinearGradient(c*CELL,r*CELL,(c+1)*CELL,(r+1)*CELL);
                wg.addColorStop(0,"#1e1b4b");
                wg.addColorStop(1,"#0f172a");
                mx.fillStyle=wg;
                mx.fillRect(c*CELL,r*CELL,CELL,CELL);
                // Wall border glow
                mx.strokeStyle="rgba(79,70,229,0.4)";
                mx.lineWidth=1;
                mx.strokeRect(c*CELL,r*CELL,CELL,CELL);
            } else {
                mx.fillStyle="rgba(15,23,42,0.8)";
                mx.fillRect(c*CELL,r*CELL,CELL,CELL);
                mx.strokeStyle="rgba(79,70,229,0.1)";
                mx.lineWidth=0.5;
                mx.strokeRect(c*CELL,r*CELL,CELL,CELL);
            }
        }
    }

    // Draw lattice dots on open cells
    for(let r=0;r<ROWS;r++){
        for(let c=0;c<COLS;c++){
            if(maze[r][c]===0){
                mx.beginPath();
                mx.arc(c*CELL+CELL/2,r*CELL+CELL/2,2,0,Math.PI*2);
                mx.fillStyle="rgba(79,70,229,0.3)";
                mx.fill();
            }
        }
    }

    // Draw keys with glow
    keys.forEach(k=>{
        if(k.collected) return;
        // Glow
        mx.beginPath();
        mx.arc(k.x*CELL+CELL/2,k.y*CELL+CELL/2,18,0,Math.PI*2);
        mx.fillStyle=k.color+"22";
        mx.fill();
        // Key emoji
        mx.font="22px sans-serif";
        mx.textAlign="center";
        mx.fillText(k.item,k.x*CELL+CELL/2,k.y*CELL+CELL/1.4);
        // Label
        mx.font="7px sans-serif";
        mx.fillStyle=k.color;
        mx.fillText(k.name,k.x*CELL+CELL/2,k.y*CELL+CELL-4);
    });

    // Draw particles
    particles.forEach(p=>{
        mx.beginPath();
        mx.arc(p.x,p.y,p.r,0,Math.PI*2);
        mx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,"0");
        mx.fill();
    });

    // Draw enemies
    enemies.forEach(e=>{
        const size = e.type.boss ? 28 : 22;
        // Boss pulse effect
        if(e.type.boss){
            mx.beginPath();
            mx.arc(e.x*CELL+CELL/2,e.y*CELL+CELL/2,20+Math.sin(Date.now()*0.005)*4,0,Math.PI*2);
            mx.fillStyle="rgba(220,38,38,0.2)";
            mx.fill();
        }
        mx.font=size+"px sans-serif";
        mx.textAlign="center";
        mx.fillText(e.type.emoji,e.x*CELL+CELL/2,e.y*CELL+CELL/1.3);
        // Enemy label
        mx.font="7px sans-serif";
        mx.fillStyle=e.type.color;
        mx.fillText(e.type.name,e.x*CELL+CELL/2,e.y*CELL+2);
    });

    // Draw player with glow
    mx.beginPath();
    mx.arc(player.x*CELL+CELL/2,player.y*CELL+CELL/2,16,0,Math.PI*2);
    mx.fillStyle="rgba(16,185,129,0.2)";
    mx.fill();
    mx.font="24px sans-serif";
    mx.textAlign="center";
    mx.fillText("🕵️",player.x*CELL+CELL/2,player.y*CELL+CELL/1.35);

    // Player highlight
    mx.strokeStyle="#10b981";
    mx.lineWidth=2;
    mx.strokeRect(player.x*CELL+2,player.y*CELL+2,CELL-4,CELL-4);

    // Game over overlay
    if(!running&&lives<=0){
        mx.fillStyle="rgba(0,0,0,0.8)";
        mx.fillRect(0,0,mc.width,mc.height);
        mx.fillStyle="#ef4444";
        mx.font="bold 28px sans-serif";
        mx.textAlign="center";
        mx.fillText("☠️ QUANTUM WIN!",mc.width/2,mc.height/2-30);
        mx.fillStyle="white";
        mx.font="16px sans-serif";
        mx.fillText("Score: "+score,mc.width/2,mc.height/2+10);
        mx.fillStyle="#a5b4fc";
        mx.font="12px sans-serif";
        mx.fillText("Kyber lattice math beats quantum attackers!",mc.width/2,mc.height/2+40);
    }

    // Win overlay
    if(!running&&lives>0&&collected===keys.length){
        mx.fillStyle="rgba(0,0,0,0.7)";
        mx.fillRect(0,0,mc.width,mc.height);
        mx.fillStyle="#10b981";
        mx.font="bold 26px sans-serif";
        mx.textAlign="center";
        mx.fillText("🎉 LEVEL "+level+" COMPLETE!",mc.width/2,mc.height/2-30);
        mx.fillStyle="white";
        mx.font="15px sans-serif";
        mx.fillText("Score: "+score,mc.width/2,mc.height/2+10);
        if(level<3){
            mx.fillStyle="#a5b4fc";
            mx.font="13px sans-serif";
            mx.fillText("Press Next Level →",mc.width/2,mc.height/2+40);
        }
    }
}

// Idle screen
mx.fillStyle="#0f0c29";
mx.fillRect(0,0,mc.width,mc.height);
mx.fillStyle="#a5b4fc";
mx.font="bold 20px sans-serif";
mx.textAlign="center";
mx.fillText("🌀 Lattice Maze Escape",mc.width/2,mc.height/2-50);
mx.fillStyle="#6b7280";
mx.font="13px sans-serif";
mx.fillText("Collect Kyber keys, avoid quantum attackers",mc.width/2,mc.height/2-15);
mx.fillText("3 levels with increasing difficulty!",mc.width/2,mc.height/2+15);
mx.fillStyle="#4f46e5";
mx.font="bold 14px sans-serif";
mx.fillText("Press ▶ Start to play!",mc.width/2,mc.height/2+50);
</script>
</body>
</html>
""", height=680)

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

// 12 defined wave configurations
const WAVE_DEFS = [
    {wave:1,  name:"First Contact",     enemies:[0,0,0,1],        count:4,  boss:false, bonusBits:60,  desc:"Easy intro wave!"},
    {wave:2,  name:"Quantum Scouts",    enemies:[0,0,1,1,2],      count:5,  boss:false, bonusBits:70,  desc:"More enemies!"},
    {wave:3,  name:"BOSS Wave 1",       enemies:[0,1,2,3],        count:5,  boss:true,  bonusBits:100, desc:"First boss!"},
    {wave:4,  name:"Shor Surge",        enemies:[0,0,0,1,1,2],    count:6,  boss:false, bonusBits:80,  desc:"Faster Shor attacks!"},
    {wave:5,  name:"Grover Storm",      enemies:[1,1,1,2,3],      count:7,  boss:false, bonusBits:90,  desc:"Grover speeders!"},
    {wave:6,  name:"BOSS Wave 2",       enemies:[0,1,2,3,0],      count:7,  boss:true,  bonusBits:120, desc:"Stronger boss!"},
    {wave:7,  name:"Quantum Flood",     enemies:[0,1,2,3,0,1],    count:8,  boss:false, bonusBits:100, desc:"Mixed attack!"},
    {wave:8,  name:"QAOA Assault",      enemies:[3,3,3,0,1,2,3],  count:9,  boss:false, bonusBits:110, desc:"QAOA everywhere!"},
    {wave:9,  name:"BOSS Wave 3",       enemies:[0,1,2,3,0,1],    count:9,  boss:true,  bonusBits:150, desc:"Mega boss!"},
    {wave:10, name:"Full Quantum Army", enemies:[0,1,2,3,0,1,2,3],count:10, boss:false, bonusBits:120, desc:"All enemy types!"},
    {wave:11, name:"Quantum Apocalypse",enemies:[0,1,2,3,3,0,1,2],count:12, boss:true,  bonusBits:180, desc:"Almost impossible!"},
    {wave:12, name:"FINAL BOSS",        enemies:[0,1,2,3,0,1,2,3],count:14, boss:true,  bonusBits:300, desc:"The quantum computer!"},
];

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
    if (wave >= 12) { showMsg("🏆 All 12 waves complete! You are a Quantum Guardian!"); return; }
    wave++;
    waveRunning=true;
    spawnQ=[];

    const wdef = WAVE_DEFS[Math.min(wave-1, WAVE_DEFS.length-1)];
    const hpBoost = 1+(wave-1)*0.2;

    showMsg("🌊 Wave "+wave+"/12: "+wdef.name+" — "+wdef.desc);

    if (wdef.boss) {
        // Add boss at start
        const boss = {...ENEMY_TYPES[4]};
        boss.hp = Math.floor(boss.hp * hpBoost);
        boss.maxHp = boss.hp;
        spawnQ.push({...boss, delay:0});
    }

    // Add regular enemies
    for(let i=0;i<wdef.count;i++){
        const eIdx = wdef.enemies[i % wdef.enemies.length];
        const eType = ENEMY_TYPES[Math.min(eIdx, ENEMY_TYPES.length-2)];
        const boosted = {...eType,
            hp:Math.floor(eType.hp*hpBoost),
            maxHp:Math.floor(eType.hp*hpBoost),
            delay:(i+1)*45
        };
        spawnQ.push(boosted);
    }

    document.getElementById("wave").textContent=wave+"/12";
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
        const wdef = WAVE_DEFS[Math.min(wave-1, WAVE_DEFS.length-1)];
        const bonus = wdef.bonusBits;
        bits+=bonus;
        updateUI();
        if(wave>=12){
            showMsg("🏆 ALL 12 WAVES CLEARED! Quantum Guardian! Score: "+score);
        } else {
            showMsg("✅ Wave "+wave+"/12 cleared! +"+bonus+" bits. Next: "+WAVE_DEFS[wave].name);
        }
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
    """Quantum Zombie Blast — clean redesign with better UI and gameplay."""
    diff = {
        "easy":   {"speed": 1.2, "rate": 100, "hp": 30,  "label": "🟢 Recruit",     "waves": 5},
        "medium": {"speed": 1.8, "rate": 75,  "hp": 55,  "label": "🟡 Code Cadet",  "waves": 8},
        "hard":   {"speed": 2.8, "rate": 50,  "hp": 90,  "label": "🔴 Cipher Corps", "waves": 12},
    }.get(difficulty, {"speed": 1.2, "rate": 100, "hp": 30, "label": "🟢 Recruit", "waves": 5})

    st.subheader("🧟 Quantum Zombie Blast!")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"🎯 Difficulty: **{diff['label']}**")
    with col2:
        st.info("🔫 SPACE or Fire button to shoot")
    with col3:
        st.info("← → Arrow keys or buttons to move")

    import streamlit.components.v1 as components_zb
    components_zb.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#0f172a;font-family:sans-serif;color:white;}}
#zb-wrap{{display:flex;flex-direction:column;align-items:center;padding:10px;}}
.zb-hud{{display:flex;justify-content:space-between;width:500px;margin-bottom:8px;gap:6px;}}
.hud-box{{background:#1e293b;border:1px solid #334155;border-radius:8px;
padding:5px 10px;font-size:12px;font-weight:bold;color:#a5b4fc;flex:1;text-align:center;}}
#zbCanvas{{border:2px solid #4f46e5;border-radius:12px;display:block;}}
.weapon-bar{{display:flex;gap:5px;margin:8px 0;flex-wrap:wrap;justify-content:center;}}
.wbtn{{padding:6px 10px;border-radius:8px;border:2px solid transparent;
cursor:pointer;font-size:11px;font-weight:bold;color:white;transition:all 0.15s;}}
.wbtn.active{{border-color:white;transform:scale(1.08);}}
.ctrl-bar{{display:flex;gap:6px;margin:4px 0;justify-content:center;}}
.cbtn{{padding:8px 18px;border-radius:8px;border:none;cursor:pointer;
font-size:13px;font-weight:bold;background:#4f46e5;color:white;}}
.cbtn:active{{background:#3730a3;}}
#zb-msg{{font-size:12px;color:#34d399;min-height:18px;margin:4px;
text-align:center;max-width:500px;}}
#zb-fact{{background:rgba(79,70,229,0.15);border:1px solid rgba(79,70,229,0.4);
border-radius:8px;padding:6px 12px;margin:4px;font-size:11px;color:#a5b4fc;
max-width:500px;display:none;text-align:center;}}
</style>
</head>
<body>
<div id="zb-wrap">
    <div class="zb-hud">
        <div class="hud-box">❤️ HP<br><span id="zhp">100</span></div>
        <div class="hud-box">⭐ Score<br><span id="zscore">0</span></div>
        <div class="hud-box">🌊 Wave<br><span id="zwave">1</span></div>
        <div class="hud-box">🧟 Left<br><span id="zleft">0</span></div>
        <div class="hud-box">🎯 Killed<br><span id="zkilled">0</span></div>
    </div>
    <canvas id="zbCanvas" width="500" height="460"></canvas>
    <div id="zb-msg">Press Start to play!</div>
    <div id="zb-fact"></div>
    <div class="weapon-bar">
        <button class="wbtn active" id="w0" style="background:#10b981" onclick="selW(0)">🔐 Kyber</button>
        <button class="wbtn" id="w1" style="background:#3b82f6" onclick="selW(1)">✍️ Dilithium</button>
        <button class="wbtn" id="w2" style="background:#8b5cf6" onclick="selW(2)">🌲 SPHINCS+</button>
        <button class="wbtn" id="w3" style="background:#ef4444" onclick="selW(3)">⚡ LWE Bomb</button>
    </div>
    <div class="ctrl-bar">
        <button class="cbtn" onclick="moveL()">◀</button>
        <button class="cbtn" style="background:#10b981" onclick="startGame()">▶ Start</button>
        <button class="cbtn" style="background:#ef4444" onclick="fire()">🔫 Fire</button>
        <button class="cbtn" onclick="moveR()">▶</button>
    </div>
</div>
<script>
const W=500, H=460;
const zc = document.getElementById("zbCanvas");
const zx = zc.getContext("2d");

const WEAPONS = [
    {{name:"Kyber Blaster",   emoji:"🔐", color:"#10b981", dmg:30,  spd:9, spread:1, area:0,  fact:"ML-KEM FIPS 203 — Quantum-safe key encapsulation!"}},
    {{name:"Dilithium Cannon",emoji:"✍️", color:"#3b82f6", dmg:70,  spd:6, spread:1, area:0,  fact:"ML-DSA FIPS 204 — Quantum-safe digital signatures!"}},
    {{name:"SPHINCS Shotgun", emoji:"🌲", color:"#8b5cf6", dmg:25,  spd:8, spread:3, area:0,  fact:"SLH-DSA FIPS 205 — Hash-based backup standard!"}},
    {{name:"LWE Bomb",        emoji:"⚡", color:"#ef4444", dmg:150, spd:5, spread:1, area:70, fact:"Learning With Errors — The hardest quantum math!"}},
];

const ZOMBIES = [
    {{label:"RSA☠️",   emoji:"🧟",   color:"#ef4444", hp:{diff['hp']},      pts:10, fact:"RSA is broken by Shor's Algorithm!"}},
    {{label:"ECC💀",   emoji:"🧟‍♀️",  color:"#f97316", hp:{int(diff['hp']*0.7)}, pts:15, fact:"ECC is also broken by Shor's Algorithm!"}},
    {{label:"DES⚠️",  emoji:"🧟‍♂️",  color:"#eab308", hp:{int(diff['hp']*0.5)}, pts:20, fact:"DES was classically broken in 1999!"}},
    {{label:"MD5💥",   emoji:"🧟",   color:"#ec4899", hp:{int(diff['hp']*0.6)}, pts:18, fact:"MD5 has dangerous collision attacks!"}},
];

const BASE_SPEED = {diff['speed']};
const BASE_RATE = {diff['rate']};
const MAX_WAVES = 12;

// 12 wave configs
const WAVE_CONFIG = [
    {{wave:1,  speed:BASE_SPEED*0.7, rate:Math.floor(BASE_RATE*1.4), count:4,  boss:false, name:"First Wave"}},
    {{wave:2,  speed:BASE_SPEED*0.8, rate:Math.floor(BASE_RATE*1.3), count:5,  boss:false, name:"Getting Warmer"}},
    {{wave:3,  speed:BASE_SPEED*0.9, rate:Math.floor(BASE_RATE*1.2), count:6,  boss:true,  name:"Boss Wave!"}},
    {{wave:4,  speed:BASE_SPEED*1.0, rate:Math.floor(BASE_RATE*1.1), count:7,  boss:false, name:"Speed Up"}},
    {{wave:5,  speed:BASE_SPEED*1.1, rate:Math.floor(BASE_RATE*1.0), count:8,  boss:false, name:"Halfway There"}},
    {{wave:6,  speed:BASE_SPEED*1.2, rate:Math.floor(BASE_RATE*0.9), count:9,  boss:true,  name:"Boss Strikes!"}},
    {{wave:7,  speed:BASE_SPEED*1.3, rate:Math.floor(BASE_RATE*0.85),count:10, boss:false, name:"Expert Territory"}},
    {{wave:8,  speed:BASE_SPEED*1.4, rate:Math.floor(BASE_RATE*0.8), count:11, boss:false, name:"Quantum Surge"}},
    {{wave:9,  speed:BASE_SPEED*1.5, rate:Math.floor(BASE_RATE*0.75),count:12, boss:true,  name:"Super Boss!"}},
    {{wave:10, speed:BASE_SPEED*1.6, rate:Math.floor(BASE_RATE*0.7), count:14, boss:false, name:"Almost There"}},
    {{wave:11, speed:BASE_SPEED*1.7, rate:Math.floor(BASE_RATE*0.65),count:16, boss:true,  name:"Final Boss!"}},
    {{wave:12, speed:BASE_SPEED*1.8, rate:Math.floor(BASE_RATE*0.6), count:18, boss:true,  name:"QUANTUM APOCALYPSE!"}},
];

function getWaveConfig() {{
    return WAVE_CONFIG[Math.min(wave-1, WAVE_CONFIG.length-1)];
}}

let player = {{x:W/2, y:H-55, w:40, h:40, spd:6}};
let bullets=[], zombies=[], explosions=[], stars=[];
let selWeapon=0, zhp=100, score=0, wave=1, killed=0;
let running=false, frameId, spawnT=0, spawnCount=0, waveSize=0;
let keys={{}};

// Generate starfield
for(let i=0;i<60;i++) stars.push({{x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.5+0.5}});

function selW(i) {{
    selWeapon=i;
    document.querySelectorAll(".wbtn").forEach((b,j)=>b.classList.toggle("active",j===i));
    showMsg(WEAPONS[i].emoji+" "+WEAPONS[i].name+" — "+WEAPONS[i].fact);
}}

function showMsg(msg) {{ document.getElementById("zb-msg").textContent=msg; }}
function showFact(fact) {{
    const f=document.getElementById("zb-fact");
    f.textContent="📚 "+fact; f.style.display="block";
    clearTimeout(window._ft);
    window._ft=setTimeout(()=>{{f.style.display="none";}},3500);
}}

function updateHUD() {{
    document.getElementById("zhp").textContent=Math.max(0,zhp);
    document.getElementById("zscore").textContent=score;
    document.getElementById("zwave").textContent=wave;
    document.getElementById("zleft").textContent=Math.max(0,waveSize-spawnCount)+zombies.length;
    document.getElementById("zkilled").textContent=killed;
}}

function startGame() {{
    bullets=[]; zombies=[]; explosions=[];
    zhp=100; score=0; wave=1; killed=0; spawnT=0; spawnCount=0;
    waveSize=WAVE_CONFIG[0].count; running=true; player.x=W/2;
    updateHUD();
    showMsg("🧟 Wave 1 incoming! Blast the quantum zombies!");
    cancelAnimationFrame(frameId);
    loop();
}}

function moveL() {{ if(running) player.x=Math.max(25,player.x-player.spd*3); }}
function moveR() {{ if(running) player.x=Math.min(W-25,player.x+player.spd*3); }}

function fire() {{
    if(!running) return;
    const w=WEAPONS[selWeapon];
    const angles = w.spread===3 ? [-0.3,0,0.3] : [0];
    angles.forEach(angle=>{{
        const spd_x = Math.sin(angle)*w.spd;
        bullets.push({{
            x:player.x, y:player.y-20,
            vx:spd_x, vy:-w.spd,
            dmg:w.dmg, color:w.color,
            emoji:w.emoji, area:w.area,
            fact:w.fact
        }});
    }});
}}

document.addEventListener("keydown", e=>{{
    keys[e.key]=true;
    if(e.key===" "){{e.preventDefault();fire();}}
}});
document.addEventListener("keyup", e=>{{keys[e.key]=false;}});

function spawnZombie() {{
    const wcfg = getWaveConfig();
    const isBoss = wcfg.boss && zombies.length===0 && spawnCount===0;
    const z = isBoss ? ZOMBIES[ZOMBIES.length-1] : ZOMBIES[Math.floor(Math.random()*(ZOMBIES.length-1))];
    const hpBoost=1+(wave-1)*0.15;
    zombies.push({{
        x:Math.random()*(W-60)+30, y:-40,
        w:isBoss?52:38, h:isBoss?52:38,
        hp:Math.floor(z.hp*hpBoost*(isBoss?3:1)),
        maxHp:Math.floor(z.hp*hpBoost*(isBoss?3:1)),
        spd:wcfg.speed,
        wobble:Math.random()*Math.PI*2,
        label:z.label, emoji:z.emoji,
        color:z.color, pts:z.pts*wave,
        fact:z.fact
    }});
    spawnCount++;
}}

function loop() {{
    frameId=requestAnimationFrame(loop);
    if(!running) return;

    // Controls
    if(keys["ArrowLeft"]||keys["a"]) player.x=Math.max(25,player.x-player.spd);
    if(keys["ArrowRight"]||keys["d"]) player.x=Math.min(W-25,player.x+player.spd);

    // Spawn
    spawnT++;
    const effRate=Math.max(20,SPAWN_RATE-(wave-1)*5);
    if(spawnT>=effRate && spawnCount<waveSize) {{ spawnZombie(); spawnT=0; }}

    // Move bullets
    bullets=bullets.filter(b=>{{
        b.x+=b.vx; b.y+=b.vy;
        return b.y>-20 && b.x>-20 && b.x<W+20;
    }});

    // Move zombies
    zombies.forEach(z=>{{
        z.wobble+=0.06;
        z.y+=z.spd;
        z.x+=Math.sin(z.wobble)*0.6;
    }});

    // Bullet-zombie collision
    bullets=bullets.filter(b=>{{
        let hit=false;
        zombies=zombies.filter(z=>{{
            const dist=Math.hypot(b.x-z.x-z.w/2, b.y-z.y-z.h/2);
            const hitR=b.area>0?b.area:20;
            if(dist<hitR){{
                z.hp-=b.dmg;
                hit=true;
                if(z.hp<=0){{
                    score+=z.pts; killed++;
                    showFact(z.fact);
                    // Explosion
                    for(let i=0;i<8;i++) explosions.push({{
                        x:z.x+z.w/2, y:z.y+z.h/2,
                        vx:(Math.random()-0.5)*5,
                        vy:(Math.random()-0.5)*5,
                        r:4, alpha:1, color:z.color
                    }});
                    updateHUD();
                    return false;
                }}
                return true;
            }}
            return true;
        }});
        if(hit && b.area===0) showFact(b.fact);
        return b.area>0 ? false : !hit;
    }});

    // Zombie reaches player
    zombies=zombies.filter(z=>{{
        if(z.y+z.h>=player.y&&z.y<=player.y+player.h&&
           z.x+z.w>=player.x-22&&z.x<=player.x+22){{
            zhp-=8; updateHUD();
            showMsg("💀 "+z.label+" hit you! "+z.fact);
            if(zhp<=0){{ running=false; showMsg("☠️ Game Over! Score: "+score); }}
            return false;
        }}
        return true;
    }});

    // Update explosions
    explosions=explosions.filter(e=>{{
        e.x+=e.vx; e.y+=e.vy; e.alpha-=0.05; return e.alpha>0;
    }});

    // Wave complete
    if(spawnCount>=waveSize&&zombies.length===0){{
        if(wave>=MAX_WAVES){{
            running=false;
            showMsg("🏆 QUANTUM GUARDIAN! All 12 waves cleared! Score: "+score);
        }} else {{
            wave++;
            const nextCfg = getWaveConfig();
            waveSize=nextCfg.count;
            spawnCount=0; spawnT=0;
            document.getElementById("zwave").textContent=wave+"/12";
            showMsg("✅ Wave "+(wave-1)+" cleared! Wave "+wave+": "+nextCfg.name+" incoming!");
        }}
    }}

    updateHUD();
    render();
}}

function render() {{
    zx.clearRect(0,0,W,H);

    // Sky gradient
    const grad=zx.createLinearGradient(0,0,0,H);
    grad.addColorStop(0,"#0f0c29");
    grad.addColorStop(1,"#1e1b4b");
    zx.fillStyle=grad; zx.fillRect(0,0,W,H);

    // Stars
    stars.forEach(s=>{{
        zx.beginPath();
        zx.arc(s.x,s.y,s.r,0,Math.PI*2);
        zx.fillStyle="rgba(255,255,255,0.5)";
        zx.fill();
    }});

    // Ground
    zx.fillStyle="#1e1b4b";
    zx.fillRect(0,H-35,W,35);
    zx.fillStyle="#4f46e5";
    zx.fillRect(0,H-35,W,3);

    // Grid lines on ground
    zx.strokeStyle="rgba(79,70,229,0.2)";
    for(let i=0;i<W;i+=50){{
        zx.beginPath();
        zx.moveTo(i,H-35);
        zx.lineTo(i,H);
        zx.stroke();
    }}

    // Explosions
    explosions.forEach(e=>{{
        zx.beginPath();
        zx.arc(e.x,e.y,e.r,0,Math.PI*2);
        const hex=Math.floor(e.alpha*255).toString(16).padStart(2,"0");
        zx.fillStyle=e.color+hex;
        zx.fill();
    }});

    // Zombies
    zombies.forEach(z=>{{
        // Shadow
        zx.beginPath();
        zx.ellipse(z.x+z.w/2,z.y+z.h+4,z.w/2,6,0,0,Math.PI*2);
        zx.fillStyle="rgba(0,0,0,0.3)";
        zx.fill();

        // Emoji
        zx.font="28px sans-serif";
        zx.textAlign="center";
        zx.fillText(z.emoji,z.x+z.w/2,z.y+z.h);

        // Label
        zx.font="bold 9px sans-serif";
        zx.fillStyle=z.color;
        zx.fillText(z.label,z.x+z.w/2,z.y-3);

        // HP bar
        const bw=38,bh=4;
        zx.fillStyle="#374151";
        zx.fillRect(z.x+z.w/2-bw/2,z.y-12,bw,bh);
        const pct=Math.max(0,z.hp/z.maxHp);
        zx.fillStyle=pct>0.5?"#10b981":pct>0.25?"#f59e0b":"#ef4444";
        zx.fillRect(z.x+z.w/2-bw/2,z.y-12,bw*pct,bh);
    }});

    // Bullets
    bullets.forEach(b=>{{
        zx.font=(b.area>0?"20":"14")+"px sans-serif";
        zx.textAlign="center";
        zx.fillText(b.emoji,b.x,b.y+5);
        if(b.area>0){{
            zx.beginPath();
            zx.arc(b.x,b.y,b.area,0,Math.PI*2);
            zx.strokeStyle=b.color+"44";
            zx.lineWidth=2;
            zx.stroke();
        }}
    }});

    // Player
    zx.font="34px sans-serif";
    zx.textAlign="center";
    zx.fillText("🧑‍💻",player.x,player.y+12);

    // Player HP bar
    const pw=56;
    zx.fillStyle="#374151";
    zx.fillRect(player.x-pw/2,player.y+16,pw,6);
    zx.fillStyle=zhp>60?"#10b981":zhp>30?"#f59e0b":"#ef4444";
    zx.fillRect(player.x-pw/2,player.y+16,pw*(zhp/100),6);

    // Weapon HUD
    const w=WEAPONS[selWeapon];
    zx.fillStyle="rgba(15,23,42,0.8)";
    zx.beginPath();
    zx.roundRect(8,H-32,180,22,4);
    zx.fill();
    zx.fillStyle=w.color;
    zx.font="bold 11px sans-serif";
    zx.textAlign="left";
    zx.fillText(w.emoji+" "+w.name,14,H-17);

    // Wave progress bar
    const wPct=spawnCount/Math.max(1,waveSize);
    zx.fillStyle="rgba(15,23,42,0.8)";
    zx.beginPath();
    zx.roundRect(W-140,H-32,132,22,4);
    zx.fill();
    zx.fillStyle="#334155";
    zx.fillRect(W-134,H-26,120,10);
    zx.fillStyle="#4f46e5";
    zx.fillRect(W-134,H-26,120*wPct,10);
    zx.fillStyle="#a5b4fc";
    zx.font="9px sans-serif";
    zx.textAlign="left";
    zx.fillText("Wave "+wave+" progress",W-134,H-18);

    // Game over / win overlay
    if(!running&&(score>0||zhp<=0)){{
        zx.fillStyle="rgba(0,0,0,0.75)";
        zx.fillRect(0,0,W,H);
        zx.fillStyle=zhp>0?"#10b981":"#ef4444";
        zx.font="bold 30px sans-serif";
        zx.textAlign="center";
        zx.fillText(zhp>0?"🏆 YOU WIN!":"💀 GAME OVER",W/2,H/2-40);
        zx.fillStyle="white";
        zx.font="18px sans-serif";
        zx.fillText("Score: "+score+" | Killed: "+killed,W/2,H/2);
        zx.fillStyle="#a5b4fc";
        zx.font="13px sans-serif";
        zx.fillText("Kyber + Dilithium + SPHINCS+ = Quantum Safe!",W/2,H/2+40);
    }}
}}

// Idle screen
zx.fillStyle="#0f0c29";
zx.fillRect(0,0,W,H);
stars.forEach(s=>{{
    zx.beginPath();
    zx.arc(s.x,s.y,s.r,0,Math.PI*2);
    zx.fillStyle="rgba(255,255,255,0.5)";
    zx.fill();
}});
zx.fillStyle="#a5b4fc";
zx.font="bold 24px sans-serif";
zx.textAlign="center";
zx.fillText("🧟 Quantum Zombie Blast",W/2,H/2-60);
zx.fillStyle="#6b7280";
zx.font="13px sans-serif";
zx.fillText("Blast RSA, ECC and DES zombies",W/2,H/2-25);
zx.fillText("with Kyber, Dilithium, SPHINCS+ and LWE!",W/2,H/2+5);
zx.fillStyle="#4f46e5";
zx.font="bold 15px sans-serif";
zx.fillText("Press ▶ Start to play",W/2,H/2+45);
</script>
</body>
</html>
""", height=700)

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
    """6-8: Enhanced QuantumCraft Lattice Mines with better graphics, enemies, boss levels."""
    st.subheader("⛏️ QuantumCraft — Lattice Mines Enhanced!")
    st.markdown(
        "Dig deep into the **quantum lattice mines**! "
        "Mine rare PQC algorithms, avoid quantum creepers, find the ladder to go deeper. "
        "Boss enemies appear at depth 3+! WASD to move, E to mine, F to place walls."
    )

    with st.expander("📚 Mining Guide — PQC Algorithms by Depth", expanded=False):
        cols = st.columns(3)
        with cols[0]:
            st.success("**Surface (Depth 1-2)**")
            st.info("🔐 Kyber — ML-KEM FIPS 203\n✍️ Dilithium — ML-DSA FIPS 204")
        with cols[1]:
            st.warning("**Deep (Depth 3-4)**")
            st.info("🌲 SPHINCS+ — SLH-DSA FIPS 205\n🦅 Falcon — FN-DSA FIPS 206")
        with cols[2]:
            st.error("**Ultra Deep (Depth 5+)**")
            st.info("🧮 LWE Crystal — Hardest PQC math!\n💎 Quantum Core — Ultimate find!")

    import streamlit.components.v1 as components_qcm
    components_qcm.html("""
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0f172a;font-family:sans-serif;color:white;}
#qm-wrap{display:flex;flex-direction:column;align-items:center;padding:10px;}
.qm-hud{display:flex;justify-content:space-between;width:540px;margin-bottom:8px;gap:5px;}
.hud-box{background:#1e293b;border:1px solid #334155;border-radius:8px;
padding:5px 8px;font-size:11px;font-weight:bold;color:#a5b4fc;flex:1;text-align:center;}
#qmCanvas{border:2px solid #3b82f6;border-radius:12px;display:block;}
.qm-inv{display:flex;gap:5px;margin:6px 0;flex-wrap:wrap;justify-content:center;}
.inv-slot{background:#1e293b;border:1px solid #334155;border-radius:6px;
padding:3px 8px;font-size:11px;color:#a5b4fc;}
.qm-btns{display:flex;gap:5px;margin:4px 0;flex-wrap:wrap;justify-content:center;}
.qm-btn{padding:7px 12px;border-radius:8px;border:none;cursor:pointer;
font-size:12px;font-weight:bold;color:white;}
.qm-btn:active{opacity:0.8;}
#qm-msg{font-size:12px;color:#60a5fa;min-height:18px;margin:4px;text-align:center;}
#qm-fact{background:rgba(59,130,246,0.15);border:1px solid rgba(59,130,246,0.4);
border-radius:8px;padding:6px 12px;margin:4px;font-size:11px;color:#a5b4fc;
max-width:540px;display:none;text-align:center;}
</style>
</head>
<body>
<div id="qm-wrap">
    <div class="qm-hud">
        <div class="hud-box">❤️ HP<br><span id="mhp">120</span></div>
        <div class="hud-box">⭐ Score<br><span id="mscore">0</span></div>
        <div class="hud-box">⬇️ Depth<br><span id="mdepth">1</span></div>
        <div class="hud-box">💎 Rare<br><span id="mrare">0</span></div>
        <div class="hud-box">⛏️ Mined<br><span id="mmined">0</span></div>
    </div>
    <canvas id="qmCanvas" width="540" height="420"></canvas>
    <div id="qm-msg">Press Start to begin mining!</div>
    <div id="qm-fact"></div>
    <div class="qm-inv">
        <div class="inv-slot" id="m-kyber">🔐 Kyber: 0</div>
        <div class="inv-slot" id="m-dilithium">✍️ Dilithium: 0</div>
        <div class="inv-slot" id="m-sphincs">🌲 SPHINCS: 0</div>
        <div class="inv-slot" id="m-falcon">🦅 Falcon: 0</div>
        <div class="inv-slot" id="m-lwe">🧮 LWE: 0</div>
        <div class="inv-slot" id="m-qcore">💎 QCore: 0</div>
    </div>
    <div class="qm-btns">
        <button class="qm-btn" style="background:#10b981" onclick="startMines()">▶ Start</button>
        <button class="qm-btn" style="background:#3b82f6" onclick="mineMid()">⛏️ Mine (E)</button>
        <button class="qm-btn" style="background:#4f46e5" onclick="placeMid()">🧱 Place (F)</button>
        <button class="qm-btn" style="background:#f59e0b" onclick="goDeeper()">⬇️ Deeper</button>
        <button class="qm-btn" style="background:#374151" onclick="startMines()">🔄 Reset</button>
    </div>
</div>
<script>
const mc = document.getElementById("qmCanvas");
const mx = mc.getContext("2d");
const CELL=40, COLS=13, ROWS=10;

const BLOCKS = {
    empty:     {color:"#0f172a",    label:"",  solid:false, mineable:false},
    stone:     {color:"#374151",    label:"🪨", solid:true,  mineable:true,  item:null,       pts:2,  rare:false},
    kyber:     {color:"#10b981",    label:"K",  solid:true,  mineable:true,  item:"kyber",    pts:20, rare:false,
                fact:"ML-KEM FIPS 203 — NIST standard key encapsulation!"},
    dilithium: {color:"#3b82f6",    label:"D",  solid:true,  mineable:true,  item:"dilithium",pts:30, rare:false,
                fact:"ML-DSA FIPS 204 — Quantum-safe digital signatures!"},
    sphincs:   {color:"#8b5cf6",    label:"S",  solid:true,  mineable:true,  item:"sphincs",  pts:40, rare:true,
                fact:"SLH-DSA FIPS 205 — Hash-based backup signature standard!"},
    falcon:    {color:"#f59e0b",    label:"F",  solid:true,  mineable:true,  item:"falcon",   pts:55, rare:true,
                fact:"FN-DSA FIPS 206 — Smallest quantum-safe signature ever!"},
    lwe:       {color:"#ec4899",    label:"L",  solid:true,  mineable:true,  item:"lwe",      pts:70, rare:true,
                fact:"Learning With Errors — The hardest PQC math problem!"},
    qcore:     {color:"#fbbf24",    label:"Q",  solid:true,  mineable:true,  item:"qcore",    pts:150,rare:true,
                fact:"Quantum Core — Master all NIST PQC standards to protect the world!"},
    wall:      {color:"#111827",    label:"",   solid:true,  mineable:false},
    ladder:    {color:"#78350f",    label:"▼",  solid:false, mineable:false, special:"deeper"},
    placed:    {color:"#1d4ed8",    label:"■",  solid:true,  mineable:false},
    boss_wall: {color:"#7f1d1d",    label:"☠",  solid:true,  mineable:false},
};

const ENEMIES = [
    {emoji:"☠️", name:"Shor",    color:"#ef4444", fact:"Shor breaks RSA and ECC!",           boss:false, dmg:15},
    {emoji:"🌀", name:"Grover",  color:"#f97316", fact:"Grover speeds up brute force attacks!",boss:false, dmg:10},
    {emoji:"👾", name:"HHL",     color:"#a855f7", fact:"HHL attacks linear algebra problems!", boss:false, dmg:12},
    {emoji:"💀", name:"Q-BOSS",  color:"#dc2626", fact:"Full quantum computer — ultimate threat!",boss:true, dmg:30},
];

let mw=[], mp, me=[], minv, mscore=0, mhp=120, mdepth=1, mrare=0, mmined=0;
let mrun=false, mk={}, mmt=0, particles=[];

// 12 depth level configs
const DEPTH_CONFIG = [
    {depth:1,  name:"Surface",        rareChance:0.04, enemyCount:1, hasBoss:false, desc:"Safe to mine!"},
    {depth:2,  name:"Shallow",        rareChance:0.07, enemyCount:1, hasBoss:false, desc:"Some rare ore!"},
    {depth:3,  name:"Stone Layer",    rareChance:0.10, enemyCount:2, hasBoss:true,  desc:"First boss!"},
    {depth:4,  name:"Iron Vein",      rareChance:0.13, enemyCount:2, hasBoss:false, desc:"More enemies!"},
    {depth:5,  name:"Crystal Cave",   rareChance:0.16, enemyCount:3, hasBoss:false, desc:"LWE crystals!"},
    {depth:6,  name:"Deep Rock",      rareChance:0.19, enemyCount:3, hasBoss:true,  desc:"Boss guardian!"},
    {depth:7,  name:"Quantum Seam",   rareChance:0.22, enemyCount:3, hasBoss:false, desc:"Rare quantum ore!"},
    {depth:8,  name:"Lattice Core",   rareChance:0.25, enemyCount:4, hasBoss:false, desc:"Dense lattice!"},
    {depth:9,  name:"Kyber Vault",    rareChance:0.27, enemyCount:4, hasBoss:true,  desc:"Vault boss!"},
    {depth:10, name:"Cipher Depths",  rareChance:0.29, enemyCount:5, hasBoss:false, desc:"Expert mining!"},
    {depth:11, name:"Quantum Abyss",  rareChance:0.30, enemyCount:5, hasBoss:true,  desc:"Final guardian!"},
    {depth:12, name:"Quantum Core",   rareChance:0.35, enemyCount:6, hasBoss:true,  desc:"Ultimate depth!"},
];

function genMines(depth) {
    mw=[];
    const dcfg = DEPTH_CONFIG[Math.min(depth-1, DEPTH_CONFIG.length-1)];
    const rareChance = dcfg.rareChance;
    const hasBoss = dcfg.hasBoss;

    for(let r=0;r<ROWS;r++){
        mw[r]=[];
        for(let c=0;c<COLS;c++){
            if(r===0||r===ROWS-1||c===0||c===COLS-1){mw[r][c]="wall";continue;}
            const rn=Math.random();
            if(depth>=5&&rn<0.02)      mw[r][c]="qcore";
            else if(rn<rareChance*0.25) mw[r][c]="lwe";
            else if(rn<rareChance*0.5)  mw[r][c]="falcon";
            else if(rn<rareChance*0.75) mw[r][c]="sphincs";
            else if(rn<rareChance*1.2)  mw[r][c]="dilithium";
            else if(rn<rareChance*2.0)  mw[r][c]="kyber";
            else if(rn<0.45)            mw[r][c]="stone";
            else                        mw[r][c]="empty";
        }
    }
    // Clear spawn area
    mw[1][1]="empty";mw[1][2]="empty";mw[2][1]="empty";mw[2][2]="empty";
    // Add ladder
    mw[ROWS-2][COLS-2]="ladder";
    // Boss area at depth 3+
    if(hasBoss){
        mw[ROWS-2][COLS-4]="boss_wall";
        mw[ROWS-3][COLS-4]="boss_wall";
    }
}

function startMines(){
    mdepth=1;mscore=0;mhp=120;mrare=0;mmined=0;
    minv={kyber:0,dilithium:0,sphincs:0,falcon:0,lwe:0,qcore:0};
    genMines(1);mp={x:1,y:1};me=[];particles=[];
    for(let i=0;i<2;i++)spawnEnemy();
    mrun=true;updateUI();
    cancelAnimationFrame(window._mF);mLoop();
}

function spawnEnemy(){
    const x=Math.floor(Math.random()*(COLS-5))+COLS-6;
    const y=Math.floor(Math.random()*(ROWS-4))+2;
    if(mw[y]&&mw[y][x]==="empty"){
        const isBoss = mdepth>=3&&Math.random()<0.3;
        const eType = isBoss ? ENEMIES[3] : ENEMIES[Math.floor(Math.random()*3)];
        me.push({x,y,timer:0,rate:isBoss?80:25+Math.floor(Math.random()*35),...eType});
    }
}

function mCanWalk(x,y){
    if(x<0||y<0||x>=COLS||y>=ROWS)return false;
    const b=BLOCKS[mw[y][x]];
    return b&&!b.solid;
}

function showFact(fact){
    const f=document.getElementById("qm-fact");
    f.textContent="📚 "+fact;f.style.display="block";
    clearTimeout(window._ft);
    window._ft=setTimeout(()=>{f.style.display="none";},4000);
}

function mineMid(){
    if(!mrun)return;
    const dirs=[{dx:0,dy:-1},{dx:0,dy:1},{dx:-1,dy:0},{dx:1,dy:0}];
    for(const d of dirs){
        const nx=mp.x+d.dx,ny=mp.y+d.dy;
        if(nx>=0&&ny>=0&&nx<COLS&&ny<ROWS){
            const bt=mw[ny][nx],b=BLOCKS[bt];
            if(b&&b.mineable){
                if(b.item){
                    minv[b.item]=(minv[b.item]||0)+1;
                    if(b.rare)mrare++;
                    showFact(b.fact);
                    // Sparkle
                    for(let i=0;i<8;i++) particles.push({
                        x:nx*CELL+CELL/2,y:ny*CELL+CELL/2,
                        vx:(Math.random()-0.5)*5,vy:(Math.random()-0.5)*5,
                        color:BLOCKS[bt].color,alpha:1,r:3
                    });
                }
                mscore+=b.pts;mmined++;mw[ny][nx]="empty";
                document.getElementById("qm-msg").textContent="Mined "+bt+"! +"+b.pts+" pts";
                updateUI();return;
            }
        }
    }
    document.getElementById("qm-msg").textContent="Nothing to mine here — move next to a glowing block!";
}

function placeMid(){
    if(!mrun||minv.kyber<=0){
        document.getElementById("qm-msg").textContent="Need Kyber blocks to build walls!";return;
    }
    const dirs=[{dx:0,dy:-1},{dx:1,dy:0},{dx:-1,dy:0},{dx:0,dy:1}];
    for(const d of dirs){
        const nx=mp.x+d.dx,ny=mp.y+d.dy;
        if(nx>=0&&ny>=0&&nx<COLS&&ny<ROWS&&mw[ny][nx]==="empty"){
            minv.kyber--;mw[ny][nx]="placed";
            document.getElementById("qm-msg").textContent="Kyber wall placed! Blocks quantum creepers!";
            updateUI();return;
        }
    }
}

function goDeeper(){
    if(!mrun)return;
    if(mp.x>=COLS-3&&mp.y>=ROWS-3){
        if(mdepth>=12){
            document.getElementById("qm-msg").textContent="🏆 MAX DEPTH REACHED! Quantum Core Miner! Score:"+mscore+" Rare:"+mrare;
            mrun=false;
            return;
        }
        mdepth++;
        genMines(mdepth);mp={x:1,y:1};me=[];particles=[];
        const dcfg3 = DEPTH_CONFIG[Math.min(mdepth-1, DEPTH_CONFIG.length-1)];
        for(let i=0;i<dcfg3.enemyCount;i++)spawnEnemy();
        document.getElementById("mdepth").textContent=mdepth+"/12";
        document.getElementById("qm-msg").textContent="Depth "+mdepth+"/12: "+dcfg3.name+"! "+dcfg3.desc;
        updateUI();
    } else {
        document.getElementById("qm-msg").textContent="Find the ▼ ladder in the bottom-right corner!";
    }
}

function updateUI(){
    document.getElementById("mscore").textContent=mscore;
    document.getElementById("mhp").textContent=Math.max(0,mhp);
    document.getElementById("mdepth").textContent=mdepth;
    document.getElementById("mrare").textContent=mrare;
    document.getElementById("mmined").textContent=mmined;
    document.getElementById("m-kyber").textContent="🔐 Kyber:"+minv.kyber;
    document.getElementById("m-dilithium").textContent="✍️ Dilithium:"+minv.dilithium;
    document.getElementById("m-sphincs").textContent="🌲 SPHINCS:"+minv.sphincs;
    document.getElementById("m-falcon").textContent="🦅 Falcon:"+minv.falcon;
    document.getElementById("m-lwe").textContent="🧮 LWE:"+minv.lwe;
    document.getElementById("m-qcore").textContent="💎 QCore:"+minv.qcore;
}

document.addEventListener("keydown",e=>{
    mk[e.key]=true;
    if(e.key==="e"||e.key==="E")mineMid();
    if(e.key==="f"||e.key==="F")placeMid();
});
document.addEventListener("keyup",e=>{mk[e.key]=false;});

function mLoop(){
    window._mF=requestAnimationFrame(mLoop);
    mmt++;
    if(mmt>=8){
        mmt=0;if(!mrun)return;
        let nx=mp.x,ny=mp.y;
        if(mk["ArrowUp"]||mk["w"])ny--;
        if(mk["ArrowDown"]||mk["s"])ny++;
        if(mk["ArrowLeft"]||mk["a"])nx--;
        if(mk["ArrowRight"]||mk["d"])nx++;
        if(mCanWalk(nx,ny)||(mw[ny]&&mw[ny][nx]==="ladder")){mp.x=nx;mp.y=ny;}

        // Move enemies
        me.forEach((e,i)=>{
            e.timer++;if(e.timer<e.rate)return;e.timer=0;
            const dx=mp.x-e.x,dy=mp.y-e.y;const moves=[];
            if(dx>0&&mCanWalk(e.x+1,e.y))moves.push({x:e.x+1,y:e.y});
            if(dx<0&&mCanWalk(e.x-1,e.y))moves.push({x:e.x-1,y:e.y});
            if(dy>0&&mCanWalk(e.x,e.y+1))moves.push({x:e.x,y:e.y+1});
            if(dy<0&&mCanWalk(e.x,e.y-1))moves.push({x:e.x,y:e.y-1});
            if(moves.length>0){
                moves.sort((a,b)=>
                    Math.hypot(a.x-mp.x,a.y-mp.y)-Math.hypot(b.x-mp.x,b.y-mp.y)
                );
                const mv=e.boss||Math.random()<0.7?moves[0]:moves[Math.floor(Math.random()*moves.length)];
                e.x=mv.x;e.y=mv.y;
            }
            if(e.x===mp.x&&e.y===mp.y){
                mhp-=e.dmg;updateUI();me.splice(i,1);
                showFact(e.fact);
                document.getElementById("qm-msg").textContent=
                    (e.boss?"💀 BOSS hit!":"☠️ "+e.name+" hit!")+" -"+e.dmg+" HP! "+e.fact;
                if(mhp<=0){
                    mrun=false;
                    document.getElementById("qm-msg").textContent="Mine collapsed! Score:"+mscore+" Rare:"+mrare;
                }
            }
        });
    }

    // Update particles
    particles=particles.filter(p=>{
        p.x+=p.vx;p.y+=p.vy;p.alpha-=0.05;
        p.vx*=0.9;p.vy*=0.9;
        return p.alpha>0;
    });

    mDraw();
}

function mDraw(){
    mx.clearRect(0,0,mc.width,mc.height);

    // Background gradient
    const bg=mx.createLinearGradient(0,0,0,mc.height);
    bg.addColorStop(0,"#0f172a");
    bg.addColorStop(1,"#1a0a2e");
    mx.fillStyle=bg;mx.fillRect(0,0,mc.width,mc.height);

    // Draw blocks
    for(let r=0;r<ROWS;r++){
        for(let c=0;c<COLS;c++){
            const bt=mw[r][c],b=BLOCKS[bt];if(!b)continue;
            mx.fillStyle=b.color;mx.fillRect(c*CELL,r*CELL,CELL,CELL);
            mx.strokeStyle="rgba(255,255,255,0.04)";
            mx.lineWidth=0.5;
            mx.strokeRect(c*CELL,r*CELL,CELL,CELL);

            // Block label
            if(b.label){
                mx.font=b.label.length>1?"18px sans-serif":"bold 14px sans-serif";
                mx.fillStyle="rgba(255,255,255,0.9)";
                mx.textAlign="center";
                mx.fillText(b.label,c*CELL+CELL/2,r*CELL+CELL/1.5);
            }

            // Glow for rare blocks
            if(b.mineable&&b.rare){
                mx.strokeStyle=b.color+"88";
                mx.lineWidth=2;
                mx.strokeRect(c*CELL+1,r*CELL+1,CELL-2,CELL-2);
            } else if(b.mineable&&b.item){
                mx.strokeStyle="rgba(255,255,255,0.2)";
                mx.lineWidth=1;
                mx.strokeRect(c*CELL+2,r*CELL+2,CELL-4,CELL-4);
            }

            // Depth indicator for ladder
            if(bt==="ladder"){
                mx.fillStyle="#f59e0b";
                mx.font="10px sans-serif";
                mx.textAlign="center";
                mx.fillText("DEEPER",c*CELL+CELL/2,r*CELL+CELL-4);
            }
        }
    }

    // Draw particles
    particles.forEach(p=>{
        mx.beginPath();
        mx.arc(p.x,p.y,p.r,0,Math.PI*2);
        mx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,"0");
        mx.fill();
    });

    // Draw enemies
    me.forEach(e=>{
        const size=e.boss?28:22;
        if(e.boss){
            mx.beginPath();
            mx.arc(e.x*CELL+CELL/2,e.y*CELL+CELL/2,20+Math.sin(Date.now()*0.005)*3,0,Math.PI*2);
            mx.fillStyle="rgba(220,38,38,0.25)";
            mx.fill();
        }
        mx.font=size+"px sans-serif";
        mx.textAlign="center";
        mx.fillText(e.emoji,e.x*CELL+CELL/2,e.y*CELL+CELL/1.35);
        if(e.boss){
            mx.fillStyle="#dc2626";
            mx.font="bold 8px sans-serif";
            mx.fillText("BOSS",e.x*CELL+CELL/2,e.y*CELL+4);
        }
    });

    // Draw player with glow
    mx.beginPath();
    mx.arc(mp.x*CELL+CELL/2,mp.y*CELL+CELL/2,16,0,Math.PI*2);
    mx.fillStyle="rgba(59,130,246,0.2)";
    mx.fill();
    mx.font="24px sans-serif";
    mx.textAlign="center";
    mx.fillText("⛏️",mp.x*CELL+CELL/2,mp.y*CELL+CELL/1.35);
    mx.strokeStyle="#3b82f6";
    mx.lineWidth=2;
    mx.strokeRect(mp.x*CELL+2,mp.y*CELL+2,CELL-4,CELL-4);

    // Depth HUD corner
    mx.fillStyle="rgba(15,23,42,0.8)";
    mx.beginPath();
    mx.roundRect(8,mc.height-30,160,22,4);
    mx.fill();
    mx.fillStyle="#3b82f6";
    mx.font="bold 11px sans-serif";
    mx.textAlign="left";
    mx.fillText("⬇️ Depth "+mdepth+" — "+
        (mdepth<3?"Surface":"mdepth"<5?"Deep Zone":"Ultra Deep!"),12,mc.height-15);

    // HP bar
    const hw=100;
    mx.fillStyle="rgba(15,23,42,0.8)";
    mx.beginPath();mx.roundRect(mc.width-hw-12,mc.height-30,hw+4,22,4);mx.fill();
    mx.fillStyle="#374151";
    mx.fillRect(mc.width-hw-8,mc.height-24,hw,10);
    const hpPct=Math.max(0,mhp/120);
    mx.fillStyle=hpPct>0.5?"#10b981":hpPct>0.25?"#f59e0b":"#ef4444";
    mx.fillRect(mc.width-hw-8,mc.height-24,hw*hpPct,10);

    // Game over overlay
    if(!mrun){
        mx.fillStyle="rgba(0,0,0,0.85)";
        mx.fillRect(0,0,mc.width,mc.height);
        mx.fillStyle=mhp<=0?"#ef4444":"#10b981";
        mx.font="bold 26px sans-serif";
        mx.textAlign="center";
        mx.fillText(mhp<=0?"💥 Mine Collapsed!":"⛏️ Keep Mining!",mc.width/2,mc.height/2-30);
        mx.fillStyle="white";
        mx.font="15px sans-serif";
        mx.fillText("Score: "+mscore+" | Rare: "+mrare+" | Depth: "+mdepth,mc.width/2,mc.height/2+10);
        mx.fillStyle="#a5b4fc";
        mx.font="12px sans-serif";
        mx.fillText("Kyber, Dilithium, SPHINCS+, Falcon — all NIST approved!",mc.width/2,mc.height/2+40);
    }
}

// Idle screen
mx.fillStyle="#0f172a";mx.fillRect(0,0,mc.width,mc.height);
const idBg=mx.createLinearGradient(0,0,0,mc.height);
idBg.addColorStop(0,"#0f172a");idBg.addColorStop(1,"#1a0a2e");
mx.fillStyle=idBg;mx.fillRect(0,0,mc.width,mc.height);
mx.fillStyle="#3b82f6";mx.font="bold 20px sans-serif";mx.textAlign="center";
mx.fillText("⛏️ QuantumCraft — Lattice Mines",mc.width/2,mc.height/2-55);
mx.fillStyle="#a5b4fc";mx.font="13px sans-serif";
mx.fillText("Mine 🔐 Kyber  ✍️ Dilithium  🌲 SPHINCS+  🦅 Falcon  🧮 LWE  💎 QCore",mc.width/2,mc.height/2-20);
mx.fillText("Go deeper for rarer algorithms!  Boss enemies at depth 3+!",mc.width/2,mc.height/2+10);
mx.fillStyle="white";mx.font="bold 14px sans-serif";
mx.fillText("Press ▶ Start to mine!",mc.width/2,mc.height/2+50);
</script>
</body>
</html>
""", height=680)

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
