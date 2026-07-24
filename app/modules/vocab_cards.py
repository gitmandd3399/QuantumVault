def render_vocab_cards():
    """Clean filterable vocab study interface drawn from the shared PQC bank."""
    import json
    import streamlit as st
    import streamlit.components.v1 as components
    from modules.pqc_vocab import VOCAB_BANK

    COLORS = {"Basics": "#10b981", "Quantum": "#8b5cf6", "PQC": "#3b82f6",
              "Math": "#f59e0b", "Computers": "#06b6d4", "Threats": "#ef4444",
              "Defense": "#22c55e", "Signatures": "#a855f7"}
    cards = [{"w": w, "e": e, "s": s, "f": f, "x": x, "t": t, "c": c,
              "col": COLORS.get(c, "#6366f1")}
             for w, e, s, f, x, t, c in VOCAB_BANK]

    st.subheader("\U0001F4DD Secret Word Book")
    st.markdown(
        "**Tap a card to see what the word means!** Pick a level or topic to see fewer words at a time. "
        "Mark the ones you know to fill up your progress bar."
    )

    html = HTML_TEMPLATE.replace("__CARDS__", json.dumps(cards)) \
                        .replace("__CATS__", json.dumps(sorted(COLORS.keys())))
    components.html(html, height=690, scrolling=True)

    st.caption(
        "\U0001F4A1 These are the same words used in Word Search, Word Rescue, and the Crossword \u2014 "
        "practice here and you will spot them in the games!"
    )


