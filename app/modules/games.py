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
    """Free game: Prime Factorization — Break RSA before Shor does!"""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("🔢 Prime Factor Cracker — Break RSA!")
    st.markdown(
        "**RSA encryption** is secured by one hard problem: factoring large numbers. "
        "Find the two prime factors before the Quantum Monster (Shor\'s Algorithm) does! "
        "This is FREE for everyone — no account needed!"
    )
    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;}
#wrap{display:flex;flex-direction:column;align-items:center;padding:12px;max-width:540px;margin:0 auto;}
.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;width:100%;margin-bottom:8px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:6px 4px;
    text-align:center;font-size:10px;color:#60a5fa;}
.hb b{display:block;font-size:16px;color:white;}
#main-card{background:#071520;border:2px solid #1d4ed8;border-radius:16px;
    padding:20px;width:100%;text-align:center;margin-bottom:10px;}
#number-display{font-size:3rem;font-weight:900;color:#60a5fa;margin:10px 0;
    text-shadow:0 0 20px rgba(59,130,246,0.5);}
#challenge-text{font-size:12px;color:#94a3b8;margin-bottom:12px;}
.input-row{display:flex;gap:8px;justify-content:center;align-items:center;margin:10px 0;flex-wrap:wrap;}
.factor-input{background:#0a1f35;border:2px solid #1d4ed8;border-radius:8px;
    color:white;font-size:1.2rem;font-weight:bold;text-align:center;
    padding:8px;width:90px;outline:none;}
.factor-input:focus{border-color:#60a5fa;box-shadow:0 0 12px rgba(59,130,246,0.3);}
.mult-sign{font-size:1.5rem;color:#475569;}
#check-btn{padding:10px 24px;border-radius:8px;border:none;cursor:pointer;
    background:linear-gradient(135deg,#1d4ed8,#06b6d4);color:white;
    font-size:14px;font-weight:bold;transition:all 0.2s;}
#check-btn:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(59,130,246,0.4);}
#msg{font-size:13px;min-height:20px;margin:8px;text-align:center;font-weight:bold;}
#fact-box{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);
    border-radius:10px;padding:10px 14px;margin:6px 0;font-size:11px;color:#93c5fd;
    display:none;line-height:1.6;width:100%;}
#shor-bar-wrap{width:100%;margin:8px 0;}
#shor-label{font-size:10px;color:#ef4444;margin-bottom:3px;display:flex;justify-content:space-between;}
#shor-bar{height:14px;background:#1e293b;border-radius:7px;overflow:hidden;border:1px solid #334155;}
#shor-fill{height:100%;width:0%;background:linear-gradient(90deg,#ef4444,#f97316);
    border-radius:7px;transition:width 0.5s;}
