def render_logic_gates():
    import streamlit as st
    import streamlit.components.v1 as components
    st.subheader("Logic Gate Lab")
    components.html("""
<html>
<body style="background:#020d14;color:white;font-family:sans-serif;padding:20px;">
<h3>Logic Gate Lab Test</h3>
<p>If you see this, the tab is working!</p>
<canvas id="cv" width="400" height="200" style="border:1px solid #3b82f6;display:block;margin-top:10px;"></canvas>
<script>
var cv=document.getElementById('cv');
var cx=cv.getContext('2d');
cx.fillStyle='#020d14';cx.fillRect(0,0,400,200);
cx.font='bold 20px sans-serif';cx.fillStyle='#10b981';cx.textAlign='center';
cx.fillText('Canvas is working!',200,100);
</script>
</body>
</html>
""", height=300)