HTML_TEMPLATE = """<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0b1526;font-family:'Segoe UI',sans-serif;color:#e2e8f0;padding:10px}
.wrap{max-width:600px;margin:0 auto}
.crow{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:7px;align-items:center}
.clab{font-size:10.5px;color:#64748b;font-weight:800;letter-spacing:.5px;min-width:50px}
.tb,.cb,.mb{padding:6px 12px;border-radius:15px;border:1.5px solid #475569;background:#1e293b;
color:#cbd5e1;font-size:12px;font-weight:700;cursor:pointer}
.tb:hover,.cb:hover,.mb:hover{border-color:#a5b4fc}
.tb.on,.mb.on{background:#312e81;border-color:#818cf8;color:#e0e7ff}
.cb.on{background:#1a1500;border-color:#fbbf24;color:#fbbf24}
.stats{display:flex;justify-content:space-between;font-size:12px;color:#94a3b8;margin:10px 0 5px}
.track{height:5px;background:#1e293b;border-radius:3px;overflow:hidden;margin-bottom:13px}
#bar{height:100%;background:linear-gradient(90deg,#10b981,#34d399);width:0;transition:width .3s}
.pos{font-size:11.5px;color:#64748b;margin-bottom:7px;display:flex;align-items:center;gap:7px}
.pill{padding:2px 9px;border-radius:10px;font-size:10.5px;font-weight:800;border:1px solid}
.pill.known{background:#05301f;color:#34d399;border-color:#10b98155}
.card{background:#111c30;border:2px solid #475569;border-radius:16px;padding:26px 22px;
min-height:225px;cursor:pointer;display:flex;align-items:center;justify-content:center}
.card:hover{transform:translateY(-2px)}
.side{width:100%;text-align:center}
.bigemoji{font-size:54px;line-height:1;margin-bottom:13px}
.word{font-size:29px;font-weight:800;letter-spacing:1px}
.tap{font-size:11.5px;color:#475569;margin-top:15px;font-style:italic}
.back{text-align:left}
.lab{font-size:10px;font-weight:800;color:#64748b;letter-spacing:1px;margin-bottom:5px}
.simple{font-size:17px;line-height:1.45;margin-bottom:15px}
.full{font-size:13px;line-height:1.5;color:#94a3b8;margin-bottom:13px}
.ex{background:#0c1a30;border-left:3px solid #60a5fa;border-radius:6px;padding:9px 12px;
font-size:12.5px;line-height:1.5;color:#bfdbfe;font-style:italic}
.nav{display:flex;gap:6px;margin-top:11px}
.nb{padding:11px 16px;border-radius:10px;border:1.5px solid #475569;background:#1e293b;
color:#e2e8f0;font-size:15px;font-weight:800;cursor:pointer}
.nb:hover{border-color:#a5b4fc}
.nb.wide{flex:1;font-size:13px}
.blist{display:flex;flex-direction:column;gap:4px;max-height:420px;overflow-y:auto}
.brow{display:flex;align-items:center;gap:9px;background:#111c30;border:1px solid #263449;
border-radius:9px;padding:9px 11px;cursor:pointer;text-align:left}
.brow:hover{background:#18243c}
.brow.bk{border-color:#10b98144}
.bem{font-size:18px;flex-shrink:0}
.bw{font-weight:800;font-size:12.5px;min-width:94px;flex-shrink:0}
.bs{font-size:11.5px;color:#94a3b8;flex:1;line-height:1.35}
.bdot{width:7px;height:7px;border-radius:50%;flex-shrink:0}
.empty{text-align:center;color:#64748b;padding:40px;font-size:14px}
</style></head><body><div class="wrap">
<div class="crow"><span class="clab">LEVEL</span>
<button class="tb on" onclick="setTier(0,this)">All</button>
<button class="tb" onclick="setTier(1,this)">&#127793; Easy</button>
<button class="tb" onclick="setTier(2,this)">&#127774; Medium</button>
<button class="tb" onclick="setTier(3,this)">&#128293; Tricky</button></div>
<div class="crow"><span class="clab">TOPIC</span><span id="cats"></span></div>
<div class="crow"><span class="clab">VIEW</span>
<button class="mb on" onclick="setMode('study',this)">&#127183; Flashcards</button>
<button class="mb" onclick="setMode('browse',this)">&#128203; Word list</button></div>
<div class="stats"><span id="count"></span><span id="known"></span></div>
<div class="track"><div id="bar"></div></div>
<div id="study"></div><div id="browse" style="display:none"></div>
</div><script>
var ALL=__CARDS__,CATS=__CATS__;
var tier=0,cat="",idx=0,flip=false,known={},mode="study";
function el(i){return document.getElementById(i)}
function filt(){return ALL.filter(function(c){
 if(tier&&c.t!==tier)return false;if(cat&&c.c!==cat)return false;return true})}
function setTier(t,b){tier=t;idx=0;flip=false;
 var x=document.querySelectorAll(".tb");for(var i=0;i<x.length;i++)x[i].classList.remove("on");
 b.classList.add("on");render()}
function setCat(c,b){cat=c;idx=0;flip=false;
 var x=document.querySelectorAll(".cb");for(var i=0;i<x.length;i++)x[i].classList.remove("on");
 b.classList.add("on");render()}
function setMode(m,b){mode=m;flip=false;
 var x=document.querySelectorAll(".mb");for(var i=0;i<x.length;i++)x[i].classList.remove("on");
 b.classList.add("on");render()}
function doFlip(){flip=!flip;render()}
function nx(){var f=filt();if(!f.length)return;idx=(idx+1)%f.length;flip=false;render()}
function pv(){var f=filt();if(!f.length)return;idx=(idx-1+f.length)%f.length;flip=false;render()}
function shuf(){var f=filt();if(!f.length)return;idx=Math.floor(Math.random()*f.length);flip=false;render()}
function mark(){var f=filt();if(!f.length)return;known[f[idx].w]=true;nx()}
function jump(w){var f=filt();for(var i=0;i<f.length;i++)if(f[i].w===w){idx=i;break}
 flip=false;mode="study";
 var x=document.querySelectorAll(".mb");for(var i=0;i<x.length;i++)x[i].classList.remove("on");
 x[0].classList.add("on");render()}
function render(){var f=filt();
 el("count").textContent=f.length+" word"+(f.length===1?"":"s");
 var nk=0;for(var i=0;i<f.length;i++)if(known[f[i].w])nk++;
 el("known").textContent=nk+" learned";
 el("bar").style.width=(f.length?nk/f.length*100:0)+"%";
 if(!f.length){el("study").innerHTML="<div class='empty'>No words match. Try another filter!</div>";
  el("browse").innerHTML="";return}
 el("study").style.display=mode==="study"?"block":"none";
 el("browse").style.display=mode==="browse"?"block":"none";
 if(mode==="study"){
  if(idx>=f.length)idx=0;
  var c=f[idx],kn=known[c.w];
  var body=flip?("<div class='side back'><div class='lab'>WHAT IT MEANS</div><div class='simple'>"+c.s+
   "</div><div class='lab'>THE FULL VERSION</div><div class='full'>"+c.f+"</div><div class='ex'>"+c.x+"</div></div>")
   :("<div class='side'><div class='bigemoji'>"+c.e+"</div><div class='word'>"+c.w+
   "</div><div class='tap'>tap the card to see what it means</div></div>");
  el("study").innerHTML="<div class='pos'>"+(idx+1)+" of "+f.length+
   "<span class='pill' style='background:"+c.col+"22;color:"+c.col+";border-color:"+c.col+"55'>"+c.c+"</span>"+
   (kn?"<span class='pill known'>&#10003; learned</span>":"")+"</div>"+
   "<div class='card' style='border-color:"+c.col+"' onclick='doFlip()'>"+body+"</div>"+
   "<div class='nav'><button class='nb' onclick='pv()'>&#8592;</button>"+
   "<button class='nb wide' onclick='mark()'>&#10003; I know this one</button>"+
   "<button class='nb' onclick='shuf()'>&#127922;</button>"+
   "<button class='nb' onclick='nx()'>&#8594;</button></div>";
 }else{
  var h="<div class='blist'>";
  for(var i=0;i<f.length;i++){var b=f[i];
   h+="<button class='brow"+(known[b.w]?" bk":"")+"' onclick=\"jump('"+b.w+"')\">"+
    "<span class='bem'>"+b.e+"</span><span class='bw'>"+b.w+"</span>"+
    "<span class='bs'>"+b.s+"</span><span class='bdot' style='background:"+b.col+"'></span></button>"}
  el("browse").innerHTML=h+"</div>";
 }}
function buildCats(){var h="<button class='cb on' onclick=\"setCat('',this)\">All topics</button>";
 for(var i=0;i<CATS.length;i++)h+="<button class='cb' onclick=\"setCat('"+CATS[i]+"',this)\">"+CATS[i]+"</button>";
 el("cats").innerHTML=h}
buildCats();render();
</script></body></html>"""
