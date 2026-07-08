def render_logic_gates():
    """Middle School: Logic Gate Builder."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("⚡ Logic Gate Lab — Build Circuits from Scratch!")
    st.markdown(
        "**Click to place gates, then wire them together!** "
        "AND, OR, XOR, NOT, NAND — the building blocks of ALL cryptography. "
        "Toggle inputs and watch the circuit come alive!"
    )

    components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;}
#app{display:flex;flex-direction:column;height:560px;}
#topbar{background:#071520;border-bottom:1px solid #1a3a5a;padding:6px 10px;
    display:flex;align-items:center;gap:8px;flex-shrink:0;}
.pill{background:#0a1f35;border:1px solid #1a3a5a;border-radius:20px;
    padding:3px 10px;font-size:10px;color:#60a5fa;}
.pill b{color:white;}
#mode-row{display:flex;gap:4px;margin-left:auto;}
.mbtn{padding:4px 10px;border-radius:6px;border:1px solid #1a3a5a;
    background:transparent;color:#60a5fa;font-size:10px;cursor:pointer;}
.mbtn.on{background:#1d4ed8;color:white;border-color:#3b82f6;}
#middle{display:flex;flex:1;overflow:hidden;}
#pal{width:110px;flex-shrink:0;background:#071520;border-right:1px solid #1a3a5a;
    padding:6px;overflow-y:auto;}
.pt{font-size:8px;font-weight:700;letter-spacing:1px;color:#475569;
    text-transform:uppercase;padding:4px 0;margin-bottom:4px;}
.gi{background:#0a1f35;border:1px solid #1a3a5a;border-radius:7px;
    padding:7px 5px;margin-bottom:5px;cursor:pointer;text-align:center;transition:all 0.15s;}
.gi:hover{transform:scale(1.04);border-color:#3b82f6;}
.gi.sel{border-color:#fbbf24;background:#1a1500;}
.gn{font-size:10px;font-weight:700;margin-bottom:1px;}
.gd{font-size:8px;color:#94a3b8;}
#cv-wrap{flex:1;position:relative;}
#cv{display:block;cursor:crosshair;}
#rp{width:150px;flex-shrink:0;background:#071520;border-left:1px solid #1a3a5a;
    padding:8px;overflow-y:auto;font-size:9px;}
.rt{font-size:8px;font-weight:700;letter-spacing:1px;color:#475569;
    text-transform:uppercase;margin-bottom:6px;}
.tt{width:100%;border-collapse:collapse;font-size:9px;margin-bottom:8px;}
.tt th{background:#0a1f35;padding:3px;text-align:center;color:#60a5fa;}
.tt td{padding:3px;text-align:center;border-bottom:1px solid #1a3a5a;}
.v1{color:#10b981;font-weight:700;} .v0{color:#475569;}
#chal{background:#071520;border-top:1px solid #1a3a5a;padding:6px 10px;flex-shrink:0;}
.ct{font-size:10px;font-weight:700;color:#60a5fa;margin-bottom:2px;}
.cd{font-size:9px;color:#94a3b8;}
.cp2{height:4px;background:#1e293b;border-radius:2px;margin-top:5px;}
.cpf{height:100%;border-radius:2px;background:#10b981;transition:width 0.4s;}
#msgbar{background:#071520;border-top:1px solid #1a3a5a;padding:5px 10px;
    font-size:10px;color:#60a5fa;flex-shrink:0;}
.confp{position:fixed;pointer-events:none;z-index:999;width:7px;height:7px;
    border-radius:2px;animation:cfanim linear forwards;}
@keyframes cfanim{0%{transform:translateY(-20px) rotate(0deg);opacity:1;}
    100%{transform:translateY(500px) rotate(720deg);opacity:0;}}
</style>
</head>
<body>
<div id="app">
<div id="topbar">
    <span style="font-size:11px;font-weight:700;color:#7c3aed">⚡ Logic Gate Lab</span>
    <div class="pill">⭐ <b id="sv">0</b></div>
    <div class="pill">Gates: <b id="gv">0</b></div>
    <div id="mode-row">
        <button class="mbtn on" id="mb-place" onclick="setMode('place')">🏗 Place</button>
        <button class="mbtn" id="mb-wire" onclick="setMode('wire')">🔌 Wire</button>
        <button class="mbtn" id="mb-del" onclick="setMode('del')">🗑 Del</button>
        <button class="mbtn" onclick="clearAll()" style="color:#ef4444">✕ Clear</button>
    </div>
</div>
<div id="middle">
<div id="pal">
    <div class="pt">Gates</div>
    <div class="gi sel" id="si-AND" onclick="selType('AND')">
        <div class="gn" style="color:#3b82f6">AND</div>
        <div class="gd">Both = 1</div>
    </div>
    <div class="gi" id="si-OR" onclick="selType('OR')">
        <div class="gn" style="color:#10b981">OR</div>
        <div class="gd">Either = 1</div>
    </div>
    <div class="gi" id="si-NOT" onclick="selType('NOT')">
        <div class="gn" style="color:#ef4444">NOT</div>
        <div class="gd">Flip 0↔1</div>
    </div>
    <div class="gi" id="si-XOR" onclick="selType('XOR')">
        <div class="gn" style="color:#fbbf24">XOR</div>
        <div class="gd">Different=1</div>
    </div>
    <div class="gi" id="si-NAND" onclick="selType('NAND')">
        <div class="gn" style="color:#8b5cf6">NAND</div>
        <div class="gd">NOT AND</div>
    </div>
    <div class="gi" id="si-NOR" onclick="selType('NOR')">
        <div class="gn" style="color:#f97316">NOR</div>
        <div class="gd">NOT OR</div>
    </div>
    <div class="pt" style="margin-top:6px">I/O</div>
    <div class="gi" id="si-IN" onclick="selType('IN')">
        <div class="gn" style="color:#94a3b8">INPUT</div>
        <div class="gd">Click=toggle</div>
    </div>
    <div class="gi" id="si-OUT" onclick="selType('OUT')">
        <div class="gn" style="color:#ca8a04">OUTPUT</div>
        <div class="gd">Shows result</div>
    </div>
</div>
<div id="cv-wrap"><canvas id="cv"></canvas></div>
<div id="rp">
    <div class="rt">Truth Table</div>
    <div id="tt-wrap"></div>
    <div class="rt" style="margin-top:8px">PQC Link</div>
    <div id="pqc-tip" style="color:#10b981;line-height:1.5">
        XOR is the core of SHA-3 — used in SPHINCS+ (FIPS 205)!
    </div>
</div>
</div>
<div id="chal">
    <div class="ct" id="ch-t">🎯 Challenge 1: Build an AND circuit</div>
    <div class="cd" id="ch-d">Place 2 INPUTs → AND gate → OUTPUT. Wire them in Wire mode!</div>
    <div class="cp2"><div class="cpf" id="ch-p" style="width:0%"></div></div>
</div>
<div id="msgbar" id="msg">Click a gate type on the left, then click the canvas to place it!</div>
</div>

<script>
var cv=document.getElementById('cv'),ctx=cv.getContext('2d'),W=0,H=0;
function resize(){var r=document.getElementById('cv-wrap').getBoundingClientRect();W=cv.width=r.width;H=cv.height=r.height;}
resize();

var gates=[],wires=[],mode='place',selT='AND',wireFrom=null,score=0,nid=1,curCh=0;

var COLORS={AND:'#3b82f6',OR:'#10b981',NOT:'#ef4444',XOR:'#fbbf24',NAND:'#8b5cf6',NOR:'#f97316',IN:'#475569',OUT:'#ca8a04'};
var TIPS={AND:'AND gates appear in SHA-3 and AES cipher circuits!',OR:'OR logic builds multiplexers used in crypto hardware!',NOT:'NOT gates create complements — key to S-box in AES!',XOR:'XOR is THE crypto gate! SHA-3, AES, ML-KEM all use XOR!',NAND:'NAND is universal — build ANY circuit with just NAND!',NOR:'NOR is universal too — used in compact ASIC PQC chips!',IN:'Inputs = the bits of your key or plaintext!',OUT:'Output = the encrypted or hashed result!'};
var TT={AND:[[0,0,0],[0,1,0],[1,0,0],[1,1,1]],OR:[[0,0,0],[0,1,1],[1,0,1],[1,1,1]],NOT:[[0,1],[1,0]],XOR:[[0,0,0],[0,1,1],[1,0,1],[1,1,0]],NAND:[[0,0,1],[0,1,1],[1,0,1],[1,1,0]],NOR:[[0,0,1],[0,1,0],[1,0,0],[1,1,0]]};

var CHALS=[
    {t:'🎯 Challenge 1: AND Circuit',d:'Place 2 INPUTs + AND + OUTPUT, wire them up!',
     chk:function(){var a=gates.find(function(g){return g.t==='AND';}),i=gates.filter(function(g){return g.t==='IN';}),o=gates.find(function(g){return g.t==='OUT';});return a&&i.length>=2&&o&&wires.filter(function(w){return w.to===a.id;}).length>=2&&wires.find(function(w){return w.from===a.id&&w.to===o.id;});},
     prog:function(){var p=0;if(gates.find(function(g){return g.t==='IN';}))p+=25;if(gates.filter(function(g){return g.t==='IN';}).length>=2)p+=25;if(gates.find(function(g){return g.t==='AND';}))p+=25;if(gates.find(function(g){return g.t==='OUT';}))p+=25;return p;}},
    {t:'🎯 Challenge 2: Half Adder (XOR+AND)',d:'Connect 2 inputs to BOTH XOR and AND gates. Two outputs = Sum + Carry!',
     chk:function(){return gates.find(function(g){return g.t==='XOR';})&&gates.find(function(g){return g.t==='AND';})&&gates.filter(function(g){return g.t==='OUT';}).length>=2;},
     prog:function(){var p=0;if(gates.find(function(g){return g.t==='XOR';}))p+=34;if(gates.find(function(g){return g.t==='AND';}))p+=33;if(gates.filter(function(g){return g.t==='OUT';}).length>=2)p+=33;return p;}},
    {t:'🎯 Challenge 3: XOR → NOT = XNOR',d:'Chain XOR into NOT gate to build XNOR: same inputs = 1!',
     chk:function(){var x=gates.find(function(g){return g.t==='XOR';}),n=gates.find(function(g){return g.t==='NOT';});return x&&n&&wires.find(function(w){return w.from===x.id&&w.to===n.id;});},
     prog:function(){var p=0;if(gates.find(function(g){return g.t==='XOR';}))p+=33;if(gates.find(function(g){return g.t==='NOT';}))p+=34;var x=gates.find(function(g){return g.t==='XOR';}),n=gates.find(function(g){return g.t==='NOT';});if(x&&n&&wires.find(function(w){return w.from===x.id&&w.to===n.id;}))p+=33;return p;}},
    {t:'🏆 Challenge 4: SHA-3 XOR Chain',d:'XOR is the heart of SHA-3! Build: INPUT→XOR→XOR→OUTPUT to simulate a hash round.',
     chk:function(){var xs=gates.filter(function(g){return g.t==='XOR';});return xs.length>=2&&wires.find(function(w){var f=gates.find(function(g){return g.id===w.from;}),t=gates.find(function(g){return g.id===w.to;});return f&&t&&f.t==='XOR'&&t.t==='XOR';});},
     prog:function(){var n=gates.filter(function(g){return g.t==='XOR';}).length,c=wires.filter(function(w){var f=gates.find(function(g){return g.id===w.from;}),t=gates.find(function(g){return g.id===w.to;});return f&&t&&f.t==='XOR'&&t.t==='XOR';}).length;return Math.min(100,n*25+c*50);}},
];

function mkGate(t,x,y){return{id:nid++,t:t,x:x,y:y,w:t==='IN'||t==='OUT'?50:66,h:t==='IN'||t==='OUT'?36:46,v:t==='IN'?0:null};}
function outPt(g){return{x:g.x+g.w,y:g.y+g.h/2};}
function inPts(g){if(g.t==='IN'||g.t==='OUT')return [{x:g.x,y:g.y+g.h/2}];var n=g.t==='NOT'?1:2;var pts=[];for(var i=0;i<n;i++)pts.push({x:g.x,y:g.y+g.h*(i+1)/(n+1)});return pts;}
function gateAt(mx,my){for(var i=gates.length-1;i>=0;i--){var g=gates[i];if(mx>=g.x&&mx<=g.x+g.w&&my>=g.y&&my<=g.y+g.h)return g;}return null;}
function portAt(mx,my){var found=null;gates.forEach(function(g){if(g.t!=='IN'){var op=outPt(g);if(Math.hypot(mx-op.x,my-op.y)<10)found={g:g,k:'out'};}if(g.t!=='OUT'){inPts(g).forEach(function(p,i){if(Math.hypot(mx-p.x,my-p.y)<10)found={g:g,k:'in',i:i};});}});return found;}

cv.addEventListener('click',function(e){
    var r=cv.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
    if(mode==='place'){
        var g=gateAt(mx,my);
        if(g){if(g.t==='IN'){g.v=1-g.v;score+=2;sim();chk();return;}}
        var ng=mkGate(selT,mx-33,my-23);gates.push(ng);score+=5;sim();chk();
        document.getElementById('gv').textContent=gates.length;
        document.getElementById('sv').textContent=score;
    } else if(mode==='del'){
        var g2=gateAt(mx,my);
        if(g2){gates=gates.filter(function(x){return x.id!==g2.id;});wires=wires.filter(function(w){return w.from!==g2.id&&w.to!==g2.id;});sim();chk();}
    } else if(mode==='wire'){
        var p=portAt(mx,my);
        if(!p) return;
        if(!wireFrom){wireFrom=p;setMsg('Now click the destination port (triangle=input, circle=output)');}
        else{
            if(wireFrom.g.id!==p.g.id&&wireFrom.k!==p.k){
                var src=wireFrom.k==='out'?wireFrom:p,dst=wireFrom.k==='in'?wireFrom:p;
                if(src.k==='out'&&dst.k==='in'){
                    if(!wires.find(function(w){return w.from===src.g.id&&w.to===dst.g.id&&w.ti===dst.i;})){
                        wires.push({from:src.g.id,to:dst.g.id,ti:dst.i,on:false});
                        score+=10;document.getElementById('sv').textContent=score;
                        sim();chk();setMsg('Wire connected! Toggle INPUTs to test.');
                    }
                }
            }
            wireFrom=null;
        }
    }
});

var dragging=null,dox=0,doy=0;
cv.addEventListener('mousedown',function(e){if(mode!=='place')return;var r=cv.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;var g=gateAt(mx,my);if(g&&g.t!=='IN'){dragging=g;dox=mx-g.x;doy=my-g.y;}});
cv.addEventListener('mousemove',function(e){if(dragging){var r=cv.getBoundingClientRect();dragging.x=e.clientX-r.left-dox;dragging.y=e.clientY-r.top-doy;}});
cv.addEventListener('mouseup',function(){dragging=null;});

function sim(){
    var vals={};
    gates.forEach(function(g){if(g.t==='IN')vals[g.id]=g.v;});
    for(var p=0;p<12;p++){
        gates.forEach(function(g){
            if(g.t==='IN') return;
            var iw=wires.filter(function(w){return w.to===g.id;});
            if(g.t==='OUT'){var w=iw[0];if(w&&vals[w.from]!==undefined){g.v=vals[w.from];vals[g.id]=g.v;}}
            else if(g.t==='NOT'){var w=iw[0];if(w&&vals[w.from]!==undefined){g.v=vals[w.from]?0:1;vals[g.id]=g.v;}}
            else{var w0=iw.find(function(w){return w.ti===0;}),w1=iw.find(function(w){return w.ti===1;});
                if(w0&&w1&&vals[w0.from]!==undefined&&vals[w1.from]!==undefined){
                    var a=vals[w0.from],b=vals[w1.from],v=0;
                    if(g.t==='AND')v=a&b;else if(g.t==='OR')v=a|b;else if(g.t==='XOR')v=a^b;
                    else if(g.t==='NAND')v=(a&b)?0:1;else if(g.t==='NOR')v=(a|b)?0:1;
                    g.v=v;vals[g.id]=v;}}
        });
    }
    wires.forEach(function(w){w.on=vals[w.from]===1;});
}

function draw(){
    ctx.clearRect(0,0,W,H);ctx.fillStyle='#050a0f';ctx.fillRect(0,0,W,H);
    ctx.strokeStyle='#0a1f2e';ctx.lineWidth=0.4;
    for(var x2=0;x2<W;x2+=40){ctx.beginPath();ctx.moveTo(x2,0);ctx.lineTo(x2,H);ctx.stroke();}
    for(var y2=0;y2<H;y2+=40){ctx.beginPath();ctx.moveTo(0,y2);ctx.lineTo(W,y2);ctx.stroke();}
    // Wires
    wires.forEach(function(w){
        var f=gates.find(function(g){return g.id===w.from;}),t=gates.find(function(g){return g.id===w.to;});
        if(!f||!t)return;
        var sp=outPt(f),ep=inPts(t)[w.ti];if(!ep)return;
        var col=w.on?'#10b981':'#1e3a5a',mid=(sp.x+ep.x)/2;
        ctx.beginPath();ctx.moveTo(sp.x,sp.y);ctx.bezierCurveTo(mid,sp.y,mid,ep.y,ep.x,ep.y);
        ctx.strokeStyle=col;ctx.lineWidth=w.on?2.5:1.5;
        if(w.on){ctx.shadowColor='#10b981';ctx.shadowBlur=6;}
        ctx.stroke();ctx.shadowBlur=0;
        ctx.beginPath();ctx.arc(ep.x,ep.y,3,0,Math.PI*2);ctx.fillStyle=col;ctx.fill();
    });
    // Wire in progress
    if(wireFrom&&mode==='wire'){
        var pt=wireFrom.k==='out'?outPt(wireFrom.g):inPts(wireFrom.g)[wireFrom.i];
        if(pt){ctx.beginPath();ctx.arc(pt.x,pt.y,8,0,Math.PI*2);ctx.strokeStyle='#fbbf24';ctx.lineWidth=2;ctx.stroke();}
    }
    // Port dots in wire mode
    if(mode==='wire'){
        gates.forEach(function(g){
            if(g.t!=='IN'){inPts(g).forEach(function(p){ctx.beginPath();ctx.arc(p.x,p.y,5,0,Math.PI*2);ctx.fillStyle='#3b82f625';ctx.fill();ctx.strokeStyle='#3b82f6';ctx.lineWidth=1;ctx.stroke();});}
            if(g.t!=='OUT'){var op=outPt(g);ctx.beginPath();ctx.arc(op.x,op.y,5,0,Math.PI*2);ctx.fillStyle='#10b98125';ctx.fill();ctx.strokeStyle='#10b981';ctx.lineWidth=1;ctx.stroke();}
        });
    }
    // Gates
    gates.forEach(function(g){drawGate(g);});
}

function drawGate(g){
    var col=COLORS[g.t]||'#334155';
    if(g.v===1){ctx.shadowColor=col;ctx.shadowBlur=12;}
    ctx.fillStyle=col+'22';ctx.strokeStyle=col;ctx.lineWidth=2;
    if(g.t==='IN'){
        ctx.beginPath();if(ctx.roundRect)ctx.roundRect(g.x,g.y,g.w,g.h,7);else ctx.rect(g.x,g.y,g.w,g.h);
        ctx.fillStyle=g.v?col+'44':'#0a1f35';ctx.fill();ctx.strokeStyle=g.v?col:'#334155';ctx.stroke();
        ctx.font='bold 15px sans-serif';ctx.fillStyle=g.v?col:'#475569';ctx.textAlign='center';ctx.textBaseline='middle';
        ctx.fillText(g.v?'1':'0',g.x+g.w/2,g.y+g.h/2);
        ctx.font='7px sans-serif';ctx.fillStyle='#475569';ctx.fillText('INPUT',g.x+g.w/2,g.y+g.h-6);
        ctx.beginPath();ctx.arc(g.x+g.w,g.y+g.h/2,4,0,Math.PI*2);ctx.fillStyle=g.v?col:'#334155';ctx.fill();
    } else if(g.t==='OUT'){
        ctx.beginPath();if(ctx.roundRect)ctx.roundRect(g.x,g.y,g.w,g.h,7);else ctx.rect(g.x,g.y,g.w,g.h);
        ctx.fillStyle=g.v?col+'44':'#0a1f35';ctx.fill();ctx.strokeStyle=g.v?col:'#334155';ctx.stroke();
        ctx.font=g.v?'20px':'14px';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(g.v?'💡':'⬛',g.x+g.w/2,g.y+g.h/2-2);
        ctx.font='7px sans-serif';ctx.fillStyle='#475569';ctx.fillText(g.v!==null?String(g.v):'?',g.x+g.w/2,g.y+g.h-6);
        ctx.beginPath();ctx.arc(g.x,g.y+g.h/2,4,0,Math.PI*2);ctx.fillStyle='#334155';ctx.fill();
    } else {
        drawShape(g,col);
        ctx.font='bold 10px monospace';ctx.fillStyle='white';ctx.textAlign='center';ctx.textBaseline='middle';
        ctx.fillText(g.t,g.x+g.w/2,g.y+g.h/2);
        if(g.v!==null){ctx.beginPath();ctx.arc(g.x+g.w-7,g.y+7,7,0,Math.PI*2);ctx.fillStyle=g.v?'#10b981':'#ef4444';ctx.fill();ctx.font='bold 8px sans-serif';ctx.fillStyle='white';ctx.fillText(g.v,g.x+g.w-7,g.y+7);}
        inPts(g).forEach(function(p){ctx.beginPath();ctx.arc(p.x,p.y,3,0,Math.PI*2);ctx.fillStyle=col+'80';ctx.fill();});
        var op=outPt(g);ctx.beginPath();ctx.arc(op.x,op.y,3,0,Math.PI*2);ctx.fillStyle=col;ctx.fill();
    }
    ctx.shadowBlur=0;
}

function drawShape(g,col){
    var x=g.x,y=g.y,w=g.w,h=g.h;
    ctx.beginPath();
    if(g.t==='AND'||g.t==='NAND'){
        ctx.moveTo(x,y);ctx.lineTo(x+w*0.5,y);ctx.bezierCurveTo(x+w*1.1,y,x+w*1.1,y+h,x+w*0.5,y+h);ctx.lineTo(x,y+h);ctx.closePath();
        ctx.fillStyle=col+'22';ctx.fill();ctx.strokeStyle=col;ctx.stroke();
        if(g.t==='NAND'){ctx.beginPath();ctx.arc(x+w+5,y+h/2,5,0,Math.PI*2);ctx.stroke();}
    } else if(g.t==='OR'||g.t==='NOR'||g.t==='XOR'){
        ctx.moveTo(x,y);ctx.quadraticCurveTo(x+w*0.4,y+h/2,x,y+h);ctx.quadraticCurveTo(x+w*0.6,y+h,x+w,y+h/2);ctx.quadraticCurveTo(x+w*0.6,y,x,y);
        ctx.fillStyle=col+'22';ctx.fill();ctx.strokeStyle=col;ctx.stroke();
        if(g.t==='NOR'){ctx.beginPath();ctx.arc(x+w+5,y+h/2,5,0,Math.PI*2);ctx.stroke();}
        if(g.t==='XOR'){ctx.beginPath();ctx.moveTo(x-6,y);ctx.quadraticCurveTo(x-6+w*0.4,y+h/2,x-6,y+h);ctx.stroke();}
    } else if(g.t==='NOT'){
        ctx.moveTo(x,y);ctx.lineTo(x+w*0.8,y+h/2);ctx.lineTo(x,y+h);ctx.closePath();
        ctx.fillStyle=col+'22';ctx.fill();ctx.strokeStyle=col;ctx.stroke();
        ctx.beginPath();ctx.arc(x+w*0.9,y+h/2,w*0.1,0,Math.PI*2);ctx.stroke();
    }
}

function chk(){
    if(curCh>=CHALS.length)return;
    var ch=CHALS[curCh],prog=ch.prog();
    document.getElementById('ch-p').style.width=prog+'%';
    if(ch.chk()){
        confetti();score+=100;document.getElementById('sv').textContent=score;
        setMsg('🏆 Challenge '+(curCh+1)+' Complete! +100 pts!');
        setTimeout(function(){
            curCh++;
            if(curCh<CHALS.length){
                document.getElementById('ch-t').textContent=CHALS[curCh].t;
                document.getElementById('ch-d').textContent=CHALS[curCh].d;
                document.getElementById('ch-p').style.width='0%';
            } else {
                document.getElementById('ch-t').textContent='🎓 ALL DONE! You mastered logic gates!';
                document.getElementById('ch-d').textContent='These gates are the foundation of SHA-3, AES, and every PQC algorithm!';
            }
        },2000);
    }
}

function setMode(m){
    mode=m;wireFrom=null;
    ['place','wire','del'].forEach(function(x){document.getElementById('mb-'+x).classList.remove('on');});
    document.getElementById('mb-'+m).classList.add('on');
    setMsg(m==='place'?'Place mode: Click canvas to place gate, drag to move, click INPUT to toggle':m==='wire'?'Wire mode: Click output port (green) then input port (blue)':'Delete mode: Click any gate to remove it');
}

function selType(t){
    selT=t;
    document.querySelectorAll('.gi').forEach(function(el){el.classList.remove('sel');});
    document.getElementById('si-'+t).classList.add('sel');
    showTT(t);
    document.getElementById('pqc-tip').textContent=TIPS[t]||'';
}

function showTT(t){
    var data=TT[t];if(!data)return;
    var isOne=t==='NOT';
    var h='<table class="tt"><tr>';
    if(!isOne)h+='<th>A</th><th>B</th>';else h+='<th>In</th>';
    h+='<th>Out</th></tr>';
    data.forEach(function(row){h+='<tr>';row.forEach(function(v){h+='<td class="'+(v?'v1':'v0')+'">'+v+'</td>';});h+='</tr>';});
    h+='</table>';
    document.getElementById('tt-wrap').innerHTML=h;
}

function clearAll(){gates=[];wires=[];sim();document.getElementById('gv').textContent=0;setMsg('Cleared! Start building.');}
function setMsg(m){document.getElementById('msgbar').textContent=m;}

function confetti(){
    var c=['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444','#f97316'];
    for(var i=0;i<20;i++){setTimeout(function(){
        var el=document.createElement('div');el.className='confp';
        el.style.left=Math.random()*100+'vw';el.style.background=c[Math.floor(Math.random()*c.length)];
        el.style.animationDuration=(1+Math.random()*2)+'s';
        document.body.appendChild(el);setTimeout(function(){el.remove();},3000);
    },i*40);}
}

showTT('AND');
setMsg('Pick a gate from the left panel, then click the canvas to place it!');
function loop(){requestAnimationFrame(loop);draw();}
loop();
</script>
</body>
</html>
""", height=620)
