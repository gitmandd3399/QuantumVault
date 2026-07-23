def render_lock_puzzle():
    """Elementary: 4-round lock challenge, 32 levels."""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("\U0001F512 Agent Pixel's Lock Challenge!")
    st.markdown("\U0001F6A8 **The Quantum Monster is coming!** Pick the RIGHT lock for each vault. **4 rounds, 32 vaults!** Each round starts easy and gets trickier.")
    components.html(r"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0b1526;font-family:'Segoe UI',sans-serif;color:#e2e8f0;padding:12px}
.wrap{max-width:560px;margin:0 auto}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
#lvnum{font-size:12px;color:#94a3b8;font-weight:800}
.sc{background:#1a1500;border:2px solid #fbbf24;border-radius:9px;padding:4px 13px;color:#fbbf24;font-weight:800;font-size:15px}
.track{height:7px;background:#1e293b;border-radius:4px;overflow:hidden;margin-bottom:14px}
#bar{height:100%;background:linear-gradient(90deg,#10b981,#34d399);width:0;transition:width .35s}
h2{color:#a5b4fc;font-size:19px;margin-bottom:3px}
.sub{color:#64748b;font-size:12.5px;margin-bottom:13px}
.rb{display:flex;align-items:center;gap:11px;width:100%;background:#111c30;border:2px solid #334155;
border-radius:12px;padding:14px;margin-bottom:9px;color:#e2e8f0;cursor:pointer;text-align:left}
.rb:hover{border-color:#a5b4fc;background:#18243c}
.rb.done{border-color:#10b981}
.ri{font-size:26px;flex-shrink:0}
.rt{flex:1}.rt b{font-size:15px}
.rs{display:block;font-size:11.5px;color:#64748b;margin-top:2px}
.backl{background:none;border:none;color:#64748b;font-size:12px;cursor:pointer;padding:0;margin-bottom:8px}
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
.nb{display:block}.done2{text-align:center;padding:24px 12px}
.trophy{font-size:60px}.done2 h2{color:#fbbf24;margin:6px 0}
.big{font-size:36px;font-weight:800;color:#fbbf24}.vd{font-size:15px;margin:8px 0 14px}
.recap{background:#111c30;border:1px solid #334155;border-radius:11px;padding:14px;text-align:left;font-size:13.5px;line-height:2}
.confp{position:fixed;top:-10px;width:9px;height:9px;border-radius:2px;pointer-events:none;animation:cf linear forwards;z-index:999}
@keyframes cf{to{transform:translateY(105vh) rotate(600deg);opacity:0}}
</style></head><body>
<div class="wrap" id="picker">
<h2>&#128272; Agent Pixel's Lock Challenge</h2>
<div class="sub">4 rounds &middot; 32 vaults to protect &middot; pick a round to start</div>
<div id="rounds"></div>
</div>
<div class="wrap" id="game" style="display:none">
<button class="backl" onclick="toPicker()">&#8592; All rounds</button>
<div class="top"><span id="lvnum"></span><span class="sc">&#11088; <span id="score">0</span></span></div>
<div class="track"><div id="bar"></div></div>
<div class="vaultbox"><div id="vault"></div><div id="vname"></div><div id="story"></div></div>
<div class="pick">&#128073; Pick the right lock:</div>
<div id="locks"></div><div id="feed" class="feed"></div>
<button id="nextb" onclick="next()">Next Level &#8594;</button>
</div><script>
var RS = [{"t": "Agent Pixel's First Missions", "i": "\ud83d\udd10", "lv": [{"n": 1, "vault": "\ud83d\udce6", "vname": "The Toy Box", "story": "Agent Pixel needs to lock her toy box. Which lock keeps it safe?", "locks": [{"e": "\ud83d\udd12", "name": "Strong Lock", "clue": "Thick metal. Nobody can break it!", "ok": true, "msg": "Yes! A strong lock keeps the toy box safe."}, {"e": "\ud83d\udd13", "name": "Broken Lock", "clue": "It has a big crack down the middle.", "ok": false, "msg": "Oh no! A cracked lock pops right open."}]}, {"n": 2, "vault": "\ud83c\udf6a", "vname": "The Cookie Jar", "story": "Someone keeps taking cookies! Pick a lock that really works.", "locks": [{"e": "\ud83e\uddfb", "name": "Paper Lock", "clue": "Made of paper. It looks nice!", "ok": false, "msg": "Paper tears! Pretty is not the same as safe."}, {"e": "\ud83d\udd12", "name": "Metal Lock", "clue": "Hard metal. Needs a real key.", "ok": true, "msg": "Great pick! Only someone with the key can open it."}]}, {"n": 3, "vault": "\ud83d\udcb0", "vname": "The Piggy Bank", "story": "Pixel's savings need protecting. One of these locks is old and tired.", "locks": [{"e": "\ud83d\udd12", "name": "Old Lock", "clue": "It worked GREAT for 40 whole years!", "ok": false, "msg": "Tricky! Working a long time does not mean it still works."}, {"e": "\ud83d\udd11", "name": "Super-Lock", "clue": "Brand new. A giant dot puzzle nobody can solve.", "ok": true, "msg": "Yes! Too hard even for a super-computer."}, {"e": "\ud83d\udd26", "name": "Light Lock", "clue": "It glows in the dark. So cool!", "ok": false, "msg": "Glowing is fun, but it does not keep secrets safe!"}]}, {"n": 4, "vault": "\ud83d\udce8", "vname": "The Secret Note", "story": "Pixel is sending a note to Byte. Which lock HIDES what it says?", "locks": [{"e": "\u270d\ufe0f", "name": "Name Lock", "clue": "It proves the note is really from Pixel.", "ok": false, "msg": "Close! That proves WHO sent it. It does not HIDE the words."}, {"e": "\ud83d\udd11", "name": "Hiding Lock", "clue": "It scrambles the words so nobody can read them.", "ok": true, "msg": "Perfect! Hiding the words is the job here."}, {"e": "\ud83d\uddd1\ufe0f", "name": "Trash Lock", "clue": "It deletes the note forever.", "ok": false, "msg": "Then Byte gets nothing!"}]}, {"n": 5, "vault": "\ud83d\udcf1", "vname": "The Tablet", "story": "Real lock names now! The tablet needs the lock that SHARES secret keys.", "locks": [{"e": "\ud83d\udd11", "name": "KYBER", "clue": "Shares secret keys safely. Big-kid name: ML-KEM.", "ok": true, "msg": "Yes! Scientists picked Kyber in 2024."}, {"e": "\u270d\ufe0f", "name": "DILITHIUM", "clue": "Signs your name so people know it is you.", "ok": false, "msg": "Good lock, wrong job! Dilithium signs things."}, {"e": "\ud83d\udd12", "name": "RSA", "clue": "The old favorite. Everyone used it for years.", "ok": false, "msg": "RSA is the OLD lock. Super-computers break it now."}]}, {"n": 6, "vault": "\ud83d\udcdc", "vname": "The Homework Proof", "story": "The teacher needs to know the homework is really Pixel's.", "locks": [{"e": "\ud83d\udd11", "name": "KYBER", "clue": "Shares secret keys safely.", "ok": false, "msg": "Kyber hides things. We need to PROVE who made it!"}, {"e": "\u270d\ufe0f", "name": "DILITHIUM", "clue": "Signs it. Big-kid name: ML-DSA.", "ok": true, "msg": "Yes! Nobody can pretend to be Pixel."}, {"e": "\ud83d\udd04", "name": "SHUFFLE", "clue": "Mixes up all the letters.", "ok": false, "msg": "Now the teacher cannot read it either!"}]}, {"n": 7, "vault": "\u231a", "vname": "The Smart Watch", "story": "A watch has a TINY computer. It needs a small signature lock.", "locks": [{"e": "\ud83c\udf32", "name": "SPHINCS+", "clue": "Super safe! But signatures are really BIG.", "ok": false, "msg": "Too big for a tiny watch. Size matters!"}, {"e": "\ud83e\udd85", "name": "FALCON", "clue": "The tiniest signatures. Perfect for small gadgets.", "ok": true, "msg": "Yes! Small gadget, small lock."}, {"e": "\ud83d\udd11", "name": "KYBER", "clue": "Shares secret keys safely.", "ok": false, "msg": "We needed a SIGNATURE, not a key share."}]}, {"n": 8, "vault": "\ud83c\udfe5", "vname": "The Hospital Vault", "story": "FINAL! Doctor records must stay secret a WHOLE LIFE.", "locks": [{"e": "\ud83d\udd12", "name": "RSA", "clue": "The old lock. Still used in places!", "ok": false, "msg": "No! 80 years is too long for RSA."}, {"e": "\ud83d\udd11", "name": "KYBER (strongest size)", "clue": "Shares keys at the strongest setting.", "ok": true, "msg": "PERFECT! Lifetime secrets need the strongest size."}, {"e": "\ud83e\udd85", "name": "FALCON", "clue": "Tiny signatures for small gadgets.", "ok": false, "msg": "Falcon signs. A hospital must HIDE records first."}, {"e": "\ud83d\udd26", "name": "Glow Lock", "clue": "It looks amazing!", "ok": false, "msg": "Looking cool never keeps secrets safe!"}]}]}, {"t": "Everyday Vaults", "i": "\ud83c\udfe0", "lv": [{"n": 1, "vault": "\ud83c\udf92", "vname": "The Backpack", "story": "Pixel's backpack has her lunch AND her secret notebook.", "locks": [{"e": "\ud83d\udd12", "name": "Zipper Lock", "clue": "A tiny lock that needs a key.", "ok": true, "msg": "Yes! Only Pixel has the key."}, {"e": "\ud83e\udea2", "name": "Ribbon", "clue": "A pretty bow tied on the zipper.", "ok": false, "msg": "Anyone can untie a bow!"}]}, {"n": 2, "vault": "\ud83d\udcd3", "vname": "The Diary", "story": "Pixel writes secrets in her diary. Which lock keeps them private?", "locks": [{"e": "\ud83d\udc40", "name": "See-Through Lock", "clue": "Made of clear glass. You can see right in!", "ok": false, "msg": "If you can see in, it is not secret!"}, {"e": "\ud83d\udd10", "name": "Secret Lock", "clue": "You need a secret word to open it.", "ok": true, "msg": "Perfect! Only someone who knows the word gets in."}]}, {"n": 3, "vault": "\ud83d\udeb2", "vname": "The Bike", "story": "Pixel's bike is outside all day. One lock only LOOKS strong.", "locks": [{"e": "\ud83d\udd17", "name": "Rusty Chain", "clue": "It is thick! But covered in rust.", "ok": false, "msg": "Rust makes it weak. Thick is not the same as strong."}, {"e": "\ud83d\udd12", "name": "U-Lock", "clue": "Solid metal. Brand new. No weak spots.", "ok": true, "msg": "Yes! Strong AND in good shape."}, {"e": "\ud83e\uddf5", "name": "String", "clue": "So easy to carry around!", "ok": false, "msg": "Easy to carry, easy to snip!"}]}, {"n": 4, "vault": "\ud83c\udfae", "vname": "The Game Account", "story": "Someone is pretending to be Pixel online! Which lock PROVES it is her?", "locks": [{"e": "\ud83d\udd11", "name": "Hiding Lock", "clue": "It scrambles her messages.", "ok": false, "msg": "That hides messages. We need to PROVE who she is!"}, {"e": "\u270d\ufe0f", "name": "Name Lock", "clue": "It puts her special mark on everything.", "ok": true, "msg": "Yes! Now everyone knows it is really Pixel."}, {"e": "\ud83d\udeab", "name": "Block Lock", "clue": "It blocks everybody.", "ok": false, "msg": "Now her friends cannot play either!"}]}, {"n": 5, "vault": "\ud83d\udcf8", "vname": "The Photo Album", "story": "Family photos must stay private a LONG time. Pick the key-sharing lock.", "locks": [{"e": "\ud83d\udd11", "name": "KYBER", "clue": "Shares secret keys safely. Big-kid name: ML-KEM.", "ok": true, "msg": "Yes! Kyber keeps the photos private."}, {"e": "\ud83d\udd12", "name": "RSA", "clue": "The old lock everyone used to use.", "ok": false, "msg": "Old lock! A super-computer can open it."}, {"e": "\ud83d\uddbc\ufe0f", "name": "Frame Lock", "clue": "It puts photos in a nice frame.", "ok": false, "msg": "Pretty, but anyone can still look!"}]}, {"n": 6, "vault": "\ud83d\udce7", "vname": "The Note to Grandma", "story": "Grandma needs to know this letter is REALLY from Pixel.", "locks": [{"e": "\u270d\ufe0f", "name": "DILITHIUM", "clue": "Signs it. Big-kid name: ML-DSA.", "ok": true, "msg": "Yes! Nobody can fake Pixel's letter."}, {"e": "\ud83d\udd11", "name": "KYBER", "clue": "Shares secret keys safely.", "ok": false, "msg": "Kyber shares keys. We need to PROVE who wrote it."}, {"e": "\ud83d\udc8c", "name": "Heart Sticker", "clue": "A cute sticker on the envelope!", "ok": false, "msg": "Anyone can buy that sticker!"}]}, {"n": 7, "vault": "\ud83d\udd0b", "vname": "The Tiny Sensor", "story": "A teeny sensor has almost NO room inside.", "locks": [{"e": "\ud83c\udf32", "name": "SPHINCS+", "clue": "Super safe, but signatures are HUGE.", "ok": false, "msg": "Too big for a teeny sensor!"}, {"e": "\ud83e\udd85", "name": "FALCON", "clue": "The tiniest signatures of them all.", "ok": true, "msg": "Yes! Tiny space needs a tiny lock."}, {"e": "\ud83d\udd12", "name": "RSA", "clue": "The old lock. Kind of big too.", "ok": false, "msg": "Old AND big. Two problems!"}]}, {"n": 8, "vault": "\ud83c\udfe6", "vname": "The Bank Vault", "story": "FINAL! Money records must stay secret for many, many years.", "locks": [{"e": "\ud83d\udd11", "name": "KYBER (strongest size)", "clue": "Shares keys at the strongest setting.", "ok": true, "msg": "PERFECT! Long secrets need the strongest size."}, {"e": "\u270d\ufe0f", "name": "DILITHIUM", "clue": "Signs things so you know who sent them.", "ok": false, "msg": "Signing is good, but first HIDE the records."}, {"e": "\ud83d\udd12", "name": "RSA", "clue": "Banks used this for a long time!", "ok": false, "msg": "Used to. Now super-computers break it."}, {"e": "\ud83d\udd11", "name": "KYBER (smallest size)", "clue": "Shares keys at the weakest setting.", "ok": false, "msg": "Right lock, wrong size!"}]}]}, {"t": "Helping Others", "i": "\ud83e\udd1d", "lv": [{"n": 1, "vault": "\ud83c\udfe0", "vname": "The Treehouse", "story": "The secret club treehouse needs a lock only members can open.", "locks": [{"e": "\ud83d\udd10", "name": "Password Lock", "clue": "Only club members know the word.", "ok": true, "msg": "Yes! Members in, everyone else out."}, {"e": "\ud83d\udeaa", "name": "Open Door", "clue": "No lock at all. Very friendly!", "ok": false, "msg": "Friendly, but not secret!"}]}, {"n": 2, "vault": "\ud83d\udc15", "vname": "The Pet Door", "story": "The dog door should let the DOG in, but not strangers.", "locks": [{"e": "\ud83d\udd73\ufe0f", "name": "Big Hole", "clue": "Anyone can fit through!", "ok": false, "msg": "Anyone means ANYONE."}, {"e": "\ud83d\udce1", "name": "Collar Lock", "clue": "Only opens for the dog's special collar.", "ok": true, "msg": "Yes! It checks WHO is coming in."}]}, {"n": 3, "vault": "\ud83d\udcda", "vname": "The Library Records", "story": "Which books people borrow is private. One lock is out of date.", "locks": [{"e": "\ud83d\udd12", "name": "Old Lock", "clue": "The library has used it since forever.", "ok": false, "msg": "Forever is the problem! New computers break old locks."}, {"e": "\ud83d\udd11", "name": "Super-Lock", "clue": "New. Uses a dot puzzle nobody can solve.", "ok": true, "msg": "Yes! Borrowing stays private."}, {"e": "\ud83d\udccb", "name": "Clipboard", "clue": "Write names on paper by the door.", "ok": false, "msg": "Everyone walking by can read it!"}]}, {"n": 4, "vault": "\ud83d\udd2c", "vname": "The Science Fair", "story": "Pixel invented something! She must PROVE the idea is hers.", "locks": [{"e": "\u270d\ufe0f", "name": "Name Lock", "clue": "Stamps her mark on the invention papers.", "ok": true, "msg": "Yes! Nobody can say they made it first."}, {"e": "\ud83d\udd11", "name": "Hiding Lock", "clue": "Hides the invention completely.", "ok": false, "msg": "Then judges cannot see it! PROVE, do not hide."}, {"e": "\ud83d\udda8\ufe0f", "name": "Copy Lock", "clue": "Makes lots of copies.", "ok": false, "msg": "More copies does not prove who made it."}]}, {"n": 5, "vault": "\ud83c\udfe5", "vname": "The Doctor Visit", "story": "Checkup notes go to another doctor. Pick the key-sharing lock.", "locks": [{"e": "\ud83d\udd11", "name": "KYBER", "clue": "Shares secret keys safely. Big-kid name: ML-KEM.", "ok": true, "msg": "Yes! The notes stay private on the way."}, {"e": "\ud83d\udce2", "name": "Speaker Lock", "clue": "Reads the notes out loud!", "ok": false, "msg": "The whole waiting room heard that!"}, {"e": "\ud83d\udd12", "name": "RSA", "clue": "An older lock still used in places.", "ok": false, "msg": "Doctor notes last a lifetime. Too long for RSA."}]}, {"n": 6, "vault": "\ud83c\udfeb", "vname": "The Report Card", "story": "School must prove this report card is real and grades were not changed.", "locks": [{"e": "\ud83d\udd11", "name": "KYBER", "clue": "Shares secret keys safely.", "ok": false, "msg": "Kyber hides. We need to PROVE it is real!"}, {"e": "\u270d\ufe0f", "name": "DILITHIUM", "clue": "Signs it. Big-kid name: ML-DSA.", "ok": true, "msg": "Yes! Changed grades would be caught."}, {"e": "\u270f\ufe0f", "name": "Pencil", "clue": "Write the grades in pencil.", "ok": false, "msg": "Pencil erases! Anyone could change them."}]}, {"n": 7, "vault": "\ud83d\udef0\ufe0f", "vname": "The Weather Sensor", "story": "A mountain sensor runs on a tiny battery.", "locks": [{"e": "\ud83e\udd85", "name": "FALCON", "clue": "The smallest signatures.", "ok": true, "msg": "Yes! Saves battery and space."}, {"e": "\ud83c\udf32", "name": "SPHINCS+", "clue": "Very safe, but very big signatures.", "ok": false, "msg": "Too big for a mountain sensor!"}, {"e": "\ud83d\udcfa", "name": "Screen Lock", "clue": "Shows the weather on a big screen.", "ok": false, "msg": "That is not a lock at all!"}]}, {"n": 8, "vault": "\ud83d\uddfa\ufe0f", "vname": "The Time Capsule", "story": "FINAL! This capsule opens in 100 YEARS.", "locks": [{"e": "\ud83d\udd12", "name": "RSA", "clue": "Strong today!", "ok": false, "msg": "Today is not enough. 100 years is a LONG time."}, {"e": "\ud83d\udd11", "name": "KYBER (strongest size)", "clue": "Shares keys at the strongest setting.", "ok": true, "msg": "PERFECT! Longer secret, stronger lock."}, {"e": "\ud83e\ude99", "name": "Coin Lock", "clue": "Put in a coin to open.", "ok": false, "msg": "Anyone with a coin gets in!"}, {"e": "\ud83c\udf32", "name": "SPHINCS+", "clue": "Signs things very safely.", "ok": false, "msg": "Signing proves WHO. We must HIDE what is inside."}]}]}, {"t": "Space Mission", "i": "\ud83d\ude80", "lv": [{"n": 1, "vault": "\ud83d\ude80", "vname": "The Rocket Hatch", "story": "The rocket hatch must stay shut in space.", "locks": [{"e": "\ud83d\udd12", "name": "Space Lock", "clue": "Built for space. Sealed tight.", "ok": true, "msg": "Yes! Sealed tight is what space needs."}, {"e": "\ud83e\uddf2", "name": "Magnet", "clue": "Sticks pretty well!", "ok": false, "msg": "Pretty well is not good enough in space!"}]}, {"n": 2, "vault": "\ud83e\udd16", "vname": "The Robot Helper", "story": "Only Pixel should give the robot orders.", "locks": [{"e": "\ud83d\udd0a", "name": "Loud Lock", "clue": "Anyone who shouts gets to give orders.", "ok": false, "msg": "Then anyone can boss the robot around!"}, {"e": "\ud83d\udddd\ufe0f", "name": "Key Lock", "clue": "Only Pixel's key gives orders.", "ok": true, "msg": "Yes! The robot listens only to Pixel."}]}, {"n": 3, "vault": "\ud83d\udef8", "vname": "The Space Station", "story": "The station is old. One lock was built long ago.", "locks": [{"e": "\ud83d\udd12", "name": "1970s Lock", "clue": "It protected the station for 50 years!", "ok": false, "msg": "Great run, but new computers crack it now."}, {"e": "\ud83d\udd11", "name": "Super-Lock", "clue": "New. An impossible dot puzzle.", "ok": true, "msg": "Yes! Time to upgrade the old station."}, {"e": "\ud83e\uddf5", "name": "Space Tape", "clue": "Tape holds everything together!", "ok": false, "msg": "Tape is not a lock!"}]}, {"n": 4, "vault": "\ud83d\udce1", "vname": "The Message From Earth", "story": "A message arrives. Is it REALLY from Mission Control?", "locks": [{"e": "\ud83d\udd11", "name": "Hiding Lock", "clue": "Scrambles the message.", "ok": false, "msg": "That hides it. We need to check WHO sent it!"}, {"e": "\u270d\ufe0f", "name": "Name Lock", "clue": "Checks Mission Control's special mark.", "ok": true, "msg": "Yes! Nobody can fake a message."}, {"e": "\ud83d\udd0a", "name": "Volume Lock", "clue": "Makes the message louder.", "ok": false, "msg": "Louder does not mean truer!"}]}, {"n": 5, "vault": "\ud83c\udf0c", "vname": "The Star Map", "story": "The secret star map must travel to Earth safely.", "locks": [{"e": "\ud83d\udd11", "name": "KYBER", "clue": "Shares secret keys safely. Big-kid name: ML-KEM.", "ok": true, "msg": "Yes! Kyber protects the map on its trip."}, {"e": "\u270d\ufe0f", "name": "DILITHIUM", "clue": "Signs things.", "ok": false, "msg": "Signing proves who sent it. First HIDE the map."}, {"e": "\ud83d\udd12", "name": "RSA", "clue": "The old space lock.", "ok": false, "msg": "Old lock! Not safe from super-computers."}]}, {"n": 6, "vault": "\ud83d\udee0\ufe0f", "vname": "The Repair Order", "story": "A repair order tells the robot what to fix. It must be REAL!", "locks": [{"e": "\u270d\ufe0f", "name": "DILITHIUM", "clue": "Signs the order. Big-kid name: ML-DSA.", "ok": true, "msg": "Yes! A fake order would be caught."}, {"e": "\ud83d\udd11", "name": "KYBER", "clue": "Shares secret keys safely.", "ok": false, "msg": "Kyber hides. We need to PROVE the order is real."}, {"e": "\ud83d\udcdd", "name": "Sticky Note", "clue": "Just write it on a note.", "ok": false, "msg": "Anyone could write a fake note!"}]}, {"n": 7, "vault": "\ud83d\udef0\ufe0f", "vname": "The Mini Satellite", "story": "This satellite is the size of a shoebox.", "locks": [{"e": "\ud83c\udf32", "name": "SPHINCS+", "clue": "Very safe. Very big signatures.", "ok": false, "msg": "Too big for a shoebox satellite!"}, {"e": "\ud83e\udd85", "name": "FALCON", "clue": "Tiny signatures for tiny machines.", "ok": true, "msg": "Yes! Tiny satellite, tiny lock."}, {"e": "\ud83d\udd11", "name": "KYBER", "clue": "Shares secret keys.", "ok": false, "msg": "We needed a SIGNATURE, not a key share."}]}, {"n": 8, "vault": "\ud83c\udfdb\ufe0f", "vname": "The Museum Vault", "story": "FINAL! Mission records must stay safe FOREVER.", "locks": [{"e": "\ud83d\udd11", "name": "KYBER (strongest size)", "clue": "Shares keys at the strongest setting.", "ok": true, "msg": "PERFECT! You are a true Lock Master!"}, {"e": "\ud83d\udd11", "name": "KYBER (smallest size)", "clue": "Shares keys at the weakest setting.", "ok": false, "msg": "Right lock, wrong size!"}, {"e": "\ud83d\udd12", "name": "RSA", "clue": "Museums trusted it for years.", "ok": false, "msg": "Not for forever. Super-computers will break it."}, {"e": "\ud83e\udd85", "name": "FALCON", "clue": "Tiny signatures.", "ok": false, "msg": "Falcon signs. We must HIDE the records first."}]}]}];
var best = {}, rIdx = 0, L = [], idx = 0, score = 0, done = {}, tries = 0;
function el(i){return document.getElementById(i)}
function toPicker(){
 el("game").style.display="none";el("picker").style.display="block";
 var h="";
 for(var i=0;i<RS.length;i++){
  var b=best[i];
  h+="<button class='rb"+(b?" done":"")+"' onclick='startRound("+i+")'><span class='ri'>"+RS[i].i+
     "</span><span class='rt'><b>"+RS[i].t+"</b><span class='rs'>8 vaults"+
     (b?" &middot; best: "+b+" pts":"")+"</span></span></button>";}
 el("rounds").innerHTML=h;
}
function startRound(i){
 rIdx=i;L=RS[i].lv;idx=0;score=0;done={};tries=0;
 el("picker").style.display="none";el("game").style.display="block";
 render();window.scrollTo(0,0);
}
function render(){
 var lv=L[idx];
 el("lvnum").textContent=RS[rIdx].t+" — Level "+lv.n+" of "+L.length;
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
  el("nextb").textContent=idx<L.length-1?"Next Level \u2192":"\uD83C\uDFC6 Finish Round!";
 }else{
  tries++;btn.classList.add("wrong");
  f.className="feed bad";f.innerHTML=k.msg+"<br><i>Try another lock!</i>";
 }
}
function next(){if(idx<L.length-1){idx++;render();window.scrollTo(0,0);}else{finish();}}
function finish(){
 var p=score===L.length*100;
 if(!best[rIdx]||score>best[rIdx])best[rIdx]=score;
 el("game").innerHTML="<div class='done2'><div class='trophy'>"+(p?"\uD83C\uDFC6":"\u2B50")+
  "</div><h2>Round Complete!</h2><div class='big'>"+score+" points</div><div class='vd'>"+
  (p?"PERFECT! Every lock right on the first try!":"Great job, agent! All 8 vaults protected.")+
  "</div><div class='recap'><b>Remember:</b><br>&#128273; Some locks <b>hide</b> secrets (Kyber)<br>"+
  "&#9997;&#65039; Some locks <b>prove who you are</b> (Dilithium)<br>&#129413; Tiny gadgets need <b>tiny locks</b> (Falcon)<br>"+
  "&#128274; Old locks stop working when new computers arrive</div>"+
  "<button class='nb' onclick='startRound("+rIdx+")'>&#128260; Replay Round</button>"+
  "<button class='nb' style='background:#334155' onclick='location.reload()'>&#8592; All Rounds</button></div>";
}
function confetti(){
 var c=["#fbbf24","#10b981","#3b82f6","#8b5cf6","#ef4444"];
 for(var i=0;i<18;i++){(function(n){setTimeout(function(){
  var d=document.createElement("div");d.className="confp";
  d.style.left=Math.random()*100+"vw";d.style.background=c[Math.floor(Math.random()*c.length)];
  d.style.animationDuration=(1+Math.random()*2)+"s";document.body.appendChild(d);
  setTimeout(function(){d.remove()},3000);},n*40)})(i)}
}
toPicker();
</script></body></html>""", height=780, scrolling=True)
