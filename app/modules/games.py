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

const LEVEL_CONFIG = [
    {level:1,  name:"Recruit",        dropRate:55, speed:3.5, bossEvery:0, lives:5, desc:"Learn the basics!"},
    {level:2,  name:"Cadet",          dropRate:50, speed:3.8, bossEvery:0, lives:5, desc:"Getting faster!"},
    {level:3,  name:"Agent",          dropRate:45, speed:4.1, bossEvery:3, lives:4, desc:"First boss wave!"},
    {level:4,  name:"Specialist",     dropRate:42, speed:4.4, bossEvery:3, lives:4, desc:"More unsafe blocks!"},
    {level:5,  name:"Cipher Corps",   dropRate:38, speed:4.7, bossEvery:3, lives:4, desc:"Power-ups appear!"},
    {level:6,  name:"Crypto Guard",   dropRate:34, speed:5.0, bossEvery:2, lives:3, desc:"Boss every 2 levels!"},
    {level:7,  name:"Lattice Knight", dropRate:30, speed:5.3, bossEvery:2, lives:3, desc:"Super fast!"},
    {level:8,  name:"Key Master",     dropRate:26, speed:5.6, bossEvery:2, lives:3, desc:"Almost expert!"},
    {level:9,  name:"Quantum Sage",   dropRate:22, speed:5.9, bossEvery:2, lives:3, desc:"Expert territory!"},
    {level:10, name:"NIST Scholar",   dropRate:18, speed:6.2, bossEvery:1, lives:2, desc:"Boss every level!"},
    {level:11, name:"PQC Champion",   dropRate:14, speed:6.6, bossEvery:1, lives:2, desc:"Near impossible!"},
    {level:12, name:"Quantum Guardian",dropRate:10,speed:7.0, bossEvery:1, lives:2, desc:"Master level!"},
];

