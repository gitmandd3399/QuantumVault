def render_quantum_sandbox():
    """Quantum Sandbox — minimal test version."""
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("🧪 Quantum Sandbox")
    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
body{background:#020d14;color:white;font-family:sans-serif;margin:0;padding:20px;}
#cv{border:2px solid #3b82f6;cursor:crosshair;display:block;}
#msg{color:#10b981;margin-top:8px;font-size:14px;}
.btn{padding:8px 16px;background:#1d4ed8;border:none;border-radius:8px;
    color:white;cursor:pointer;margin:4px;font-size:12px;}
</style>
</head>
<body>
<canvas id="cv" width="500" height="300"></canvas>
<div id="msg">Click the canvas or buttons to test!</div>
<div>
    <button class="btn" onclick="addBall()">Add Ball</button>
    <button class="btn" onclick="clearAll()">Clear</button>
</div>
<script>
const cv = document.getElementById("cv");
const cx = cv.getContext("2d");
let balls = [];

cv.addEventListener("click", function(e) {
    const r = cv.getBoundingClientRect();
    const x = e.clientX - r.left;
    const y = e.clientY - r.top;
    balls.push({x:x, y:y, vx:(Math.random()-0.5)*4, vy:-3, r:10, color:"#10b981"});
    document.getElementById("msg").textContent = "Clicked at " + Math.round(x) + "," + Math.round(y) + "! Balls: " + balls.length;
});

function addBall(){
    balls.push({x:250, y:50, vx:(Math.random()-0.5)*4, vy:-2, r:12, color:"#fbbf24"});
    document.getElementById("msg").textContent = "Ball added! Total: " + balls.length;
}

function clearAll(){ balls=[]; document.getElementById("msg").textContent = "Cleared!"; }

function loop(){
    requestAnimationFrame(loop);
    cx.fillStyle="#020d14"; cx.fillRect(0,0,500,300);
    balls.forEach(function(b){
        b.vy += 0.3;
        b.x += b.vx; b.y += b.vy;
        if(b.y+b.r>290){b.y=290-b.r;b.vy*=-0.7;b.vx*=0.95;}
        if(b.x-b.r<0||b.x+b.r>500) b.vx*=-0.8;
        cx.beginPath();cx.arc(b.x,b.y,b.r,0,Math.PI*2);
        cx.fillStyle=b.color;cx.fill();
    });
}
loop();
document.getElementById("msg").textContent = "Ready! Click canvas to spawn balls.";
</script>
</body>
</html>
""", height=420)
