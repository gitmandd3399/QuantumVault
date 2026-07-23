def render_lock_puzzle():
    """Elementary: 8-level lock challenge."""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("\U0001F512 Agent Pixel's Lock Challenge!")
    st.markdown("\U0001F6A8 **The Quantum Monster is coming!** Pick the RIGHT lock for each vault. Read the clues \u2014 some locks look great but will not keep the secret safe. **8 vaults!**")
    components.html(r"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0b1526;font-family:'Segoe UI',sans-serif;color:#e2e8f0;padding:12px}
.wrap{max-width:560px;margin:0 auto}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
#lvnum{font-size:12px;color:#94a3b8;font-weight:800}
.sc{background:#1a1500;border:2px solid #fbbf24;border-radius:9px;padding:4px 13px;color:#fbbf24;font-weight:800;font-size:15px}
.track{height:7px;background:#1e293b;border-radius:4px;overflow:hidden;margin-bottom:14px}
#bar{height:100%;background:linear-gradient(90deg,#10b981,#34d399);width:0;transition:width .35s}
.vaultbox{background:#111c30;border:2px solid #334155;border-radius:14px;padding:16px;text-align:center;margin-bottom:12px}
#vault{font-size:48px}#vname{font-size:16px;font-weight:800;color:#a5b4fc;margin-top:4px}
#story{font-size:15px;line-height:1.5;margin-top:8px}
.pick{font-size:13px;color:#94a3b8;font-weight:800;margin-bottom:8px}
.lock{display:flex;align-items:center;gap:12px;width:100%;background:#1e293b;border:2px solid #475569;
border-radius:12px;padding:13px;margin-bottom:9px;color:#e2e8f0;cursor:pointer;text-align:left}
.lock:hover{border-color:#a5b4fc;background:#243044}
.le{font-size:30px;flex-shrink:0}.li{display:flex;flex-direction:column;gap:3px}
.li b{font-size:15px}.lc{font-size:12.5px;color:#94a3b8;line-height:1.4}
.lock.right{background:#05301f;border-color:#10b981}
.lock.wrong{background:#2d0a0a;border-color:#ef4444;opacity:.55}
.feed{display:none;border-radius:10px;padding:12px 14px;font-size:14px;line-height:1.5;margin-top:4px}
.feed.good{background:#05301f;border:1px solid #10b981;color:#34d399}
.feed.bad{background:#2d0a0a;border:1px solid #ef4444;color:#fca5a5}
.pts{background:#fbbf24;color:#1a1500;border-radius:9px;padding:1px 8px;font-size:12px;font-weight:800}
#nextb,.nb{display:none;width:100%;margin-top:11px;padding:13px;border:none;border-radius:11px;
background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;font-weight:800;font-size:15px;cursor:pointer}
.nb{display:block}.done{text-align:center;padding:24px 12px}
.trophy{font-size:60px}.done h2{color:#fbbf24;margin:6px 0}
.big{font-size:36px;font-weight:800;color:#fbbf24}.vd{font-size:15px;margin:8px 0 14px}
.recap{background:#111c30;border:1px solid #334155;border-radius:11px;padding:14px;text-align:left;font-size:13.5px;line-height:2}
.confp{position:fixed;top:-10px;width:9px;height:9px;border-radius:2px;pointer-events:none;animation:cf linear forwards;z-index:999}
@keyframes cf{to{transform:translateY(105vh) rotate(600deg);opacity:0}}
</style></head><body><div class="wrap">
<div class="top"><span id="lvnum"></span><span class="sc">&#11088; <span id="score">0</span></span></div>
<div class="track"><div id="bar"></div></div>
<div class="vaultbox"><div id="vault"></div><div id="vname"></div><div id="story"></div></div>
<div class="pick">&#128073; Pick the right lock:</div>
<div id="locks"></div><div id="feed" class="feed"></div>
<button id="nextb" onclick="next()">Next Level &#8594;</button>
</div><script>
var L = [{"n": 1, "vault": "\ud83d\udce6", "vname": "The Toy Box", "story": "Agent Pixel needs to lock her toy box. Which lock keeps it safe?", "locks": [{"e": "\ud83d\udd12", "name": "Strong Lock", "clue": "Thick metal. Nobody can break it!", "ok": true, "msg": "Yes! A strong lock keeps the toy box safe."}, {"e": "\ud83d\udd13", "name": "Broken Lock", "clue": "It has a big crack down the middle.", "ok": false, "msg": "Oh no! A cracked lock pops right open."}]}, {"n": 2, "vault": "\ud83c\udf6a", "vname": "The Cookie Jar", "story": "Someone keeps taking cookies! Pick a lock that really works.", "locks": [{"e": "\ud83e\uddfb", "name": "Paper Lock", "clue": "Made of paper. It looks nice!", "ok": false, "msg": "Paper tears! Pretty is not the same as safe."}, {"e": "\ud83d\udd12", "name": "Metal Lock", "clue": "Hard metal. Needs a real key.", "ok": true, "msg": "Great pick! Only someone with the key can open it."}]}, {"n": 3, "vault": "\ud83d\udcb0", "vname": "The Piggy Bank", "story": "Pixel's savings need protecting. One of these locks is old and tired.", "locks": [{"e": "\ud83d\udd12", "name": "Old Lock", "clue": "It worked GREAT for 40 whole years!", "ok": false, "msg": "Tricky! Working a long time does not mean it still works. A super-computer can pop this one open."}, {"e": "\ud83d\udd11", "name": "Super-Lock", "clue": "Brand new. Built from a giant dot puzzle nobody can solve.", "ok": true, "msg": "Yes! The dot puzzle is too hard even for a super-computer."}, {"e": "\ud83d\udd26", "name": "Light Lock", "clue": "It glows in the dark. So cool!", "ok": false, "msg": "Glowing is fun, but it does not keep secrets safe!"}]}, {"n": 4, "vault": "\ud83d\udce8", "vname": "The Secret Note", "story": "Pixel is sending a note to Byte. Which lock HIDES what it says?", "locks": [{"e": "\u270d\ufe0f", "name": "Name Lock", "clue": "It proves the note is really from Pixel.", "ok": false, "msg": "Close! That proves WHO sent it. It does not HIDE the words."}, {"e": "\ud83d\udd11", "name": "Hiding Lock", "clue": "It scrambles the words so nobody can read them.", "ok": true, "msg": "Perfect! Hiding the words is exactly the job here."}, {"e": "\ud83d\uddd1\ufe0f", "name": "Trash Lock", "clue": "It deletes the note forever.", "ok": false, "msg": "Then Byte gets nothing! Hide it, do not lose it."}]}, {"n": 5, "vault": "\ud83d\udcf1", "vname": "The Tablet", "story": "Real lock names now! Pixel's tablet needs the lock that SHARES secret keys safely.", "locks": [{"e": "\ud83d\udd11", "name": "KYBER", "clue": "Shares secret keys safely. Big-kid name: ML-KEM.", "ok": true, "msg": "Yes! Kyber (ML-KEM) shares keys. Scientists picked it in 2024."}, {"e": "\u270d\ufe0f", "name": "DILITHIUM", "clue": "Signs your name so people know it is you.", "ok": false, "msg": "Good lock, wrong job! Dilithium signs things."}, {"e": "\ud83d\udd12", "name": "RSA", "clue": "The old favorite. Everyone used it for years.", "ok": false, "msg": "RSA is the OLD lock. Super-computers can break it now."}]}, {"n": 6, "vault": "\ud83d\udcdc", "vname": "The Homework Proof", "story": "Pixel's teacher needs to know the homework is really hers and nobody changed it.", "locks": [{"e": "\ud83d\udd11", "name": "KYBER", "clue": "Shares secret keys safely.", "ok": false, "msg": "Kyber hides things. We need to PROVE who made it!"}, {"e": "\u270d\ufe0f", "name": "DILITHIUM", "clue": "Signs it so everyone knows it is from you. Big-kid name: ML-DSA.", "ok": true, "msg": "Yes! Dilithium (ML-DSA) signs it. Nobody can pretend to be Pixel."}, {"e": "\ud83d\udd04", "name": "SHUFFLE", "clue": "Mixes up all the letters.", "ok": false, "msg": "Now the teacher cannot read it either! Oops."}]}, {"n": 7, "vault": "\u231a", "vname": "The Smart Watch", "story": "A watch has a TINY computer inside. It needs a signature lock that fits in a small space.", "locks": [{"e": "\ud83c\udf32", "name": "SPHINCS+", "clue": "Super safe! But its signatures are really BIG.", "ok": false, "msg": "Very safe, but too big for a tiny watch. Size matters!"}, {"e": "\ud83e\udd85", "name": "FALCON", "clue": "Makes the tiniest signatures. Perfect for small gadgets.", "ok": true, "msg": "Yes! Small gadget, small lock."}, {"e": "\ud83d\udd11", "name": "KYBER", "clue": "Shares secret keys safely.", "ok": false, "msg": "Kyber shares keys. We needed a SIGNATURE."}]}, {"n": 8, "vault": "\ud83c\udfe5", "vname": "The Hospital Vault", "story": "FINAL MISSION! Doctor records must stay secret for a person's WHOLE LIFE.", "locks": [{"e": "\ud83d\udd12", "name": "RSA", "clue": "The old lock. Still used in lots of places!", "ok": false, "msg": "No! Records must stay secret 80 years. RSA will not last."}, {"e": "\ud83d\udd11", "name": "KYBER (biggest size)", "clue": "Shares keys safely, and this is the strongest size.", "ok": true, "msg": "PERFECT! Lifetime secrets need the strongest size. You are a real agent now!"}, {"e": "\ud83e\udd85", "name": "FALCON", "clue": "Tiny signatures for small gadgets.", "ok": false, "msg": "Falcon signs. A hospital must HIDE the records first."}, {"e": "\ud83d\udd26", "name": "Glow Lock", "clue": "It looks amazing!", "ok": false, "msg": "Looking cool never keeps secrets safe. You know better now!"}]}];
var idx=0,score=0,done={},tries=0;
function el(i){return document.getElementById(i)}
function render(){
 var lv=L[idx];
 el("lvnum").textContent="Level "+lv.n+" of "+L.length;
 el("vault").textContent=lv.vault;el("vname").textContent=lv.vname;
 el("story").textContent=lv.story;el("score").textContent=score;
 el("bar").style.width=(Object.keys(done).length/L.length*100)+"%";
 var h="";
 for(var i=0;i<lv.locks.length;i++){var k=lv.locks[i];
  h+="<button class='lock' id='lk"+i+"' onclick='choose("+i+")'><span class='le'>"+k.e+
     "</span><span class='li'><b>"+k.name+"</b><span class='lc'>"+k.clue+"</span></span></button>";}
 el("locks").innerHTML=h;el("feed").style.display="none";el("nextb").style.display="none";tries=0;
}
function choose(i){
 var k=L[idx].locks[i],btn=el("lk"+i),f=el("feed");
 if(btn.classList.contains("wrong")||btn.classList.contains("right"))return;
 f.style.display="block";
 if(k.ok){
  btn.classList.add("right");
  var pts=tries===0?100:50;
  if(!done[idx]){score+=pts;done[idx]=true;}
  f.className="feed good";
  f.innerHTML="<b>&#127881; "+k.msg+"</b> <span class='pts'>+"+pts+"</span>";
  el("score").textContent=score;confetti();
  el("bar").style.width=(Object.keys(done).length/L.length*100)+"%";
  el("nextb").style.display="block";
  el("nextb").textContent=idx<L.length-1?"Next Level \u2192":"\uD83C\uDFC6 Finish!";
 }else{
  tries++;btn.classList.add("wrong");
  f.className="feed bad";f.innerHTML=k.msg+"<br><i>Try another lock!</i>";
 }
}
function next(){if(idx<L.length-1){idx++;render();window.scrollTo(0,0);}else{finish();}}
function finish(){
 var p=score===L.length*100;
 document.body.innerHTML="<div class='wrap'><div class='done'><div class='trophy'>"+
  (p?"\uD83C\uDFC6":"\u2B50")+"</div><h2>All Vaults Locked!</h2><div class='big'>"+score+
  " points</div><div class='vd'>"+(p?"PERFECT! Every lock right on the first try!":"Great job, agent! All 8 vaults protected.")+
  "</div><div class='recap'><b>What you learned:</b><br>&#128273; Some locks <b>hide</b> secrets (Kyber)<br>"+
  "&#9997;&#65039; Some locks <b>prove who you are</b> (Dilithium)<br>&#129413; Tiny gadgets need <b>tiny locks</b> (Falcon)<br>"+
  "&#128274; Old locks stop working when new computers arrive</div>"+
  "<button class='nb' onclick='location.reload()'>&#128260; Play Again</button></div></div>";
}
function confetti(){
 var c=["#fbbf24","#10b981","#3b82f6","#8b5cf6","#ef4444"];
 for(var i=0;i<20;i++){(function(n){setTimeout(function(){
  var d=document.createElement("div");d.className="confp";
  d.style.left=Math.random()*100+"vw";d.style.background=c[Math.floor(Math.random()*c.length)];
  d.style.animationDuration=(1+Math.random()*2)+"s";document.body.appendChild(d);
  setTimeout(function(){d.remove()},3000);},n*40)})(i)}
}
render();
</script></body></html>""", height=760, scrolling=True)
