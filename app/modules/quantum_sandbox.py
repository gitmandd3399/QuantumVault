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

    components.html(r"""
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
// VERLET PHYSICS — points track current pos AND old pos (no explicit velocity)
// Velocity is implied: vel = pos - oldPos. This is naturally stable —
// energy can only be removed (via friction), never accidentally added.
// ══════════════════════════════════════════════════════════════════════════════
const GRAVITY = 0.5;
const AIR_FRICTION = 0.992;   // multiply implied velocity each frame (energy loss)
const GROUND_FRICTION = 0.85; // extra friction when touching ground
const GROUND_BOUNCE = 0.35;   // how much vertical velocity survives a bounce
const WALL_BOUNCE = 0.4;
const CONSTRAINT_ITERATIONS = 4; // more iterations = stiffer, more stable joints

function makePoint(x, y, r) {
    return { x, y, oldX:x, oldY:y, r, pinned:false };
}

function verletUpdate(p) {
    if (p.pinned) return;
    const vx = (p.x - p.oldX) * AIR_FRICTION;
    const vy = (p.y - p.oldY) * AIR_FRICTION;
    p.oldX = p.x; p.oldY = p.y;
    p.x += vx;
    p.y += vy + GRAVITY * (gravityOn ? 1 : 0);
}

function verletConstrainGround(p, groundY) {
    if (p.y + p.r > groundY) {
        const vx = (p.x - p.oldX);
        p.y = groundY - p.r;
        // Kill vertical velocity, dampen horizontal (friction)
        p.oldY = p.y + (p.y - p.oldY) * GROUND_BOUNCE * -1;
        p.oldX = p.x - vx * GROUND_FRICTION;
    }
    if (p.x - p.r < 0) { p.x = p.r; p.oldX = p.x + (p.x-p.oldX)*WALL_BOUNCE; }
    if (p.x + p.r > W) { p.x = W-p.r; p.oldX = p.x + (p.x-p.oldX)*WALL_BOUNCE; }
    if (p.y - p.r < 0) { p.y = p.r; p.oldY = p.y + (p.y-p.oldY)*WALL_BOUNCE; }
}

// Distance constraint — keeps two points a fixed distance apart (a "stick")
function satisfyStick(a, b, restLen, stiffness) {
    const dx = b.x - a.x, dy = b.y - a.y;
    const dist = Math.sqrt(dx*dx + dy*dy) || 0.0001;
    const diff = (dist - restLen) / dist;
    const offX = dx * 0.5 * diff * stiffness;
    const offY = dy * 0.5 * diff * stiffness;
    if (!a.pinned) { a.x += offX; a.y += offY; }
    if (!b.pinned) { b.x -= offX; b.y -= offY; }
}

// ── MOB STRUCTURE — stick figure with points + sticks ───────────────────────
function createMob(x, y, template) {
    const s = template.scale || 1;
    const mob = {
        type:'mob', face:template.face, color:template.color, hp:template.hp,
        maxHp:template.hp, frozen:false, shielded:false, id:Math.random(),
        scale:s,
        points: {
            head: makePoint(x, y-32*s, 11*s),
            neck: makePoint(x, y-18*s, 4*s),
            body: makePoint(x, y, 13*s),
            hip:  makePoint(x, y+16*s, 6*s),
            lhand:makePoint(x-24*s, y-6*s, 5*s),
            rhand:makePoint(x+24*s, y-6*s, 5*s),
            lfoot:makePoint(x-12*s, y+34*s, 6*s),
            rfoot:makePoint(x+12*s, y+34*s, 6*s),
        },
        sticks: [
            {a:'head',b:'neck', len:14*s},
            {a:'neck',b:'body', len:18*s},
            {a:'body',b:'hip',  len:16*s},
            {a:'neck',b:'lhand',len:26*s},
            {a:'neck',b:'rhand',len:26*s},
            {a:'hip', b:'lfoot',len:34*s},
            {a:'hip', b:'rfoot',len:34*s},
            // Extra stabilizing sticks so it doesn't fold weirdly
            {a:'head',b:'body', len:30*s},
            {a:'body',b:'lfoot',len:46*s},
            {a:'body',b:'rfoot',len:46*s},
        ],
    };
    return mob;
}

function updateMob(mob, groundY) {
    const pts = Object.values(mob.points);
    if (mob.frozen) return;

    // Step 1: integrate each point (gravity + inertia)
    pts.forEach(p => verletUpdate(p));

    // Step 2: satisfy stick constraints (several passes for stability)
    for (let iter = 0; iter < CONSTRAINT_ITERATIONS; iter++) {
        mob.sticks.forEach(s => {
            satisfyStick(mob.points[s.a], mob.points[s.b], s.len, 0.9);
        });
        // Step 3: ground/wall collision after each constraint pass
        pts.forEach(p => verletConstrainGround(p, groundY));
    }

    mob.x = mob.points.body.x;
    mob.y = mob.points.body.y;
}

function maybeDetachLimb(mob, force) {
    // What this does: if hit hard enough, permanently remove ONE outer-limb
    // stick constraint so that hand/foot floats free as debris with sparks.
    // Kid-friendly version of Melon's dismemberment - no gore, just sparks!
    if (force < 9 || mob.sticks.length <= 7) return; // keep core skeleton intact
    const detachable = ['lhand','rhand','lfoot','rfoot'];
    const stillAttached = mob.sticks.filter(s => detachable.includes(s.a) || detachable.includes(s.b));
    if (!stillAttached.length) return;
    if (Math.random() > 0.15) return; // don't detach every single hit
    const victim = stillAttached[Math.floor(Math.random()*stillAttached.length)];
    mob.sticks = mob.sticks.filter(s => s !== victim);
    const limbKey = detachable.includes(victim.a) ? victim.a : victim.b;
    const pt = mob.points[limbKey];
    if (pt) {
        for (let i=0;i<10;i++){
            const a=Math.random()*Math.PI*2, sp=2+Math.random()*4;
            particles.push({x:pt.x,y:pt.y,vx:Math.cos(a)*sp,vy:Math.sin(a)*sp-2,
                r:2+Math.random()*2,alpha:1,color:'#fbbf24'});
        }
        showToast('⚡ Limb detached! Quantum Bot still functional.');
    }
}

function applyImpulseToMob(mob, srcX, srcY, force) {
    maybeDetachLimb(mob, force);
    Object.values(mob.points).forEach(p => {
        const dx = p.x - srcX, dy = p.y - srcY;
        const d = Math.sqrt(dx*dx+dy*dy) || 1;
        const f = force * Math.max(0, 1 - d/220);
        // To apply an impulse in Verlet, we move oldX/oldY backward
        // (this creates implied velocity in the desired direction)
        p.oldX -= (dx/d) * f * (0.5 + Math.random()*0.4);
        p.oldY -= (dy/d) * f * (0.5 + Math.random()*0.4) + f*0.15;
    });
}

// ── REGULAR OBJECTS (non-mob) — still simple velocity physics, lighter weight ─
let objects = [];
let mobs = [];
let particles = [], explosions = [], lightnings = [];
let currentTool = 'place', currentCat = 'mobs';
let selectedSpawnItem = CATEGORIES.mobs[0];
let dragMob=null, dragPointKey=null, dragObj=null, dragOffX=0, dragOffY=0;
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
                if(t.points) applyImpulseToMob(t,obj.x,obj.y,4);
            }
        }
        objects=objects.filter(o=>o!==obj);
    } else if(obj.type==='wave'||obj.type==='tornado'){
        explosions.push({x:obj.x,y:obj.y,r:0,maxR:240,alpha:0.7,color:obj.color,type:'wave'});
        [...objects,...mobs].forEach(o=>{
            if(o!==obj){
                const dx=o.x-obj.x,dy=o.y-obj.y,d=Math.sqrt(dx*dx+dy*dy)||1;
                if(d<240){
                    if(o.points) applyImpulseToMob(o,obj.x,obj.y,5);
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
                    if(o.points) applyImpulseToMob(o,obj.x,obj.y,4);
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
                if(o.points) applyImpulseToMob(o,o.x+dx/d*40,o.y+dy/d*40,3);
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
            applyImpulseToMob(mob,x,y,f);
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

    // ── MOBS — stick figure rendering ──────────────────────────────────────────
    mobs.forEach(mob=>{
        const p=mob.points;
        cx.save();

        const limbs=[['neck','lhand'],['neck','rhand'],['hip','lfoot'],['hip','rfoot'],
                     ['head','neck'],['neck','body'],['body','hip']];
        limbs.forEach(([a,b])=>{
            if(!p[a]||!p[b]) return;
            const x1=p[a].x,y1=p[a].y,x2=p[b].x,y2=p[b].y;
            const ang=Math.atan2(y2-y1,x2-x1);
            const w=4.5*mob.scale; // capsule half-width
            cx.save();
            cx.beginPath();
            cx.moveTo(x1+Math.cos(ang+Math.PI/2)*w, y1+Math.sin(ang+Math.PI/2)*w);
            cx.lineTo(x2+Math.cos(ang+Math.PI/2)*w, y2+Math.sin(ang+Math.PI/2)*w);
            cx.arc(x2,y2,w,ang+Math.PI/2,ang-Math.PI/2);
            cx.lineTo(x1+Math.cos(ang-Math.PI/2)*w, y1+Math.sin(ang-Math.PI/2)*w);
            cx.arc(x1,y1,w,ang-Math.PI/2,ang+Math.PI/2);
            cx.closePath();
            cx.fillStyle=mob.color+'55';
            cx.fill();
            cx.strokeStyle=mob.color+'aa';
            cx.lineWidth=1;
            cx.stroke();
            cx.restore();
        });

        // Hands/feet
        [p.lhand,p.rhand,p.lfoot,p.rfoot].forEach(pt=>{
            cx.beginPath();cx.arc(pt.x,pt.y,pt.r,0,Math.PI*2);
            cx.fillStyle=mob.color+'70';cx.fill();
        });

        // Body
        cx.beginPath();cx.arc(p.body.x,p.body.y,p.body.r,0,Math.PI*2);
        cx.fillStyle='#071520';cx.fill();
        cx.strokeStyle=mob.shielded?'#10b981':mob.color;
        cx.lineWidth=mob.shielded?3:2;cx.stroke();

        // Head
        cx.beginPath();cx.arc(p.head.x,p.head.y,p.head.r,0,Math.PI*2);
        cx.fillStyle='#071520';cx.fill();
        cx.strokeStyle=mob.color;cx.lineWidth=2;cx.stroke();

        // Check if "down" — body close to ground = collapsed look
        const isDown = p.body.y > gy - 30;
        cx.font=(11*mob.scale)+'px serif';
        cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(isDown?'😵':mob.face, p.head.x, p.head.y);

        if(mob.hp<mob.maxHp){
            const bw=30*mob.scale;
            cx.fillStyle='#1e293b';cx.fillRect(p.head.x-bw/2,p.head.y-p.head.r-9,bw,4);
            cx.fillStyle=mob.hp/mob.maxHp>0.5?'#10b981':'#ef4444';
            cx.fillRect(p.head.x-bw/2,p.head.y-p.head.r-9,bw*Math.max(0,mob.hp/mob.maxHp),4);
        }
        if(mob.frozen){
            cx.font='12px serif';
            cx.fillText('❄️',p.head.x,p.head.y-p.head.r-18);
        }
        cx.restore();
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
    const gy=GROUND_Y();
    mobs.forEach(m=>updateMob(m,gy));
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
function getMobAt(x,y){
    return mobs.find(m=>Object.values(m.points).some(p=>Math.hypot(p.x-x,p.y-y)<p.r+8));
}
function getMobPointKeyAt(mob,x,y){
    return Object.entries(mob.points).find(([k,p])=>Math.hypot(p.x-x,p.y-y)<p.r+8)?.[0];
}
function getObjAt(x,y){
    return [...objects].reverse().find(o=>Math.abs(o.x-x)<o.w/2+5&&Math.abs(o.y-y)<o.h/2+5);
}

world.addEventListener('mousemove',e=>{
    const p=getPos(e); mouseX=p.x; mouseY=p.y;
    if(dragMob&&dragPointKey&&currentTool==='grab'){
        const pt=dragMob.points[dragPointKey];
        pt.x=p.x-dragOffX; pt.y=p.y-dragOffY;
        // oldX/oldY stay behind so releasing creates a throw motion
    } else if(dragObj&&currentTool==='grab'){
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
            dragPointKey=getMobPointKeyAt(mob,p.x,p.y)||'body';
            const pt=mob.points[dragPointKey];
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
    if(dragMob && dragPointKey){
        // Throw: give the point a velocity boost based on recent mouse movement
        const pt=dragMob.points[dragPointKey];
        const p=getPos(e);
        const dx=p.x-mouseX, dy=p.y-mouseY;
        pt.oldX = pt.x - (p.x - pt.oldX)*0.6;
        pt.oldY = pt.y - (p.y - pt.oldY)*0.6;
    }
    dragMob=null; dragPointKey=null;
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
        if(ctxTarget.points){
            applyImpulseToMob(ctxTarget, ctxTarget.x, ctxTarget.y+200, 14);
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
