def render_quantum_sandbox():
    """Quantum Sandbox — Melon-style physics playground with PQC theme."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("🧪 Quantum Sandbox")
    st.markdown("**No rules. No score. Just quantum chaos!** Drag objects from the left panel onto the world.")

    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;overflow:hidden;}

#game{display:flex;width:100%;height:580px;position:relative;}

/* ── LEFT SPAWN PANEL ── */
#spawn-panel{
    width:110px;flex-shrink:0;
    background:#071520;
    border-right:2px solid #1a3a5a;
    display:flex;flex-direction:column;
    overflow:hidden;
}
#panel-title{
    background:#0a1f35;padding:8px 6px;
    font-size:10px;color:#60a5fa;font-weight:bold;
    letter-spacing:1px;text-align:center;
    border-bottom:1px solid #1a3a5a;
}
#panel-cats{
    display:flex;gap:2px;padding:4px;
    border-bottom:1px solid #1a3a5a;
    flex-wrap:wrap;justify-content:center;
}
.cat-btn{
    padding:3px 6px;border-radius:4px;border:1px solid #1a3a5a;
    background:transparent;color:#475569;font-size:9px;cursor:pointer;
    transition:all 0.1s;
}
.cat-btn:hover,.cat-btn.active{background:#1d4ed820;border-color:#3b82f6;color:#60a5fa;}
#spawn-items{
    flex:1;overflow-y:auto;padding:4px;
    scrollbar-width:thin;scrollbar-color:#1a3a5a transparent;
}
.spawn-item{
    display:flex;flex-direction:column;align-items:center;
    padding:6px 4px;border-radius:8px;border:1px solid #1a3a5a;
    background:#071520;cursor:grab;margin-bottom:4px;
    transition:all 0.15s;color:#94a3b8;font-size:9px;text-align:center;
}
.spawn-item:hover{background:#0a1f35;border-color:#3b82f6;color:white;
    transform:scale(1.05);}
.spawn-item:active{cursor:grabbing;}
.spawn-item .si-emoji{font-size:20px;margin-bottom:2px;}

/* ── WORLD CANVAS ── */
#world{flex:1;position:relative;overflow:hidden;cursor:crosshair;}
#cv{display:block;width:100%;height:100%;}

/* ── TOP HUD ── */
#hud{
    position:absolute;top:6px;left:6px;right:6px;
    display:flex;gap:4px;pointer-events:none;z-index:10;
}
.hud-pill{
    background:#071520cc;border:1px solid #1a3a5a;
    border-radius:20px;padding:3px 10px;font-size:10px;color:#60a5fa;
}

/* ── CONTEXT MENU ── */
#ctx-menu{
    position:absolute;background:#071520;border:1px solid #1d4ed8;
    border-radius:8px;padding:4px;z-index:100;display:none;
    box-shadow:0 4px 20px rgba(0,0,0,0.5);min-width:120px;
}
.ctx-item{
    padding:6px 12px;font-size:11px;color:#94a3b8;cursor:pointer;
    border-radius:4px;transition:all 0.1s;
}
.ctx-item:hover{background:#0a1f35;color:white;}

/* ── TOOLBAR ── */
#toolbar{
    position:absolute;bottom:6px;left:50%;transform:translateX(-50%);
    display:flex;gap:4px;z-index:10;
    background:#071520cc;border:1px solid #1a3a5a;
    border-radius:20px;padding:4px 8px;
}
.tool{
    padding:5px 10px;border-radius:12px;border:1px solid #1a3a5a;
    background:transparent;color:#60a5fa;font-size:10px;cursor:pointer;
    transition:all 0.15s;
}
.tool:hover{background:#1d4ed820;border-color:#3b82f6;}
.tool.active{background:#1d4ed8;border-color:#60a5fa;color:white;}

/* ── FACT TOAST ── */
#toast{
    position:absolute;bottom:50px;left:50%;transform:translateX(-50%);
    background:#071520ee;border:1px solid #3b82f6;border-radius:8px;
    padding:7px 14px;font-size:10px;color:#93c5fd;
    z-index:20;opacity:0;transition:opacity 0.3s;
    max-width:300px;text-align:center;pointer-events:none;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
#toast.show{opacity:1;}
</style>
</head>
<body>
<div id="game">

  <!-- SPAWN PANEL -->
  <div id="spawn-panel">
    <div id="panel-title">⬛ SPAWN</div>
    <div id="panel-cats">
      <button class="cat-btn active" onclick="setCat('agents')">🤖</button>
      <button class="cat-btn" onclick="setCat('weapons')">💥</button>
      <button class="cat-btn" onclick="setCat('props')">🏗️</button>
      <button class="cat-btn" onclick="setCat('effects')">✨</button>
    </div>
    <div id="spawn-items"></div>
  </div>

  <!-- WORLD -->
  <div id="world">
    <canvas id="cv"></canvas>

    <!-- HUD -->
    <div id="hud">
      <div class="hud-pill">🤖 <span id="h-obj">0</span> objects</div>
      <div class="hud-pill">💥 <span id="h-exp">0</span> explosions</div>
      <div class="hud-pill" id="h-fps">60 fps</div>
    </div>

    <!-- TOOLBAR -->
    <div id="toolbar">
      <button class="tool active" onclick="setTool('place')" id="t-place">✋ Place</button>
      <button class="tool" onclick="setTool('move')" id="t-move">🖐 Move</button>
      <button class="tool" onclick="setTool('delete')" id="t-delete">🗑 Delete</button>
      <button class="tool" onclick="resetWorld()" id="t-reset">🔄 Reset</button>
      <button class="tool" onclick="toggleGravity()" id="t-grav">🌍 Gravity</button>
      <button class="tool" onclick="explodeAll()" id="t-chaos">💥 CHAOS!</button>
    </div>

    <!-- CONTEXT MENU -->
    <div id="ctx-menu">
      <div class="ctx-item" onclick="ctxDelete()">🗑️ Delete</div>
      <div class="ctx-item" onclick="ctxFreeze()">❄️ Freeze</div>
      <div class="ctx-item" onclick="ctxExplode()">💥 Explode</div>
      <div class="ctx-item" onclick="ctxShield()">🔐 Add Shield</div>
      <div class="ctx-item" onclick="closeCtx()">✕ Close</div>
    </div>

    <!-- TOAST -->
    <div id="toast"></div>
  </div>

</div>

<script>
// ── CANVAS SETUP ──────────────────────────────────────────────────────────────
const cv = document.getElementById('cv');
const cx = cv.getContext('2d');
let W, H;
function resize(){
    const rect = document.getElementById('world').getBoundingClientRect();
    W = cv.width = rect.width;
    H = cv.height = rect.height;
}
resize();
window.addEventListener('resize', resize);

// ── SPAWN CATEGORIES ──────────────────────────────────────────────────────────
const CATEGORIES = {
    agents: [
        {emoji:'🤖', name:'Quantum Bot',  type:'agent',  mass:3, hp:100, color:'#3b82f6'},
        {emoji:'👾', name:'Shor Agent',   type:'enemy',  mass:3, hp:80,  color:'#ef4444'},
        {emoji:'🦾', name:'Cyber Guard',  type:'agent',  mass:4, hp:120, color:'#10b981'},
        {emoji:'👽', name:'Q-Alien',      type:'enemy',  mass:2, hp:60,  color:'#8b5cf6'},
        {emoji:'🧑‍💻', name:'Hacker',     type:'agent',  mass:3, hp:90,  color:'#f59e0b'},
        {emoji:'🦅', name:'Falcon Bot',   type:'agent',  mass:2, hp:80,  color:'#06b6d4'},
    ],
    weapons: [
        {emoji:'💣', name:'Shor Bomb',    type:'bomb',   mass:2, blast:80,  color:'#ef4444'},
        {emoji:'⚡', name:'Q-Zapper',     type:'zapper', mass:1, blast:40,  color:'#fbbf24'},
        {emoji:'🔥', name:'Laser',        type:'laser',  mass:1, blast:50,  color:'#f97316'},
        {emoji:'💥', name:'Mega Bomb',    type:'bomb',   mass:4, blast:160, color:'#dc2626'},
        {emoji:'🌊', name:'Grover Wave',  type:'wave',   mass:1, blast:30,  color:'#8b5cf6'},
        {emoji:'🎇', name:'Sparkle Mine', type:'mine',   mass:2, blast:60,  color:'#fbbf24'},
    ],
    props: [
        {emoji:'🏛️', name:'Server',      type:'prop',   mass:8,  hp:200, color:'#334155'},
        {emoji:'💾', name:'Data Vault',   type:'prop',   mass:6,  hp:150, color:'#1d4ed8'},
        {emoji:'📡', name:'Antenna',      type:'prop',   mass:3,  hp:80,  color:'#475569'},
        {emoji:'🔐', name:'Kyber Shield', type:'shield', mass:5,  hp:300, color:'#10b981'},
        {emoji:'🧱', name:'Wall Block',   type:'wall',   mass:10, hp:400, color:'#64748b'},
        {emoji:'🚀', name:'Q-Drone',      type:'drone',  mass:2,  hp:60,  color:'#06b6d4'},
        {emoji:'🏦', name:'Bank Node',    type:'prop',   mass:7,  hp:180, color:'#ca8a04'},
        {emoji:'⚙️', name:'Mechanism',   type:'prop',   mass:4,  hp:100, color:'#475569'},
    ],
    effects: [
        {emoji:'✨', name:'Sparkles',     type:'effect', mass:0.1, color:'#fbbf24'},
        {emoji:'🌀', name:'Vortex',       type:'vortex', mass:0.1, color:'#8b5cf6'},
        {emoji:'❄️', name:'Freeze Ray',   type:'freeze', mass:0.1, color:'#60a5fa'},
        {emoji:'🌪️', name:'Tornado',     type:'tornado',mass:0.1, color:'#94a3b8'},
        {emoji:'☠️', name:'Shor Ray',     type:'ray',    mass:0.1, color:'#ef4444'},
        {emoji:'🛡️', name:'Force Field', type:'field',  mass:0.1, color:'#10b981'},
    ],
};

const FACTS = [
    "🔐 Kyber (ML-KEM FIPS 203) protects data like a shield — even quantum computers can't break it!",
    "☠️ Shor's Algorithm can break RSA encryption — that's why we need post-quantum crypto!",
    "⚡ Quantum computers use qubits that can be 0 AND 1 at the same time — superposition!",
    "🌊 Grover's Algorithm speeds up searches — but Kyber is designed to resist it!",
    "🦅 Falcon (FIPS 206) makes tiny signatures perfect for small IoT devices!",
    "🏛️ Servers need Dilithium (ML-DSA FIPS 204) signatures to verify all messages!",
    "💾 Data vaults use ML-KEM to protect encryption keys — the keys to your secrets!",
    "🌀 Entanglement lets quantum computers try millions of keys simultaneously!",
    "🔧 NIST mandated quantum-safe crypto by 2035 — NSM-10 executive order!",
    "🛡️ SPHINCS+ (FIPS 205) uses hash trees — secure even if math is broken!",
];

// ── GAME STATE ────────────────────────────────────────────────────────────────
let objects = [];
let particles = [];
let explosions = [];
let currentTool = 'place';
let currentCat = 'agents';
let selectedItem = null;
let dragObj = null;
let dragOffX = 0, dragOffY = 0;
let ctxObj = null;
let gravityOn = true;
let totalExplosions = 0;
let frameCount = 0, fpsTime = performance.now(), fps = 60;

// ── SPAWN PANEL ───────────────────────────────────────────────────────────────
let selectedSpawnItem = CATEGORIES.agents[0];

function setCat(cat){
    currentCat = cat;
    document.querySelectorAll('.cat-btn').forEach(b=>b.classList.remove('active'));
    event.target.classList.add('active');
    buildPanel();
}

function buildPanel(){
    const items = CATEGORIES[currentCat];
    const container = document.getElementById('spawn-items');
    container.innerHTML = '';
    items.forEach(item=>{
        const div = document.createElement('div');
        div.className = 'spawn-item';
        div.innerHTML = `<span class="si-emoji">${item.emoji}</span>${item.name}`;
        div.title = item.name;
        div.onclick = ()=>{ selectedSpawnItem=item; showToast('Selected: '+item.name); };
        div.draggable = true;
        div.ondragstart = e=>{ selectedSpawnItem=item; };
        container.appendChild(div);
    });
}
buildPanel();

// ── OBJECT CREATION ───────────────────────────────────────────────────────────
function spawnObject(x, y, item){
    const obj = {
        x, y,
        vx: (Math.random()-0.5)*2,
        vy: -1,
        w: item.type==='wall'?80:40,
        h: item.type==='wall'?40:40,
        emoji: item.emoji,
        name: item.name,
        type: item.type,
        mass: item.mass||3,
        hp: item.hp||100,
        maxHp: item.hp||100,
        color: item.color||'#3b82f6',
        frozen: false,
        shielded: item.type==='shield',
        blast: item.blast||0,
        rotation: 0,
        rotVel: (Math.random()-0.5)*0.02,
        id: Math.random(),
        age: 0,
        activated: false,
    };
    objects.push(obj);
    updateHUD();

    // Auto activate effects
    if(['bomb','mine','zapper','laser','wave','ray'].includes(item.type)){
        setTimeout(()=>activateObject(obj), 800+Math.random()*600);
    }
    if(item.type==='drone'){
        obj.vx = (Math.random()-0.5)*3;
        obj.vy = -3;
    }

    showFactRandom();
    return obj;
}

// ── ACTIVATION ────────────────────────────────────────────────────────────────
function activateObject(obj){
    if(!obj||!objects.includes(obj)) return;
    obj.activated = true;

    if(obj.type==='bomb'||obj.type==='mine'){
        doExplosion(obj.x, obj.y, obj.blast||80);
        objects = objects.filter(o=>o!==obj);
    } else if(obj.type==='zapper'){
        // Shoot lightning to nearest object
        const nearest = objects.filter(o=>o!==obj&&o.type!=='zapper')
            .sort((a,b)=>dist2(a,obj)-dist2(b,obj))[0];
        if(nearest){
            spawnLightning(obj.x,obj.y,nearest.x,nearest.y);
            if(!nearest.shielded) nearest.hp-=40;
            if(nearest.hp<=0) objects=objects.filter(o=>o!==nearest);
        }
        objects=objects.filter(o=>o!==obj);
    } else if(obj.type==='wave'){
        // Grover wave — weaken all non-shielded
        explosions.push({x:obj.x,y:obj.y,r:0,maxR:250,alpha:0.7,color:'#8b5cf6',type:'wave'});
        objects.forEach(o=>{
            if(o!==obj&&!o.shielded&&o.hp){
                o.hp-=25; o.vx+=(Math.random()-0.5)*3; o.vy-=2;
            }
        });
        objects=objects.filter(o=>o!==obj);
    } else if(obj.type==='freeze'){
        objects.forEach(o=>{ if(o!==obj) o.frozen=true; });
        setTimeout(()=>objects.forEach(o=>o.frozen=false), 3000);
        objects=objects.filter(o=>o!==obj);
    } else if(obj.type==='tornado'){
        // Fling nearby objects
        objects.forEach(o=>{
            if(o!==obj){
                const angle=Math.atan2(o.y-obj.y,o.x-obj.x);
                o.vx+=Math.cos(angle+Math.PI/2)*5;
                o.vy+=Math.sin(angle+Math.PI/2)*5-3;
            }
        });
        objects=objects.filter(o=>o!==obj);
        explosions.push({x:obj.x,y:obj.y,r:0,maxR:120,alpha:0.8,color:'#94a3b8',type:'wave'});
    } else if(obj.type==='vortex'){
        objects.forEach(o=>{
            if(o!==obj){
                const dx=obj.x-o.x, dy=obj.y-o.y;
                const d=Math.sqrt(dx*dx+dy*dy)||1;
                o.vx+=dx/d*2; o.vy+=dy/d*2;
            }
        });
        objects=objects.filter(o=>o!==obj);
    } else if(obj.type==='ray'||obj.type==='laser'){
        // Shoot ray right
        for(let i=0;i<8;i++){
            particles.push({
                x:obj.x,y:obj.y,
                vx:Math.cos(i*Math.PI/4)*6,
                vy:Math.sin(i*Math.PI/4)*6,
                r:5,alpha:1,color:obj.color,type:'ray'
            });
        }
        objects=objects.filter(o=>o!==obj);
    } else if(obj.type==='field'){
        // Force field — push nearby objects away
        objects.forEach(o=>{
            if(o!==obj){
                const dx=o.x-obj.x, dy=o.y-obj.y;
                const d=Math.sqrt(dx*dx+dy*dy)||1;
                if(d<150){ o.vx+=dx/d*4; o.vy+=dy/d*4; }
            }
        });
        objects=objects.filter(o=>o!==obj);
        explosions.push({x:obj.x,y:obj.y,r:0,maxR:150,alpha:0.6,color:'#10b981',type:'wave'});
    }
    updateHUD();
}

// ── EXPLOSION ────────────────────────────────────────────────────────────────
function doExplosion(x, y, radius){
    totalExplosions++;
    explosions.push({x,y,r:0,maxR:radius,alpha:1,color:'#ef4444',type:'explosion'});
    // Spawn particles
    for(let i=0;i<20;i++){
        const a=Math.random()*Math.PI*2, s=2+Math.random()*6;
        particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s-2,
            r:3+Math.random()*4,alpha:1,
            color:['#ef4444','#f97316','#fbbf24'][Math.floor(Math.random()*3)],
            type:'debris'});
    }
    // Affect objects
    objects.forEach(o=>{
        const dx=o.x-x, dy=o.y-y, d=Math.sqrt(dx*dx+dy*dy)||1;
        if(d<radius){
            const force=(1-d/radius)*12;
            if(!o.frozen){ o.vx+=dx/d*force; o.vy+=dy/d*force-force*0.5; }
            if(!o.shielded){ o.hp-=(1-d/radius)*60; }
            if(o.type==='bomb'&&!o.activated&&d<radius*0.5){
                o.activated=true;
                setTimeout(()=>doExplosion(o.x,o.y,o.blast||80),200);
                objects=objects.filter(ob=>ob!==o);
            }
        }
    });
    objects=objects.filter(o=>o.hp>0||o.type==='wall'||o.type==='shield');
    updateHUD();
}

// ── LIGHTNING ────────────────────────────────────────────────────────────────
let lightnings=[];
function spawnLightning(x1,y1,x2,y2){
    lightnings.push({x1,y1,x2,y2,alpha:1,segments:makeLightningSegs(x1,y1,x2,y2)});
}
function makeLightningSegs(x1,y1,x2,y2){
    const segs=[{x:x1,y:y1}];
    const steps=8;
    for(let i=1;i<steps;i++){
        const t=i/steps;
        segs.push({
            x:x1+(x2-x1)*t+(Math.random()-0.5)*30,
            y:y1+(y2-y1)*t+(Math.random()-0.5)*30
        });
    }
    segs.push({x:x2,y:y2});
    return segs;
}
function dist2(a,b){ return (a.x-b.x)**2+(a.y-b.y)**2; }

// ── PHYSICS ───────────────────────────────────────────────────────────────────
const GRAVITY = 0.35;
const FRICTION = 0.82;
const GROUND_Y = () => H - 50;

function physicsUpdate(){
    objects.forEach(o=>{
        if(o.frozen) return;
        o.age++;

        // Gravity
        if(gravityOn && o.type!=='drone' && o.type!=='effect'){
            o.vy += GRAVITY * (o.mass/3);
        }
        // Drone hovers
        if(o.type==='drone'){
            o.vy += Math.sin(o.age*0.05)*0.2;
            o.vx *= 0.99;
        }

        // Move
        o.x += o.vx; o.y += o.vy;
        o.rotation += o.rotVel;

        // Floor collision
        const gy = GROUND_Y() - o.h/2;
        if(o.y > gy){
            o.y = gy;
            o.vy *= -0.4;
            o.vx *= FRICTION;
            o.rotVel *= 0.8;
            if(Math.abs(o.vy)<0.5) o.vy=0;
        }

        // Wall collision
        if(o.x < o.w/2){ o.x=o.w/2; o.vx*=-0.6; }
        if(o.x > W-o.w/2){ o.x=W-o.w/2; o.vx*=-0.6; }
        if(o.y < o.h/2){ o.y=o.h/2; o.vy*=-0.5; }

        // Object-object collision (simple AABB)
        objects.forEach(other=>{
            if(other===o) return;
            const dx=other.x-o.x, dy=other.y-o.y;
            const overlapX=( o.w/2+other.w/2)-Math.abs(dx);
            const overlapY=( o.h/2+other.h/2)-Math.abs(dy);
            if(overlapX>0&&overlapY>0){
                if(overlapX<overlapY){
                    const sign=dx>0?1:-1;
                    o.x-=sign*overlapX*0.3;
                    other.x+=sign*overlapX*0.3;
                    const relVx=o.vx-other.vx;
                    o.vx-=relVx*0.3; other.vx+=relVx*0.3;
                } else {
                    const sign=dy>0?1:-1;
                    o.y-=sign*overlapY*0.3;
                    other.y+=sign*overlapY*0.3;
                    const relVy=o.vy-other.vy;
                    o.vy-=relVy*0.3; other.vy+=relVy*0.3;
                }
            }
        });
    });

    // Particles
    particles.forEach(p=>{
        p.x+=p.vx; p.y+=p.vy; p.alpha-=0.025;
        if(gravityOn) p.vy+=0.15;
        p.r*=0.97;
    });
    particles=particles.filter(p=>p.alpha>0);

    // Explosions / waves
    explosions.forEach(e=>{ e.r+=e.type==='wave'?5:8; e.alpha-=0.04; });
    explosions=explosions.filter(e=>e.alpha>0);

    // Lightning
    lightnings.forEach(l=>l.alpha-=0.08);
    lightnings=lightnings.filter(l=>l.alpha>0);
}

// ── DRAW ─────────────────────────────────────────────────────────────────────
function draw(){
    cx.clearRect(0,0,W,H);

    // Sky gradient
    const sky=cx.createLinearGradient(0,0,0,H);
    sky.addColorStop(0,'#020d14');
    sky.addColorStop(1,'#041020');
    cx.fillStyle=sky; cx.fillRect(0,0,W,H);

    // Grid
    cx.strokeStyle='#0a1f2e'; cx.lineWidth=0.5;
    for(let x=0;x<W;x+=40){cx.beginPath();cx.moveTo(x,0);cx.lineTo(x,H);cx.stroke();}
    for(let y=0;y<H;y+=40){cx.beginPath();cx.moveTo(0,y);cx.lineTo(W,y);cx.stroke();}

    // Ground
    const gy=GROUND_Y();
    cx.fillStyle='#0a1f35';
    cx.fillRect(0,gy,W,H-gy);
    cx.strokeStyle='#1d4ed8'; cx.lineWidth=2;
    cx.beginPath(); cx.moveTo(0,gy); cx.lineTo(W,gy); cx.stroke();

    // Ground detail lines
    cx.strokeStyle='#0d2a4a'; cx.lineWidth=1;
    for(let x=0;x<W;x+=20){
        cx.beginPath();cx.moveTo(x,gy);cx.lineTo(x,H);cx.stroke();
    }

    // Explosions/waves
    explosions.forEach(e=>{
        cx.beginPath(); cx.arc(e.x,e.y,e.r,0,Math.PI*2);
        if(e.type==='wave'){
            cx.strokeStyle=e.color+Math.floor(e.alpha*200).toString(16).padStart(2,'0');
            cx.lineWidth=3; cx.stroke();
        } else {
            const grad=cx.createRadialGradient(e.x,e.y,0,e.x,e.y,e.r);
            grad.addColorStop(0,'#fbbf24'+Math.floor(e.alpha*180).toString(16).padStart(2,'0'));
            grad.addColorStop(0.4,'#ef4444'+Math.floor(e.alpha*140).toString(16).padStart(2,'0'));
            grad.addColorStop(1,'transparent');
            cx.fillStyle=grad; cx.fill();
        }
    });

    // Lightning
    lightnings.forEach(l=>{
        cx.beginPath();
        cx.moveTo(l.segments[0].x,l.segments[0].y);
        l.segments.slice(1).forEach(s=>cx.lineTo(s.x,s.y));
        cx.strokeStyle='#fbbf24'+Math.floor(l.alpha*255).toString(16).padStart(2,'0');
        cx.lineWidth=2+l.alpha*2; cx.stroke();
        // Glow
        cx.strokeStyle='#ffffff'+Math.floor(l.alpha*80).toString(16).padStart(2,'0');
        cx.lineWidth=1; cx.stroke();
    });

    // Objects
    objects.forEach(o=>{
        cx.save();
        cx.translate(o.x,o.y);
        cx.rotate(o.rotation);

        // Shadow
        cx.shadowColor='#000'; cx.shadowBlur=8; cx.shadowOffsetY=3;

        // Shield glow
        if(o.shielded){
            cx.shadowColor=o.color; cx.shadowBlur=20;
            cx.beginPath(); cx.arc(0,0,o.w/2+4,0,Math.PI*2);
            cx.strokeStyle=o.color+'60'; cx.lineWidth=3; cx.stroke();
        }

        // Body
        if(o.type==='wall'){
            cx.fillStyle='#1e293b';
            cx.fillRect(-o.w/2,-o.h/2,o.w,o.h);
            cx.strokeStyle='#475569'; cx.lineWidth=2;
            cx.strokeRect(-o.w/2,-o.h/2,o.w,o.h);
            // Brick pattern
            cx.strokeStyle='#334155'; cx.lineWidth=0.5;
            for(let bx=-o.w/2;bx<o.w/2;bx+=20){
                cx.beginPath();cx.moveTo(bx,-o.h/2);cx.lineTo(bx,o.h/2);cx.stroke();
            }
        } else {
            // Round body
            cx.beginPath(); cx.arc(0,0,o.w/2,0,Math.PI*2);
            cx.fillStyle='#071520'; cx.fill();
            cx.strokeStyle=o.color; cx.lineWidth=o.shielded?3:2; cx.stroke();
        }

        cx.shadowBlur=0; cx.shadowOffsetY=0;

        // Emoji
        cx.font=(o.type==='wall'?'22px':'18px')+' serif';
        cx.textAlign='center'; cx.textBaseline='middle';
        cx.fillText(o.emoji,0,0);

        // HP bar (if damaged)
        if(o.hp&&o.hp<o.maxHp&&o.hp>0){
            const bw=o.w;
            cx.fillStyle='#1e293b';
            cx.fillRect(-bw/2,o.h/2+4,bw,4);
            const pct=o.hp/o.maxHp;
            cx.fillStyle=pct>0.5?'#10b981':'#ef4444';
            cx.fillRect(-bw/2,o.h/2+4,bw*pct,4);
        }

        // Frozen indicator
        if(o.frozen){
            cx.font='14px serif'; cx.textAlign='center';
            cx.fillText('❄️',0,-o.h/2-10);
        }

        cx.restore();
    });

    // Particles
    particles.forEach(p=>{
        cx.beginPath(); cx.arc(p.x,p.y,p.r,0,Math.PI*2);
        cx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,'0');
        cx.fill();
    });

    // Place preview
    if(currentTool==='place' && mouseX>0){
        cx.globalAlpha=0.5;
        cx.font='24px serif'; cx.textAlign='center'; cx.textBaseline='middle';
        cx.fillText(selectedSpawnItem.emoji, mouseX, mouseY);
        cx.globalAlpha=1;
    }
}

// ── MOUSE ─────────────────────────────────────────────────────────────────────
let mouseX=0, mouseY=0;
const world = document.getElementById('world');

function getWorldPos(e){
    const r=cv.getBoundingClientRect();
    return {
        x:(e.clientX-r.left)*(W/r.width),
        y:(e.clientY-r.top)*(H/r.height)
    };
}

function getObjAt(x,y){
    return [...objects].reverse().find(o=>{
        const dx=Math.abs(o.x-x), dy=Math.abs(o.y-y);
        return dx<o.w/2+5 && dy<o.h/2+5;
    });
}

world.addEventListener('mousemove',e=>{
    const p=getWorldPos(e); mouseX=p.x; mouseY=p.y;
    if(dragObj && currentTool==='move'){
        dragObj.x=p.x-dragOffX; dragObj.y=p.y-dragOffY;
        dragObj.vx=0; dragObj.vy=0;
    }
});

world.addEventListener('mousedown',e=>{
    if(e.button===2) return;
    const p=getWorldPos(e);

    if(currentTool==='place'){
        spawnObject(p.x, p.y, selectedSpawnItem);
    } else if(currentTool==='move'){
        const o=getObjAt(p.x,p.y);
        if(o){ dragObj=o; dragOffX=p.x-o.x; dragOffY=p.y-o.y; o.frozen=true; }
    } else if(currentTool==='delete'){
        const o=getObjAt(p.x,p.y);
        if(o){ objects=objects.filter(ob=>ob!==o); updateHUD(); }
    }
    closeCtx();
});

world.addEventListener('mouseup',e=>{
    if(dragObj){ dragObj.frozen=false; dragObj.vy=-1; dragObj=null; }
});

// Right-click context menu
world.addEventListener('contextmenu',e=>{
    e.preventDefault();
    const p=getWorldPos(e);
    ctxObj=getObjAt(p.x,p.y);
    if(ctxObj){
        const menu=document.getElementById('ctx-menu');
        menu.style.display='block';
        menu.style.left=(e.clientX-world.getBoundingClientRect().left)+'px';
        menu.style.top=(e.clientY-world.getBoundingClientRect().top)+'px';
    }
});

document.addEventListener('click',()=>closeCtx());
function closeCtx(){ document.getElementById('ctx-menu').style.display='none'; }
function ctxDelete(){ if(ctxObj){objects=objects.filter(o=>o!==ctxObj);updateHUD();}closeCtx();}
function ctxFreeze(){ if(ctxObj){ctxObj.frozen=!ctxObj.frozen;}closeCtx();}
function ctxExplode(){ if(ctxObj){doExplosion(ctxObj.x,ctxObj.y,100);objects=objects.filter(o=>o!==ctxObj);updateHUD();}closeCtx();}
function ctxShield(){ if(ctxObj){ctxObj.shielded=true;ctxObj.color='#10b981';}closeCtx();}

// Drag from spawn panel
world.addEventListener('dragover',e=>e.preventDefault());
world.addEventListener('drop',e=>{
    e.preventDefault();
    const p=getWorldPos(e);
    spawnObject(p.x,p.y,selectedSpawnItem);
});

// ── TOOLS ─────────────────────────────────────────────────────────────────────
function setTool(t){
    currentTool=t;
    document.querySelectorAll('.tool').forEach(b=>b.classList.remove('active'));
    document.getElementById('t-'+t)?.classList.add('active');
    cv.style.cursor=t==='delete'?'crosshair':t==='move'?'grab':'crosshair';
}

function resetWorld(){
    objects=[]; particles=[]; explosions=[]; lightnings=[];
    totalExplosions=0; updateHUD();
    showToast('🔄 World cleared! Start building!');
}

function toggleGravity(){
    gravityOn=!gravityOn;
    document.getElementById('t-grav').textContent=gravityOn?'🌍 Gravity':'🌌 Zero-G';
    showToast(gravityOn?'🌍 Gravity ON — objects fall!':'🌌 Zero-G mode — objects float!');
}

function explodeAll(){
    const toExplode=[...objects];
    toExplode.forEach((o,i)=>{
        setTimeout(()=>{
            if(objects.includes(o)) doExplosion(o.x,o.y,o.blast||80);
        },i*100);
    });
    showToast('💥 CHAOS MODE! Everything explodes!');
}

// ── HUD ───────────────────────────────────────────────────────────────────────
function updateHUD(){
    document.getElementById('h-obj').textContent=objects.length;
    document.getElementById('h-exp').textContent=totalExplosions;
}

// ── TOAST ─────────────────────────────────────────────────────────────────────
let toastTimeout=null;
function showToast(msg){
    const el=document.getElementById('toast');
    el.textContent=msg; el.classList.add('show');
    if(toastTimeout) clearTimeout(toastTimeout);
    toastTimeout=setTimeout(()=>el.classList.remove('show'),3500);
}

let factIdx=0;
function showFactRandom(){
    if(Math.random()<0.4) showToast(FACTS[factIdx++%FACTS.length]);
}

// ── FPS ───────────────────────────────────────────────────────────────────────
function updateFPS(){
    frameCount++;
    const now=performance.now();
    if(now-fpsTime>=1000){
        fps=Math.round(frameCount*1000/(now-fpsTime));
        document.getElementById('h-fps').textContent=fps+' fps';
        frameCount=0; fpsTime=now;
    }
}

// ── GAME LOOP ─────────────────────────────────────────────────────────────────
function loop(){
    requestAnimationFrame(loop);
    physicsUpdate();
    draw();
    updateFPS();
}

// ── INIT ─────────────────────────────────────────────────────────────────────
showToast('🧪 Select an item from the panel and click or drag it onto the world!');
loop();
</script>
</body>
</html>
""", height=640)
