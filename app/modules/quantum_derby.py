def render_quantum_derby():
    """Middle School: Quantum Derby."""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("\U0001F3C7 Quantum Derby \u2014 Bet on the Winner!")
    st.markdown("\U0001FA99 **100 coins, 6 races per season.** Each race lists its **odds** \u2014 long shots pay more! Win 3 in a row for a **streak bonus**. New races every season.")
    components.html(r"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0b1526;font-family:'Segoe UI',sans-serif;color:#e2e8f0;padding:10px}
.wrap{max-width:600px;margin:0 auto}
.hud{display:flex;justify-content:space-between;align-items:center;margin-bottom:9px;gap:6px}
.coins{background:#1a1500;border:2px solid #fbbf24;border-radius:10px;padding:5px 14px;font-weight:800;color:#fbbf24;font-size:16px}
.rd{color:#94a3b8;font-size:12px;font-weight:700}
.streak{background:#2d1500;border:1px solid #f97316;border-radius:9px;padding:3px 10px;color:#fb923c;font-size:11.5px;font-weight:800}
.card{background:#111c30;border:1px solid #334155;border-radius:12px;padding:13px;margin-bottom:9px}
.pname{color:#a5b4fc;font-weight:800;font-size:15.5px;margin-bottom:9px;text-align:center}
.vs{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center}
.side{background:#1e293b;border-radius:9px;padding:9px;text-align:center;font-size:12px}
.side b{display:block;font-size:13px;margin-top:3px}
.lbl{color:#64748b;font-size:10px;font-weight:800}
.vsx{color:#475569;font-size:17px;font-weight:800}
.odds{text-align:center;margin:9px 0 4px;font-size:12px;color:#fbbf24;font-weight:700}
.bets{display:flex;gap:5px;justify-content:center;margin:7px 0}
.chip{padding:6px 13px;border-radius:15px;border:2px solid #475569;background:#1e293b;color:#e2e8f0;cursor:pointer;font-weight:800;font-size:12.5px}
.chip.on{border-color:#fbbf24;background:#1a1500;color:#fbbf24}
.picks{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px;margin-top:5px}
.pick{padding:11px 3px;border-radius:10px;border:2px solid #475569;background:#1e293b;color:#e2e8f0;cursor:pointer;font-weight:800;font-size:12.5px;line-height:1.3}
.pick:hover{border-color:#a5b4fc}
.po{display:block;font-size:10px;color:#fbbf24;margin-top:2px}
canvas{display:block;margin:0 auto;border-radius:12px;background:#08101f}
.banner{text-align:center;font-weight:800;font-size:15px;padding:9px;border-radius:10px;margin:8px 0;display:none}
.win{background:#05301f;color:#34d399;border:1px solid #10b981}
.lose{background:#2d0a0a;color:#f87171;border:1px solid #ef4444}
.why,.pqcb{border-radius:7px;padding:9px 12px;font-size:12.5px;line-height:1.5;margin:6px 0;display:none}
.why{background:#0c1a30;border-left:3px solid #60a5fa}
.nextb{display:none;width:100%;padding:12px;border:none;border-radius:10px;background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;font-weight:800;font-size:14px;cursor:pointer}
#final{display:none;text-align:center;padding:16px}
#final h2{color:#fbbf24;margin-bottom:6px}
.bigc{font-size:40px;font-weight:800;color:#fbbf24}
.vd{font-size:15px;font-weight:700;margin:7px 0 12px}
.rec{background:#111c30;border:1px solid #334155;border-radius:10px;padding:13px;text-align:left;font-size:12.5px;line-height:1.9;margin-bottom:11px}
</style></head><body><div class="wrap">
<div class="hud"><div class="coins">&#129689; <span id="coins">100</span></div>
<div class="streak" id="streakbox" style="display:none">&#128293; <span id="streak">0</span> in a row</div>
<div class="rd" id="rd"></div></div>
<div class="card" id="betcard">
<div class="pname" id="pname"></div>
<div class="vs"><div class="side"><span class="lbl">&#128421;&#65039; CLASSICAL</span><b id="pcl"></b></div>
<div class="vsx">VS</div><div class="side"><span class="lbl">&#9883;&#65039; QUANTUM</span><b id="pqu"></b></div></div>
<div class="odds" id="oddsline"></div>
<div style="text-align:center;color:#94a3b8;font-size:11px">Wager:</div>
<div class="bets"><button class="chip" onclick="setBet(10,this)">10</button>
<button class="chip on" onclick="setBet(25,this)">25</button>
<button class="chip" onclick="setBet(50,this)">50</button>
<button class="chip" onclick="setBet(-1,this)">ALL IN</button></div>
<div class="picks"><button class="pick" onclick="lock('classical_safe')">&#128421;&#65039; Classical<span class="po" id="oc"></span></button>
<button class="pick" onclick="lock('quantum')">&#9883;&#65039; Quantum<span class="po" id="oq"></span></button>
<button class="pick" onclick="lock('tie')">&#129309; Tie<span class="po" id="ot"></span></button></div></div>
<canvas id="track" width="576" height="210"></canvas>
<div class="banner" id="banner"></div><div class="why" id="why"></div><div class="pqcb" id="pqcbox"></div>
<button class="nextb" id="nextb" onclick="nextRace()">Next Race &#8594;</button>
<div id="final" class="card"></div></div><script>
var ALL=[{"n": "\ud83d\udd22 Factor RSA-2048", "c": "\ud83d\udc22 Millions of YEARS", "q": "\u26a1 Just HOURS", "w": "quantum", "o": 1.5, "why": "Shor's Algorithm finds prime factors exponentially faster.", "pqc": "\u274c RSA is BROKEN by quantum \u2014 that is why we need Kyber!", "col": "#ef4444"}, {"n": "\ud83c\udfd7\ufe0f Solve Lattice SVP", "c": "\ud83d\udc22 Super hard", "q": "\ud83d\udc22 STILL super hard!", "w": "tie", "o": 3.0, "why": "No quantum algorithm gives a big speedup on lattice problems.", "pqc": "\u2705 Kyber is SAFE \u2014 quantum cannot shortcut lattices!", "col": "#10b981"}, {"n": "\ud83d\udd0d Search Unsorted Data", "c": "\ud83d\udc22 Check ALL N items", "q": "\u26a1 Only \u221aN steps", "w": "quantum", "o": 1.5, "why": "Grover's Algorithm gives a quadratic speedup on search.", "pqc": "\u26a0\ufe0f SHA-3 still safe \u2014 just use 256-bit output!", "col": "#f59e0b"}, {"n": "\ud83c\udf00 Break SHA3-256", "c": "\ud83d\udc22 2^256 tries", "q": "\u26a1 2^128 tries", "w": "classical_safe", "o": 2.5, "why": "Grover only square-roots the work \u2014 2^128 is still impossible.", "pqc": "\u2705 SHA-3 is SAFE \u2014 double the output beats Grover!", "col": "#10b981"}, {"n": "\ud83d\udd11 Break ECC P-256", "c": "\ud83d\udc22 Billions of years", "q": "\u26a1 Hours with Shor", "w": "quantum", "o": 1.4, "why": "Elliptic curves fall to Shor just like RSA does.", "pqc": "\u274c ECC is BROKEN too \u2014 curves are not safer!", "col": "#ef4444"}, {"n": "\ud83d\udd10 Break AES-256", "c": "\ud83d\udc22 2^256 keys", "q": "\ud83d\udc22 2^128 keys", "w": "classical_safe", "o": 2.5, "why": "Grover halves the effective key size, but 2^128 is still unreachable.", "pqc": "\u2705 AES-256 survives \u2014 no migration needed!", "col": "#10b981"}, {"n": "\ud83e\uddee Add Two Numbers", "c": "\u26a1 Instant", "q": "\ud83d\udc22 Slower!", "w": "classical_safe", "o": 2.0, "why": "Quantum computers are terrible at ordinary arithmetic.", "pqc": "\ud83d\udca1 Quantum is a specialist tool, not a faster laptop.", "col": "#3b82f6"}, {"n": "\u269b\ufe0f Simulate a Molecule", "c": "\ud83d\udc22 Impossible at scale", "q": "\u26a1 Natural fit", "w": "quantum", "o": 1.6, "why": "Nature is quantum, so quantum computers model it directly.", "pqc": "\ud83d\udca1 The BEST use of quantum \u2014 medicine and materials!", "col": "#8b5cf6"}, {"n": "\ud83c\udfb2 True Random Numbers", "c": "\ud83d\udc22 Only pseudo-random", "q": "\u26a1 Truly random", "w": "quantum", "o": 1.7, "why": "Quantum measurement is fundamentally unpredictable.", "pqc": "\u2705 Quantum RNG makes stronger encryption keys!", "col": "#8b5cf6"}, {"n": "\ud83d\udcc1 Store a Big File", "c": "\u26a1 Easy, cheap", "q": "\ud83d\udc22 Terrible at it", "w": "classical_safe", "o": 2.0, "why": "Qubits are fragile and lose their state.", "pqc": "\ud83d\udca1 Quantum computes; it does not store.", "col": "#3b82f6"}, {"n": "\ud83e\udde9 Solve NTRU Lattice", "c": "\ud83d\udc22 Very hard", "q": "\ud83d\udc22 Still very hard", "w": "tie", "o": 3.0, "why": "NTRU is another lattice family with no quantum shortcut.", "pqc": "\u2705 Lattice math holds up across the family!", "col": "#10b981"}, {"n": "\ud83c\udf32 Forge a Hash Signature", "c": "\ud83d\udc22 2^128 work", "q": "\ud83d\udc22 2^64 work", "w": "classical_safe", "o": 2.5, "why": "Hash signatures only lose the square root to Grover.", "pqc": "\u2705 SPHINCS+ stays safe with bigger hashes!", "col": "#10b981"}, {"n": "\ud83c\udf10 Break TLS Handshake", "c": "\ud83d\udc22 Not feasible", "q": "\u26a1 Broken by Shor", "w": "quantum", "o": 1.4, "why": "The handshake key exchange is what Shor destroys.", "pqc": "\u274c Why browsers switched to hybrid ML-KEM!", "col": "#ef4444"}, {"n": "\ud83c\udfaf Guess a 20-char Password", "c": "\ud83d\udc22 Basically forever", "q": "\ud83d\udc22 Also forever", "w": "tie", "o": 2.8, "why": "Grover helps a little, but a long password still wins.", "pqc": "\ud83d\udca1 Length beats quantum too!", "col": "#10b981"}, {"n": "\ud83d\udcca Sort a Million Records", "c": "\u26a1 Fast and cheap", "q": "\ud83d\udc22 No advantage", "w": "classical_safe", "o": 2.2, "why": "Sorting has no quantum speedup worth the overhead.", "pqc": "\ud83d\udca1 Classical computers are not going anywhere.", "col": "#3b82f6"}, {"n": "\ud83d\udddd\ufe0f Break Diffie-Hellman", "c": "\ud83d\udc22 Very hard", "q": "\u26a1 Shor breaks it", "w": "quantum", "o": 1.4, "why": "Discrete logs fall to Shor, same as factoring.", "pqc": "\u274c Another classic broken!", "col": "#ef4444"}, {"n": "\ud83e\udde0 Train an AI Model", "c": "\u26a1 Works today", "q": "\ud83e\udd14 Maybe someday", "w": "classical_safe", "o": 2.3, "why": "Quantum machine learning is promising but not practical yet.", "pqc": "\ud83d\udca1 Do not believe every quantum headline!", "col": "#3b82f6"}, {"n": "\ud83d\udd13 Crack ML-KEM (Kyber)", "c": "\ud83d\udc22 No known way", "q": "\ud83d\udc22 No known way", "w": "tie", "o": 3.2, "why": "Neither classical nor quantum has a shortcut.", "pqc": "\u2705 This is the point \u2014 Kyber is the future!", "col": "#10b981"}];var POOL=[],r=0,coins=100,bet=25,phase="bet",streak=0,called=0,RP=6;
var cv=document.getElementById("track"),cx=cv.getContext("2d");
function el(i){return document.getElementById(i)}
function sh(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}return a}
function init(){POOL=sh(ALL.slice()).slice(0,RP);r=0;coins=100;streak=0;called=0;phase="bet";show()}
function cur(){return POOL[r]}
function show(){var c=cur();el("coins").textContent=coins;el("rd").textContent="Race "+(r+1)+" of "+RP;
el("pname").textContent=c.n;el("pcl").textContent=c.c;el("pqu").textContent=c.q;
el("oddsline").innerHTML="&#127942; Correct pick pays <b>"+c.o.toFixed(1)+"x</b> your wager";
var p=c.o.toFixed(1)+"x";el("oc").textContent=p;el("oq").textContent=p;el("ot").textContent=p;
el("betcard").style.display="block";["banner","why","pqcbox","nextb"].forEach(function(i){el(i).style.display="none"});
el("streakbox").style.display=streak>1?"block":"none";el("streak").textContent=streak;draw(0,0,"")}
function setBet(v,b){var cs=document.querySelectorAll(".chip");for(var i=0;i<cs.length;i++)cs[i].classList.remove("on");
b.classList.add("on");bet=(v===-1)?coins:Math.min(v,coins)}
function lock(pk){if(phase!=="bet")return;bet=Math.min(bet,coins);if(bet<1)bet=Math.min(10,coins);
phase="race";el("betcard").style.display="none";var w=cur().w,t0=performance.now();
requestAnimationFrame(function f(now){var t=Math.min(1,(now-t0)/3400),pc,pq;
var s=function(x){return x<0.42?x*0.72:0.30+(x-0.42)*1.28},fd=function(x){return x<0.42?x*0.70:0.29+(x-0.42)*0.52},ev=function(x){return x*0.94};
if(w==="quantum"){pq=s(t);pc=fd(t)}else if(w==="classical_safe"){pc=s(t);pq=fd(t)}
else{pc=ev(t)+Math.sin(t*16)*0.014;pq=ev(t)-Math.sin(t*16)*0.014}
draw(pc,pq,t<1?"":w);if(t<1)requestAnimationFrame(f);else settle(pk,w)})}
function draw(pc,pq,win){var W=cv.width,H=cv.height;cx.clearRect(0,0,W,H);
cx.fillStyle="#08101f";cx.fillRect(0,0,W,H);cx.globalAlpha=.45;cx.font="14px serif";
var cr=["\uD83C\uDF89","\uD83D\uDC40","\uD83D\uDE4C","\u2B50","\uD83C\uDFC1"];
for(var i=0;i<14;i++)cx.fillText(cr[i%5],14+i*41,20);cx.globalAlpha=1;
cx.fillStyle="#0e1a2e";cx.fillRect(10,42,W-20,58);cx.fillRect(10,116,W-20,58);
cx.strokeStyle="#1e3050";cx.setLineDash([9,9]);cx.lineWidth=2;
cx.beginPath();cx.moveTo(10,110);cx.lineTo(W-10,110);cx.stroke();cx.setLineDash([]);
for(var y=38;y<H-14;y+=13){cx.fillStyle=(Math.floor(y/13)%2)?"#e2e8f0":"#475569";cx.fillRect(W-32,y,9,13)}
var ln=function(y,p,em,lb,col){var x=22+p*(W-88);cx.font="10.5px sans-serif";cx.fillStyle=col;cx.fillText(lb,14,y-24);
if(p>0.02&&p<0.96){cx.globalAlpha=.4;cx.font="13px serif";cx.fillText("\uD83D\uDCA8",x-19,y+7);cx.globalAlpha=1}
cx.font="31px serif";cx.fillText(em,x,y+11+Math.sin(performance.now()/85+y)*2.5)};
ln(76,pc,"\uD83D\uDDA5\uFE0F","CLASSICAL","#60a5fa");ln(150,pq,"\u269B\uFE0F","QUANTUM","#c084fc");
if(win){cx.font="bold 15px sans-serif";cx.fillStyle="#fbbf24";cx.textAlign="center";
cx.fillText(win==="tie"?"\uD83D\uDCF8 PHOTO FINISH \u2014 TIE!":(win==="quantum"?"\u269B\uFE0F QUANTUM WINS!":"\uD83D\uDDA5\uFE0F CLASSICAL HOLDS!"),W/2,H-8);cx.textAlign="left"}}
function settle(pk,w){phase="reveal";var c=cur(),ok=pk===w;
var pay=ok?Math.round(bet*c.o*(streak>=2?1.5:1)):-bet;coins=Math.max(0,coins+pay);
if(ok){called++;streak++}else{streak=0}if(coins===0)coins=25;
el("coins").textContent=coins;el("streakbox").style.display=streak>1?"block":"none";el("streak").textContent=streak;
var b=el("banner");b.className="banner "+(ok?"win":"lose");b.style.display="block";
b.innerHTML=ok?("\uD83C\uDFAF Called it! +"+pay+(streak>=3?" \uD83D\uDD25 STREAK BONUS!":"")):("\uD83D\uDE2E Wrong \u2014 lost "+bet+(coins===25?" The bank spots you 25!":""));
var wy=el("why");wy.style.display="block";wy.innerHTML="\uD83D\uDCA1 <b>Why:</b> "+c.why;
var pb=el("pqcbox");pb.style.display="block";pb.style.background=c.col+"20";pb.style.borderLeft="3px solid "+c.col;
pb.innerHTML="\uD83D\uDD10 <b>PQC Impact:</b> "+c.pqc;
var nb=el("nextb");nb.style.display="block";nb.textContent=r<RP-1?"Next Race \u2192":"\uD83C\uDFC6 Final Results!"}
function nextRace(){if(r<RP-1){r++;phase="bet";show();window.scrollTo(0,0)}
else{["betcard","banner","why","pqcbox","nextb"].forEach(function(i){el(i).style.display="none"});
cv.style.display="none";var f=el("final");f.style.display="block";
var v=coins>=400?"\uD83C\uDFC6 QUANTUM ORACLE!":coins>=200?"\uD83E\uDD48 Sharp bettor!":coins>=100?"\uD83E\uDD49 Broke even \u2014 run it back!":"\uD83D\uDCDA Quantum does NOT win everything!";
f.innerHTML="<h2>\uD83C\uDFC1 Season Complete!</h2><div class='bigc'>\uD83E\uDE99 "+coins+"</div><div class='vd'>"+v+
"</div><div style='color:#94a3b8;font-size:12.5px;margin-bottom:10px'>Correct: "+called+" / "+RP+"</div>"+
"<div class='rec'><b>The big idea:</b><br>\u26A1 Quantum CRUSHES factoring \u2014 RSA, ECC, DH all fall<br>"+
"\uD83D\uDEE1\uFE0F Quantum barely dents AES-256 and SHA-3<br>"+
"\uD83E\uDD1D Quantum has NO shortcut for lattices \u2014 Kyber wins<br>"+
"\uD83D\uDCA1 Quantum is a specialist tool, not a faster computer</div>"+
"<button class='nextb' style='display:block' onclick='again()'>\uD83D\uDD04 New Season</button>"}}
function again(){el("final").style.display="none";cv.style.display="block";init()}
init();
</script></body></html>""", height=760, scrolling=True)
