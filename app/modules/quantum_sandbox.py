def render_quantum_sandbox():
    """Free game: Quantum Sandbox — Melon-style physics playground with PP-style mobs."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("🧪 Quantum Sandbox")
    st.markdown(
        "**No rules. No score. Just quantum chaos!** "
        "Select from the spawn panel and click the world to place objects. "
        "Use Grab to throw mobs around!"
    )

    components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;overflow:hidden;}
#game{display:flex;width:100%;height:560px;}
#panel{width:110px;flex-shrink:0;background:#071520;border-right:2px solid #1a3a5a;
    display:flex;flex-direction:column;}
#panel-title{background:#0a1f35;padding:6px;font-size:10px;color:#60a5fa;
    font-weight:bold;text-align:center;border-bottom:1px solid #1a3a5a;letter-spacing:1px;}
#cats{display:flex;gap:2px;padding:4px;border-bottom:1px solid #1a3a5a;flex-wrap:wrap;justify-content:center;}
.cat{padding:3px 5px;border-radius:4px;border:1px solid #1a3a5a;background:transparent;
    color:#475569;font-size:9px;cursor:pointer;}
.cat.active,.cat:hover{background:#1d4ed820;border-color:#3b82f6;color:#60a5fa;}
#items{flex:1;overflow-y:auto;padding:4px;scrollbar-width:thin;}
.item{display:flex;flex-direction:column;align-items:center;padding:5px 3px;
    border-radius:7px;border:1px solid #1a3a5a;background:#071520;cursor:pointer;
    margin-bottom:4px;font-size:9px;color:#94a3b8;text-align:center;transition:all 0.1s;}
.item:hover,.item.active{background:#0a1f35;border-color:#3b82f6;color:white;}
.item .ie{font-size:18px;margin-bottom:2px;}
#world{flex:1;position:relative;overflow:hidden;}
canvas{display:block;width:100%;height:100%;cursor:crosshair;}
#hud{position:absolute;top:5px;left:5px;right:5px;display:flex;gap:4px;pointer-events:none;}
.hp{background:#071520cc;border:1px solid #1a3a5a;border-radius:16px;
    padding:2px 8px;font-size:10px;color:#60a5fa;}
#bar{position:absolute;bottom:5px;left:50%;transform:translateX(-50%);
    display:flex;gap:3px;background:#071520cc;border:1px solid #1a3a5a;
    border-radius:16px;padding:3px 8px;}
.tb{padding:4px 9px;border-radius:10px;border:1px solid #1a3a5a;
    background:transparent;color:#60a5fa;font-size:10px;cursor:pointer;}
.tb.active{background:#1d4ed8;color:white;border-color:#60a5fa;}
.tb:hover{background:#1d4ed820;}
#toast{position:absolute;bottom:40px;left:50%;transform:translateX(-50%);
    background:#071520ee;border:1px solid #3b82f6;border-radius:7px;
    padding:5px 12px;font-size:10px;color:#93c5fd;opacity:0;
    transition:opacity 0.3s;pointer-events:none;text-align:center;white-space:nowrap;}
#toast.show{opacity:1;}
</style>
</head>
<body>
<div id="game">
<div id="panel">
    <div id="panel-title">SPAWN</div>
    <div id="cats">
        <button class="cat active" onclick="setCat('mobs',this)">🤖</button>
        <button class="cat" onclick="setCat('weapons',this)">💥</button>
        <button class="cat" onclick="setCat('props',this)">🏗️</button>
    </div>
    <div id="items"></div>
</div>
<div id="world">
    <canvas id="cv"></canvas>
    <div id="hud">
        <div class="hp">🤖 <span id="hobj">0</span></div>
        <div class="hp">💥 <span id="hexp">0</span></div>
        <div class="hp" id="hfps">60fps</div>
    </div>
    <div id="bar">
        <button class="tb active" onclick="setTool('place')" id="t-place">✋ Place</button>
        <button class="tb" onclick="setTool('grab')" id="t-grab">🤏 Grab</button>
        <button class="tb" onclick="setTool('del')" id="t-del">🗑 Delete</button>
        <button class="tb" onclick="resetWorld()">🔄 Reset</button>
        <button class="tb" onclick="toggleG()" id="t-grav">🌍 Gravity</button>
        <button class="tb" onclick="chaos()">💥 CHAOS!</button>
    </div>
    <div id="toast"></div>
</div>
</div>

<script>
var cv = document.getElementById('cv');
var cx = cv.getContext('2d');
var W, H;
function resize() {
    var r = document.getElementById('world').getBoundingClientRect();
    W = cv.width = r.width;
    H = cv.height = r.height;
}
resize();
window.addEventListener('resize', resize);

var CATS = {
    mobs: [
        {emoji:'🤖', name:'Quantum Bot',  type:'mob', color:'#3b82f6', hp:5},
        {emoji:'👾', name:'Shor Agent',   type:'mob', color:'#ef4444', hp:3},
        {emoji:'🦾', name:'Cyber Guard',  type:'mob', color:'#10b981', hp:8},
        {emoji:'👽', name:'Q-Alien',      type:'mob', color:'#8b5cf6', hp:2},
        {emoji:'🧑‍💻',name:'Hacker',     type:'mob', color:'#f59e0b', hp:4},
        {emoji:'💀', name:'Shor Ghost',   type:'mob', color:'#6b7280', hp:1},
    ],
    weapons: [
        {emoji:'💣', name:'Shor Bomb',   type:'bomb',  blast:80,  color:'#ef4444'},
        {emoji:'⚡', name:'Q-Zapper',    type:'zapper',blast:40,  color:'#fbbf24'},
        {emoji:'💥', name:'Mega Bomb',   type:'bomb',  blast:150, color:'#dc2626'},
        {emoji:'🌊', name:'Wave',        type:'wave',  blast:30,  color:'#8b5cf6'},
        {emoji:'🎇', name:'Mine',        type:'mine',  blast:60,  color:'#fbbf24'},
    ],
    props: [
        {emoji:'🏛️', name:'Server',     type:'prop', hp:200, color:'#334155'},
        {emoji:'💾', name:'Data Vault',  type:'prop', hp:150, color:'#1d4ed8'},
        {emoji:'🔐', name:'PQC Shield',  type:'shield',hp:300, color:'#10b981'},
        {emoji:'🧱', name:'Wall',        type:'wall', hp:400, color:'#64748b'},
        {emoji:'🏦', name:'Bank Node',   type:'prop', hp:180, color:'#ca8a04'},
    ],
};

var FACTS = [
    'ML-KEM (Kyber FIPS 203) protects key exchange — quantum computers cannot break it!',
    'Shor Bots represent Shor Algorithm — it breaks RSA by factoring primes!',
    'Falcon (FIPS 206) makes the smallest quantum-safe signatures for IoT devices!',
    'NIST mandated PQC migration by 2035 — NSM-10 executive order!',
    'SPHINCS+ uses SHA-3 hash trees — safe even if all lattice math breaks!',
];

// ── STATE ─────────────────────────────────────────────────────────────────────
var objects = [];
var mobs = [];
var particles = [];
var explosions = [];
var selectedItem = CATS.mobs[0];
var currentTool = 'place';
var currentCat = 'mobs';
var gravOn = true;
var totalExp = 0;
var dragObj = null, dragMob = null;
var dragOX = 0, dragOY = 0;
var ctxObj = null;
var mouseX = 0, mouseY = 0;
var fc = 0, ft = performance.now();

var GY = function() { return H - 50; };
var GRAV = 0.4;
var FRIC = 0.84;
var MAXV = 12;

// ── MOB — People Playground pixel humanoid ────────────────────────────────────
// Simple single rigid body + pixel skeleton drawn on top
// Stable and playable — no separate limb physics that can explode
function makeMob(x, y, tmpl) {
    var s = 0.9 + Math.random() * 0.25; // height variance like PP
    return {
        type: 'mob',
        x: x, y: y, vx: 0, vy: 0,
        w: 16*s, h: 38*s, // collision box
        s: s, color: tmpl.color, face: tmpl.emoji,
        hp: tmpl.hp, maxHp: tmpl.hp,
        frozen: false, shielded: false,
        walkPhase: Math.random() * 6.28,
        knockTimer: 0,
        rotation: 0,
        id: Math.random(),
    };
}

// ── SPAWN ─────────────────────────────────────────────────────────────────────
function spawnAt(x, y, item) {
    if (item.type === 'mob') {
        mobs.push(makeMob(x, y, item));
    } else {
        var obj = {
            x:x, y:y, vx:(Math.random()-0.5)*1.5, vy:-0.5,
            w: item.type==='wall'?80:34, h: item.type==='wall'?34:34,
            emoji:item.emoji, type:item.type,
            hp:item.hp||100, maxHp:item.hp||100,
            color:item.color||'#3b82f6',
            frozen:false, shielded:item.type==='shield',
            blast:item.blast||0,
            rotation:0, rotV:(Math.random()-0.5)*0.03,
            age:0, id:Math.random(),
        };
        objects.push(obj);
        if (['bomb','mine','zapper','wave'].includes(item.type)) {
            setTimeout(function() { activate(obj); }, 600 + Math.random()*800);
        }
    }
    showFactRandom();
    updateHUD();
}

// ── ACTIVATE ──────────────────────────────────────────────────────────────────
function activate(obj) {
    if (!objects.includes(obj)) return;
    if (obj.type==='bomb' || obj.type==='mine') {
        explode(obj.x, obj.y, obj.blast||80);
        objects = objects.filter(function(o){return o!==obj;});
    } else if (obj.type==='zapper') {
        var all = objects.concat(mobs).filter(function(o){return o!==obj;});
        all.sort(function(a,b){return dist2(a,obj)-dist2(b,obj);});
        if (all[0]) {
            explosions.push({x:obj.x,y:obj.y,x2:all[0].x,y2:all[0].y,type:'laser',alpha:1,color:'#fbbf24'});
            if (!all[0].shielded) {
                if (all[0].hp!==undefined) all[0].hp -= 40;
                knock(all[0], obj.x, obj.y, 4);
            }
        }
        objects = objects.filter(function(o){return o!==obj;});
    } else if (obj.type==='wave') {
        explosions.push({x:obj.x,y:obj.y,r:0,maxR:220,alpha:0.7,color:obj.color,type:'wave'});
        objects.concat(mobs).forEach(function(o) {
            if (o===obj) return;
            var dx=o.x-obj.x, dy=o.y-obj.y, d=Math.sqrt(dx*dx+dy*dy)||1;
            if (d<220) knock(o, obj.x, obj.y, 5);
        });
        objects = objects.filter(function(o){return o!==obj;});
    }
    updateHUD();
}

function knock(o, sx, sy, f) {
    var dx=o.x-sx, dy=o.y-sy, d=Math.sqrt(dx*dx+dy*dy)||1;
    var force = f * Math.max(0, 1-d/220);
    o.vx += dx/d*force;
    o.vy += dy/d*force - force*0.25;
    if (o.knockTimer !== undefined) o.knockTimer = 30;
}

function dist2(a,b){return (a.x-b.x)*(a.x-b.x)+(a.y-b.y)*(a.y-b.y);}

// ── EXPLOSION ─────────────────────────────────────────────────────────────────
function explode(x, y, radius) {
    totalExp++;
    explosions.push({x:x,y:y,r:0,maxR:radius,alpha:1,color:'#ef4444',type:'explosion'});
    for (var i=0;i<16;i++) {
        var a=Math.random()*6.28, sp=2+Math.random()*5;
        particles.push({x:x,y:y,vx:Math.cos(a)*sp,vy:Math.sin(a)*sp-2,
            r:2+Math.random()*3,alpha:1,
            color:['#ef4444','#f97316','#fbbf24'][Math.floor(Math.random()*3)]});
    }
    objects.concat(mobs).forEach(function(o) {
        var dx=o.x-x, dy=o.y-y, d=Math.sqrt(dx*dx+dy*dy)||1;
        if (d<radius) {
            var f=(1-d/radius)*10;
            knock(o, x, y, f);
            if (!o.shielded && o.hp!==undefined) o.hp -= (1-d/radius)*55;
            if (o.type==='bomb' && d<radius*0.5) {
                setTimeout(function(oo){return function(){
                    if(objects.includes(oo)){explode(oo.x,oo.y,oo.blast||80);objects=objects.filter(function(x){return x!==oo;});}
                };}(o), 180);
            }
        }
    });
    objects = objects.filter(function(o){return o.hp>0||o.type==='wall'||o.shielded;});
    mobs = mobs.filter(function(m){return m.hp>0;});
    updateHUD();
}

// ── PHYSICS ───────────────────────────────────────────────────────────────────
function updateObj(o) {
    if (o.frozen) return;
    o.age++;
    if (gravOn) o.vy += GRAV * 0.65;
    o.x += o.vx; o.y += o.vy;
    o.rotation += o.rotV;
    o.vx *= 0.995; o.vy *= 0.995;
    var gy = GY() - o.h/2;
    if (o.y > gy) { o.y=gy; o.vy*=-0.32; o.vx*=FRIC; o.rotV*=0.8; if(Math.abs(o.vy)<0.4)o.vy=0; }
    if (o.x < o.w/2) { o.x=o.w/2; o.vx*=-0.5; }
    if (o.x > W-o.w/2) { o.x=W-o.w/2; o.vx*=-0.5; }
    if (o.y < o.h/2) { o.y=o.h/2; o.vy*=-0.4; }
    if (Math.abs(o.vx)>MAXV) o.vx=Math.sign(o.vx)*MAXV;
    if (Math.abs(o.vy)>MAXV) o.vy=Math.sign(o.vy)*MAXV;
}

function updateMob(m) {
    if (m.frozen) return;
    if (gravOn) m.vy += GRAV * 0.7;
    m.x += m.vx; m.y += m.vy;
    m.vx *= 0.992; m.vy *= 0.992;
    var gy = GY() - m.h/2;
    if (m.y > gy) { m.y=gy; m.vy*=-0.28; m.vx*=FRIC; if(Math.abs(m.vy)<0.5)m.vy=0; }
    if (m.x < m.w/2) { m.x=m.w/2; m.vx*=-0.5; }
    if (m.x > W-m.w/2) { m.x=W-m.w/2; m.vx*=-0.5; }
    if (m.y < m.h/2) { m.y=m.h/2; m.vy*=-0.3; }
    if (Math.abs(m.vx)>MAXV) m.vx=Math.sign(m.vx)*MAXV;
    if (Math.abs(m.vy)>MAXV) m.vy=Math.sign(m.vy)*MAXV;
    if (m.knockTimer>0) m.knockTimer--;
    // Walk cycle
    var spd = Math.abs(m.vx);
    if (spd > 0.3 && m.y >= GY()-m.h/2-2) m.walkPhase += 0.18;
    // Lean in direction of motion
    m.rotation = Math.max(-0.3, Math.min(0.3, m.vx * 0.05));
}

// ── DRAW MOB — People Playground pixel humanoid ───────────────────────────────
function drawMob(m) {
    var s = m.s;
    var x = m.x, y = m.y;
    var swing = Math.sin(m.walkPhase) * 0.45;
    var knocked = m.knockTimer > 5;
    var col = m.color;
    var dark = col;

    cx.save();
    cx.translate(x, y);
    cx.rotate(m.rotation);

    if (m.shielded) { cx.shadowColor='#10b981'; cx.shadowBlur=10; }

    // ── LEGS ──────────────────────────────────────────────────────────────────
    var thighL = 10*s, shinL = 10*s, limbW = 4*s;
    // Left leg: thigh + knee + shin
    cx.save();
    cx.translate(-5*s, 6*s);
    cx.rotate(knocked ? 0.8 : swing*0.8);
    cx.fillStyle = col+'bb';
    cx.fillRect(-limbW/2, 0, limbW, thighL);
    // Knee joint
    cx.beginPath(); cx.arc(0, thighL, limbW*0.8, 0, 6.28); cx.fillStyle=col; cx.fill();
    // Shin
    cx.save(); cx.translate(0, thighL);
    cx.rotate(knocked ? 0.5 : Math.max(0, swing)*0.5);
    cx.fillStyle = col+'99';
    cx.fillRect(-limbW/2, 0, limbW, shinL);
    // Foot
    cx.fillStyle = col;
    cx.fillRect(-limbW, shinL-2*s, limbW*2.5, 3*s);
    cx.restore();
    cx.restore();

    // Right leg
    cx.save();
    cx.translate(5*s, 6*s);
    cx.rotate(knocked ? -0.8 : -swing*0.8);
    cx.fillStyle = col+'bb';
    cx.fillRect(-limbW/2, 0, limbW, thighL);
    cx.beginPath(); cx.arc(0, thighL, limbW*0.8, 0, 6.28); cx.fillStyle=col; cx.fill();
    cx.save(); cx.translate(0, thighL);
    cx.rotate(knocked ? -0.5 : Math.max(0,-swing)*0.5);
    cx.fillStyle = col+'99';
    cx.fillRect(-limbW/2, 0, limbW, shinL);
    cx.fillStyle = col;
    cx.fillRect(-limbW, shinL-2*s, limbW*2.5, 3*s);
    cx.restore();
    cx.restore();

    // ── TORSO ─────────────────────────────────────────────────────────────────
    var tw = 7*s, th = 14*s;
    cx.fillStyle = col+'dd';
    cx.beginPath();
    if (cx.roundRect) cx.roundRect(-tw, -th, tw*2, th*2, 2*s);
    else cx.rect(-tw, -th, tw*2, th*2);
    cx.fill();
    cx.strokeStyle = col; cx.lineWidth = 1*s; cx.stroke();
    cx.shadowBlur = 0;

    // ── ARMS ──────────────────────────────────────────────────────────────────
    var uArmL = 8*s, lArmL = 7*s, armW = 3.5*s;
    // Left arm: upper + elbow + forearm
    cx.save();
    cx.translate(-tw, -th*0.5);
    cx.rotate(knocked ? 1.2 : -swing*0.6 - 0.1);
    cx.fillStyle = col+'cc';
    cx.fillRect(-armW/2, 0, armW, uArmL);
    cx.beginPath(); cx.arc(0, uArmL, armW*0.9, 0, 6.28); cx.fillStyle=col; cx.fill();
    cx.save(); cx.translate(0, uArmL);
    cx.rotate(knocked ? 0.8 : Math.max(0,-swing)*0.4);
    cx.fillStyle = col+'99';
    cx.fillRect(-armW/2, 0, armW, lArmL);
    cx.beginPath(); cx.arc(0, lArmL, armW*1.1, 0, 6.28); cx.fillStyle=col; cx.fill();
    cx.restore(); cx.restore();

    // Right arm
    cx.save();
    cx.translate(tw, -th*0.5);
    cx.rotate(knocked ? -1.2 : swing*0.6 + 0.1);
    cx.fillStyle = col+'cc';
    cx.fillRect(-armW/2, 0, armW, uArmL);
    cx.beginPath(); cx.arc(0, uArmL, armW*0.9, 0, 6.28); cx.fillStyle=col; cx.fill();
    cx.save(); cx.translate(0, uArmL);
    cx.rotate(knocked ? -0.8 : Math.max(0,swing)*0.4);
    cx.fillStyle = col+'99';
    cx.fillRect(-armW/2, 0, armW, lArmL);
    cx.beginPath(); cx.arc(0, lArmL, armW*1.1, 0, 6.28); cx.fillStyle=col; cx.fill();
    cx.restore(); cx.restore();

    // ── NECK ──────────────────────────────────────────────────────────────────
    cx.fillStyle = col+'88';
    cx.fillRect(-2.5*s, -th-3*s, 5*s, 4*s);

    // ── HEAD (square pixel style) ─────────────────────────────────────────────
    var hw = 8*s, hh = 8*s;
    var hTop = -th - hh*2 - 2*s;
    cx.fillStyle = col;
    cx.beginPath();
    if (cx.roundRect) cx.roundRect(-hw, hTop, hw*2, hh*2, 3*s);
    else cx.rect(-hw, hTop, hw*2, hh*2);
    cx.fill();
    cx.strokeStyle = col; cx.lineWidth = 1*s; cx.stroke();

    // Face
    cx.fillStyle = '#0a1628';
    if (knocked) {
        // X eyes
        cx.strokeStyle = '#0a1628'; cx.lineWidth = 1.5*s;
        cx.beginPath();cx.moveTo(-hw*0.45,hTop+hh*0.5);cx.lineTo(-hw*0.1,hTop+hh*0.9);cx.stroke();
        cx.beginPath();cx.moveTo(-hw*0.1,hTop+hh*0.5);cx.lineTo(-hw*0.45,hTop+hh*0.9);cx.stroke();
        cx.beginPath();cx.moveTo(hw*0.1,hTop+hh*0.5);cx.lineTo(hw*0.45,hTop+hh*0.9);cx.stroke();
        cx.beginPath();cx.moveTo(hw*0.45,hTop+hh*0.5);cx.lineTo(hw*0.1,hTop+hh*0.9);cx.stroke();
    } else {
        cx.fillRect(-hw*0.45, hTop+hh*0.4, 2.5*s, 2.5*s);
        cx.fillRect(hw*0.1,   hTop+hh*0.4, 2.5*s, 2.5*s);
        cx.fillRect(-hw*0.25, hTop+hh*1.1, hw*0.5, 1.5*s);
    }

    // HP bar
    if (m.hp < m.maxHp) {
        var bw = hw*2.5;
        cx.fillStyle='#1e293b'; cx.fillRect(-bw/2, hTop-8*s, bw, 4*s);
        cx.fillStyle=m.hp/m.maxHp>0.5?'#10b981':'#ef4444';
        cx.fillRect(-bw/2, hTop-8*s, bw*Math.max(0,m.hp/m.maxHp), 4*s);
    }
    if (m.frozen) {
        cx.font='11px serif'; cx.textAlign='center'; cx.textBaseline='middle';
        cx.fillText('❄️', 0, hTop-14*s);
    }
    cx.restore();
}

// ── DRAW ──────────────────────────────────────────────────────────────────────
function draw() {
    cx.clearRect(0,0,W,H);
    cx.fillStyle='#020d14'; cx.fillRect(0,0,W,H);
    // Grid
    cx.strokeStyle='#0a1f2e'; cx.lineWidth=0.5;
    for(var gx=0;gx<W;gx+=40){cx.beginPath();cx.moveTo(gx,0);cx.lineTo(gx,H);cx.stroke();}
    for(var gy2=0;gy2<H;gy2+=40){cx.beginPath();cx.moveTo(0,gy2);cx.lineTo(W,gy2);cx.stroke();}
    // Ground
    var gy=GY();
    cx.fillStyle='#0a1f35'; cx.fillRect(0,gy,W,H-gy);
    cx.strokeStyle='#1d4ed8'; cx.lineWidth=2;
    cx.beginPath();cx.moveTo(0,gy);cx.lineTo(W,gy);cx.stroke();
    // Explosions
    explosions.forEach(function(e) {
        if (e.type==='laser') {
            cx.beginPath();cx.moveTo(e.x,e.y);cx.lineTo(e.x2,e.y2);
            cx.strokeStyle='#fbbf24'+Math.floor(e.alpha*255).toString(16).padStart(2,'0');
            cx.lineWidth=3;cx.stroke();
        } else if (e.type==='wave') {
            cx.beginPath();cx.arc(e.x,e.y,e.r,0,6.28);
            cx.strokeStyle=e.color+Math.floor(e.alpha*200).toString(16).padStart(2,'0');
            cx.lineWidth=3;cx.stroke();
        } else {
            var g=cx.createRadialGradient(e.x,e.y,0,e.x,e.y,e.r);
            g.addColorStop(0,'#fbbf24'+Math.floor(e.alpha*180).toString(16).padStart(2,'0'));
            g.addColorStop(0.5,'#ef4444'+Math.floor(e.alpha*120).toString(16).padStart(2,'0'));
            g.addColorStop(1,'transparent');
            cx.beginPath();cx.arc(e.x,e.y,e.r,0,6.28);
            cx.fillStyle=g;cx.fill();
        }
    });
    // Objects
    objects.forEach(function(o) {
        cx.save();cx.translate(o.x,o.y);cx.rotate(o.rotation);
        if(o.shielded){cx.shadowColor=o.color;cx.shadowBlur=12;}
        cx.beginPath();cx.arc(0,0,o.w/2,0,6.28);
        cx.fillStyle='#071520';cx.fill();
        cx.strokeStyle=o.color;cx.lineWidth=2;cx.stroke();
        cx.shadowBlur=0;
        cx.font='15px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(o.emoji,0,0);
        cx.restore();
    });
    // Mobs
    mobs.forEach(drawMob);
    // Particles
    particles.forEach(function(p) {
        cx.beginPath();cx.arc(p.x,p.y,p.r,0,6.28);
        cx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,'0');
        cx.fill();
    });
    // Place preview
    if (currentTool==='place' && mouseX>0) {
        cx.globalAlpha=0.45;
        cx.font='20px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(selectedItem.emoji,mouseX,mouseY);
        cx.globalAlpha=1;
    }
}

// ── UPDATE ────────────────────────────────────────────────────────────────────
function update() {
    objects.forEach(updateObj);
    mobs.forEach(updateMob);
    particles.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.vy+=0.12;p.alpha-=0.025;p.r*=0.96;});
    particles=particles.filter(function(p){return p.alpha>0;});
    explosions.forEach(function(e){
        if(e.type==='laser'){e.alpha-=0.07;}
        else{e.r+=e.type==='wave'?5:7;e.alpha-=0.04;}
    });
    explosions=explosions.filter(function(e){return e.alpha>0;});
    fc++;
    var now=performance.now();
    if(now-ft>=1000){
        document.getElementById('hfps').textContent=Math.round(fc*1000/(now-ft))+'fps';
        fc=0;ft=now;
    }
}
function loop(){requestAnimationFrame(loop);update();draw();}

// ── INPUT ─────────────────────────────────────────────────────────────────────
var world=document.getElementById('world');
function getP(e){
    var r=cv.getBoundingClientRect();
    return{x:(e.clientX-r.left)*(W/r.width),y:(e.clientY-r.top)*(H/r.height)};
}
function mobAt(x,y){return mobs.find(function(m){return Math.hypot(m.x-x,m.y-y)<m.w+5;});}
function objAt(x,y){return objects.slice().reverse().find(function(o){return Math.abs(o.x-x)<o.w/2+5&&Math.abs(o.y-y)<o.h/2+5;});}

world.addEventListener('mousemove',function(e){
    var p=getP(e);mouseX=p.x;mouseY=p.y;
    if(dragMob&&currentTool==='grab'){dragMob.x=p.x-dragOX;dragMob.y=p.y-dragOY;dragMob.vx=0;dragMob.vy=0;}
    else if(dragObj&&currentTool==='grab'){dragObj.x=p.x-dragOX;dragObj.y=p.y-dragOY;dragObj.vx=0;dragObj.vy=0;}
});
world.addEventListener('mousedown',function(e){
    if(e.button===2)return;
    var p=getP(e);
    if(currentTool==='place'){spawnAt(p.x,p.y,selectedItem);}
    else if(currentTool==='grab'){
        var m=mobAt(p.x,p.y);
        if(m){dragMob=m;dragOX=p.x-m.x;dragOY=p.y-m.y;}
        else{var o=objAt(p.x,p.y);if(o){dragObj=o;dragOX=p.x-o.x;dragOY=p.y-o.y;}}
    } else if(currentTool==='del'){
        var m2=mobAt(p.x,p.y);
        if(m2)mobs=mobs.filter(function(x){return x!==m2;});
        else{var o2=objAt(p.x,p.y);if(o2)objects=objects.filter(function(x){return x!==o2;});}
        updateHUD();
    }
});
world.addEventListener('mouseup',function(e){
    var p=getP(e);
    if(dragMob){dragMob.vx=(p.x-mouseX)*0.7;dragMob.vy=(p.y-mouseY)*0.7-1;dragMob=null;}
    if(dragObj){dragObj.vy-=1.5;dragObj=null;}
});
world.addEventListener('contextmenu',function(e){e.preventDefault();});

// ── TOOLS + PANEL ─────────────────────────────────────────────────────────────
function setTool(t){
    currentTool=t;
    document.querySelectorAll('.tb').forEach(function(b){b.classList.remove('active');});
    var el=document.getElementById('t-'+t);
    if(el)el.classList.add('active');
    cv.style.cursor=t==='del'?'crosshair':t==='grab'?'grab':'crosshair';
}
function setCat(cat,btn){
    currentCat=cat;
    document.querySelectorAll('.cat').forEach(function(b){b.classList.remove('active');});
    if(btn)btn.classList.add('active');
    var items=CATS[cat];
    var c=document.getElementById('items');
    c.innerHTML='';
    items.forEach(function(item,i){
        var d=document.createElement('div');
        d.className='item'+(i===0?' active':'');
        d.innerHTML='<span class="ie">'+item.emoji+'</span>'+item.name;
        d.onclick=function(){
            selectedItem=item;
            document.querySelectorAll('.item').forEach(function(el){el.classList.remove('active');});
            d.classList.add('active');
        };
        c.appendChild(d);
    });
    if(items.length)selectedItem=items[0];
}
function resetWorld(){objects=[];mobs=[];particles=[];explosions=[];totalExp=0;updateHUD();toast('🔄 World cleared!');}
function toggleG(){gravOn=!gravOn;document.getElementById('t-grav').textContent=gravOn?'🌍 Gravity':'🌌 Zero-G';toast(gravOn?'🌍 Gravity ON!':'🌌 Zero-G!');}
function chaos(){var all=objects.concat(mobs);all.forEach(function(o,i){setTimeout(function(){if(objects.includes(o)||mobs.includes(o))explode(o.x,o.y,80);},i*100);});toast('💥 CHAOS!');}
function updateHUD(){document.getElementById('hobj').textContent=objects.length+mobs.length;document.getElementById('hexp').textContent=totalExp;}
var _tt=null;
function toast(m){var el=document.getElementById('toast');el.textContent=m;el.classList.add('show');if(_tt)clearTimeout(_tt);_tt=setTimeout(function(){el.classList.remove('show');},2800);}
var _fi=0;
function showFactRandom(){if(Math.random()<0.4)toast(FACTS[_fi++%FACTS.length]);}

// ── INIT ─────────────────────────────────────────────────────────────────────
setCat('mobs', document.querySelector('.cat'));
toast('🤖 Select a mob from the panel and click to spawn! Grab tool lets you throw!');
loop();
</script>
</body>
</html>
""", height=640)
