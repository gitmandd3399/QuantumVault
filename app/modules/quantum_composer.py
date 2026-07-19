def render_quantum_composer():
    """9-12: Quantum Circuit Composer — IBM-style drag-and-drop quantum circuit builder with PQC connections."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("⚛️ Quantum Circuit Composer")
    st.markdown(
        "**Build real quantum circuits like IBM's Quantum Composer!** "
        "Drag gates onto qubit wires, see the Bloch sphere update live, "
        "and discover how quantum gates connect to PQC algorithms."
    )

    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0a0a14;font-family:'Segoe UI',monospace,sans-serif;color:#e2e8f0;overflow-x:hidden;}
#wrap{display:grid;grid-template-columns:140px 1fr 200px;height:620px;gap:0;}

/* GATE PALETTE */
#palette{background:#0d1117;border-right:1px solid #1e3a5a;overflow-y:auto;padding:8px 6px;}
.pal-section{margin-bottom:10px;}
.pal-title{font-size:8px;font-weight:700;letter-spacing:1.5px;color:#475569;
    text-transform:uppercase;padding:4px 2px;margin-bottom:4px;}
.gate-chip{display:flex;align-items:center;gap:5px;padding:5px 7px;border-radius:6px;
    margin-bottom:3px;cursor:grab;border:1px solid transparent;transition:all 0.15s;
    font-size:10px;font-weight:700;user-select:none;}
.gate-chip:hover{filter:brightness(1.2);transform:scale(1.03);}
.gate-chip:active{cursor:grabbing;}
.gate-chip .gs{width:22px;height:22px;border-radius:4px;display:flex;align-items:center;
    justify-content:center;font-size:10px;font-weight:900;flex-shrink:0;}

/* Circuit colors matching IBM */
.g-single{border-color:#1d4ed840;} .g-single .gs{background:#1d4ed8;color:white;}
.g-phase{border-color:#0891b240;} .g-phase .gs{background:#0891b2;color:white;}
.g-multi{border-color:#7c3aed40;} .g-multi .gs{background:#7c3aed;color:white;}
.g-measure{border-color:#05966940;} .g-measure .gs{background:#059669;color:white;}
.g-pqc{border-color:#dc262640;} .g-pqc .gs{background:#dc2626;color:white;}

/* CIRCUIT AREA */
#circuit-area{background:#050a0f;display:flex;flex-direction:column;position:relative;}
#circuit-toolbar{background:#0d1117;border-bottom:1px solid #1e3a5a;padding:6px 10px;
    display:flex;align-items:center;gap:8px;flex-shrink:0;}
.tb-btn{padding:4px 10px;border-radius:6px;border:1px solid #1e3a5a;background:transparent;
    color:#60a5fa;font-size:10px;cursor:pointer;transition:all 0.15s;}
.tb-btn:hover{background:#1e3a5a;color:white;}
.tb-btn.active{background:#1d4ed8;color:white;border-color:#3b82f6;}
#circuit-label{font-size:10px;color:#475569;margin-left:auto;}

#circuit-canvas-wrap{flex:1;overflow:hidden;position:relative;}
#circuit-cv{display:block;}

/* RIGHT PANEL */
#right-panel{background:#0d1117;border-left:1px solid #1e3a5a;display:flex;
    flex-direction:column;overflow:hidden;}
.rp-section{border-bottom:1px solid #1e3a5a;padding:10px;}
.rp-title{font-size:9px;font-weight:700;letter-spacing:1px;color:#475569;
    text-transform:uppercase;margin-bottom:8px;}

/* BLOCH SPHERE */
#bloch-cv{display:block;margin:0 auto;}

/* PROBABILITY BARS */
.prob-bar-wrap{margin-bottom:5px;}
.prob-label{font-size:9px;color:#94a3b8;display:flex;justify-content:space-between;margin-bottom:2px;}
.prob-bar-bg{height:10px;background:#1e293b;border-radius:3px;overflow:hidden;}
.prob-bar-fill{height:100%;border-radius:3px;transition:width 0.4s ease;}

/* GATE INFO */
#gate-info{flex:1;padding:10px;overflow-y:auto;}
.gi-name{font-size:14px;font-weight:700;color:#60a5fa;margin-bottom:4px;}
.gi-matrix{font-family:monospace;font-size:9px;color:#94a3b8;background:#050a0f;
    padding:6px;border-radius:6px;margin:6px 0;line-height:1.8;}
.gi-desc{font-size:10px;color:#94a3b8;line-height:1.6;margin-bottom:6px;}
.gi-pqc{font-size:9px;color:#10b981;background:rgba(16,185,129,0.08);
    border:1px solid rgba(16,185,129,0.2);border-radius:6px;padding:5px 7px;line-height:1.5;}

/* BOTTOM BAR */
#bottom-bar{background:#0d1117;border-top:1px solid #1e3a5a;
    padding:6px 10px;display:flex;gap:8px;align-items:center;grid-column:1/-1;}
#qasm-output{flex:1;background:#050a0f;border:1px solid #1e3a5a;border-radius:6px;
    padding:5px 8px;font-family:monospace;font-size:9px;color:#a78bfa;
    overflow-x:auto;white-space:nowrap;}
#result-msg{font-size:10px;color:#10b981;min-width:200px;}

/* CHALLENGE PANEL */
#challenge-box{background:rgba(59,130,246,0.06);border:1px solid rgba(59,130,246,0.2);
    border-radius:8px;padding:8px 10px;margin:6px 10px;font-size:10px;}
.ch-title{color:#60a5fa;font-weight:700;margin-bottom:3px;font-size:10px;}
.ch-desc{color:#94a3b8;line-height:1.5;}
.ch-badge{display:inline-block;background:rgba(16,185,129,0.15);color:#10b981;
    border:1px solid #10b981;border-radius:10px;padding:1px 6px;font-size:8px;margin-top:4px;}

/* CONFETTI */
.cp{position:fixed;pointer-events:none;z-index:999;width:7px;height:7px;
    border-radius:2px;animation:cf linear forwards;}
@keyframes cf{0%{transform:translateY(-20px) rotate(0deg);opacity:1;}
    100%{transform:translateY(600px) rotate(720deg);opacity:0;}}
</style>
</head>
<body>
<div style="background:#0d1117;border-bottom:1px solid #1e3a5a;padding:6px 12px;
    display:flex;align-items:center;gap:8px;font-size:11px;">
    <span style="color:#7c3aed;font-weight:700">⚛ Quantum Circuit Composer</span>
    <span style="color:#475569">|</span>
    <span id="qubit-count-label" style="color:#60a5fa">3 Qubits</span>
    <span style="color:#475569">|</span>
    <span id="depth-label" style="color:#94a3b8">Depth: 0</span>
    <div style="margin-left:auto;display:flex;gap:6px;">
        <button class="tb-btn" onclick="addQubit()">+ Qubit</button>
        <button class="tb-btn" onclick="removeQubit()">- Qubit</button>
        <button class="tb-btn active" onclick="runCircuit()">▶ Simulate</button>
        <button class="tb-btn" onclick="clearCircuit()">🗑 Clear</button>
    </div>
</div>

<div id="wrap">
<!-- GATE PALETTE -->
<div id="palette">
    <div class="pal-section">
        <div class="pal-title">Single-Qubit</div>
        <div class="gate-chip g-single" draggable="true" ondragstart="dragGate(event,'H')" onclick="selectGate('H')">
            <div class="gs">H</div><span>Hadamard</span>
        </div>
        <div class="gate-chip g-single" draggable="true" ondragstart="dragGate(event,'X')" onclick="selectGate('X')">
            <div class="gs">X</div><span>NOT / Pauli-X</span>
        </div>
        <div class="gate-chip g-single" draggable="true" ondragstart="dragGate(event,'Y')" onclick="selectGate('Y')">
            <div class="gs">Y</div><span>Pauli-Y</span>
        </div>
        <div class="gate-chip g-single" draggable="true" ondragstart="dragGate(event,'Z')" onclick="selectGate('Z')">
            <div class="gs">Z</div><span>Pauli-Z</span>
        </div>
    </div>
    <div class="pal-section">
        <div class="pal-title">Phase Gates</div>
        <div class="gate-chip g-phase" draggable="true" ondragstart="dragGate(event,'S')" onclick="selectGate('S')">
            <div class="gs" style="background:#0891b2">S</div><span>S Gate (90°)</span>
        </div>
        <div class="gate-chip g-phase" draggable="true" ondragstart="dragGate(event,'T')" onclick="selectGate('T')">
            <div class="gs" style="background:#0891b2">T</div><span>T Gate (45°)</span>
        </div>
        <div class="gate-chip g-phase" draggable="true" ondragstart="dragGate(event,'Sdg')" onclick="selectGate('Sdg')">
            <div class="gs" style="background:#0891b2">S†</div><span>S† (-90°)</span>
        </div>
    </div>
    <div class="pal-section">
        <div class="pal-title">Multi-Qubit</div>
        <div class="gate-chip g-multi" draggable="true" ondragstart="dragGate(event,'CNOT')" onclick="selectGate('CNOT')">
            <div class="gs" style="background:#7c3aed">CX</div><span>CNOT</span>
        </div>
        <div class="gate-chip g-multi" draggable="true" ondragstart="dragGate(event,'CZ')" onclick="selectGate('CZ')">
            <div class="gs" style="background:#7c3aed">CZ</div><span>Ctrl-Z</span>
        </div>
        <div class="gate-chip g-multi" draggable="true" ondragstart="dragGate(event,'SWAP')" onclick="selectGate('SWAP')">
            <div class="gs" style="background:#7c3aed">SW</div><span>SWAP</span>
        </div>
    </div>
    <div class="pal-section">
        <div class="pal-title">Measure</div>
        <div class="gate-chip g-measure" draggable="true" ondragstart="dragGate(event,'M')" onclick="selectGate('M')">
            <div class="gs" style="background:#059669">M</div><span>Measure</span>
        </div>
        <div class="gate-chip g-measure" draggable="true" ondragstart="dragGate(event,'RESET')" onclick="selectGate('RESET')">
            <div class="gs" style="background:#059669">|0⟩</div><span>Reset</span>
        </div>
    </div>
    <div class="pal-section">
        <div class="pal-title" style="color:#dc2626">PQC Gates</div>
        <div class="gate-chip g-pqc" draggable="true" ondragstart="dragGate(event,'LWE')" onclick="selectGate('LWE')">
            <div class="gs" style="background:#dc2626">LWE</div><span>Lattice</span>
        </div>
        <div class="gate-chip g-pqc" draggable="true" ondragstart="dragGate(event,'NTRU')" onclick="selectGate('NTRU')">
            <div class="gs" style="background:#dc2626">NTR</div><span>NTRU</span>
        </div>
        <div class="gate-chip g-pqc" draggable="true" ondragstart="dragGate(event,'KYBER')" onclick="selectGate('KYBER')">
            <div class="gs" style="background:#dc2626">KYB</div><span>ML-KEM</span>
        </div>
    </div>
</div>

<!-- CIRCUIT AREA -->
<div id="circuit-area">
    <div id="challenge-box">
        <div class="ch-title" id="ch-title">🎯 Challenge 1: Bell State</div>
        <div class="ch-desc" id="ch-desc">Create a Bell state — add an H gate to q[0], then a CNOT (CX) with q[0] as control and q[1] as target. This creates quantum entanglement!</div>
        <div id="ch-badge" style="display:none"><span class="ch-badge">✅ Challenge Complete!</span></div>
    </div>
    <canvas id="circuit-cv"></canvas>
</div>

<!-- RIGHT PANEL -->
<div id="right-panel">
    <div class="rp-section">
        <div class="rp-title">Bloch Sphere (q[0])</div>
        <canvas id="bloch-cv" width="180" height="180"></canvas>
    </div>
    <div class="rp-section">
        <div class="rp-title">Probabilities</div>
        <div id="prob-bars"></div>
    </div>
    <div id="gate-info">
        <div class="rp-title">Gate Info</div>
        <div class="gi-name" id="gi-name">Select a gate</div>
        <div class="gi-desc" id="gi-desc">Click any gate in the palette to learn about it.</div>
        <div class="gi-matrix" id="gi-matrix"></div>
        <div class="gi-pqc" id="gi-pqc" style="display:none"></div>
    </div>
</div>
</div>

<!-- BOTTOM BAR -->
<div id="bottom-bar">
    <span style="font-size:9px;color:#475569;flex-shrink:0">OpenQASM 2.0:</span>
    <div id="qasm-output">// Add gates to build your circuit</div>
    <div id="result-msg"></div>
</div>

<script>
var circuitCv = document.getElementById('circuit-cv');
var ccx = circuitCv.getContext('2d');
var blochCv = document.getElementById('bloch-cv');
var bcx = blochCv.getContext('2d');

var NUM_QUBITS = 3;
var MAX_STEPS = 10;
var WIRE_H = 56;
var STEP_W = 58;
var LEFT_PAD = 50;
var TOP_PAD = 30;

// Circuit state: circuit[qubit][step] = gate or null
var circuit = [];
var selectedGateType = 'H';
var dragGateType = null;
var hoverCell = null;
var frameId = null;

// Bloch sphere state [theta, phi] per qubit
var blochStates = [];

function initCircuit() {
    circuit = [];
    blochStates = [];
    for (var q = 0; q < NUM_QUBITS; q++) {
        circuit.push(new Array(MAX_STEPS).fill(null));
        blochStates.push({theta: 0, phi: 0}); // |0> state
    }
    resizeCanvas();
    updateQASM();
    updateProbs();
    drawBloch(blochStates[0]);
}

function resizeCanvas() {
    var wrap = document.getElementById('circuit-canvas-wrap') ||
               document.getElementById('circuit-area');
    var W = wrap ? wrap.offsetWidth : 500;
    var H = TOP_PAD + NUM_QUBITS * WIRE_H + 30;
    circuitCv.width = Math.max(W, LEFT_PAD + MAX_STEPS * STEP_W + 40);
    circuitCv.height = H;
}

// ── GATE DEFINITIONS ─────────────────────────────────────────────────────────
var GATE_INFO = {
    H: {name:'Hadamard (H)',color:'#1d4ed8',
        matrix:'[1/√2  1/√2]\n[1/√2 -1/√2]',
        desc:'Creates superposition — puts |0⟩ into (|0⟩+|1⟩)/√2. The qubit is now "both 0 and 1 at once" until measured.',
        pqc:'Foundation of quantum computing. The H gate enables Shor Algorithm — which is why RSA is vulnerable. ML-KEM uses lattice math specifically designed to resist quantum algorithms that use superposition!',
        effect:function(s){return [s[1]/Math.sqrt(2)+s[0]/Math.sqrt(2),s[1]/Math.sqrt(2)-s[0]/Math.sqrt(2)];}
    },
    X: {name:'Pauli-X (NOT)',color:'#1d4ed8',
        matrix:'[0  1]\n[1  0]',
        desc:'Quantum NOT gate — flips |0⟩↔|1⟩. Equivalent to classical NOT but works on superpositions too.',
        pqc:'X gates appear in error correction circuits. ML-DSA (Dilithium) uses similar bit-flip operations in its lattice signing algorithm.',
        effect:function(s){return [s[1],s[0]];}
    },
    Y: {name:'Pauli-Y',color:'#1d4ed8',
        matrix:'[0  -i]\n[i   0]',
        desc:'Rotates the Bloch sphere 180° around the Y-axis. Introduces a complex phase factor i.',
        pqc:'Y gates represent combined bit and phase flips — relevant to quantum error models that PQC must protect against.',
        effect:function(s){return [-s[1],s[0]];}
    },
    Z: {name:'Pauli-Z (Phase Flip)',color:'#1d4ed8',
        matrix:'[1   0]\n[0  -1]',
        desc:'Flips the phase of |1⟩. Leaves |0⟩ unchanged but negates |1⟩. Undetectable by classical measurement alone.',
        pqc:'Phase operations are central to Grover Algorithm — the quantum search that can break symmetric cryptography. SPHINCS+ uses hash chains designed to resist Grover speedup!',
        effect:function(s){return [s[0],-s[1]];}
    },
    S: {name:'S Gate (Phase 90°)',color:'#0891b2',
        matrix:'[1  0]\n[0  i]',
        desc:'Rotates phase by 90° (π/2). Often called the "square root of Z" gate.',
        pqc:'Phase gates are the building blocks of quantum Fourier Transform — used in Shor Algorithm. Understanding phase helps explain WHY RSA keys must move to ML-KEM.',
        effect:function(s){return [s[0],{re:0,im:1}];}
    },
    T: {name:'T Gate (Phase 45°)',color:'#0891b2',
        matrix:'[1      0   ]\n[0  e^(iπ/4)]',
        desc:'Rotates phase by 45° (π/4). The T gate is used to build universal quantum circuits.',
        pqc:'T gates create the complexity needed for quantum speedup. They are why we need quantum-safe cryptography — classical crypto assumed these rotations were too slow to exploit.',
        effect:function(s){return [s[0],s[1]];}
    },
    Sdg: {name:'S† Gate (-90°)',color:'#0891b2',
        matrix:'[1   0]\n[0  -i]',
        desc:'Inverse of S gate. Rotates phase by -90°. Undoes the S gate operation.',
        pqc:'Gate inverses are crucial for quantum error correction — a key requirement of any quantum-safe system.',
        effect:function(s){return [s[0],s[1]];}
    },
    CNOT: {name:'CNOT / CX Gate',color:'#7c3aed',
        matrix:'[1 0 0 0]\n[0 1 0 0]\n[0 0 0 1]\n[0 0 1 0]',
        desc:'Controlled-NOT: flips target qubit ONLY when control is |1⟩. Creates ENTANGLEMENT — the heart of quantum computing.',
        pqc:'CNOT + H = Bell State = Maximum Entanglement. Shor Algorithm uses entangled qubits to factor RSA keys. ML-KEM is designed so entanglement cannot help an attacker extract the secret key!',
        effect:null
    },
    CZ: {name:'Controlled-Z Gate',color:'#7c3aed',
        matrix:'[1 0 0  0]\n[0 1 0  0]\n[0 0 1  0]\n[0 0 0 -1]',
        desc:'Applies Z gate to target only when control is |1⟩. Used in many entanglement protocols.',
        pqc:'CZ gates appear in quantum key distribution protocols. PQC replaces these protocols with classical-computable alternatives like ML-KEM.',
        effect:null
    },
    SWAP: {name:'SWAP Gate',color:'#7c3aed',
        matrix:'[1 0 0 0]\n[0 0 1 0]\n[0 1 0 0]\n[0 0 0 1]',
        desc:'Swaps the quantum states of two qubits entirely.',
        pqc:'SWAP networks are used in quantum algorithms and error correction. Falcon (FN-DSA) uses NTRU lattices which have swap-like ring structure.',
        effect:null
    },
    M: {name:'Measurement',color:'#059669',
        matrix:'Collapses\nquantum state\nto 0 or 1',
        desc:'COLLAPSES the quantum state — forces the qubit to choose 0 or 1 with probabilities from the state vector. Measurement is irreversible!',
        pqc:'Measurement is why quantum crypto works: eavesdropping collapses the state and reveals the attacker. ML-KEM protects against attackers who collect data BEFORE measurement.',
        effect:null
    },
    RESET: {name:'Reset to |0⟩',color:'#059669',
        matrix:'Forces qubit\nback to |0⟩',
        desc:'Resets qubit to ground state |0⟩. Used to reuse qubits in quantum error correction.',
        pqc:'Qubit reset is fundamental to error correction — required for long quantum computations like breaking RSA keys.',
        effect:null
    },
    LWE: {name:'LWE Lattice Gate',color:'#dc2626',
        matrix:'[lattice\nmath\noperator]',
        desc:'Learning With Errors (LWE) — the mathematical hard problem underlying ML-KEM (Kyber). Represents a lattice operation that is easy to compute but impossible to reverse.',
        pqc:'FIPS 203 (ML-KEM) is built entirely on LWE hardness. Even with a quantum computer running Shor Algorithm, LWE cannot be efficiently solved. This is WHY Kyber is quantum-safe!',
        effect:null
    },
    NTRU: {name:'NTRU Lattice Gate',color:'#dc2626',
        matrix:'[NTRU\nring\noperator]',
        desc:'NTRU is the lattice problem underlying Falcon (FN-DSA). Operates in polynomial rings — much more compact than standard LWE.',
        pqc:'FIPS 206 (Falcon) uses NTRU lattices to create the SMALLEST quantum-safe signatures — only 666 bytes! Critical for IoT and satellites where bandwidth is limited.',
        effect:null
    },
    KYBER: {name:'ML-KEM (Kyber)',color:'#dc2626',
        matrix:'[encapsulate\nkey exchange\noperator]',
        desc:'Represents the full ML-KEM key encapsulation mechanism. One operation generates a shared secret that cannot be broken even by quantum computers.',
        pqc:'FIPS 203 — Google Chrome already uses this for 20% of all HTTPS connections! Your browser may be using ML-KEM right now. This is the quantum-safe replacement for RSA key exchange.',
        effect:null
    },
};

// ── DRAG AND DROP ─────────────────────────────────────────────────────────────
function dragGate(e, type) {
    dragGateType = type;
    e.dataTransfer.setData('text', type);
}

circuitCv.addEventListener('dragover', function(e) {
    e.preventDefault();
    var cell = getCell(e);
    hoverCell = cell;
});

circuitCv.addEventListener('drop', function(e) {
    e.preventDefault();
    var cell = getCell(e);
    if (cell && dragGateType) {
        placeGate(cell.q, cell.s, dragGateType);
        dragGateType = null;
        hoverCell = null;
    }
});

circuitCv.addEventListener('click', function(e) {
    var cell = getCell(e);
    if (cell) {
        if (circuit[cell.q][cell.s]) {
            // Click existing gate to remove
            circuit[cell.q][cell.s] = null;
        } else {
            placeGate(cell.q, cell.s, selectedGateType);
        }
        updateAll();
    }
});

circuitCv.addEventListener('mousemove', function(e) {
    hoverCell = getCell(e);
});

circuitCv.addEventListener('mouseleave', function() {
    hoverCell = null;
});

function getCell(e) {
    var r = circuitCv.getBoundingClientRect();
    var mx = e.clientX - r.left;
    var my = e.clientY - r.top;
    var s = Math.floor((mx - LEFT_PAD) / STEP_W);
    var q = Math.floor((my - TOP_PAD) / WIRE_H);
    if (s >= 0 && s < MAX_STEPS && q >= 0 && q < NUM_QUBITS) {
        return {q:q, s:s};
    }
    return null;
}

function placeGate(q, s, type) {
    // For CNOT/CZ/SWAP, need 2 qubits
    if ((type==='CNOT'||type==='CZ'||type==='SWAP') && NUM_QUBITS > 1) {
        // Place as control on clicked qubit, target on next qubit
        var target = (q + 1) % NUM_QUBITS;
        circuit[q][s] = {type:type, role:'control', pair:target};
        circuit[target][s] = {type:type, role:'target', pair:q};
    } else {
        circuit[q][s] = {type:type};
    }
    updateAll();
    checkChallenges();
}

// ── SIMULATION ────────────────────────────────────────────────────────────────
function simulate() {
    // Simple statevector simulation for single qubit
    var states = [];
    for (var q = 0; q < NUM_QUBITS; q++) {
        var state = [1, 0]; // |0>
        for (var s = 0; s < MAX_STEPS; s++) {
            var g = circuit[q][s];
            if (!g) continue;
            var info = GATE_INFO[g.type];
            if (info && info.effect) {
                state = info.effect(state);
            } else if (g.type === 'X') {
                state = [state[1], state[0]];
            } else if (g.type === 'H') {
                var a = state[0], b = state[1];
                state = [(a+b)/Math.sqrt(2), (a-b)/Math.sqrt(2)];
            } else if (g.type === 'Z') {
                state = [state[0], -state[1]];
            } else if (g.type === 'RESET') {
                state = [1, 0];
            }
        }
        states.push(state);
        // Update Bloch sphere
        var alpha = state[0], beta = state[1];
        var theta = 2 * Math.acos(Math.min(1, Math.abs(alpha)));
        blochStates[q] = {theta: theta, phi: 0};
    }

    // Draw Bloch for q[0]
    drawBloch(blochStates[0]);

    // Update probabilities
    updateProbs(states);
    return states;
}

function runCircuit() {
    var states = simulate();
    setResult('✅ Simulated! Check Bloch sphere and probabilities →');
    setTimeout(function(){setResult('');}, 3000);
}

// ── DRAW CIRCUIT ─────────────────────────────────────────────────────────────
function draw() {
    var W = circuitCv.width, H = circuitCv.height;
    ccx.clearRect(0,0,W,H);
    ccx.fillStyle='#050a0f';ccx.fillRect(0,0,W,H);

    // Step numbers
    for (var s = 0; s < MAX_STEPS; s++) {
        var sx = LEFT_PAD + s * STEP_W + STEP_W/2;
        ccx.font = '9px monospace';
        ccx.fillStyle = '#2d4a6a';
        ccx.textAlign = 'center';
        ccx.fillText(s, sx, 16);
    }

    // Qubit wires
    for (var q = 0; q < NUM_QUBITS; q++) {
        var wy = TOP_PAD + q * WIRE_H + WIRE_H/2;

        // Qubit label
        ccx.font = 'bold 11px monospace';
        ccx.fillStyle = '#475569';
        ccx.textAlign = 'right';
        ccx.fillText('q['+q+']', LEFT_PAD-8, wy+4);

        // Initial state
        ccx.font = '10px monospace';
        ccx.fillStyle = '#1e3a5a';
        ccx.textAlign = 'center';
        ccx.fillText('|0⟩', LEFT_PAD-30, wy+4);

        // Wire line
        ccx.beginPath();
        ccx.moveTo(LEFT_PAD, wy);
        ccx.lineTo(LEFT_PAD + MAX_STEPS * STEP_W, wy);
        ccx.strokeStyle = '#1e3a5a';
        ccx.lineWidth = 1.5;
        ccx.stroke();

        // Classical wire (below)
        ccx.beginPath();
        ccx.moveTo(LEFT_PAD, wy+6);
        ccx.lineTo(LEFT_PAD + MAX_STEPS * STEP_W, wy+6);
        ccx.strokeStyle = '#0d2136';
        ccx.lineWidth = 1;
        ccx.stroke();

        // Gates
        for (var si = 0; si < MAX_STEPS; si++) {
            var g = circuit[q][si];
            var gx = LEFT_PAD + si * STEP_W + STEP_W/2;
            var gy = wy;

            // Hover highlight
            if (hoverCell && hoverCell.q === q && hoverCell.s === si && !g) {
                ccx.fillStyle = GATE_INFO[selectedGateType] ?
                    GATE_INFO[selectedGateType].color + '22' : '#1e3a5a22';
                ccx.fillRect(gx-18, gy-18, 36, 36);
            }

            if (!g) continue;

            var info = GATE_INFO[g.type];
            var col = info ? info.color : '#334155';

            if (g.role === 'control') {
                // Control dot
                ccx.beginPath();ccx.arc(gx, gy, 6, 0, Math.PI*2);
                ccx.fillStyle = col;ccx.fill();
                // Line to target
                var targetY = TOP_PAD + g.pair * WIRE_H + WIRE_H/2;
                ccx.beginPath();ccx.moveTo(gx, gy);ccx.lineTo(gx, targetY);
                ccx.strokeStyle = col;ccx.lineWidth=2;ccx.stroke();
            } else if (g.role === 'target') {
                if (g.type === 'CNOT') {
                    // Target circle with cross
                    ccx.beginPath();ccx.arc(gx, gy, 12, 0, Math.PI*2);
                    ccx.strokeStyle = col;ccx.lineWidth=2;ccx.stroke();
                    ccx.beginPath();ccx.moveTo(gx, gy-12);ccx.lineTo(gx, gy+12);
                    ccx.moveTo(gx-12, gy);ccx.lineTo(gx+12, gy);
                    ccx.strokeStyle=col;ccx.stroke();
                } else if (g.type === 'SWAP') {
                    // X marker
                    ccx.beginPath();
                    ccx.moveTo(gx-8,gy-8);ccx.lineTo(gx+8,gy+8);
                    ccx.moveTo(gx+8,gy-8);ccx.lineTo(gx-8,gy+8);
                    ccx.strokeStyle=col;ccx.lineWidth=2.5;ccx.stroke();
                } else {
                    // CZ target dot
                    ccx.beginPath();ccx.arc(gx, gy, 6, 0, Math.PI*2);
                    ccx.fillStyle=col;ccx.fill();
                }
            } else if (g.type === 'M') {
                // Measurement symbol
                ccx.fillStyle = col+'33';
                ccx.fillRect(gx-14, gy-14, 28, 28);
                ccx.strokeStyle = col;ccx.lineWidth=1.5;ccx.strokeRect(gx-14, gy-14, 28, 28);
                ccx.font = '13px serif';ccx.textAlign='center';ccx.textBaseline='middle';
                ccx.fillStyle=col;ccx.fillText('⊗', gx, gy);
                // Meter arc
                ccx.beginPath();ccx.arc(gx, gy+3, 8, Math.PI, 0);
                ccx.strokeStyle=col;ccx.lineWidth=1.5;ccx.stroke();
                ccx.beginPath();ccx.moveTo(gx, gy+3);ccx.lineTo(gx+7, gy-3);
                ccx.strokeStyle=col;ccx.stroke();
            } else {
                // Standard gate box
                var gw = 30, gh = 28;
                // Shadow glow
                ccx.shadowColor = col;ccx.shadowBlur = 8;
                ccx.fillStyle = col+'33';
                if(ccx.roundRect) ccx.roundRect(gx-gw/2, gy-gh/2, gw, gh, 5);
                else ccx.rect(gx-gw/2, gy-gh/2, gw, gh);
                ccx.fill();
                ccx.strokeStyle = col;ccx.lineWidth=1.5;ccx.stroke();
                ccx.shadowBlur=0;
                // Gate label
                ccx.font = 'bold '+(g.type.length>3?'8':'11')+'px monospace';
                ccx.fillStyle='white';ccx.textAlign='center';ccx.textBaseline='middle';
                ccx.fillText(g.type==='Sdg'?'S†':g.type, gx, gy);
            }
        }
    }

    // Column separators
    for (var si2 = 0; si2 < MAX_STEPS; si2++) {
        var lx = LEFT_PAD + si2 * STEP_W;
        ccx.beginPath();ccx.moveTo(lx, TOP_PAD-10);ccx.lineTo(lx, TOP_PAD+NUM_QUBITS*WIRE_H+10);
        ccx.strokeStyle='#0d2136';ccx.lineWidth=0.5;ccx.stroke();
    }
}

// ── BLOCH SPHERE ─────────────────────────────────────────────────────────────
function drawBloch(state) {
    var W=180, H=180, cx=90, cy=90, R=65;
    bcx.clearRect(0,0,W,H);
    bcx.fillStyle='#050a0f';bcx.fillRect(0,0,W,H);

    // Sphere outline
    bcx.beginPath();bcx.ellipse(cx,cy,R,R,0,0,Math.PI*2);
    bcx.strokeStyle='#1e3a5a';bcx.lineWidth=1.5;bcx.stroke();
    bcx.fillStyle='rgba(29,78,216,0.04)';bcx.fill();

    // Equator
    bcx.beginPath();bcx.ellipse(cx,cy,R,R*0.3,0,0,Math.PI*2);
    bcx.strokeStyle='#1e3a5a60';bcx.lineWidth=1;bcx.setLineDash([3,3]);bcx.stroke();bcx.setLineDash([]);

    // Axes
    var axes=[
        {dx:0,dy:-1,label:'|0⟩',col:'#60a5fa'},
        {dx:0,dy:1,label:'|1⟩',col:'#ef4444'},
        {dx:1,dy:0,label:'|+⟩',col:'#10b981'},
        {dx:-1,dy:0,label:'|−⟩',col:'#8b5cf6'},
    ];
    axes.forEach(function(a){
        bcx.beginPath();bcx.moveTo(cx,cy);bcx.lineTo(cx+a.dx*R,cy+a.dy*R);
        bcx.strokeStyle=a.col+'50';bcx.lineWidth=1;bcx.stroke();
        bcx.font='9px sans-serif';bcx.fillStyle=a.col;bcx.textAlign='center';
        bcx.fillText(a.label,cx+a.dx*(R+12),cy+a.dy*(R+12)+3);
    });

    // State vector
    var theta = state ? state.theta : 0;
    var phi = state ? (state.phi || 0) : 0;
    var vx = Math.sin(theta) * Math.cos(phi);
    var vy = -Math.cos(theta);
    var vz = Math.sin(theta) * Math.sin(phi);

    var projX = cx + vx * R;
    var projY = cy + vy * R;

    // Draw vector
    bcx.beginPath();bcx.moveTo(cx,cy);bcx.lineTo(projX,projY);
    bcx.strokeStyle='#fbbf24';bcx.lineWidth=2.5;bcx.stroke();
    // Arrow head
    bcx.beginPath();bcx.arc(projX,projY,4,0,Math.PI*2);
    bcx.fillStyle='#fbbf24';bcx.fill();
    // Shadow circle
    bcx.beginPath();bcx.moveTo(cx,cy);
    bcx.lineTo(cx+vx*R,cy);
    bcx.setLineDash([2,2]);bcx.strokeStyle='#fbbf2440';bcx.lineWidth=1;bcx.stroke();
    bcx.beginPath();bcx.moveTo(cx+vx*R,cy);bcx.lineTo(projX,projY);
    bcx.stroke();bcx.setLineDash([]);

    // State label
    var stateLabel = Math.abs(theta) < 0.1 ? '|0⟩' :
                     Math.abs(theta-Math.PI) < 0.1 ? '|1⟩' :
                     Math.abs(theta-Math.PI/2) < 0.1 ? '|+⟩' : 'superposition';
    bcx.font='bold 9px sans-serif';bcx.fillStyle='#fbbf24';bcx.textAlign='center';
    bcx.fillText(stateLabel, cx, H-6);
}

// ── PROBABILITIES ─────────────────────────────────────────────────────────────
function updateProbs(states) {
    var container = document.getElementById('prob-bars');
    if (!states) {
        // Default: all |0>
        states = [];
        for (var q=0;q<NUM_QUBITS;q++) states.push([1,0]);
    }
    // For multi-qubit, show |00>, |01>, |10>, |11> (up to 3 qubits)
    var n = Math.min(NUM_QUBITS, 3);
    var numStates = Math.pow(2, n);
    var probs = new Array(numStates).fill(0);
    // Simple tensor product approximation
    probs[0] = 1;
    for (var qi=0;qi<n;qi++) {
        var s = states[qi] || [1,0];
        var p0 = s[0]*s[0], p1 = s[1]*s[1];
        // Normalize
        var norm = p0+p1; if(norm>0){p0/=norm;p1/=norm;}
        var newProbs = new Array(numStates).fill(0);
        for (var bi=0;bi<numStates;bi++) {
            var bit = (bi >> (n-1-qi)) & 1;
            newProbs[bi] += probs[bi] * (bit===0 ? p0 : p1);
        }
        probs = newProbs;
    }
    var html = '';
    var cols = ['#3b82f6','#10b981','#8b5cf6','#f59e0b','#ef4444','#06b6d4','#ec4899','#84cc16'];
    for (var bi2=0;bi2<Math.min(numStates,8);bi2++) {
        var label = '|';
        for (var qi2=0;qi2<n;qi2++) label+=((bi2>>(n-1-qi2))&1);
        label+='⟩';
        var pct = (probs[bi2]*100).toFixed(1);
        html += '<div class="prob-bar-wrap">'+
            '<div class="prob-label"><span>'+label+'</span><span>'+pct+'%</span></div>'+
            '<div class="prob-bar-bg"><div class="prob-bar-fill" style="width:'+pct+'%;background:'+cols[bi2%cols.length]+'"></div></div>'+
            '</div>';
    }
    container.innerHTML = html;
}

// ── OPENQASM OUTPUT ───────────────────────────────────────────────────────────
function updateQASM() {
    var qasm = 'OPENQASM 2.0;\ninclude "qelib1.inc";\n';
    qasm += 'qreg q['+NUM_QUBITS+'];\ncreg c['+NUM_QUBITS+'];\n';
    var hasGates = false;
    for (var s=0;s<MAX_STEPS;s++) {
        for (var q=0;q<NUM_QUBITS;q++) {
            var g = circuit[q][s];
            if (!g) continue;
            if (g.role === 'target') continue; // skip target, written with control
            hasGates = true;
            var t = g.type;
            if (t==='H') qasm+='h q['+q+'];\n';
            else if (t==='X') qasm+='x q['+q+'];\n';
            else if (t==='Y') qasm+='y q['+q+'];\n';
            else if (t==='Z') qasm+='z q['+q+'];\n';
            else if (t==='S') qasm+='s q['+q+'];\n';
            else if (t==='T') qasm+='t q['+q+'];\n';
            else if (t==='Sdg') qasm+='sdg q['+q+'];\n';
            else if (t==='CNOT') qasm+='cx q['+q+'],q['+g.pair+'];\n';
            else if (t==='CZ') qasm+='cz q['+q+'],q['+g.pair+'];\n';
            else if (t==='SWAP') qasm+='swap q['+q+'],q['+g.pair+'];\n';
            else if (t==='M') qasm+='measure q['+q+'] -> c['+q+'];\n';
            else if (t==='RESET') qasm+='reset q['+q+'];\n';
            else if (t==='LWE'||t==='NTRU'||t==='KYBER') qasm+='// PQC: '+t+' on q['+q+']\n';
        }
    }
    if (!hasGates) qasm += '// Add gates to build your circuit';
    // Depth count
    var depth = 0;
    for (var si=0;si<MAX_STEPS;si++) {
        var hasGate=false;
        for (var qi=0;qi<NUM_QUBITS;qi++) if(circuit[qi][si])hasGate=true;
        if(hasGate) depth++;
    }
    document.getElementById('qasm-output').textContent = qasm.replace(/\n/g,' | ');
    document.getElementById('depth-label').textContent = 'Depth: '+depth;
    return qasm;
}

// ── CHALLENGES ───────────────────────────────────────────────────────────────
var currentChallenge = 0;
var challenges = [
    {
        title:'🎯 Challenge 1: Bell State',
        desc:'Create a Bell state — add H to q[0], then CNOT with q[0] as control and q[1] as target. Maximum entanglement!',
        check: function() {
            var hasH = false, hasCNOT = false;
            for (var s=0;s<MAX_STEPS;s++) {
                if (circuit[0][s] && circuit[0][s].type==='H') hasH=true;
                if (circuit[0][s] && circuit[0][s].type==='CNOT' && circuit[0][s].role==='control') hasCNOT=true;
            }
            return hasH && hasCNOT;
        }
    },
    {
        title:'🎯 Challenge 2: Superposition All',
        desc:'Put ALL qubits in superposition — place an H gate on every qubit wire.',
        check: function() {
            for (var q=0;q<NUM_QUBITS;q++) {
                var hasH=false;
                for (var s=0;s<MAX_STEPS;s++) if(circuit[q][s]&&circuit[q][s].type==='H') hasH=true;
                if(!hasH) return false;
            }
            return true;
        }
    },
    {
        title:'🎯 Challenge 3: Quantum Teleportation',
        desc:'Build the start of quantum teleportation: H on q[0], CNOT q[0]→q[1], then measure q[0].',
        check: function() {
            var hasH=false,hasCNOT=false,hasMeasure=false;
            for(var s=0;s<MAX_STEPS;s++){
                if(circuit[0][s]&&circuit[0][s].type==='H') hasH=true;
                if(circuit[0][s]&&circuit[0][s].type==='CNOT'&&circuit[0][s].role==='control') hasCNOT=true;
                if(circuit[0][s]&&circuit[0][s].type==='M') hasMeasure=true;
            }
            return hasH&&hasCNOT&&hasMeasure;
        }
    },
    {
        title:'🎯 Challenge 4: PQC Lattice Circuit',
        desc:'Add an LWE gate to any qubit to represent the lattice operation that makes ML-KEM quantum-safe!',
        check: function() {
            for(var q=0;q<NUM_QUBITS;q++)
                for(var s=0;s<MAX_STEPS;s++)
                    if(circuit[q][s]&&(circuit[q][s].type==='LWE'||circuit[q][s].type==='NTRU'||circuit[q][s].type==='KYBER')) return true;
            return false;
        }
    },
];

function checkChallenges() {
    if (currentChallenge >= challenges.length) return;
    var ch = challenges[currentChallenge];
    if (ch.check()) {
        document.getElementById('ch-badge').style.display='block';
        confetti();
        setTimeout(function() {
            currentChallenge++;
            if (currentChallenge < challenges.length) {
                document.getElementById('ch-title').textContent = challenges[currentChallenge].title;
                document.getElementById('ch-desc').textContent = challenges[currentChallenge].desc;
                document.getElementById('ch-badge').style.display='none';
            } else {
                document.getElementById('ch-title').textContent='🏆 All Challenges Complete!';
                document.getElementById('ch-desc').textContent='You mastered quantum circuits! You now understand the gates that make Shor Algorithm work — and why PQC algorithms like ML-KEM are designed to resist them.';
            }
        }, 2000);
    }
}

// ── GATE SELECTION ────────────────────────────────────────────────────────────
function selectGate(type) {
    selectedGateType = type;
    document.querySelectorAll('.gate-chip').forEach(function(el) {
        el.style.borderColor='transparent';
    });
    var info = GATE_INFO[type];
    if (info) {
        document.getElementById('gi-name').textContent = info.name;
        document.getElementById('gi-name').style.color = info.color;
        document.getElementById('gi-desc').textContent = info.desc;
        document.getElementById('gi-matrix').textContent = info.matrix;
        if (info.pqc) {
            document.getElementById('gi-pqc').textContent = '🔐 PQC Connection: '+info.pqc;
            document.getElementById('gi-pqc').style.display='block';
        } else {
            document.getElementById('gi-pqc').style.display='none';
        }
    }
}

// ── CONTROLS ──────────────────────────────────────────────────────────────────
function addQubit() {
    if (NUM_QUBITS >= 5) return;
    NUM_QUBITS++;
    circuit.push(new Array(MAX_STEPS).fill(null));
    blochStates.push({theta:0,phi:0});
    document.getElementById('qubit-count-label').textContent=NUM_QUBITS+' Qubits';
    resizeCanvas();updateAll();
}

function removeQubit() {
    if (NUM_QUBITS <= 1) return;
    NUM_QUBITS--;
    circuit.pop();blochStates.pop();
    document.getElementById('qubit-count-label').textContent=NUM_QUBITS+' Qubits';
    resizeCanvas();updateAll();
}

function clearCircuit() {
    for (var q=0;q<NUM_QUBITS;q++) circuit[q]=new Array(MAX_STEPS).fill(null);
    for (var q2=0;q2<NUM_QUBITS;q2++) blochStates[q2]={theta:0,phi:0};
    drawBloch(blochStates[0]);
    updateAll();
}

function updateAll() {
    draw();
    updateQASM();
    simulate();
}

function setResult(msg) {
    document.getElementById('result-msg').textContent=msg;
}

function confetti() {
    var cols=['#fbbf24','#10b981','#3b82f6','#8b5cf6','#ef4444'];
    for(var i=0;i<20;i++){setTimeout(function(){
        var el=document.createElement('div');el.className='cp';
        el.style.left=Math.random()*100+'vw';
        el.style.background=cols[Math.floor(Math.random()*cols.length)];
        el.style.animationDuration=(1+Math.random()*2)+'s';
        document.body.appendChild(el);setTimeout(function(){el.remove();},3000);
    },i*40);}
}

// ── INIT ──────────────────────────────────────────────────────────────────────
initCircuit();
selectGate('H');
drawBloch({theta:0,phi:0});
updateProbs();

// Animation loop
function loop(){requestAnimationFrame(loop);draw();}
loop();
</script>
</body>
</html>
""", height=1050, scrolling=True)
