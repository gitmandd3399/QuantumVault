def render_quantum_sandbox():
    """Free game: Quantum Sandbox — Melon-style physics with ragdoll mobs."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("🧪 Quantum Sandbox")
    st.markdown(
        "**No rules. No score. Just quantum chaos!** "
        "Spawn mobs, drop bombs, build shields. "
        "Drag objects to throw them!"
    )

    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;overflow:hidden;}
#game{display:flex;width:100%;height:580px;position:relative;}

/* SPAWN PANEL */
#spawn-panel{width:115px;flex-shrink:0;background:#071520;
    border-right:2px solid #1a3a5a;display:flex;flex-direction:column;}
#panel-title{background:#0a1f35;padding:7px 6px;font-size:10px;color:#60a5fa;
    font-weight:bold;letter-spacing:1px;text-align:center;
    border-bottom:1px solid #1a3a5a;}
#panel-cats{display:flex;gap:2px;padding:4px;border-bottom:1px solid #1a3a5a;
    flex-wrap:wrap;justify-content:center;}
.cat-btn{padding:3px 6px;border-radius:4px;border:1px solid #1a3a5a;
    background:transparent;color:#475569;font-size:9px;cursor:pointer;transition:all 0.1s;}
.cat-btn:hover,.cat-btn.active{background:#1d4ed820;border-color:#3b82f6;color:#60a5fa;}
#spawn-items{flex:1;overflow-y:auto;padding:4px;scrollbar-width:thin;
    scrollbar-color:#1a3a5a transparent;}
.spawn-item{display:flex;flex-direction:column;align-items:center;padding:6px 4px;
    border-radius:8px;border:1px solid #1a3a5a;background:#071520;cursor:grab;
    margin-bottom:4px;transition:all 0.15s;color:#94a3b8;font-size:9px;text-align:center;}
.spawn-item:hover{background:#0a1f35;border-color:#3b82f6;color:white;transform:scale(1.05);}
.spawn-item .si-emoji{font-size:20px;margin-bottom:2px;}

/* WORLD */
#world{flex:1;position:relative;overflow:hidden;}
#cv{display:block;width:100%;height:100%;cursor:crosshair;}

/* HUD */
#hud{position:absolute;top:6px;left:6px;right:6px;display:flex;gap:4px;
    pointer-events:none;z-index:10;}
.hud-pill{background:#071520cc;border:1px solid #1a3a5a;border-radius:20px;
    padding:3px 10px;font-size:10px;color:#60a5fa;}

/* TOOLBAR */
#toolbar{position:absolute;bottom:6px;left:50%;transform:translateX(-50%);
    display:flex;gap:4px;z-index:10;background:#071520cc;
    border:1px solid #1a3a5a;border-radius:20px;padding:4px 8px;}
.tool{padding:5px 10px;border-radius:12px;border:1px solid #1a3a5a;
    background:transparent;color:#60a5fa;font-size:10px;cursor:pointer;transition:all 0.15s;}
.tool:hover{background:#1d4ed820;border-color:#3b82f6;}
.tool.active{background:#1d4ed8;border-color:#60a5fa;color:white;}

/* CTX MENU */
#ctx-menu{position:absolute;background:#071520;border:1px solid #1d4ed8;
    border-radius:8px;padding:4px;z-index:100;display:none;
    box-shadow:0 4px 20px rgba(0,0,0,0.5);min-width:120px;}
.ctx-item{padding:6px 12px;font-size:11px;color:#94a3b8;cursor:pointer;border-radius:4px;}
.ctx-item:hover{background:#0a1f35;color:white;}

/* TOAST */
#toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);
    background:#071520ee;border:1px solid #3b82f6;border-radius:8px;
    padding:7px 14px;font-size:10px;color:#93c5fd;z-index:50;
    opacity:0;transition:opacity 0.3s;max-width:320px;text-align:center;pointer-events:none;}
#toast.show{opacity:1;}
</style>
</head>
<body>
<div id="game">

<!-- SPAWN PANEL -->
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

<!-- WORLD -->
<div id="world">
    <canvas id="cv"></canvas>
    <div id="hud">
        <div class="hud-pill">🤖 <span id="h-obj">0</span></div>
        <div class="hud-pill">💥 <span id="h-exp">0</span></div>
        <div class="hud-pill" id="h-fps">60 fps</div>
    </div>
    <div id="toolbar">
        <button class="tool active" onclick="setTool('place')" id="t-place">✋ Place</button>
        <button class="tool" onclick="setTool('grab')" id="t-grab">🤏 Grab</button>
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

// ── SPAWN CATEGORIES ──────────────────────────────────────────────────────────
const CATEGORIES = {
    mobs:[
        {emoji:'🤖',name:'Quantum Bot',  type:'mob', color:'#3b82f6', mass:4, hp:5, face:'🤖'},
        {emoji:'👾',name:'Shor Agent',   type:'mob', color:'#ef4444', mass:3, hp:3, face:'👾'},
        {emoji:'🦾',name:'Cyber Guard',  type:'mob', color:'#10b981', mass:6, hp:8, face:'🦾'},
        {emoji:'👽',name:'Q-Alien',      type:'mob', color:'#8b5cf6', mass:2, hp:2, face:'👽'},
        {emoji:'🧑‍💻',name:'Hacker',   type:'mob', color:'#f59e0b', mass:3, hp:4, face:'🧑‍💻'},
        {emoji:'💀',name:'Shor Ghost',   type:'mob', color:'#6b7280', mass:1, hp:1, face:'💀'},
    ],
    weapons:[
        {emoji:'💣',name:'Shor Bomb',    type:'bomb',   mass:2, blast:80,  color:'#ef4444'},
        {emoji:'⚡',name:'Q-Zapper',     type:'zapper', mass:1, blast:40,  color:'#fbbf24'},
        {emoji:'🔥',name:'Laser',        type:'laser',  mass:1, blast:50,  color:'#f97316'},
        {emoji:'💥',name:'Mega Bomb',    type:'bomb',   mass:4, blast:160, color:'#dc2626'},
        {emoji:'🌊',name:'Grover Wave',  type:'wave',   mass:1, blast:30,  color:'#8b5cf6'},
        {emoji:'🎇',name:'Sparkle Mine', type:'mine',   mass:2, blast:60,  color:'#fbbf24'},
    ],
    props:[
        {emoji:'🏛️',name:'Server',      type:'prop', mass:8,  hp:200, color:'#334155'},
        {emoji:'💾',name:'Data Vault',   type:'prop', mass:6,  hp:150, color:'#1d4ed8'},
        {emoji:'📡',name:'Antenna',      type:'prop', mass:3,  hp:80,  color:'#475569'},
        {emoji:'🔐',name:'Kyber Shield', type:'shield',mass:5, hp:300, color:'#10b981'},
        {emoji:'🧱',name:'Wall Block',   type:'wall', mass:10, hp:400, color:'#64748b'},
        {emoji:'🚀',name:'Q-Drone',      type:'drone',mass:2,  hp:60,  color:'#06b6d4'},
        {emoji:'🏦',name:'Bank Node',    type:'prop', mass:7,  hp:180, color:'#ca8a04'},
        {emoji:'⚙️',name:'Mechanism',   type:'prop', mass:4,  hp:100, color:'#475569'},
    ],
    effects:[
        {emoji:'✨',name:'Sparkles',     type:'effect',  mass:0.1,color:'#fbbf24'},
        {emoji:'🌀',name:'Vortex',       type:'vortex',  mass:0.1,color:'#8b5cf6'},
        {emoji:'❄️',name:'Freeze Ray',   type:'freeze',  mass:0.1,color:'#60a5fa'},
        {emoji:'🌪️',name:'Tornado',     type:'tornado', mass:0.1,color:'#94a3b8'},
        {emoji:'☠️',name:'Shor Ray',     type:'ray',     mass:0.1,color:'#ef4444'},
        {emoji:'🛡️',name:'Force Field', type:'field',   mass:0.1,color:'#10b981'},
    ],
};

const FACTS = [
    '🔐 ML-KEM (Kyber FIPS 203) protects key exchange — quantum computers cannot break it!',
    '☠️ Shor Bots represent Shor\'s Algorithm — it breaks RSA by factoring prime numbers!',
    '⚡ Grover\'s Algorithm gives quantum a speedup but Kyber\'s lattice math resists it!',
    '💥 Chain reactions show how cascading vulnerabilities work in real networks!',
    '🦅 Falcon (FIPS 206) makes tiny signatures — perfect for small IoT devices!',
    '🌊 Harvest-Now-Decrypt-Later: enemies collect data TODAY to decrypt when QC arrives!',
    '🛡️ NIST mandated migration to PQC by 2035 — NSM-10 executive order!',
];

// ── RAGDOLL MOB STRUCTURE ─────────────────────────────────────────────────────
// A mob has: body, head, left arm, right arm, left leg, right leg
// Each part is a physics body connected by joints
function createMob(x, y, template) {
    const mob = {
        type: 'mob',
        face: template.face,
        color: template.color,
        mass: template.mass,
        hp: template.hp,
        maxHp: template.hp,
        frozen: false,
        shielded: false,
        id: Math.random(),
        ragdoll: true,
        // Body parts: each has x,y,vx,vy,r (radius)
        parts: {
            body: {x, y,       vx:0, vy:0, r:14, color:template.color},
            head: {x, y:-28,   vx:0, vy:0, r:10, color:template.color},
            larm: {x:x-14,y:-8,vx:0,vy:0, r:5,  color:template.color},
            rarm: {x:x+14,y:-8,vx:0,vy:0, r:5,  color:template.color},
            lleg: {x:x-8, y:16,vx:0,vy:0, r:5,  color:template.color},
            rleg: {x:x+8, y:16,vx:0,vy:0, r:5,  color:template.color},
        },
        // Joint rest lengths (distance between connected parts)
        joints:[
            {a:'head',b:'body', len:22},
            {a:'larm',b:'body', len:14},
            {a:'rarm',b:'body', len:14},
            {a:'lleg',b:'body', len:18},
            {a:'rleg',b:'body', len:18},
        ],
        collapsed: false,
        collapseTimer: 0,
    };
    // Initialize part positions relative to body
    mob.parts.head.x = x; mob.parts.head.y = y - 28;
    mob.parts.larm.x = x-16; mob.parts.larm.y = y - 6;
    mob.parts.rarm.x = x+16; mob.parts.rarm.y = y - 6;
    mob.parts.lleg.x = x-8;  mob.parts.lleg.y = y + 16;
    mob.parts.rleg.x = x+8;  mob.parts.rleg.y = y + 16;
    return mob;
}

// ── GAME STATE ────────────────────────────────────────────────────────────────
let objects = []; // all non-mob objects
let mobs = [];    // ragdoll mobs
let particles = [], explosions = [], waves = [], lightnings = [];
let currentTool = 'place';
let currentCat = 'mobs';
let selectedSpawnItem = CATEGORIES.mobs[0];
let dragObj = null, dragMob = null, dragPart = null;
let dragOffX = 0, dragOffY = 0;
let ctxTarget = null;
let gravityOn = true;
let totalExplosions = 0;
let mouseX = 0, mouseY = 0;
let frameCount = 0, fpsTime = performance.now(), fps = 60;

const GRAVITY = 0.4;
const GROUND_Y = () => H - 50;
const FRICTION = 0.82;

// ── PANEL ─────────────────────────────────────────────────────────────────────
function setCat(cat) {
    currentCat = cat;
    event.target.parentNode.querySelectorAll('.cat-btn').forEach(b=>b.classList.remove('active'));
    event.target.classList.add('active');
    buildPanel();
}

function buildPanel() {
    const items = CATEGORIES[currentCat];
    const container = document.getElementById('spawn-items');
    container.innerHTML = '';
    items.forEach(item => {
        const div = document.createElement('div');
        div.className = 'spawn-item';
        div.innerHTML = `<span class="si-emoji">${item.emoji}</span>${item.name}`;
        div.onclick = () => { selectedSpawnItem = item; showToast('Selected: '+item.name); };
        div.draggable = true;
        container.appendChild(div);
    });
}
buildPanel();

// ── SPAWN OBJECT ─────────────────────────────────────────────────────────────
function spawnAt(x, y, item) {
    if (item.type === 'mob') {
        const mob = createMob(x, y, item);
        mob.vx = (Math.random()-0.5)*0.5;
        mob.vy = -0.5;
        mobs.push(mob);
        showFactRandom();
    } else {
        const obj = {
            x, y, vx:(Math.random()-0.5)*2, vy:-1,
            w:item.type==='wall'?80:38, h:item.type==='wall'?38:38,
            emoji:item.emoji, name:item.name, type:item.type,
            mass:item.mass||3, hp:item.hp||100, maxHp:item.hp||100,
            color:item.color||'#3b82f6', frozen:false, shielded:item.type==='shield',
            blast:item.blast||0, rotation:0, rotVel:(Math.random()-0.5)*0.02,
            id:Math.random(), age:0,
        };
        objects.push(obj);
        if (['bomb','mine','zapper','laser','wave','ray','tornado','vortex','freeze','field'].includes(item.type)) {
            setTimeout(() => activateObject(obj), 800+Math.random()*600);
        }
        showFactRandom();
    }
    updateHUD();
}

// ── ACTIVATE OBJECT ───────────────────────────────────────────────────────────
function activateObject(obj) {
    if (!objects.includes(obj)) return;
    if (obj.type==='bomb'||obj.type==='mine') {
        doExplosion(obj.x,obj.y,obj.blast||80);
        objects=objects.filter(o=>o!==obj);
    } else if (obj.type==='zapper') {
        const targets=[...objects,...mobs].filter(o=>o!==obj)
            .sort((a,b)=>dist2(a,obj)-dist2(b,obj));
        if (targets[0]) {
            const t=targets[0];
            lightnings.push({x1:obj.x,y1:obj.y,x2:t.x,y2:t.y,alpha:1});
            if (!t.shielded) {
                if (t.hp!==undefined) t.hp-=40;
                if (t.parts) ragdollImpact(t, obj.x, obj.y, 5);
            }
        }
        objects=objects.filter(o=>o!==obj);
    } else if (obj.type==='wave'||obj.type==='tornado') {
        explosions.push({x:obj.x,y:obj.y,r:0,maxR:250,alpha:0.7,color:obj.color,type:'wave'});
        [...objects,...mobs].forEach(o=>{
            if(o!==obj){
                const dx=o.x-obj.x, dy=o.y-obj.y;
                const d=Math.sqrt(dx*dx+dy*dy)||1;
                if(d<250){
                    if(o.parts) ragdollImpact(o,obj.x,obj.y,8);
                    else { o.vx+=(dx/d)*6; o.vy-=3; }
                }
            }
        });
        objects=objects.filter(o=>o!==obj);
    } else if (obj.type==='freeze') {
        [...objects,...mobs].forEach(o=>o.frozen=true);
        setTimeout(()=>[...objects,...mobs].forEach(o=>o.frozen=false),3000);
        objects=objects.filter(o=>o!==obj);
    } else if (obj.type==='field') {
        [...objects,...mobs].forEach(o=>{
            if(o!==obj){
                const dx=o.x-obj.x, dy=o.y-obj.y;
                const d=Math.sqrt(dx*dx+dy*dy)||1;
                if(d<160){ o.vx+=dx/d*5; o.vy+=dy/d*5; }
                if(o.parts) ragdollImpact(o,obj.x,obj.y,5);
            }
        });
        objects=objects.filter(o=>o!==obj);
        explosions.push({x:obj.x,y:obj.y,r:0,maxR:160,alpha:0.6,color:'#10b981',type:'wave'});
    } else if (obj.type==='vortex') {
        [...objects,...mobs].forEach(o=>{
            if(o!==obj){
                const dx=obj.x-o.x, dy=obj.y-o.y, d=Math.sqrt(dx*dx+dy*dy)||1;
                o.vx+=dx/d*3; o.vy+=dy/d*3;
                if(o.parts) ragdollImpact(o,obj.x,obj.y,3);
            }
        });
        objects=objects.filter(o=>o!==obj);
    } else if (obj.type==='ray') {
        for(let i=0;i<8;i++){
            particles.push({x:obj.x,y:obj.y,vx:Math.cos(i*Math.PI/4)*6,
                vy:Math.sin(i*Math.PI/4)*6,r:5,alpha:1,color:obj.color});
        }
        objects=objects.filter(o=>o!==obj);
    }
    updateHUD();
}

// ── EXPLOSION ─────────────────────────────────────────────────────────────────
function doExplosion(x, y, radius) {
    totalExplosions++;
    explosions.push({x,y,r:0,maxR:radius,alpha:1,color:'#ef4444',type:'explosion'});
    for(let i=0;i<20;i++){
        const a=Math.random()*Math.PI*2, s=2+Math.random()*6;
        particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s-2,
            r:3+Math.random()*4,alpha:1,
            color:['#ef4444','#f97316','#fbbf24'][Math.floor(Math.random()*3)]});
    }
    // Affect objects
    objects.forEach(o=>{
        const dx=o.x-x, dy=o.y-y, d=Math.sqrt(dx*dx+dy*dy)||1;
        if(d<radius){
            const f=(1-d/radius)*12;
            if(!o.frozen){o.vx+=dx/d*f; o.vy+=dy/d*f-f*0.5;}
            if(!o.shielded) o.hp-=(1-d/radius)*60;
            if(o.type==='bomb'&&!o.activated&&d<radius*0.5){
                o.activated=true;
                setTimeout(()=>doExplosion(o.x,o.y,o.blast||80),200);
                objects=objects.filter(ob=>ob!==o);
            }
        }
    });
    // Affect mobs — ragdoll impact!
    mobs.forEach(mob=>{
        const dx=mob.x-x, dy=mob.y-y, d=Math.sqrt(dx*dx+dy*dy)||1;
        if(d<radius){
            const f=(1-d/radius)*14;
            ragdollImpact(mob, x, y, f);
            if(!mob.shielded) mob.hp-=(1-d/radius)*40;
        }
    });
    objects=objects.filter(o=>o.hp>0||o.type==='wall'||o.type==='shield'||o.shielded);
    mobs=mobs.filter(m=>m.hp>0);
    updateHUD();
}

// ── RAGDOLL PHYSICS ───────────────────────────────────────────────────────────
function ragdollImpact(mob, impX, impY, force) {
    // Apply force to each body part independently
    Object.values(mob.parts).forEach(part => {
        const dx = part.x - impX, dy = part.y - impY;
        const d = Math.sqrt(dx*dx+dy*dy)||1;
        const f = force * (1 - Math.min(d/200, 1));
        part.vx += (dx/d) * f * (0.3+Math.random()*0.3);
        part.vy += (dy/d) * f * (0.3+Math.random()*0.3) - f*0.2;
    });
    mob.collapsed = true;
    mob.collapseTimer = 60;
}

function updateMobs() {
    mobs.forEach(mob => {
        if (mob.frozen) return;
        mob.collapseTimer = Math.max(0, mob.collapseTimer-1);
        if (mob.collapseTimer === 0) mob.collapsed = false;

        const gy = GROUND_Y();
        const parts = mob.parts;

        // Update each part with physics
        Object.keys(parts).forEach(key => {
            const p = parts[key];
            if (gravityOn && !mob.frozen) p.vy += GRAVITY * (mob.mass/4);
            p.x += p.vx; p.y += p.vy;

            // Ground collision
            if (p.y + p.r > gy) {
                p.y = gy - p.r;
                p.vy *= -0.35;
                p.vx *= FRICTION;
                if(Math.abs(p.vy)<0.5) p.vy=0;
            }
            // Wall collisions
            if(p.x-p.r<0){p.x=p.r;p.vx*=-0.3;}
            if(p.x+p.r>W){p.x=W-p.r;p.vx*=-0.3;}
            if(p.y-p.r<0){p.y=p.r;p.vy*=-0.2;}
            // Air resistance damping
            p.vx*=0.97; p.vy*=0.97;
            // Cap velocity so mobs never fly off screen
            const maxV=8;
            if(Math.abs(p.vx)>maxV) p.vx=Math.sign(p.vx)*maxV;
            if(Math.abs(p.vy)>maxV) p.vy=Math.sign(p.vy)*maxV;
        });

        // Apply joint constraints (keep parts connected)
        if (!mob.collapsed) {
            mob.joints.forEach(j => {
                const a = parts[j.a], b = parts[j.b];
                const dx = a.x-b.x, dy = a.y-b.y;
                const d = Math.sqrt(dx*dx+dy*dy)||0.001;
                const diff = (d - j.len) / d * 0.4;
                const cx = dx*diff*0.5, cy = dy*diff*0.5;
                a.x -= cx; a.y -= cy;
                b.x += cx; b.y += cy;
                // Transfer some velocity
                const avgVx=(a.vx+b.vx)*0.1, avgVy=(a.vy+b.vy)*0.1;
                a.vx = a.vx*0.9+avgVx; a.vy = a.vy*0.9+avgVy;
                b.vx = b.vx*0.9+avgVx; b.vy = b.vy*0.9+avgVy;
            });
        } else {
            // Collapsed — looser joints for ragdoll feel
            mob.joints.forEach(j => {
                const a=parts[j.a], b=parts[j.b];
                const dx=a.x-b.x, dy=a.y-b.y;
                const d=Math.sqrt(dx*dx+dy*dy)||0.001;
                const maxLen = j.len*2.5;
                if(d>maxLen){
                    const diff=(d-maxLen)/d*0.3;
                    const cx=dx*diff*0.5, cy=dy*diff*0.5;
                    a.x-=cx; a.y-=cy;
                    b.x+=cx; b.y+=cy;
                }
            });
        }

        // Update mob center position from body part
        mob.x = parts.body.x;
        mob.y = parts.body.y;
    });
}

function updateObjects() {
    objects.forEach(o=>{
        if(o.frozen) return;
        o.age++;
        if(gravityOn&&o.type!=='drone') o.vy+=GRAVITY*(o.mass/3);
        if(o.type==='drone'){o.vy+=Math.sin(o.age*0.05)*0.2; o.vx*=0.99;}
        o.x+=o.vx; o.y+=o.vy; o.rotation+=o.rotVel;
        const gy=GROUND_Y()-o.h/2;
        if(o.y>gy){o.y=gy;o.vy*=-0.4;o.vx*=FRICTION;o.rotVel*=0.8;if(Math.abs(o.vy)<0.5)o.vy=0;}
        if(o.x<o.w/2){o.x=o.w/2;o.vx*=-0.6;}
        if(o.x>W-o.w/2){o.x=W-o.w/2;o.vx*=-0.6;}
        if(o.y<o.h/2){o.y=o.h/2;o.vy*=-0.5;}
    });
}

function dist2(a,b){return(a.x-b.x)**2+(a.y-b.y)**2;}

// ── DRAW ──────────────────────────────────────────────────────────────────────
function draw() {
    cx.clearRect(0,0,W,H);
    cx.fillStyle='#020d14'; cx.fillRect(0,0,W,H);
    // Grid
    cx.strokeStyle='#0a1f2e'; cx.lineWidth=0.5;
    for(let x=0;x<W;x+=40){cx.beginPath();cx.moveTo(x,0);cx.lineTo(x,H);cx.stroke();}
    for(let y=0;y<H;y+=40){cx.beginPath();cx.moveTo(0,y);cx.lineTo(W,y);cx.stroke();}
    // Ground
    const gy=GROUND_Y();
    cx.fillStyle='#0a1f35'; cx.fillRect(0,gy,W,H-gy);
    cx.strokeStyle='#1d4ed8'; cx.lineWidth=2;
    cx.beginPath();cx.moveTo(0,gy);cx.lineTo(W,gy);cx.stroke();

    // Explosions/waves
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

    // Lightning
    lightnings.forEach(l=>{
        cx.beginPath();cx.moveTo(l.x1,l.y1);cx.lineTo(l.x2,l.y2);
        cx.strokeStyle='#fbbf24'+Math.floor(l.alpha*255).toString(16).padStart(2,'0');
        cx.lineWidth=2+l.alpha*2;cx.stroke();
    });

    // Objects
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

    // MOBS — ragdoll drawing
    mobs.forEach(mob=>{
        const p=mob.parts;
        cx.save();

        // Draw limbs first (behind body)
        cx.strokeStyle=mob.color+'80';
        cx.lineWidth=6;
        cx.lineCap='round';

        // Left arm
        cx.beginPath();cx.moveTo(p.body.x,p.body.y-4);cx.lineTo(p.larm.x,p.larm.y);cx.stroke();
        // Right arm
        cx.beginPath();cx.moveTo(p.body.x,p.body.y-4);cx.lineTo(p.rarm.x,p.rarm.y);cx.stroke();
        // Left leg
        cx.beginPath();cx.moveTo(p.body.x,p.body.y+8);cx.lineTo(p.lleg.x,p.lleg.y);cx.stroke();
        // Right leg
        cx.beginPath();cx.moveTo(p.body.x,p.body.y+8);cx.lineTo(p.rleg.x,p.rleg.y);cx.stroke();
        // Neck
        cx.beginPath();cx.moveTo(p.body.x,p.body.y-12);cx.lineTo(p.head.x,p.head.y+6);cx.stroke();

        // Hand circles
        [p.larm,p.rarm,p.lleg,p.rleg].forEach(pt=>{
            cx.beginPath();cx.arc(pt.x,pt.y,pt.r,0,Math.PI*2);
            cx.fillStyle=mob.color+'60';cx.fill();
        });

        // Body circle
        cx.beginPath();cx.arc(p.body.x,p.body.y,p.body.r,0,Math.PI*2);
        cx.fillStyle='#071520';cx.fill();
        cx.strokeStyle=mob.shielded?'#10b981':mob.color;
        cx.lineWidth=mob.shielded?3:2;cx.stroke();

        // Head
        cx.beginPath();cx.arc(p.head.x,p.head.y,p.head.r,0,Math.PI*2);
        cx.fillStyle='#071520';cx.fill();
        cx.strokeStyle=mob.color;cx.lineWidth=2;cx.stroke();

        // Face emoji
        cx.font=(mob.collapsed?'12px':'14px')+' serif';
        cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(mob.collapsed?'😵':mob.face,p.head.x,p.head.y);

        // HP bar
        if(mob.hp<mob.maxHp){
            const bw=30;
            cx.fillStyle='#1e293b';cx.fillRect(p.head.x-bw/2,p.head.y-p.head.r-8,bw,4);
            cx.fillStyle=mob.hp/mob.maxHp>0.5?'#10b981':'#ef4444';
            cx.fillRect(p.head.x-bw/2,p.head.y-p.head.r-8,bw*(mob.hp/mob.maxHp),4);
        }

        // Frozen indicator
        if(mob.frozen){
            cx.font='12px serif';
            cx.fillText('❄️',p.head.x,p.head.y-p.head.r-16);
        }

        cx.restore();
    });

    // Particles
    particles.forEach(p=>{
        cx.beginPath();cx.arc(p.x,p.y,p.r,0,Math.PI*2);
        cx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,'0');
        cx.fill();
    });

    // Place preview
    if(currentTool==='place'&&mouseX>0){
        cx.globalAlpha=0.5;
        cx.font='22px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(selectedSpawnItem.emoji,mouseX,mouseY);
        cx.globalAlpha=1;
    }
}

// ── GAME LOOP ─────────────────────────────────────────────────────────────────
function update() {
    updateObjects();
    updateMobs();
    particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.vy+=0.1;p.alpha-=0.025;p.r*=0.96;});
    particles=particles.filter(p=>p.alpha>0);
    explosions.forEach(e=>{e.r+=e.type==='wave'?5:8;e.alpha-=0.04;});
    explosions=explosions.filter(e=>e.alpha>0);
    lightnings.forEach(l=>l.alpha-=0.08);
    lightnings=lightnings.filter(l=>l.alpha>0);
    frameCount++;
    const now=performance.now();
    if(now-fpsTime>=1000){
        fps=Math.round(frameCount*1000/(now-fpsTime));
        document.getElementById('h-fps').textContent=fps+' fps';
        frameCount=0;fpsTime=now;
    }
}

function loop(){requestAnimationFrame(loop);update();draw();}

// ── MOUSE INPUT ───────────────────────────────────────────────────────────────
const world=document.getElementById('world');
function getPos(e){
    const r=cv.getBoundingClientRect();
    return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)};
}

function getMobAt(x,y){
    return mobs.find(m=>{
        return Object.values(m.parts).some(p=>Math.hypot(p.x-x,p.y-y)<p.r+8);
    });
}
function getMobPartAt(mob,x,y){
    return Object.entries(mob.parts).find(([k,p])=>Math.hypot(p.x-x,p.y-y)<p.r+8)?.[0];
}
function getObjAt(x,y){
    return [...objects].reverse().find(o=>Math.abs(o.x-x)<o.w/2+5&&Math.abs(o.y-y)<o.h/2+5);
}

world.addEventListener('mousemove',e=>{
    const p=getPos(e);mouseX=p.x;mouseY=p.y;
    if(dragMob&&dragPart&&currentTool==='grab'){
        const part=dragMob.parts[dragPart];
        part.vx=(p.x-dragOffX-part.x)*0.3;
        part.vy=(p.y-dragOffY-part.y)*0.3;
        part.x=p.x-dragOffX;
        part.y=p.y-dragOffY;
    } else if(dragObj&&currentTool==='grab'){
        dragObj.vx=(p.x-dragOffX-dragObj.x)*0.3;
        dragObj.vy=(p.y-dragOffY-dragObj.y)*0.3;
        dragObj.x=p.x-dragOffX;
        dragObj.y=p.y-dragOffY;
    }
});

world.addEventListener('mousedown',e=>{
    if(e.button===2) return;
    const p=getPos(e);
    closeCtx();

    if(currentTool==='place'){
        spawnAt(p.x,p.y,selectedSpawnItem);
    } else if(currentTool==='grab'){
        // Try to grab a mob part first
        const mob=getMobAt(p.x,p.y);
        if(mob){
            dragMob=mob;
            dragPart=getMobPartAt(mob,p.x,p.y)||'body';
            const part=mob.parts[dragPart];
            dragOffX=p.x-part.x; dragOffY=p.y-part.y;
        } else {
            const obj=getObjAt(p.x,p.y);
            if(obj){dragObj=obj;dragOffX=p.x-obj.x;dragOffY=p.y-obj.y;}
        }
    } else if(currentTool==='delete'){
        const mob=getMobAt(p.x,p.y);
        if(mob) mobs=mobs.filter(m=>m!==mob);
        else {
            const obj=getObjAt(p.x,p.y);
            if(obj) objects=objects.filter(o=>o!==obj);
        }
        updateHUD();
    }
});

world.addEventListener('mouseup',e=>{
    if(dragMob){
        // Fling the dragged part
        if(dragPart){
            const part=dragMob.parts[dragPart];
            part.vx*=2; part.vy*=2;
        }
        dragMob=null; dragPart=null;
    }
    if(dragObj){ dragObj.frozen=false; dragObj.vy-=1; dragObj=null; }
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
        ctxTarget.shielded=true;ctxTarget.color='#10b981';
    } else if(action==='fling'){
        if(ctxTarget.parts){
            Object.values(ctxTarget.parts).forEach(p=>{p.vy=-8;p.vx=(Math.random()-0.5)*4;});
            ctxTarget.collapsed=true;ctxTarget.collapseTimer=40;
        } else { ctxTarget.vy=-15; }
    }
    closeCtx();
}

// Drag from panel
world.addEventListener('dragover',e=>e.preventDefault());
world.addEventListener('drop',e=>{e.preventDefault();const p=getPos(e);spawnAt(p.x,p.y,selectedSpawnItem);});

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
    all.forEach((o,i)=>setTimeout(()=>{
        doExplosion(o.x,o.y,o.blast||80);
    },i*100));
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
function showFactRandom(){
    if(Math.random()<0.4) showToast(FACTS[factIdx++%FACTS.length]);
}

// ── INIT ─────────────────────────────────────────────────────────────────────
showToast('🤖 Select a mob from the panel and click to spawn! Grab to throw!');
loop();
</script>
</body>
</html>
""", height=660)