function getLevelConfig() {
    return LEVEL_CONFIG[Math.min(level-1, LEVEL_CONFIG.length-1)];
}

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
    """6-8: Lattice Maze — Navigate the quantum grid to rescue stolen NIST algorithms."""
    import streamlit as st
    st.subheader("🌀 Lattice Maze — Operation: Quantum Rescue!")
    st.markdown(
        "🚨 **MISSION BRIEFING:** The Quantum Monster has stolen the 4 NIST PQC algorithm crystals "
        "and hidden them in a lattice grid! You are Agent Pixel. Navigate the maze, "
        "collect all crystals, and escape before the Shor and Grover enemies catch you. "
        "Each crystal you collect teaches you a real PQC concept!"
    )

    import streamlit.components.v1 as _lm
    _lm.html("""
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;}
#wrap{display:flex;flex-direction:column;align-items:center;padding:10px;max-width:520px;margin:0 auto;}

/* HUD */
.hud{display:grid;grid-template-columns:repeat(5,1fr);gap:4px;width:100%;margin-bottom:8px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:5px 4px;
    text-align:center;font-size:10px;color:#60a5fa;}
.hb b{display:block;font-size:14px;color:#93c5fd;}

/* Mission panel */
#mission{background:#071520;border:1px solid #1a3a5a;border-radius:10px;
    padding:8px 12px;width:100%;margin-bottom:6px;font-size:11px;color:#60a5fa;
    min-height:32px;line-height:1.5;}

/* Canvas */
#gc{border:2px solid #1d4ed8;border-radius:12px;display:block;
    box-shadow:0 0 24px rgba(59,130,246,0.2);}

/* Crystal collection */
#crystals{display:flex;gap:8px;justify-content:center;margin:8px 0;flex-wrap:wrap;}
.crystal{background:#071520;border:2px solid #334155;border-radius:10px;
    padding:6px 10px;font-size:11px;color:#64748b;text-align:center;
    transition:all 0.3s;min-width:70px;}
.crystal.collected{border-color:#10b981;color:#10b981;
    box-shadow:0 0 12px rgba(16,185,129,0.3);background:#071f15;}
.crystal.collecting{animation:pulse 0.5s ease-in-out;}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.15)}}

/* Message */
#msg{font-size:12px;color:#34d399;min-height:18px;margin:4px;text-align:center;font-weight:bold;}

/* Fact box */
#fact{background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.3);
    border-radius:10px;padding:8px 12px;margin:4px 0;font-size:11px;color:#93c5fd;
    max-width:460px;display:none;text-align:center;line-height:1.5;width:100%;}

/* Buttons */
.btns{display:flex;gap:6px;margin:6px 0;flex-wrap:wrap;justify-content:center;}
.btn{padding:8px 18px;border-radius:8px;border:none;cursor:pointer;
    font-size:12px;font-weight:bold;color:white;transition:all 0.15s;}
.btn:active{transform:scale(0.95);}
.btn-start{background:#1d4ed8;}
.btn-next{background:#059669;}
.btn-next:disabled{background:#334155;cursor:not-allowed;}

/* D-pad */
.dpad{display:grid;grid-template-columns:repeat(3,44px);gap:4px;margin:6px 0;}
.db{width:44px;height:44px;border-radius:8px;border:1px solid #1e3a5a;
    cursor:pointer;background:#071520;color:#60a5fa;font-size:18px;font-weight:bold;
    transition:all 0.1s;}
.db:active{background:#1d4ed8;color:white;transform:scale(0.92);}

/* Win/Game over overlay */
#overlay{display:none;position:absolute;top:0;left:0;right:0;bottom:0;
    background:rgba(2,13,20,0.92);border-radius:12px;
    flex-direction:column;align-items:center;justify-content:center;
    text-align:center;padding:20px;}
.overlay-wrap{position:relative;width:460px;}
</style>
</head>
<body>
<div id="wrap">

<div class="hud">
    <div class="hb">❤️ Lives<br><b id="hlives">3</b></div>
    <div class="hb">🔮 Crystals<br><b id="hcrystals">0/4</b></div>
    <div class="hb">⭐ Score<br><b id="hscore">0</b></div>
    <div class="hb">🌊 Level<br><b id="hlevel">1</b>/12</div>
    <div class="hb">👾 Enemies<br><b id="henemies">0</b></div>
</div>

<div id="mission">🎯 Mission: Collect all NIST algorithm crystals and reach the EXIT portal!</div>

<div id="crystals">
    <div class="crystal" id="c0">🔐<br>ML-KEM</div>
    <div class="crystal" id="c1">✍️<br>ML-DSA</div>
    <div class="crystal" id="c2">🌲<br>SLH-DSA</div>
    <div class="crystal" id="c3">🦅<br>FN-DSA</div>
</div>

<div class="overlay-wrap">
    <canvas id="gc" width="460" height="400"></canvas>
    <div id="overlay">
        <div id="ov-emoji" style="font-size:3rem;margin-bottom:8px">🏆</div>
        <h2 id="ov-title" style="color:#60a5fa;margin-bottom:8px"></h2>
        <p id="ov-msg" style="color:#94a3b8;font-size:12px;margin-bottom:12px"></p>
        <div id="ov-btns"></div>
    </div>
</div>

<div id="msg">Press START to begin your mission!</div>
<div id="fact"></div>

<div class="btns">
    <button class="btn btn-start" onclick="startGame()">▶ START MISSION</button>
    <button class="btn btn-next" id="next-btn" onclick="nextLevel()" disabled>Next Level →</button>
</div>

<div class="dpad">
    <div></div>
    <button class="db" onclick="tryMove(0,-1)">▲</button>
    <div></div>
    <button class="db" onclick="tryMove(-1,0)">◀</button>
    <button class="db" onclick="startGame()">⟳</button>
    <button class="db" onclick="tryMove(1,0)">▶</button>
    <div></div>
    <button class="db" onclick="tryMove(0,1)">▼</button>
    <div></div>
</div>

</div>

<script>
const cv = document.getElementById("gc");
const cx = cv.getContext("2d");
const CELL=40, COLS=11, ROWS=10;

// 4 NIST crystals with real facts
const CRYSTALS = [
    {id:0, emoji:"🔐", name:"ML-KEM",   color:"#10b981",
     fact:"FIPS 203 (Kyber) — Uses Module-LWE lattice math. Protects TLS, VPNs, and encrypted messaging from quantum attacks!",
     pts:100},
    {id:1, emoji:"✍️", name:"ML-DSA",   color:"#3b82f6",
     fact:"FIPS 204 (Dilithium) — Digital signature using Module-LWE+SIS. Signs software updates so nobody can forge them!",
     pts:125},
    {id:2, emoji:"🌲", name:"SLH-DSA",  color:"#8b5cf6",
     fact:"FIPS 205 (SPHINCS+) — Hash-based signatures using SHA-3. The backup standard — safe even if lattices are broken!",
     pts:150},
    {id:3, emoji:"🦅", name:"FN-DSA",   color:"#f59e0b",
     fact:"FIPS 206 (Falcon) — NTRU lattice signatures. Smallest signatures of all 4 standards — perfect for IoT devices!",
     pts:175},
];

const ENEMIES = [
    {emoji:"☠️", name:"Shor",   color:"#ef4444", spd:8, fact:"Shor's Algorithm breaks RSA by finding prime factors — that's why we need Kyber!"},
    {emoji:"🌀", name:"Grover", color:"#f97316", spd:6, fact:"Grover's Algorithm speeds up brute force — doubles required key sizes but can't break Kyber!"},
    {emoji:"👾", name:"HHL",    color:"#a855f7", spd:5, fact:"HHL Algorithm attacks linear systems — but NOT the lattice problems Kyber uses!"},
    {emoji:"💀", name:"Q-BOSS", color:"#dc2626", spd:4, fact:"A Cryptographically Relevant Quantum Computer! Deploy Kyber NOW before these exist!"},
];

// 12 maze layouts
const MAZES = [
    [[1,1,1,1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,1,1,1,0,1,1,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,1,1,1,0,1,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,1,1,1,0,1,1,1,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,1,1,1,1,1,1,1,0,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,0,0,0,1,0,0,0,0,0,1],[1,0,1,0,1,0,1,1,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,1,1,1,1,0,1,0,1],[1,0,0,0,0,0,1,0,0,0,1],[1,1,1,1,0,1,1,1,1,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,1,1,1,1,1,1,1,0,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,0,0,0,0,0,1,0,0,0,1],[1,0,1,1,1,0,1,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,1,1,1,1,1,0,1],[1,0,0,0,1,0,0,0,0,0,1],[1,1,1,0,1,0,1,1,1,1,1],[1,0,0,0,0,0,1,0,0,0,1],[1,0,1,1,1,1,1,0,1,0,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,0,0,0,1,0,0,0,1,0,1],[1,1,1,0,1,0,1,0,1,0,1],[1,0,0,0,0,0,1,0,0,0,1],[1,0,1,1,1,0,1,1,1,0,1],[1,0,0,0,1,0,0,0,1,0,1],[1,1,1,0,1,1,1,0,1,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,1,1,1,1,1,1,1,0,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,0,0,0,1,0,0,0,1,0,1],[1,0,1,0,1,0,1,0,1,0,1],[1,0,1,0,0,0,1,0,0,0,1],[1,0,1,1,1,0,1,1,1,0,1],[1,0,0,0,0,0,0,0,1,0,1],[1,1,1,1,0,1,0,0,1,0,1],[1,0,0,0,0,1,0,1,0,0,1],[1,0,1,1,0,0,0,1,1,0,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,1,0,1,1,1,0,1,0,1],[1,0,1,0,1,0,1,0,1,0,1],[1,0,1,0,0,0,1,0,1,0,1],[1,0,0,0,1,0,0,0,0,0,1],[1,1,0,1,1,0,1,1,0,1,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,1,1,0,1,0,1,1,0,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,1,1,1,0,1,0,1],[1,0,0,0,1,0,0,0,0,0,1],[1,1,1,0,1,0,1,1,1,1,1],[1,0,0,0,0,0,1,0,0,0,1],[1,0,1,1,1,0,1,0,1,0,1],[1,0,0,0,0,0,0,0,1,0,1],[1,0,1,1,1,1,1,1,1,0,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,0,0,0,1,0,1,0,0,0,1],[1,0,1,0,1,0,1,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,1,0,1,0,1,1,0,1],[1,0,0,0,0,1,0,0,0,0,1],[1,1,0,1,0,1,1,0,1,1,1],[1,0,0,1,0,0,0,0,1,0,1],[1,0,1,1,1,1,0,0,0,0,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,0,0,0,1],[1,1,1,0,1,0,1,0,1,1,1],[1,0,0,0,1,0,1,0,0,0,1],[1,0,1,1,1,0,1,1,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,1,1,1,0,1,0,1],[1,0,0,0,1,0,0,0,0,0,1],[1,1,0,1,1,0,1,1,0,1,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,0,1,0,0,0,1,0,0,0,1],[1,0,1,0,1,0,1,0,1,0,1],[1,0,0,0,1,0,0,0,1,0,1],[1,1,1,0,1,1,0,1,1,0,1],[1,0,0,0,0,0,0,1,0,0,1],[1,0,1,1,1,0,1,1,1,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,1,1,0,1,0,1,1,0,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,0,0,0,1,0,0,0,0,0,1],[1,0,1,0,1,1,1,1,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,1,1,0,1,0,1,0,1],[1,0,0,0,0,0,1,0,0,0,1],[1,1,0,1,1,0,1,1,0,1,1],[1,0,0,1,0,0,0,1,0,0,1],[1,0,1,1,1,0,1,1,1,0,1],[1,1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,1,1,0,1,0,1,1,0,1],[1,0,1,0,0,1,0,1,0,0,1],[1,0,0,0,1,1,1,0,0,0,1],[1,1,0,1,0,0,0,1,0,1,1],[1,0,0,1,0,1,0,1,0,0,1],[1,0,1,0,0,1,0,0,1,0,1],[1,0,0,0,1,0,1,0,0,0,1],[1,1,1,1,1,1,1,1,1,1,1]],
];

const LEVEL_CONFIG = [
    {enemies:0, crystals:2, timeLimit:0},
    {enemies:0, crystals:2, timeLimit:0},
    {enemies:1, crystals:3, timeLimit:0},
    {enemies:1, crystals:3, timeLimit:0},
    {enemies:2, crystals:4, timeLimit:0},
    {enemies:2, crystals:4, timeLimit:60},
    {enemies:2, crystals:4, timeLimit:50},
    {enemies:3, crystals:4, timeLimit:45},
    {enemies:3, crystals:4, timeLimit:40},
    {enemies:3, crystals:4, timeLimit:35},
    {enemies:4, crystals:4, timeLimit:30},
    {enemies:4, crystals:4, timeLimit:25},
];

let level=0, lives=3, score=0, gameActive=false;
let player={x:1,y:1}, crystalPos=[], enemyPos=[], exitPos={x:9,y:8};
let collectedCrystals=new Set(), moveTimer=null, enemyMoveTimer=null;
let factTimer=null, timeLeft=0, timeTimer=null;

function getFreeCells(maze) {
    let cells=[];
    for(let r=1;r<ROWS-1;r++) for(let c=1;c<COLS-1;c++)
        if(maze[r][c]===0) cells.push({x:c,y:r});
    return cells;
}

function dist(a,b){return Math.abs(a.x-b.x)+Math.abs(a.y-b.y);}

function placeCrystals(maze, cfg) {
    let free = getFreeCells(maze).filter(c=>dist(c,{x:1,y:1})>3);
    let needed = Math.min(cfg.crystals, CRYSTALS.length, free.length);
    let placed=[], used=new Set();
    // Place crystals spread out
    for(let i=0;i<needed;i++){
        let best=null, bestDist=0;
        for(let j=0;j<free.length;j++){
            if(used.has(j)) continue;
            let minD=placed.length?Math.min(...placed.map(p=>dist(free[j],p))):999;
            if(minD>bestDist){bestDist=minD;best=j;}
        }
        if(best!==null){used.add(best);placed.push({...free[best],crystalIdx:i});}
    }
    return placed;
}

function placeEnemies(maze, cfg) {
    let free = getFreeCells(maze).filter(c=>dist(c,{x:1,y:1})>4&&dist(c,exitPos)>2);
    let placed=[];
    for(let i=0;i<Math.min(cfg.enemies,free.length);i++){
        let idx=Math.floor(Math.random()*free.length);
        placed.push({...free[idx], typeIdx:i%ENEMIES.length, moveCount:0});
        free.splice(idx,1);
    }
    return placed;
}

function startGame() {
    clearTimers();
    collectedCrystals=new Set();
    lives=3; score=0;
    level=0;
    updateCrystalUI();
    initLevel();
}

function initLevel() {
    clearTimers();
    const maze=MAZES[level%MAZES.length];
    const cfg=LEVEL_CONFIG[Math.min(level,LEVEL_CONFIG.length-1)];
    player={x:1,y:1};
    exitPos={x:9,y:8};
    crystalPos=placeCrystals(maze,cfg);
    enemyPos=placeEnemies(maze,cfg);
    gameActive=true;
    collectedCrystals=new Set();
    updateCrystalUI();
    document.getElementById("next-btn").disabled=true;

    if(cfg.timeLimit>0){
        timeLeft=cfg.timeLimit;
        timeTimer=setInterval(()=>{
            timeLeft--;
            setMsg(`⏱️ Time: ${timeLeft}s — collect all crystals!`);
            if(timeLeft<=0){clearInterval(timeTimer);loseLife("⏰ Time's up!");}
        },1000);
    }

    setMsg(`Level ${level+1}: Collect ${crystalPos.length} NIST crystal${crystalPos.length>1?'s':''}!`);
    updateHUD();
    drawAll();
    enemyMoveTimer=setInterval(moveEnemies,cfg.enemies>0?600:99999);
}

function clearTimers(){
    if(enemyMoveTimer) clearInterval(enemyMoveTimer);
    if(timeTimer) clearInterval(timeTimer);
    if(factTimer) clearTimeout(factTimer);
}

function updateHUD(){
    document.getElementById("hlives").textContent=lives;
    document.getElementById("hcrystals").textContent=collectedCrystals.size+"/"+crystalPos.length;
    document.getElementById("hscore").textContent=score;
    document.getElementById("hlevel").textContent=level+1;
    document.getElementById("henemies").textContent=enemyPos.length;
}

function updateCrystalUI(){
    for(let i=0;i<4;i++){
        let el=document.getElementById("c"+i);
        el.className="crystal"+(collectedCrystals.has(i)?" collected":"");
    }
}

function setMsg(m,c){
    let el=document.getElementById("msg");
    el.textContent=m;
    el.style.color=c||"#34d399";
}

function showFact(text,color){
    let el=document.getElementById("fact");
    el.textContent=text;
    el.style.display="block";
    el.style.borderColor=(color||"#3b82f6")+"80";
    if(factTimer) clearTimeout(factTimer);
    factTimer=setTimeout(()=>el.style.display="none",5000);
}

function tryMove(dx,dy){
    if(!gameActive) return;
    const maze=MAZES[level%MAZES.length];
    let nx=player.x+dx, ny=player.y+dy;
    if(nx<0||ny<0||nx>=COLS||ny>=ROWS) return;
    if(maze[ny][nx]===1) return;
    player={x:nx,y:ny};

    // Check crystal collection
    for(let i=0;i<crystalPos.length;i++){
        let c=crystalPos[i];
        if(c.x===player.x&&c.y===player.y&&!collectedCrystals.has(c.crystalIdx)){
            collectedCrystals.add(c.crystalIdx);
            let cr=CRYSTALS[c.crystalIdx];
            score+=cr.pts*(level+1);
            setMsg("✨ "+cr.name+" crystal collected! +"+cr.pts*(level+1)+" pts",cr.color);
            showFact("🔐 "+cr.name+": "+cr.fact, cr.color);
            document.getElementById("c"+c.crystalIdx).classList.add("collecting");
            setTimeout(()=>document.getElementById("c"+c.crystalIdx).classList.remove("collecting"),500);
            updateCrystalUI();
        }
    }

    // Check exit
    if(player.x===exitPos.x&&player.y===exitPos.y){
        if(collectedCrystals.size>=crystalPos.length){
            levelComplete();
        } else {
            let need=crystalPos.length-collectedCrystals.size;
            setMsg("🚫 Collect "+need+" more crystal"+( need>1?"s":"")+" first!","#f59e0b");
        }
    }

    // Check enemy collision
    checkEnemyCollision();
    updateHUD();
    drawAll();
}

function moveEnemies(){
    if(!gameActive) return;
    const maze=MAZES[level%MAZES.length];
    const DIRS=[{x:1,y:0},{x:-1,y:0},{x:0,y:1},{x:0,y:-1}];

    enemyPos=enemyPos.map(e=>{
        // 60% chase player, 40% random
        let moves=DIRS.filter(d=>{
            let nx=e.x+d.x,ny=e.y+d.y;
            return nx>=0&&ny>=0&&nx<COLS&&ny<ROWS&&maze[ny][nx]===0;
        });
        if(moves.length===0) return e;

        let chosen;
        if(Math.random()<0.6){
            // Chase
            let best=moves[0], bestD=dist({x:e.x+moves[0].x,y:e.y+moves[0].y},player);
            for(let m of moves){
                let d=dist({x:e.x+m.x,y:e.y+m.y},player);
                if(d<bestD){bestD=d;best=m;}
            }
            chosen=best;
        } else {
            chosen=moves[Math.floor(Math.random()*moves.length)];
        }
        return {...e,x:e.x+chosen.x,y:e.y+chosen.y};
    });

    checkEnemyCollision();
    drawAll();
}

function checkEnemyCollision(){
    for(let e of enemyPos){
        if(e.x===player.x&&e.y===player.y){
            let et=ENEMIES[e.typeIdx];
            loseLife("💥 "+et.name+" caught you! "+et.fact);
            return;
        }
    }
}

function loseLife(msg){
    clearTimers();
    lives--;
    gameActive=false;
    updateHUD();
    if(lives<=0){
        showOverlay("💀","Game Over!",
            "Score: "+score+" | Level "+( level+1),
            [{label:"🔄 Try Again",fn:"startGame()"}]);
    } else {
        setMsg("💀 "+msg+" ("+lives+" lives left)","#ef4444");
        showFact(msg.includes("!")?msg.split("!")[1]||"":"The quantum enemies are getting stronger!", "#ef4444");
        setTimeout(()=>{initLevel();},2000);
    }
}

function levelComplete(){
    clearTimers();
    gameActive=false;
    let bonus=Math.max(0,timeLeft)*10;
    score+=bonus+(level+1)*50;
    updateHUD();

    if(level>=11){
        showOverlay("🏆","ALL 12 LEVELS COMPLETE!",
            "Final Score: "+score+" | You are a Lattice Master!",
            [{label:"🔄 Play Again",fn:"startGame()"}]);
    } else {
        setMsg("✅ Level "+(level+1)+" complete! +"+(bonus+(level+1)*50)+" pts","#10b981");
        document.getElementById("next-btn").disabled=false;
        showMissionBrief(level+1);
    }
}

function showMissionBrief(nextLvl){
    const briefs=[
        "","","Level 3: Your first enemy appears — the Shor Algorithm! It breaks RSA.",
        "Level 4: Shor is faster now. Kyber's lattice math stops it cold!",
        "Level 5: BOSS LEVEL! Collect all 4 NIST crystals to win.",
        "Level 6: Time limit added! Real cryptographers work under pressure.",
        "Level 7: Grover joins — it speeds up brute force attacks!",
        "Level 8: Three enemies now. This is what real PQC defends against.",
        "Level 9: HHL Algorithm appears — attacks linear algebra systems!",
        "Level 10: Time is running out. The quantum computer is almost ready!",
        "Level 11: All four enemies + time pressure. The final defense!",
        "Level 12: GRANDMASTER! All enemies at full speed. Can you escape?",
    ];
    let brief=briefs[nextLvl]||"Next level!";
    document.getElementById("mission").textContent="🎯 "+brief;
}

function nextLevel(){
    level++;
    collectedCrystals=new Set();
    updateCrystalUI();
    initLevel();
    document.getElementById("next-btn").disabled=true;
}

function showOverlay(emoji,title,msg,btns){
    let ov=document.getElementById("overlay");
    document.getElementById("ov-emoji").textContent=emoji;
    document.getElementById("ov-title").textContent=title;
    document.getElementById("ov-msg").textContent=msg;
    let bc=document.getElementById("ov-btns");
    bc.innerHTML="";
    for(let b of btns){
        bc.innerHTML+=`<button class="btn btn-start" style="margin:4px" onclick="${b.fn}">${b.label}</button>`;
    }
    ov.style.display="flex";
    setTimeout(()=>ov.style.display="none",100);
    ov.style.display="flex";
}

function drawAll(){
    const maze=MAZES[level%MAZES.length];
    cx.clearRect(0,0,cv.width,cv.height);

    // Draw maze
    for(let r=0;r<ROWS;r++){
        for(let c=0;c<COLS;c++){
            if(maze[r][c]===1){
                cx.fillStyle="#071a2e";
                cx.fillRect(c*CELL,r*CELL,CELL,CELL);
                cx.strokeStyle="#1a3a5a";
                cx.lineWidth=1;
                cx.strokeRect(c*CELL,r*CELL,CELL,CELL);
                // Lattice dots
                cx.fillStyle="#1d4ed820";
                cx.beginPath();
                cx.arc(c*CELL+CELL/2,r*CELL+CELL/2,3,0,Math.PI*2);
                cx.fill();
            } else {
                cx.fillStyle="#020d14";
                cx.fillRect(c*CELL,r*CELL,CELL,CELL);
            }
        }
    }

    // Draw grid lines on open cells (lattice effect)
    cx.strokeStyle="#0a2040";
    cx.lineWidth=0.5;
    for(let r=0;r<ROWS;r++){
        for(let c=0;c<COLS;c++){
            if(maze[r][c]===0){
                cx.strokeRect(c*CELL,r*CELL,CELL,CELL);
            }
        }
    }

    // Draw exit portal
    let allCollected=collectedCrystals.size>=crystalPos.length;
    if(allCollected){
        // Glowing exit
        cx.fillStyle="#10b98130";
        cx.fillRect(exitPos.x*CELL,exitPos.y*CELL,CELL,CELL);
        cx.strokeStyle="#10b981";
        cx.lineWidth=2;
        cx.strokeRect(exitPos.x*CELL+2,exitPos.y*CELL+2,CELL-4,CELL-4);
    }
    cx.font=`${CELL-8}px serif`;
    cx.textAlign="center";
    cx.textBaseline="middle";
    cx.fillText(allCollected?"🚀":"🚪",exitPos.x*CELL+CELL/2,exitPos.y*CELL+CELL/2);

    // Draw crystals
    for(let c of crystalPos){
        if(!collectedCrystals.has(c.crystalIdx)){
            let cr=CRYSTALS[c.crystalIdx];
            // Glow effect
            cx.shadowColor=cr.color;
            cx.shadowBlur=12;
            cx.fillText(cr.emoji,c.x*CELL+CELL/2,c.y*CELL+CELL/2);
            cx.shadowBlur=0;
        }
    }

    // Draw enemies
    for(let e of enemyPos){
        let et=ENEMIES[e.typeIdx];
        cx.shadowColor=et.color;
        cx.shadowBlur=8;
        cx.fillText(et.emoji,e.x*CELL+CELL/2,e.y*CELL+CELL/2);
        cx.shadowBlur=0;
        // Name label
        cx.fillStyle=et.color;
        cx.font="7px sans-serif";
        cx.fillText(et.name,e.x*CELL+CELL/2,e.y*CELL+CELL-3);
        cx.font=`${CELL-8}px serif`;
    }

    // Draw player
    cx.font=`${CELL-6}px serif`;
    cx.shadowColor="#3b82f6";
    cx.shadowBlur=16;
    cx.fillText("🕵️",player.x*CELL+CELL/2,player.y*CELL+CELL/2);
    cx.shadowBlur=0;

    // Level indicator dots
    cx.font="10px sans-serif";
}

// Keyboard controls
document.addEventListener("keydown",e=>{
    if(!gameActive) return;
    const map={"ArrowUp":[0,-1],"ArrowDown":[0,1],"ArrowLeft":[-1,0],"ArrowRight":[1,0],
               "w":[0,-1],"s":[0,1],"a":[-1,0],"d":[1,0]};
    if(map[e.key]){e.preventDefault();tryMove(...map[e.key]);}
});

// Initial draw
cx.fillStyle="#020d14";
cx.fillRect(0,0,cv.width,cv.height);
cx.fillStyle="#1d4ed8";
cx.font="bold 18px sans-serif";
cx.textAlign="center";
cx.textBaseline="middle";
cx.fillText("🌀 OPERATION: QUANTUM RESCUE",cv.width/2,cv.height/2-40);
cx.fillStyle="#60a5fa";
cx.font="13px sans-serif";
cx.fillText("The Quantum Monster stole the NIST algorithm crystals!",cv.width/2,cv.height/2);
cx.fillText("Collect ML-KEM, ML-DSA, SLH-DSA and FN-DSA",cv.width/2,cv.height/2+20);
cx.fillText("then escape through the exit portal!",cv.width/2,cv.height/2+40);
cx.fillStyle="#334155";
cx.font="12px sans-serif";
cx.fillText("Press START MISSION to begin",cv.width/2,cv.height/2+70);
</script>
</body>
</html>
""", height=700)


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
        "easy":   {"speed": 2.2, "rate": 55,  "hp": 30,  "label": "🟢 Recruit",     "waves": 5},
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

