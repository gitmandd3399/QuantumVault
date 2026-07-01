def render_quantum_sandbox():
    """Free game: Quantum Sandbox — Melon-style physics with stable Verlet ragdoll mobs."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("🧪 Quantum Sandbox")
    st.markdown(
        "**No rules. No score. Just quantum chaos!** "
        "Spawn mobs, drop bombs, build shields. "
        "Drag objects to throw them!"
    )

    st.iframe(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;overflow:hidden;}
#game{display:flex;width:100%;height:580px;position:relative;}

#spawn-panel{width:115px;flex-shrink:0;background:#071520;
    border-right:2px solid #1a3a5a;display:flex;flex-direction:column;}
#panel-title{background:#0a1f35;padding:7px 6px;font-size:10px;color:#60a5fa;
    font-weight:bold;letter-spacing:1px;text-align:center;border-bottom:1px solid #1a3a5a;}
#panel-cats{display:flex;gap:2px;padding:4px;border-bottom:1px solid #1a3a5a;
    flex-wrap:wrap;justify-content:center;}
.cat-btn{padding:3px 6px;border-radius:4px;border:1px solid #1a3a5a;
    background:transparent;color:#475569;font-size:9px;cursor:pointer;transition:all 0.1s;}
.cat-btn:hover,.cat-btn.active{background:#1d4ed820;border-color:#3b82f6;color:#60a5fa;}
#spawn-items{flex:1;overflow-y:auto;padding:4px;scrollbar-width:thin;
    scrollbar-color:#1a3a5a transparent;}
.spawn-item{display:flex;flex-direction:column;align-items:center;padding:6px 4px;
    border-radius:8px;border:1px solid #1a3a5a;background:#071520;cursor:pointer;
    margin-bottom:4px;transition:all 0.15s;color:#94a3b8;font-size:9px;text-align:center;}
.spawn-item:hover{background:#0a1f35;border-color:#3b82f6;color:white;transform:scale(1.05);}
.spawn-item.active{border-color:#fbbf24;background:#1a1500;}
.spawn-item .si-emoji{font-size:20px;margin-bottom:2px;}

#world{flex:1;position:relative;overflow:hidden;}
#cv{display:block;width:100%;height:100%;cursor:crosshair;}

#hud{position:absolute;top:6px;left:6px;right:6px;display:flex;gap:4px;
    pointer-events:none;z-index:10;}
.hud-pill{background:#071520cc;border:1px solid #1a3a5a;border-radius:20px;
    padding:3px 10px;font-size:10px;color:#60a5fa;}

#toolbar{position:absolute;bottom:6px;left:50%;transform:translateX(-50%);
    display:flex;gap:4px;z-index:10;background:#071520cc;
    border:1px solid #1a3a5a;border-radius:20px;padding:4px 8px;flex-wrap:wrap;
    justify-content:center;max-width:90%;}
.tool{padding:5px 10px;border-radius:12px;border:1px solid #1a3a5a;
    background:transparent;color:#60a5fa;font-size:10px;cursor:pointer;transition:all 0.15s;}
.tool:hover{background:#1d4ed820;border-color:#3b82f6;}
.tool.active{background:#1d4ed8;border-color:#60a5fa;color:white;}

#ctx-menu{position:absolute;background:#071520;border:1px solid #1d4ed8;
    border-radius:8px;padding:4px;z-index:100;display:none;
    box-shadow:0 4px 20px rgba(0,0,0,0.5);min-width:120px;}
.ctx-item{padding:6px 12px;font-size:11px;color:#94a3b8;cursor:pointer;border-radius:4px;}
.ctx-item:hover{background:#0a1f35;color:white;}

#toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);
    background:#071520ee;border:1px solid #3b82f6;border-radius:8px;
    padding:7px 14px;font-size:10px;color:#93c5fd;z-index:50;
    opacity:0;transition:opacity 0.3s;max-width:320px;text-align:center;pointer-events:none;}
#toast.show{opacity:1;}
</style>
</head>
<body>
<div id="game">

<div id="spawn-panel">
    <div id="panel-title">⬛ SPAWN</div>
    <div id="panel-cats">
        <button class="cat-btn active" onclick="setCat('mobs')">🤖</button>
        <button class="cat-btn" onclick="setCat('weapons')">💥</button>
        <button class="cat-btn" onclick="setCat('props')">🏗️</button>
        <button class="cat-btn" onclick="setCat('effects')">✨</button>
    </div>
    <div id="spawn-items"></div>
</div>

<div id="world">
    <canvas id="cv"></canvas>
    <div id="hud">
        <div class="hud-pill">🤖 <span id="h-obj">0</span></div>
        <div class="hud-pill">💥 <span id="h-exp">0</span></div>
        <div class="hud-pill" id="h-fps">60 fps</div>
    </div>
    <div id="toolbar">
        <button class="tool active" onclick="setTool('place')" id="t-place">✋ Place</button>
        <button class="tool" onclick="setTool('grab')" id="t-grab">🤏 Grab/Throw</button>
        <button class="tool" onclick="setTool('delete')" id="t-delete">🗑 Delete</button>
        <button class="tool" onclick="resetWorld()">🔄 Reset</button>
        <button class="tool" onclick="toggleGravity()" id="t-grav">🌍 Gravity</button>
        <button class="tool" onclick="explodeAll()">💥 CHAOS!</button>
    </div>
    <div id="ctx-menu">
        <div class="ctx-item" onclick="ctxAction('delete')">🗑️ Delete</div>
        <div class="ctx-item" onclick="ctxAction('freeze')">❄️ Freeze/Unfreeze</div>
        <div class="ctx-item" onclick="ctxAction('explode')">💥 Explode</div>
        <div class="ctx-item" onclick="ctxAction('shield')">🔐 Add Shield</div>
        <div class="ctx-item" onclick="ctxAction('fling')">🚀 Fling Up!</div>
        <div class="ctx-item" onclick="closeCtx()">✕ Close</div>
    </div>
</div>
</div>
<div id="toast"></div>

<script>
const cv = document.getElementById('cv');
const cx = cv.getContext('2d');
let W, H;
function resize(){
    const r = document.getElementById('world').getBoundingClientRect();
    W = cv.width = r.width; H = cv.height = r.height;
}
resize(); window.addEventListener('resize', resize);

// ── CATEGORIES ────────────────────────────────────────────────────────────────
const CATEGORIES = {
    mobs:[
        {emoji:'🤖',name:'Quantum Bot',  type:'mob', color:'#3b82f6', scale:1.0, hp:5, face:'🤖'},
        {emoji:'👾',name:'Shor Agent',   type:'mob', color:'#ef4444', scale:0.9, hp:3, face:'👾'},
        {emoji:'🦾',name:'Cyber Guard',  type:'mob', color:'#10b981', scale:1.2, hp:8, face:'🦾'},
        {emoji:'👽',name:'Q-Alien',      type:'mob', color:'#8b5cf6', scale:0.85,hp:2, face:'👽'},
        {emoji:'🧑‍💻',name:'Hacker',   type:'mob', color:'#f59e0b', scale:1.0, hp:4, face:'🧑‍💻'},
        {emoji:'💀',name:'Shor Ghost',   type:'mob', color:'#6b7280', scale:0.8, hp:1, face:'💀'},
    ],
    weapons:[
        {emoji:'💣',name:'Shor Bomb',    type:'bomb',   blast:80,  color:'#ef4444'},
        {emoji:'⚡',name:'Q-Zapper',     type:'zapper', blast:40,  color:'#fbbf24'},
        {emoji:'🔥',name:'Laser',        type:'laser',  blast:50,  color:'#f97316'},
        {emoji:'💥',name:'Mega Bomb',    type:'bomb',   blast:150, color:'#dc2626'},
        {emoji:'🌊',name:'Grover Wave',  type:'wave',   blast:30,  color:'#8b5cf6'},
        {emoji:'🎇',name:'Sparkle Mine', type:'mine',   blast:60,  color:'#fbbf24'},
    ],
    props:[
        {emoji:'🏛️',name:'Server',      type:'prop',  hp:200, color:'#334155'},
        {emoji:'💾',name:'Data Vault',   type:'prop',  hp:150, color:'#1d4ed8'},
        {emoji:'📡',name:'Antenna',      type:'prop',  hp:80,  color:'#475569'},
        {emoji:'🔐',name:'Kyber Shield', type:'shield',hp:300, color:'#10b981'},
        {emoji:'🧱',name:'Wall Block',   type:'wall',  hp:400, color:'#64748b'},
        {emoji:'🏦',name:'Bank Node',    type:'prop',  hp:180, color:'#ca8a04'},
    ],
    effects:[
        {emoji:'❄️',name:'Freeze Ray',   type:'freeze', color:'#60a5fa'},
        {emoji:'🌪️',name:'Tornado',     type:'tornado',color:'#94a3b8'},
        {emoji:'🛡️',name:'Force Field', type:'field',  color:'#10b981'},
        {emoji:'🌀',name:'Vortex',       type:'vortex', color:'#8b5cf6'},
    ],
};

const FACTS = [
    '🔐 ML-KEM (Kyber FIPS 203) protects key exchange — quantum computers cannot break it!',
    '☠️ Shor Bots represent Shor\'s Algorithm — it breaks RSA by factoring prime numbers!',
    '⚡ Grover\'s Algorithm gives quantum a speedup but Kyber\'s lattice math resists it!',
    '💥 Chain reactions show how cascading vulnerabilities work in real networks!',
    '🦅 Falcon (FIPS 206) makes tiny signatures — perfect for small IoT devices!',
    '🛡️ NIST mandated migration to PQC by 2035 — NSM-10 executive order!',
];

// ══════════════════════════════════════════════════════════════════════════════
// PEOPLE PLAYGROUND STYLE MOB SYSTEM
// Each mob is a skeleton of Verlet points connected by distance constraints.
// Two-segment limbs: upper arm + forearm, thigh + shin.
// Joints are visible circles. Grab any point and drag — body follows.
// Knockback sets all joint velocities. Collapse flag loosens all constraints.
// ══════════════════════════════════════════════════════════════════════════════

const GRAVITY_MOB = 0.45;
const AIR_DAMP = 0.993;     // very light air resistance
const GND_BOUNCE = 0.28;
const GND_FRIC   = 0.82;
const WALL_BOUNCE = 0.35;
const CONSTRAINT_ITERS = 6; // iterations per frame (higher = stiffer joints)

// ── Verlet point ──────────────────────────────────────────────────────────────
function mkPt(x, y) {
    return { x, y, ox: x, oy: y, pinned: false };
}

// ── Integrate one point ───────────────────────────────────────────────────────
function integratePt(p, grav) {
    if (p.pinned) return;
    const vx = (p.x - p.ox) * AIR_DAMP;
    const vy = (p.y - p.oy) * AIR_DAMP;
    p.ox = p.x; p.oy = p.y;
    p.x += vx;
    p.y += vy + grav;
}

// ── Collide one point with world ──────────────────────────────────────────────
function collidePt(p, r, groundY) {
    if (p.y + r > groundY) {
        const vx = p.x - p.ox;
        p.y = groundY - r;
        p.oy = p.y + (p.y - p.oy) * GND_BOUNCE * -1;
        p.ox = p.x - vx * GND_FRIC;
    }
    if (p.x - r < 0)  { p.x = r;   p.ox = p.x + (p.x - p.ox) * WALL_BOUNCE; }
    if (p.x + r > W)  { p.x = W-r; p.ox = p.x + (p.x - p.ox) * WALL_BOUNCE; }
    if (p.y - r < 0)  { p.y = r;   p.oy = p.y + (p.y - p.oy) * WALL_BOUNCE; }
}

// ── Distance constraint (keep two points a fixed length apart) ────────────────
function constrain(a, b, len, stiff) {
    const dx = b.x - a.x, dy = b.y - a.y;
    const d = Math.sqrt(dx*dx + dy*dy) || 0.0001;
    const diff = (d - len) / d * 0.5 * stiff;
    const offX = dx * diff, offY = dy * diff;
    if (!a.pinned) { a.x += offX; a.y += offY; }
    if (!b.pinned) { b.x -= offX; b.y -= offY; }
}

// ── Build a mob skeleton ──────────────────────────────────────────────────────
// Skeleton layout (all offsets from spawn centre):
//
//          [HEAD]
//            |
//          [NECK]
//         /      \
//     [LSHO]    [RSHO]   <- shoulders
//       |            |
//     [LELB]    [RELB]   <- elbows
//       |            |
//     [LHAN]    [RHAN]   <- hands
//
//          [HIP]
//         /      \
//     [LKNE]    [RKNE]   <- knees
//       |            |
//     [LFOT]    [RFOT]   <- feet
//
// Extra "cheat" sticks keep head above hips so standing is stable:
// NECK<->HIP   LSHO<->RSHO (shoulder brace)   LKNE<->RKNE (hip brace)

function createMob(cx_spawn, cy_spawn, template) {
    const s = (template.scale || 1) * (0.9 + Math.random() * 0.2); // slight height variance
    const c = template.color;

    // Joint positions (y increases downward)
    const head  = mkPt(cx_spawn,        cy_spawn - 36*s);
    const neck  = mkPt(cx_spawn,        cy_spawn - 24*s);
    const lsho  = mkPt(cx_spawn - 10*s, cy_spawn - 20*s);
    const rsho  = mkPt(cx_spawn + 10*s, cy_spawn - 20*s);
    const lelb  = mkPt(cx_spawn - 18*s, cy_spawn - 8*s);
    const relb  = mkPt(cx_spawn + 18*s, cy_spawn - 8*s);
    const lhan  = mkPt(cx_spawn - 18*s, cy_spawn + 4*s);
    const rhan  = mkPt(cx_spawn + 18*s, cy_spawn + 4*s);
    const hip   = mkPt(cx_spawn,        cy_spawn);
    const lkne  = mkPt(cx_spawn - 6*s,  cy_spawn + 14*s);
    const rkne  = mkPt(cx_spawn + 6*s,  cy_spawn + 14*s);
    const lfot  = mkPt(cx_spawn - 6*s,  cy_spawn + 28*s);
    const rfot  = mkPt(cx_spawn + 6*s,  cy_spawn + 28*s);

    const pts = { head, neck, lsho, rsho, lelb, relb, lhan, rhan,
                  hip, lkne, rkne, lfot, rfot };

    // Sticks: {a, b, len, stiff}
    const dist = (a,b) => Math.hypot(a.x-b.x, a.y-b.y);
    const sticks = [
        // Spine
        {a:'head', b:'neck', len:dist(head,neck), stiff:0.9},
        {a:'neck', b:'hip',  len:dist(neck,hip),  stiff:0.85},
        // Shoulders
        {a:'neck', b:'lsho', len:dist(neck,lsho), stiff:0.85},
        {a:'neck', b:'rsho', len:dist(neck,rsho), stiff:0.85},
        {a:'lsho', b:'rsho', len:dist(lsho,rsho), stiff:0.7},  // shoulder brace
        // Arms
        {a:'lsho', b:'lelb', len:dist(lsho,lelb), stiff:0.88},
        {a:'rsho', b:'relb', len:dist(rsho,relb), stiff:0.88},
        {a:'lelb', b:'lhan', len:dist(lelb,lhan), stiff:0.88},
        {a:'relb', b:'rhan', len:dist(relb,rhan), stiff:0.88},
        // Hips and legs
        {a:'hip',  b:'lkne', len:dist(hip, lkne), stiff:0.88},
        {a:'hip',  b:'rkne', len:dist(hip, rkne), stiff:0.88},
        {a:'lkne', b:'rkne', len:dist(lkne,rkne), stiff:0.6},  // hip brace
        {a:'lkne', b:'lfot', len:dist(lkne,lfot), stiff:0.88},
        {a:'rkne', b:'rfot', len:dist(rkne,rfot), stiff:0.88},
        // Cross braces to stop full collapse
        {a:'neck', b:'lkne', len:dist(neck,lkne), stiff:0.3},
        {a:'neck', b:'rkne', len:dist(neck,rkne), stiff:0.3},
    ];

    return {
        type: 'mob',
        pts, sticks, s, c,
        face: template.face,
        color: template.color,
        hp: template.hp, maxHp: template.hp,
        frozen: false, shielded: false,
        id: Math.random(),
        collapsed: false,
        // convenience centre for HUD / collision queries
        get x() { return (this.pts.neck.x + this.pts.hip.x) * 0.5; },
        get y() { return (this.pts.neck.y + this.pts.hip.y) * 0.5; },
    };
}

// ── Update one mob ────────────────────────────────────────────────────────────
function updateMobNew(mob, groundY) {
    if (mob.frozen) return;
    const grav = gravityOn ? GRAVITY_MOB : 0;
    const ptArr = Object.values(mob.pts);

    // 1. Integrate (apply gravity + inertia to every point)
    ptArr.forEach(p => integratePt(p, grav));

    // 2. Satisfy constraints + collide (several passes)
    const stiffScale = mob.collapsed ? 0.15 : 1.0;
    for (let iter = 0; iter < CONSTRAINT_ITERS; iter++) {
        mob.sticks.forEach(s => {
            constrain(mob.pts[s.a], mob.pts[s.b], s.len, s.stiff * stiffScale);
        });
        ptArr.forEach(p => collidePt(p, 3, groundY));
    }
}

// ── Apply impulse (knockback) ─────────────────────────────────────────────────
function knockMob(mob, srcX, srcY, force) {
    Object.values(mob.pts).forEach(p => {
        const dx = p.x - srcX, dy = p.y - srcY;
        const d = Math.sqrt(dx*dx + dy*dy) || 1;
        const f = force * Math.max(0, 1 - d / 240);
        // Move oldX/oldY backward to create Verlet velocity impulse
        p.ox -= (dx/d) * f * (0.4 + Math.random()*0.35);
        p.oy -= (dy/d) * f * (0.4 + Math.random()*0.35) + f * 0.12;
    });
    if (force > 7) { mob.collapsed = true; setTimeout(() => mob.collapsed = false, 1200); }
}

// ── Find mob/point at screen position ────────────────────────────────────────
function getMobAt(x, y) {
    return mobs.find(m => {
        return Object.values(m.pts).some(p => Math.hypot(p.x-x, p.y-y) < 10);
    });
}
function getMobPtKeyAt(mob, x, y) {
    return Object.entries(mob.pts)
        .find(([k,p]) => Math.hypot(p.x-x, p.y-y) < 14)?.[0] || null;
}


// ── REGULAR OBJECTS (non-mob) — still simple velocity physics, lighter weight ─
let objects = [];
let mobs = [];
let particles = [], explosions = [], lightnings = [];
let currentTool = 'place', currentCat = 'mobs';
let selectedSpawnItem = CATEGORIES.mobs[0];
let dragMob=null, dragObj=null, dragOffX=0, dragOffY=0;
let ctxTarget=null;
let gravityOn = true;
let totalExplosions = 0;
let mouseX=0, mouseY=0;
let frameCount=0, fpsTime=performance.now();

function setCat(cat){
    currentCat=cat;
    document.querySelectorAll('.cat-btn').forEach(b=>b.classList.remove('active'));
    event.target.classList.add('active');
    buildPanel();
}
function buildPanel(){
    const items=CATEGORIES[currentCat];
    const c=document.getElementById('spawn-items');
    c.innerHTML='';
    items.forEach((item,i)=>{
        const div=document.createElement('div');
        div.className='spawn-item'+(i===0&&currentCat===currentCat?'':'');
        div.innerHTML=`<span class="si-emoji">${item.emoji}</span>${item.name}`;
        div.onclick=()=>{
            selectedSpawnItem=item;
            document.querySelectorAll('.spawn-item').forEach(el=>el.classList.remove('active'));
            div.classList.add('active');
            showToast('Selected: '+item.name);
        };
        c.appendChild(div);
    });
    if (c.firstChild) c.firstChild.classList.add('active');
}
buildPanel();

function spawnAt(x,y,item){
    if (item.type==='mob'){
        const varied = Object.assign({}, item, {scale:(item.scale||1)*(0.85+Math.random()*0.3)});
        mobs.push(createMob(x,y,varied));
        showFactRandom();
    } else {
        const obj={
            x,y,vx:(Math.random()-0.5)*1,vy:-0.5,
            w:item.type==='wall'?80:38,h:item.type==='wall'?38:38,
            emoji:item.emoji,type:item.type,
            hp:item.hp||100,maxHp:item.hp||100,color:item.color||'#3b82f6',
            frozen:false,shielded:item.type==='shield',blast:item.blast||0,
            rotation:0,rotVel:(Math.random()-0.5)*0.02,age:0,
        };
        objects.push(obj);
        if(['bomb','mine','zapper','laser','wave','tornado','vortex','freeze','field'].includes(item.type)){
            setTimeout(()=>activateObject(obj),800+Math.random()*600);
        }
        showFactRandom();
    }
    updateHUD();
}

function activateObject(obj){
    if(!objects.includes(obj)) return;
    if(obj.type==='bomb'||obj.type==='mine'){
        doExplosion(obj.x,obj.y,obj.blast||80);
        objects=objects.filter(o=>o!==obj);
    } else if(obj.type==='zapper'){
        const targets=[...objects,...mobs].filter(o=>o!==obj)
            .sort((a,b)=>dist2(a,obj)-dist2(b,obj));
        if(targets[0]){
            const t=targets[0];
            lightnings.push({x1:obj.x,y1:obj.y,x2:t.x,y2:t.y,alpha:1});
            if(!t.shielded){
                if(t.hp!==undefined) t.hp-=40;
                if(t.face) knockMob(t,obj.x,obj.y,4);
            }
        }
        objects=objects.filter(o=>o!==obj);
    } else if(obj.type==='wave'||obj.type==='tornado'){
        explosions.push({x:obj.x,y:obj.y,r:0,maxR:240,alpha:0.7,color:obj.color,type:'wave'});
        [...objects,...mobs].forEach(o=>{
            if(o!==obj){
                const dx=o.x-obj.x,dy=o.y-obj.y,d=Math.sqrt(dx*dx+dy*dy)||1;
                if(d<240){
                    if(o.face) knockMob(o,obj.x,obj.y,5);
                    else { o.vx+=(dx/d)*3; o.vy-=2; }
                }
            }
        });
        objects=objects.filter(o=>o!==obj);
    } else if(obj.type==='freeze'){
        [...objects,...mobs].forEach(o=>o.frozen=true);
        setTimeout(()=>[...objects,...mobs].forEach(o=>o.frozen=false),3000);
        objects=objects.filter(o=>o!==obj);
    } else if(obj.type==='field'){
        [...objects,...mobs].forEach(o=>{
            if(o!==obj){
                const dx=o.x-obj.x,dy=o.y-obj.y,d=Math.sqrt(dx*dx+dy*dy)||1;
                if(d<160){
                    if(o.face) knockMob(o,obj.x,obj.y,4);
                    else { o.vx+=dx/d*3; o.vy+=dy/d*3; }
                }
            }
        });
        objects=objects.filter(o=>o!==obj);
        explosions.push({x:obj.x,y:obj.y,r:0,maxR:160,alpha:0.6,color:'#10b981',type:'wave'});
    } else if(obj.type==='vortex'){
        [...objects,...mobs].forEach(o=>{
            if(o!==obj){
                const dx=obj.x-o.x,dy=obj.y-o.y,d=Math.sqrt(dx*dx+dy*dy)||1;
                if(o.face) knockMob(o,o.x+dx/d*40,o.y+dy/d*40,3);
                else { o.vx+=dx/d*2; o.vy+=dy/d*2; }
            }
        });
        objects=objects.filter(o=>o!==obj);
    }
    updateHUD();
}

function doExplosion(x,y,radius){
    totalExplosions++;
    explosions.push({x,y,r:0,maxR:radius,alpha:1,color:'#ef4444',type:'explosion'});
    for(let i=0;i<18;i++){
        const a=Math.random()*Math.PI*2,s=2+Math.random()*5;
        particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s-2,
            r:3+Math.random()*3,alpha:1,
            color:['#ef4444','#f97316','#fbbf24'][Math.floor(Math.random()*3)]});
    }
    objects.forEach(o=>{
        const dx=o.x-x,dy=o.y-y,d=Math.sqrt(dx*dx+dy*dy)||1;
        if(d<radius){
            const f=(1-d/radius)*8;
            if(!o.frozen){o.vx+=dx/d*f;o.vy+=dy/d*f-f*0.4;}
            if(!o.shielded) o.hp-=(1-d/radius)*60;
            if(o.type==='bomb'&&!o.activated&&d<radius*0.5){
                o.activated=true;
                setTimeout(()=>doExplosion(o.x,o.y,o.blast||80),200);
                objects=objects.filter(ob=>ob!==o);
            }
        }
    });
    mobs.forEach(mob=>{
        const dx=mob.x-x,dy=mob.y-y,d=Math.sqrt(dx*dx+dy*dy)||1;
        if(d<radius){
            const f=(1-d/radius)*9;
            knockMob(mob,x,y,f);
            if(!mob.shielded) mob.hp-=(1-d/radius)*40;
        }
    });
    objects=objects.filter(o=>o.hp>0||o.type==='wall'||o.shielded);
    mobs=mobs.filter(m=>m.hp>0);
    updateHUD();
}

function updateObjects(){
    const FRICTION=0.85, GRAV=0.4;
    objects.forEach(o=>{
        if(o.frozen) return;
        o.age++;
        if(gravityOn) o.vy+=GRAV*0.7;
        o.x+=o.vx; o.y+=o.vy; o.rotation+=o.rotVel;
        o.vx*=0.995; o.vy*=0.995; // mild air drag so nothing accelerates forever
        const gy=GROUND_Y()-o.h/2;
        if(o.y>gy){o.y=gy;o.vy*=-0.35;o.vx*=FRICTION;o.rotVel*=0.8;if(Math.abs(o.vy)<0.4)o.vy=0;}
        if(o.x<o.w/2){o.x=o.w/2;o.vx*=-0.5;}
        if(o.x>W-o.w/2){o.x=W-o.w/2;o.vx*=-0.5;}
        if(o.y<o.h/2){o.y=o.h/2;o.vy*=-0.4;}
        // Cap velocity
        const maxV=12;
        if(Math.abs(o.vx)>maxV) o.vx=Math.sign(o.vx)*maxV;
        if(Math.abs(o.vy)>maxV) o.vy=Math.sign(o.vy)*maxV;
    });
}

function GROUND_Y(){ return H-50; }
function dist2(a,b){ return (a.x-b.x)**2+(a.y-b.y)**2; }

// ── DRAW ──────────────────────────────────────────────────────────────────────

// ── MOB DRAW HELPERS (must be outside forEach) ───────────────────────────────
function drawSeg(cx, pts, a, b, w, color) {
    const ax=pts[a].x, ay=pts[a].y, bx=pts[b].x, by=pts[b].y;
    cx.save();
    cx.strokeStyle=color; cx.lineWidth=w; cx.lineCap='round';
    cx.beginPath(); cx.moveTo(ax,ay); cx.lineTo(bx,by); cx.stroke();
    cx.restore();
}
function drawJoint(cx, pts, key, r, color) {
    cx.beginPath(); cx.arc(pts[key].x,pts[key].y,r,0,Math.PI*2);
    cx.fillStyle=color; cx.fill();
}

function draw(){
    cx.clearRect(0,0,W,H);
    cx.fillStyle='#020d14'; cx.fillRect(0,0,W,H);
    cx.strokeStyle='#0a1f2e'; cx.lineWidth=0.5;
    for(let x=0;x<W;x+=40){cx.beginPath();cx.moveTo(x,0);cx.lineTo(x,H);cx.stroke();}
    for(let y=0;y<H;y+=40){cx.beginPath();cx.moveTo(0,y);cx.lineTo(W,y);cx.stroke();}
    const gy=GROUND_Y();
    cx.fillStyle='#0a1f35'; cx.fillRect(0,gy,W,H-gy);
    cx.strokeStyle='#1d4ed8'; cx.lineWidth=2;
    cx.beginPath();cx.moveTo(0,gy);cx.lineTo(W,gy);cx.stroke();

    explosions.forEach(e=>{
        cx.beginPath();cx.arc(e.x,e.y,e.r,0,Math.PI*2);
        if(e.type==='wave'){
            cx.strokeStyle=e.color+Math.floor(e.alpha*200).toString(16).padStart(2,'0');
            cx.lineWidth=3;cx.stroke();
        } else {
            const g=cx.createRadialGradient(e.x,e.y,0,e.x,e.y,e.r);
            g.addColorStop(0,'#fbbf24'+Math.floor(e.alpha*180).toString(16).padStart(2,'0'));
            g.addColorStop(0.4,'#ef4444'+Math.floor(e.alpha*140).toString(16).padStart(2,'0'));
            g.addColorStop(1,'transparent');
            cx.fillStyle=g;cx.fill();
        }
    });
    lightnings.forEach(l=>{
        cx.beginPath();cx.moveTo(l.x1,l.y1);cx.lineTo(l.x2,l.y2);
        cx.strokeStyle='#fbbf24'+Math.floor(l.alpha*255).toString(16).padStart(2,'0');
        cx.lineWidth=2+l.alpha*2;cx.stroke();
    });

    objects.forEach(o=>{
        cx.save();cx.translate(o.x,o.y);cx.rotate(o.rotation);
        if(o.shielded){cx.shadowColor=o.color;cx.shadowBlur=15;}
        cx.beginPath();cx.arc(0,0,o.w/2,0,Math.PI*2);
        cx.fillStyle='#071520';cx.fill();
        cx.strokeStyle=o.color;cx.lineWidth=2;cx.stroke();
        cx.shadowBlur=0;
        cx.font='16px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(o.emoji,0,0);
        cx.restore();
    });

    // ── MOBS — People Playground skeleton draw ──────────────────────────────────
    mobs.forEach(mob=>{
        const p = mob.pts;
        const s = mob.s;
        const isKnocked = mob.collapsed;

        // Shield glow on torso
        if (mob.shielded) { cx.shadowColor='#10b981'; cx.shadowBlur=10; }

        // ── LIMB SEGMENTS (drawn back to front) ──────────────────────────────
        // Use module-level drawSeg/drawJoint helpers

        const lw  = 5*s;   // limb segment width
        const jw  = 3.5*s; // joint radius
        const col = mob.color;
        const dark = col+'99';

        // Legs (back layer)
        drawSeg(cx, p, 'hip',  'lkne', lw*1.1, dark);
        drawSeg(cx, p, 'hip',  'rkne', lw*1.1, dark);
        drawSeg(cx, p, 'lkne', 'lfot', lw,     dark);
        drawSeg(cx, p, 'rkne', 'rfot', lw,     dark);

        // Arms (back layer)
        drawSeg(cx, p, 'lsho', 'lelb', lw*0.9, dark);
        drawSeg(cx, p, 'rsho', 'relb', lw*0.9, dark);
        drawSeg(cx, p, 'lelb', 'lhan', lw*0.8, dark);
        drawSeg(cx, p, 'relb', 'rhan', lw*0.8, dark);

        // Torso spine
        drawSeg(cx, p, 'neck', 'hip',  lw*1.3, col+'cc');

        // Shoulder bar
        drawSeg(cx, p, 'lsho', 'rsho', lw*0.9, col+'bb');

        // Neck
        drawSeg(cx, p, 'head', 'neck', lw*0.9, col+'bb');

        // ── JOINTS (elbow, knee, shoulder circles) ────────────────────────────
        cx.shadowBlur = 0;
                [['lelb',jw],['relb',jw],['lkne',jw],['rkne',jw],
         ['lsho',jw*1.1],['rsho',jw*1.1],['hip',jw*1.3],
         ['neck',jw*1.1]].forEach(([k,r])=>drawJoint(cx,p,k,r,col));

        // Hands and feet as slightly larger circles
                [['lhan',jw*1.2],['rhan',jw*1.2],
         ['lfot',jw*1.3],['rfot',jw*1.3]].forEach(([k,r])=>drawJoint(cx,p,k,r,col));

        // ── HEAD (square pixel style) ─────────────────────────────────────────
        const hx = p.head.x, hy = p.head.y;
        const hw = 8*s, hh = 8*s;
        if (mob.shielded) { cx.shadowColor='#10b981'; cx.shadowBlur=12; }
        cx.fillStyle = col;
        cx.beginPath();
        cx.roundRect(hx-hw, hy-hh, hw*2, hh*2, 3*s);
        cx.fill();
        cx.strokeStyle = col+'ff'; cx.lineWidth=1*s; cx.stroke();
        cx.shadowBlur = 0;

        // Face
        if (isKnocked) {
            // X eyes when collapsed/knocked
            cx.strokeStyle='#1e293b'; cx.lineWidth=1.5*s;
            [[-0.5,-0.1],[-0.1,-0.5]].forEach(([dx1,dx2])=>{
                cx.beginPath();
                cx.moveTo(hx+hw*dx1, hy-hh*0.1);
                cx.lineTo(hx+hw*dx2, hy+hh*0.5);
                cx.stroke();
            });
            cx.beginPath();cx.moveTo(hx+hw*0.1,hy-hh*0.1);cx.lineTo(hx+hw*0.5,hy+hh*0.5);cx.stroke();
            cx.beginPath();cx.moveTo(hx+hw*0.5,hy-hh*0.1);cx.lineTo(hx+hw*0.1,hy+hh*0.5);cx.stroke();
        } else {
            // Dot eyes + pixel mouth
            cx.fillStyle='#1e293b';
            cx.fillRect(hx-hw*0.45, hy-hh*0.1, 2.5*s, 2.5*s);
            cx.fillRect(hx+hw*0.1,  hy-hh*0.1, 2.5*s, 2.5*s);
            cx.fillRect(hx-hw*0.25, hy+hh*0.5, hw*0.5, 1.5*s);
        }

        // HP bar above head
        if (mob.hp < mob.maxHp) {
            const bw=hw*2.5;
            cx.fillStyle='#1e293b'; cx.fillRect(hx-bw/2, hy-hh-9*s, bw, 4*s);
            cx.fillStyle=mob.hp/mob.maxHp>0.5?'#10b981':'#ef4444';
            cx.fillRect(hx-bw/2, hy-hh-9*s, bw*Math.max(0,mob.hp/mob.maxHp), 4*s);
        }
        if (mob.frozen) {
            cx.font='12px serif'; cx.textAlign='center'; cx.textBaseline='middle';
            cx.fillText('❄️', hx, hy-hh-18*s);
        }
    });
    });

    particles.forEach(p=>{
        cx.beginPath();cx.arc(p.x,p.y,p.r,0,Math.PI*2);
        cx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,'0');
        cx.fill();
    });
    if(currentTool==='place'&&mouseX>0){
        cx.globalAlpha=0.5;
        cx.font='22px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(selectedSpawnItem.emoji,mouseX,mouseY);
        cx.globalAlpha=1;
    }
}

function update(){
    updateObjects();
    const gY=GROUND_Y(); mobs.forEach(m=>updateMobNew(m,gY));
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.vy+=0.1;p.alpha-=0.025;p.r*=0.96;});
    particles=particles.filter(p=>p.alpha>0);
    explosions.forEach(e=>{e.r+=e.type==='wave'?5:8;e.alpha-=0.04;});
    explosions=explosions.filter(e=>e.alpha>0);
    lightnings.forEach(l=>l.alpha-=0.08);
    lightnings=lightnings.filter(l=>l.alpha>0);
    frameCount++;
    const now=performance.now();
    if(now-fpsTime>=1000){
        document.getElementById('h-fps').textContent=Math.round(frameCount*1000/(now-fpsTime))+' fps';
        frameCount=0;fpsTime=now;
    }
}
function loop(){requestAnimationFrame(loop);update();draw();}

// ── INPUT ─────────────────────────────────────────────────────────────────────
const world=document.getElementById('world');
function getPos(e){
    const r=cv.getBoundingClientRect();
    return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)};
}
function getObjAt(x,y){
    return [...objects].reverse().find(o=>Math.abs(o.x-x)<o.w/2+5&&Math.abs(o.y-y)<o.h/2+5);
}

// dragPtKey tracks WHICH skeleton point we grabbed
let dragPtKey = null;

world.addEventListener('mousemove',e=>{
    const p=getPos(e); mouseX=p.x; mouseY=p.y;
    if(dragMob && dragPtKey && currentTool==='grab'){
        // Move the grabbed point — leave ox/oy behind to create throw velocity
        const pt = dragMob.pts[dragPtKey];
        if(pt){ pt.x = p.x - dragOffX; pt.y = p.y - dragOffY; }
    } else if(dragObj && currentTool==='grab'){
        dragObj.x=p.x-dragOffX; dragObj.y=p.y-dragOffY;
        dragObj.vx=0; dragObj.vy=0;
    }
});

world.addEventListener('mousedown',e=>{
    if(e.button===2) return;
    const p=getPos(e);
    closeCtx();
    if(currentTool==='place'){
        spawnAt(p.x,p.y,selectedSpawnItem);
    } else if(currentTool==='grab'){
        const mob=getMobAt(p.x,p.y);
        if(mob){
            dragMob=mob;
            dragPtKey=getMobPtKeyAt(mob,p.x,p.y) || 'neck';
            const pt=mob.pts[dragPtKey];
            dragOffX=p.x-pt.x; dragOffY=p.y-pt.y;
        } else {
            const obj=getObjAt(p.x,p.y);
            if(obj){dragObj=obj;dragOffX=p.x-obj.x;dragOffY=p.y-obj.y;dragObj.frozen=true;}
        }
    } else if(currentTool==='delete'){
        const mob=getMobAt(p.x,p.y);
        if(mob) mobs=mobs.filter(m=>m!==mob);
        else { const obj=getObjAt(p.x,p.y); if(obj) objects=objects.filter(o=>o!==obj); }
        updateHUD();
    }
});

world.addEventListener('mouseup',e=>{
    if(dragMob && dragPtKey){
        // Throw: the velocity is already encoded in pt.x - pt.ox
        // Boost it slightly for satisfying throw feel
        const pt = dragMob.pts[dragPtKey];
        if(pt){
            const throwVx = (pt.x - pt.ox) * 1.5;
            const throwVy = (pt.y - pt.oy) * 1.5;
            pt.ox = pt.x - throwVx;
            pt.oy = pt.y - throwVy;
        }
        dragMob=null; dragPtKey=null;
    }
    if(dragObj){ dragObj.frozen=false; dragObj.vy-=2; dragObj=null; }
});
    if(dragObj){ dragObj.frozen=false; dragObj.vy-=2; dragObj=null; }
});

world.addEventListener('contextmenu',e=>{
    e.preventDefault();
    const p=getPos(e);
    ctxTarget=getMobAt(p.x,p.y)||getObjAt(p.x,p.y);
    if(ctxTarget){
        const menu=document.getElementById('ctx-menu');
        menu.style.display='block';
        menu.style.left=(e.clientX-world.getBoundingClientRect().left)+'px';
        menu.style.top=(e.clientY-world.getBoundingClientRect().top)+'px';
    }
});
document.addEventListener('click',closeCtx);
function closeCtx(){document.getElementById('ctx-menu').style.display='none';}

function ctxAction(action){
    if(!ctxTarget){closeCtx();return;}
    if(action==='delete'){
        mobs=mobs.filter(m=>m!==ctxTarget);
        objects=objects.filter(o=>o!==ctxTarget);
        updateHUD();
    } else if(action==='freeze'){
        ctxTarget.frozen=!ctxTarget.frozen;
    } else if(action==='explode'){
        doExplosion(ctxTarget.x,ctxTarget.y,100);
        mobs=mobs.filter(m=>m!==ctxTarget);
        objects=objects.filter(o=>o!==ctxTarget);
        updateHUD();
    } else if(action==='shield'){
        ctxTarget.shielded=true; ctxTarget.color='#10b981';
    } else if(action==='fling'){
        if(ctxTarget.face){
            knockMob(ctxTarget, ctxTarget.x, ctxTarget.y+200, 14);
        } else { ctxTarget.vy=-10; }
    }
    closeCtx();
}

world.addEventListener('dragover',e=>e.preventDefault());

// ── TOOLS ─────────────────────────────────────────────────────────────────────
function setTool(t){
    currentTool=t;
    document.querySelectorAll('.tool').forEach(b=>b.classList.remove('active'));
    document.getElementById('t-'+t)?.classList.add('active');
    cv.style.cursor=t==='delete'?'crosshair':t==='grab'?'grab':'crosshair';
}
function resetWorld(){
    objects=[];mobs=[];particles=[];explosions=[];lightnings=[];
    totalExplosions=0;updateHUD();
    showToast('🔄 World cleared!');
}
function toggleGravity(){
    gravityOn=!gravityOn;
    document.getElementById('t-grav').textContent=gravityOn?'🌍 Gravity':'🌌 Zero-G';
    showToast(gravityOn?'🌍 Gravity ON!':'🌌 Zero-G mode!');
}
function explodeAll(){
    const all=[...objects,...mobs];
    all.forEach((o,i)=>setTimeout(()=>{ if(objects.includes(o)||mobs.includes(o)) doExplosion(o.x,o.y,80);},i*100));
    showToast('💥 CHAOS MODE!');
}
function updateHUD(){
    document.getElementById('h-obj').textContent=objects.length+mobs.length;
    document.getElementById('h-exp').textContent=totalExplosions;
}
let toastTimer=null;
function showToast(m){
    const el=document.getElementById('toast');
    el.textContent=m;el.classList.add('show');
    if(toastTimer)clearTimeout(toastTimer);
    toastTimer=setTimeout(()=>el.classList.remove('show'),3000);
}
let factIdx=0;
function showFactRandom(){ if(Math.random()<0.4) showToast(FACTS[factIdx++%FACTS.length]); }

showToast('🤖 Select a mob and click to spawn! Use Grab/Throw to fling them around!');
loop();
</script>
</body>
</html>
""", height=660)
