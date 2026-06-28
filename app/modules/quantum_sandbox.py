def render_quantum_sandbox():
    """Free game: Quantum Sandbox — physics-based PQC playground."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("🧪 Quantum Sandbox")
    st.markdown(
        "**Free play!** Drop bombs, build shields, trigger chain reactions. "
        "No rules — just quantum chaos! Learn PQC by experimenting."
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
.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:3px;width:100%;margin-bottom:6px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:5px 3px;
    text-align:center;font-size:9px;color:#60a5fa;}
.hb b{display:block;font-size:13px;color:white;}

/* TOOLBAR */
#toolbar{display:flex;gap:4px;flex-wrap:wrap;justify-content:center;
    width:100%;margin-bottom:6px;}
.tool-btn{padding:6px 10px;border-radius:8px;border:2px solid #1a3a5a;
    background:#071520;color:#94a3b8;font-size:11px;cursor:pointer;
    transition:all 0.15s;text-align:center;min-width:70px;}
.tool-btn:hover{border-color:#3b82f6;color:white;background:#0a1f35;}
.tool-btn.active{border-color:#fbbf24;background:#1a1500;color:#fbbf24;}
.tool-btn .t-emoji{font-size:16px;display:block;margin-bottom:2px;}

/* CANVAS */
#gc{border:2px solid #1d4ed8;border-radius:12px;display:block;cursor:crosshair;
    box-shadow:0 0 20px rgba(59,130,246,0.15);}

/* INFO BAR */
#info-bar{background:#071520;border:1px solid #1a3a5a;border-radius:8px;
    padding:6px 12px;width:100%;margin-top:5px;font-size:11px;
    color:#60a5fa;text-align:center;min-height:28px;}

/* BOTTOM BUTTONS */
.btns{display:flex;gap:5px;flex-wrap:wrap;justify-content:center;margin-top:6px;}
.btn{padding:7px 14px;border-radius:8px;border:none;cursor:pointer;
    font-size:11px;font-weight:bold;color:white;transition:all 0.15s;}
.btn:hover{filter:brightness(1.2);}
.btn-reset{background:linear-gradient(135deg,#334155,#475569);}
.btn-chaos{background:linear-gradient(135deg,#dc2626,#ef4444);}
.btn-shield{background:linear-gradient(135deg,#059669,#10b981);}
.btn-spawn{background:linear-gradient(135deg,#1d4ed8,#3b82f6);}

/* FACT BOX */
#fact{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);
    border-radius:8px;padding:7px 10px;margin-top:5px;font-size:10px;
    color:#93c5fd;display:none;line-height:1.5;width:100%;text-align:center;}
</style>
</head>
<body>
<div id="wrap">

<div class="hud">
    <div class="hb">🌐 Nodes<br><b id="h-nodes">0</b></div>
    <div class="hb">🔐 Shields<br><b id="h-shields">0</b></div>
    <div class="hb">💥 Destroyed<br><b id="h-destroyed">0</b></div>
    <div class="hb">⚡ Zaps<br><b id="h-zaps">0</b></div>
</div>

<!-- TOOLBAR -->
<div id="toolbar">
    <div class="tool-btn active" onclick="setTool('shor')" id="tool-shor">
        <span class="t-emoji">☠️</span>Shor Bomb
    </div>
    <div class="tool-btn" onclick="setTool('kyber')" id="tool-kyber">
        <span class="t-emoji">🔐</span>Kyber Shield
    </div>
    <div class="tool-btn" onclick="setTool('zap')" id="tool-zap">
        <span class="t-emoji">⚡</span>Quantum Zap
    </div>
    <div class="tool-btn" onclick="setTool('grover')" id="tool-grover">
        <span class="t-emoji">🌊</span>Grover Wave
    </div>
    <div class="tool-btn" onclick="setTool('repair')" id="tool-repair">
        <span class="t-emoji">🔧</span>Repair
    </div>
    <div class="tool-btn" onclick="setTool('spawn')" id="tool-spawn">
        <span class="t-emoji">💻</span>Add Node
    </div>
</div>

<canvas id="gc" width="560" height="360"></canvas>

<div id="info-bar">👆 Click on the canvas to use your selected tool!</div>
<div id="fact"></div>

<div class="btns">
    <button class="btn btn-reset" onclick="resetSandbox()">🔄 Reset</button>
    <button class="btn btn-shield" onclick="shieldAll()">🔐 Shield All</button>
    <button class="btn btn-chaos" onclick="chaosMode()">🎲 CHAOS!</button>
    <button class="btn btn-spawn" onclick="spawnWave()">🌊 Spawn Wave</button>
</div>
</div>

<script>
const cv = document.getElementById('gc');
const cx = cv.getContext('2d');
const W = 560, H = 360;

// ── GAME STATE ────────────────────────────────────────────────────────────────
let nodes = [], edges = [], particles = [], lasers = [], waves = [];
let currentTool = 'shor';
let destroyed = 0, zaps = 0, shieldsPlaced = 0;
let frameId = null, factTimeout = null;

// ── NODE TYPES ────────────────────────────────────────────────────────────────
const NODE_EMOJIS = ['🏦','🏥','🏛️','⚡','📡','🌍','🔭','🚀','🏫','💊'];
const SHIELD_TYPES = [
    {name:'ML-KEM',  color:'#10b981', hp:5},
    {name:'ML-DSA',  color:'#3b82f6', hp:4},
    {name:'SPHINCS+',color:'#8b5cf6', hp:3},
    {name:'Falcon',  color:'#f59e0b', hp:4},
];
const FACTS = [
    "☠️ Shor's Algorithm can factor RSA keys instantly on a quantum computer!",
    "🔐 ML-KEM (Kyber FIPS 203) uses lattice math — immune to Shor's Algorithm!",
    "⚡ Grover's Algorithm gives quantum a speedup but can't break Kyber!",
    "💥 Cascade failures happen when connected nodes share vulnerabilities!",
    "🛡️ Dilithium (ML-DSA FIPS 204) signs every packet — no forgery possible!",
    "🌊 Harvest-Now-Decrypt-Later: enemies collect data NOW to decrypt LATER!",
    "🔧 NIST mandates migration to PQC by 2035 — NSM-10 law!",
    "🦅 Falcon (FN-DSA FIPS 206) makes the smallest quantum-safe signatures!",
];

// ── GENERATE INITIAL NETWORK ─────────────────────────────────────────────────
function genNetwork(count){
    nodes = []; edges = [];
    // Center hub
    nodes.push(makeNode(W/2, H/2, true));
    // Ring nodes
    const R = 120;
    for(let i=0;i<Math.min(count-1,8);i++){
        const a = (i/(count-1))*Math.PI*2 - Math.PI/2;
        nodes.push(makeNode(
            W/2 + R*Math.cos(a),
            H/2 + R*Math.sin(a),
            false
        ));
    }
    // Random outer nodes
    for(let i=nodes.length;i<count;i++){
        const a = Math.random()*Math.PI*2;
        const r = 60 + Math.random()*130;
        nodes.push(makeNode(
            Math.max(30, Math.min(W-30, W/2+r*Math.cos(a))),
            Math.max(30, Math.min(H-30, H/2+r*Math.sin(a))),
            false
        ));
    }
    // Connect hub to all
    for(let i=1;i<nodes.length;i++) addEdge(0,i);
    // Connect nearby nodes
    for(let i=0;i<nodes.length;i++){
        for(let j=i+1;j<nodes.length;j++){
            const d = dist(nodes[i],nodes[j]);
            if(d<160 && !edges.find(e=>(e.a===i&&e.b===j)||(e.a===j&&e.b===i))){
                addEdge(i,j);
            }
        }
    }
}

function makeNode(x,y,isHub){
    return {
        x, y,
        vx: (Math.random()-0.5)*0.3,
        vy: (Math.random()-0.5)*0.3,
        emoji: NODE_EMOJIS[Math.floor(Math.random()*NODE_EMOJIS.length)],
        shield: null,
        shieldHp: 0,
        hp: 100,
        maxHp: 100,
        destroyed: false,
        pulse: Math.random()*Math.PI*2,
        wobble: 0,
        isHub,
        id: Math.random(),
    };
}

function addEdge(a,b){
    edges.push({a,b,stress:0,broken:false,zap:0});
}

function dist(a,b){ return Math.hypot(a.x-b.x, a.y-b.y); }

// ── TOOL SELECTION ────────────────────────────────────────────────────────────
function setTool(tool){
    currentTool = tool;
    document.querySelectorAll('.tool-btn').forEach(b=>b.classList.remove('active'));
    document.getElementById('tool-'+tool)?.classList.add('active');
    const info = {
        shor:   '☠️ Shor Bomb — click a node to destroy it with a quantum explosion!',
        kyber:  '🔐 Kyber Shield — click a node to protect it with ML-KEM lattice armor!',
        zap:    '⚡ Quantum Zap — click a node to send lightning through all connections!',
        grover: '🌊 Grover Wave — click anywhere to send a weakening wave across the network!',
        repair: '🔧 Repair — click a destroyed node to bring it back online!',
        spawn:  '💻 Add Node — click anywhere to spawn a new network node!',
    };
    setInfo(info[tool]||'Select a tool above');
}

// ── CANVAS CLICK ──────────────────────────────────────────────────────────────
cv.addEventListener('click', e=>{
    const rect = cv.getBoundingClientRect();
    const mx = (e.clientX-rect.left)*(W/rect.width);
    const my = (e.clientY-rect.top)*(H/rect.height);

    if(currentTool === 'spawn'){
        const n = makeNode(mx, my, false);
        // Connect to nearest 2 nodes
        const sorted = [...nodes].sort((a,b)=>dist({x:mx,y:my},a)-dist({x:mx,y:my},b));
        nodes.push(n);
        const ni = nodes.length-1;
        sorted.slice(0,2).forEach(nb=>{
            const bi = nodes.indexOf(nb);
            if(bi>=0) addEdge(ni,bi);
        });
        spawnParticles(mx,my,'#3b82f6',6);
        setInfo('💻 New node spawned! It connects to nearby nodes automatically.');
        updateHUD(); return;
    }

    if(currentTool === 'grover'){
        waves.push({x:mx,y:my,r:0,maxR:300,alpha:1,color:'#8b5cf6'});
        // Weaken all unshielded nodes
        nodes.forEach(n=>{
            if(!n.destroyed&&!n.shield){
                n.hp = Math.max(10, n.hp-20);
                n.wobble = 8;
            }
        });
        spawnParticles(mx,my,'#8b5cf6',10);
        showFact(FACTS[Math.floor(Math.random()*FACTS.length)]);
        setInfo('🌊 Grover Wave weakened all unshielded nodes! Deploy Kyber shields to protect them!');
        updateHUD(); return;
    }

    // Find clicked node
    const node = nodes.find(n=>dist({x:mx,y:my},n)<22 && !n.destroyed);
    const deadNode = nodes.find(n=>dist({x:mx,y:my},n)<22 && n.destroyed);

    if(currentTool==='repair' && deadNode){
        deadNode.destroyed=false; deadNode.hp=100;
        deadNode.shield=null; deadNode.shieldHp=0;
        spawnParticles(deadNode.x,deadNode.y,'#10b981',10);
        destroyed=Math.max(0,destroyed-1);
        edges.forEach(edge=>{
            const ni=nodes.indexOf(deadNode);
            if(edge.a===ni||edge.b===ni){edge.broken=false;edge.stress=0;}
        });
        setInfo('🔧 Node repaired and back online!');
        updateHUD(); return;
    }

    if(!node) return;
    const ni = nodes.indexOf(node);

    if(currentTool==='shor'){
        shorBomb(node, ni);
    } else if(currentTool==='kyber'){
        deployShield(node);
    } else if(currentTool==='zap'){
        quantumZap(node, ni);
    }
});

// ── SHOR BOMB ─────────────────────────────────────────────────────────────────
function shorBomb(node, ni){
    if(node.shield){
        node.shieldHp--;
        spawnParticles(node.x,node.y,'#10b981',8);
        setInfo('🛡️ '+node.shield.name+' shield blocked the Shor Bomb! '+(node.shieldHp)+' hits left.');
        if(node.shieldHp<=0){
            node.shield=null;
            setInfo('💥 Shield destroyed! Node is now vulnerable!');
        }
        showFact('🔐 This is exactly how Kyber works — the lattice math absorbs quantum attacks!');
        return;
    }
    node.destroyed=true; node.hp=0;
    destroyed++;
    spawnParticles(node.x,node.y,'#ef4444',20);
    waves.push({x:node.x,y:node.y,r:0,maxR:80,alpha:1,color:'#ef4444'});
    // Cascade: stress connected nodes
    edges.forEach(edge=>{
        if(edge.a===ni||edge.b===ni){
            edge.broken=true; edge.stress=1;
            const other=nodes[edge.a===ni?edge.b:edge.a];
            if(other&&!other.destroyed&&!other.shield){
                other.hp=Math.max(0,other.hp-30);
                other.wobble=12;
                if(other.hp<=0){
                    other.destroyed=true; destroyed++;
                    spawnParticles(other.x,other.y,'#f97316',12);
                }
            }
        }
    });
    showFact("☠️ Shor's Algorithm destroyed the RSA key in milliseconds! This is why we need Kyber!");
    setInfo('💥 BOOM! Shor Bomb destroyed a node and triggered cascade failures!');
    updateHUD();
}

// ── KYBER SHIELD ─────────────────────────────────────────────────────────────
function deployShield(node){
    if(node.shield){
        setInfo('🔐 This node already has a '+node.shield.name+' shield!'); return;
    }
    const sh = SHIELD_TYPES[Math.floor(Math.random()*SHIELD_TYPES.length)];
    node.shield=sh; node.shieldHp=sh.hp; node.hp=100;
    shieldsPlaced++;
    spawnParticles(node.x,node.y,sh.color,12);
    showFact('🔐 '+sh.name+' shield deployed! Uses lattice math that quantum computers cannot break!');
    setInfo('🔐 '+sh.name+' shield active! This node is now quantum-safe!');
    updateHUD();
}

// ── QUANTUM ZAP ───────────────────────────────────────────────────────────────
function quantumZap(node, ni){
    zaps++;
    const connected=[];
    edges.forEach(e=>{
        if(e.a===ni) connected.push(e.b);
        if(e.b===ni) connected.push(e.a);
        if(e.a===ni||e.b===ni) e.zap=1;
    });
    connected.forEach(ci=>{
        const cn=nodes[ci];
        if(cn&&!cn.destroyed){
            lasers.push({x1:node.x,y1:node.y,x2:cn.x,y2:cn.y,
                color:'#fbbf24',alpha:1,width:3});
            if(!cn.shield){ cn.hp=Math.max(0,cn.hp-15); cn.wobble=6; }
            else{ cn.shieldHp--; if(cn.shieldHp<=0) cn.shield=null; }
        }
    });
    spawnParticles(node.x,node.y,'#fbbf24',8);
    showFact("⚡ Quantum Zap travels through network connections — just like real cyberattacks propagate through networks!");
    setInfo('⚡ Quantum Zap sent through '+connected.length+' connections!');
    updateHUD();
}

// ── CHAOS MODE ────────────────────────────────────────────────────────────────
function chaosMode(){
    let count=0;
    nodes.forEach((n,i)=>{
        if(!n.destroyed&&Math.random()<0.5){
            setTimeout(()=>{ if(!n.shield){ shorBomb(n,i); } }, count*200);
            count++;
        }
    });
    showFact('🎲 CHAOS MODE! This simulates a full-scale quantum computer attack on your network!');
    setInfo('🎲 CHAOS! Random Shor Bombs dropping across the network!');
}

// ── SHIELD ALL ────────────────────────────────────────────────────────────────
function shieldAll(){
    nodes.forEach(n=>{
        if(!n.destroyed&&!n.shield){
            const sh=SHIELD_TYPES[Math.floor(Math.random()*SHIELD_TYPES.length)];
            n.shield=sh; n.shieldHp=sh.hp; n.hp=100;
            shieldsPlaced++;
            spawnParticles(n.x,n.y,sh.color,6);
        }
    });
    showFact('🔐 All nodes shielded with NIST PQC algorithms! The network is now quantum-safe!');
    setInfo('🔐 All nodes protected with quantum-safe shields! Try CHAOS mode now!');
    updateHUD();
}

// ── SPAWN WAVE ────────────────────────────────────────────────────────────────
function spawnWave(){
    const types=['☠️ Shor Bot','🌀 Grover Drone','👾 CRQC Agent'];
    for(let i=0;i<4;i++){
        setTimeout(()=>{
            const a=Math.random()*Math.PI*2, r=280;
            const x=W/2+r*Math.cos(a), y=H/2+r*Math.sin(a);
            waves.push({x,y,r:0,maxR:60,alpha:0.8,color:'#ef4444'});
            // Attack random unshielded node
            const targets=nodes.filter(n=>!n.destroyed&&!n.shield);
            if(targets.length){
                const t=targets[Math.floor(Math.random()*targets.length)];
                const ti=nodes.indexOf(t);
                lasers.push({x1:x,y1:y,x2:t.x,y2:t.y,color:'#ef4444',alpha:1,width:2});
                setTimeout(()=>shorBomb(t,ti), 500);
            }
        }, i*600);
    }
    setInfo('🌊 Quantum attack wave incoming! Deploy shields to defend!');
}

// ── RESET ─────────────────────────────────────────────────────────────────────
function resetSandbox(){
    destroyed=0; zaps=0; shieldsPlaced=0;
    particles=[]; lasers=[]; waves=[];
    genNetwork(10);
    updateHUD();
    setInfo('🔄 Network reset! 10 nodes ready. Select a tool and click a node!');
    document.getElementById('fact').style.display='none';
}

// ── PARTICLES ─────────────────────────────────────────────────────────────────
function spawnParticles(x,y,color,n){
    for(let i=0;i<n;i++){
        const a=Math.random()*Math.PI*2, s=Math.random()*4+1;
        particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,
            r:Math.random()*4+1,alpha:1,color});
    }
}

// ── UPDATE HUD ────────────────────────────────────────────────────────────────
function updateHUD(){
    document.getElementById('h-nodes').textContent=nodes.filter(n=>!n.destroyed).length;
    document.getElementById('h-shields').textContent=nodes.filter(n=>n.shield&&!n.destroyed).length;
    document.getElementById('h-destroyed').textContent=destroyed;
    document.getElementById('h-zaps').textContent=zaps;
}

function setInfo(msg){ document.getElementById('info-bar').textContent=msg; }

function showFact(text){
    const el=document.getElementById('fact');
    el.textContent=text; el.style.display='block';
    if(factTimeout) clearTimeout(factTimeout);
    factTimeout=setTimeout(()=>el.style.display='none',5000);
}

// ── GAME LOOP ─────────────────────────────────────────────────────────────────
function update(){
    // Update nodes
    nodes.forEach(n=>{
        if(n.destroyed) return;
        n.pulse+=0.04;
        if(n.wobble>0){ n.wobble*=0.85; }
        // Gentle drift
        n.x+=n.vx; n.y+=n.vy;
        // Bounce off walls
        if(n.x<25||n.x>W-25) n.vx*=-1;
        if(n.y<25||n.y>H-25) n.vy*=-1;
        n.x=Math.max(25,Math.min(W-25,n.x));
        n.y=Math.max(25,Math.min(H-25,n.y));
    });
    // Update particles
    particles.forEach(p=>{ p.x+=p.vx; p.y+=p.vy; p.alpha-=0.035; p.r*=0.96; });
    particles=particles.filter(p=>p.alpha>0);
    // Update lasers
    lasers.forEach(l=>l.alpha-=0.06);
    lasers=lasers.filter(l=>l.alpha>0);
    // Update waves
    waves.forEach(w=>{ w.r+=4; w.alpha-=0.04; });
    waves=waves.filter(w=>w.alpha>0);
    // Update edge zap
    edges.forEach(e=>{ if(e.zap>0) e.zap-=0.05; });
}

function draw(){
    cx.clearRect(0,0,W,H);
    // Background
    cx.fillStyle='#020d14'; cx.fillRect(0,0,W,H);
    // Grid
    cx.strokeStyle='#0a1f2e'; cx.lineWidth=0.4;
    for(let x=0;x<W;x+=30){cx.beginPath();cx.moveTo(x,0);cx.lineTo(x,H);cx.stroke();}
    for(let y=0;y<H;y+=30){cx.beginPath();cx.moveTo(0,y);cx.lineTo(W,y);cx.stroke();}

    // Draw waves
    waves.forEach(w=>{
        cx.beginPath(); cx.arc(w.x,w.y,w.r,0,Math.PI*2);
        cx.strokeStyle=w.color+Math.floor(w.alpha*255).toString(16).padStart(2,'0');
        cx.lineWidth=2; cx.stroke();
    });

    // Draw edges
    edges.forEach(e=>{
        const na=nodes[e.a], nb=nodes[e.b];
        if(!na||!nb) return;
        cx.beginPath(); cx.moveTo(na.x,na.y); cx.lineTo(nb.x,nb.y);
        cx.setLineDash(e.broken?[4,4]:[]);
        if(e.zap>0){
            cx.strokeStyle='#fbbf24'; cx.lineWidth=2+e.zap*2;
        } else if(e.broken){
            cx.strokeStyle='#47556930'; cx.lineWidth=1;
        } else {
            const bothShielded=nodes[e.a].shield&&nodes[e.b].shield;
            cx.strokeStyle=bothShielded?'#10b98130':'#1d4ed820';
            cx.lineWidth=1;
        }
        cx.stroke(); cx.setLineDash([]);
    });

    // Draw lasers
    lasers.forEach(l=>{
        cx.beginPath(); cx.moveTo(l.x1,l.y1); cx.lineTo(l.x2,l.y2);
        cx.strokeStyle=l.color+Math.floor(l.alpha*255).toString(16).padStart(2,'0');
        cx.lineWidth=l.width; cx.stroke();
    });

    // Draw nodes
    nodes.forEach(n=>{
        const wob=n.wobble||0;
        const nx=n.x+(Math.random()-0.5)*wob*0.3;
        const ny=n.y+(Math.random()-0.5)*wob*0.3;

        if(n.destroyed){
            // Destroyed node
            cx.beginPath(); cx.arc(nx,ny,18,0,Math.PI*2);
            cx.fillStyle='#1a0505'; cx.fill();
            cx.strokeStyle='#ef444440'; cx.lineWidth=1; cx.stroke();
            cx.font='14px serif'; cx.textAlign='center'; cx.textBaseline='middle';
            cx.globalAlpha=0.3; cx.fillText('💀',nx,ny); cx.globalAlpha=1;
            return;
        }

        // Shield glow
        const shColor=n.shield?n.shield.color:'#1d4ed8';
        if(n.shield){
            cx.shadowColor=shColor; cx.shadowBlur=15;
            // Shield ring
            cx.beginPath();
            cx.arc(nx,ny,24+Math.sin(n.pulse)*2,0,Math.PI*2);
            cx.strokeStyle=shColor+'60'; cx.lineWidth=2; cx.stroke();
        }

        // Pulse ring
        const pr=20+Math.sin(n.pulse)*3;
        cx.beginPath(); cx.arc(nx,ny,pr,0,Math.PI*2);
        cx.strokeStyle=(n.shield?shColor:'#ef4444')+'25';
        cx.lineWidth=1; cx.stroke();

        // HP arc
        if(n.hp<100){
            cx.beginPath();
            cx.arc(nx,ny,22,-Math.PI/2,-Math.PI/2+(n.hp/100)*Math.PI*2);
            cx.strokeStyle=n.hp>50?'#10b981':'#ef4444';
            cx.lineWidth=3; cx.stroke();
        }

        // Node body
        cx.beginPath(); cx.arc(nx,ny,18,0,Math.PI*2);
        cx.fillStyle=n.isHub?'#0d2a4a':'#071520';
        cx.fill();
        cx.strokeStyle=n.shield?shColor:(n.isHub?'#60a5fa':'#334155');
        cx.lineWidth=n.isHub?3:2; cx.stroke();
        cx.shadowBlur=0;

        // Emoji
        cx.font=(n.isHub?'16px':'13px')+' serif';
        cx.textAlign='center'; cx.textBaseline='middle';
        cx.fillText(n.emoji,nx,ny);

        // Shield icon
        if(n.shield){
            cx.font='9px serif'; cx.fillStyle=shColor;
            const icons={
                'ML-KEM':'🔐','ML-DSA':'✍️','SPHINCS+':'🌲','Falcon':'🦅'
            };
            cx.fillText(icons[n.shield.name]||'🛡️',nx+14,ny-14);
            // Shield HP bar
            cx.fillStyle='#1e293b'; cx.fillRect(nx-12,ny-26,24,3);
            cx.fillStyle=shColor;
            cx.fillRect(nx-12,ny-26,24*(n.shieldHp/n.shield.hp),3);
        }

        // Hub label
        if(n.isHub){
            cx.font='8px sans-serif'; cx.fillStyle='#60a5fa';
            cx.fillText('HUB',nx,ny+26);
        }
    });

    // Draw particles
    particles.forEach(p=>{
        cx.beginPath(); cx.arc(p.x,p.y,p.r,0,Math.PI*2);
        cx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,'0');
        cx.fill();
    });
}

function loop(){ frameId=requestAnimationFrame(loop); update(); draw(); }

// ── INIT ─────────────────────────────────────────────────────────────────────
genNetwork(10);
updateHUD();
setInfo('🧪 Welcome to Quantum Sandbox! Select a tool above and click a node!');
loop();
</script>
</body>
</html>
""", height=720)