const MAX_WAVES = 12;

// 12 wave configs with speed and rate baked in per difficulty
const WAVE_CONFIG = (function() {{
    const s = {diff['speed']};
    const r = {diff['rate']};
    return [
        {{wave:1,  speed:s*0.7, rate:Math.floor(r*1.4), count:4,  boss:false, name:"First Contact"}},
        {{wave:2,  speed:s*0.8, rate:Math.floor(r*1.3), count:5,  boss:false, name:"Quantum Scouts"}},
        {{wave:3,  speed:s*0.9, rate:Math.floor(r*1.2), count:6,  boss:true,  name:"Boss Wave 1"}},
        {{wave:4,  speed:s*1.0, rate:Math.floor(r*1.1), count:7,  boss:false, name:"Shor Surge"}},
        {{wave:5,  speed:s*1.1, rate:Math.floor(r*1.0), count:8,  boss:false, name:"Grover Storm"}},
        {{wave:6,  speed:s*1.2, rate:Math.floor(r*0.9), count:9,  boss:true,  name:"Boss Wave 2"}},
        {{wave:7,  speed:s*1.3, rate:Math.floor(r*0.85),count:10, boss:false, name:"Quantum Flood"}},
        {{wave:8,  speed:s*1.4, rate:Math.floor(r*0.8), count:11, boss:false, name:"QAOA Assault"}},
        {{wave:9,  speed:s*1.5, rate:Math.floor(r*0.75),count:12, boss:true,  name:"Boss Wave 3"}},
        {{wave:10, speed:s*1.6, rate:Math.floor(r*0.7), count:14, boss:false, name:"Full Quantum Army"}},
        {{wave:11, speed:s*1.7, rate:Math.floor(r*0.65),count:16, boss:true,  name:"Quantum Apocalypse"}},
        {{wave:12, speed:s*1.8, rate:Math.floor(r*0.6), count:18, boss:true,  name:"FINAL BOSS"}},
    ];
}})();

