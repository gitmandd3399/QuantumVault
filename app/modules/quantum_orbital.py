def render_quantum_orbital():
    """All grades: Quantum Orbital Defense — Build rocket, launch, protect satellite with PQC!"""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("🚀 Quantum Orbital Defense")
    st.markdown(
        "**Build a rocket, launch to orbit, and defend your satellite from quantum attacks!** "
        "Real rocket science + real PQC cryptography. "
        "NSA requires quantum-safe satellites by 2027 — the clock is ticking!"
    )

    components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;overflow:hidden;}
#wrap{max-width:580px;margin:0 auto;padding:8px;}

/* HUD */
.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-bottom:6px;}
.hb{background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:5px 3px;
    text-align:center;font-size:9px;color:#60a5fa;}
.hb b{display:block;font-size:14px;color:white;}

/* PHASE TABS */
#phase-bar{display:flex;gap:3px;margin-bottom:6px;}
.phase-tab{flex:1;padding:6px 4px;border-radius:8px;border:2px solid #1a3a5a;
    background:#071520;font-size:10px;font-weight:bold;text-align:center;
    color:#475569;transition:all 0.2s;}
.phase-tab.active{background:#1d4ed8;border-color:#60a5fa;color:white;}
.phase-tab.done{background:#059669;border-color:#10b981;color:white;}

/* CANVAS */
#cv{border:2px solid #1d4ed8;border-radius:10px;display:block;
    box-shadow:0 0 20px rgba(29,78,216,0.2);}

/* MSG + FACT */
#msg{background:#071520;border:1px solid #1a3a5a;border-radius:8px;
    padding:5px 10px;margin-top:5px;font-size:10px;color:#60a5fa;
    text-align:center;min-height:22px;}
#fact{background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);
    border-radius:8px;padding:6px 10px;margin-top:4px;font-size:10px;
    color:#93c5fd;display:none;line-height:1.5;text-align:center;}

/* BUILDER PARTS PANEL */
#parts-panel{display:flex;gap:4px;flex-wrap:wrap;justify-content:center;
    margin-top:5px;padding:4px;background:#071520;border:1px solid #1a3a5a;
    border-radius:8px;}
.part-btn{padding:5px 8px;border-radius:8px;border:1px solid #1a3a5a;
    background:#0a1f35;color:#94a3b8;font-size:9px;cursor:pointer;
    text-align:center;transition:all 0.15s;min-width:58px;}
.part-btn:hover{border-color:#3b82f6;color:white;}
.part-btn.selected{border-color:#fbbf24;background:#1a1500;color:#fbbf24;}
.part-btn .pe{font-size:14px;display:block;margin-bottom:1px;}

/* LAUNCH BUTTON */
#launch-btn{width:100%;padding:10px;background:linear-gradient(135deg,#dc2626,#ef4444);
    border:none;border-radius:10px;color:white;font-size:14px;font-weight:bold;
    cursor:pointer;margin-top:5px;transition:all 0.2s;display:none;}
#launch-btn:hover{filter:brightness(1.15);}
#launch-btn:disabled{opacity:0.4;cursor:not-allowed;}

/* ORBITAL SHIELDS */
#shield-panel{display:flex;gap:4px;flex-wrap:wrap;justify-content:center;
    margin-top:5px;display:none;}
.shield-btn{padding:5px 10px;border-radius:8px;border:2px solid #1a3a5a;
    background:#071520;color:#94a3b8;font-size:10px;cursor:pointer;
    transition:all 0.15s;text-align:center;}
.shield-btn:hover{border-color:#3b82f6;}
.shield-btn.active{border-color:#fbbf24;background:#1a1500;color:#fbbf24;}
.shield-btn.locked{opacity:0.3;cursor:not-allowed;}

/* TOAST */
#toast{position:fixed;top:14px;left:50%;transform:translateX(-50%);
    background:#071520;border:2px solid #fbbf24;border-radius:10px;
    padding:7px 14px;font-size:11px;color:#fbbf24;font-weight:bold;
    z-index:100;opacity:0;transition:opacity 0.3s;pointer-events:none;text-align:center;}
#toast.show{opacity:1;}

/* CONFETTI */
.cp{position:fixed;pointer-events:none;z-index:999;width:8px;height:8px;
    border-radius:2px;animation:cf linear forwards;}
@keyframes cf{0%{transform:translateY(-20px) rotate(0deg);opacity:1;}
    100%{transform:translateY(600px) rotate(720deg);opacity:0;}}
</style>
</head>
<body>
<div id="wrap">

<!-- HUD -->
<div class="hud">
    <div class="hb">🚀 Phase<br><b id="h-phase">BUILD</b></div>
    <div class="hb">⚖️ TWR<br><b id="h-twr">0.0</b></div>
    <div class="hb">🛡️ PQC<br><b id="h-pqc">0/4</b></div>
    <div class="hb">⭐ Score<br><b id="h-score">0</b></div>
</div>

<!-- PHASE TABS -->
<div id="phase-bar">
    <div class="phase-tab active" id="pt-build">⚙️ 1. Build</div>
    <div class="phase-tab" id="pt-launch">🚀 2. Launch</div>
    <div class="phase-tab" id="pt-orbit">🛰️ 3. Defend</div>
</div>

<!-- CANVAS -->
<canvas id="cv" width="560" height="360"></canvas>

<!-- MSG + FACT -->
<div id="msg">Select parts and stack your rocket! TWR must be above 1.2 to launch.</div>
<div id="fact"></div>

<!-- BUILDER PARTS -->
<div id="parts-panel">
    <div class="part-btn selected" onclick="selectPart('raptor')" id="pb-raptor">
        <span class="pe">🔥</span>Raptor<br>
        <span style="color:#ef4444">W:2 T:+8</span>
    </div>
    <div class="part-btn" onclick="selectPart('tank')" id="pb-tank">
        <span class="pe">⛽</span>Fuel Tank<br>
        <span style="color:#60a5fa">W:3 T:0</span>
    </div>
    <div class="part-btn" onclick="selectPart('booster')" id="pb-booster">
        <span class="pe">🔵</span>Booster<br>
        <span style="color:#ef4444">W:1 T:+4</span>
    </div>
    <div class="part-btn" onclick="selectPart('payload')" id="pb-payload">
        <span class="pe">📡</span>Sat Bus<br>
        <span style="color:#60a5fa">W:2 T:0</span>
    </div>
    <div class="part-btn" onclick="selectPart('kyber')" id="pb-kyber">
        <span class="pe">🔐</span>ML-KEM<br>
        <span style="color:#10b981">W:1 PQC!</span>
    </div>
    <div class="part-btn" onclick="selectPart('dilithium')" id="pb-dilithium">
        <span class="pe">✍️</span>ML-DSA<br>
        <span style="color:#10b981">W:1 PQC!</span>
    </div>
    <div class="part-btn" onclick="selectPart('sphincs')" id="pb-sphincs">
        <span class="pe">🌲</span>SPHINCS+<br>
        <span style="color:#10b981">W:1 PQC!</span>
    </div>
    <div class="part-btn" onclick="selectPart('falcon')" id="pb-falcon">
        <span class="pe">🦅</span>Falcon<br>
        <span style="color:#10b981">W:1 PQC!</span>
    </div>
    <div class="part-btn" onclick="clearRocket()" style="border-color:#ef4444;color:#ef4444">
        <span class="pe">🗑️</span>Clear<br>
        <span>Reset</span>
    </div>
</div>

<!-- LAUNCH BUTTON -->
<button id="launch-btn" onclick="startLaunch()">🚀 LAUNCH ROCKET!</button>

<!-- PLAY AGAIN BUTTON -->
<button id="play-again-btn" onclick="resetGame()"
    style="display:none;width:100%;padding:12px;margin-top:5px;
    background:linear-gradient(135deg,#059669,#10b981);border:none;
    border-radius:10px;color:white;font-size:15px;font-weight:bold;
    cursor:pointer;animation:pulse 1s infinite;">
    🔄 Play Again — Launch Another Satellite!
</button>
<style>
@keyframes pulse{0%,100%{transform:scale(1);}50%{transform:scale(1.02);}}
</style>

<!-- ORBITAL SHIELD PANEL -->
<div id="shield-panel">
    <div class="shield-btn" onclick="deployShield('kyber')" id="sb-kyber">🔐 ML-KEM</div>
    <div class="shield-btn" onclick="deployShield('dilithium')" id="sb-dilithium">✍️ ML-DSA</div>
    <div class="shield-btn" onclick="deployShield('sphincs')" id="sb-sphincs">🌲 SPHINCS+</div>
    <div class="shield-btn" onclick="deployShield('falcon')" id="sb-falcon">🦅 Falcon</div>
</div>

</div><!-- end wrap -->
<div id="toast"></div>

<script>
// ── CONSTANTS ─────────────────────────────────────────────────────────────────
var W = 560, H = 360;
var cv = document.getElementById('cv');
var cx = cv.getContext('2d');

// ── PART DEFINITIONS ──────────────────────────────────────────────────────────
var PARTS = {
    raptor:    {emoji:'🔥', name:'Raptor Engine',  weight:2, thrust:8,  pqc:null,  color:'#ef4444', h:36},
    tank:      {emoji:'⛽', name:'Fuel Tank',       weight:3, thrust:0,  pqc:null,  color:'#3b82f6', h:48},
    booster:   {emoji:'🔵', name:'Side Booster',   weight:1, thrust:4,  pqc:null,  color:'#8b5cf6', h:40},
    payload:   {emoji:'📡', name:'Satellite Bus',  weight:2, thrust:0,  pqc:null,  color:'#f59e0b', h:40},
    kyber:     {emoji:'🔐', name:'ML-KEM Module',  weight:1, thrust:0,  pqc:'kyber',     color:'#10b981', h:30},
    dilithium: {emoji:'✍️',  name:'ML-DSA Module',  weight:1, thrust:0,  pqc:'dilithium', color:'#3b82f6', h:30},
    sphincs:   {emoji:'🌲', name:'SPHINCS+ Module', weight:1, thrust:0,  pqc:'sphincs',  color:'#8b5cf6', h:30},
    falcon:    {emoji:'🦅', name:'Falcon Module',   weight:1, thrust:0,  pqc:'falcon',   color:'#f59e0b', h:30},
};

var PQC_INFO = {
    kyber:     {name:'ML-KEM',   fips:'FIPS 203', desc:'Blocks Shor Algorithm key attacks!',      attack:'Quantum Key Crack'},
    dilithium: {name:'ML-DSA',   fips:'FIPS 204', desc:'Blocks signature forgery attacks!',      attack:'Command Forgery'},
    sphincs:   {name:'SPHINCS+', fips:'FIPS 205', desc:'Blocks hash collision firmware attacks!', attack:'Firmware Hijack'},
    falcon:    {name:'Falcon',   fips:'FIPS 206', desc:'Blocks IoT side-channel attacks!',       attack:'Side-Channel Theft'},
};

var ATTACK_FACTS = [
    '☠️ Harvest Now Decrypt Later: Enemy nations record ALL satellite transmissions TODAY to decrypt them when quantum computers arrive!',
    '🛰️ Real satellites in orbit today will still be operating in 2035 when quantum computers may be ready — they NEED PQC now!',
    '🔐 NSA CNSA 2.0 mandates all National Security Systems must be quantum-safe by January 2027!',
    '🌍 SpaceX Starlink, GPS, and military satellites all need PQC upgrades before the quantum threat arrives!',
    '⚡ Shor Algorithm can break RSA-2048 (used by most satellites today) in seconds on a quantum computer!',
    '🚀 Satellites launched TODAY will be in orbit for 10-20 years — quantum computers arrive well before that!',
];

// ── GAME STATE ─────────────────────────────────────────────────────────────────
var phase = 'build'; // build | launch | orbit
var rocketParts = []; // bottom to top
var selectedPart = 'raptor';
var score = 0;

// Launch state
var launchAlt = 0;    // 0-100 (km)
var launchVel = 0;    // velocity
var launchFuel = 100; // fuel %
var throttle = false;
var maxQ = false;     // max aerodynamic stress zone
var stageDropped = false;
var launchDone = false;
var rocketX = W/2;
var rocketY = H-60;
var rocketTilt = 0;
var exhaust = [];
var debris = [];
var stars = [];
var cloudY = H*0.4;

// Orbit state
var satAngle = 0;       // current orbital angle
var satHP = 100;
var satMaxHP = 100;
var orbitRadius = 100;
var attackWave = 0;
var attacks = [];
var shields = {};       // which PQC shields satellite has
var selectedShield = null;
var pulses = [];
var orbitScore = 0;
var earthPulse = 0;
var attackTimer = 0;
var gameOver = false;

// ── TUTORIAL SYSTEM ────────────────────────────────────────────────────────
var tutorialStep = 0;
var showTutorial = true;
var TUTORIAL_STEPS = [
    {
        phase: 'build',
        title: '⚙️ STEP 1: Build Your Rocket',
        lines: [
            '🔥 Start with a Raptor Engine at the bottom (gives thrust)',
            '⛽ Add Fuel Tanks above it (more fuel = higher orbit)',
            '🔐 Add PQC Modules to protect your satellite in orbit',
            '📡 Put the Satellite Bus on top (required!)',
            '📊 Watch the TWR meter — must be GREEN (>1.2) to launch!',
        ],
        tip: 'Click the canvas to place the selected part!',
        color: '#3b82f6',
    },
    {
        phase: 'build',
        title: '🛡️ STEP 2: Add PQC Shields',
        lines: [
            '🔐 ML-KEM (FIPS 203) — Blocks Quantum Key Attacks',
            '✍️ ML-DSA (FIPS 204) — Blocks Signature Forgery',
            '🌲 SPHINCS+ (FIPS 205) — Blocks Firmware Hijacks',
            '🦅 Falcon (FIPS 206) — Blocks IoT Side-Channel Attacks',
            '☠️ NSA requires ALL satellites quantum-safe by 2027!',
        ],
        tip: 'More PQC modules = harder to attack in orbit!',
        color: '#10b981',
    },
    {
        phase: 'launch',
        title: '🚀 STEP 3: Launch to Orbit',
        lines: [
            '🖱️ Hold/Click the canvas to THROTTLE the rocket',
            '⚠️ MAX-Q at 20-40km: maximum aerodynamic stress!',
            '💥 STAGE at 60km: rocket drops lower stage to go faster',
            '🌍 Tilt east at 10km (real gravity turn maneuver!)',
            '🛰️ Reach 100km to achieve orbit!',
        ],
        tip: 'Real orbit = going sideways fast enough to keep missing Earth!',
        color: '#f59e0b',
    },
    {
        phase: 'orbit',
        title: '🛰️ STEP 4: Defend Your Satellite',
        lines: [
            '👾 Quantum attacks fly toward your satellite',
            '🔐 Select the RIGHT PQC shield from the bottom panel',
            '🖱️ Click on the attack to destroy it with your shield',
            '❌ Wrong shield = attack gets through and damages satellite!',
            '🏆 Survive as many waves as possible!',
        ],
        tip: 'Match the shield to the attack type — read the attack label!',
        color: '#8b5cf6',
    },
];

function nextTutorial() {
    tutorialStep++;
    if (tutorialStep >= TUTORIAL_STEPS.length) {
        showTutorial = false;
    }
}
function skipTutorial() { showTutorial = false; }


// ── INIT STARS ────────────────────────────────────────────────────────────────
for (var i=0;i<80;i++) {
    stars.push({
        x: Math.random()*W, y: Math.random()*H,
        r: Math.random()*1.5, alpha: Math.random()*0.7+0.3,
        twinkle: Math.random()*6.28
    });
}

// ── BUILD PHASE ───────────────────────────────────────────────────────────────
function selectPart(type) {
    selectedPart = type;
    document.querySelectorAll('.part-btn').forEach(function(b){b.classList.remove('selected');});
    var el = document.getElementById('pb-'+type);
    if (el) el.classList.add('selected');
}

function addPart(type) {
    if (rocketParts.length >= 8) { toast('Max 8 parts!'); return; }
    rocketParts.push(type);
    updateBuildStats();
    setMsg('Added '+PARTS[type].name+'! TWR = '+getTWR().toFixed(2));
    if (PARTS[type].pqc) {
        showFact('🔐 '+PARTS[type].name+' ('+PQC_INFO[PARTS[type].pqc].fips+'): '+PQC_INFO[PARTS[type].pqc].desc);
    }
}

function clearRocket() {
    rocketParts = [];
    updateBuildStats();
    setMsg('Rocket cleared! Stack parts to build your rocket.');
}

function getTotalWeight() {
    return rocketParts.reduce(function(s,p){return s+PARTS[p].weight;}, 0);
}

function getTotalThrust() {
    return rocketParts.reduce(function(s,p){return s+PARTS[p].thrust;}, 0);
}

function getTWR() {
    var w = getTotalWeight();
    return w > 0 ? getTotalThrust() / w : 0;
}

function getPQCModules() {
    var pqc = {};
    rocketParts.forEach(function(p){ if(PARTS[p].pqc) pqc[PARTS[p].pqc]=true; });
    return pqc;
}

function getPQCCount() {
    return Object.keys(getPQCModules()).length;
}

function updateBuildStats() {
    var twr = getTWR();
    var pqc = getPQCCount();
    document.getElementById('h-twr').textContent = twr.toFixed(1);
    document.getElementById('h-twr').style.color = twr>=1.2?'#10b981':twr>=0.8?'#fbbf24':'#ef4444';
    document.getElementById('h-pqc').textContent = pqc+'/4';
    document.getElementById('h-pqc').style.color = pqc>=4?'#10b981':pqc>=2?'#fbbf24':'#ef4444';

    // Show launch button if valid
    var canLaunch = twr>=1.2 && rocketParts.includes('payload') && rocketParts.length>=3;
    document.getElementById('launch-btn').style.display = canLaunch?'block':'none';
    if (canLaunch) {
        document.getElementById('launch-btn').textContent = pqc<2?
            '⚠️ LAUNCH (WARNING: Only '+pqc+'/4 PQC shields!)':
            '🚀 LAUNCH ROCKET! ('+pqc+'/4 PQC shields)';
    }
}

// Canvas click for build phase
cv.addEventListener('click', function(e) {
    // Handle end game restart click
    if (endGameState) {
        var r = cv.getBoundingClientRect();
        var mx = (e.clientX-r.left)*(W/r.width);
        var my = (e.clientY-r.top)*(H/r.height);
        if (mx>playAgainBtn.x && mx<playAgainBtn.x+playAgainBtn.w &&
            my>playAgainBtn.y && my<playAgainBtn.y+playAgainBtn.h) {
            resetGame();
        }
        return;
    }
    // Handle tutorial clicks first
    if (showTutorial) {
        var r = cv.getBoundingClientRect();
        var mx = (e.clientX-r.left)*(W/r.width);
        var my = (e.clientY-r.top)*(H/r.height);
        var step = TUTORIAL_STEPS[Math.min(tutorialStep, TUTORIAL_STEPS.length-1)];
        if (!step) { showTutorial=false; return; }
        var cw=420, ch=240, cx2=W/2-cw/2, cy2=H/2-ch/2;
        // Next button hit test
        if (mx>W/2+20&&mx<W/2+140&&my>cy2+ch-35&&my<cy2+ch-9) { nextTutorial(); return; }
        // Skip button hit test
        if (mx>W/2-140&&mx<W/2-30&&my>cy2+ch-35&&my<cy2+ch-9) { skipTutorial(); return; }
        return;
    }
    if (phase === 'build') {
        addPart(selectedPart);
    } else if (phase === 'launch') {
        throttle = !throttle;
    } else if (phase === 'orbit') {
        // Click on attack to use shield
        var r = cv.getBoundingClientRect();
        var mx = (e.clientX-r.left)*(W/r.width);
        var my = (e.clientY-r.top)*(H/r.height);
        tryDestroyAttack(mx, my);
    }
});

// Hold for throttle
cv.addEventListener('mousedown', function(){if(phase==='launch') throttle=true;});
cv.addEventListener('mouseup', function(){if(phase==='launch') throttle=false;});
cv.addEventListener('touchstart', function(e){e.preventDefault();if(phase==='launch')throttle=true;},{passive:false});
cv.addEventListener('touchend', function(e){e.preventDefault();if(phase==='launch')throttle=false;},{passive:false});

// ── LAUNCH PHASE ──────────────────────────────────────────────────────────────
function startLaunch() {
    phase = 'launch';
    launchAlt = 0; launchVel = 0; launchFuel = 100;
    stageDropped = false; launchDone = false;
    rocketX = W/2; rocketY = H-80; rocketTilt = 0;
    exhaust = []; debris = [];
    maxQ = false;
    shields = getPQCModules();

    document.getElementById('pt-build').classList.remove('active');
    document.getElementById('pt-launch').classList.add('active');
    document.getElementById('parts-panel').style.display='none';
    document.getElementById('launch-btn').style.display='none';
    setMsg('🚀 LAUNCH! Hold/click to throttle. Tilt east at 10km. Stage at 60km!');
    if(tutorialStep<2){tutorialStep=2;showTutorial=true;}
    showFact('🚀 Real rockets use a "gravity turn" — they tilt east as they climb to build orbital velocity. SpaceX Falcon 9 does this automatically!');

    // Add space debris
    for(var i=0;i<6;i++) {
        debris.push({
            x: Math.random()*W, y: -50-Math.random()*200,
            vx:(Math.random()-0.5)*1.5, vy:0.8+Math.random()*1.2,
            r:3+Math.random()*5, color:'#475569'
        });
    }
}

function updateLaunch() {
    if (launchDone) return;
    var twr = getTWR();

    if (throttle && launchFuel > 0) {
        var accel = (twr - 1.0) * 0.08;
        launchVel += accel;
        launchFuel = Math.max(0, launchFuel - 0.4);
        // Exhaust particles
        exhaust.push({
            x: rocketX+(Math.random()-0.5)*10,
            y: rocketY+40,
            vx:(Math.random()-0.5)*3, vy:2+Math.random()*4,
            alpha:1, r:3+Math.random()*4,
            color:['#ef4444','#f97316','#fbbf24'][Math.floor(Math.random()*3)]
        });
    }

    launchAlt += launchVel;

    // Gravity turn — tilt east after 10km
    if (launchAlt > 10) {
        rocketTilt = Math.min(0.4, (launchAlt-10)/100);
        rocketX = Math.min(W-60, W/2 + (launchAlt-10)*0.8);
    }

    // Max Q zone (20-40km) — aerodynamic turbulence
    maxQ = launchAlt>20 && launchAlt<40;
    if (maxQ && throttle) {
        rocketX += (Math.random()-0.5)*3;
        rocketY += (Math.random()-0.5)*2;
    }

    // Stage separation at 60km
    if (launchAlt>60 && !stageDropped) {
        stageDropped = true;
        launchVel += 0.8; // velocity boost from staging
        toast('💥 STAGE SEPARATION! Mass reduced — accelerating!');
        showFact('🚀 Real staging: Falcon 9 drops its first stage at ~70km, SpaceX then lands it back for reuse. This is the "Tsiolkovsky rocket equation" in action — shed mass to go faster!');
    }

    // Orbit achieved at 100km
    if (launchAlt >= 100) {
        launchDone = true;
        setTimeout(startOrbit, 1500);
        toast('🛰️ ORBIT ACHIEVED! 28,000 km/h! Deploying satellite...');
        showFact('🛰️ You reached orbit! Real Low Earth Orbit is at 400km (ISS altitude). Your satellite must maintain 7.8 km/s sideways velocity to keep "falling around" the Earth!');
        score += 500 + getPQCCount()*100;
        updateHUD();
        confetti();
    }

    // Move debris
    debris.forEach(function(d){d.y+=d.vy;d.x+=d.vx;});
    debris = debris.filter(function(d){return d.y<H+50;});

    // Debris collision check
    debris.forEach(function(d){
        if(Math.hypot(d.x-rocketX,d.y-rocketY)<d.r+20&&!launchDone){
            launchVel = Math.max(0, launchVel-0.3);
            toast('☄️ Debris hit! Velocity reduced!');
        }
    });

    // Update exhaust
    exhaust.forEach(function(p){p.y+=p.vy;p.x+=p.vx;p.alpha-=0.04;p.r*=0.93;});
    exhaust = exhaust.filter(function(p){return p.alpha>0;});

    // Update HUD
    document.getElementById('h-twr').textContent = launchAlt.toFixed(0)+'km';
    document.getElementById('h-phase').textContent = 'LAUNCH';
    setMsg((throttle?'🔥 THROTTLE UP! ':'⬇️ Hold click to throttle! ')+
        'Alt: '+launchAlt.toFixed(0)+'km | Fuel: '+launchFuel.toFixed(0)+'% | Vel: '+launchVel.toFixed(2)+'km/s'+
        (maxQ?' | ⚠️ MAX-Q!':''));
}

// ── ORBIT PHASE ───────────────────────────────────────────────────────────────
function startOrbit() {
    phase = 'orbit';
    satAngle = 0; satHP = 100; attackWave = 0;
    attacks = []; pulses = []; gameOver = false;
    attackTimer = 0; earthPulse = 0;
    orbitScore = 0;

    document.getElementById('pt-launch').classList.remove('active');
    document.getElementById('pt-launch').classList.add('done');
    document.getElementById('pt-orbit').classList.add('active');
    document.getElementById('shield-panel').style.display='flex';

    // Set available shields
    var pqc = getPQCModules();
    ['kyber','dilithium','sphincs','falcon'].forEach(function(k){
        var btn = document.getElementById('sb-'+k);
        if (!pqc[k]) {
            btn.classList.add('locked');
            btn.title = 'Not installed! You need '+PQC_INFO[k].name+' module on your rocket.';
        }
    });
    selectedShield = Object.keys(pqc)[0] || null;
    if (selectedShield) document.getElementById('sb-'+selectedShield).classList.add('active');

    document.getElementById('h-phase').textContent = 'ORBIT';
    setMsg('🛰️ Satellite deployed! Click attacks to destroy them. Select the RIGHT shield!');
    tutorialStep=3;showTutorial=true;
    showFact('🛰️ Your satellite orbits at 400km — the same altitude as the ISS! It takes 90 minutes to circle Earth once at 7.8 km/s.');
}

function deployShield(type) {
    if (!shields[type]) { toast('❌ '+PQC_INFO[type].name+' not installed! Add it to your rocket next time.'); return; }
    selectedShield = type;
    document.querySelectorAll('.shield-btn').forEach(function(b){b.classList.remove('active');});
    document.getElementById('sb-'+type).classList.add('active');
    setMsg('Selected: '+PQC_INFO[type].emoji+' '+PQC_INFO[type].name+' ('+PQC_INFO[type].fips+') — '+PQC_INFO[type].desc);
}

function spawnAttack() {
    var pqcTypes = ['kyber','dilithium','sphincs','falcon'];
    // Pick attack type (prefer ones the player doesn't have)
    var type = pqcTypes[Math.floor(Math.random()*pqcTypes.length)];
    var info = PQC_INFO[type];
    // Start attack from outside orbit
    var angle = Math.random()*Math.PI*2;
    var startR = 190;
    attacks.push({
        x: W/2+Math.cos(angle)*startR,
        y: H/2+Math.sin(angle)*startR,
        angle: angle, r: startR,
        speed: 0.5+attackWave*0.08,
        type: type, name: info.attack,
        emoji: ['🔐','✍️','🌲','🦅'][pqcTypes.indexOf(type)],
        hp: 2, radius: 12,
        color: ['#ef4444','#f97316','#8b5cf6','#fbbf24'][pqcTypes.indexOf(type)],
        pulse: 0,
    });
}

function tryDestroyAttack(mx, my) {
    if (!selectedShield) { toast('Select a shield first!'); return; }
    attacks.forEach(function(a,i) {
        if (Math.hypot(a.x-mx,a.y-my)<a.radius+10) {
            if (a.type===selectedShield) {
                // Correct shield!
                attacks.splice(i,1);
                orbitScore += 100*(attackWave+1);
                score += 100*(attackWave+1);
                updateHUD();
                pulses.push({x:a.x,y:a.y,r:0,maxR:50,alpha:1,color:PQC_INFO[selectedShield].color||'#10b981'});
                toast('✅ '+PQC_INFO[selectedShield].name+' blocked '+a.name+'! +'+100*(attackWave+1)+' pts!');
                showFact(ATTACK_FACTS[Math.floor(Math.random()*ATTACK_FACTS.length)]);
                confetti();
            } else {
                // Wrong shield!
                toast('❌ Wrong shield! Use '+PQC_INFO[a.type].name+' ('+PQC_INFO[a.type].fips+') against '+a.name+'!');
                satHP -= 10;
                pulses.push({x:a.x,y:a.y,r:0,maxR:40,alpha:1,color:'#ef4444'});
                attacks.splice(i,1);
                if(satHP<=0) endGame();
            }
        }
    });
}

function updateOrbit() {
    if (gameOver) return;
    satAngle += 0.008;
    earthPulse += 0.03;

    // Spawn attacks
    attackTimer++;
    var spawnRate = Math.max(60, 200-attackWave*15);
    if (attackTimer>=spawnRate) {
        attackTimer=0;
        spawnAttack();
        if(attacks.length>3) attackWave++;
    }

    // Move attacks toward satellite
    var satX = W/2+Math.cos(satAngle)*orbitRadius;
    var satY = H/2+Math.sin(satAngle)*orbitRadius;
    attacks.forEach(function(a) {
        var dx=satX-a.x, dy=satY-a.y;
        var d=Math.sqrt(dx*dx+dy*dy)||1;
        a.x+=dx/d*a.speed; a.y+=dy/d*a.speed;
        a.pulse+=0.1;
        // Hit satellite
        if(d<16) {
            satHP=Math.max(0,satHP-15);
            attacks=attacks.filter(function(x){return x!==a;});
            pulses.push({x:satX,y:satY,r:0,maxR:50,alpha:1,color:'#ef4444'});
            setMsg('💥 '+a.name+' hit satellite! HP: '+satHP+'%');
            if(satHP<=0) endGame();
        }
    });

    // Update pulses
    pulses.forEach(function(p){p.r+=4;p.alpha-=0.06;});
    pulses=pulses.filter(function(p){return p.alpha>0;});

    // Update score display
    document.getElementById('h-twr').textContent = satHP+'%';
    document.getElementById('h-twr').style.color = satHP>60?'#10b981':satHP>30?'#fbbf24':'#ef4444';
    updateHUD();
}

// ── END GAME STATE ────────────────────────────────────────────────────────────
var endGameState = null; // null | {won, score, wave, pqcCount, timer}
var endGameTimer = 0;
var restartBtnHit = false;
var playAgainBtn = {x:W/2-70, y:0, w:140, h:34};

function endGame() {
    gameOver = true;
    var pqcCount = Object.keys(shields).length;
    endGameState = {
        won: orbitScore > 200,
        score: score,
        wave: attackWave,
        pqcCount: pqcCount,
        timer: 0,
    };
    document.getElementById('h-phase').textContent = endGameState.won?'VICTORY!':'GAME OVER';
    setMsg(endGameState.won?
        '🏆 Mission success! Score: '+score+' | Waves survived: '+attackWave:
        '💀 Satellite lost! Score: '+score+' | PQC shields: '+pqcCount+'/4');
    showFact('☠️ This is exactly what CNSA 2.0 prevents — quantum-safe encryption must be on every satellite by 2027!');
    if(endGameState.won) confetti();
    // Show HTML play again button
    document.getElementById('play-again-btn').style.display='block';
    document.getElementById('play-again-btn').textContent =
        endGameState.won ?
        '🔄 Play Again — Launch Another Satellite!' :
        '🔄 Try Again — Add More PQC Shields!';
    document.getElementById('play-again-btn').style.background =
        endGameState.won ?
        'linear-gradient(135deg,#059669,#10b981)' :
        'linear-gradient(135deg,#1d4ed8,#3b82f6)';
}

function drawEndGame() {
    if (!endGameState) return;
    endGameState.timer++;

    var won = endGameState.won;
    var t = Math.min(1, endGameState.timer/30); // fade in

    // Dark overlay with fade
    cx.fillStyle = 'rgba(0,0,0,'+(0.82*t)+')';
    cx.fillRect(0,0,W,H);

    // Card
    var cw=380, ch=260, cx2=W/2-cw/2, cy2=H/2-ch/2;
    var cardY = cy2 + (1-t)*30; // slide in from below

    // Card shadow
    cx.fillStyle = 'rgba(0,0,0,0.5)';
    cx.beginPath();
    if(cx.roundRect) cx.roundRect(cx2+4,cardY+4,cw,ch,14); else cx.rect(cx2+4,cardY+4,cw,ch);
    cx.fill();

    // Card body
    var grad = cx.createLinearGradient(cx2,cardY,cx2,cardY+ch);
    grad.addColorStop(0, won?'#071a0e':'#1a0505');
    grad.addColorStop(1, '#071520');
    cx.fillStyle = grad;
    cx.beginPath();
    if(cx.roundRect) cx.roundRect(cx2,cardY,cw,ch,14); else cx.rect(cx2,cardY,cw,ch);
    cx.fill();
    cx.strokeStyle = won?'#10b981':'#ef4444';
    cx.lineWidth = 2; cx.stroke();

    // Animated border glow
    var glow = 0.4+0.4*Math.sin(endGameState.timer*0.1);
    cx.shadowColor = won?'#10b981':'#ef4444';
    cx.shadowBlur = 20*glow;
    cx.strokeStyle = won?'#10b981':'#ef4444';
    cx.stroke();
    cx.shadowBlur = 0;

    // Big emoji
    cx.globalAlpha = t;
    cx.font = '40px serif';
    cx.textAlign = 'center';
    cx.fillText(won?'🏆':'💀', W/2, cardY+52);

    // Title
    cx.font = 'bold 18px sans-serif';
    cx.fillStyle = won?'#10b981':'#ef4444';
    cx.fillText(won?'SATELLITE SECURED!':'SATELLITE LOST!', W/2, cardY+82);

    // Subtitle
    cx.font = '11px sans-serif';
    cx.fillStyle = '#94a3b8';
    cx.fillText(won?'Your PQC shields held against quantum attacks!':'The quantum hackers broke through your defenses!', W/2, cardY+102);

    // Stats row
    var stats = [
        {label:'Score', value:endGameState.score, color:'#fbbf24', emoji:'⭐'},
        {label:'Waves', value:endGameState.wave,  color:'#60a5fa', emoji:'🌊'},
        {label:'PQC',   value:endGameState.pqcCount+'/4', color:'#10b981', emoji:'🔐'},
    ];
    stats.forEach(function(s,i) {
        var sx = cx2+50+i*110;
        cx.fillStyle = '#071520';
        cx.beginPath();
        if(cx.roundRect) cx.roundRect(sx-30,cardY+115,90,50,8); else cx.rect(sx-30,cardY+115,90,50);
        cx.fill();
        cx.strokeStyle = s.color+'40'; cx.lineWidth=1; cx.stroke();
        cx.font='18px serif'; cx.textAlign='center';
        cx.fillText(s.emoji, sx+15, cardY+133);
        cx.font='bold 14px sans-serif'; cx.fillStyle=s.color;
        cx.fillText(s.value, sx+15, cardY+153);
        cx.font='9px sans-serif'; cx.fillStyle='#475569';
        cx.fillText(s.label, sx+15, cardY+163);
    });

    // PQC grade
    var grade = endGameState.pqcCount===4?'A+ QUANTUM SAFE':
                endGameState.pqcCount===3?'B  MOSTLY SAFE':
                endGameState.pqcCount===2?'C  PARTIALLY SAFE':
                endGameState.pqcCount===1?'D  VULNERABLE':'F  CRITICAL RISK';
    var gradeColor = endGameState.pqcCount===4?'#10b981':
                     endGameState.pqcCount>=2?'#fbbf24':'#ef4444';
    cx.fillStyle = gradeColor+'20';
    cx.beginPath();
    if(cx.roundRect) cx.roundRect(cx2+10,cardY+175,cw-20,22,6); else cx.rect(cx2+10,cardY+175,cw-20,22);
    cx.fill();
    cx.font='bold 10px sans-serif'; cx.fillStyle=gradeColor; cx.textAlign='center';
    cx.fillText('PQC SECURITY GRADE: '+grade, W/2, cardY+190);

    // Play Again button
    var btnY = cardY+ch-38;
    playAgainBtn = {x:W/2-70, y:btnY, w:140, h:30};
    var btnHover = false; // static for now
    cx.fillStyle = won?'#059669':'#1d4ed8';
    cx.beginPath();
    if(cx.roundRect) cx.roundRect(W/2-70,btnY,140,30,8); else cx.rect(W/2-70,btnY,140,30);
    cx.fill();
    cx.font='bold 12px sans-serif'; cx.fillStyle='white'; cx.textAlign='center';
    cx.fillText('🔄 Play Again!', W/2, btnY+20);

    cx.globalAlpha = 1;
}

function resetGame() {
    // Full reset
    phase='build';
    rocketParts=[];
    score=0;
    launchAlt=0;launchVel=0;launchFuel=100;
    stageDropped=false;launchDone=false;
    rocketX=W/2;rocketY=H-80;rocketTilt=0;
    exhaust=[];debris=[];
    satAngle=0;satHP=100;attackWave=0;
    attacks=[];shields={};pulses=[];
    orbitScore=0;gameOver=false;
    endGameState=null;
    tutorialStep=0;showTutorial=true;
    throttle=false;
    document.getElementById('h-phase').textContent='BUILD';
    document.getElementById('h-twr').textContent='0.0';
    document.getElementById('h-pqc').textContent='0/4';
    document.getElementById('h-score').textContent='0';
    document.getElementById('pt-build').className='phase-tab active';
    document.getElementById('pt-launch').className='phase-tab';
    document.getElementById('pt-orbit').className='phase-tab';
    document.getElementById('parts-panel').style.display='flex';
    document.getElementById('launch-btn').style.display='none';
    document.getElementById('shield-panel').style.display='none';
    document.getElementById('play-again-btn').style.display='none';
    // Re-enable all shield buttons
    ['kyber','dilithium','sphincs','falcon'].forEach(function(k){
        var btn=document.getElementById('sb-'+k);
        btn.classList.remove('locked','active');
    });
    updateBuildStats();
    setMsg('⚙️ Select parts below and click the canvas to stack them!');
    showFact('🚀 Try to add all 4 PQC modules for maximum satellite security!');
    selectedPart='raptor';
    document.querySelectorAll('.part-btn').forEach(function(b){b.classList.remove('selected');});
    document.getElementById('pb-raptor').classList.add('selected');
}

// ── DRAW ──────────────────────────────────────────────────────────────────────
function draw() {
    cx.clearRect(0,0,W,H);

    if (phase==='build') drawBuild();
    else if (phase==='launch') drawLaunch();
    else if (phase==='orbit') drawOrbit();

    if (showTutorial) drawTutorial();
    if (endGameState) drawEndGame();
}

function drawTutorial() {
    var step = TUTORIAL_STEPS[Math.min(tutorialStep, TUTORIAL_STEPS.length-1)];
    if (!step || step.phase !== phase) return;

    // Dark overlay
    cx.fillStyle = 'rgba(0,0,0,0.75)';
    cx.fillRect(0,0,W,H);

    // Tutorial card
    var cw=420, ch=240, cx2=W/2-cw/2, cy2=H/2-ch/2;
    cx.fillStyle = '#071520';
    cx.beginPath();
    cx.roundRect(cx2,cy2,cw,ch,12);
    cx.fill();
    cx.strokeStyle = step.color;
    cx.lineWidth = 2;
    cx.stroke();

    // Title
    cx.font = 'bold 14px sans-serif';
    cx.fillStyle = step.color;
    cx.textAlign = 'center';
    cx.fillText(step.title, W/2, cy2+28);

    // Lines
    cx.font = '11px sans-serif';
    cx.textAlign = 'left';
    step.lines.forEach(function(line, i) {
        cx.fillStyle = '#e2e8f0';
        cx.fillText(line, cx2+16, cy2+56+i*26);
    });

    // Tip box
    cx.fillStyle = step.color+'20';
    cx.fillRect(cx2+10, cy2+ch-58, cw-20, 26);
    cx.font = '10px sans-serif';
    cx.fillStyle = step.color;
    cx.textAlign = 'center';
    cx.fillText('💡 ' + step.tip, W/2, cy2+ch-40);

    // Progress dots
    TUTORIAL_STEPS.forEach(function(s,i) {
        cx.beginPath();
        cx.arc(W/2-(TUTORIAL_STEPS.length-1)*10+i*20, cy2+ch-16, 4, 0, 6.28);
        cx.fillStyle = i===tutorialStep ? step.color : '#334155';
        cx.fill();
    });

    // Buttons
    // Next button
    cx.fillStyle = step.color;
    cx.beginPath();
    cx.roundRect(W/2+20, cy2+ch-35, 120, 26, 6);
    cx.fill();
    cx.font = 'bold 11px sans-serif';
    cx.fillStyle = 'white';
    cx.textAlign = 'center';
    cx.fillText(tutorialStep<TUTORIAL_STEPS.length-1?'Next →':'Got it! ✓', W/2+80, cy2+ch-17);

    // Skip button
    cx.fillStyle = '#334155';
    cx.beginPath();
    cx.roundRect(W/2-140, cy2+ch-35, 110, 26, 6);
    cx.fill();
    cx.fillStyle = '#94a3b8';
    cx.fillText('Skip Tutorial', W/2-85, cy2+ch-17);
}

function drawBuild() {
    // Space background
    cx.fillStyle='#020d14';cx.fillRect(0,0,W,H);
    drawStars();

    // Launch pad
    cx.fillStyle='#0a1f35';cx.fillRect(0,H-50,W,50);
    cx.fillStyle='#1a3a5a';cx.fillRect(W/2-40,H-50,80,10);
    cx.fillStyle='#334155';
    for(var i=0;i<5;i++) cx.fillRect(W/2-35+i*16,H-50,8,50);

    // Draw rocket parts stacked
    var startY = H-60;
    var rw = 40; // rocket width
    rocketParts.forEach(function(pType,i) {
        var p = PARTS[pType];
        var y = startY - i*p.h - p.h;
        var x = W/2 - rw/2;

        // Part body
        cx.fillStyle = p.color+'cc';
        if (cx.roundRect) cx.roundRect.call(cx,x,y,rw,p.h,4);
        else cx.rect(x,y,rw,p.h);
        cx.fill();
        cx.strokeStyle=p.color;cx.lineWidth=1.5;cx.stroke();

        // Part emoji + name
        cx.font='16px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(p.emoji,W/2,y+p.h*0.4);
        cx.font='8px sans-serif';cx.fillStyle='white';
        cx.fillText(p.name,W/2,y+p.h*0.75);

        // PQC glow
        if(p.pqc){cx.shadowColor='#10b981';cx.shadowBlur=10;cx.strokeRect(x,y,rw,p.h);cx.shadowBlur=0;}

        startY = startY;
    });

    // TWR meter
    var twr = getTWR();
    var meterX=10,meterY=10,meterW=100,meterH=12;
    cx.fillStyle='#1e293b';cx.fillRect(meterX,meterY,meterW,meterH);
    cx.fillStyle=twr>=1.2?'#10b981':twr>=0.8?'#fbbf24':'#ef4444';
    cx.fillRect(meterX,meterY,Math.min(meterW,meterW*twr/2),meterH);
    cx.strokeStyle='#334155';cx.lineWidth=1;cx.strokeRect(meterX,meterY,meterW,meterH);
    cx.font='9px sans-serif';cx.fillStyle='white';cx.textAlign='left';
    cx.fillText('TWR: '+twr.toFixed(2)+(twr>=1.2?' ✅':' ❌ Need >1.2'),meterX+2,meterY+meterH+12);

    // PQC shield indicator
    var pqcList=['kyber','dilithium','sphincs','falcon'];
    var pqcOwned=getPQCModules();
    pqcList.forEach(function(k,i){
        var info=PQC_INFO[k];
        cx.font='11px serif';cx.textAlign='left';
        cx.fillStyle=pqcOwned[k]?'#10b981':'#334155';
        cx.fillText((pqcOwned[k]?'✅':'⬜')+info.name,W-130,15+i*16);
    });

    // Instructions overlay when empty
    if(rocketParts.length===0){
        cx.font='bold 13px sans-serif';cx.fillStyle='#60a5fa';cx.textAlign='center';
        cx.fillText('👆 Click canvas to place selected part!',W/2,H/2-10);
        cx.font='10px sans-serif';cx.fillStyle='#475569';
        cx.fillText('Build from bottom up: Engine → Fuel → PQC Modules → Satellite',W/2,H/2+15);
    }

    // Mission deadline banner
    cx.fillStyle='rgba(220,38,38,0.12)';cx.fillRect(0,H-90,W,28);
    cx.font='bold 10px sans-serif';cx.fillStyle='#ef4444';cx.textAlign='center';
    cx.fillText('⚠️ NSA CNSA 2.0: ALL satellites must be quantum-safe by January 2027!',W/2,H-72);

    // Selected part highlight box
    var sp=PARTS[selectedPart];
    cx.fillStyle='#071520';
    cx.beginPath();if(cx.roundRect)cx.roundRect(W-130,H-95,125,60,8);else cx.rect(W-130,H-95,125,60);
    cx.fill();
    cx.strokeStyle=sp.pqc?'#10b981':'#3b82f6';cx.lineWidth=1.5;cx.stroke();
    cx.font='20px serif';cx.textAlign='center';
    cx.fillText(sp.emoji,W-67,H-72);
    cx.font='9px sans-serif';cx.fillStyle='white';
    cx.fillText(sp.name,W-67,H-53);
    cx.fillStyle=sp.pqc?'#10b981':sp.thrust>0?'#ef4444':'#60a5fa';
    cx.fillText(sp.pqc?'🔐 PQC SHIELD':sp.thrust>0?'⚡ THRUST: +'+sp.thrust:'⚖️ WEIGHT: '+sp.weight,W-67,H-42);
}

function drawLaunch() {
    // Sky gradient based on altitude
    var skyAlpha = Math.min(1,launchAlt/100);
    var sky=cx.createLinearGradient(0,0,0,H);
    sky.addColorStop(0,'rgb('+Math.round(2+skyAlpha*0)+','+Math.round(13+skyAlpha*0)+','+Math.round(20+skyAlpha*0)+')');
    sky.addColorStop(1,'rgb('+Math.round(2+(1-skyAlpha)*100)+','+Math.round(13+(1-skyAlpha)*100)+','+Math.round(20+(1-skyAlpha)*150)+')');
    cx.fillStyle=sky;cx.fillRect(0,0,W,H);

    // Stars appear as we go higher
    if(launchAlt>30) { cx.globalAlpha=(launchAlt-30)/70; drawStars(); cx.globalAlpha=1; }

    // Earth curve at bottom
    if(launchAlt<80){
        cx.fillStyle='rgb('+Math.round(10+(1-launchAlt/100)*20)+','+Math.round(31+(1-launchAlt/100)*60)+','+Math.round(53)+')';;
        cx.fillRect(0,H-50*(1-launchAlt/100),W,50);
        cx.fillStyle='#166534';
        cx.fillRect(0,H-30*(1-launchAlt/100),W,15);
    }

    // Clouds
    if(launchAlt<30){
        cx.fillStyle='rgba(255,255,255,'+(0.3*(1-launchAlt/30))+')';
        [80,200,350,480].forEach(function(cx2){
            cx.beginPath();cx.ellipse(cx2,cloudY+launchAlt*2,40,15,0,0,Math.PI*2);cx.fill();
        });
    }

    // Max-Q warning zone
    if(maxQ){
        cx.fillStyle='rgba(239,68,68,0.05)';cx.fillRect(0,0,W,H);
        cx.font='bold 12px sans-serif';cx.fillStyle='#ef4444';cx.textAlign='center';
        cx.fillText('⚠️ MAX-Q — MAXIMUM AERODYNAMIC STRESS!',W/2,30);
    }

    // Space debris
    debris.forEach(function(d){
        cx.fillStyle=d.color;
        cx.beginPath();cx.arc(d.x,d.y,d.r,0,6.28);cx.fill();
    });

    // Exhaust
    exhaust.forEach(function(p){
        cx.beginPath();cx.arc(p.x,p.y,p.r,0,6.28);
        cx.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,'0');
        cx.fill();
    });

    // Altitude marker
    var altMarkers=[10,20,40,60,100];
    altMarkers.forEach(function(alt){
        var screenY=H-80-(alt/100)*(H-100);
        if(screenY>0&&screenY<H){
            cx.strokeStyle='#1a3a5a30';cx.lineWidth=1;cx.setLineDash([4,4]);
            cx.beginPath();cx.moveTo(0,screenY);cx.lineTo(W,screenY);cx.stroke();
            cx.setLineDash([]);
            cx.font='9px sans-serif';cx.fillStyle='#475569';cx.textAlign='left';
            cx.fillText(alt+'km'+(alt===40?' ← MAX-Q':alt===60?' ← STAGING':alt===100?' ← ORBIT':''),4,screenY-2);
        }
    });

    // Rocket
    cx.save();
    cx.translate(rocketX,rocketY);
    cx.rotate(rocketTilt);
    // Flame
    if(throttle&&launchFuel>0){
        cx.beginPath();
        cx.moveTo(-8,30);cx.lineTo(8,30);cx.lineTo(0,55+Math.random()*15);
        cx.fillStyle='#f97316';cx.fill();
        cx.beginPath();
        cx.moveTo(-4,30);cx.lineTo(4,30);cx.lineTo(0,45+Math.random()*10);
        cx.fillStyle='#fbbf24';cx.fill();
    }
    // Body
    cx.fillStyle='#e2e8f0';cx.fillRect(-10,-30,20,60);
    cx.fillStyle='#94a3b8';cx.fillRect(-10,-30,20,60);
    // Nose cone
    cx.beginPath();cx.moveTo(-10,-30);cx.lineTo(10,-30);cx.lineTo(0,-50);cx.closePath();
    cx.fillStyle='#f1f5f9';cx.fill();
    // Stage line
    if(stageDropped){cx.strokeStyle='#ef4444';cx.lineWidth=1;cx.setLineDash([2,2]);
        cx.beginPath();cx.moveTo(-11,0);cx.lineTo(11,0);cx.stroke();cx.setLineDash([]);}
    // Fins
    cx.fillStyle='#64748b';
    cx.beginPath();cx.moveTo(-10,20);cx.lineTo(-20,35);cx.lineTo(-10,30);cx.closePath();cx.fill();
    cx.beginPath();cx.moveTo(10,20);cx.lineTo(20,35);cx.lineTo(10,30);cx.closePath();cx.fill();
    // Altitude progress
    var progH=H*0.8;
    cx.fillStyle='#1e293b';cx.fillRect(W/2-60+12,-H/2+20,8,progH);
    cx.fillStyle='#10b981';cx.fillRect(W/2-60+12,-H/2+20+(1-launchAlt/100)*progH,8,launchAlt/100*progH);
    cx.restore();

    // Altitude progress bar (right side)
    var barX=W-18, barH=H*0.65, barY=(H-barH)/2;
    cx.fillStyle='#1e293b';cx.fillRect(barX,barY,10,barH);
    var fillH = (launchAlt/100)*barH;
    var barGrad=cx.createLinearGradient(0,barY+barH,0,barY);
    barGrad.addColorStop(0,'#3b82f6');barGrad.addColorStop(0.6,'#10b981');barGrad.addColorStop(1,'#fbbf24');
    cx.fillStyle=barGrad;cx.fillRect(barX,barY+barH-fillH,10,fillH);
    cx.strokeStyle='#334155';cx.lineWidth=1;cx.strokeRect(barX,barY,10,barH);
    // Target marker
    cx.fillStyle='#fbbf24';cx.fillRect(barX-4,barY,18,2);
    cx.font='8px sans-serif';cx.fillStyle='#fbbf24';cx.textAlign='right';
    cx.fillText('ORBIT',barX-2,barY+8);
    cx.font='9px sans-serif';cx.fillStyle='#10b981';cx.textAlign='right';
    cx.fillText(launchAlt.toFixed(0)+'km',barX-2,barY+barH-fillH+14);

    // Throttle hint
    if(!throttle){
        cx.font='12px sans-serif';cx.fillStyle='#fbbf24';cx.textAlign='center';
        cx.fillText('Click/Hold to THROTTLE! →',W/2,H-15);
    }

    // Fuel gauge
    cx.fillStyle='#1e293b';cx.fillRect(10,H-25,120,10);
    cx.fillStyle=launchFuel>30?'#10b981':'#ef4444';
    cx.fillRect(10,H-25,launchFuel*1.2,10);
    cx.font='9px sans-serif';cx.fillStyle='white';cx.textAlign='left';
    cx.fillText('FUEL: '+launchFuel.toFixed(0)+'%',12,H-28);
}

function drawOrbit() {
    // Deep space background
    cx.fillStyle='#020408';cx.fillRect(0,0,W,H);
    drawStars();

    // Earth
    earthPulse+=0.02;
    var earthR=80;
    var eg=cx.createRadialGradient(W/2,H/2,20,W/2,H/2,earthR);
    eg.addColorStop(0,'#1d4ed8');
    eg.addColorStop(0.6,'#166534');
    eg.addColorStop(1,'#0f172a');
    cx.beginPath();cx.arc(W/2,H/2,earthR,0,6.28);
    cx.fillStyle=eg;cx.fill();
    cx.strokeStyle='#3b82f630';cx.lineWidth=2;cx.stroke();
    // Atmosphere glow
    cx.beginPath();cx.arc(W/2,H/2,earthR+8,0,6.28);
    cx.strokeStyle='rgba(59,130,246,0.2)';cx.lineWidth=6;cx.stroke();
    // Cloud wisps on earth
    cx.fillStyle='rgba(255,255,255,0.1)';
    cx.beginPath();cx.ellipse(W/2-20,H/2-30,25,8,0.5,0,6.28);cx.fill();
    cx.beginPath();cx.ellipse(W/2+30,H/2+20,20,7,-0.3,0,6.28);cx.fill();

    // Orbit path
    cx.beginPath();cx.arc(W/2,H/2,orbitRadius,0,6.28);
    cx.strokeStyle='#1d4ed820';cx.lineWidth=1.5;cx.setLineDash([5,5]);cx.stroke();
    cx.setLineDash([]);

    // HP ring around earth
    cx.beginPath();cx.arc(W/2,H/2,earthR+15,0,(satHP/100)*6.28);
    cx.strokeStyle=satHP>60?'#10b981':satHP>30?'#fbbf24':'#ef4444';
    cx.lineWidth=3;cx.stroke();

    // Attack warning arrows at edge of screen pointing toward satellite
    var satX2=W/2+Math.cos(satAngle)*orbitRadius;
    var satY2=H/2+Math.sin(satAngle)*orbitRadius;
    attacks.forEach(function(a) {
        var dx=satX2-a.x, dy=satY2-a.y;
        var d=Math.sqrt(dx*dx+dy*dy)||1;
        // Draw arrow line from attack toward satellite
        cx.beginPath();
        cx.setLineDash([4,4]);
        cx.moveTo(a.x,a.y);
        cx.lineTo(a.x+dx/d*20,a.y+dy/d*20);
        cx.strokeStyle=a.color+'40';cx.lineWidth=1;cx.stroke();
        cx.setLineDash([]);
    });

    // Attacks
    attacks.forEach(function(a){
        var glow=0.5+0.5*Math.sin(a.pulse);
        cx.shadowColor=a.color;cx.shadowBlur=10*glow;
        cx.font='18px serif';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(a.emoji,a.x,a.y);
        cx.shadowBlur=0;
        // Attack label
        cx.font='8px sans-serif';cx.fillStyle=a.color;
        cx.fillText(a.name,a.x,a.y+16);
    });

    // Pulses
    pulses.forEach(function(p){
        cx.beginPath();cx.arc(p.x,p.y,p.r,0,6.28);
        cx.strokeStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,'0');
        cx.lineWidth=3;cx.stroke();
    });

    // Satellite
    var satX=W/2+Math.cos(satAngle)*orbitRadius;
    var satY=H/2+Math.sin(satAngle)*orbitRadius;

    // Shield glow around satellite
    if(selectedShield&&shields[selectedShield]){
        cx.shadowColor=PQC_INFO[selectedShield].color||'#10b981';
        cx.shadowBlur=20;
    }
    cx.font='20px serif';cx.textAlign='center';cx.textBaseline='middle';
    cx.fillText('🛰️',satX,satY);
    cx.shadowBlur=0;

    // PQC shields display
    var ownedShields=Object.keys(shields);
    ownedShields.forEach(function(k,i){
        var info=PQC_INFO[k];
        cx.font='10px sans-serif';cx.fillStyle='#10b981';cx.textAlign='left';
        cx.fillText('✅ '+info.name+' ('+info.fips+')',5,15+i*14);
    });

    // Missing shields warning
    var missing=['kyber','dilithium','sphincs','falcon'].filter(function(k){return !shields[k];});
    missing.forEach(function(k,i){
        var info=PQC_INFO[k];
        cx.font='10px sans-serif';cx.fillStyle='#ef4444';cx.textAlign='left';
        cx.fillText('❌ '+info.name+' MISSING — vulnerable to '+info.attack,5,H-5-i*14);
    });

    // Wave counter
    cx.font='10px sans-serif';cx.fillStyle='#fbbf24';cx.textAlign='right';
    cx.fillText('🌊 Wave '+attackWave+' | Defense: '+orbitScore,W-5,15);
}

function drawStars() {
    stars.forEach(function(s){
        s.twinkle+=0.02;
        cx.beginPath();cx.arc(s.x,s.y,s.r,0,6.28);
        cx.fillStyle='rgba(255,255,255,'+(s.alpha*(0.5+0.5*Math.sin(s.twinkle)))+')';
        cx.fill();
    });
}

// ── HELPERS ───────────────────────────────────────────────────────────────────
function updateHUD() {
    document.getElementById('h-score').textContent=score;
    document.getElementById('h-pqc').textContent=Object.keys(shields).length+'/4';
}
function setMsg(m){document.getElementById('msg').textContent=m;}
var _ft=null;
function showFact(t){var el=document.getElementById('fact');el.textContent=t;el.style.display='block';if(_ft)clearTimeout(_ft);_ft=setTimeout(function(){el.style.display='none';},7000);}
var _tt=null;
function toast(m){var el=document.getElementById('toast');el.textContent=m;el.classList.add('show');if(_tt)clearTimeout(_tt);_tt=setTimeout(function(){el.classList.remove('show');},3000);}
function confetti(){var c=['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444'];for(var i=0;i<20;i++){setTimeout(function(){var el=document.createElement('div');el.className='cp';el.style.left=Math.random()*100+'vw';el.style.background=c[Math.floor(Math.random()*c.length)];el.style.animationDuration=(1+Math.random()*2)+'s';document.body.appendChild(el);setTimeout(function(){el.remove();},3000);},i*40);}}

// ── GAME LOOP ─────────────────────────────────────────────────────────────────
function update() {
    if (phase==='launch') updateLaunch();
    else if (phase==='orbit') updateOrbit();
}
function loop(){requestAnimationFrame(loop);update();draw();}

// ── INIT ─────────────────────────────────────────────────────────────────────
updateBuildStats();
setMsg('⚙️ Select parts below and click the canvas to stack them! Build TWR > 1.2 to launch.');
showFact('🚀 Real rocket science: TWR (Thrust-to-Weight Ratio) must exceed 1.0 to lift off! SpaceX Falcon 9 has a TWR of about 1.3 at liftoff. NASA SLS has a TWR of 1.5!');
loop();
</script>
</body>
</html>
""", height=700)
