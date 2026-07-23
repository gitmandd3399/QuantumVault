def render_secure_network():
    """Level 2-3: Secure the Network - topology inspection and PQC migration decisions."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("\U0001f310 Secure the Network")
    st.markdown(
        "**You are the network security engineer.** Each scenario gives you a real topology \u2014 "
        "star, hub-and-spoke, mesh, hybrid. Click any link to inspect what protocol it uses, what "
        "crypto protects it, and how long that data must stay secret. Then decide: leave it, or "
        "migrate it. **Not every link needs upgrading** \u2014 knowing which ones do not is half the skill.\n\n"
        "**Level 3 networks are harder:** you get a limited number of migration slots, so you must "
        "triage by risk \u2014 and after each fix you must justify *why*. Use the Hint button if you get stuck."
    )

    components.html(r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0b1526;font-family:'Segoe UI',system-ui,sans-serif;color:#e2e8f0;padding:10px;}
.wrap{max-width:700px;margin:0 auto;}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;}
.sc{background:#1a1500;border:2px solid #fbbf24;border-radius:9px;padding:5px 14px;
color:#fbbf24;font-weight:800;font-size:15px;}
h2{color:#a5b4fc;font-size:18px;}
.sub{color:#64748b;font-size:12px;margin-bottom:12px;}
#scens{display:flex;flex-direction:column;gap:8px;}
.sb{display:flex;align-items:center;gap:11px;background:#111c30;border:2px solid #334155;
border-radius:11px;padding:13px;color:#e2e8f0;cursor:pointer;text-align:left;}
.sb:hover{border-color:#a5b4fc;background:#18243c;}
.lvl{border-radius:7px;min-width:30px;height:30px;display:flex;align-items:center;
justify-content:center;font-weight:800;font-size:12px;flex-shrink:0;}
.lv2{background:#7c6dfa;} .lv3{background:#dc2626;}
.sinfo{display:flex;flex-direction:column;gap:2px;}
.sinfo b{font-size:14px;}
.stopo2{font-size:11px;color:#64748b;}
.backl{background:none;border:none;color:#64748b;font-size:12px;cursor:pointer;padding:0;margin-bottom:8px;}
.backl:hover{color:#a5b4fc;}
#stopo{display:inline-block;background:#1e1b4b;border:1px solid #4f46e5;border-radius:11px;
padding:2px 10px;font-size:10.5px;font-weight:800;color:#c7d2fe;margin-left:8px;}
#brief{background:#111c30;border-left:3px solid #60a5fa;border-radius:6px;padding:10px 13px;
font-size:12.5px;line-height:1.55;margin:9px 0;color:#cbd5e1;}
#topo{background:#0a1120;border:1px solid #1e3a5a;border-radius:11px;padding:6px;margin-bottom:9px;}
.lk{cursor:pointer;}
#prog{font-size:11.5px;color:#64748b;text-align:center;margin-bottom:9px;}
#panel{background:#111c30;border:1px solid #334155;border-radius:11px;padding:13px;min-height:120px;}
.hint{color:#64748b;font-size:13px;text-align:center;padding:26px 10px;}
.ptitle{font-weight:800;font-size:14.5px;color:#a5b4fc;margin-bottom:8px;}
.pt{width:100%;font-size:12px;margin-bottom:10px;}
.pt td{padding:3px 0;vertical-align:top;}
.pt td:first-child{color:#64748b;width:120px;}
.plab{font-size:12px;color:#94a3b8;font-weight:700;margin-bottom:7px;}
.act{display:block;width:100%;text-align:left;background:#1e293b;border:2px solid #475569;
border-radius:9px;padding:9px 12px;margin-bottom:6px;color:#e2e8f0;font-size:12.5px;
font-weight:700;cursor:pointer;}
.act:hover{border-color:#a5b4fc;}
.ad{display:block;font-size:10.5px;color:#64748b;font-weight:400;margin-top:2px;}
.res{font-weight:800;font-size:14px;margin-bottom:7px;}
.res.good{color:#34d399;} .res.bad{color:#f87171;}
.why{background:#0c1a30;border-left:3px solid #60a5fa;border-radius:6px;padding:9px 12px;
font-size:12.5px;line-height:1.55;color:#cbd5e1;}
#quizbox{display:none;background:#111c30;border:2px solid #4f46e5;border-radius:12px;
padding:14px;margin-top:10px;}
.qlab{font-size:10.5px;font-weight:800;color:#818cf8;letter-spacing:1px;margin-bottom:6px;}
#qq{font-size:14.5px;line-height:1.45;margin-bottom:10px;}
.qopt{display:block;width:100%;text-align:left;background:#1e293b;border:2px solid #475569;
border-radius:9px;padding:10px 13px;margin-bottom:6px;color:#e2e8f0;font-size:13px;cursor:pointer;}
.qopt:hover:enabled{border-color:#a5b4fc;}
.qopt.qright{background:#05301f;border-color:#10b981;color:#34d399;font-weight:700;}
.qopt.qwrong{background:#2d0a0a;border-color:#ef4444;color:#f87171;}
#qwhy{display:none;background:#0c1a30;border-left:3px solid #60a5fa;border-radius:6px;
padding:9px 12px;font-size:12.5px;line-height:1.5;margin-top:8px;}
.g{color:#34d399;} .r{color:#f87171;}
#donebox{display:none;text-align:center;background:#111c30;border:2px solid #10b981;
border-radius:12px;padding:16px;margin-top:10px;}
.dtitle{font-size:17px;font-weight:800;color:#34d399;}
.dsub{font-size:12.5px;color:#94a3b8;margin:5px 0 10px;}
.nb{width:100%;padding:11px;border:none;border-radius:9px;background:linear-gradient(135deg,#4f46e5,#7c3aed);
color:white;font-weight:800;font-size:13.5px;cursor:pointer;}
#advbar{display:flex;justify-content:space-between;align-items:center;background:#1a1500;
border:1px solid #fbbf24;border-radius:9px;padding:8px 13px;margin-bottom:9px;}
.bslots{font-size:12.5px;color:#fcd34d;font-weight:700;}
.bslots b{font-size:15px;color:#fbbf24;}
.hintb{background:#1e293b;border:1.5px solid #475569;border-radius:7px;padding:5px 12px;
color:#cbd5e1;font-size:12px;font-weight:700;cursor:pointer;}
.hintb:hover{border-color:#fbbf24;color:#fbbf24;}
#hintbox{background:#0c1a30;border-left:3px solid #fbbf24;border-radius:6px;padding:10px 13px;
font-size:12.5px;margin-bottom:9px;color:#cbd5e1;}
.hsub{font-size:11px;color:#64748b;font-style:italic;}
.ht{width:100%;font-size:11.5px;margin-top:7px;}
.ht td{padding:2px 6px 2px 0;color:#94a3b8;}
.ht td:first-child{color:#fbbf24;font-weight:800;width:26px;}
.cost{background:#3b2f05;color:#fbbf24;border-radius:8px;padding:1px 7px;font-size:10px;
font-weight:800;margin-left:5px;}
.act.blocked{opacity:.4;cursor:not-allowed;}
.act.just{font-weight:400;font-size:12px;line-height:1.4;}
.dwarn{background:#2a1a05;border-left:3px solid #f59e0b;border-radius:6px;padding:9px 12px;
font-size:12px;line-height:1.5;color:#fcd34d;margin-bottom:10px;text-align:left;}
.confp{position:fixed;top:-10px;width:9px;height:9px;border-radius:2px;pointer-events:none;
animation:cf linear forwards;z-index:999;}
@keyframes cf{to{transform:translateY(105vh) rotate(600deg);opacity:0;}}
</style></head><body><div class="wrap">
<div id="picker">
  <div class="top"><div><h2>&#127760; Secure the Network</h2>
  <div class="sub">Inspect each link. Decide what needs post-quantum protection.</div></div>
  <div class="sc">&#11088; <span id="score">0</span></div></div>
  <div id="scens"></div>
</div>
<div id="game" style="display:none">
  <button class="backl" onclick="backToPicker()">&#8592; All networks</button>
  <div class="top"><div><h2 style="display:inline" id="sname"></h2><span id="stopo"></span></div>
  <div class="sc">&#11088; <span id="score2">0</span></div></div>
  <div id="brief"></div>
  <div id="advbar" style="display:none">
    <div class="bslots">&#128295; Migration slots: <b id="bleft">0</b> of <b id="bmax">0</b> left</div>
    <button class="hintb" onclick="toggleHint()">&#128161; Hint</button>
  </div>
  <div id="hintbox" style="display:none"></div>
  <div id="topo"></div>
  <div id="prog"></div>
  <div id="panel"></div>
  <div id="quizbox">
    <div class="qlab">NETWORKING CHECK</div>
    <div id="qq"></div><div id="qopts"></div><div id="qwhy"></div>
  </div>
  <div id="donebox"></div>
</div>
</div>
<script>

var D = {"scenarios": [{"id": "office", "level": 2, "name": "The Small Office", "topo": "Star Topology", "brief": "Four workstations connect through a central switch to a router, then out to the internet. Customer credit card data crosses the internet link every day. Inspect each link and secure what needs it.", "nodes": [{"id": "pc1", "l": "PC-1", "i": "&#128187;", "x": 70, "y": 60, "ip": "192.168.1.10"}, {"id": "pc2", "l": "PC-2", "i": "&#128187;", "x": 70, "y": 140, "ip": "192.168.1.11"}, {"id": "pc3", "l": "PC-3", "i": "&#128187;", "x": 70, "y": 220, "ip": "192.168.1.12"}, {"id": "sw", "l": "Switch", "i": "&#128225;", "x": 230, "y": 140, "ip": "192.168.1.1"}, {"id": "rtr", "l": "Router", "i": "&#128260;", "x": 390, "y": 140, "ip": "203.0.113.5"}, {"id": "net", "l": "Internet", "i": "&#127760;", "x": 530, "y": 140, "ip": "public"}], "links": [{"id": "l1", "a": "pc1", "b": "sw", "proto": "Ethernet (LAN)", "crypto": "None (switched LAN)", "data": "Internal traffic", "life": "n/a", "fix": "leave", "why": "Physical LAN segments inside a locked office are not the quantum risk. Encrypting every internal cable adds cost without addressing harvest-now-decrypt-later. Focus effort where traffic leaves your control."}, {"id": "l2", "a": "pc2", "b": "sw", "proto": "Ethernet (LAN)", "crypto": "None (switched LAN)", "data": "Internal traffic", "life": "n/a", "fix": "leave", "why": "Same as the other LAN links. Internal wired segments are lower priority than anything crossing the internet."}, {"id": "l3", "a": "pc3", "b": "sw", "proto": "Ethernet (LAN)", "crypto": "None (switched LAN)", "data": "Internal traffic", "life": "n/a", "fix": "leave", "why": "Secure the perimeter first. LAN encryption is a later hardening step, not a quantum-migration priority."}, {"id": "l4", "a": "sw", "b": "rtr", "proto": "Ethernet (LAN)", "crypto": "None (switched LAN)", "data": "Aggregated internal traffic", "life": "n/a", "fix": "leave", "why": "Still inside the trusted network. The router's outbound link is where the real exposure begins."}, {"id": "l5", "a": "rtr", "b": "net", "proto": "TLS 1.3 over the public internet", "crypto": "RSA-2048 key exchange", "data": "Customer credit card numbers", "life": "7+ years (PCI retention)", "fix": "kem", "why": "This is the exposed link. RSA-2048 key exchange falls to Shor's algorithm, and an attacker recording this traffic today can decrypt it once a CRQC exists. Card data retained for years is a textbook harvest-now-decrypt-later target. Upgrade to hybrid ML-KEM (FIPS 203)."}], "quiz": {"q": "In a star topology, what is the single point of failure?", "o": ["The central switch", "Any one PC", "The internet link", "The cabling"], "a": 0, "why": "Every device depends on the central node. Lose the switch and the whole segment goes down &mdash; which is why mesh topologies exist."}}, {"id": "branches", "level": 2, "name": "Branch Office VPNs", "topo": "Hub-and-Spoke", "brief": "Headquarters connects to three branch offices over VPN tunnels. Each tunnel carries different data. Not every tunnel is equally urgent &mdash; inspect the data type and lifetime before you decide.", "nodes": [{"id": "hq", "l": "HQ", "i": "&#127970;", "x": 300, "y": 140, "ip": "10.0.0.1"}, {"id": "b1", "l": "Branch A", "i": "&#127978;", "x": 90, "y": 50, "ip": "10.1.0.1"}, {"id": "b2", "l": "Branch B", "i": "&#127978;", "x": 90, "y": 230, "ip": "10.2.0.1"}, {"id": "b3", "l": "Branch C", "i": "&#127978;", "x": 510, "y": 140, "ip": "10.3.0.1"}], "links": [{"id": "v1", "a": "hq", "b": "b1", "proto": "IPsec VPN tunnel", "crypto": "RSA-2048 + AES-128", "data": "Employee HR records", "life": "Lifetime of employment + 7 years", "fix": "kem", "why": "HR records carry a very long confidentiality requirement, and RSA-2048 key exchange is quantum-vulnerable. Upgrade the key exchange to hybrid ML-KEM. Note the AES-128 is a separate (smaller) concern."}, {"id": "v2", "a": "hq", "b": "b2", "proto": "IPsec VPN tunnel", "crypto": "ECDH P-256 + AES-256", "data": "Daily sales totals", "life": "Public within 90 days", "fix": "kem", "why": "ECDH is also broken by Shor &mdash; elliptic curves are not safer than RSA against quantum attack. The short data lifetime lowers urgency, but the fix is the same: hybrid ML-KEM. Prioritize it after the HR tunnel."}, {"id": "v3", "a": "hq", "b": "b3", "proto": "IPsec VPN tunnel", "crypto": "Hybrid X25519 + ML-KEM-768", "data": "Inventory counts", "life": "1 year", "fix": "leave", "why": "This tunnel is already migrated. Classical X25519 combined with ML-KEM means an attacker must break both to succeed. Leave it alone &mdash; recognizing what is already secure is part of the job."}], "quiz": {"q": "Why does hybrid key exchange combine a classical algorithm with a post-quantum one?", "o": ["An attacker must break BOTH to succeed", "It is twice as fast", "It uses less bandwidth", "Regulations require two algorithms"], "a": 0, "why": "During migration, post-quantum algorithms have less battle-testing than classical ones. Combining them means a flaw in either alone is not fatal."}}, {"id": "hospital", "level": 3, "name": "The Hospital Mesh", "topo": "Partial Mesh", "budget": 2, "brief": "A hospital network with redundant paths between critical systems. Patient records must stay confidential for a patient's entire lifetime. Some links here are already fine &mdash; find the ones that are not.", "nodes": [{"id": "rec", "l": "Records DB", "i": "&#128451;", "x": 90, "y": 60, "ip": "10.5.1.10"}, {"id": "img", "l": "Imaging", "i": "&#129535;", "x": 90, "y": 220, "ip": "10.5.1.20"}, {"id": "core", "l": "Core Rtr", "i": "&#128260;", "x": 280, "y": 140, "ip": "10.5.0.1"}, {"id": "spec", "l": "Specialist", "i": "&#128104;&#8205;&#9877;&#65039;", "x": 480, "y": 60, "ip": "remote"}, {"id": "bkp", "l": "Backup Site", "i": "&#128190;", "x": 480, "y": 220, "ip": "10.9.0.1"}], "links": [{"id": "h1", "a": "rec", "b": "core", "proto": "Internal TLS", "crypto": "AES-256-GCM, ECDH P-384", "data": "Patient records at rest and in motion", "life": "Patient lifetime (80+ years)", "fix": "kem", "pri": 2, "just": {"o": ["Lifetime-confidential data on the main records path, and ECDH is quantum-vulnerable", "AES-256 is broken by Grover so the whole link is unsafe", "Internal links are always the highest priority", "Newer algorithms are always faster"], "a": 0}, "why": "AES-256 is fine against quantum attack (Grover only halves its strength). The problem is ECDH P-384 for key exchange &mdash; Shor breaks it. Upgrade the key exchange to ML-KEM-1024 given the extreme data lifetime."}, {"id": "h2", "a": "img", "b": "core", "proto": "DICOM over TLS", "crypto": "AES-256-GCM, ML-KEM-1024", "data": "Medical imaging", "life": "Patient lifetime", "fix": "leave", "pri": 99, "why": "Already migrated and correctly sized. ML-KEM-1024 is the highest security level, appropriate for lifetime-confidential data. Nothing to do."}, {"id": "h3", "a": "core", "b": "spec", "proto": "External TLS to specialist clinic", "crypto": "RSA-2048", "data": "Referred patient files crossing the public internet", "life": "Patient lifetime", "fix": "kem", "pri": 1, "just": {"o": ["It combines maximum exposure (public internet), maximum data lifetime, and broken key exchange", "External links always matter more than internal ones", "RSA-2048 is the weakest algorithm in existence", "Specialists need faster connections"], "a": 0}, "why": "The highest-risk link in this network: quantum-vulnerable key exchange, lifetime-confidential data, and it crosses the public internet where it can be harvested. This is your first priority."}, {"id": "h4", "a": "core", "b": "bkp", "proto": "Backup replication", "crypto": "AES-256, ECDSA P-256 signatures", "data": "Full database backups", "life": "Patient lifetime", "fix": "dsa", "pri": 3, "just": {"o": ["Forgeable signatures would let an attacker substitute a tampered backup", "The backups are not encrypted at all", "ECDSA is slower than ML-DSA", "Backups do not need confidentiality"], "a": 0}, "why": "Encryption is fine, but the integrity signatures use ECDSA &mdash; forgeable once quantum computers arrive, meaning an attacker could substitute a tampered backup. Re-sign with ML-DSA (FIPS 204)."}], "quiz": {"q": "Why is AES-256 considered safe against quantum attack while RSA-2048 is not?", "o": ["Grover only gives a square-root speedup; Shor gives an exponential one", "AES is newer", "AES uses larger files", "RSA is not really encryption"], "a": 0, "why": "Grover reduces AES-256 to roughly 128-bit effective strength &mdash; still infeasible. Shor breaks RSA outright. Different algorithms, completely different threat."}}, {"id": "school", "level": 3, "name": "The School District", "topo": "Hybrid (Star + Mesh core)", "budget": 1, "brief": "A district network serving students and staff. There is a certificate authority signing device certs, a WiFi network, and a student records system. One decision here has a cascading effect &mdash; think about what depends on what.", "nodes": [{"id": "ca", "l": "Root CA", "i": "&#127942;", "x": 300, "y": 45, "ip": "10.0.0.5"}, {"id": "srv", "l": "Student SIS", "i": "&#128451;", "x": 90, "y": 150, "ip": "10.0.1.10"}, {"id": "core", "l": "Core", "i": "&#128260;", "x": 300, "y": 150, "ip": "10.0.0.1"}, {"id": "wifi", "l": "WiFi APs", "i": "&#128246;", "x": 510, "y": 150, "ip": "10.0.2.1"}, {"id": "chr", "l": "Chromebooks", "i": "&#128241;", "x": 510, "y": 250, "ip": "10.0.2.x"}], "links": [{"id": "s1", "a": "ca", "b": "core", "proto": "Certificate issuance", "crypto": "ECDSA P-256 root signing key", "data": "Signs every device certificate in the district", "life": "10-year root validity", "fix": "dsa", "pri": 1, "just": {"o": ["It is the root of trust \u2014 one forgeable key invalidates every certificate downstream", "Certificate authorities are attacked more often than other systems", "ECDSA keys are too short to be useful", "It handles the most network traffic"], "a": 0}, "why": "This is the root of trust. If the CA signing key is forgeable, every certificate it ever issued becomes untrustworthy &mdash; the failure cascades to every device downstream. Long validity plus catastrophic blast radius means migrate to ML-DSA (or SLH-DSA for maximum conservatism)."}, {"id": "s2", "a": "srv", "b": "core", "proto": "Internal TLS", "crypto": "RSA-2048, AES-128", "data": "Student records (FERPA protected)", "life": "Student lifetime + legal retention", "fix": "kem", "pri": 2, "just": {"o": ["FERPA-protected records with long retention, protected by quantum-vulnerable RSA", "AES-128 is completely broken today", "Student data has no legal protection", "Internal servers cannot be attacked"], "a": 0}, "why": "FERPA-protected records with a long retention requirement, protected by quantum-vulnerable RSA key exchange. Upgrade to hybrid ML-KEM."}, {"id": "s3", "a": "core", "b": "wifi", "proto": "WPA3-Enterprise", "crypto": "AES-256-GCM", "data": "Campus wireless traffic", "life": "Session only", "fix": "leave", "pri": 99, "why": "AES-256 resists Grover, and session traffic has no long confidentiality window. Not a migration priority &mdash; spend your budget on the CA and the SIS instead."}, {"id": "s4", "a": "wifi", "b": "chr", "proto": "Client association", "crypto": "AES-256-GCM", "data": "Student device traffic", "life": "Session only", "fix": "leave", "pri": 99, "why": "Same reasoning. Recognizing what does NOT need migration is as valuable as finding what does &mdash; migration budgets are finite."}], "quiz": {"q": "Why is a certificate authority's signing key the highest-priority migration target?", "o": ["Every certificate it signed becomes untrustworthy if it is forgeable", "It is the fastest to replace", "It uses the most bandwidth", "CAs are always attacked first"], "a": 0, "why": "Roots of trust cascade. One forged CA key undermines every device that trusts it &mdash; which is exactly why NIST recommends conservative, long-lived signature schemes here."}}], "actions": [{"k": "leave", "l": "&#9989; Leave as-is", "d": "Already secure or not a priority"}, {"k": "kem", "l": "&#128273; Upgrade key exchange &rarr; hybrid ML-KEM", "d": "FIPS 203"}, {"k": "dsa", "l": "&#9997;&#65039; Re-sign with ML-DSA / SLH-DSA", "d": "FIPS 204 / 205"}, {"k": "aes", "l": "&#128274; Increase symmetric key size", "d": "AES-128 &rarr; AES-256"}]};
var sIdx = 0, S = null, decided = {}, score = 0, quizDone = false;
var budgetUsed = 0, pendingJust = null, hintOn = false;
function isAdv(){ return !!(S && S.budget); }
function budgetLeft(){ return isAdv() ? (S.budget - budgetUsed) : 999; }

function el(id){ return document.getElementById(id); }
function setScore(){ var a=el("score"), b=el("score2"); if(a) a.textContent=score; if(b) b.textContent=score; }
function node(id){ for (var i=0;i<S.nodes.length;i++){ if (S.nodes[i].id===id) return S.nodes[i]; } return null; }

function pick(i){
    sIdx = i; S = D.scenarios[i]; decided = {}; quizDone = false;
    budgetUsed = 0; pendingJust = null; hintOn = false;
    el("picker").style.display = "none";
    el("game").style.display = "block";
    el("sname").textContent = S.name;
    el("stopo").textContent = S.topo;
    el("brief").textContent = S.brief;
    setScore();
    el("quizbox").style.display = "none";
    el("donebox").style.display = "none";
    el("advbar").style.display = isAdv() ? "flex" : "none";
    el("hintbox").style.display = "none";
    draw(); renderPanel(null);
    window.scrollTo(0,0);
}

function draw(){
    var w = 620, h = 300, svg = "";
    for (var i=0;i<S.links.length;i++){
        var L = S.links[i], a = node(L.a), b = node(L.b);
        var d = decided[L.id];
        var col = !d ? "#475569" : (d.right ? "#10b981" : "#ef4444");
        var dash = (!d && L.fix !== "leave") ? "" : "";
        svg += "<line x1='"+a.x+"' y1='"+a.y+"' x2='"+b.x+"' y2='"+b.y+"' stroke='"+col+
               "' stroke-width='"+(d?4:3)+"' "+dash+" class='lk' onclick=\"sel('"+L.id+"')\" />";
        var mx = (a.x+b.x)/2, my = (a.y+b.y)/2;
        svg += "<circle cx='"+mx+"' cy='"+my+"' r='11' fill='#0b1526' stroke='"+col+
               "' stroke-width='2' class='lk' onclick=\"sel('"+L.id+"')\" />";
        svg += "<text x='"+mx+"' y='"+(my+4)+"' text-anchor='middle' font-size='11' fill='"+col+
               "' class='lk' onclick=\"sel('"+L.id+"')\">"+(d ? (d.right?"\u2713":"\u2717") : "?")+"</text>";
    }
    for (var j=0;j<S.nodes.length;j++){
        var n = S.nodes[j];
        svg += "<g><rect x='"+(n.x-34)+"' y='"+(n.y-24)+"' width='68' height='48' rx='9' fill='#111c30' stroke='#334155'/>";
        svg += "<text x='"+n.x+"' y='"+(n.y-2)+"' text-anchor='middle' font-size='17'>"+n.i+"</text>";
        svg += "<text x='"+n.x+"' y='"+(n.y+15)+"' text-anchor='middle' font-size='8.5' fill='#94a3b8'>"+n.l+"</text></g>";
        svg += "<text x='"+n.x+"' y='"+(n.y+35)+"' text-anchor='middle' font-size='7.5' fill='#475569'>"+n.ip+"</text>";
    }
    el("topo").innerHTML = "<svg viewBox='0 0 "+w+" "+h+"' width='100%'>"+svg+"</svg>";
    var n = Object.keys(decided).length;
    el("prog").textContent = n + " / " + S.links.length + " links reviewed";
    if (isAdv()){
        el("bleft").textContent = budgetLeft();
        el("bmax").textContent = S.budget;
    }
    if (n === S.links.length && !quizDone){ showQuiz(); }
}

function sel(lid){
    var L = null;
    for (var i=0;i<S.links.length;i++){ if (S.links[i].id===lid) L = S.links[i]; }
    if (!L) return;
    renderPanel(L);
}

function renderPanel(L){
    if (!L){
        el("panel").innerHTML = "<div class='hint'>&#128072; Click any link (the circle on the line) to inspect it.</div>";
        return;
    }
    var d = decided[L.id];
    var h = "<div class='ptitle'>" + node(L.a).l + " &harr; " + node(L.b).l + "</div>" +
        "<table class='pt'>" +
        "<tr><td>Protocol</td><td>" + L.proto + "</td></tr>" +
        "<tr><td>Crypto in use</td><td><b>" + L.crypto + "</b></td></tr>" +
        "<tr><td>Data carried</td><td>" + L.data + "</td></tr>" +
        "<tr><td>Must stay secret</td><td><b>" + L.life + "</b></td></tr>" +
        "</table>";
    if (pendingJust && pendingJust.lid === L.id){
        h += "<div class='plab'>&#129504; Why is this the right call?</div>";
        for (var i=0;i<L.just.o.length;i++){
            h += "<button class='act just' onclick=\"justify("+i+")\">" + L.just.o[i] + "</button>";
        }
    } else if (!d){
        h += "<div class='plab'>What do you do with this link?</div>";
        for (var i=0;i<D.actions.length;i++){
            var A = D.actions[i];
            var costs = isAdv() && A.k !== "leave";
            var blocked = costs && budgetLeft() <= 0;
            h += "<button class='act" + (blocked ? " blocked" : "") + "'" +
                 (blocked ? " disabled" : " onclick=\"decide('"+L.id+"','"+A.k+"')\"") + ">" +
                 A.l + (costs ? " <span class='cost'>1 slot</span>" : "") +
                 "<span class='ad'>" + A.d + (blocked ? " &mdash; no migration slots left" : "") + "</span></button>";
        }
    } else {
        h += "<div class='res " + (d.right ? "good" : "bad") + "'>" +
             (d.right ? "&#9989; Correct" : "&#10060; Not the best call") + "</div>" +
             "<div class='why'>" + L.why + "</div>";
    }
    el("panel").innerHTML = h;
}

function decide(lid, act){
    var L = null;
    for (var i=0;i<S.links.length;i++){ if (S.links[i].id===lid) L = S.links[i]; }
    if (!L || decided[lid]) return;
    var right = act === L.fix;
    if (isAdv() && act !== "leave"){
        if (budgetLeft() <= 0) return;
        budgetUsed++;
    }
    decided[lid] = {act: act, right: right};
    if (right){ score += 100; confetti(); }
    setScore();
    if (isAdv() && right && act !== "leave" && L.just){
        pendingJust = {lid: lid};
        draw(); renderPanel(L);
        return;
    }
    draw(); renderPanel(L);
}

function justify(i){
    if (!pendingJust) return;
    var L = null;
    for (var k=0;k<S.links.length;k++){ if (S.links[k].id===pendingJust.lid) L = S.links[k]; }
    var right = i === L.just.a;
    if (right){ score += 50; }
    decided[L.id].just = right;
    pendingJust = null;
    setScore();
    draw();
    renderPanel(L);
    var p = el("panel");
    p.innerHTML = p.innerHTML +
        "<div class='res " + (right ? "good" : "bad") + "' style='margin-top:9px'>" +
        (right ? "&#129504; Reasoning correct! +50" : "&#129504; That was not the strongest reason.") +
        "</div><div class='why'>" + L.just.o[L.just.a] + "</div>";
}

function toggleHint(){
    hintOn = !hintOn;
    var hb = el("hintbox");
    if (!hintOn){ hb.style.display = "none"; return; }
    var rows = S.links.slice().sort(function(a,b){ return (a.pri||99) - (b.pri||99); });
    var h = "<b>&#128161; Risk ranking hint</b><br><span class='hsub'>Sorted by how long the data must stay secret and how exposed the link is. This does not tell you the fix &mdash; just where to look first.</span><table class='ht'>";
    for (var i=0;i<rows.length;i++){
        var r = rows[i];
        h += "<tr><td>" + (r.pri && r.pri < 90 ? "#" + r.pri : "&mdash;") + "</td><td>" +
             node(r.a).l + " &harr; " + node(r.b).l + "</td><td>" + r.life + "</td></tr>";
    }
    h += "</table>";
    hb.innerHTML = h;
    hb.style.display = "block";
}

function showQuiz(){
    el("quizbox").style.display = "block";
    el("qq").textContent = S.quiz.q;
    var h = "";
    for (var i=0;i<S.quiz.o.length;i++){
        h += "<button class='qopt' onclick='ans("+i+",this)'>" + S.quiz.o[i] + "</button>";
    }
    el("qopts").innerHTML = h;
    el("qwhy").style.display = "none";
}

function ans(i, btn){
    if (quizDone) return;
    quizDone = true;
    var right = i === S.quiz.a;
    var bs = document.querySelectorAll(".qopt");
    for (var k=0;k<bs.length;k++){ bs[k].disabled = true; if (k===S.quiz.a) bs[k].classList.add("qright"); }
    if (!right) btn.classList.add("qwrong");
    else { score += 100; confetti(); }
    setScore();
    el("qwhy").style.display = "block";
    el("qwhy").innerHTML = (right ? "<b class='g'>&#9989; Correct! +100</b><br>" : "<b class='r'>Not quite.</b><br>") + S.quiz.why;
    var n = 0;
    for (var key in decided){ if (decided[key].right) n++; }
    el("donebox").style.display = "block";
    var extra = "";
    if (isAdv()){
        var missed = [];
        for (var m=0;m<S.links.length;m++){
            var LL = S.links[m];
            if (LL.fix !== "leave" && (!decided[LL.id] || !decided[LL.id].right)){
                missed.push("#" + LL.pri + " " + node(LL.a).l + " &harr; " + node(LL.b).l);
            }
        }
        extra = "<div class='dwarn'>" + (missed.length
            ? "&#9888;&#65039; Still exposed: " + missed.join(", ") +
              "<br><span class='hsub'>With a limited budget you cannot fix everything &mdash; but did you spend your slots on the highest-risk links?</span>"
            : "&#127942; Every vulnerable link migrated within budget. That is the whole job.") + "</div>";
    }
    el("donebox").innerHTML = "<div class='dtitle'>&#127881; " + S.name + " secured!</div>" +
        "<div class='dsub'>" + n + " of " + S.links.length + " links called correctly &middot; " + score + " points total</div>" +
        extra +
        "<button class='nb' onclick='backToPicker()'>&#8592; Choose another network</button>";
}

function backToPicker(){
    el("game").style.display = "none";
    el("picker").style.display = "block";
    buildPicker();
}

function buildPicker(){
    var h = "";
    for (var i=0;i<D.scenarios.length;i++){
        var s = D.scenarios[i];
        h += "<button class='sb' onclick='pick("+i+")'>" +
             "<span class='lvl lv"+s.level+"'>L"+s.level+"</span>" +
             "<span class='sinfo'><b>"+s.name+"</b><span class='stopo2'>"+s.topo+" &middot; "+s.links.length+" links</span></span>" +
             "</button>";
    }
    el("scens").innerHTML = h;
    setScore();
}

function confetti(){
    var c = ["#fbbf24","#10b981","#3b82f6","#8b5cf6"];
    for (var i=0;i<14;i++){
        (function(n){ setTimeout(function(){
            var d = document.createElement("div"); d.className = "confp";
            d.style.left = Math.random()*100+"vw";
            d.style.background = c[Math.floor(Math.random()*c.length)];
            d.style.animationDuration = (1+Math.random()*2)+"s";
            document.body.appendChild(d);
            setTimeout(function(){ d.remove(); }, 3000);
        }, n*40); })(i);
    }
}

buildPicker();

</script></body></html>
""", height=880, scrolling=True)

    with st.expander("\U0001f393 Want to build real networks? Cisco Packet Tracer is free"):
        st.markdown(
            "This game teaches you **which crypto belongs where**. To actually build and configure "
            "networks \u2014 routers, switches, VLANs, real VPN tunnels \u2014 the industry-standard "
            "practice tool is **Cisco Packet Tracer**, and it is free.\n\n"
            "**How to get it:**\n"
            "1. Create a free account at **netacad.com** (Cisco Networking Academy \u2014 open to everyone, "
            "including self-learners)\n"
            "2. Enroll in the free course **\u201cGetting Started with Cisco Packet Tracer\u201d**\n"
            "3. Download from the Resource Hub \u2192 Lab Downloads (Windows, macOS, or Ubuntu; about 1.4 GB)\n\n"
            "\u26a0\ufe0f **Chromebook users:** Packet Tracer is a desktop install and will not run on a "
            "Chromebook. Use a home computer or a school lab machine \u2014 or keep practicing the crypto "
            "decisions right here, which works on any device.\n\n"
            "Cisco Networking Academy also offers free courses in networking, cybersecurity, and Python "
            "that align with certifications like CCNA and CompTIA Network+."
        )
        st.caption(
            "Download only from netacad.com \u2014 third-party sites may ship modified builds. "
            "Packet Tracer is a trademark of Cisco Systems, Inc. QuantumVault Academy is not affiliated "
            "with or endorsed by Cisco."
        )