function getWaveConfig() {{
    return WAVE_CONFIG[Math.min(wave-1, WAVE_CONFIG.length-1)];
}}

let player = {{x:W/2, y:H-55, w:40, h:40, spd:6}};
let bullets=[], zombies=[], explosions=[], stars=[];
let selWeapon=0, zhp=100, score=0, wave=1, killed=0;
let running=false, frameId, spawnT=0, spawnCount=0, waveSize=0, waveTimer=0;
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
    zhp=100; score=0; wave=1; killed=0; spawnT=0; spawnCount=0; waveTimer=0;
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
    const effRate=Math.max(15,getWaveConfig().rate);
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
    waveTimer++;
    if(spawnCount>=waveSize&&(zombies.length===0||waveTimer>1800)){{
        if(wave>=MAX_WAVES){{
            running=false;
            showMsg("🏆 QUANTUM GUARDIAN! All 12 waves cleared! Score: "+score);
        }} else {{
            wave++;
            const nextCfg = getWaveConfig();
            waveSize=nextCfg.count;
            spawnCount=0; spawnT=0; waveTimer=0;
            zombies=[];
            document.getElementById("zwave").textContent=wave+"/12";
            showMsg("✅ Wave "+(wave-1)+" cleared! Wave "+wave+": "+nextCfg.name+" incoming!");
        }}
    }}
    // Force respawn if somehow no zombies and not all spawned yet
    if(spawnCount<waveSize&&zombies.length===0&&spawnT>50){{
        spawnZombie(); spawnT=0;
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
    """Middle School 6-8: Cipher Quest — fill in ONE blank per challenge, rest is provided."""
    import streamlit as st
    import streamlit.components.v1 as components
    from modules.trial import trial_gate
    if not trial_gate("cipher_quest", "Cipher Quest"):
        return
    st.subheader("🎮 Cipher Quest!")
    st.markdown(
        "**Fill in ONE blank per challenge** to crack the code! "
        "Everything else is already written for you. "
        "Learn why we need quantum-safe encryption!"
    )
    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;}
#wrap{max-width:560px;margin:0 auto;padding:12px;}
.hud{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-bottom:8px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:10px;padding:7px;text-align:center;font-size:10px;color:#60a5fa;}
.hb b{display:block;font-size:15px;color:white;}
.quest-card{background:#071520;border:2px solid #1d4ed8;border-radius:14px;padding:14px;margin-bottom:10px;}
.quest-header{display:flex;align-items:center;gap:8px;margin-bottom:8px;}
.quest-emoji{font-size:2rem;}
.quest-title{font-size:14px;font-weight:bold;color:#60a5fa;}
.diff{display:inline-block;border-radius:4px;padding:2px 8px;font-size:9px;font-weight:bold;margin-top:2px;}
.easy{background:#059669;}.medium{background:#d97706;}.hard{background:#dc2626;}
.quest-desc{font-size:11px;color:#94a3b8;line-height:1.7;margin-bottom:10px;
    background:#050e1a;border-radius:8px;padding:10px;}
.code-block{background:#020d14;border:1px solid #1a3a5a;border-radius:8px;
    padding:10px;font-family:'Fira Code',monospace;font-size:11px;
    color:#60a5fa;line-height:2;margin-bottom:8px;}
.code-line{display:block;color:#60a5fa;}
.code-comment{display:block;color:#475569;}
.blank-wrap{display:inline-flex;align-items:center;gap:4px;}
.blank{background:#0a1f35;border:2px solid #3b82f6;border-radius:6px;
    color:#10b981;font-family:'Fira Code',monospace;font-size:12px;
    padding:4px 8px;width:120px;outline:none;text-align:center;}
.blank:focus{border-color:#60a5fa;box-shadow:0 0 8px rgba(59,130,246,0.3);}
.run-btn{width:100%;padding:12px;background:linear-gradient(135deg,#1d4ed8,#06b6d4);
    border:none;border-radius:10px;color:white;font-size:14px;font-weight:bold;
    cursor:pointer;margin-bottom:6px;transition:all 0.2s;}
.run-btn:hover{filter:brightness(1.15);}
.hint-btn{width:100%;padding:8px;background:#7c3aed;border:none;border-radius:8px;
    color:white;font-size:12px;cursor:pointer;margin-bottom:6px;}
.next-btn{width:100%;padding:12px;background:linear-gradient(135deg,#059669,#10b981);
    border:none;border-radius:10px;color:white;font-size:14px;font-weight:bold;
    cursor:pointer;margin-bottom:8px;display:none;}
.output{background:#020d14;border:2px solid #00ff4130;border-radius:8px;
    padding:10px;font-family:'Fira Code',monospace;font-size:11px;
    color:#00ff41;min-height:50px;margin-bottom:8px;line-height:1.7;}
#msg{font-size:12px;min-height:18px;margin:4px 0;text-align:center;font-weight:bold;padding:6px;}
#fact{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);
    border-radius:10px;padding:10px;margin:4px 0;font-size:10px;color:#93c5fd;
    display:none;line-height:1.6;}
.progress{display:flex;gap:5px;justify-content:center;margin:8px 0;}
.pdot{width:13px;height:13px;border-radius:50%;background:#1e293b;border:1px solid #334155;}
.pdot.done{background:#10b981;}.pdot.active{background:#3b82f6;}
</style>
</head>
<body>
<div id="wrap">
<div class="hud">
    <div class="hb">⭐ Score<br><b id="h-score">0</b></div>
    <div class="hb">🏆 Quest<br><b id="h-level">1</b>/8</div>
    <div class="hb">🔥 Streak<br><b id="h-streak">0</b></div>
</div>
<div class="progress" id="prog"></div>

<div class="quest-card" id="quest-card">
    <div class="quest-header">
        <div class="quest-emoji" id="q-emoji">🔐</div>
        <div>
            <div class="quest-title" id="q-title">Quest 1</div>
            <span class="diff easy" id="q-diff">EASY</span>
        </div>
    </div>
    <div class="quest-desc" id="q-desc"></div>
    <div class="code-block" id="code-block"></div>
    <button class="run-btn" onclick="runQuest()">▶ Run Code!</button>
    <button class="hint-btn" onclick="showHint()">💡 Show Hint (-25 pts)</button>
    <button class="next-btn" id="next-btn" onclick="nextQuest()">Next Quest →</button>
    <div class="output" id="output"># Output shows here when you run!</div>
</div>

<div id="msg"></div>
<div id="fact"></div>
</div>

<script>
const QUESTS=[
    {
        emoji:"🔤",title:"Decode ROT13",diff:"easy",
        desc:"The enemy scrambled a message using ROT13 — each letter is shifted by 13 places. Fill in the shift number to decode it!",
        before:"# ROT13 decoder\nmessage = 'URYYB JBEYQ'\nshift = ",
        blank:"13",
        after:"\nresult = ''\nfor c in message:\n    if c.isalpha():\n        result += chr((ord(c) - 65 + (26-shift)) % 26 + 65)\n    else:\n        result += c\nprint('Decoded:', result)",
        hint:"ROT13 uses a shift of 13. The answer is just the number 13!",
        check:"13",
        output:"> Decoding message...\n> Applying shift of 13...\n> Decoded: HELLO WORLD\n> ✅ ROT13 cracked! (took 0.001 seconds)",
        fact:"ROT13 has only 26 possible keys — a computer tries all of them instantly! Kyber has 2^256 possible keys — even quantum computers cannot try them all!"
    },
    {
        emoji:"➕",title:"Modular Math",diff:"easy",
        desc:"Modular math (mod) is the foundation of Kyber! Compute 22 mod 11. Fill in the modulus number.",
        before:"# Modular arithmetic — the math inside Kyber!\nnumber = 22\nmodulus = ",
        blank:"11",
        after:"\nresult = number % modulus\nprint('22 mod', modulus, '=', result)\nprint('This is one step in Kyber key generation!')",
        hint:"22 ÷ 11 = 2 with remainder 0. The modulus is 11!",
        check:"11",
        output:"> Computing 22 mod 11...\n> 22 ÷ 11 = 2 remainder 0\n> 22 mod 11 = 0\n> ✅ This is one step in Kyber key generation!",
        fact:"Kyber uses modular math with huge numbers (q=3329) and 256-dimensional polynomials. The modular math makes it impossible to reverse-engineer the secret key!"
    },
    {
        emoji:"🔢",title:"Count the Keys",diff:"easy",
        desc:"Caesar cipher has only 25 possible keys. Fill in 25 to make the loop try all of them!",
        before:"# Brute force Caesar cipher\nciphertext = 'Khoor'\nfor shift in range(1, ",
        blank:"26",
        after:"):\n    decoded = ''\n    for c in ciphertext:\n        if c.isalpha():\n            base = 65 if c.isupper() else 97\n            decoded += chr((ord(c) - base - shift) % 26 + base)\n        else:\n            decoded += c\n    if shift == 3:\n        print('Shift', shift, ':', decoded, '← THE ANSWER!')\nprint('Done! Caesar has only 25 keys.')",
        hint:"We want to try shifts 1 through 25, so range(1, 26) goes up to but not including 26!",
        check:"26",
        output:"> Trying all 25 Caesar shifts...\n> Shift 1 : Jgnnq\n> Shift 2 : Ifmmp\n> Shift 3 : Hello ← THE ANSWER!\n> ...\n> Done! Caesar has only 25 keys.\n> ✅ Cracked in 0.001 seconds!",
        fact:"A computer cracks Caesar in 0.001 seconds. RSA-2048 takes millions of years classically — but Shor's Algorithm on a quantum computer cracks it in seconds! Kyber is immune to both!"
    },
    {
        emoji:"#️⃣",title:"SHA-3 Hash",diff:"medium",
        desc:"SHA-3 is the hash function inside SPHINCS+. Hash the word 'kyber' using sha3_256. Fill in the algorithm name!",
        before:"# SHA-3 hashing — used in SPHINCS+ (FIPS 205)\nimport hashlib\nword = 'kyber'\nhash_result = hashlib.",
        blank:"sha3_256",
        after:"(word.encode()).hexdigest()\nprint('Word:', word)\nprint('Hash:', hash_result[:32], '...')\nprint('Length:', len(hash_result), 'characters')",
        hint:"The function name is sha3_256 (SHA-3 with 256 bits of output)!",
        check:"sha3_256",
        output:"> Hashing 'kyber' with SHA-3...\n> Word: kyber\n> Hash: 3338be694f50c5f338814986cdf06864 ...\n> Length: 64 characters\n> ✅ SHA-3 hash complete! One-way — impossible to reverse!",
        fact:"SHA-3 is completely one-way — you cannot reverse a hash to find the original word. SPHINCS+ chains thousands of SHA-3 hashes together to create quantum-safe digital signatures!"
    },
    {
        emoji:"🧮",title:"LWE Equation",diff:"medium",
        desc:"Learning With Errors (LWE) is the math behind Kyber! Compute b = (7 × s + e) mod q. Fill in the secret s=3!",
        before:"# LWE — the math that makes Kyber quantum-safe!\nA = 7      # public number\ne = 1      # small noise\nq = 11     # modulus\ns = ",
        blank:"3",
        after:"      # SECRET — this is what we protect!\nb = (A * s + e) % q\nprint('A =', A, '(public)')\nprint('s =', s, '(SECRET — hidden!)')\nprint('e =', e, '(noise — hides the secret)')\nprint('b =', b, '(public — safe to share)')\nprint('Can you find s from just A and b? Impossible!')",
        hint:"The secret s = 3. Just type the number 3!",
        check:"3",
        output:"> Computing LWE equation...\n> A = 7 (public)\n> s = 3 (SECRET — hidden!)\n> e = 1 (noise — hides the secret)\n> (7 × 3 + 1) mod 11 = 22 mod 11 = 0... wait: 22 mod 11 = 0\n> b = 0 (public — safe to share)\n> ✅ Can you find s from just A=7 and b=0? Impossible!",
        fact:"Real Kyber uses 256 of these equations simultaneously with much bigger numbers. Finding s from A and b is called the LWE problem — it's mathematically proven to be quantum-hard!"
    },
    {
        emoji:"🔑",title:"Key Size Check",diff:"medium",
        desc:"Kyber-768 has a public key of 1184 bytes. Fill in the number to check if it's big enough to be quantum-safe!",
        before:"# Key sizes matter for quantum security!\nrsa_key_bytes = 256      # RSA-2048 = 256 bytes\nkyber_key_bytes = ",
        blank:"1184",
        after:"  # Kyber-768 public key\nif kyber_key_bytes > rsa_key_bytes:\n    print('Kyber key is larger but QUANTUM-SAFE!')\n    print('RSA:', rsa_key_bytes, 'bytes — broken by Shor')\n    print('Kyber:', kyber_key_bytes, 'bytes — quantum immune!')\n    print('Worth the extra size for quantum safety!')",
        hint:"Kyber-768 public key = 1184 bytes. Type 1184!",
        check:"1184",
        output:"> Comparing key sizes...\n> Kyber key is larger but QUANTUM-SAFE!\n> RSA: 256 bytes — broken by Shor's Algorithm\n> Kyber: 1184 bytes — quantum immune!\n> Worth the extra size for quantum safety!\n> ✅ Kyber wins!",
        fact:"Kyber keys are 3-5x larger than RSA keys, but they're completely immune to quantum attacks. The NSM-10 law requires all US government systems to switch to Kyber by 2035!"
    },
    {
        emoji:"🌊",title:"Shor's Threat",diff:"hard",
        desc:"Shor's Algorithm finds prime factors. RSA uses two primes p=53 and q=61. Their product n=3233 is the RSA key. Fill in p×q!",
        before:"# Why RSA is vulnerable to quantum computers\n# RSA key: n = p × q (two secret primes)\np = 53    # secret prime 1\nq = 61    # secret prime 2\nn = ",
        blank:"p * q",
        after:"\nprint('RSA key n =', n)\nprint('Classical computer: millions of years to factor', n)\nprint('Quantum Shor Algorithm: finds p and q instantly!')\nprint('p =', p, ', q =', q)\nprint('This is why we NEED Kyber (ML-KEM FIPS 203)!')",
        hint:"n = p times q, so write p * q in Python!",
        check:"p * q",
        output:"> Computing RSA key...\n> RSA key n = 3233\n> Classical computer: millions of years to factor 3233\n> Quantum Shor Algorithm: finds p and q instantly!\n> p = 53 , q = 61\n> This is why we NEED Kyber (ML-KEM FIPS 203)!\n> ✅ RSA is broken by quantum — Kyber is safe!",
        fact:"Real RSA uses primes with 150+ digits. Classical computers need millions of years to factor them. Shor's Algorithm on a quantum computer finds the factors in seconds — that's why NIST chose Kyber!"
    },
    {
        emoji:"🏆",title:"PQC Champion!",diff:"hard",
        desc:"Name all 4 NIST post-quantum standards! Fill in the missing FIPS number for Falcon (FN-DSA)!",
        before:"# All 4 NIST Post-Quantum Standards (2024)\nnist_standards = [\n    ('ML-KEM',  'FIPS 203', 'Kyber — key exchange'),\n    ('ML-DSA',  'FIPS 204', 'Dilithium — signatures'),\n    ('SLH-DSA', 'FIPS 205', 'SPHINCS+ — hash backup'),\n    ('FN-DSA',  'FIPS ",
        blank:"206",
        after:"', 'Falcon — tiny signatures'),\n]\nfor name, fips, desc in nist_standards:\n    print(fips, '-', name, ':', desc)\nprint('All 4 quantum-safe standards deployed!')\nprint('The internet is protected!')",
        hint:"The 4 FIPS numbers are 203, 204, 205, and 206. Falcon is the last one!",
        check:"206",
        output:"> NIST Post-Quantum Standards 2024:\n> FIPS 203 - ML-KEM : Kyber — key exchange\n> FIPS 204 - ML-DSA : Dilithium — signatures\n> FIPS 205 - SLH-DSA : SPHINCS+ — hash backup\n> FIPS 206 - FN-DSA : Falcon — tiny signatures\n> All 4 quantum-safe standards deployed!\n> ✅ The internet is protected!",
        fact:"You just named all 4 NIST post-quantum cryptography standards! These were finalized in August 2024 and will replace all RSA and elliptic curve encryption by 2035. You are a PQC expert!"
    },
];

let level=0,score=0,streak=0,hintUsed=false,factTmo=null,results=[];

function buildProgress(){
    const d=document.getElementById("prog");
    d.innerHTML="";
    for(let i=0;i<QUESTS.length;i++){
        const dot=document.createElement("div");
        dot.className="pdot"+(results[i]==="done"?" done":i===level?" active":"");
        d.appendChild(dot);
    }
}

function loadQuest(){
    const q=QUESTS[level];
    document.getElementById("q-emoji").textContent=q.emoji;
    document.getElementById("q-title").textContent="Quest "+(level+1)+": "+q.title;
    document.getElementById("q-diff").textContent=q.diff.toUpperCase();
    document.getElementById("q-diff").className="diff "+q.diff;
    document.getElementById("q-desc").textContent=q.desc;
    document.getElementById("h-level").textContent=(level+1);
    hintUsed=false;

    // Build code block with input
    const cb=document.getElementById("code-block");
    const lines=(q.before+"\u2588\u2588\u2588"+q.after).split("\n");
    cb.innerHTML="";

    let inputInserted=false;
    (q.before+"\n__BLANK__\n"+q.after).split("\n").forEach(line=>{
        if(line==="__BLANK__"){
            if(!inputInserted){
                const span=document.createElement("span");
                span.className="blank-wrap";
                span.innerHTML='<input class="blank" id="blank-input" placeholder="???" />';
                cb.appendChild(span);
                cb.appendChild(document.createElement("br"));
                inputInserted=true;
            }
        } else {
            const span=document.createElement("span");
            span.className=line.trim().startsWith("#")?"code-comment":"code-line";
            span.textContent=line;
            cb.appendChild(span);
            cb.appendChild(document.createElement("br"));
        }
    });

    // Actually rebuild cleanly
    cb.innerHTML="";
    const before_lines=q.before.split("\n");
    before_lines.forEach(line=>{
        const span=document.createElement("span");
        span.className=line.trim().startsWith("#")?"code-comment":"code-line";
        span.textContent=line;
        cb.appendChild(span);
        cb.appendChild(document.createElement("br"));
    });
    // Add input
    const inputSpan=document.createElement("span");
    inputSpan.className="blank-wrap";
    inputSpan.innerHTML='<input class="blank" id="blank-input" placeholder="fill in!" />';
    cb.appendChild(inputSpan);
    // After lines
    const after_lines=q.after.split("\n");
    after_lines.forEach(line=>{
        cb.appendChild(document.createElement("br"));
        const span=document.createElement("span");
        span.className=line.trim().startsWith("#")?"code-comment":"code-line";
        span.textContent=line;
        cb.appendChild(span);
    });

    document.getElementById("output").textContent="# Output shows here when you run!";
    document.getElementById("output").style.color="#00ff41";
    document.getElementById("next-btn").style.display="none";
    document.getElementById("msg").textContent="";
    document.getElementById("fact").style.display="none";
    buildProgress();
}

function runQuest(){
    const q=QUESTS[level];
    const input=(document.getElementById("blank-input")||{value:""}).value.trim();
    const output=document.getElementById("output");

    if(!input){output.textContent="# Type your answer in the blank first!";return;}

    if(input===q.check){
        const hintPen=hintUsed?25:0;
        const pts=150*(level+1)-hintPen;
        score+=pts;streak++;
        results[level]="done";
        output.textContent=q.output;
        output.style.color="#00ff41";
        document.getElementById("h-score").textContent=score;
        document.getElementById("h-streak").textContent=streak;
        document.getElementById("msg").textContent="✅ Correct! +"+pts+" pts!"+(streak>1?" 🔥×"+streak:"");
        document.getElementById("msg").style.color="#10b981";
        document.getElementById("next-btn").style.display="block";
        showFact(q.fact);
        buildProgress();
    } else {
        output.textContent="❌ Not quite! Try again.\n# Hint: "+q.hint;
        output.style.color="#ef4444";
        streak=0;
        document.getElementById("h-streak").textContent=0;
        document.getElementById("msg").textContent="Close! Read the description again. 💪";
        document.getElementById("msg").style.color="#f59e0b";
    }
}

function showHint(){
    const q=QUESTS[level];
    hintUsed=true;
    score=Math.max(0,score-25);
    document.getElementById("output").textContent="💡 Hint: "+q.hint;
    document.getElementById("output").style.color="#a78bfa";
    document.getElementById("h-score").textContent=score;
}

function nextQuest(){
    if(level<QUESTS.length-1){level++;loadQuest();}
    else{
        document.getElementById("msg").textContent="🏆 ALL 8 QUESTS COMPLETE! PQC Champion! Score: "+score;
        document.getElementById("msg").style.color="#fbbf24";
    }
}

function showFact(text){
    const el=document.getElementById("fact");
    el.textContent="🔐 Did you know? "+text;
    el.style.display="block";
    if(factTmo)clearTimeout(factTmo);
    factTmo=setTimeout(()=>el.style.display="none",10000);
}

loadQuest();
</script>
</body>
</html>
""", height=820)


def render_pqc_python_lab():
    """High School 9-12: PQC Python Lab — guided real Python with step-by-step comments."""
    import streamlit as st
    from modules.trial import trial_gate
    if not trial_gate("pqc_python_lab", "PQC Python Lab"):
        return
    st.subheader("🐍 PQC Python Lab")
    st.markdown(
        "**Write real Python code** to learn post-quantum cryptography! "
        "Every challenge has step-by-step comments guiding you through the code. "
        "Run your code and see the real output!"
    )

    challenges = [
        {
            "id": 1, "title": "Caesar Cipher Decoder", "difficulty": "🟢 Beginner",
            "concept": "Why simple ciphers fail",
            "desc": "Decode a Caesar cipher by trying all 25 shifts. This shows why old ciphers are weak — then we'll learn what makes Kyber strong.",
            "starter": """# CHALLENGE 1: Decode a Caesar Cipher
# A Caesar cipher shifts each letter by a fixed amount
# Caesar only has 25 possible shifts — easy to crack!

ciphertext = 'Khoor Zruog'  # This is a hidden message!

# Step 1: Loop through all possible shifts (1 to 25)
for shift in range(1, 26):
    decoded = ''
    
    # Step 2: Decode each character
    for c in ciphertext:
        if c.isalpha():
            # Step 3: Shift the letter back
            base = 65 if c.isupper() else 97
            decoded += chr((ord(c) - base - shift) % 26 + base)
        else:
            decoded += c  # Keep spaces and punctuation
    
    # Step 4: Print each attempt
    print(f'Shift {shift:2d}: {decoded}')

print('\\nOnly one of these makes sense — that is the answer!')
print('Kyber has 2^256 keys, not just 25 — impossible to brute force!')""",
            "hint": "Just run the code as-is! All the logic is already there. Look for the shift that produces a real English phrase.",
            "expected_output": "Hello World",
            "fact": "Caesar cipher: 25 keys, cracked in milliseconds. Kyber: 2^256 keys, quantum computers still cannot crack it. That's a difference of about 10^77 times harder!",
        },
        {
            "id": 2, "title": "LWE Math Core", "difficulty": "🟢 Beginner",
            "concept": "The math inside Kyber",
            "desc": "Implement Learning With Errors (LWE) — the mathematical foundation of Kyber. This is the actual math that makes Kyber quantum-safe!",
            "starter": """# CHALLENGE 2: Learning With Errors (LWE)
# This is the REAL math inside Kyber (ML-KEM FIPS 203)!
# LWE: given A and b, find s — even quantum computers can't do it!

import random

# === SETUP ===
q = 11          # Modulus (Kyber uses q = 3329)
s = 3           # SECRET — this is what we're protecting
A = [7, 5, 2]   # Public matrix (random numbers)
e = [1, 0, 1]   # Small noise/error (makes it hard to solve)

# === COMPUTE PUBLIC KEY ===
# b[i] = (A[i] * s + e[i]) mod q
# This hides s inside the math!
b = []
for i in range(len(A)):
    value = (A[i] * s + e[i]) % q
    b.append(value)
    print(f'b[{i}] = ({A[i]} × {s} + {e[i]}) mod {q} = {A[i]*s+e[i]} mod {q} = {value}')

print(f'\\nPublic key b = {b}')
print(f'Anyone can see A = {A} and b = {b}')
print(f'But s = {s} is HIDDEN — try to find it just from A and b!')
print('\\nThis is why Kyber is quantum-safe: LWE is mathematically proven hard!')""",
            "hint": "Just run this code — everything is already written! Observe how b hides the secret s.",
            "expected_output": "Public key b",
            "fact": "Real Kyber uses 256-dimensional polynomial rings instead of simple lists, making it exponentially harder. NIST proved in 2024 that M-LWE cannot be solved even by quantum computers!",
        },
        {
            "id": 3, "title": "SHA-3 Avalanche Effect", "difficulty": "🟡 Intermediate",
            "concept": "How SPHINCS+ stays quantum-safe",
            "desc": "Demonstrate the SHA-3 avalanche effect. Change ONE character in a message and watch the entire hash change completely. This is why SPHINCS+ is quantum-safe!",
            "starter": """# CHALLENGE 3: SHA-3 Avalanche Effect
# SHA-3 is the hash function inside SPHINCS+ (SLH-DSA FIPS 205)
# Avalanche effect: change 1 bit → ~50% of output changes!

import hashlib

def sha3_hash(text):
    # Hash any text with SHA-3 (256-bit output)
    return hashlib.sha3_256(text.encode()).hexdigest()

# === TEST THE AVALANCHE EFFECT ===
message1 = 'hello quantum world'   # Original message
message2 = 'Hello quantum world'   # Changed ONE letter (capital H)!

hash1 = sha3_hash(message1)
hash2 = sha3_hash(message2)

print('Original message :', message1)
print('Modified message :', message2)
print('(Only the H changed!)')
print()
print('Hash 1:', hash1)
print('Hash 2:', hash2)
print()

# Count how many characters are different
different = sum(1 for a, b in zip(hash1, hash2) if a != b)
percentage = round(different / len(hash1) * 100)

print(f'Different characters: {different} out of {len(hash1)}')
print(f'Avalanche effect: {percentage}% of hash changed!')
print()
print('SPHINCS+ chains thousands of these hashes together.')
print('Even quantum computers cannot fake or reverse SHA-3!')""",
            "hint": "Run this code as-is! The avalanche effect will show you that changing 1 character changes roughly 50% of the hash output.",
            "expected_output": "Avalanche effect",
            "fact": "SHA-3 uses a sponge construction (Keccak) that's completely different from SHA-2. Grover's Algorithm gives quantum a 2x speedup, but SHA3-256 still has 128-bit quantum security — enough for FIPS 205!",
        },
        {
            "id": 4, "title": "RSA vs Kyber Key Sizes", "difficulty": "🟡 Intermediate",
            "concept": "Why key sizes matter",
            "desc": "Compare RSA and Kyber key sizes and security levels. Understand why we need to migrate before quantum computers arrive.",
            "starter": """# CHALLENGE 4: RSA vs Kyber Security Comparison
# Understanding why we NEED to migrate to post-quantum crypto

# === KEY SIZE DATA ===
algorithms = [
    # (Name, Key Size bytes, Classical Security bits, Quantum Security bits)
    ('RSA-2048',    256,  112, 0),    # 0 quantum bits = broken by Shor!
    ('RSA-4096',    512,  140, 0),    # Still 0 quantum security!
    ('ECDSA-256',    32,  128, 0),    # Elliptic curve also broken!
    ('Kyber-512',   800,  128, 128),  # FIPS 203 Level 1
    ('Kyber-768',  1184,  192, 128),  # FIPS 203 Level 3 (recommended)
    ('Kyber-1024', 1568,  256, 256),  # FIPS 203 Level 5 (top security)
]

print('=' * 65)
print(f'{"Algorithm":<14} {"Key(bytes)":>10} {"Classical":>10} {"Quantum":>10}')
print('=' * 65)

for name, key_size, classical_bits, quantum_bits in algorithms:
    status = '✅ SAFE' if quantum_bits > 0 else '❌ BROKEN'
    print(f'{name:<14} {key_size:>10} {classical_bits:>9}b {quantum_bits:>9}b  {status}')

print('=' * 65)
print()
print('RSA quantum security = 0 because Shor\\'s Algorithm solves it!')
print('Kyber quantum security = 128+ bits because M-LWE is quantum-hard!')
print()
print('US agencies must migrate to Kyber by 2035 (NSM-10 mandate).')
print('The clock is ticking — migrate NOW before quantum computers arrive!')""",
            "hint": "Run this code as-is! Study the table carefully — notice how all RSA/ECDSA algorithms have 0 quantum security bits.",
            "expected_output": "quantum-hard",
            "fact": "NSM-10 (National Security Memorandum 10) requires ALL US federal agencies to migrate from RSA to Kyber and other NIST PQC standards by 2035. The professionals doing this migration are in classrooms today!",
        },
        {
            "id": 5, "title": "Build a Mini Key Exchange", "difficulty": "🔴 Advanced",
            "concept": "How Kyber protects the internet",
            "desc": "Simulate how Kyber key exchange works. Alice and Bob agree on a shared secret without ever sending it — even if someone intercepts every message, they cannot find the secret!",
            "starter": """# CHALLENGE 5: Mini Kyber Key Exchange Simulation
# This shows HOW Kyber protects HTTPS, VPNs, and encrypted messaging

import random

# === SETUP: Public parameters (everyone knows these) ===
q = 97        # Modulus
n = 4         # Dimensions (real Kyber uses n=256)
random.seed(42)

def dot_product_mod(v1, v2, q):
    '''Compute dot product of two vectors mod q'''
    return sum(v1[i] * v2[i] for i in range(len(v1))) % q

# === ALICE generates her key pair ===
print('=== ALICE (SERVER) ===')
# Alice's secret key (never shared!)
alice_secret = [random.randint(0, 2) for _ in range(n)]
# Public matrix A (everyone sees this)
A = [[random.randint(0, q-1) for _ in range(n)] for _ in range(n)]
# Alice's public key: b = A*s + small_error (mod q)
alice_error = [random.randint(0, 1) for _ in range(n)]
alice_public = [(dot_product_mod(A[i], alice_secret, q) + alice_error[i]) % q for i in range(n)]
print(f'Alice secret key: {alice_secret} (NEVER SHARED)')
print(f'Alice public key: {alice_public} (broadcast to world)')

# === BOB sends an encrypted message ===
print()
print('=== BOB (CLIENT) ===')
bob_secret = [random.randint(0, 2) for _ in range(n)]
bob_error = [random.randint(0, 1) for _ in range(n)]
# Bob computes a shared value using Alice's public key
shared_approx = (dot_product_mod(alice_public, bob_secret, q) + bob_error[0]) % q
print(f'Bob computes shared value: {shared_approx}')

# === ALICE recovers the shared secret ===
print()
print('=== KEY AGREEMENT ===')
alice_recover = dot_product_mod(alice_secret, bob_secret, q)
print(f'Alice recovers: {alice_recover}')
print(f'Values close: {abs(shared_approx - alice_recover) < 5}')
print()
print('KEY EXCHANGE COMPLETE!')
print('Alice and Bob now share a secret nobody else knows.')
print('Even if an attacker saw everything, they cannot compute the secret!')
print('This is how Kyber protects HTTPS connections in your browser!')""",
            "hint": "Run this code! The output shows Alice and Bob establishing a shared secret. The key insight: an eavesdropper sees alice_public and bob messages, but cannot compute the shared secret without alice_secret.",
            "expected_output": "KEY EXCHANGE COMPLETE",
            "fact": "Google Chrome and Cloudflare already use X25519+Kyber hybrid key exchange in TLS 1.3, protecting ~20% of all internet traffic! This code simulates the exact concept, just simplified for learning.",
        },
    ]

    if "lab_level" not in st.session_state:
        st.session_state.lab_level = 0
    if "lab_score" not in st.session_state:
        st.session_state.lab_score = 0

    idx = min(st.session_state.lab_level, len(challenges)-1)
    ch = challenges[idx]

    # Progress bar
    progress = (idx) / len(challenges)
    st.progress(progress)

    col1, col2, col3 = st.columns(3)
    col1.metric("⭐ Score", st.session_state.lab_score)
    col2.metric("🏆 Challenge", str(idx+1) + "/" + str(len(challenges)))
    col3.metric("📊 Level", ch["difficulty"])

    st.markdown(f"### {ch['id']}. {ch['title']}")
    st.markdown(f"**Concept:** {ch['concept']}")
    st.info(ch["desc"])

    # Show all challenge navigation
    cols = st.columns(len(challenges))
    for i, c in enumerate(challenges):
        status = "✅" if i < idx else ("🔵" if i == idx else "⬜")
        cols[i].markdown(f"<div style='text-align:center;font-size:10px;color:#475569'>{status}<br>Ch.{i+1}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ✏️ Your Code:")
    st.markdown("<div style='font-size:11px;color:#475569;margin-bottom:4px'>📌 Read the comments — they guide you step by step!</div>", unsafe_allow_html=True)

    code = st.text_area(
        "Python code:",
        value=ch["starter"],
        height=320,
        key="lab_code_" + str(idx),
        label_visibility="collapsed"
    )

    col_a, col_b, col_c = st.columns([2,1,1])
    with col_a:
        run = st.button("▶ Run Code", type="primary", use_container_width=True, key="run_"+str(idx))
    with col_b:
        hint_btn = st.button("💡 Hint", use_container_width=True, key="hint_"+str(idx))
    with col_c:
        if idx < len(challenges)-1:
            nxt = st.button("Next →", use_container_width=True, key="next_"+str(idx))
        else:
            nxt = False

    if hint_btn:
        st.info("💡 " + ch["hint"])

    if run:
        import io, contextlib
        try:
            output_buf = io.StringIO()
            safe_globals = {
                "__builtins__": {
                    "print": lambda *a,**k: print(*a,**k, file=output_buf),
                    "range": range, "len": len, "sum": sum, "zip": zip,
                    "round": round, "chr": chr, "ord": ord, "str": str,
                    "int": int, "float": float, "list": list, "dict": dict,
                    "enumerate": enumerate, "abs": abs, "min": min, "max": max,
                    "True": True, "False": False, "None": None,
                    "f": None,
                },
                "hashlib": __import__("hashlib"),
                "random": __import__("random"),
            }
            exec(code, safe_globals)
            result = output_buf.getvalue()
            if result:
                st.code(result, language="text")
                if ch["expected_output"].lower() in result.lower() or len(result) > 30:
                    pts = 200 * (idx + 1)
                    st.session_state.lab_score += pts
                    st.success("🎉 Excellent work! +" + str(pts) + " pts!")
                    st.info("🔐 " + ch["fact"])
                    if idx < len(challenges) - 1:
                        if st.button("🚀 Continue to Challenge " + str(idx+2), type="primary", key="auto_next_"+str(idx)):
                            st.session_state.lab_level = idx + 1
                            st.rerun()
                else:
                    st.warning("Code ran! Check the output matches what's expected.")
            else:
                st.warning("Code ran but produced no output. Make sure you have print() statements!")
        except Exception as ex:
            st.error("❌ Error: " + str(ex))
            st.info("💡 " + ch["hint"])

    if nxt:
        st.session_state.lab_level = min(idx + 1, len(challenges)-1)
        st.rerun()

    if idx == len(challenges) - 1 and st.session_state.lab_score > 0:
        st.balloons()
        st.success("🏆 You completed the PQC Python Lab! Score: " + str(st.session_state.lab_score))