.hint-btn{padding:5px 12px;border-radius:6px;border:1px solid #334155;
    background:#071520;color:#60a5fa;font-size:11px;cursor:pointer;margin:3px;}
.hint-btn:hover{background:#0a1f35;border-color:#1d4ed8;}
#hints-used{font-size:10px;color:#475569;text-align:center;}
.level-badge{display:inline-block;background:linear-gradient(135deg,#1d4ed8,#7c3aed);
    border-radius:20px;padding:3px 12px;font-size:11px;font-weight:bold;margin-bottom:8px;}
#btn-row{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin:8px 0;}
.btn{padding:8px 18px;border-radius:8px;border:none;cursor:pointer;
    font-size:12px;font-weight:bold;color:white;}
.btn-start{background:#1d4ed8;}
.btn-next{background:#059669;}
.btn-next:disabled{background:#1e293b;color:#475569;cursor:not-allowed;}
.btn-hint{background:#7c3aed;}
#progress-dots{display:flex;gap:6px;justify-content:center;margin:8px 0;flex-wrap:wrap;}
.dot{width:12px;height:12px;border-radius:50%;background:#1e293b;border:1px solid #334155;}
.dot.done{background:#10b981;border-color:#10b981;}
.dot.current{background:#3b82f6;border-color:#60a5fa;box-shadow:0 0 6px rgba(59,130,246,0.5);}
.dot.failed{background:#ef4444;border-color:#ef4444;}
</style>
</head>
<body>
<div id="wrap">
<div class="hud">
    <div class="hb">⭐ Score<br><b id="h-score">0</b></div>
    <div class="hb">🌊 Level<br><b id="h-level">1</b>/12</div>
    <div class="hb">💡 Hints<br><b id="h-hints">3</b></div>
    <div class="hb">🔥 Streak<br><b id="h-streak">0</b></div>
</div>

<div id="main-card">
    <div class="level-badge" id="level-badge">Level 1 — Apprentice</div>
    <div id="challenge-text">Find the two prime factors of:</div>
    <div id="number-display">—</div>
    <div id="shor-bar-wrap">
        <div id="shor-label">
            <span>☠️ Shor's Algorithm solving it...</span>
            <span id="shor-pct">0%</span>
        </div>
        <div id="shor-bar"><div id="shor-fill"></div></div>
    </div>
    <div class="input-row">
        <input class="factor-input" id="p-input" type="number" min="2" placeholder="p" 
               onkeydown="if(event.key==='Enter') checkAnswer()"/>
        <span class="mult-sign">×</span>
        <input class="factor-input" id="q-input" type="number" min="2" placeholder="q"
               onkeydown="if(event.key==='Enter') checkAnswer()"/>
        <span class="mult-sign">=</span>
        <span id="n-confirm" style="font-size:1.2rem;color:#475569;min-width:60px">?</span>
    </div>
    <button id="check-btn" onclick="checkAnswer()">🔓 Factor It!</button>
    <div id="msg"></div>
</div>

<div id="fact-box"></div>

<div id="progress-dots"></div>

<div id="btn-row">
    <button class="btn btn-start" onclick="startGame()">▶ New Game</button>
    <button class="btn btn-hint" onclick="useHint()">💡 Hint (-50pts)</button>
    <button class="btn btn-next" id="next-btn" onclick="nextLevel()" disabled>Next Level →</button>
</div>
<div id="hints-used"></div>
</div>

<script>
const LEVELS = [
    {level:1,  name:"Apprentice",     primes:[2,3,5,7,11,13],          timeLimit:60, desc:"Small primes only — easy start!"},
    {level:2,  name:"Cadet",          primes:[2,3,5,7,11,13,17,19],    timeLimit:55, desc:"A few more primes!"},
    {level:3,  name:"Analyst",        primes:[11,13,17,19,23,29],       timeLimit:50, desc:"Medium primes now!"},
    {level:4,  name:"Codebreaker",    primes:[17,19,23,29,31,37],       timeLimit:45, desc:"Getting harder!"},
    {level:5,  name:"Cryptographer",  primes:[23,29,31,37,41,43],       timeLimit:40, desc:"RSA uses primes like these!"},
    {level:6,  name:"RSA Hacker",     primes:[29,31,37,41,43,47],       timeLimit:35, desc:"Shor is getting faster!"},
    {level:7,  name:"Quantum Guard",  primes:[37,41,43,47,53,59],       timeLimit:30, desc:"This is real RSA territory!"},
    {level:8,  name:"Lattice Knight", primes:[41,43,47,53,59,61],       timeLimit:28, desc:"Kyber beats all of these!"},
    {level:9,  name:"PQC Defender",   primes:[47,53,59,61,67,71],       timeLimit:25, desc:"Almost expert level!"},
    {level:10, name:"NIST Scholar",   primes:[53,59,61,67,71,73],       timeLimit:22, desc:"Expert cryptographer!"},
    {level:11, name:"PQC Champion",   primes:[61,67,71,73,79,83],       timeLimit:18, desc:"Near impossible for humans!"},
    {level:12, name:"Quantum Master", primes:[71,73,79,83,89,97],       timeLimit:15, desc:"Only Shor's Algorithm is faster!"},
];

const FACTS = [
    "RSA-2048 uses primes with 300+ digits — classical computers need millions of years to factor them!",
    "Shor's Algorithm can factor any RSA number instantly on a quantum computer!",
    "That's why NIST chose Kyber (ML-KEM) — it's based on lattice math, not prime factorization!",
    "The largest RSA number ever factored classically was RSA-250 — it took 2,700 CPU years!",
    "Google's quantum computer factored small numbers in 2019 — RSA-2048 is next!",
    "ML-KEM (Kyber) FIPS 203 is immune to Shor's Algorithm — lattice problems can't be quantum-factored!",
    "Every time you use HTTPS today, RSA or ECDH protects you — but not for long!",
    "The NSM-10 mandate requires all US agencies to migrate from RSA by 2035!",
    "Dilithium (ML-DSA FIPS 204) replaces RSA signatures — same security, quantum-safe!",
    "A cryptographically relevant quantum computer (CRQC) would break all RSA instantly!",
    "Post-quantum cryptography uses hard lattice problems instead of factoring!",
    "You just did what takes a classical computer microseconds — a quantum computer does RSA-2048 in seconds!",
];

let level=1, score=0, streak=0, hintsLeft=3, gameActive=false;
let currentN=0, currentP=0, currentQ=0;
let shorTimer=null, shorProgress=0, levelResults=[];
let factTimeout=null;

function getPrimes(arr) { return arr; }

function genProblem(lvl) {
    const cfg = LEVELS[Math.min(lvl-1, LEVELS.length-1)];
    const primes = cfg.primes;
    let p = primes[Math.floor(Math.random()*primes.length)];
    let q;
    do { q = primes[Math.floor(Math.random()*primes.length)]; } while(q===p);
    if(p>q){let t=p;p=q;q=t;}
    return {p, q, n:p*q};
}

function startGame(){
    level=1; score=0; streak=0; hintsLeft=3;
    gameActive=true; levelResults=[];
    updateHUD();
    buildDots();
    loadLevel();
    document.getElementById("next-btn").disabled=true;
}

function loadLevel(){
    const cfg = LEVELS[Math.min(level-1, LEVELS.length-1)];
    const prob = genProblem(level);
    currentN=prob.n; currentP=prob.p; currentQ=prob.q;
    shorProgress=0;
    document.getElementById("number-display").textContent=currentN;
    document.getElementById("level-badge").textContent="Level "+level+" — "+cfg.name;
    document.getElementById("challenge-text").textContent=cfg.desc+" | Factor: "+currentN+" = p × q";
    document.getElementById("p-input").value="";
    document.getElementById("q-input").value="";
    document.getElementById("n-confirm").textContent="?";
    document.getElementById("msg").textContent="";
    document.getElementById("fact-box").style.display="none";
    document.getElementById("shor-fill").style.width="0%";
    document.getElementById("shor-pct").textContent="0%";
    document.getElementById("next-btn").disabled=true;
    document.getElementById("h-hints").textContent=hintsLeft;
    updateDots();

    // Start Shor's timer
    if(shorTimer) clearInterval(shorTimer);
    let elapsed=0;
    shorTimer=setInterval(()=>{
        if(!gameActive) return;
        elapsed++;
        shorProgress=Math.min(100, elapsed/cfg.timeLimit*100);
        document.getElementById("shor-fill").style.width=shorProgress+"%";
        document.getElementById("shor-pct").textContent=Math.floor(shorProgress)+"%";
        if(shorProgress>=100){
            clearInterval(shorTimer);
            shorSolves();
        }
    },1000);
    document.getElementById("p-input").focus();
}

function shorSolves(){
    gameActive=false;
    streak=0;
    levelResults.push("failed");
    updateDots();
    setMsg("☠️ Shor's Algorithm solved it first! "+currentN+" = "+currentP+" × "+currentQ,"#ef4444");
    showFact("☠️ This is why RSA is vulnerable! Shor's Algorithm factors numbers exponentially faster than classical computers. That's why we need Kyber (FIPS 203)!","#ef4444");
    document.getElementById("next-btn").disabled=false;
    updateHUD();
}

function checkAnswer(){
    if(!gameActive) return;
    const p=parseInt(document.getElementById("p-input").value)||0;
    const q=parseInt(document.getElementById("q-input").value)||0;
    document.getElementById("n-confirm").textContent=p&&q?p+"×"+q+"="+(p*q):"?";

    if(p<2||q<2){setMsg("Enter two numbers greater than 1!","#f59e0b");return;}

    if((p===currentP&&q===currentQ)||(p===currentQ&&q===currentP)){
        // Correct!
        clearInterval(shorTimer);
        gameActive=false;
        streak++;
        const timeBonus=Math.floor((100-shorProgress)*2);
        const levelPts=level*100+timeBonus+(streak>2?streak*50:0);
        score+=levelPts;
        levelResults.push("done");
        updateDots();
        updateHUD();
        setMsg("🎉 CORRECT! "+currentN+" = "+currentP+" × "+currentQ+" | +"+levelPts+" pts"+(streak>1?" 🔥×"+streak:""),"#10b981");
        showFact("✅ "+FACTS[Math.min(level-1,FACTS.length-1)],"#10b981");
        document.getElementById("next-btn").disabled=level>=12;
        if(level>=12){
            setMsg("🏆 QUANTUM MASTER! You factored all 12 levels! Final score: "+score,"#fbbf24");
        }
    } else if(p*q===currentN){
        // Right product but not prime
        setMsg("⚠️ "+p+"×"+q+"="+currentN+" but those aren't both prime! Find PRIME factors.","#f59e0b");
    } else {
        setMsg("❌ "+p+"×"+q+"="+(p*q)+" ≠ "+currentN+". Try again!","#ef4444");
        streak=Math.max(0,streak-1);
        score=Math.max(0,score-10);
        updateHUD();
    }
}

function useHint(){
    if(hintsLeft<=0){setMsg("No hints left!","#f59e0b");return;}
    if(!gameActive){setMsg("Start a level first!","#f59e0b");return;}
    hintsLeft--;
    score=Math.max(0,score-50);
    updateHUD();
    // Give the smaller prime
    setMsg("💡 Hint: One factor is "+currentP+" — now find the other!","#a78bfa");
    document.getElementById("p-input").value=currentP;
    document.getElementById("hints-used").textContent="Hints used — each costs 50 pts";
}

function nextLevel(){
    if(level>=12) return;
    level++;
    gameActive=true;
    loadLevel();
    document.getElementById("next-btn").disabled=true;
}

function updateHUD(){
    document.getElementById("h-score").textContent=score;
    document.getElementById("h-level").textContent=level;
    document.getElementById("h-hints").textContent=hintsLeft;
    document.getElementById("h-streak").textContent=streak;
}

function buildDots(){
    let html="";
    for(let i=0;i<12;i++) html+=`<div class="dot" id="dot-${i+1}"></div>`;
    document.getElementById("progress-dots").innerHTML=html;
}

function updateDots(){
    for(let i=0;i<12;i++){
        let el=document.getElementById("dot-"+(i+1));
        if(!el) continue;
        el.className="dot";
        if(i<levelResults.length){
            el.classList.add(levelResults[i]==="done"?"done":"failed");
        } else if(i===levelResults.length){
            el.classList.add("current");
        }
    }
}

function setMsg(m,c){
    let el=document.getElementById("msg");
    el.textContent=m; el.style.color=c||"#34d399";
}

function showFact(text,color){
    let el=document.getElementById("fact-box");
    el.textContent=text; el.style.display="block";
    el.style.borderColor=(color||"#3b82f6")+"50";
    if(factTimeout) clearTimeout(factTimeout);
    factTimeout=setTimeout(()=>el.style.display="none",6000);
}

// Live multiply preview
document.addEventListener("input",e=>{
    if(e.target.id==="p-input"||e.target.id==="q-input"){
        const p=parseInt(document.getElementById("p-input").value)||0;
        const q=parseInt(document.getElementById("q-input").value)||0;
        document.getElementById("n-confirm").textContent=p&&q?(p*q===currentN?"✅ "+p*q:"❌ "+p*q):"?";
        document.getElementById("n-confirm").style.color=p&&q&&p*q===currentN?"#10b981":"#ef4444";
    }
});

// Keyboard
document.addEventListener("keydown",e=>{
    if(e.key==="Enter") checkAnswer();
});

// Initial state
buildDots();
setMsg("Press ▶ New Game to start factoring!");
</script>
</body>
</html>
""", height=700)




def render_network_defender():
    """Free game: Quantum Network Defender v2 — Cinematic network defense with waves, animations, and boss attacks!"""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("🌐 Quantum Network Defender!")
    st.markdown(
        "**MISSION:** Quantum attack ships are targeting your network nodes! "
        "Click nodes to deploy Kyber shields before they get hacked. "
        "Survive all 12 waves to save the internet! **FREE for everyone!**"
    )
    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow:hidden;}
#wrap{display:flex;flex-direction:column;align-items:center;padding:8px;max-width:560px;margin:0 auto;}
.hud{display:grid;grid-template-columns:repeat(5,1fr);gap:3px;width:100%;margin-bottom:6px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:5px 3px;
    text-align:center;font-size:9px;color:#60a5fa;transition:all 0.3s;}
.hb b{display:block;font-size:14px;color:white;}
.hb.flash{background:#1d4ed8;border-color:#60a5fa;}

#wave-announce{background:linear-gradient(135deg,#071520,#0a1f35);
    border:2px solid #1d4ed8;border-radius:12px;padding:10px 16px;
    width:100%;text-align:center;margin-bottom:6px;font-size:13px;
    color:#60a5fa;font-weight:bold;min-height:36px;}

#gc{border:2px solid #1d4ed8;border-radius:12px;display:block;cursor:pointer;
    box-shadow:0 0 30px rgba(59,130,246,0.2);}

#bottom-panel{display:grid;grid-template-columns:1fr 1fr;gap:6px;width:100%;margin-top:6px;}
#shield-panel{background:#071520;border:1px solid #1a3a5a;border-radius:10px;padding:8px;}
#shield-panel h4{color:#10b981;font-size:11px;margin-bottom:4px;}
.shield-btn{padding:5px 10px;border-radius:6px;border:none;cursor:pointer;
    font-size:11px;font-weight:bold;color:white;margin:2px;display:block;width:100%;
    text-align:left;transition:all 0.15s;}
.shield-btn:hover{filter:brightness(1.2);transform:translateX(2px);}
.shield-btn.kyber{background:linear-gradient(90deg,#059669,#10b981);}
.shield-btn.dilithium{background:linear-gradient(90deg,#1d4ed8,#3b82f6);}
.shield-btn.sphincs{background:linear-gradient(90deg,#7c3aed,#8b5cf6);}
.shield-btn:disabled{background:#1e293b;color:#475569;cursor:not-allowed;}

#info-panel{background:#071520;border:1px solid #1a3a5a;border-radius:10px;padding:8px;}
#info-panel h4{color:#60a5fa;font-size:11px;margin-bottom:4px;}
#node-info{font-size:10px;color:#94a3b8;line-height:1.5;}

#msg{font-size:11px;color:#34d399;min-height:18px;margin:4px;text-align:center;
    font-weight:bold;width:100%;}
#fact-box{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);
    border-radius:8px;padding:7px 10px;margin:3px 0;font-size:10px;color:#93c5fd;
    display:none;line-height:1.5;width:100%;}

.btns{display:flex;gap:5px;flex-wrap:wrap;justify-content:center;margin:5px 0;}
.btn{padding:7px 16px;border-radius:8px;border:none;cursor:pointer;
    font-size:12px;font-weight:bold;color:white;transition:all 0.15s;}
.btn:hover{filter:brightness(1.2);transform:translateY(-1px);}
.btn-start{background:linear-gradient(135deg,#1d4ed8,#06b6d4);}
.btn-next{background:linear-gradient(135deg,#059669,#10b981);}
.btn-next:disabled{background:#1e293b;color:#475569;cursor:not-allowed;transform:none;}
.btn-repair{background:linear-gradient(135deg,#d97706,#f59e0b);}
</style>
</head>
<body>
<div id="wrap">

<div class="hud">
    <div class="hb" id="hb-score">⭐ Score<br><b id="h-score">0</b></div>
    <div class="hb" id="hb-wave">🌊 Wave<br><b id="h-wave">1</b>/12</div>
    <div class="hb" id="hb-shields">🛡️ Shields<br><b id="h-shields">3</b></div>
    <div class="hb" id="hb-nodes">💻 Nodes<br><b id="h-nodes">0/0</b></div>
    <div class="hb" id="hb-hp">❤️ Network<br><b id="h-hp">100%</b></div>
</div>

<div id="wave-announce">Press START to defend the quantum internet! 🌐</div>

<canvas id="gc" width="540" height="380"></canvas>

<div id="bottom-panel">
    <div id="shield-panel">
        <h4>🔐 Deploy Shield (click node first)</h4>
        <button class="shield-btn kyber" id="btn-kyber" onclick="deployShield('kyber')" disabled>
            🔐 Kyber ML-KEM — Strongest
        </button>
        <button class="shield-btn dilithium" id="btn-dilith" onclick="deployShield('dilithium')" disabled>
            ✍️ Dilithium ML-DSA — Fast
        </button>
        <button class="shield-btn sphincs" id="btn-sphincs" onclick="deployShield('sphincs')" disabled>
            🌲 SPHINCS+ — Backup
        </button>
    </div>
    <div id="info-panel">
        <h4>📡 Node Info</h4>
        <div id="node-info">Click a node to see its status and deploy a quantum-safe shield!</div>
    </div>
</div>

<div id="msg"></div>
<div id="fact-box"></div>

<div class="btns">
    <button class="btn btn-start" onclick="startGame()">🚀 START</button>
    <button class="btn btn-repair" onclick="repairAll()">🔧 Repair All (-200pts)</button>
    <button class="btn btn-next" id="next-btn" onclick="nextWave()" disabled>Next Wave →</button>
</div>
</div>

<script>
const cv=document.getElementById("gc");
const cx=cv.getContext("2d");
const W=540,H=380;

// Wave configurations
const WAVES=[
    {wave:1,  name:"First Contact",     nodes:4,  enemies:2, spd:0.4, hp:30,  reward:200, desc:"Basic Shor probes incoming!"},
    {wave:2,  name:"Quantum Scouts",    nodes:5,  enemies:3, spd:0.5, hp:35,  reward:250, desc:"More scouts — defend the left flank!"},
    {wave:3,  name:"Lattice Breach",    nodes:5,  enemies:4, spd:0.55,hp:40,  reward:300, desc:"They found a weak RSA node!"},
    {wave:4,  name:"Shor Surge",        nodes:6,  enemies:5, spd:0.6, hp:45,  reward:350, desc:"Shor Algorithm ships deployed!"},
    {wave:5,  name:"Grover Storm",      nodes:6,  enemies:6, spd:0.65,hp:50,  reward:400, desc:"Grover speedup detected!"},
    {wave:6,  name:"RSA Collapse",      nodes:7,  enemies:7, spd:0.7, hp:55,  reward:500, desc:"All RSA nodes are prime targets!"},
    {wave:7,  name:"Quantum Flood",     nodes:7,  enemies:8, spd:0.75,hp:60,  reward:600, desc:"Multiple simultaneous attacks!"},
    {wave:8,  name:"CRQC Advance",      nodes:8,  enemies:9, spd:0.8, hp:70,  reward:700, desc:"Cryptographically Relevant QC detected!"},
    {wave:9,  name:"Pentagon Breach",   nodes:8,  enemies:10,spd:0.85,hp:80,  reward:800, desc:"Critical infrastructure targeted!"},
    {wave:10, name:"Global Attack",     nodes:9,  enemies:12,spd:0.9, hp:90,  reward:1000,desc:"World financial system under attack!"},
    {wave:11, name:"Quantum Apocalypse",nodes:9,  enemies:14,spd:1.0, hp:100, reward:1200,desc:"Final defense — deploy everything!"},
    {wave:12, name:"FINAL BOSS",        nodes:10, enemies:16,spd:1.1, hp:150, reward:2000,desc:"BOSS: The Quantum Monster itself!"},
];

const NODE_TYPES=[
    {emoji:"🏦",name:"Bank",       color:"#f59e0b"},
    {emoji:"🏥",name:"Hospital",   color:"#10b981"},
    {emoji:"🏛️",name:"Government", color:"#3b82f6"},
    {emoji:"⚡",name:"Power Grid", color:"#f97316"},
    {emoji:"📡",name:"Satellite",  color:"#8b5cf6"},
    {emoji:"🌍",name:"Internet Hub",color:"#06b6d4"},
    {emoji:"🔭",name:"Research",   color:"#ec4899"},
    {emoji:"🚀",name:"Military",   color:"#ef4444"},
    {emoji:"🏫",name:"School",     color:"#84cc16"},
    {emoji:"💊",name:"Pharma",     color:"#a78bfa"},
];

const ENEMY_TYPES=[
    {emoji:"☠️",name:"Shor Bot",    color:"#ef4444",dmg:8},
    {emoji:"🌀",name:"Grover Swarm",color:"#f97316",dmg:6},
    {emoji:"👾",name:"CRQC Drone",  color:"#a855f7",dmg:12},
    {emoji:"💀",name:"Q-BOSS",      color:"#dc2626",dmg:20},
];

const SHIELD_FACTS={
    kyber:"ML-KEM (FIPS 203) — Module Learning With Errors lattice math. The strongest post-quantum key exchange, used in TLS 1.3!",
    dilithium:"ML-DSA (FIPS 204) — Module Lattice Digital Signature Algorithm. Signs every packet so enemies can't forge data!",
    sphincs:"SLH-DSA (FIPS 205) — Stateless Hash-Based Signature. Uses only SHA-3 — safe even if all lattice math breaks!",
};

let wave=1,score=0,shieldsLeft=3,networkHp=100,gameActive=false;
let nodes=[],enemies=[],particles=[],lasers=[];
let selectedNode=null,gameLoop=null,factTimeout=null;
let enemySpawnTimer=0,enemiesSpawned=0,waveEnemyCount=0;
let frameCount=0;

function genNodes(count){
    nodes=[];
    const cx2=W/2,cy2=H/2-20;
    const radii=[80,160,230];
    let placed=0;
    for(let ring=0;ring<radii.length&&placed<count;ring++){
        const perRing=ring===0?1:ring===1?4:count-placed;
        const r=radii[ring];
        for(let i=0;i<perRing&&placed<count;i++){
            const angle=(i/perRing)*Math.PI*2-(Math.PI/2);
            nodes.push({
                x:cx2+r*Math.cos(angle),
                y:cy2+r*Math.sin(angle),
                type:NODE_TYPES[placed%NODE_TYPES.length],
                shield:null,
                hp:100,
                maxHp:100,
                id:placed,
                pulse:Math.random()*Math.PI*2,
                hacked:false,
                beingAttacked:false,
            });
            placed++;
        }
    }
}

function spawnEnemy(){
    const cfg=WAVES[Math.min(wave-1,WAVES.length-1)];
    const typeIdx=wave>=12?3:wave>=8?2:wave>=4?Math.floor(Math.random()*2):0;
    const et=ENEMY_TYPES[typeIdx];
    // Pick a random unshielded node as target
    const targets=nodes.filter(n=>!n.hacked&&n.shield===null);
    if(targets.length===0) return;
    const target=targets[Math.floor(Math.random()*targets.length)];
    // Spawn from edge
    const angle=Math.random()*Math.PI*2;
    const spawnR=260;
    enemies.push({
        x:W/2+spawnR*Math.cos(angle),
        y:H/2-20+spawnR*Math.sin(angle),
        tx:target.x, ty:target.y,
        targetId:target.id,
        type:et,
        hp:cfg.hp,
        maxHp:cfg.hp,
        spd:cfg.spd,
        id:Math.random(),
        flash:0,
        dead:false,
        reached:false,
    });
    enemiesSpawned++;
}

function startGame(){
    wave=1;score=0;shieldsLeft=3;networkHp=100;
    gameActive=true;selectedNode=null;
    enemiesSpawned=0;waveEnemyCount=0;
    frameCount=0;
    if(gameLoop) cancelAnimationFrame(gameLoop);
    document.getElementById("next-btn").disabled=true;
    initWave();
    loop();
}

function initWave(){
    const cfg=WAVES[Math.min(wave-1,WAVES.length-1)];
    genNodes(cfg.nodes);
    enemies=[];particles=[];lasers=[];
    enemiesSpawned=0;
    waveEnemyCount=cfg.enemies;
    enemySpawnTimer=0;
    selectedNode=null;
    disableShieldBtns();
    document.getElementById("wave-announce").textContent=
        "🌊 Wave "+wave+"/12: "+cfg.name+" — "+cfg.desc;
    document.getElementById("next-btn").disabled=true;
    updateHUD();
}

function loop(){
    if(!gameActive){draw();return;}
    frameCount++;
    update();
    draw();
    gameLoop=requestAnimationFrame(loop);
}

function update(){
    const cfg=WAVES[Math.min(wave-1,WAVES.length-1)];

    // Spawn enemies
    enemySpawnTimer++;
    const spawnRate=Math.max(30,90-wave*5);
    if(enemySpawnTimer>=spawnRate&&enemiesSpawned<waveEnemyCount){
        spawnEnemy();
        enemySpawnTimer=0;
    }

    // Update nodes pulse
    nodes.forEach(n=>{n.pulse+=0.05;});

    // Move enemies
    enemies.forEach(e=>{
        if(e.dead||e.reached) return;
        // Retarget if target got shielded
        const tnode=nodes[e.targetId];
        if(tnode&&tnode.shield!==null&&!tnode.hacked){
            // Find new unshielded target
            const newTargets=nodes.filter(n=>!n.hacked&&n.shield===null&&n.id!==e.targetId);
            if(newTargets.length>0){
                const nt=newTargets[Math.floor(Math.random()*newTargets.length)];
                e.targetId=nt.id;
                e.tx=nt.x;e.ty=nt.y;
            }
        }
        const dx=e.tx-e.x,dy=e.ty-e.y;
        const dist=Math.sqrt(dx*dx+dy*dy);
        if(dist<12){
            e.reached=true;
            // Attack the node
            const node=nodes[e.targetId];
            if(node){
                if(node.shield){
                    // Shield absorbs it!
                    score+=50;
                    spawnParticles(node.x,node.y,"#10b981",8);
                    addLaser(e.x,e.y,node.x,node.y,"#10b981");
                    setMsg("🛡️ "+node.shield.toUpperCase()+" shield blocked "+e.type.name+"! +50pts","#10b981");
                } else if(!node.hacked){
                    node.hp-=e.type.dmg*(1+wave*0.05);
                    networkHp=Math.max(0,networkHp-e.type.dmg*0.5);
                    spawnParticles(node.x,node.y,"#ef4444",6);
                    addLaser(e.x,e.y,node.x,node.y,"#ef4444");
                    if(node.hp<=0){
                        node.hacked=true;
                        node.hp=0;
                        spawnParticles(node.x,node.y,"#f97316",15);
                        flashHUD("hb-hp");
                        setMsg("💥 "+node.type.name+" HACKED by "+e.type.name+"!","#ef4444");
                        showFact("☠️ "+e.type.name+" broke through! This is why "+
                            (wave<4?"RSA needs replacing":"Kyber is essential")+"!","#ef4444");
                    }
                }
            }
            e.dead=true;
        } else {
            e.x+=dx/dist*e.spd;
            e.y+=dy/dist*e.spd;
        }
        if(e.flash>0) e.flash--;
    });

    enemies=enemies.filter(e=>!e.dead&&!e.reached);

    // Update particles
    particles.forEach(p=>{
        p.x+=p.vx;p.y+=p.vy;p.alpha-=0.04;p.r*=0.95;
    });
    particles=particles.filter(p=>p.alpha>0);

    // Update lasers
    lasers.forEach(l=>l.alpha-=0.08);
    lasers=lasers.filter(l=>l.alpha>0);

    updateHUD();

    // Check wave complete
    if(enemiesSpawned>=waveEnemyCount&&enemies.length===0){
        waveComplete();
    }

    // Check game over
    if(networkHp<=0){
        gameOver();
    }
}

function waveComplete(){
    if(!gameActive) return;
    gameActive=false;
    cancelAnimationFrame(gameLoop);
    const cfg=WAVES[Math.min(wave-1,WAVES.length-1)];
    const bonus=cfg.reward+shieldsLeft*100;
    score+=bonus;
    shieldsLeft+=2; // Reward shields for next wave
    updateHUD();
    if(wave>=12){
        document.getElementById("wave-announce").textContent=
            "🏆 INTERNET SAVED! You defeated all 12 waves! Final Score: "+score;
        setMsg("🏆 QUANTUM GUARDIAN! You saved the global internet! Score: "+score,"#fbbf24");
        showFact("🔐 You deployed Kyber, Dilithium, and SPHINCS+ to protect the entire internet! "+
            "This is exactly what NIST FIPS 203-206 was designed to do!","#10b981");
    } else {
        document.getElementById("wave-announce").textContent=
            "✅ Wave "+wave+" cleared! +"+bonus+" pts | "+shieldsLeft+" shields ready | Next: "+
            WAVES[wave].name;
        setMsg("✅ Wave "+wave+" complete! +"+bonus+" pts. Deploy more shields!","#10b981");
        showFact("🔐 "+SHIELD_FACTS[["kyber","dilithium","sphincs"][wave%3]],"#10b981");
        document.getElementById("next-btn").disabled=false;
    }
    draw();
}

function gameOver(){
    gameActive=false;
    cancelAnimationFrame(gameLoop);
    document.getElementById("wave-announce").textContent=
        "💀 NETWORK COMPROMISED! Score: "+score+" | Wave "+wave+"/12";
    setMsg("💀 The quantum attackers broke through! Deploy shields faster next time!","#ef4444");
    showFact("☠️ Without post-quantum encryption, this is what happens when quantum computers arrive! "+
        "NIST finalized Kyber, Dilithium, SPHINCS+, and Falcon in 2024 to prevent exactly this!","#ef4444");
    draw();
}

function repairAll(){
    if(score<200){setMsg("Need 200 pts to repair!","#f59e0b");return;}
    score-=200;
    nodes.forEach(n=>{n.hacked=false;n.hp=100;});
    networkHp=Math.min(100,networkHp+20);
    spawnParticles(W/2,H/2-20,"#10b981",20);
    setMsg("🔧 All nodes repaired! -200 pts","#10b981");
    updateHUD();
}

function deployShield(type){
    if(selectedNode===null) return;
    if(shieldsLeft<=0){setMsg("No shields left! Clear more waves to earn shields!","#f59e0b");return;}
    const node=nodes[selectedNode];
    if(!node||node.hacked){setMsg("Cannot shield a hacked node!","#ef4444");return;}
    if(node.shield){setMsg("Node already shielded with "+node.shield.toUpperCase()+"!","#f59e0b");return;}
    node.shield=type;
    node.hp=100;
    shieldsLeft--;
    score+=50;
    spawnParticles(node.x,node.y,type==="kyber"?"#10b981":type==="dilithium"?"#3b82f6":"#8b5cf6",12);
    flashHUD("hb-shields");
    setMsg("🔐 "+type.toUpperCase()+" shield deployed on "+node.type.name+"! +50pts","#10b981");
    showFact("🔐 "+SHIELD_FACTS[type],"#10b981");
    selectedNode=null;
    disableShieldBtns();
    updateHUD();
    // Retarget all enemies attacking this node
    enemies.forEach(e=>{
        if(e.targetId===node.id){
            const newTargets=nodes.filter(n=>!n.hacked&&n.shield===null&&n.id!==node.id);
            if(newTargets.length>0){
                const nt=newTargets[Math.floor(Math.random()*newTargets.length)];
                e.targetId=nt.id;e.tx=nt.x;e.ty=nt.y;
            }
        }
    });
}

function nextWave(){
    wave++;
    gameActive=true;
    initWave();
    loop();
}

cv.addEventListener("click",e=>{
    if(!gameActive) return;
    const rect=cv.getBoundingClientRect();
    const mx=e.clientX-rect.left,my=e.clientY-rect.top;
    for(let n of nodes){
        if(Math.hypot(mx-n.x,my-n.y)<22){
            selectedNode=n.id;
            const shieldColor=n.shield?
                {kyber:"#10b981",dilithium:"#3b82f6",sphincs:"#8b5cf6"}[n.shield]:"#ef4444";
            document.getElementById("node-info").innerHTML=
                "<b style='color:"+shieldColor+"'>"+n.type.emoji+" "+n.type.name+"</b><br>"+
                "HP: "+(n.hacked?"💀 HACKED":Math.ceil(n.hp)+"%")+"<br>"+
                "Shield: "+(n.shield?"✅ "+n.shield.toUpperCase():"❌ None — VULNERABLE!")+
                "<br><span style='color:#60a5fa;font-size:9px'>Click a shield button to protect!</span>";
            // Enable buttons
            document.getElementById("btn-kyber").disabled=n.hacked||n.shield!==null||shieldsLeft<=0;
            document.getElementById("btn-dilith").disabled=n.hacked||n.shield!==null||shieldsLeft<=0;
            document.getElementById("btn-sphincs").disabled=n.hacked||n.shield!==null||shieldsLeft<=0;
            return;
        }
    }
    selectedNode=null;
    disableShieldBtns();
    document.getElementById("node-info").textContent="Click a node to see its status!";
});

function disableShieldBtns(){
    ["btn-kyber","btn-dilith","btn-sphincs"].forEach(id=>
        document.getElementById(id).disabled=true);
}

function spawnParticles(x,y,color,count){
    for(let i=0;i<count;i++){
        const angle=Math.random()*Math.PI*2;
        const spd=Math.random()*3+1;
        particles.push({x,y,vx:Math.cos(angle)*spd,vy:Math.sin(angle)*spd,
            r:Math.random()*4+2,alpha:1,color});
    }
}

function addLaser(x1,y1,x2,y2,color){
    lasers.push({x1,y1,x2,y2,color,alpha:1});
}

function flashHUD(id){
    const el=document.getElementById(id);
    el.classList.add("flash");
    setTimeout(()=>el.classList.remove("flash"),300);
}

function updateHUD(){
    document.getElementById("h-score").textContent=score;
    document.getElementById("h-wave").textContent=wave;
    document.getElementById("h-shields").textContent=shieldsLeft;
    const total=nodes.length;
    const safe=nodes.filter(n=>n.shield&&!n.hacked).length;
    document.getElementById("h-nodes").textContent=safe+"/"+total;
    document.getElementById("h-hp").textContent=Math.ceil(networkHp)+"%";
    document.getElementById("h-hp").style.color=
        networkHp>60?"white":networkHp>30?"#f59e0b":"#ef4444";
}

function setMsg(m,c){
    let el=document.getElementById("msg");
    el.textContent=m;el.style.color=c||"#34d399";
}

function showFact(text,color){
    let el=document.getElementById("fact-box");
    el.textContent=text;el.style.display="block";
    el.style.borderColor=(color||"#3b82f6")+"50";
    if(factTimeout) clearTimeout(factTimeout);
    factTimeout=setTimeout(()=>el.style.display="none",6000);
}

function draw(){
    cx.clearRect(0,0,W,H);
    // Background
    cx.fillStyle="#020d14";
    cx.fillRect(0,0,W,H);
    // Grid
    cx.strokeStyle="#0a1f2e";cx.lineWidth=0.5;
    for(let x=0;x<W;x+=30){cx.beginPath();cx.moveTo(x,0);cx.lineTo(x,H);cx.stroke();}
    for(let y=0;y<H;y+=30){cx.beginPath();cx.moveTo(0,y);cx.lineTo(W,y);cx.stroke();}

    // Draw connection lines between nodes
    cx.lineWidth=1;
    for(let i=0;i<nodes.length;i++){
        for(let j=i+1;j<nodes.length;j++){
            const a=nodes[i],b=nodes[j];
            const dist2=Math.hypot(a.x-b.x,a.y-b.y);
            if(dist2<160){
                const bothShielded=a.shield&&b.shield;
                const eitherHacked=a.hacked||b.hacked;
                cx.beginPath();cx.moveTo(a.x,a.y);cx.lineTo(b.x,b.y);
                cx.setLineDash(eitherHacked?[4,4]:[]);
                cx.strokeStyle=eitherHacked?"#47556920":bothShielded?"#10b98130":"#1d4ed820";
                cx.lineWidth=eitherHacked?0.5:1;
                cx.stroke();
                cx.setLineDash([]);
            }
        }
    }

    // Draw lasers
    for(let l of lasers){
        cx.beginPath();cx.moveTo(l.x1,l.y1);cx.lineTo(l.x2,l.y2);
        cx.strokeStyle=l.color+Math.floor(l.alpha*255).toString(16).padStart(2,"0");
        cx.lineWidth=2;cx.stroke();
    }

    // Draw nodes
    for(let n of nodes){
        const isSelected=n.id===selectedNode;
        const shieldColor=n.shield?
            {kyber:"#10b981",dilithium:"#3b82f6",sphincs:"#8b5cf6"}[n.shield]:"#ef4444";

        // Pulse ring
        if(!n.hacked){
            const pulseR=20+Math.sin(n.pulse)*3;
            cx.beginPath();cx.arc(n.x,n.y,pulseR,0,Math.PI*2);
            cx.strokeStyle=(n.shield?shieldColor:"#ef4444")+"40";
            cx.lineWidth=1;cx.stroke();
        }

        // Shield glow
        if(n.shield&&!n.hacked){
            cx.shadowColor=shieldColor;cx.shadowBlur=15;
        }

        // Node circle
        cx.beginPath();cx.arc(n.x,n.y,18,0,Math.PI*2);
        cx.fillStyle=n.hacked?"#1a0505":isSelected?"#0d2a4a":"#071520";
        cx.fill();
        cx.strokeStyle=n.hacked?"#ef4444":isSelected?"#fbbf24":n.shield?shieldColor:"#334155";
        cx.lineWidth=isSelected?3:2;
        cx.stroke();
        cx.shadowBlur=0;

        // Emoji
        cx.font="14px serif";cx.textAlign="center";cx.textBaseline="middle";
        cx.globalAlpha=n.hacked?0.4:1;
        cx.fillText(n.hacked?"💀":n.type.emoji,n.x,n.y);
        cx.globalAlpha=1;

        // HP bar
        if(!n.hacked&&n.hp<100){
            const bw=32,bh=4,bx=n.x-bw/2,by=n.y+20;
            cx.fillStyle="#1e293b";cx.fillRect(bx,by,bw,bh);
            cx.fillStyle=n.hp>50?"#10b981":"#ef4444";
            cx.fillRect(bx,by,bw*(n.hp/100),bh);
        }

        // Shield indicator
        if(n.shield&&!n.hacked){
            cx.font="10px sans-serif";cx.textAlign="center";cx.fillStyle=shieldColor;
            cx.fillText({kyber:"🔐",dilithium:"✍️",sphincs:"🌲"}[n.shield],n.x,n.y-24);
        }
    }

    // Draw enemies
    cx.textAlign="center";cx.textBaseline="middle";
    for(let e of enemies){
        if(e.dead) continue;
        // Enemy trail
        cx.shadowColor=e.type.color;cx.shadowBlur=10;
        cx.font="16px serif";
        cx.fillText(e.type.emoji,e.x,e.y);
        cx.shadowBlur=0;
        // HP bar
        const bw=24,bh=3,bx=e.x-bw/2,by=e.y+12;
        cx.fillStyle="#1e293b";cx.fillRect(bx,by,bw,bh);
        cx.fillStyle="#ef4444";
        cx.fillRect(bx,by,bw*(e.hp/e.maxHp),bh);
        // Attack line
        cx.beginPath();cx.moveTo(e.x,e.y);cx.lineTo(e.tx,e.ty);
        cx.strokeStyle=e.type.color+"20";cx.lineWidth=0.5;cx.stroke();
    }

    // Draw particles
    for(let p of particles){
        cx.beginPath();cx.arc(p.x,p.y,p.r,0,Math.PI*2);
        cx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,"0");
        cx.fill();
    }

    // Draw network HP bar at bottom
    const hpW=W-40,hpH=6,hpX=20,hpY=H-12;
    cx.fillStyle="#1e293b";cx.fillRect(hpX,hpY,hpW,hpH);
    const hpColor=networkHp>60?"#10b981":networkHp>30?"#f59e0b":"#ef4444";
    cx.fillStyle=hpColor;cx.fillRect(hpX,hpY,hpW*(networkHp/100),hpH);
    cx.fillStyle="#60a5fa";cx.font="9px sans-serif";cx.textAlign="left";
    cx.fillText("Network Health",hpX,hpY-3);

    // Intro screen
    if(!gameActive&&frameCount===0){
        cx.fillStyle="rgba(2,13,20,0.85)";cx.fillRect(0,0,W,H);
        cx.fillStyle="#1d4ed8";cx.font="bold 18px sans-serif";cx.textAlign="center";
        cx.fillText("🌐 QUANTUM NETWORK DEFENDER",W/2,H/2-60);
        cx.fillStyle="#60a5fa";cx.font="12px sans-serif";
        cx.fillText("Quantum attack ships are targeting your network!",W/2,H/2-30);
        cx.fillText("Click nodes → Deploy Kyber/Dilithium/SPHINCS+ shields",W/2,H/2-10);
        cx.fillText("Shields block attacks — unshielded nodes get hacked!",W/2,H/2+10);
        cx.fillText("Earn shields by clearing waves!",W/2,H/2+30);
        cx.fillStyle="#334155";cx.font="11px sans-serif";
        cx.fillText("Press 🚀 START to begin",W/2,H/2+60);
    }
}
draw();
</script>
</body>
</html>
""", height=820)


def render_secret_message():
    """Free game: Secret Message Maker — K-5 cipher introduction!"""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("🔤 Secret Message Maker!")
    st.markdown(
        "**Type a secret message and encrypt it!** "
        "Can you decode the mystery messages? "
        "Learn why simple ciphers are NOT quantum-safe — and what is! "
        "FREE for everyone!"
    )
    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;}
#wrap{display:flex;flex-direction:column;align-items:center;padding:12px;max-width:540px;margin:0 auto;}
.hud{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;width:100%;margin-bottom:8px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:6px 4px;text-align:center;font-size:10px;color:#60a5fa;}
.hb b{display:block;font-size:16px;color:white;}
.tabs{display:flex;gap:4px;width:100%;margin-bottom:8px;}
.tab{flex:1;padding:8px;border-radius:8px;border:1px solid #1a3a5a;background:#071520;
    color:#60a5fa;font-size:12px;font-weight:bold;cursor:pointer;text-align:center;}
.tab.active{background:#1d4ed8;border-color:#3b82f6;color:white;}
.card{background:#071520;border:1px solid #1a3a5a;border-radius:12px;padding:14px;width:100%;margin-bottom:8px;}
.card h4{color:#60a5fa;margin-bottom:8px;font-size:13px;}
.msg-input{width:100%;background:#0a1f35;border:2px solid #1d4ed8;border-radius:8px;
    color:white;font-size:13px;padding:10px;outline:none;resize:none;font-family:'Segoe UI',sans-serif;}
.msg-input:focus{border-color:#60a5fa;}
.msg-output{width:100%;background:#051018;border:1px solid #1a3a5a;border-radius:8px;
    color:#10b981;font-size:13px;padding:10px;min-height:50px;font-family:'Fira Code',monospace;
    word-break:break-all;line-height:1.6;}
.cipher-select{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0;}
.cipher-btn{padding:5px 12px;border-radius:20px;border:1px solid #1a3a5a;
    background:#071520;color:#60a5fa;font-size:11px;cursor:pointer;}
.cipher-btn.active{background:#1d4ed8;border-color:#3b82f6;color:white;}
#msg{font-size:12px;color:#34d399;min-height:18px;margin:4px;text-align:center;font-weight:bold;}
#fact-box{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);
    border-radius:8px;padding:8px 12px;margin:4px 0;font-size:11px;color:#93c5fd;
    display:none;line-height:1.5;width:100%;}
.challenge-card{background:#071520;border:2px solid #7c3aed;border-radius:12px;
    padding:14px;width:100%;margin-bottom:8px;}
.challenge-card h4{color:#a78bfa;margin-bottom:6px;font-size:13px;}
.encrypted-msg{font-family:'Fira Code',monospace;font-size:14px;color:#fbbf24;
    letter-spacing:2px;background:#051018;padding:10px;border-radius:6px;
    word-break:break-all;margin:8px 0;}
.decode-input{width:100%;background:#0a1f35;border:2px solid #7c3aed;border-radius:8px;
    color:white;font-size:13px;padding:8px;outline:none;}
.decode-input:focus{border-color:#a78bfa;}
.btn{padding:8px 16px;border-radius:8px;border:none;cursor:pointer;
    font-size:12px;font-weight:bold;color:white;margin:3px;}
.btn-blue{background:#1d4ed8;}
.btn-purple{background:#7c3aed;}
.btn-green{background:#059669;}
.btn-row{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;margin:6px 0;}
.key-display{display:flex;gap:3px;flex-wrap:wrap;margin:6px 0;justify-content:center;}
.key-pair{background:#0a1f35;border:1px solid #1a3a5a;border-radius:4px;
    padding:3px 5px;font-size:9px;color:#60a5fa;font-family:monospace;}
.key-pair span{color:#10b981;}
.level-badge{display:inline-block;background:linear-gradient(135deg,#7c3aed,#1d4ed8);
    border-radius:20px;padding:3px 12px;font-size:11px;font-weight:bold;margin-bottom:6px;}
#progress{display:flex;gap:4px;justify-content:center;flex-wrap:wrap;margin:6px 0;}
.pdot{width:12px;height:12px;border-radius:50%;background:#1e293b;border:1px solid #334155;}
.pdot.done{background:#10b981;}.pdot.current{background:#3b82f6;}
.pdot.failed{background:#ef4444;}
</style>
</head>
<body>
<div id="wrap">
<div class="hud">
    <div class="hb">⭐ Score<br><b id="h-score">0</b></div>
    <div class="hb">🏆 Level<br><b id="h-level">1</b>/12</div>
    <div class="hb">🔥 Streak<br><b id="h-streak">0</b></div>
</div>

<div class="tabs">
    <div class="tab active" onclick="showTab('encrypt')">🔐 Encrypt</div>
    <div class="tab" onclick="showTab('decode')">🕵️ Decode Challenge</div>
    <div class="tab" onclick="showTab('learn')">📚 Learn</div>
</div>

<!-- ENCRYPT TAB -->
<div id="tab-encrypt">
    <div class="card">
        <h4>Choose a cipher:</h4>
        <div class="cipher-select">
            <button class="cipher-btn active" onclick="setCipher('substitution',this)">🔄 Substitution</button>
            <button class="cipher-btn" onclick="setCipher('caesar',this)">⚔️ Caesar (+3)</button>
            <button class="cipher-btn" onclick="setCipher('reverse',this)">↩️ Reverse</button>
            <button class="cipher-btn" onclick="setCipher('morse',this)">📡 Morse</button>
        </div>
        <div id="cipher-info" style="font-size:10px;color:#64748b;margin-bottom:8px;">
            Each letter maps to a different letter — like a secret code!
        </div>
    </div>
    <div class="card">
        <h4>✏️ Type your message:</h4>
        <textarea class="msg-input" id="plain-input" rows="3" 
            placeholder="Type anything here..." 
            oninput="encrypt()">Hello World</textarea>
    </div>
    <div class="card">
        <h4>🔐 Encrypted message:</h4>
        <div class="msg-output" id="cipher-output">—</div>
        <div class="btn-row" style="margin-top:8px">
            <button class="btn btn-blue" onclick="copyEncrypted()">📋 Copy</button>
            <button class="btn btn-purple" onclick="showKeyMap()">🗝️ Show Key</button>
        </div>
        <div id="key-map" style="display:none;margin-top:6px">
            <div style="font-size:10px;color:#60a5fa;margin-bottom:4px">Cipher Key:</div>
            <div class="key-display" id="key-display"></div>
        </div>
    </div>
</div>

<!-- DECODE TAB -->
<div id="tab-decode" style="display:none">
    <div class="challenge-card">
        <div class="level-badge" id="challenge-badge">Level 1</div>
        <h4 id="challenge-title">🕵️ Decode this secret message!</h4>
        <div id="challenge-hint" style="font-size:10px;color:#64748b;margin-bottom:6px;"></div>
        <div class="encrypted-msg" id="challenge-msg">—</div>
        <input class="decode-input" id="decode-input" type="text" 
               placeholder="Type your decoded message here..."
               onkeydown="if(event.key==='Enter') checkDecode()"/>
        <div class="btn-row" style="margin-top:8px">
            <button class="btn btn-purple" onclick="checkDecode()">🔓 Submit Answer</button>
            <button class="btn btn-blue" onclick="getDecodeHint()">💡 Hint</button>
            <button class="btn btn-green" id="next-challenge" onclick="nextChallenge()" style="display:none">Next →</button>
        </div>
    </div>
    <div id="progress"></div>
</div>

<!-- LEARN TAB -->
<div id="tab-learn" style="display:none">
    <div class="card">
        <h4>🔐 Why Simple Ciphers FAIL</h4>
        <div style="font-size:11px;color:#94a3b8;line-height:1.7">
            <p style="margin-bottom:6px">⚔️ <b style="color:#ef4444">Substitution Cipher:</b> Easy to crack with frequency analysis. 'E' is the most common letter in English — find the most common encrypted letter and you have your key!</p>
            <p style="margin-bottom:6px">⚔️ <b style="color:#f59e0b">Caesar Cipher:</b> Only 25 possible keys — a computer tries all of them in milliseconds!</p>
            <p style="margin-bottom:6px">⚔️ <b style="color:#f97316">RSA Encryption:</b> Was considered unbreakable — until quantum computers. Shor's Algorithm factors RSA keys in seconds!</p>
            <p style="margin-bottom:6px">✅ <b style="color:#10b981">Kyber (ML-KEM FIPS 203):</b> Uses lattice math — even quantum computers can't break it! The hardest problem in all of cryptography!</p>
        </div>
    </div>
    <div class="card">
        <h4>📊 Cipher Strength Comparison</h4>
        <div style="font-size:11px">
            <div style="margin:4px 0">Substitution <div style="background:#ef4444;height:8px;width:10%;border-radius:4px;display:inline-block;margin-left:6px"></div> <span style="color:#ef4444">Weak</span></div>
            <div style="margin:4px 0">Caesar &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <div style="background:#f59e0b;height:8px;width:15%;border-radius:4px;display:inline-block;margin-left:6px"></div> <span style="color:#f59e0b">Very Weak</span></div>
            <div style="margin:4px 0">RSA-2048 &nbsp;&nbsp; <div style="background:#3b82f6;height:8px;width:70%;border-radius:4px;display:inline-block;margin-left:6px"></div> <span style="color:#3b82f6">Strong (classical)</span></div>
            <div style="margin:4px 0">RSA vs Shor <div style="background:#ef4444;height:8px;width:10%;border-radius:4px;display:inline-block;margin-left:6px"></div> <span style="color:#ef4444">Broken by quantum!</span></div>
            <div style="margin:4px 0">Kyber &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <div style="background:#10b981;height:8px;width:100%;border-radius:4px;display:inline-block;margin-left:6px"></div> <span style="color:#10b981">Quantum-Safe! ✅</span></div>
        </div>
    </div>
</div>

<div id="msg">Type a message to encrypt it!</div>
<div id="fact-box"></div>
</div>

<script>
let currentCipher = "substitution";
let challengeLevel = 1;
let score = 0, streak = 0;
let challengeResults = [];
let hintUsed = false;
let factTimeout = null;

const SUB_MAP = {
    a:"q",b:"w",c:"e",d:"r",e:"t",f:"y",g:"u",h:"i",i:"o",j:"p",
    k:"a",l:"s",m:"d",n:"f",o:"g",p:"h",q:"j",r:"k",s:"l",t:"z",
    u:"x",v:"c",w:"v",x:"b",y:"n",z:"m"
};
const REV_SUB = Object.fromEntries(Object.entries(SUB_MAP).map(([k,v])=>[v,k]));

const CHALLENGES = [
    {level:1, cipher:"substitution", plain:"HELLO",      hint:"5 letters, a greeting!"},
    {level:2, cipher:"caesar",       plain:"CAT",         hint:"A furry animal with 3 letters"},
    {level:3, cipher:"substitution", plain:"QUANTUM",     hint:"Related to physics and computing!"},
    {level:4, cipher:"reverse",      plain:"SECRET",      hint:"Something hidden — 6 letters"},
    {level:5, cipher:"caesar",       plain:"KYBER",       hint:"A NIST post-quantum algorithm!"},
    {level:6, cipher:"substitution", plain:"ENCRYPT",     hint:"What you do to a secret message"},
    {level:7, cipher:"reverse",      plain:"LATTICE",     hint:"The math behind Kyber — 7 letters"},
    {level:8, cipher:"caesar",       plain:"QUANTUM SAFE",hint:"Two words: describes Kyber"},
    {level:9, cipher:"substitution", plain:"NIST FIPS",   hint:"The organization that standardized PQC"},
    {level:10,cipher:"reverse",      plain:"SHOR ATTACK", hint:"Two words: how quantum breaks RSA"},
    {level:11,cipher:"caesar",       plain:"POST QUANTUM",hint:"Two words: the new era of cryptography"},
    {level:12,cipher:"substitution", plain:"KYBER WINS",  hint:"Two words: the quantum-safe future!"},
];

const CIPHER_INFO = {
    substitution: "Each letter maps to a different letter — like a secret code!",
    caesar: "Shift each letter 3 positions forward in the alphabet (A→D, B→E...)",
    reverse: "Reverse the entire message!",
    morse: "Convert to dots and dashes (Morse code)",
};

function applySubstitution(text){
    return text.split("").map(c=>{
        if(/[a-z]/.test(c)) return SUB_MAP[c]||c;
        if(/[A-Z]/.test(c)) return (SUB_MAP[c.toLowerCase()]||c).toUpperCase();
        return c;
    }).join("");
}

function applyCaesar(text, shift=3){
    return text.split("").map(c=>{
        if(/[a-zA-Z]/.test(c)){
            const base=c<="Z"?65:97;
            return String.fromCharCode((c.charCodeAt(0)-base+shift+26)%26+base);
        }
        return c;
    }).join("");
}

function applyReverse(text){ return text.split("").reverse().join(""); }

function applyMorse(text){
    const M={"A":".-","B":"-...","C":"-.-.","D":"-..","E":".","F":"..-.","G":"--.","H":"....","I":"..","J":".---","K":"-.-","L":".-..","M":"--","N":"-.","O":"---","P":".--.","Q":"--.-","R":".-.","S":"...","T":"-","U":"..-","V":"...-","W":".--","X":"-..-","Y":"-.--","Z":"--.."," ":"/"};
    return text.toUpperCase().split("").map(c=>M[c]||c).join(" ");
}

function applycipher(text, cipher){
    switch(cipher){
        case "substitution": return applySubstitution(text);
        case "caesar": return applyCaesar(text);
        case "reverse": return applyReverse(text);
        case "morse": return applyMorse(text);
        default: return text;
    }
}

function encryptChallenge(plain, cipher){ return applycipher(plain, cipher); }

function setCipher(cipher, btn){
    currentCipher = cipher;
    document.querySelectorAll(".cipher-btn").forEach(b=>b.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById("cipher-info").textContent = CIPHER_INFO[cipher];
    encrypt();
}

function encrypt(){
    const input = document.getElementById("plain-input").value;
    if(!input){document.getElementById("cipher-output").textContent="—";return;}
    const encrypted = applycipher(input, currentCipher);
    document.getElementById("cipher-output").textContent = encrypted;
}

function copyEncrypted(){
    const text = document.getElementById("cipher-output").textContent;
    if(navigator.clipboard) navigator.clipboard.writeText(text);
    setMsg("📋 Copied to clipboard!","#10b981");
}

function showKeyMap(){
    const km = document.getElementById("key-map");
    km.style.display = km.style.display==="none"?"block":"none";
    const kd = document.getElementById("key-display");
    kd.innerHTML = Object.entries(SUB_MAP).map(([k,v])=>
        `<div class="key-pair">${k.toUpperCase()}→<span>${v.toUpperCase()}</span></div>`
    ).join("");
}

function showTab(tab){
    ["encrypt","decode","learn"].forEach(t=>{
        document.getElementById("tab-"+t).style.display=t===tab?"block":"none";
    });
    document.querySelectorAll(".tab").forEach((t,i)=>{
        t.classList.toggle("active",["encrypt","decode","learn"][i]===tab);
    });
    if(tab==="decode") loadChallenge();
}

function loadChallenge(){
    const ch = CHALLENGES[Math.min(challengeLevel-1, CHALLENGES.length-1)];
    const encrypted = encryptChallenge(ch.plain, ch.cipher);
    document.getElementById("challenge-badge").textContent="Level "+challengeLevel+" — "+ch.cipher.charAt(0).toUpperCase()+ch.cipher.slice(1)+" Cipher";
    document.getElementById("challenge-title").textContent="🕵️ Decode this "+ch.cipher+" message!";
    document.getElementById("challenge-hint").textContent="Cipher: "+ch.cipher+" | Hint available if stuck";
    document.getElementById("challenge-msg").textContent=encrypted;
    document.getElementById("decode-input").value="";
    document.getElementById("next-challenge").style.display="none";
    hintUsed=false;
    buildProgress();
    updateHUD();
}

function checkDecode(){
    const answer = document.getElementById("decode-input").value.trim().toUpperCase();
    const ch = CHALLENGES[Math.min(challengeLevel-1, CHALLENGES.length-1)];
    if(answer === ch.plain.toUpperCase()){
        const pts = hintUsed?50:100*(challengeLevel);
        score += pts;
        streak++;
        challengeResults[challengeLevel-1]="done";
        buildProgress();
        updateHUD();
        setMsg("🎉 CORRECT! +"+pts+" pts"+(streak>1?" 🔥×"+streak:"")+(hintUsed?" (hint used)":""),"#10b981");
        showFact("✅ "+getCipherFact(ch.cipher),"#10b981");
        document.getElementById("next-challenge").style.display="inline-block";
    } else {
        streak=0;
        score=Math.max(0,score-10);
        updateHUD();
        setMsg("❌ Not quite! The message is: "+ch.plain.length+" letters. Try again!","#ef4444");
    }
}

function getDecodeHint(){
    const ch = CHALLENGES[Math.min(challengeLevel-1, CHALLENGES.length-1)];
    hintUsed=true;
    setMsg("💡 Hint: "+ch.hint+" | Cipher: "+ch.cipher,"#a78bfa");
    score=Math.max(0,score-25);
    updateHUD();
}

function nextChallenge(){
    if(challengeLevel>=12){
        setMsg("🏆 ALL 12 CHALLENGES COMPLETE! You are a Cipher Master! Score: "+score,"#fbbf24");
        return;
    }
    challengeLevel++;
    loadChallenge();
}

function getCipherFact(cipher){
    const facts={
        substitution:"Substitution ciphers were used by Julius Caesar 2,000 years ago — but frequency analysis breaks them in minutes!",
        caesar:"Caesar cipher has only 25 possible keys — a quantum computer could try all of them in nanoseconds!",
        reverse:"Simple reversals are the weakest cipher — but they teach the concept of transformation!",
        morse:"Morse code is not encryption — it's an encoding. Anyone with a chart can decode it!",
    };
    return facts[cipher]||"Even complex classical ciphers fail against quantum computers — that's why we need Kyber!";
}

function buildProgress(){
    let html="";
    for(let i=0;i<12;i++){
        let cls="pdot";
        if(i<challengeResults.length) cls+=" "+(challengeResults[i]==="done"?"done":"failed");
        else if(i===challengeLevel-1) cls+=" current";
        html+=`<div class="${cls}"></div>`;
    }
    document.getElementById("progress").innerHTML=html;
}

function updateHUD(){
    document.getElementById("h-score").textContent=score;
    document.getElementById("h-level").textContent=challengeLevel;
    document.getElementById("h-streak").textContent=streak;
}

function setMsg(m,c){
    let el=document.getElementById("msg");
    el.textContent=m; el.style.color=c||"#34d399";
}

function showFact(text,color){
    let el=document.getElementById("fact-box");
    el.textContent=text; el.style.display="block";
    el.style.borderColor=(color||"#3b82f6")+"50";
    if(factTimeout) clearTimeout(factTimeout);
    factTimeout=setTimeout(()=>el.style.display="none",6000);
}

// Init
encrypt();
buildProgress();
</script>
</body>
</html>
""", height=750)


def render_ctf_game():
    """Free game: QuantumVault CTF — Operation Quantum Shield — Real PQC Capture The Flag!"""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("🚩 Operation Quantum Shield — PQC Capture The Flag!")
    st.markdown(
        "**You are a PQC Agent.** 12 missions. Each hides a FLAG behind a real cryptography challenge. "
        "Solve puzzles, crack codes, identify algorithms, and stop the quantum attackers. "
        "Faster = more points. **FREE to play!**"
    )
    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow-x:hidden;}
#wrap{display:flex;flex-direction:column;align-items:center;padding:10px;max-width:560px;margin:0 auto;}

/* HUD */
.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:3px;width:100%;margin-bottom:6px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:5px 3px;
    text-align:center;font-size:9px;color:#60a5fa;transition:background 0.3s;}
.hb b{display:block;font-size:14px;color:white;}
.hb.flash{background:#1d4ed8;}

/* Mission select */
#mission-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;width:100%;margin:6px 0;}
.mission-btn{background:#071520;border:2px solid #1a3a5a;border-radius:10px;padding:8px 4px;
    text-align:center;cursor:pointer;transition:all 0.2s;font-size:10px;}
.mission-btn:hover{border-color:#3b82f6;background:#0a1f35;}
.mission-btn.locked{opacity:0.4;cursor:not-allowed;}
.mission-btn.completed{border-color:#10b981;background:#071f15;}
.mission-btn.active{border-color:#fbbf24;background:#1a1500;}
.mission-btn .m-num{font-size:16px;font-weight:900;color:#60a5fa;}
.mission-btn.completed .m-num{color:#10b981;}
.mission-btn .m-flag{font-size:11px;}

/* Mission card */
#mission-card{background:#071520;border:2px solid #1d4ed8;border-radius:14px;
    padding:14px;width:100%;margin:6px 0;display:none;}
#mission-card.visible{display:block;}
.mission-header{display:flex;align-items:center;gap:10px;margin-bottom:10px;}
.mission-icon{font-size:2rem;}
.mission-meta h3{color:#60a5fa;font-size:14px;margin-bottom:2px;}
.mission-meta p{color:#475569;font-size:10px;}
.diff-badge{display:inline-block;border-radius:4px;padding:2px 8px;font-size:9px;font-weight:bold;}
.diff-easy{background:#059669;color:white;}
.diff-medium{background:#d97706;color:white;}
.diff-hard{background:#dc2626;color:white;}

/* Timer bar */
#timer-wrap{width:100%;margin:6px 0;}
#timer-bar{height:8px;background:#1e293b;border-radius:4px;overflow:hidden;}
#timer-fill{height:100%;background:linear-gradient(90deg,#10b981,#3b82f6);
    border-radius:4px;transition:width 0.5s;}
#timer-text{font-size:10px;color:#60a5fa;text-align:right;margin-top:2px;}

/* Challenge area */
#challenge-area{background:#051018;border:1px solid #1a3a5a;border-radius:10px;
    padding:12px;margin:8px 0;width:100%;}
.challenge-text{font-size:12px;color:#94a3b8;line-height:1.7;margin-bottom:10px;}
.code-block{background:#020d14;border:1px solid #1a3a5a;border-radius:6px;
    padding:8px 10px;font-family:'Fira Code',monospace;font-size:11px;
    color:#10b981;margin:6px 0;word-break:break-all;line-height:1.6;}
.options-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:8px 0;}
.option-btn{padding:8px 10px;border-radius:8px;border:2px solid #1a3a5a;
    background:#071520;color:#94a3b8;font-size:11px;cursor:pointer;
    text-align:left;transition:all 0.15s;line-height:1.4;}
.option-btn:hover{border-color:#3b82f6;color:white;background:#0a1f35;}
.option-btn.correct{border-color:#10b981;background:#071f15;color:#10b981;}
.option-btn.wrong{border-color:#ef4444;background:#1a0505;color:#ef4444;}
.flag-input-wrap{display:flex;gap:6px;margin:8px 0;}
.flag-input{flex:1;background:#020d14;border:2px solid #1d4ed8;border-radius:8px;
    color:#10b981;font-family:'Fira Code',monospace;font-size:13px;padding:8px 10px;
    outline:none;}
.flag-input:focus{border-color:#60a5fa;}
.flag-input::placeholder{color:#1e3a5a;}
.submit-btn{padding:8px 16px;border-radius:8px;border:none;cursor:pointer;
    background:linear-gradient(135deg,#1d4ed8,#06b6d4);color:white;
    font-size:12px;font-weight:bold;}
.submit-btn:hover{filter:brightness(1.2);}

/* Hint system */
.hint-wrap{display:flex;gap:5px;flex-wrap:wrap;align-items:center;margin:6px 0;}
.hint-btn{padding:4px 10px;border-radius:6px;border:1px solid #334155;
    background:#071520;color:#60a5fa;font-size:10px;cursor:pointer;}
.hint-btn:hover{border-color:#1d4ed8;}
#hint-text{font-size:10px;color:#a78bfa;margin-top:4px;display:none;line-height:1.5;}

/* Messages */
#msg{font-size:12px;min-height:20px;margin:4px;text-align:center;
    font-weight:bold;width:100%;}
#fact-box{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);
    border-radius:8px;padding:8px 12px;margin:4px 0;font-size:10px;color:#93c5fd;
    display:none;line-height:1.5;width:100%;}

/* Flag capture animation */
#flag-capture{display:none;position:fixed;top:0;left:0;right:0;bottom:0;
    background:rgba(2,13,20,0.95);z-index:999;flex-direction:column;
    align-items:center;justify-content:center;text-align:center;}
#flag-capture.show{display:flex;}
.flag-emoji{font-size:5rem;animation:flagWave 0.5s ease-out;}
@keyframes flagWave{0%{transform:scale(0) rotate(-20deg)}70%{transform:scale(1.2) rotate(5deg)}100%{transform:scale(1) rotate(0)}}
.flag-title{font-size:1.8rem;font-weight:900;color:#10b981;margin:10px 0;}
.flag-pts{font-size:1rem;color:#60a5fa;margin-bottom:16px;}
.continue-btn{padding:10px 24px;border-radius:8px;border:none;cursor:pointer;
    background:linear-gradient(135deg,#059669,#10b981);color:white;
    font-size:14px;font-weight:bold;}

/* Btns */
.btns{display:flex;gap:5px;flex-wrap:wrap;justify-content:center;margin:6px 0;}
.btn{padding:7px 16px;border-radius:8px;border:none;cursor:pointer;
    font-size:12px;font-weight:bold;color:white;}
.btn-start{background:linear-gradient(135deg,#1d4ed8,#06b6d4);}
.btn-back{background:#334155;}

/* Progress dots */
.progress{display:flex;gap:4px;justify-content:center;margin:4px 0;flex-wrap:wrap;}
.pdot{width:10px;height:10px;border-radius:50%;background:#1e293b;border:1px solid #334155;}
.pdot.done{background:#10b981;}.pdot.active{background:#fbbf24;}
</style>
</head>
<body>

<!-- Flag Capture Overlay -->
<div id="flag-capture">
    <div class="flag-emoji">🚩</div>
    <div class="flag-title">FLAG CAPTURED!</div>
    <div id="flag-pts" class="flag-pts">+500 pts</div>
    <div id="flag-text" style="color:#94a3b8;font-size:11px;max-width:300px;margin-bottom:16px;line-height:1.6;"></div>
    <button class="continue-btn" onclick="closeFlagCapture()">Continue Mission →</button>
</div>

<div id="wrap">
<div class="hud">
    <div class="hb" id="hb-score">⭐ Score<br><b id="h-score">0</b></div>
    <div class="hb" id="hb-flags">🚩 Flags<br><b id="h-flags">0</b>/12</div>
    <div class="hb" id="hb-hints">💡 Hints<br><b id="h-hints">3</b></div>
    <div class="hb" id="hb-rank">🏆 Rank<br><b id="h-rank">Recruit</b></div>
</div>

<div class="progress" id="progress-dots"></div>

<!-- Mission Select -->
<div id="mission-select">
    <div style="text-align:center;margin:8px 0">
        <div style="font-size:1.1rem;font-weight:bold;color:#60a5fa">🚩 SELECT YOUR MISSION</div>
        <div style="font-size:10px;color:#475569;margin-top:2px">Complete missions in order to unlock harder ones</div>
    </div>
    <div id="mission-grid"></div>
    <div style="text-align:center;margin-top:8px;font-size:10px;color:#475569">
        🔓 Complete each mission to unlock the next | 💡 Hints cost 50pts each
    </div>
</div>

<!-- Active Mission -->
<div id="mission-card">
    <div class="mission-header">
        <div class="mission-icon" id="m-icon">🔐</div>
        <div class="mission-meta">
            <h3 id="m-title">Mission 1</h3>
            <p id="m-subtitle">Difficulty: Easy</p>
            <span class="diff-badge diff-easy" id="m-diff">EASY</span>
        </div>
    </div>
    <div id="timer-wrap">
        <div id="timer-bar"><div id="timer-fill" style="width:100%"></div></div>
        <div id="timer-text">⏱️ Time remaining: --</div>
    </div>
    <div id="challenge-area"></div>
    <div class="hint-wrap">
        <button class="hint-btn" onclick="useHint(1)">💡 Hint 1</button>
        <button class="hint-btn" onclick="useHint(2)">💡 Hint 2</button>
        <button class="hint-btn" onclick="useHint(3)">💡 Hint 3</button>
        <span style="font-size:9px;color:#334155">(-50pts each)</span>
    </div>
    <div id="hint-text"></div>
    <div id="msg"></div>
    <div id="fact-box"></div>
    <div class="btns">
        <button class="btn btn-back" onclick="backToSelect()">← Missions</button>
    </div>
</div>

</div>

<script>
const MISSIONS = [
    {
        id:1, icon:"🔐", title:"The RSA Breach",
        subtitle:"Identify the vulnerable algorithm", diff:"EASY", pts:200, time:90,
        type:"mcq",
        challenge:"<b>SITUATION:</b> Our intelligence shows an enemy quantum computer just broke into a government server. The server was using one of these encryption algorithms. Which one did Shor's Algorithm break?",
        options:[
            {text:"ML-KEM (Kyber) FIPS 203 — Module Learning With Errors", correct:false},
            {text:"RSA-2048 — Prime factorization based encryption", correct:true},
            {text:"SLH-DSA (SPHINCS+) FIPS 205 — Hash-based signatures", correct:false},
            {text:"ML-DSA (Dilithium) FIPS 204 — Lattice signatures", correct:false},
        ],
        flag:"FLAG{SH0R_BREAKS_RS4}",
        fact:"Shor's Algorithm factors large prime numbers exponentially faster than classical computers — instantly breaking RSA-2048 which protects most internet traffic today!",
        hints:["Think about which algorithm uses prime factorization as its security basis","Shor's Algorithm specifically targets problems involving large prime numbers","RSA = Rivest–Shamir–Adleman — named after its inventors who used primes as the hard problem"],
    },
    {
        id:2, icon:"🔤", title:"The Caesar Intercept",
        subtitle:"Decode the enemy message", diff:"EASY", pts:250, time:80,
        type:"decode",
        challenge:"<b>INTERCEPTED TRANSMISSION:</b> Enemy agents sent this encoded message. They used a Caesar cipher shifted by 13 (ROT13). Decode it to find the FLAG — the decoded message IS the flag:<br><br>",
        code:"SYNT{PNR F4E_VF_J34X}",
        flag:"FLAG{CAE S4R_IS_W34K}",
        fact:"Caesar cipher only has 25 possible keys — a quantum computer tries all of them in nanoseconds! This is why we need Kyber's lattice math which has astronomically more possible keys.",
        hints:["ROT13 means shift each letter 13 positions back in the alphabet","A→N, B→O, C→P... N→A, O→B etc. Numbers stay the same","Try: S→F, Y→L, T→A, N→G = FLAG..."],
    },
    {
        id:3, icon:"🌀", title:"Kyber Key Hunt",
        subtitle:"Find the correct Kyber property", diff:"EASY", pts:300, time:80,
        type:"mcq",
        challenge:"<b>BRIEFING:</b> NIST finalized ML-KEM (Kyber) as FIPS 203 in August 2024. Your mission: identify the correct mathematical problem that makes Kyber quantum-safe. The enemy thinks they can break it — prove them wrong.",
        options:[
            {text:"Integer Factorization — finding prime factors of large numbers", correct:false},
            {text:"Discrete Logarithm Problem — used in elliptic curve cryptography", correct:false},
            {text:"Module Learning With Errors (M-LWE) — finding a secret in a noisy lattice", correct:true},
            {text:"Knapsack Problem — subset sum cryptography", correct:false},
        ],
        flag:"FLAG{LW3_L4TT1C3_M4TH}",
        fact:"Module-LWE: given a matrix A and vector b = As + e (where s is secret and e is noise), find s. Even quantum computers can't solve this efficiently — that's why Kyber is quantum-safe!",
        hints:["Kyber is based on lattice cryptography, not prime numbers","LWE stands for Learning With Errors","The security comes from the hardness of finding a secret vector hidden in random-looking equations"],
    },
    {
        id:4, icon:"🔢", title:"The Prime Trap",
        subtitle:"Factor the semiprime before time runs out", diff:"MEDIUM", pts:400, time:70,
        type:"factor",
        challenge:"<b>ENEMY TRAP:</b> The enemy locked a server with RSA using this small key. Factor it to prove RSA is breakable. Enter the two prime factors (p and q where p < q):",
        number:3127,
        p:53, q:59,
        flag:"FLAG{RS4_F4CT0R3D}",
        fact:"3127 = 53 × 59. Real RSA uses primes with 150+ digits each — impossible to factor classically but trivial for Shor's Algorithm! That's why NIST chose Kyber instead.",
        hints:["Try dividing 3127 by prime numbers starting from 47","53 is one of the factors","53 × 59 = ?"],
    },
    {
        id:5, icon:"✍️", title:"Signature Forgery",
        subtitle:"Which signature stops quantum forgery", diff:"MEDIUM", pts:450, time:70,
        type:"mcq",
        challenge:"<b>CRISIS:</b> An enemy quantum computer forged a digital signature on a software update — millions of devices installed malware. Which NIST signature algorithm would have PREVENTED this attack?",
        options:[
            {text:"ECDSA — Elliptic Curve Digital Signature Algorithm", correct:false},
            {text:"RSA-PSS — Probabilistic Signature Scheme", correct:false},
            {text:"ML-DSA (Dilithium) FIPS 204 — Module Lattice Digital Signatures", correct:true},
            {text:"HMAC-SHA256 — Hash-based Message Authentication", correct:false},
        ],
        flag:"FLAG{D1L1TH1UM_S1GNS}",
        fact:"ML-DSA (Dilithium) FIPS 204 uses Module-LWE and Module-SIS lattice problems. It creates unforgeable signatures even against quantum computers — protecting software updates, certificates, and legal documents!",
        hints:["ECDSA and RSA-PSS are both quantum-vulnerable via Shor's Algorithm","Look for the NIST PQC standard (FIPS number)","Dilithium was standardized as FIPS 204 in August 2024"],
    },
    {
        id:6, icon:"🌲", title:"The Hash Fortress",
        subtitle:"Decode the SHA-3 avalanche", diff:"MEDIUM", pts:500, time:65,
        type:"mcq",
        challenge:"<b>INTEL:</b> SPHINCS+ (SLH-DSA FIPS 205) uses hash functions instead of lattice math. An agent changed ONE character in a message and the hash completely changed — this is the avalanche effect. Which property makes SHA-3 quantum-resistant enough for SPHINCS+?",
        options:[
            {text:"SHA-3 can be reversed to find the original message", correct:false},
            {text:"SHA-3 outputs are always 32 bytes regardless of input size", correct:false},
            {text:"SHA-3 requires 2^128 quantum operations to find a collision — still infeasible", correct:true},
            {text:"SHA-3 uses prime numbers internally like RSA", correct:false},
        ],
        flag:"FLAG{H4SH_4V4L4NCH3}",
        fact:"Grover's Algorithm gives quantum computers a square-root speedup on brute force — reducing SHA-3-256 security from 2^256 to 2^128 operations. Still too hard! That's why SHA-3 based SPHINCS+ remains quantum-safe.",
        hints:["Grover's Algorithm gives a quadratic speedup, not exponential","SHA-3-256 with 256-bit security becomes 128-bit against quantum — still secure","The key is that Grover helps but doesn't completely break hash functions like Shor breaks RSA"],
    },
    {
        id:7, icon:"🦅", title:"Falcon Files",
        subtitle:"Identify the smallest signature standard", diff:"MEDIUM", pts:550, time:60,
        type:"mcq",
        challenge:"<b>FIELD REPORT:</b> IoT devices and smart cards need tiny digital signatures — every byte matters. One NIST PQC standard produces the SMALLEST signatures of all four. Which is it and what lattice does it use?",
        options:[
            {text:"ML-KEM (Kyber) FIPS 203 — Module-LWE lattice", correct:false},
            {text:"ML-DSA (Dilithium) FIPS 204 — Module lattice", correct:false},
            {text:"FN-DSA (Falcon) FIPS 206 — NTRU lattice, smallest signatures", correct:true},
            {text:"SLH-DSA (SPHINCS+) FIPS 205 — Hash-based, largest signatures", correct:false},
        ],
        flag:"FLAG{F4LC0N_NTR U_NTRU}",
        fact:"Falcon (FN-DSA FIPS 206) uses NTRU lattices and produces signatures about 3x smaller than Dilithium — critical for IoT sensors, smart cards, and embedded systems where storage is measured in kilobytes!",
        hints:["SPHINCS+ actually has the LARGEST signatures of the four","Falcon uses a different type of lattice — NTRU — not Module-LWE","FN-DSA = Falcon NTRU Digital Signature Algorithm"],
    },
    {
        id:8, icon:"🕵️", title:"The NIST Timeline",
        subtitle:"Complete the PQC timeline", diff:"HARD", pts:650, time:55,
        type:"mcq",
        challenge:"<b>CLASSIFIED:</b> You've captured an enemy document showing their timeline for breaking RSA. Your handler asks: when did NIST officially finalize the first 4 post-quantum cryptography standards, and what law requires US agencies to migrate?",
        options:[
            {text:"January 2022 — Executive Order 14028 on Cybersecurity", correct:false},
            {text:"August 2024 — FIPS 203/204/205/206 + NSM-10 migration mandate by 2035", correct:true},
            {text:"December 2023 — NIST Special Publication 800-208", correct:false},
            {text:"March 2025 — Presidential Policy Directive 41", correct:false},
        ],
        flag:"FLAG{N1ST_2024_F1PS}",
        fact:"NIST finalized FIPS 203 (Kyber), 204 (Dilithium), 205 (SPHINCS+), and 206 (Falcon) in August 2024. National Security Memorandum 10 (NSM-10) requires ALL US federal agencies to migrate by 2035!",
        hints:["This happened very recently — after 2023","Look for the FIPS numbers 203, 204, 205, 206","NSM-10 = National Security Memorandum 10"],
    },
    {
        id:9, icon:"⚡", title:"Harvest Now Decrypt Later",
        subtitle:"Identify the current quantum threat", diff:"HARD", pts:700, time:55,
        type:"mcq",
        challenge:"<b>URGENT ALERT:</b> Intelligence confirms enemy agents are already collecting encrypted government communications — even though quantum computers can't break them yet. What is this attack called and why is it dangerous RIGHT NOW?",
        options:[
            {text:"Man-in-the-Middle Attack — intercepting communications in real time", correct:false},
            {text:"Harvest Now Decrypt Later — storing encrypted data to decrypt when quantum computers arrive", correct:true},
            {text:"Replay Attack — resending old captured packets", correct:false},
            {text:"Side Channel Attack — measuring power consumption to find keys", correct:false},
        ],
        flag:"FLAG{H4RV3ST_N0W_D3CRYPT}",
        fact:"Harvest Now Decrypt Later (HNDL) is happening TODAY. Nation-states are storing encrypted government communications, medical records, and financial data — waiting for quantum computers to arrive and decrypt it all. This is why migrating to Kyber NOW is urgent!",
        hints:["This attack doesn't need a quantum computer today","The threat is about storing data for future decryption","The name literally describes the two-phase attack: collect now, decrypt when quantum computers exist"],
    },
    {
        id:10, icon:"🔬", title:"The LWE Lab",
        subtitle:"Solve a baby LWE problem", diff:"HARD", pts:800, time:50,
        type:"lwe",
        challenge:"<b>MATH LAB:</b> Learning With Errors (LWE) is the math behind Kyber. In this baby version: we have secret <b>s = 3</b>, modulus <b>q = 11</b>. Given equation: <b>(7 × s + noise) mod 11 = ?</b><br><br>With noise = 1, calculate the result. This is one equation in a real Kyber key — enemies must solve thousands of these simultaneously to break it!",
        answer:"10",
        flag:"FLAG{LW3_M4TH_PR0V3N}",
        fact:"(7 × 3 + 1) mod 11 = 22 mod 11 = 0... wait: 7×3=21, 21+1=22, 22 mod 11 = 0. Kyber uses vectors of thousands of these equations with unknown noise — finding s requires solving an NP-hard problem even for quantum computers!",
        hints:["Calculate 7 × 3 first","Then add the noise value of 1","Finally take mod 11 (remainder when divided by 11). 21+1=22, 22÷11=2 remainder ?"],
    },
    {
        id:11, icon:"🌍", title:"TLS 1.3 + Kyber",
        subtitle:"Identify the hybrid handshake", diff:"HARD", pts:900, time:45,
        type:"mcq",
        challenge:"<b>NETWORK INTERCEPT:</b> You captured a TLS 1.3 handshake from a quantum-safe connection. The key exchange used a hybrid approach combining classical and post-quantum algorithms. Which combination is Google Chrome and Cloudflare currently deploying?",
        options:[
            {text:"RSA-4096 + ML-DSA (Dilithium) hybrid", correct:false},
            {text:"X25519 + ML-KEM-768 (Kyber) hybrid key exchange", correct:true},
            {text:"ECDH-P384 + FN-DSA (Falcon) hybrid", correct:false},
            {text:"DH-4096 + SLH-DSA (SPHINCS+) hybrid", correct:false},
        ],
        flag:"FLAG{X25519_KYBER_TLS}",
        fact:"Google Chrome deployed X25519+Kyber hybrid TLS in 2023 — combining classical X25519 elliptic curve with ML-KEM-768 (Kyber). Hybrid means: secure against both classical AND quantum attacks during the transition period!",
        hints:["Google Chrome and Cloudflare already have this deployed in production","Kyber is specifically designed for key encapsulation — TLS key exchange","X25519 is a modern elliptic curve — not RSA"],
    },
    {
        id:12, icon:"💀", title:"FINAL: The Quantum Boss",
        subtitle:"Stop the CRQC before it breaks everything", diff:"HARD", pts:1500, time:40,
        type:"final",
        challenge:"<b>🚨 FINAL MISSION — CRYPTOGRAPHICALLY RELEVANT QUANTUM COMPUTER DETECTED 🚨</b><br><br>A hostile nation just activated a CRQC capable of breaking RSA-2048. You have 40 seconds to identify which COMBINATION of NIST standards protects ALL of the following: key exchange, digital signatures, AND provides a hash-based backup. Choose the complete quantum-safe stack:",
        options:[
            {text:"RSA-4096 + ECDSA + SHA-256 — just use bigger classical keys", correct:false},
            {text:"ML-KEM FIPS 203 + ML-DSA FIPS 204 + SLH-DSA FIPS 205 — complete PQC stack", correct:true},
            {text:"ML-KEM FIPS 203 only — Kyber handles everything", correct:false},
            {text:"FN-DSA FIPS 206 + SHA-3 — Falcon and hashes only", correct:false},
        ],
        flag:"FLAG{C0MPL3T3_PQC_ST4CK}",
        fact:"The complete NIST PQC stack: ML-KEM (Kyber) for key exchange in TLS/VPN, ML-DSA (Dilithium) for signing certificates and code, SLH-DSA (SPHINCS+) as hash-based backup. Together they protect all internet communications from quantum attacks!",
        hints:["You need THREE things: key exchange + signatures + backup","ML-KEM = key exchange. ML-DSA = signatures. SLH-DSA = hash backup","All four NIST standards have FIPS numbers: 203, 204, 205, 206"],
    },
];

const RANKS=["Recruit","Cadet","Analyst","Specialist","Agent","Senior Agent",
    "Cryptographer","PQC Expert","Cyber Guardian","NIST Scholar","PQC Champion","Quantum Master"];

let score=0, flagsCaptured=0, hintsLeft=3;
let missionStatus=new Array(12).fill("locked");
let currentMission=null, missionTimer=null, timeLeft=0, factTimeout=null;
let hintUsed=[false,false,false];

missionStatus[0]="available";

function buildMissionGrid(){
    const grid=document.getElementById("mission-grid");
    grid.innerHTML="";
    MISSIONS.forEach((m,i)=>{
        const status=missionStatus[i];
        const div=document.createElement("div");
        div.className="mission-btn "+(status==="locked"?"locked":status==="completed"?"completed":status==="active"?"active":"");
        div.innerHTML=`<div class="m-num">${m.id}</div><div>${m.icon}</div><div class="m-flag">${status==="completed"?"🚩✅":status==="locked"?"🔒":"🚩"}</div>`;
        div.onclick=()=>{if(status!=="locked") startMission(i);};
        grid.appendChild(div);
    });
}

function buildProgress(){
    const d=document.getElementById("progress-dots");
    d.innerHTML="";
    missionStatus.forEach(s=>{
        const dot=document.createElement("div");
        dot.className="pdot"+(s==="completed"?" done":s==="active"?" active":"");
        d.appendChild(dot);
    });
}

function startMission(idx){
    currentMission=idx;
    const m=MISSIONS[idx];
    missionStatus[idx]="active";
    hintUsed=[false,false,false];
    document.getElementById("hint-text").style.display="none";
    document.getElementById("hint-text").textContent="";
    document.getElementById("fact-box").style.display="none";
    document.getElementById("msg").textContent="";

    document.getElementById("mission-select").style.display="none";
    document.getElementById("mission-card").classList.add("visible");

    document.getElementById("m-icon").textContent=m.icon;
    document.getElementById("m-title").textContent="Mission "+m.id+": "+m.title;
    document.getElementById("m-subtitle").textContent=m.subtitle;
    const diffEl=document.getElementById("m-diff");
    diffEl.textContent=m.diff;
    diffEl.className="diff-badge diff-"+m.diff.toLowerCase();

    buildChallenge(m);
    startTimer(m.time);
    updateHUD();
}

function buildChallenge(m){
    const area=document.getElementById("challenge-area");
    let html=`<div class="challenge-text">${m.challenge}</div>`;

    if(m.type==="mcq"||m.type==="final"){
        if(m.code) html+=`<div class="code-block">${m.code}</div>`;
        html+=`<div class="options-grid">`;
        m.options.forEach((opt,i)=>{
            html+=`<button class="option-btn" id="opt-${i}" onclick="selectOption(${i})">${opt.text}</button>`;
        });
        html+=`</div>`;
    } else if(m.type==="decode"){
        html+=`<div class="code-block">${m.code}</div>`;
        html+=`<div class="flag-input-wrap">
            <input class="flag-input" id="flag-answer" placeholder="FLAG{DECODED_MESSAGE}" 
                onkeydown="if(event.key==='Enter') submitFlag()"/>
            <button class="submit-btn" onclick="submitFlag()">🚩 Submit</button>
        </div>`;
    } else if(m.type==="factor"){
        html+=`<div style="text-align:center;margin:10px 0">
            <div style="font-size:2rem;font-weight:900;color:#60a5fa">${m.number}</div>
            <div style="font-size:11px;color:#475569;margin-top:4px">Find p and q where ${m.number} = p × q</div>
        </div>
        <div style="display:flex;gap:8px;align-items:center;justify-content:center;margin:8px 0">
            <input class="flag-input" id="factor-p" placeholder="p (smaller)" type="number" style="width:120px;text-align:center"/>
            <span style="color:#60a5fa;font-size:1.2rem">×</span>
            <input class="flag-input" id="factor-q" placeholder="q (larger)" type="number" style="width:120px;text-align:center"/>
        </div>
        <div style="text-align:center">
            <button class="submit-btn" onclick="submitFactor()">🔓 Factor It!</button>
        </div>`;
    } else if(m.type==="lwe"){
        html+=`<div class="code-block">s = 3, q = 11\n(7 × s + 1) mod 11 = ?</div>
        <div class="flag-input-wrap">
            <input class="flag-input" id="lwe-answer" placeholder="Enter your answer (a number)" 
                type="number" onkeydown="if(event.key==='Enter') submitLWE()"/>
            <button class="submit-btn" onclick="submitLWE()">✓ Submit</button>
        </div>`;
    }
    area.innerHTML=html;
}

function selectOption(i){
    const m=MISSIONS[currentMission];
    const opt=m.options[i];
    document.querySelectorAll(".option-btn").forEach(b=>{
        b.onclick=null;b.style.cursor="default";
    });
    if(opt.correct){
        document.getElementById("opt-"+i).classList.add("correct");
        captureFlag(m);
    } else {
        document.getElementById("opt-"+i).classList.add("wrong");
        // Show correct answer
        m.options.forEach((o,j)=>{if(o.correct)document.getElementById("opt-"+j).classList.add("correct");});
        missionFailed(m);
    }
}

function submitFlag(){
    const m=MISSIONS[currentMission];
    const answer=document.getElementById("flag-answer").value.trim().toUpperCase().replace(/\s/g,"");
    const correct=m.flag.replace(/\s/g,"");
    if(answer===correct){
        captureFlag(m);
    } else {
        setMsg("❌ Wrong flag! Check your decoding. Try again!","#ef4444");
        score=Math.max(0,score-20);
        updateHUD();
    }
}

function submitFactor(){
    const m=MISSIONS[currentMission];
    const p=parseInt(document.getElementById("factor-p").value)||0;
    const q=parseInt(document.getElementById("factor-q").value)||0;
    if((p===m.p&&q===m.q)||(p===m.q&&q===m.p)){
        captureFlag(m);
    } else if(p*q===m.number){
        setMsg("⚠️ "+p+"×"+q+"="+m.number+" but those aren't the prime factors! Think primes!","#f59e0b");
    } else {
        setMsg("❌ "+p+"×"+q+"="+(p*q)+" ≠ "+m.number+". Try again!","#ef4444");
        score=Math.max(0,score-20);
        updateHUD();
    }
}

function submitLWE(){
    const m=MISSIONS[currentMission];
    const ans=document.getElementById("lwe-answer").value.trim();
    if(ans===m.answer){
        captureFlag(m);
    } else {
        setMsg("❌ Not quite! Remember: (7×3+1) mod 11. Check your math!","#ef4444");
        score=Math.max(0,score-20);
        updateHUD();
    }
}

function captureFlag(m){
    clearInterval(missionTimer);
    const timePts=Math.floor(timeLeft/m.time*200);
    const hintPenalty=hintUsed.filter(h=>h).length*50;
    const pts=m.pts+timePts-hintPenalty;
    score+=pts;
    flagsCaptured++;
    missionStatus[currentMission]="completed";
    if(currentMission+1<12) missionStatus[currentMission+1]="available";
    updateHUD();

    // Show flag capture overlay
    document.getElementById("flag-pts").textContent="+"+pts+" pts ("+m.pts+" base + "+timePts+" speed bonus - "+hintPenalty+" hint penalty)";
    document.getElementById("flag-text").textContent=m.fact;
    document.getElementById("flag-capture").classList.add("show");
}

function missionFailed(m){
    clearInterval(missionTimer);
    missionStatus[currentMission]="available";
    setMsg("❌ Wrong! Study the correct answer then try again. -100 pts","#ef4444");
    score=Math.max(0,score-100);
    showFact("📚 "+m.fact,"#ef4444");
    updateHUD();
}

function closeFlagCapture(){
    document.getElementById("flag-capture").classList.remove("show");
    backToSelect();
}

function backToSelect(){
    clearInterval(missionTimer);
    currentMission=null;
    document.getElementById("mission-select").style.display="block";
    document.getElementById("mission-card").classList.remove("visible");
    document.getElementById("msg").textContent="";
    buildMissionGrid();
    buildProgress();
}

function startTimer(seconds){
    timeLeft=seconds;
    updateTimer();
    clearInterval(missionTimer);
    missionTimer=setInterval(()=>{
        timeLeft--;
        updateTimer();
        if(timeLeft<=0){
            clearInterval(missionTimer);
            const m=MISSIONS[currentMission];
            setMsg("⏰ TIME'S UP! Flag not captured. Try again!","#ef4444");
            showFact("📚 "+m.fact,"#ef4444");
            score=Math.max(0,score-50);
            missionStatus[currentMission]="available";
            updateHUD();
        }
    },1000);
}

function updateTimer(){
    const m=currentMission!==null?MISSIONS[currentMission]:null;
    const maxTime=m?m.time:90;
    const pct=timeLeft/maxTime*100;
    document.getElementById("timer-fill").style.width=pct+"%";
    document.getElementById("timer-fill").style.background=
        pct>60?"linear-gradient(90deg,#10b981,#3b82f6)":
        pct>30?"linear-gradient(90deg,#f59e0b,#d97706)":
        "linear-gradient(90deg,#ef4444,#dc2626)";
    document.getElementById("timer-text").textContent="⏱️ "+timeLeft+"s remaining"+(timeLeft<10?" — HURRY!":"");
}

function useHint(n){
    const m=currentMission!==null?MISSIONS[currentMission]:null;
    if(!m) return;
    if(hintsLeft<=0){setMsg("No hints left!","#f59e0b");return;}
    if(hintUsed[n-1]){setMsg("Already used hint "+n,"#f59e0b");return;}
    hintUsed[n-1]=true;
    hintsLeft--;
    score=Math.max(0,score-50);
    const hint=m.hints[n-1]||"No more hints available!";
    const ht=document.getElementById("hint-text");
    ht.style.display="block";
    ht.textContent="💡 Hint "+n+": "+hint;
    updateHUD();
}

function updateHUD(){
    document.getElementById("h-score").textContent=score;
    document.getElementById("h-flags").textContent=flagsCaptured;
    document.getElementById("h-hints").textContent=hintsLeft;
    const rankIdx=Math.min(flagsCaptured,RANKS.length-1);
    document.getElementById("h-rank").textContent=RANKS[rankIdx];
    buildMissionGrid();
    buildProgress();
}

function setMsg(m,c){
    let el=document.getElementById("msg");
    el.textContent=m;el.style.color=c||"#34d399";
}

function showFact(text,color){
    let el=document.getElementById("fact-box");
    el.textContent=text;el.style.display="block";
    el.style.borderColor=(color||"#3b82f6")+"50";
    if(factTimeout) clearTimeout(factTimeout);
    factTimeout=setTimeout(()=>el.style.display="none",7000);
}

// Init
buildMissionGrid();
buildProgress();
</script>
</body>
</html>
""", height=820)
