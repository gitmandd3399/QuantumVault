def render_mission_control():
    """High School: PQC Mission Control - real-world FIPS 203/204/205 scenarios with code challenges."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("\U0001f6f0\ufe0f PQC Mission Control")
    st.markdown(
        "**You are the security architect.** Six real-world systems need protection. "
        "For each one, pick the right NIST standard \u2014 then complete the actual implementation code. "
        "Getting the *why* right matters as much as the *what*."
    )

    components.html(r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0a0f1c;font-family:'Segoe UI',system-ui,sans-serif;color:#e2e8f0;padding:12px;}
.wrap{max-width:720px;margin:0 auto;}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;}
.mn{color:#64748b;font-size:12px;font-weight:700;letter-spacing:1px;}
.sc{background:#1a1500;border:2px solid #fbbf24;border-radius:9px;padding:5px 14px;
color:#fbbf24;font-weight:800;font-size:15px;}
h3{color:#a5b4fc;font-size:19px;margin-bottom:10px;}
.card{background:#111c30;border:1px solid #334155;border-radius:12px;padding:14px 16px;margin-bottom:10px;}
#scenario{font-size:14.5px;line-height:1.6;}
#threat{background:#2a1a05;border-left:3px solid #f59e0b;border-radius:6px;
padding:9px 12px;font-size:13px;margin-top:10px;color:#fcd34d;}
.qh{font-size:14px;font-weight:700;color:#94a3b8;margin:14px 0 8px;}
.ch{display:block;width:100%;text-align:left;background:#1e293b;border:2px solid #475569;
border-radius:10px;padding:12px 14px;margin-bottom:8px;color:#e2e8f0;font-size:14px;cursor:pointer;}
.ch:hover{border-color:#a5b4fc;background:#243044;}
.ch b{color:#c7d2fe;}
.ok{color:#34d399;font-weight:800;font-size:16px;}
.no{color:#f87171;font-weight:800;font-size:16px;}
.why{background:#052e1f;border-left:3px solid #10b981;border-radius:6px;
padding:10px 12px;font-size:13.5px;line-height:1.55;margin:10px 0;}
.whyno{background:#2d0a0a;border-left:3px solid #ef4444;border-radius:6px;
padding:10px 12px;font-size:13.5px;line-height:1.55;margin:10px 0;}
.real{background:#0c1a30;border-left:3px solid #60a5fa;border-radius:6px;
padding:10px 12px;font-size:13px;line-height:1.55;margin:10px 0;color:#bfdbfe;}
.gob,#nextb{display:block;width:100%;margin-top:10px;padding:12px;border:none;border-radius:10px;
background:linear-gradient(135deg,#4f46e5,#7c3aed);color:white;font-weight:800;font-size:14px;cursor:pointer;}
#codeintro{font-size:13.5px;color:#94a3b8;margin-bottom:10px;}
#code{background:#020617;border:1px solid #1e3a5a;border-radius:10px;padding:12px 14px;
font-family:'SF Mono',Consolas,monospace;font-size:12.5px;line-height:1.75;overflow-x:auto;}
.cl{white-space:pre;color:#cbd5e1;}
.blank{display:inline-block;min-width:70px;text-align:center;background:#3b1d5e;
border:2px dashed #a855f7;border-radius:5px;padding:0 8px;color:#e9d5ff;font-weight:700;}
.blank.filled{background:#052e1f;border:2px solid #10b981;border-style:solid;color:#34d399;}
.copt{background:#1e293b;border:2px solid #475569;border-radius:8px;padding:8px 14px;
margin:6px 6px 0 0;color:#e2e8f0;font-size:13px;font-family:monospace;cursor:pointer;}
.copt:hover:enabled{border-color:#a855f7;}
.copt.right{background:#052e1f;border-color:#10b981;color:#34d399;}
.copt.wrong{background:#2d0a0a;border-color:#ef4444;color:#f87171;opacity:.55;}
#cfeed{margin-top:10px;font-size:13.5px;min-height:20px;}
.done{text-align:center;padding:20px;}
.done h2{color:#fbbf24;margin-bottom:8px;}
.big{font-size:38px;font-weight:800;color:#fbbf24;}
.vd{font-size:16px;font-weight:700;margin:8px 0 14px;}
.recap{background:#111c30;border:1px solid #334155;border-radius:10px;padding:14px;
text-align:left;font-size:13.5px;line-height:1.9;}
.confp{position:fixed;top:-10px;width:9px;height:9px;border-radius:2px;pointer-events:none;
animation:cf linear forwards;z-index:999;}
@keyframes cf{to{transform:translateY(105vh) rotate(600deg);opacity:0;}}
</style></head><body><div class="wrap">
<div class="top"><div class="mn" id="mnum"></div><div class="sc">&#11088; <span id="score">0</span></div></div>
<h3 id="mtitle"></h3>
<div class="card">
  <div id="scenario"></div>
  <div id="threat"></div>
</div>
<div id="choices">
  <div class="qh">Which NIST standard fits this job?</div>
  <button class="ch" onclick="choose('203')"><b>FIPS 203 &mdash; ML-KEM (Kyber)</b><br>
    <span style="font-size:12.5px;color:#94a3b8">Key encapsulation. Establishes a shared secret over an open channel.</span></button>
  <button class="ch" onclick="choose('204')"><b>FIPS 204 &mdash; ML-DSA (Dilithium)</b><br>
    <span style="font-size:12.5px;color:#94a3b8">Lattice-based digital signatures. Fast, general purpose.</span></button>
  <button class="ch" onclick="choose('205')"><b>FIPS 205 &mdash; SLH-DSA (SPHINCS+)</b><br>
    <span style="font-size:12.5px;color:#94a3b8">Hash-based signatures. Conservative, larger, long-lived.</span></button>
  <button class="ch" onclick="choose('both')"><b>Both 203 and 204</b><br>
    <span style="font-size:12.5px;color:#94a3b8">Confidentiality AND authenticity are both required.</span></button>
  <button class="ch" onclick="choose('hybrid')"><b>Hybrid: classical + 203</b><br>
    <span style="font-size:12.5px;color:#94a3b8">Combine ECDH with ML-KEM so one broken algorithm is not fatal.</span></button>
</div>
<div id="result" style="display:none"></div>
<div id="codebox" style="display:none">
  <div class="card">
    <div class="qh" style="margin-top:0">&#128187; Complete the implementation</div>
    <div id="codeintro"></div>
    <div id="code"></div>
    <div id="copts"></div>
    <div id="cfeed"></div>
  </div>
</div>
<button id="nextb" style="display:none" onclick="next()">Next Mission &#8594;</button>
</div>
<script>

var M = [{"id": "payment", "icon": "&#128179;", "title": "Mission 1: The Online Checkout", "scenario": "A customer types their credit card number into an online store. Before that number leaves their laptop, the browser and the store's server must agree on a shared secret key that nobody watching the network can figure out. An attacker is recording all the traffic today, planning to decrypt it in 10 years with a quantum computer.", "threat": "Harvest now, decrypt later. Card data has a long shelf life.", "answer": "203", "why_right": "FIPS 203 (ML-KEM) is a Key Encapsulation Mechanism. Its whole job is establishing a shared secret over an insecure channel - exactly what a TLS handshake needs before card data flows.", "why_wrong": {"204": "ML-DSA signs data to prove who sent it. Useful in the certificate, but it does not establish the encryption key.", "205": "SLH-DSA is also a signature scheme. Signatures authenticate; they do not create shared secrets."}, "real": "TLS 1.3 hybrid key exchange (X25519 + ML-KEM-768) is already deployed in Chrome, Firefox, and Cloudflare.", "code_intro": "Complete the key encapsulation. The server generates a keypair, the client encapsulates a secret to the server's public key.", "code_lines": ["from oqs import KeyEncapsulation", "", "# Server side: generate the keypair", "server = KeyEncapsulation('ML-KEM-768')", "public_key = server.generate_keypair()", "", "# Client side: encapsulate a shared secret", "client = KeyEncapsulation('ML-KEM-768')", "ciphertext, client_secret = client.____(public_key)", "", "# Server recovers the same secret", "server_secret = server.decap_secret(ciphertext)", "", "assert client_secret == server_secret  # same key, both sides!"], "blank": "encap_secret", "blank_options": ["encap_secret", "sign", "verify", "hash_secret"]}, {"id": "messaging", "icon": "&#128172;", "title": "Mission 2: The Secure Messenger", "scenario": "A journalist messages a source. Two separate problems: (1) nobody else can read the message, and (2) the source must be certain the message really came from the journalist and was not altered by an impostor.", "threat": "Eavesdropping AND impersonation. These need different tools.", "answer": "both", "why_right": "This mission needs BOTH: FIPS 203 (ML-KEM) establishes the encryption key so the message stays private, and FIPS 204 (ML-DSA) signs it so the recipient can verify the sender. Confidentiality and authenticity are separate jobs.", "why_wrong": {"203": "ML-KEM alone keeps it private, but an impostor could still send a message the source cannot distinguish from the real one.", "204": "ML-DSA alone proves who sent it, but the message itself would travel in the clear."}, "real": "Signal's PQXDH protocol combines ML-KEM with classical elliptic-curve crypto for exactly this reason.", "code_intro": "Sign the encrypted message so the recipient can verify the sender.", "code_lines": ["from oqs import Signature", "", "# Journalist creates a signing keypair", "signer = Signature('ML-DSA-65')", "verify_key = signer.generate_keypair()", "", "# Sign the ciphertext (encrypt-then-sign)", "signature = signer.sign(ciphertext)", "", "# Source verifies before trusting it", "verifier = Signature('ML-DSA-65')", "is_real = verifier.____(ciphertext, signature, verify_key)", "", "if not is_real:", "    raise ValueError('Message was forged or tampered with!')"], "blank": "verify", "blank_options": ["verify", "encap_secret", "decap_secret", "generate_keypair"]}, {"id": "firmware", "icon": "&#128295;", "title": "Mission 3: The Car Software Update", "scenario": "A car manufacturer pushes a brake-system firmware update to 2 million vehicles. The signing key must stay trustworthy for the 20-year life of those cars. If an attacker ever forges an update signature, they control the brakes.", "threat": "Extremely long lifetime + catastrophic failure mode. This calls for the most conservative option.", "answer": "205", "why_right": "FIPS 205 (SLH-DSA) builds security entirely from hash functions - no lattice assumptions at all. It has larger signatures and is slower, but for a 20-year root of trust that tradeoff is worth it. It is the conservative backup if lattice math is ever weakened.", "why_wrong": {"203": "ML-KEM does not sign anything. You cannot verify an update's origin with a KEM.", "204": "ML-DSA would work and is faster - but it rests on lattice assumptions. For a 20-year safety-critical root of trust, hash-based security is the more conservative bet."}, "real": "NIST specifically recommends SLH-DSA for firmware signing and long-term roots of trust where signature size matters less than conservative security.", "code_intro": "Sign the firmware image with the hash-based scheme.", "code_lines": ["from oqs import Signature", "import hashlib", "", "firmware = open('brake_controller_v9.bin', 'rb').read()", "digest = hashlib.sha256(firmware).digest()", "", "# SLH-DSA: security from hashes alone", "signer = Signature('____')", "vehicle_verify_key = signer.generate_keypair()", "signature = signer.sign(digest)", "", "# Every car checks this before flashing the update", "print(f'Signature size: {len(signature)} bytes')"], "blank": "SPHINCS+-SHA2-128s-simple", "blank_options": ["SPHINCS+-SHA2-128s-simple", "ML-KEM-768", "RSA-2048", "AES-256"]}, {"id": "records", "icon": "&#127973;", "title": "Mission 4: The Medical Records Transfer", "scenario": "A hospital sends a patient's full medical history to a specialist across the country. Under HIPAA this data must stay confidential essentially forever - a diagnosis leaked in 2045 is still a privacy violation.", "threat": "Indefinite confidentiality requirement. Encrypted traffic captured today is a permanent liability.", "answer": "203", "why_right": "FIPS 203 (ML-KEM) protects the key that encrypts the records in transit. Because the data must stay secret for decades, quantum-safe key exchange is required NOW - not when quantum computers arrive.", "why_wrong": {"204": "Signatures prove the hospital sent it, which matters - but they do nothing to keep the contents private.", "205": "Same issue: SLH-DSA authenticates, it does not encrypt."}, "real": "This is the textbook harvest-now-decrypt-later target. Health records have the longest confidentiality requirement of almost any data class.", "code_intro": "Use the shared secret from ML-KEM to actually encrypt the records with AES.", "code_lines": ["from oqs import KeyEncapsulation", "from cryptography.hazmat.primitives.ciphers.aead import AESGCM", "import os", "", "kem = KeyEncapsulation('ML-KEM-1024')  # highest security level", "specialist_pub = kem.generate_keypair()", "", "sender = KeyEncapsulation('ML-KEM-1024')", "ciphertext, shared_secret = sender.encap_secret(specialist_pub)", "", "# The KEM secret becomes the AES key", "aes = AESGCM(shared_secret[:32])", "nonce = os.urandom(12)", "encrypted_records = aes.____(nonce, patient_records, None)"], "blank": "encrypt", "blank_options": ["encrypt", "decrypt", "sign", "encapsulate"]}, {"id": "contract", "icon": "&#128220;", "title": "Mission 5: The Digital Contract", "scenario": "Two companies sign a merger agreement electronically. Years later, one side claims they never signed it. The signature must hold up as proof in court - and it must be verifiable quickly, thousands of times, by many different parties.", "threat": "Non-repudiation. The signer must not be able to deny it, and verification must be efficient at scale.", "answer": "204", "why_right": "FIPS 204 (ML-DSA) is the general-purpose post-quantum signature standard. Fast verification, reasonable signature size, and strong non-repudiation - the default choice for document signing and PKI.", "why_wrong": {"203": "ML-KEM cannot sign. It establishes keys; it says nothing about who agreed to what.", "205": "SLH-DSA works, but its signatures are much larger (7-30 KB vs about 3 KB) and slower to verify. For high-volume document signing, ML-DSA is the better fit."}, "real": "ML-DSA is being adopted for X.509 certificates and code signing across the industry - it is the workhorse signature standard.", "code_intro": "Verify the contract signature. Note: verification uses the PUBLIC key.", "code_lines": ["from oqs import Signature", "", "contract = open('merger_agreement.pdf', 'rb').read()", "", "# Company A signed it earlier with their private key", "verifier = Signature('ML-DSA-87')  # highest security level", "", "# Anyone can check it using only the public key", "valid = verifier.verify(contract, signature, ____)", "", "print('Legally binding' if valid else 'FORGERY DETECTED')"], "blank": "company_a_public_key", "blank_options": ["company_a_public_key", "company_a_private_key", "shared_secret", "contract_hash"]}, {"id": "vpn", "icon": "&#127760;", "title": "Mission 6: The Government VPN", "scenario": "A federal agency runs a VPN carrying classified traffic. Policy requires that a failure in ANY single algorithm must not break security. The security team is nervous about betting everything on new math.", "threat": "Single point of cryptographic failure. New algorithms have less battle-testing than RSA and ECC.", "answer": "hybrid", "why_right": "Use a HYBRID: classical ECDH combined with FIPS 203 (ML-KEM). The session key is derived from both. An attacker must break BOTH the classical and the post-quantum algorithm to win. This is the recommended migration strategy.", "why_wrong": {"203": "ML-KEM alone is the right family, but going PQC-only removes the classical safety net during the transition period.", "204": "Signatures authenticate the tunnel endpoints but do not establish the session key."}, "real": "NSA's CNSA 2.0 suite and the IETF's TLS hybrid drafts both specify combining classical and post-quantum key exchange during migration.", "code_intro": "Combine both shared secrets into one session key using a KDF.", "code_lines": ["from oqs import KeyEncapsulation", "from cryptography.hazmat.primitives.kdf.hkdf import HKDF", "from cryptography.hazmat.primitives import hashes", "", "classical_secret = ecdh_exchange(peer_public)     # X25519", "kem = KeyEncapsulation('ML-KEM-768')", "ct, pq_secret = kem.encap_secret(peer_kem_public)  # ML-KEM", "", "# Mix BOTH secrets - breaking one is not enough", "combined = classical_secret ____ pq_secret", "session_key = HKDF(algorithm=hashes.SHA384(), length=32,", "                   salt=None, info=b'vpn-session').derive(combined)"], "blank": "+", "blank_options": ["+", "-", "and", "or"]}];
var idx = 0, score = 0, phase = "brief", picked = null, codeDone = false;

function el(id) { return document.getElementById(id); }

function render() {
    var m = M[idx];
    el("mtitle").innerHTML = m.icon + " " + m.title;
    el("mnum").textContent = "Mission " + (idx + 1) + " of " + M.length;
    el("score").textContent = score;
    el("scenario").textContent = m.scenario;
    el("threat").innerHTML = "<b>&#9888;&#65039; Threat:</b> " + m.threat;
    el("choices").style.display = phase === "brief" ? "block" : "none";
    el("result").style.display = phase === "brief" ? "none" : "block";
    el("codebox").style.display = phase === "code" ? "block" : "none";
    el("nextb").style.display = (phase === "code" && codeDone) ? "block" : "none";
}

function choose(pick) {
    if (phase !== "brief") return;
    var m = M[idx];
    picked = pick;
    var right = pick === m.answer;
    if (right) { score += 100; confetti(); }
    phase = "result";
    var r = el("result");
    var html = right
        ? "<div class='ok'>&#9989; Correct! +100</div>"
        : "<div class='no'>&#10060; Not the best choice.</div>";
    html += "<div class='why'><b>Why " + labelFor(m.answer) + ":</b> " + m.why_right + "</div>";
    if (!right && m.why_wrong[pick]) {
        html += "<div class='whyno'><b>About " + labelFor(pick) + ":</b> " + m.why_wrong[pick] + "</div>";
    }
    html += "<div class='real'><b>&#127758; In the real world:</b> " + m.real + "</div>";
    html += "<button class='gob' onclick='toCode()'>&#128187; Now write the code &#8594;</button>";
    r.innerHTML = html;
    render();
}

function labelFor(a) {
    if (a === "203") return "FIPS 203 (ML-KEM)";
    if (a === "204") return "FIPS 204 (ML-DSA)";
    if (a === "205") return "FIPS 205 (SLH-DSA)";
    if (a === "both") return "BOTH 203 and 204";
    if (a === "hybrid") return "Hybrid (classical + 203)";
    return a;
}

function toCode() {
    phase = "code";
    codeDone = false;
    var m = M[idx];
    el("codeintro").textContent = m.code_intro;
    var lines = "";
    for (var i = 0; i < m.code_lines.length; i++) {
        var line = m.code_lines[i];
        var safe = line.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        if (safe.indexOf("____") !== -1) {
            safe = safe.replace("____", "<span class='blank' id='blankspot'>?</span>");
        }
        lines += "<div class='cl'>" + (safe || "&nbsp;") + "</div>";
    }
    el("code").innerHTML = lines;
    var opts = "";
    for (var j = 0; j < m.blank_options.length; j++) {
        var o = m.blank_options[j];
        opts += "<button class='copt' onclick=\"tryFill(" + j + ",this)\">" +
            o.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</button>";
    }
    el("copts").innerHTML = opts;
    el("cfeed").textContent = "";
    render();
}

function tryFill(j, btn) {
    if (codeDone) return;
    var m = M[idx];
    var val = m.blank_options[j];
    if (val === m.blank) {
        codeDone = true;
        score += 50;
        var spot = el("blankspot");
        if (spot) {
            spot.textContent = val;
            spot.className = "blank filled";
        }
        btn.classList.add("right");
        el("cfeed").innerHTML = "<span class='ok'>&#9989; Code complete! +50</span>";
        confetti();
    } else {
        btn.classList.add("wrong");
        btn.disabled = true;
        el("cfeed").innerHTML = "<span class='no'>Not quite - think about what that function actually does.</span>";
    }
    render();
}

function next() {
    if (idx < M.length - 1) {
        idx++; phase = "brief"; picked = null; codeDone = false;
        el("result").innerHTML = "";
        render();
        window.scrollTo(0, 0);
    } else {
        finish();
    }
}

function finish() {
    var max = M.length * 150;
    var verdict = score >= max * 0.9 ? "&#127942; PQC ENGINEER - you can match the standard to the threat."
        : score >= max * 0.6 ? "&#129352; Solid work. Review the misses and run it again."
        : "&#128218; Good start. The 'why' boxes are where the real learning is.";
    document.body.innerHTML =
        "<div class='wrap'><div class='done'>" +
        "<h2>&#127881; All Missions Complete</h2>" +
        "<div class='big'>" + score + " / " + max + "</div>" +
        "<div class='vd'>" + verdict + "</div>" +
        "<div class='recap'><b>The rule of thumb you just learned:</b><br>" +
        "&#128273; <b>FIPS 203 (ML-KEM)</b> - when you need to share a secret KEY (encryption in transit)<br>" +
        "&#9997;&#65039; <b>FIPS 204 (ML-DSA)</b> - when you need to PROVE who sent it (general signing)<br>" +
        "&#127794; <b>FIPS 205 (SLH-DSA)</b> - when you need conservative, long-lived signatures (firmware, roots of trust)<br>" +
        "&#128257; <b>Hybrid</b> - during migration, combine classical + PQC so one failure is not fatal</div>" +
        "<button class='gob' onclick='location.reload()'>&#128260; Run Missions Again</button>" +
        "</div></div>";
}

function confetti() {
    var c = ["#fbbf24", "#10b981", "#3b82f6", "#8b5cf6", "#06b6d4"];
    for (var i = 0; i < 18; i++) {
        (function(n) {
            setTimeout(function() {
                var d = document.createElement("div");
                d.className = "confp";
                d.style.left = Math.random() * 100 + "vw";
                d.style.background = c[Math.floor(Math.random() * c.length)];
                d.style.animationDuration = (1 + Math.random() * 2) + "s";
                document.body.appendChild(d);
                setTimeout(function() { d.remove(); }, 3000);
            }, n * 40);
        })(i);
    }
}

render();

</script></body></html>
""", height=900, scrolling=True)

    with st.expander("\U0001f4bb Want to run this code for real? (VS Code setup)"):
        st.markdown(
            "The code in these missions is real \u2014 it uses **liboqs**, the Open Quantum Safe library. "
            "To run it on your own machine:"
        )
        st.code(
            "# 1. Install the Python bindings\n"
            "pip install liboqs-python\n\n"
            "# 2. Try a real ML-KEM key exchange\n"
            "from oqs import KeyEncapsulation\n\n"
            "with KeyEncapsulation('ML-KEM-768') as server:\n"
            "    public_key = server.generate_keypair()\n"
            "    with KeyEncapsulation('ML-KEM-768') as client:\n"
            "        ciphertext, client_secret = client.encap_secret(public_key)\n"
            "    server_secret = server.decap_secret(ciphertext)\n"
            "    print('Match:', client_secret == server_secret)\n"
            "    print('Public key size:', len(public_key), 'bytes')",
            language="python",
        )
        st.caption(
            "On Apple Silicon you may need to set DYLD_LIBRARY_PATH to point at the liboqs build. "
            "Full docs: github.com/open-quantum-safe/liboqs-python"
        )
