def render_logic_gates():
    """Middle School: Logic Gate Builder — drag and drop AND, OR, XOR, NOT, NAND to build circuits."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("⚡ Logic Gate Lab — Build Circuits from Scratch!")
    st.markdown(
        "**Drag logic gates onto the canvas and connect them!** "
        "Logic gates are the building blocks of ALL computers — and quantum-safe cryptography. "
        "Complete challenges to unlock new gates and earn XP!"
    )

    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow:hidden;}
#wrap{display:flex;flex-direction:column;height:640px;}

/* TOP BAR */
#topbar{background:#071520;border-bottom:1px solid #1a3a5a;padding:6px 12px;
    display:flex;align-items:center;gap:10px;flex-shrink:0;}
.score-pill{background:#0a1f35;border:1px solid #1a3a5a;border-radius:20px;
    padding:3px 10px;font-size:10px;color:#60a5fa;}
.score-pill b{color:white;}
#mode-btns{display:flex;gap:4px;margin-left:auto;}
.mode-btn{padding:4px 10px;border-radius:6px;border:1px solid #1a3a5a;
    background:transparent;color:#60a5fa;font-size:10px;cursor:pointer;}
.mode-btn.active{background:#1d4ed8;color:white;border-color:#3b82f6;}

/* MAIN LAYOUT */
#main{display:flex;flex:1;overflow:hidden;}

/* PALETTE */
#palette{width:130px;flex-shrink:0;background:#071520;border-right:1px solid #1a3a5a;
    overflow-y:auto;padding:8px;}
.pal-title{font-size:8px;font-weight:700;letter-spacing:1.5px;color:#475569;
    text-transform:uppercase;padding:4px 0;margin-bottom:6px;}
.gate-item{background:#0a1f35;border:1px solid #1a3a5a;border-radius:8px;
    padding:8px 6px;margin-bottom:6px;cursor:grab;text-align:center;
    transition:all 0.15s;position:relative;}
.gate-item:hover{transform:scale(1.05);border-color:#3b82f6;}
.gate-item:active{cursor:grabbing;}
.gate-name{font-size:10px;font-weight:700;margin-bottom:2px;}
.gate-desc{font-size:8px;color:#94a3b8;line-height:1.4;}
.gate-preview{font-size:18px;margin-bottom:3px;}
.gate-locked{opacity:0.4;cursor:not-allowed;}
.gate-locked::after{content:'🔒';position:absolute;top:4px;right:4px;font-size:10px;}

/* CANVAS */
#canvas-wrap{flex:1;position:relative;overflow:hidden;}
#cv{display:block;cursor:crosshair;}

/* RIGHT PANEL */
#right{width:160px;flex-shrink:0;background:#071520;border-left:1px solid #1a3a5a;
    display:flex;flex-direction:column;overflow:hidden;}
.rp-sec{padding:10px;border-bottom:1px solid #1a3a5a;}
.rp-title{font-size:8px;font-weight:700;letter-spacing:1px;color:#475569;
    text-transform:uppercase;margin-bottom:8px;}

/* TRUTH TABLE */
.tt{width:100%;border-collapse:collapse;font-size:9px;}
.tt th{background:#0a1f35;padding:3px 4px;text-align:center;color:#60a5fa;font-weight:700;}
.tt td{padding:3px 4px;text-align:center;border-bottom:1px solid #1a3a5a;}
.tt .one{color:#10b981;font-weight:700;}
.tt .zero{color:#475569;}

/* CHALLENGE BOX */
#challenge{background:rgba(59,130,246,0.06);border:1px solid rgba(59,130,246,0.2);
    border-radius:8px;margin:8px;padding:8px;font-size:9px;}
.ch-title{color:#60a5fa;font-weight:700;font-size:10px;margin-bottom:4px;}
.ch-desc{color:#94a3b8;line-height:1.5;}
.ch-progress{margin-top:6px;height:4px;background:#1e293b;border-radius:2px;}
.ch-fill{height:100%;border-radius:2px;background:#10b981;transition:width 0.4s;}

/* BOTTOM BAR */
#bottom{background:#071520;border-top:1px solid #1a3a5a;padding:6px 12px;
    display:flex;gap:6px;align-items:center;flex-shrink:0;}
.bb-btn{padding:5px 12px;border-radius:6px;border:none;cursor:pointer;
    font-size:10px;font-weight:700;color:white;transition:all 0.15s;}
.bb-btn:hover{filter:brightness(1.2);}
#msg-bar{font-size:10px;color:#60a5fa;flex:1;text-align:center;}

/* WIRE TOOLTIP */
#tooltip{position:fixed;background:#071520;border:1px solid #3b82f6;border-radius:6px;
    padding:5px 10px;font-size:10px;pointer-events:none;display:none;z-index:100;}

/* CONFETTI */
.cp{position:fixed;pointer-events:none;z-index:999;width:7px;height:7px;
    border-radius:2px;animation:cf linear forwards;}
@keyframes cf{0%{transform:translateY(-20px) rotate(0deg);opacity:1;}
    100%{transform:translateY(600px) rotate(720deg);opacity:0;}}

/* WIRE ANIMATION */
@keyframes flow{0%{stroke-dashoffset:20;}100%{stroke-dashoffset:0;}}
</style>
</head>
<body>
<div id="wrap">

<!-- TOP BAR -->
<div id="topbar">
    <span style="font-size:12px;font-weight:700;color:#7c3aed">⚡ Logic Gate Lab</span>
    <div class="score-pill">⭐ Score: <b id="score-val">0</b></div>
    <div class="score-pill">🎯 Gates: <b id="gate-count">0</b></div>
    <div class="score-pill">⚡ XP: <b id="xp-val">0</b></div>
    <div id="mode-btns">
        <button class="mode-btn active" onclick="setMode('build')">🏗 Build</button>
        <button class="mode-btn" onclick="setMode('wire')">🔌 Wire</button>
        <button class="mode-btn" onclick="setMode('delete')">🗑 Delete</button>
        <button class="mode-btn" onclick="clearAll()" style="color:#ef4444">Clear</button>
    </div>
</div>

<div id="main">

<!-- GATE PALETTE -->
<div id="palette">
    <div class="pal-title">Logic Gates</div>

    <div class="gate-item" id="gi-AND" draggable="true" ondragstart="startDrag(event,'AND')" onclick="selectGateType('AND')">
        <div class="gate-preview">🔵</div>
        <div class="gate-name" style="color:#3b82f6">AND</div>
        <div class="gate-desc">Both inputs must be 1</div>
    </div>

    <div class="gate-item" id="gi-OR" draggable="true" ondragstart="startDrag(event,'OR')" onclick="selectGateType('OR')">
        <div class="gate-preview">🟢</div>
        <div class="gate-name" style="color:#10b981">OR</div>
        <div class="gate-desc">At least one input is 1</div>
    </div>

    <div class="gate-item" id="gi-NOT" draggable="true" ondragstart="startDrag(event,'NOT')" onclick="selectGateType('NOT')">
        <div class="gate-preview">🔴</div>
        <div class="gate-name" style="color:#ef4444">NOT</div>
        <div class="gate-desc">Flips 0→1 and 1→0</div>
    </div>

    <div class="gate-item" id="gi-XOR" draggable="true" ondragstart="startDrag(event,'XOR')" onclick="selectGateType('XOR')">
        <div class="gate-preview">🟡</div>
        <div class="gate-name" style="color:#fbbf24">XOR</div>
        <div class="gate-desc">Different inputs = 1</div>
    </div>

    <div class="gate-item" id="gi-NAND" draggable="true" ondragstart="startDrag(event,'NAND')" onclick="selectGateType('NAND')">
        <div class="gate-preview">🟣</div>
        <div class="gate-name" style="color:#8b5cf6">NAND</div>
        <div class="gate-desc">NOT AND — universal!</div>
    </div>

    <div class="gate-item" id="gi-NOR" draggable="true" ondragstart="startDrag(event,'NOR')" onclick="selectGateType('NOR')">
        <div class="gate-preview">🟠</div>
        <div class="gate-name" style="color:#f97316">NOR</div>
        <div class="gate-desc">NOT OR — universal!</div>
    </div>

    <div class="pal-title" style="margin-top:8px">I/O</div>

    <div class="gate-item" id="gi-INPUT" draggable="true" ondragstart="startDrag(event,'INPUT')" onclick="selectGateType('INPUT')">
        <div class="gate-preview">⬛</div>
        <div class="gate-name" style="color:#94a3b8">INPUT</div>
        <div class="gate-desc">Click to toggle 0/1</div>
    </div>

    <div class="gate-item" id="gi-OUTPUT" draggable="true" ondragstart="startDrag(event,'OUTPUT')" onclick="selectGateType('OUTPUT')">
        <div class="gate-preview">💡</div>
        <div class="gate-name" style="color:#fbbf24">OUTPUT</div>
        <div class="gate-desc">Shows result</div>
    </div>
</div>

<!-- CANVAS -->
<div id="canvas-wrap">
    <canvas id="cv"></canvas>
</div>

<!-- RIGHT PANEL -->
<div id="right">
    <div class="rp-sec">
        <div class="rp-title">Truth Table</div>
        <div id="truth-table-wrap"></div>
    </div>
    <div class="rp-sec">
        <div class="rp-title">Selected Gate</div>
        <div id="gate-info" style="font-size:9px;color:#94a3b8">
            Click any gate on the canvas to see its truth table here.
        </div>
    </div>
    <div style="padding:10px;font-size:9px;color:#94a3b8;line-height:1.6;flex:1;overflow-y:auto">
        <div style="color:#60a5fa;font-weight:700;margin-bottom:4px">🔐 PQC Connection</div>
        <div id="pqc-tip">Logic gates are the foundation of ALL cryptography! XOR is used in every hash function including SHA-3 — the algorithm behind SPHINCS+ (FIPS 205).</div>
    </div>
</div>
</div>

<!-- CHALLENGE -->
<div id="challenge">
    <div class="ch-title" id="ch-title">🎯 Challenge 1: Build an AND gate circuit</div>
    <div class="ch-desc" id="ch-desc">Place 2 INPUT nodes and connect them to an AND gate, then connect the AND gate to an OUTPUT. Click inputs to toggle 0/1!</div>
    <div class="ch-progress"><div class="ch-fill" id="ch-fill" style="width:0%"></div></div>
</div>

<!-- BOTTOM BAR -->
<div id="bottom">
    <button class="bb-btn" style="background:#059669" onclick="simulate()">▶ Simulate</button>
    <button class="bb-btn" style="background:#7c3aed" onclick="loadChallenge(currentChallenge)">🎯 Hint</button>
    <button class="bb-btn" style="background:#334155" onclick="clearAll()">🗑 Clear</button>
    <div id="msg-bar">Place gates and connect them with wires! Select BUILD mode then click to place.</div>
</div>
</div>
<div id="tooltip"></div>

<script>
var cv = document.getElementById('cv');
var ctx = cv.getContext('2d');
var W, H;

function resize() {
    var wrap = document.getElementById('canvas-wrap');
    var r = wrap.getBoundingClientRect();
    W = cv.width = r.width;
    H = cv.height = r.height;
}
resize();
window.addEventListener('resize', function(){resize();draw();});

// ── STATE ─────────────────────────────────────────────────────────────────────
var gates = [];
var wires = [];
var mode = 'build';
var selectedType = 'AND';
var dragging = null, dragOffX=0, dragOffY=0;
var wireStart = null;
var score = 0, xp = 0;
var currentChallenge = 0;

var GATE_COLORS = {
    AND:'#3b82f6', OR:'#10b981', NOT:'#ef4444',
    XOR:'#fbbf24', NAND:'#8b5cf6', NOR:'#f97316',
    INPUT:'#475569', OUTPUT:'#ca8a04',
};

var GATE_TRUTH = {
    AND:  [[0,0,0],[0,1,0],[1,0,0],[1,1,1]],
    OR:   [[0,0,0],[0,1,1],[1,0,1],[1,1,1]],
    NOT:  [[0,1],[1,0]],
    XOR:  [[0,0,0],[0,1,1],[1,0,1],[1,1,0]],
    NAND: [[0,0,1],[0,1,1],[1,0,1],[1,1,0]],
    NOR:  [[0,0,1],[0,1,0],[1,0,0],[1,1,0]],
};

var PQC_TIPS = {
    AND:'AND gates appear in SHA-3 circuits — the hash function used by SPHINCS+ (FIPS 205)!',
    OR:'OR logic is used in AES key schedules and in the Mix Columns operation of symmetric crypto.',
    NOT:'NOT gates create complements — essential for building the S-box in AES encryption!',
    XOR:'XOR is THE most important gate in cryptography! SHA-3, AES, and all stream ciphers use XOR as their core operation. ML-KEM uses XOR for key derivation!',
    NAND:'NAND is a universal gate — you can build ANY circuit with only NAND gates. Used in hardware implementations of PQC algorithms!',
    NOR:'NOR is also universal. The compact NOR designs appear in Falcon (FN-DSA) ASIC implementations for IoT devices.',
    INPUT:'Input signals represent the data being protected — bits of a plaintext message or cryptographic key.',
    OUTPUT:'Output represents the cryptographic result — a hash, signature, or encrypted value.',
};

// ── GATE CLASS ────────────────────────────────────────────────────────────────
var nextId = 1;
function createGate(type, x, y) {
    var isOneInput = type==='NOT'||type==='INPUT'||type==='OUTPUT';
    return {
        id: nextId++,
        type: type,
        x: x, y: y,
        w: type==='INPUT'||type==='OUTPUT'?50:70,
        h: type==='INPUT'||type==='OUTPUT'?40:50,
        inputs: isOneInput&&type!=='NOT' ? 1 : (type==='NOT'?1:2),
        value: type==='INPUT'?0:null,
        color: GATE_COLORS[type]||'#475569',
    };
}

function getInputPorts(g) {
    var ports = [];
    if (g.type==='INPUT') return [];
    var n = g.type==='NOT'?1:2;
    for (var i=0;i<n;i++) {
        ports.push({
            x: g.x,
            y: g.y + g.h*(i+1)/(n+1),
        });
    }
    return ports;
}

function getOutputPort(g) {
    return {x: g.x+g.w, y: g.y+g.h/2};
}

// ── DRAG FROM PALETTE ─────────────────────────────────────────────────────────
var dragType = null;
function startDrag(e, type) {
    dragType = type;
    e.dataTransfer.setData('text', type);
}
function selectGateType(type) {
    selectedType = type;
    showGateInfo(type);
}

cv.addEventListener('dragover', function(e){e.preventDefault();});
cv.addEventListener('drop', function(e){
    e.preventDefault();
    var r = cv.getBoundingClientRect();
    var x = e.clientX-r.left-35;
    var y = e.clientY-r.top-25;
    if (dragType) {
        var g = createGate(dragType, x, y);
        gates.push(g);
        score+=5;xp+=5;
        updateScore();
        dragType=null;
        simulate();
        checkChallenge();
        setMsg('Placed '+g.type+' gate! Connect it with wires in Wire mode.');
    }
});

// ── CANVAS INTERACTIONS ───────────────────────────────────────────────────────
cv.addEventListener('mousedown', function(e){
    var r=cv.getBoundingClientRect();
    var mx=e.clientX-r.left, my=e.clientY-r.top;

    if (mode==='delete') {
        // Delete gate or wire
        var g=gateAt(mx,my);
        if(g){
            gates=gates.filter(function(x){return x.id!==g.id;});
            wires=wires.filter(function(w){return w.fromId!==g.id&&w.toId!==g.id;});
            simulate();checkChallenge();
        }
        return;
    }

    if (mode==='build') {
        var g=gateAt(mx,my);
        if(g){
            if(g.type==='INPUT'){
                // Toggle input value
                g.value=1-g.value;
                score+=2;xp+=2;updateScore();
                simulate();checkChallenge();
            } else {
                showGateInfo(g.type);
                dragging=g;dragOffX=mx-g.x;dragOffY=my-g.y;
            }
        } else {
            // Place selected gate
            var ng=createGate(selectedType,mx-35,my-25);
            gates.push(ng);
            score+=5;xp+=5;updateScore();
            simulate();checkChallenge();
        }
        return;
    }

    if (mode==='wire') {
        // Check output port of a gate
        var found=null;
        gates.forEach(function(g){
            if(g.type==='OUTPUT') return;
            var op=getOutputPort(g);
            if(Math.hypot(mx-op.x,my-op.y)<12) found={gate:g,port:'output'};
        });
        // Check input port
        gates.forEach(function(g){
            if(g.type==='INPUT') return;
            getInputPorts(g).forEach(function(ip,i){
                if(Math.hypot(mx-ip.x,my-ip.y)<12) {
                    if(!found) found={gate:g,port:'input',idx:i};
                }
            });
        });
        if(found){
            if(!wireStart){
                wireStart=found;
                setMsg('Now click the destination port to complete the wire!');
            } else {
                // Complete wire
                if(wireStart.gate.id!==found.gate.id &&
                   wireStart.port!==found.port) {
                    var from=wireStart.port==='output'?wireStart:found;
                    var to=wireStart.port==='input'?wireStart:found;
                    if(from.port==='output'&&to.port==='input'){
                        // Check not duplicate
                        var dup=wires.find(function(w){
                            return w.fromId===from.gate.id&&w.toId===to.gate.id&&w.toIdx===to.idx;
                        });
                        if(!dup){
                            wires.push({fromId:from.gate.id,toId:to.gate.id,toIdx:to.idx,active:false});
                            score+=10;xp+=10;updateScore();
                            simulate();checkChallenge();
                            setMsg('Wire connected! Click Simulate to update.');
                        }
                    }
                }
                wireStart=null;
            }
        }
    }
});

cv.addEventListener('mousemove',function(e){
    var r=cv.getBoundingClientRect();
    var mx=e.clientX-r.left,my=e.clientY-r.top;
    if(dragging&&mode==='build'){
        dragging.x=mx-dragOffX;dragging.y=my-dragOffY;
    }
    // Tooltip
    var g=gateAt(mx,my);
    var tip=document.getElementById('tooltip');
    if(g){
        tip.style.display='block';
        tip.style.left=(e.clientX+12)+'px';tip.style.top=(e.clientY-20)+'px';
        tip.textContent=g.type+(g.type==='INPUT'?' = '+g.value:'')+(g.value!==null&&g.type!=='INPUT'?' → '+g.value:'');
    } else {tip.style.display='none';}
});

cv.addEventListener('mouseup',function(){dragging=null;});

function gateAt(mx,my){
    for(var i=gates.length-1;i>=0;i--){
        var g=gates[i];
        if(mx>=g.x&&mx<=g.x+g.w&&my>=g.y&&my<=g.y+g.h) return g;
    }
    return null;
}

// ── SIMULATION ────────────────────────────────────────────────────────────────
function simulate(){
    // Topological evaluation
    var vals={};
    gates.forEach(function(g){if(g.type==='INPUT') vals[g.id]=g.value;});

    // Multiple passes for propagation
    for(var pass=0;pass<10;pass++){
        gates.forEach(function(g){
            if(g.type==='INPUT') return;
            var inWires=wires.filter(function(w){return w.toId===g.id;});
            if(g.type==='NOT'){
                var w=inWires[0];
                if(w&&vals[w.fromId]!==undefined){
                    vals[g.id]=vals[w.fromId]?0:1;
                    g.value=vals[g.id];
                }
            } else if(g.type==='OUTPUT'){
                var w=inWires[0];
                if(w&&vals[w.fromId]!==undefined){
                    vals[g.id]=vals[w.fromId];g.value=vals[g.id];
                }
            } else {
                var w0=inWires.find(function(w){return w.toIdx===0;});
                var w1=inWires.find(function(w){return w.toIdx===1;});
                if(w0&&w1&&vals[w0.fromId]!==undefined&&vals[w1.fromId]!==undefined){
                    var a=vals[w0.fromId],b=vals[w1.fromId];
                    var v;
                    if(g.type==='AND') v=a&b;
                    else if(g.type==='OR') v=a|b;
                    else if(g.type==='XOR') v=a^b;
                    else if(g.type==='NAND') v=(a&b)?0:1;
                    else if(g.type==='NOR') v=(a|b)?0:1;
                    vals[g.id]=v;g.value=v;
                }
            }
        });
    }

    // Update wire states
    wires.forEach(function(w){
        w.active=vals[w.fromId]===1;
    });

    updateTruthDisplay();
}

// ── DRAW ──────────────────────────────────────────────────────────────────────
function draw(){
    ctx.clearRect(0,0,W,H);
    ctx.fillStyle='#050a0f';ctx.fillRect(0,0,W,H);

    // Grid
    ctx.strokeStyle='#0a1f2e';ctx.lineWidth=0.4;
    for(var gx=0;gx<W;gx+=40){ctx.beginPath();ctx.moveTo(gx,0);ctx.lineTo(gx,H);ctx.stroke();}
    for(var gy=0;gy<H;gy+=40){ctx.beginPath();ctx.moveTo(0,gy);ctx.lineTo(W,gy);ctx.stroke();}

    // Wires
    wires.forEach(function(w){
        var from=gates.find(function(g){return g.id===w.fromId;});
        var to=gates.find(function(g){return g.id===w.toId;});
        if(!from||!to) return;
        var sp=getOutputPort(from);
        var ep=getInputPorts(to)[w.toIdx];
        if(!ep) return;
        var col=w.active?'#10b981':'#1e3a5a';
        var mid=(sp.x+ep.x)/2;
        ctx.beginPath();
        ctx.moveTo(sp.x,sp.y);
        ctx.bezierCurveTo(mid,sp.y,mid,ep.y,ep.x,ep.y);
        ctx.strokeStyle=col;ctx.lineWidth=w.active?2.5:1.5;
        if(w.active){ctx.shadowColor='#10b981';ctx.shadowBlur=6;}
        ctx.stroke();ctx.shadowBlur=0;
        // Arrow
        ctx.beginPath();ctx.arc(ep.x,ep.y,3,0,Math.PI*2);
        ctx.fillStyle=col;ctx.fill();
    });

    // Wire in progress
    if(wireStart&&mode==='wire'){
        var sp2;
        if(wireStart.port==='output') sp2=getOutputPort(wireStart.gate);
        else sp2=getInputPorts(wireStart.gate)[wireStart.idx];
        if(sp2){
            ctx.beginPath();ctx.arc(sp2.x,sp2.y,6,0,Math.PI*2);
            ctx.strokeStyle='#fbbf24';ctx.lineWidth=2;ctx.stroke();
        }
    }

    // Gates
    gates.forEach(drawGate);

    // Port indicators in wire mode
    if(mode==='wire'){
        gates.forEach(function(g){
            if(g.type!=='INPUT'){
                getInputPorts(g).forEach(function(p){
                    ctx.beginPath();ctx.arc(p.x,p.y,5,0,Math.PI*2);
                    ctx.fillStyle='#3b82f630';ctx.fill();
                    ctx.strokeStyle='#3b82f6';ctx.lineWidth=1;ctx.stroke();
                });
            }
            if(g.type!=='OUTPUT'){
                var op=getOutputPort(g);
                ctx.beginPath();ctx.arc(op.x,op.y,5,0,Math.PI*2);
                ctx.fillStyle='#10b98130';ctx.fill();
                ctx.strokeStyle='#10b981';ctx.lineWidth=1;ctx.stroke();
            }
        });
    }
}

function drawGate(g){
    var col=g.color;
    var glow=g.value===1;

    ctx.save();
    if(glow){ctx.shadowColor=col;ctx.shadowBlur=15;}

    if(g.type==='INPUT'){
        // Toggle switch style
        ctx.fillStyle=g.value?col+'33':'#1e293b';
        ctx.strokeStyle=g.value?col:'#334155';
        ctx.lineWidth=2;
        ctx.beginPath();
        if(ctx.roundRect) ctx.roundRect(g.x,g.y,g.w,g.h,8);
        else ctx.rect(g.x,g.y,g.w,g.h);
        ctx.fill();ctx.stroke();
        ctx.font='bold 16px sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';
        ctx.fillStyle=g.value?col:'#475569';
        ctx.fillText(g.value?'1':'0',g.x+g.w/2,g.y+g.h/2);
        ctx.font='7px sans-serif';ctx.fillStyle='#475569';
        ctx.fillText('INPUT',g.x+g.w/2,g.y+g.h-7);
        // Output dot
        ctx.beginPath();ctx.arc(g.x+g.w,g.y+g.h/2,4,0,Math.PI*2);
        ctx.fillStyle=g.value?col:'#334155';ctx.fill();

    } else if(g.type==='OUTPUT'){
        // Bulb style
        ctx.fillStyle=g.value?'#fbbf2430':'#1e293b';
        ctx.strokeStyle=g.value?'#fbbf24':'#334155';
        ctx.lineWidth=2;
        ctx.beginPath();
        if(ctx.roundRect) ctx.roundRect(g.x,g.y,g.w,g.h,8);
        else ctx.rect(g.x,g.y,g.w,g.h);
        ctx.fill();ctx.stroke();
        ctx.font=g.value?'22px':'16px';
        ctx.textAlign='center';ctx.textBaseline='middle';
        ctx.fillText(g.value?'💡':'⬛',g.x+g.w/2,g.y+g.h/2-2);
        ctx.font='7px sans-serif';ctx.fillStyle='#475569';
        ctx.fillText(g.value?'1':'0',g.x+g.w/2,g.y+g.h-7);
        // Input dot
        ctx.beginPath();ctx.arc(g.x,g.y+g.h/2,4,0,Math.PI*2);
        ctx.fillStyle='#334155';ctx.fill();

    } else {
        // Logic gate shapes
        ctx.fillStyle=col+'22';
        ctx.strokeStyle=col;
        ctx.lineWidth=2;

        // Draw gate shape
        drawGateShape(g,col);

        // Gate label
        ctx.font='bold 11px monospace';
        ctx.fillStyle='white';ctx.textAlign='center';ctx.textBaseline='middle';
        ctx.fillText(g.type,g.x+g.w/2,g.y+g.h/2);

        // Value bubble
        if(g.value!==null){
            ctx.beginPath();ctx.arc(g.x+g.w-8,g.y+8,8,0,Math.PI*2);
            ctx.fillStyle=g.value?'#10b981':'#ef4444';ctx.fill();
            ctx.font='bold 8px sans-serif';ctx.fillStyle='white';
            ctx.textAlign='center';ctx.textBaseline='middle';
            ctx.fillText(g.value,g.x+g.w-8,g.y+8);
        }

        // Input ports
        getInputPorts(g).forEach(function(p){
            ctx.beginPath();ctx.arc(p.x,p.y,3,0,Math.PI*2);
            ctx.fillStyle=col+'80';ctx.fill();
        });
        // Output port
        var op=getOutputPort(g);
        ctx.beginPath();ctx.arc(op.x,op.y,3,0,Math.PI*2);
        ctx.fillStyle=col;ctx.fill();
    }

    ctx.shadowBlur=0;
    ctx.restore();
}

function drawGateShape(g,col){
    ctx.fillStyle=col+'22';ctx.strokeStyle=col;ctx.lineWidth=2;
    var x=g.x,y=g.y,w=g.w,h=g.h;

    if(g.type==='AND'){
        ctx.beginPath();
        ctx.moveTo(x,y);ctx.lineTo(x+w*0.5,y);
        ctx.bezierCurveTo(x+w*1.1,y,x+w*1.1,y+h,x+w*0.5,y+h);
        ctx.lineTo(x,y+h);ctx.closePath();
        ctx.fill();ctx.stroke();
    } else if(g.type==='OR'||g.type==='XOR'){
        ctx.beginPath();
        ctx.moveTo(x,y);
        ctx.quadraticCurveTo(x+w*0.4,y+h*0.5,x,y+h);
        ctx.quadraticCurveTo(x+w*0.6,y+h,x+w,y+h*0.5);
        ctx.quadraticCurveTo(x+w*0.6,y,x,y);
        ctx.fill();ctx.stroke();
        if(g.type==='XOR'){
            ctx.beginPath();
            ctx.moveTo(x-8,y);ctx.quadraticCurveTo(x-8+w*0.4,y+h*0.5,x-8,y+h);
            ctx.strokeStyle=col;ctx.stroke();
        }
    } else if(g.type==='NOT'){
        ctx.beginPath();
        ctx.moveTo(x,y);ctx.lineTo(x+w*0.8,y+h*0.5);ctx.lineTo(x,y+h);ctx.closePath();
        ctx.fill();ctx.stroke();
        ctx.beginPath();ctx.arc(x+w*0.9,y+h*0.5,w*0.1,0,Math.PI*2);
        ctx.stroke();
    } else if(g.type==='NAND'){
        // AND with bubble
        ctx.beginPath();
        ctx.moveTo(x,y);ctx.lineTo(x+w*0.45,y);
        ctx.bezierCurveTo(x+w,y,x+w,y+h,x+w*0.45,y+h);
        ctx.lineTo(x,y+h);ctx.closePath();
        ctx.fill();ctx.stroke();
        ctx.beginPath();ctx.arc(x+w+5,y+h*0.5,5,0,Math.PI*2);
        ctx.strokeStyle=col;ctx.stroke();
    } else if(g.type==='NOR'){
        ctx.beginPath();
        ctx.moveTo(x,y);
        ctx.quadraticCurveTo(x+w*0.4,y+h*0.5,x,y+h);
        ctx.quadraticCurveTo(x+w*0.5,y+h,x+w*0.8,y+h*0.5);
        ctx.quadraticCurveTo(x+w*0.5,y,x,y);
        ctx.fill();ctx.stroke();
        ctx.beginPath();ctx.arc(x+w*0.9,y+h*0.5,5,0,Math.PI*2);
        ctx.strokeStyle=col;ctx.stroke();
    }
}

// ── TRUTH TABLE ───────────────────────────────────────────────────────────────
function showGateInfo(type){
    var tt=GATE_TRUTH[type];
    if(!tt) return;
    var isOne=type==='NOT';
    var html='<table class="tt"><tr>';
    if(!isOne){html+='<th>A</th><th>B</th>';}
    else{html+='<th>In</th>';}
    html+='<th>Out</th></tr>';
    tt.forEach(function(row){
        html+='<tr>';
        row.forEach(function(v,i){
            html+='<td class="'+(v?'one':'zero')+'">'+v+'</td>';
        });
        html+='</tr>';
    });
    html+='</table>';
    document.getElementById('truth-table-wrap').innerHTML=html;
    document.getElementById('gate-info').innerHTML=
        '<b style="color:'+GATE_COLORS[type]+'">'+type+'</b><br>'+
        '<span style="color:#94a3b8">'+getGateDesc(type)+'</span>';
    if(PQC_TIPS[type])
        document.getElementById('pqc-tip').textContent=PQC_TIPS[type];
}

function getGateDesc(type){
    var descs={
        AND:'Output is 1 ONLY when both inputs are 1. Like "A AND B must be true".',
        OR:'Output is 1 when AT LEAST ONE input is 1.',
        NOT:'Inverts the input. 0 becomes 1, 1 becomes 0.',
        XOR:'Output is 1 when inputs are DIFFERENT. Same inputs = 0.',
        NAND:'NOT AND — opposite of AND. Only 0 when both inputs are 1.',
        NOR:'NOT OR — only 1 when both inputs are 0.',
        INPUT:'Toggle between 0 and 1 by clicking.',
        OUTPUT:'Shows the final result of your circuit.',
    };
    return descs[type]||'';
}

function updateTruthDisplay(){
    var outputs=gates.filter(function(g){return g.type==='OUTPUT';});
    if(outputs.length>0){
        var html='<div style="font-size:9px;color:#94a3b8;margin-bottom:4px">Circuit Output:</div>';
        outputs.forEach(function(o,i){
            html+='<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px">'+
                '<span style="font-size:14px">'+(o.value?'💡':'⬛')+'</span>'+
                '<span style="font-size:11px;font-weight:700;color:'+(o.value?'#10b981':'#ef4444')+'">'+
                'OUT'+(outputs.length>1?i:'')+(o.value!==null?'='+o.value:'=?')+'</span></div>';
        });
        document.getElementById('truth-table-wrap').innerHTML=html;
    }
}

// ── CHALLENGES ────────────────────────────────────────────────────────────────
var challenges=[
    {
        title:'🎯 Challenge 1: AND Gate Circuit',
        desc:'Place 2 INPUT nodes, connect them to AND gate, connect AND to OUTPUT. Toggle inputs and see it work!',
        check:function(){
            var hasAND=gates.find(function(g){return g.type==='AND';});
            var inputs=gates.filter(function(g){return g.type==='INPUT';});
            var output=gates.find(function(g){return g.type==='OUTPUT';});
            var andWires=hasAND?wires.filter(function(w){return w.toId===hasAND.id;}):[];
            var outWire=hasAND&&output?wires.find(function(w){return w.fromId===hasAND.id&&w.toId===output.id;}):null;
            return hasAND&&inputs.length>=2&&output&&andWires.length>=2&&outWire;
        },progress:function(){
            var p=0;
            if(gates.find(function(g){return g.type==='INPUT';})) p+=25;
            if(gates.filter(function(g){return g.type==='INPUT';}).length>=2) p+=25;
            if(gates.find(function(g){return g.type==='AND';})) p+=25;
            if(gates.find(function(g){return g.type==='OUTPUT';})) p+=25;
            return p;
        }
    },
    {
        title:'🎯 Challenge 2: XOR Circuit (Half Adder)',
        desc:'Build a Half Adder: connect 2 inputs to BOTH an AND gate and XOR gate. Two outputs = Sum and Carry!',
        check:function(){
            var hasXOR=gates.find(function(g){return g.type==='XOR';});
            var hasAND=gates.find(function(g){return g.type==='AND';});
            var outputs=gates.filter(function(g){return g.type==='OUTPUT';});
            return hasXOR&&hasAND&&outputs.length>=2;
        },progress:function(){
            var p=0;
            if(gates.find(function(g){return g.type==='XOR';})) p+=33;
            if(gates.find(function(g){return g.type==='AND';})) p+=33;
            if(gates.filter(function(g){return g.type==='OUTPUT';}).length>=2) p+=34;
            return p;
        }
    },
    {
        title:'🎯 Challenge 3: NOT + XOR = XNOR',
        desc:'Build an XNOR gate from XOR + NOT! Connect XOR output through a NOT gate to get "same inputs = 1".',
        check:function(){
            var hasXOR=gates.find(function(g){return g.type==='XOR';});
            var hasNOT=gates.find(function(g){return g.type==='NOT';});
            var notWire=hasXOR&&hasNOT?wires.find(function(w){return w.fromId===hasXOR.id&&w.toId===hasNOT.id;}):null;
            return hasXOR&&hasNOT&&notWire;
        },progress:function(){
            var p=0;
            if(gates.find(function(g){return g.type==='XOR';})) p+=33;
            if(gates.find(function(g){return g.type==='NOT';})) p+=33;
            var xorG=gates.find(function(g){return g.type==='XOR';});
            var notG=gates.find(function(g){return g.type==='NOT';});
            if(xorG&&notG&&wires.find(function(w){return w.fromId===xorG.id&&w.toId===notG.id;})) p+=34;
            return p;
        }
    },
    {
        title:'🎯 Challenge 4: NAND Universal Gate',
        desc:'Build an AND gate using ONLY NAND gates! NAND is universal — any logic can be made from it. Hint: NAND+NAND = AND!',
        check:function(){
            return gates.filter(function(g){return g.type==='NAND';}).length>=2&&
                   gates.find(function(g){return g.type==='OUTPUT';});
        },progress:function(){
            var n=gates.filter(function(g){return g.type==='NAND';}).length;
            return Math.min(100,n*50);
        }
    },
    {
        title:'🏆 Challenge 5: SHA-3 Mini — XOR Chain',
        desc:'XOR is the heart of SHA-3 (used in SPHINCS+ FIPS 205)! Build a chain: Input→XOR→XOR→Output. This is how hash rounds work!',
        check:function(){
            return gates.filter(function(g){return g.type==='XOR';}).length>=2&&
                   wires.filter(function(w){
                       var from=gates.find(function(g){return g.id===w.fromId;});
                       var to=gates.find(function(g){return g.id===w.toId;});
                       return from&&to&&from.type==='XOR'&&to.type==='XOR';
                   }).length>=1;
        },progress:function(){
            var n=gates.filter(function(g){return g.type==='XOR';}).length;
            var chained=wires.filter(function(w){
                var f=gates.find(function(g){return g.id===w.fromId;});
                var t=gates.find(function(g){return g.id===w.toId;});
                return f&&t&&f.type==='XOR'&&t.type==='XOR';
            }).length;
            return Math.min(100,n*30+chained*40);
        }
    },
];

function checkChallenge(){
    if(currentChallenge>=challenges.length) return;
    var ch=challenges[currentChallenge];
    var prog=ch.progress();
    document.getElementById('ch-fill').style.width=prog+'%';
    if(ch.check()){
        document.getElementById('ch-fill').style.width='100%';
        confetti();
        score+=100;xp+=50;updateScore();
        setMsg('🏆 Challenge '+( currentChallenge+1)+' COMPLETE! +100 pts, +50 XP!');
        setTimeout(function(){
            currentChallenge++;
            if(currentChallenge<challenges.length){
                var nc=challenges[currentChallenge];
                document.getElementById('ch-title').textContent=nc.title;
                document.getElementById('ch-desc').textContent=nc.desc;
                document.getElementById('ch-fill').style.width='0%';
            } else {
                document.getElementById('ch-title').textContent='🎓 ALL CHALLENGES COMPLETE!';
                document.getElementById('ch-desc').textContent='You mastered logic gates! These are the building blocks of SHA-3, AES, and all PQC algorithms. You understand cryptography at the hardware level!';
            }
        },2000);
    }
}

function loadChallenge(idx){
    if(idx>=challenges.length) return;
    var ch=challenges[idx];
    setMsg('💡 HINT: '+ch.desc);
}

// ── CONTROLS ──────────────────────────────────────────────────────────────────
function setMode(m){
    mode=m;
    if(m==='wire') wireStart=null;
    document.querySelectorAll('.mode-btn').forEach(function(b){b.classList.remove('active');});
    var labels={'build':'🏗 Build','wire':'🔌 Wire','delete':'🗑 Delete'};
    document.querySelectorAll('.mode-btn').forEach(function(b){
        if(b.textContent.trim()===labels[m]) b.classList.add('active');
    });
    setMsg(m==='build'?'Build mode: Click canvas to place selected gate, drag to move':
           m==='wire'?'Wire mode: Click output port (green) then input port (blue)':
           'Delete mode: Click any gate or wire to remove it');
}

function clearAll(){
    gates=[];wires=[];simulate();
    document.getElementById('ch-fill').style.width='0%';
    setMsg('Canvas cleared! Place gates to start building.');
}

function updateScore(){
    document.getElementById('score-val').textContent=score;
    document.getElementById('xp-val').textContent=xp;
    document.getElementById('gate-count').textContent=gates.length;
}

function setMsg(m){document.getElementById('msg-bar').textContent=m;}

function confetti(){
    var cols=['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444','#f97316'];
    for(var i=0;i<25;i++){setTimeout(function(){
        var el=document.createElement('div');el.className='cp';
        el.style.left=Math.random()*100+'vw';
        el.style.background=cols[Math.floor(Math.random()*cols.length)];
        el.style.animationDuration=(1+Math.random()*2)+'s';
        document.body.appendChild(el);setTimeout(function(){el.remove();},3000);
    },i*40);}
}

// ── LOOP ──────────────────────────────────────────────────────────────────────
function loop(){requestAnimationFrame(loop);draw();}
loop();
showGateInfo('AND');
setMsg('Welcome! Select BUILD mode, pick a gate from the left panel, and click the canvas to place it!');
</script>
</body>
</html>
""", height=700)
