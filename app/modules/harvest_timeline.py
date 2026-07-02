def render_harvest_timeline():
    """Interactive Harvest Now Decrypt Later threat timeline visualization."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("☠️ Harvest Now, Decrypt Later — The Quantum Threat Clock")
    st.markdown(
        "**The most dangerous quantum attack is already happening TODAY.** "
        "Nation-state hackers are recording your encrypted data RIGHT NOW "
        "to decrypt it when quantum computers arrive. This timeline shows why PQC can't wait."
    )

    components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;color:white;padding:16px;overflow-x:hidden;}

/* TABS */
.tabs{display:flex;gap:4px;margin-bottom:16px;}
.tab{flex:1;padding:8px;border-radius:8px;border:1px solid #1a3a5a;background:#071520;
    color:#60a5fa;font-size:11px;font-weight:bold;cursor:pointer;text-align:center;}
.tab.active{background:#dc2626;border-color:#ef4444;color:white;}

/* TIMELINE */
#timeline-section{}
.tl-wrap{position:relative;padding:10px 0;}
.tl-line{position:absolute;left:50%;top:0;bottom:0;width:3px;
    background:linear-gradient(180deg,#1d4ed8,#7c3aed,#dc2626);
    transform:translateX(-50%);}
.tl-item{display:flex;margin-bottom:20px;position:relative;align-items:flex-start;}
.tl-item.left{flex-direction:row-reverse;}
.tl-content{width:44%;background:#071520;border-radius:10px;padding:12px 14px;
    position:relative;transition:all 0.3s;}
.tl-content:hover{transform:scale(1.02);}
.tl-item.left .tl-content{margin-right:6%;}
.tl-item.right .tl-content{margin-left:6%;}
.tl-dot{position:absolute;left:50%;top:12px;width:16px;height:16px;border-radius:50%;
    transform:translateX(-50%);z-index:2;border:3px solid #020d14;}
.tl-year{font-size:18px;font-weight:bold;margin-bottom:4px;}
.tl-title{font-size:12px;font-weight:bold;margin-bottom:6px;}
.tl-desc{font-size:10px;color:#94a3b8;line-height:1.6;}
.tl-badge{display:inline-block;padding:2px 8px;border-radius:10px;
    font-size:8px;font-weight:bold;margin-top:6px;margin-right:4px;}
.tl-threat{background:#300;color:#ef4444;border:1px solid #ef4444;}
.tl-safe{background:#052e16;color:#10b981;border:1px solid #10b981;}
.tl-warn{background:#451a03;color:#f59e0b;border:1px solid #f59e0b;}
.tl-info{background:#1e3a5f;color:#60a5fa;border:1px solid #60a5fa;}

/* ANIMATED THREAT INDICATOR */
.pulse-red{animation:pulseR 1.5s infinite;}
@keyframes pulseR{0%,100%{box-shadow:0 0 0 0 rgba(239,68,68,0.7);}50%{box-shadow:0 0 0 8px rgba(239,68,68,0);}}
.pulse-green{animation:pulseG 1.5s infinite;}
@keyframes pulseG{0%,100%{box-shadow:0 0 0 0 rgba(16,185,129,0.7);}50%{box-shadow:0 0 0 8px rgba(16,185,129,0);}}

/* HARVEST VISUALIZER */
#harvest-section{display:none;}
.harvest-scene{background:#0a1520;border:1px solid #1a3a5a;border-radius:12px;
    padding:16px;margin-bottom:12px;}
.harvest-title{font-size:13px;font-weight:bold;color:#ef4444;margin-bottom:10px;}
.data-packet{display:inline-block;padding:4px 10px;border-radius:6px;margin:3px;
    font-size:9px;font-weight:bold;cursor:pointer;transition:all 0.3s;}
.packet-encrypted{background:#1d4ed820;border:1px solid #1d4ed8;color:#60a5fa;}
.packet-stolen{background:#30000080;border:1px solid #ef4444;color:#ef4444;
    animation:stolen 0.5s ease;}
@keyframes stolen{0%{transform:scale(1);}50%{transform:scale(1.3);}100%{transform:scale(1);}}
.vault-icon{font-size:2rem;margin:8px 0;}
.progress-bar-wrap{background:#1e293b;border-radius:6px;height:12px;margin:6px 0;overflow:hidden;}
.progress-bar-fill{height:100%;border-radius:6px;transition:width 1s ease;}
.step-box{background:#071520;border-radius:10px;padding:10px 14px;margin-bottom:8px;
    border-left:3px solid #1a3a5a;}
.step-box.active-step{border-left-color:#ef4444;background:#1a0505;}
.step-num{font-size:10px;color:#475569;margin-bottom:3px;}
.step-title{font-size:11px;font-weight:bold;}
.step-desc{font-size:9px;color:#94a3b8;margin-top:3px;line-height:1.5;}

/* IMPACT CALCULATOR */
#impact-section{display:none;}
.calc-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;}
.calc-box{background:#071520;border:1px solid #1a3a5a;border-radius:10px;padding:12px;}
.calc-box label{font-size:9px;color:#94a3b8;display:block;margin-bottom:4px;}
.calc-box select,.calc-box input{width:100%;background:#0a1f35;border:1px solid #1a3a5a;
    border-radius:6px;color:white;padding:5px 8px;font-size:10px;}
#impact-result{background:#071520;border:2px solid #ef4444;border-radius:12px;
    padding:14px;text-align:center;display:none;}
.impact-score{font-size:2.5rem;font-weight:bold;}
.impact-label{font-size:11px;color:#94a3b8;margin-top:4px;}
.impact-detail{font-size:10px;color:#94a3b8;margin-top:8px;line-height:1.6;}
.risk-meter{display:flex;gap:2px;margin:8px 0;}
.risk-block{flex:1;height:16px;border-radius:2px;background:#1e293b;transition:all 0.5s;}
.risk-block.filled-low{background:#10b981;}
.risk-block.filled-mid{background:#f59e0b;}
.risk-block.filled-high{background:#ef4444;}
.calc-btn{width:100%;padding:10px;background:linear-gradient(135deg,#dc2626,#ef4444);
    border:none;border-radius:8px;color:white;font-size:12px;font-weight:bold;
    cursor:pointer;margin-top:8px;}

/* LIVE COUNTER */
.counter-wrap{background:#0a0505;border:1px solid #ef444440;border-radius:10px;
    padding:12px;text-align:center;margin-bottom:12px;}
.counter-num{font-size:2rem;font-weight:bold;color:#ef4444;font-family:monospace;}
.counter-label{font-size:10px;color:#94a3b8;}
</style>
</head>
<body>

<div class="tabs">
    <div class="tab active" onclick="showTab('timeline')">📅 Threat Timeline</div>
    <div class="tab" onclick="showTab('harvest')">☠️ How It Works</div>
    <div class="tab" onclick="showTab('impact')">💀 Impact Calculator</div>
</div>

<!-- ═══ TIMELINE ═══════════════════════════════════════════════════════════ -->
<div id="timeline-section">

<div class="counter-wrap">
    <div class="counter-num" id="live-counter">0</div>
    <div class="counter-label">⚠️ Estimated encrypted records harvested by nation-states TODAY</div>
</div>

<div class="tl-wrap">
<div class="tl-line"></div>

<div class="tl-item left">
    <div class="tl-content" style="border:1px solid #1d4ed8">
        <div class="tl-year" style="color:#60a5fa">2013–NOW</div>
        <div class="tl-title">🕵️ HARVEST PHASE — Active RIGHT NOW</div>
        <div class="tl-desc">NSA PRISM, China's Volt Typhoon, Russia's Cozy Bear — nation-state hackers 
        intercept and STORE encrypted internet traffic. They can't read it yet. They don't need to. 
        They're building massive databases of today's encrypted secrets.</div>
        <span class="tl-badge tl-threat pulse-red">🔴 HAPPENING NOW</span>
        <span class="tl-badge tl-info">NSA PRISM Documents</span>
        <span class="tl-badge tl-info">Volt Typhoon 2024</span>
    </div>
    <div class="tl-dot pulse-red" style="background:#ef4444"></div>
</div>

<div class="tl-item right">
    <div class="tl-content" style="border:1px solid #f59e0b">
        <div class="tl-year" style="color:#f59e0b">2016</div>
        <div class="tl-title">🏛️ NIST Starts PQC Competition</div>
        <div class="tl-desc">NIST launches the Post-Quantum Cryptography standardization process. 
        69 algorithms submitted. The world acknowledges quantum computers WILL break RSA and ECC. 
        The 8-year race to find replacements begins.</div>
        <span class="tl-badge tl-warn">⚠️ WAKE UP CALL</span>
        <span class="tl-badge tl-info">69 Submissions</span>
    </div>
    <div class="tl-dot" style="background:#f59e0b"></div>
</div>

<div class="tl-item left">
    <div class="tl-content" style="border:1px solid #8b5cf6">
        <div class="tl-year" style="color:#8b5cf6">2022</div>
        <div class="tl-title">📜 NSA CNSA 2.0 Mandate</div>
        <div class="tl-desc">NSA releases Commercial National Security Algorithm Suite 2.0. 
        ALL National Security Systems must migrate to PQC. Deadline: 2030 for most systems, 
        2033 for protocols, 2035 for software signing. The US government officially declares 
        RSA and ECC obsolete for classified use.</div>
        <span class="tl-badge tl-warn">⚠️ GOVERNMENT MANDATE</span>
        <span class="tl-badge tl-info">NSA CNSA 2.0</span>
    </div>
    <div class="tl-dot" style="background:#8b5cf6"></div>
</div>

<div class="tl-item right">
    <div class="tl-content" style="border:1px solid #10b981">
        <div class="tl-year" style="color:#10b981">2024</div>
        <div class="tl-title">✅ NIST Finalizes PQC Standards</div>
        <div class="tl-desc">August 13, 2024 — NIST publishes FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), 
        and FIPS 205 (SLH-DSA). The quantum-safe algorithms are READY. Google Chrome deploys 
        ML-KEM for 20% of all TLS connections. Cloudflare, AWS, and Apple begin migration.</div>
        <span class="tl-badge tl-safe">✅ SOLUTION EXISTS</span>
        <span class="tl-badge tl-info">FIPS 203/204/205</span>
        <span class="tl-badge tl-info">Chrome Deployed</span>
    </div>
    <div class="tl-dot pulse-green" style="background:#10b981"></div>
</div>

<div class="tl-item left">
    <div class="tl-content" style="border:1px solid #f59e0b">
        <div class="tl-year" style="color:#f59e0b">2027</div>
        <div class="tl-title">⏰ NSA Compliance Deadline</div>
        <div class="tl-desc">All new National Security System acquisitions MUST be quantum-safe. 
        Satellites, military comms, banking infrastructure — all must have PQC implemented. 
        Any system still using RSA or ECC for classified data is non-compliant. 
        Estimated 80% of Fortune 500 companies still not migrated at this date.</div>
        <span class="tl-badge tl-warn">⏰ DEADLINE</span>
        <span class="tl-badge tl-threat">80% Not Ready</span>
    </div>
    <div class="tl-dot" style="background:#f59e0b"></div>
</div>

<div class="tl-item right">
    <div class="tl-content" style="border:1px solid #ef4444">
        <div class="tl-year" style="color:#ef4444">2030–2035</div>
        <div class="tl-title">💀 CRYPTOGRAPHICALLY RELEVANT QUANTUM COMPUTER</div>
        <div class="tl-desc">A quantum computer with ~4,000 error-corrected qubits can run Shor Algorithm 
        and break RSA-2048 in hours. IBM projects 100,000 qubit systems by 2033. 
        Google achieved quantum supremacy milestones ahead of schedule. 
        Every piece of data harvested since 2013 becomes readable INSTANTLY.</div>
        <span class="tl-badge tl-threat pulse-red">💀 DECRYPT EVERYTHING</span>
        <span class="tl-badge tl-threat">10+ Years of Data Exposed</span>
    </div>
    <div class="tl-dot pulse-red" style="background:#ef4444"></div>
</div>

<div class="tl-item left">
    <div class="tl-content" style="border:1px solid #10b981">
        <div class="tl-year" style="color:#10b981">2035+</div>
        <div class="tl-title">🛡️ PQC-Protected World</div>
        <div class="tl-desc">Organizations that deployed ML-KEM, ML-DSA, and SLH-DSA before quantum 
        computers arrived are SAFE. Their harvested data is still encrypted with lattice math 
        that quantum computers cannot break. Early movers have a permanent security advantage. 
        This is why the students learning PQC TODAY are the cybersecurity heroes of tomorrow.</div>
        <span class="tl-badge tl-safe">✅ PROTECTED</span>
        <span class="tl-badge tl-safe">Lattice Math Holds</span>
    </div>
    <div class="tl-dot pulse-green" style="background:#10b981"></div>
</div>

</div>
</div>

<!-- ═══ HOW IT WORKS ════════════════════════════════════════════════════════ -->
<div id="harvest-section">
<div class="harvest-scene">
    <div class="harvest-title">☠️ Harvest Now, Decrypt Later — Step by Step</div>

    <div class="step-box active-step" id="step1">
        <div class="step-num">STEP 1 — TODAY (2024)</div>
        <div class="step-title">🌐 You send encrypted data across the internet</div>
        <div class="step-desc">Every HTTPS connection, every email, every bank transfer — encrypted with RSA or ECC. 
        You think it's safe because no classical computer can break it in your lifetime.</div>
    </div>

    <div class="step-box" id="step2">
        <div class="step-num">STEP 2 — SIMULTANEOUSLY (2024)</div>
        <div class="step-title">🕵️ Nation-state hackers intercept and STORE your encrypted data</div>
        <div class="step-desc">Tapped fiber optic cables, compromised ISPs, mass surveillance programs — 
        encrypted packets are copied into massive data warehouses. The NSA PRISM program, 
        China's Great Firewall interception, Russia's SORM system. They store EVERYTHING.</div>
    </div>

    <div class="step-box" id="step3">
        <div class="step-num">STEP 3 — 2030-2035</div>
        <div class="step-title">💻 Quantum computer runs Shor Algorithm</div>
        <div class="step-desc">A cryptographically relevant quantum computer factors the large primes 
        that RSA depends on. What takes classical computers billions of years takes this machine 
        hours. Every RSA key ever used is now breakable.</div>
    </div>

    <div class="step-box" id="step4">
        <div class="step-num">STEP 4 — THE DECRYPT</div>
        <div class="step-title">💀 10+ years of your secrets become readable instantly</div>
        <div class="step-desc">Medical records from 2020. Financial transactions from 2019. 
        Government communications from 2015. Military intelligence from 2013. 
        All of it — decrypted and readable. The harvest paid off.</div>
    </div>

    <div class="step-box" id="step5" style="border-left-color:#10b981">
        <div class="step-num">THE DEFENSE</div>
        <div class="step-title" style="color:#10b981">🔐 Deploy PQC NOW — before the quantum computer arrives</div>
        <div class="step-desc">Data encrypted with ML-KEM today is safe EVEN IF a quantum computer 
        arrives tomorrow. Lattice-based cryptography cannot be broken by Shor Algorithm. 
        The window to protect yourself is NOW — before the harvest becomes the decrypt.</div>
    </div>

    <div style="text-align:center;margin-top:12px;">
        <button onclick="animateSteps()" style="padding:8px 20px;background:linear-gradient(135deg,#dc2626,#ef4444);border:none;border-radius:8px;color:white;font-size:11px;font-weight:bold;cursor:pointer;">
            ▶ Animate the Attack
        </button>
    </div>
</div>

<div class="harvest-scene">
    <div class="harvest-title">📦 What Data Is Being Harvested RIGHT NOW?</div>
    <div style="font-size:9px;color:#94a3b8;margin-bottom:8px">Click a data type to see if it's at risk:</div>
    <div id="data-packets">
        <div class="data-packet packet-encrypted" onclick="showRisk(this,'Medical Records','RSA-2048','CRITICAL — 30 year retention requirement. Your 2024 records readable in 2033.')">🏥 Medical Records</div>
        <div class="data-packet packet-encrypted" onclick="showRisk(this,'Bank Transactions','TLS 1.3 + ECDH','HIGH — Financial history exposed. Account recovery questions never expire.')">🏦 Bank Transfers</div>
        <div class="data-packet packet-encrypted" onclick="showRisk(this,'Government Comms','RSA-4096','CRITICAL — National security data. NSA already migrating to PQC.')">🏛️ Gov Communications</div>
        <div class="data-packet packet-encrypted" onclick="showRisk(this,'GPS/Satellite Data','ECC-256','HIGH — Navigation signals authenticated with ECC. Spoofable post-quantum.')">🛰️ Satellite Data</div>
        <div class="data-packet packet-encrypted" onclick="showRisk(this,'Email','RSA/TLS','MEDIUM-HIGH — SMTP still uses RSA. Corporate email archives at risk.')">📧 Email</div>
        <div class="data-packet packet-encrypted" onclick="showRisk(this,'Software Updates','RSA-PSS','CRITICAL — If signatures are forged, malware can be signed as legitimate.')">💿 Software Updates</div>
        <div class="data-packet packet-encrypted" onclick="showRisk(this,'VPN Traffic','ECDH','HIGH — Corporate VPN sessions recorded today decryptable tomorrow.')">🔒 VPN Traffic</div>
        <div class="data-packet packet-encrypted" onclick="showRisk(this,'Blockchain/Crypto','ECDSA','CRITICAL — Bitcoin wallets use ECC. Quantum breaks all ECDSA signatures.')">₿ Cryptocurrency</div>
        <div class="data-packet packet-encrypted" onclick="showRisk(this,'ML-KEM Protected Data','FIPS 203','✅ SAFE — Lattice math resists quantum. This data stays encrypted forever.')">🔐 PQC Protected</div>
    </div>
    <div id="risk-result" style="background:#071520;border:1px solid #1a3a5a;border-radius:8px;padding:10px;margin-top:10px;display:none;font-size:10px;"></div>
</div>
</div>

<!-- ═══ IMPACT CALCULATOR ════════════════════════════════════════════════════ -->
<div id="impact-section">
<div class="harvest-scene">
    <div class="harvest-title">💀 Quantum Threat Impact Calculator</div>
    <div style="font-size:9px;color:#94a3b8;margin-bottom:12px">
        Enter your organization details to see your quantum risk exposure:
    </div>

    <div class="calc-grid">
        <div class="calc-box">
            <label>Organization Type</label>
            <select id="org-type">
                <option value="school">🏫 School / EdTech</option>
                <option value="hospital">🏥 Hospital / Healthcare</option>
                <option value="bank">🏦 Bank / Finance</option>
                <option value="gov">🏛️ Government Agency</option>
                <option value="startup">🚀 Tech Startup</option>
                <option value="military">⚔️ Military / Defense</option>
            </select>
        </div>
        <div class="calc-box">
            <label>Data Sensitivity</label>
            <select id="data-sens">
                <option value="low">📋 Low (public info)</option>
                <option value="med">📊 Medium (employee data)</option>
                <option value="high">🔒 High (financial/medical)</option>
                <option value="critical">☢️ Critical (national security)</option>
            </select>
        </div>
        <div class="calc-box">
            <label>Records Stored</label>
            <select id="records">
                <option value="1000">Under 10,000</option>
                <option value="50000">10,000 – 100,000</option>
                <option value="500000">100K – 1 Million</option>
                <option value="5000000">1M – 10 Million</option>
                <option value="50000000">10M+</option>
            </select>
        </div>
        <div class="calc-box">
            <label>Current Encryption</label>
            <select id="encryption">
                <option value="rsa">RSA-2048 (vulnerable)</option>
                <option value="ecc">ECC-256 (vulnerable)</option>
                <option value="hybrid">Hybrid RSA+PQC (transitioning)</option>
                <option value="pqc">Full PQC (safe)</option>
            </select>
        </div>
    </div>

    <button class="calc-btn" onclick="calcImpact()">💀 Calculate My Quantum Risk</button>

    <div id="impact-result" style="margin-top:12px;">
        <div class="impact-score" id="risk-score"></div>
        <div class="impact-label" id="risk-label"></div>
        <div class="risk-meter" id="risk-meter"></div>
        <div class="impact-detail" id="risk-detail"></div>
    </div>
</div>

<div class="harvest-scene">
    <div class="harvest-title">🌍 Real Organizations Already Migrating</div>
    <div style="font-size:9px;line-height:1.8;color:#94a3b8;">
        <div style="padding:6px 0;border-bottom:1px solid #1a3a5a">
            <span style="color:#10b981;font-weight:bold">✅ Google Chrome</span> — Deployed X25519+ML-KEM hybrid TLS. Protects 20% of all internet traffic today.
        </div>
        <div style="padding:6px 0;border-bottom:1px solid #1a3a5a">
            <span style="color:#10b981;font-weight:bold">✅ Cloudflare</span> — All new TLS connections use ML-KEM key exchange since 2024.
        </div>
        <div style="padding:6px 0;border-bottom:1px solid #1a3a5a">
            <span style="color:#10b981;font-weight:bold">✅ Apple</span> — iMessage upgraded to PQC with PQXDH protocol (2024).
        </div>
        <div style="padding:6px 0;border-bottom:1px solid #1a3a5a">
            <span style="color:#10b981;font-weight:bold">✅ Signal</span> — PQXDH key agreement deployed for all messages.
        </div>
        <div style="padding:6px 0;border-bottom:1px solid #1a3a5a">
            <span style="color:#f59e0b;font-weight:bold">⚠️ US Banks</span> — FDIC issued PQC guidance. Most banks still planning, not deployed.
        </div>
        <div style="padding:6px 0;border-bottom:1px solid #1a3a5a">
            <span style="color:#f59e0b;font-weight:bold">⚠️ Healthcare</span> — HHS issued PQC advisory. HIPAA does not yet mandate PQC.
        </div>
        <div style="padding:6px 0">
            <span style="color:#ef4444;font-weight:bold">❌ Most Schools</span> — No PQC migration plans. Student data encrypted with RSA sits in databases.
        </div>
    </div>
</div>
</div>

<script>
function showTab(t) {
    ['timeline','harvest','impact'].forEach(function(id) {
        document.getElementById(id+'-section').style.display = id===t?'block':'none';
    });
    document.querySelectorAll('.tab').forEach(function(el,i) {
        el.classList.toggle('active', ['timeline','harvest','impact'][i]===t);
    });
}

// Live counter — simulates harvested records
var count = 2847293847;
function updateCounter() {
    count += Math.floor(Math.random()*1847+500);
    document.getElementById('live-counter').textContent = count.toLocaleString();
}
setInterval(updateCounter, 800);
updateCounter();

// Animate steps
var stepIdx = 0;
function animateSteps() {
    var steps = ['step1','step2','step3','step4','step5'];
    steps.forEach(function(s) {
        document.getElementById(s).classList.remove('active-step');
        if (s!=='step5') document.getElementById(s).style.borderLeftColor='#1a3a5a';
    });
    stepIdx = 0;
    function nextStep() {
        if (stepIdx >= steps.length) return;
        document.getElementById(steps[stepIdx]).classList.add('active-step');
        if (steps[stepIdx]!=='step5') document.getElementById(steps[stepIdx]).style.borderLeftColor='#ef4444';
        stepIdx++;
        setTimeout(nextStep, 1200);
    }
    nextStep();
}

function showRisk(el, name, encryption, desc) {
    document.querySelectorAll('.data-packet').forEach(function(p) {
        p.classList.remove('packet-stolen');
        p.classList.add('packet-encrypted');
    });
    var isSafe = desc.startsWith('✅');
    if (!isSafe) el.classList.add('packet-stolen');
    var r = document.getElementById('risk-result');
    r.style.display='block';
    r.style.borderColor = isSafe?'#10b981':'#ef4444';
    r.innerHTML = '<b style="color:'+(isSafe?'#10b981':'#ef4444')+'">'+name+'</b> — '+encryption+'<br>'+
        '<span style="color:#94a3b8">'+desc+'</span>';
}

function calcImpact() {
    var org = document.getElementById('org-type').value;
    var sens = document.getElementById('data-sens').value;
    var recs = parseInt(document.getElementById('records').value);
    var enc = document.getElementById('encryption').value;

    var baseRisk = {low:10,med:35,high:65,critical:95}[sens];
    var orgMult = {school:0.8,hospital:1.2,bank:1.3,gov:1.4,startup:0.7,military:1.5}[org];
    var encMult = {rsa:1.4,ecc:1.3,hybrid:0.6,pqc:0.1}[enc];
    var recsMult = recs>5000000?1.4:recs>500000?1.2:recs>50000?1.0:0.8;

    var risk = Math.min(100, Math.round(baseRisk * orgMult * encMult * recsMult));
    var cost = Math.round(recs * 0.0012 * encMult * orgMult);

    var level = risk>75?'CRITICAL':risk>50?'HIGH':risk>25?'MEDIUM':'LOW';
    var color = risk>75?'#ef4444':risk>50?'#f59e0b':risk>25?'#fbbf24':'#10b981';

    var detail = {
        rsa: 'Your RSA encryption WILL be broken when quantum computers arrive. All '+recs.toLocaleString()+' records become readable.',
        ecc: 'ECC is equally vulnerable to Shor Algorithm. Migrate to ML-KEM before 2030.',
        hybrid: 'Good start! Hybrid RSA+PQC protects against Harvest Now attacks. Complete the PQC migration.',
        pqc: 'Excellent! Full PQC deployment means harvested data stays encrypted even post-quantum.'
    }[enc];

    var orgAdvice = {
        school: 'FERPA requires protecting student records. PQC migration protects students whose data lasts decades.',
        hospital: 'HIPAA records have 6-year minimum retention. Quantum computers arrive before retention ends.',
        bank: 'GLBA requires financial record protection. Banking regulators are issuing PQC guidance now.',
        gov: 'FISMA compliance will require PQC under NSA CNSA 2.0 by 2030.',
        startup: 'IP theft via Harvest Now Decrypt Later is a real threat. Protect your competitive advantage.',
        military: 'CNSA 2.0 mandates PQC. Classified data MUST migrate by 2033.'
    }[org];

    document.getElementById('impact-result').style.display='block';
    document.getElementById('risk-score').textContent = risk+'%';
    document.getElementById('risk-score').style.color = color;
    document.getElementById('risk-label').textContent = level+' QUANTUM RISK — Est. breach cost: $'+cost.toLocaleString()+'M';
    document.getElementById('risk-label').style.color = color;

    var meter = document.getElementById('risk-meter');
    meter.innerHTML = '';
    for (var i=0;i<10;i++) {
        var b=document.createElement('div');
        b.className='risk-block';
        if(i<risk/10) b.className+=' '+(risk>75?'filled-high':risk>50?'filled-mid':'filled-low');
        meter.appendChild(b);
    }

    document.getElementById('risk-detail').innerHTML =
        '<b>Analysis:</b> '+detail+'<br><br>'+
        '<b>Your sector:</b> '+orgAdvice+'<br><br>'+
        '<b>Recommended action:</b> Deploy ML-KEM (FIPS 203) for key exchange and ML-DSA (FIPS 204) for signatures immediately.';
}
</script>
</body>
</html>
""", height=800)
