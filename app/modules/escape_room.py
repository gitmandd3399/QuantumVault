"""
modules/escape_room.py
───────────────────────
Quantum Escape Room — solve 5 PQC puzzles before time runs out!
High school focused but adaptable for all grades.
"""
import streamlit as st
import streamlit.components.v1 as components
import time


PUZZLES = [
    {
        "id": "p1", "title": "🔑 The Broken Lock",
        "desc": "The vault is locked with RSA-2048. The Quantum Monster has a quantum computer. How many years until RSA is broken?",
        "type": "multiple_choice",
        "options": ["Millions of years", "Hours to days", "Never — RSA is unbreakable", "100 years"],
        "answer": 1,
        "xp": 20,
        "color": "#ef4444",
        "solved_msg": "Correct! Shor's Algorithm breaks RSA in hours on a sufficiently large quantum computer. You need to replace the lock!",
    },
    {
        "id": "p2", "title": "🏗️ The Lattice Code",
        "desc": "To open Door 2, solve this LWE equation: A=5, e=-1, b=19, mod q=23. What is secret s?",
        "type": "number",
        "answer": "4",
        "xp": 30,
        "color": "#7c6dfa",
        "hint": "5*s + (-1) ≡ 19 mod 23 → 5s ≡ 20 mod 23 → s = ?",
        "solved_msg": "s=4! Because 5*4-1=19. You solved an LWE equation — the same math that protects Kyber!",
    },
    {
        "id": "p3", "title": "🔢 The Hash Combination",
        "desc": "The safe combination is the number of bits in a SHA3-256 hash output. Enter it:",
        "type": "number",
        "answer": "256",
        "xp": 20,
        "color": "#3b82f6",
        "hint": "SHA3-256 has the answer in its name...",
        "solved_msg": "256 bits! SHA3-256 always produces exactly 256 bits regardless of input size.",
    },
    {
        "id": "p4", "title": "📅 The Time Vault",
        "desc": "The final door needs the FIPS number of the ML-KEM standard (the Kyber standard). Enter the 3-digit number:",
        "type": "number",
        "answer": "203",
        "xp": 25,
        "color": "#10b981",
        "hint": "FIPS 20_ — Kyber was the first NIST PQC standard",
        "solved_msg": "FIPS 203! ML-KEM (Kyber) was standardized as FIPS 203 in August 2024.",
    },
    {
        "id": "p5", "title": "🛡️ The Final Cipher",
        "desc": "The escape code is the name of the quantum algorithm that breaks RSA. It was invented in 1994 by a mathematician at Bell Labs. Enter the last name:",
        "type": "text",
        "answer": "SHOR",
        "xp": 35,
        "color": "#f59e0b",
        "hint": "Peter _____ invented the algorithm in 1994",
        "solved_msg": "SHOR! Peter Shor invented Shor's Algorithm in 1994. It factors large numbers exponentially faster — breaking RSA and ECC!",
    },
]


def render_escape_room():
    st.title("🏃 Quantum Escape Room!")
    st.markdown(
        "⚠️ **ALERT: The Quantum Monster has breached the perimeter!** "
        "You are locked in the Crypto Vault. Solve 5 PQC puzzles to escape "
        "before the quantum computer breaks through the final door!"
    )

    # Initialize state
    if "escape_started" not in st.session_state:
        st.session_state.escape_started = False
    if "escape_start_time" not in st.session_state:
        st.session_state.escape_start_time = None
    if "escape_solved" not in st.session_state:
        st.session_state.escape_solved = set()
    if "escape_hints" not in st.session_state:
        st.session_state.escape_hints = set()
    if "escape_complete" not in st.session_state:
        st.session_state.escape_complete = False

    TIME_LIMIT = 300  # 5 minutes

    if not st.session_state.escape_started:
        # Pre-game screen
        components.html("""
<style>
body{margin:0;background:#0f172a;font-family:sans-serif;color:white;padding:16px;}
.intro{max-width:500px;margin:0 auto;text-align:center;}
.monster{font-size:5rem;animation:pulse 1s infinite;}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.1)}}
.door{font-size:3rem;margin:8px 0;}
.rules{background:#1e293b;border:1px solid #334155;border-radius:12px;
padding:16px;text-align:left;margin:12px 0;font-size:0.85rem;color:#ccc;line-height:1.8;}
.rule-item{display:flex;gap:8px;margin:4px 0;}
</style>
<div class="intro">
<div class="monster">👾</div>
<div style="color:#ef4444;font-weight:bold;font-size:1.1rem;margin:6px 0">
QUANTUM MONSTER DETECTED — 5 MINUTES TO ESCAPE!</div>
<div style="font-size:0.85rem;color:#888;margin-bottom:12px">
Solve 5 cryptography puzzles to unlock each door</div>
<div class="rules">
<div class="rule-item"><span>🧩</span><span>5 PQC puzzles — each unlocks one door</span></div>
<div class="rule-item"><span>⏱️</span><span>5 minute time limit — stay calm!</span></div>
<div class="rule-item"><span>💡</span><span>Hints available — cost 5 XP each</span></div>
<div class="rule-item"><span>🏆</span><span>Bonus XP for finishing fast!</span></div>
<div class="rule-item"><span>📚</span><span>Every puzzle teaches real PQC concepts</span></div>
</div>
</div>
""", height=340)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚨 START ESCAPE ROOM!", key="escape_start", type="primary", use_container_width=True):
                st.session_state.escape_started = True
                st.session_state.escape_start_time = time.time()
                st.session_state.escape_solved = set()
                st.session_state.escape_hints = set()
                st.session_state.escape_complete = False
                st.rerun()
        return

    if st.session_state.escape_complete:
        elapsed = int(time.time() - st.session_state.escape_start_time)
        mins = elapsed // 60
        secs = elapsed % 60
        bonus_xp = max(0, 100 - elapsed // 3)
        total_xp = sum(p["xp"] for p in PUZZLES if p["id"] in st.session_state.escape_solved) + bonus_xp

        components.html(f"""
<style>
body{{margin:0;background:#0f172a;font-family:sans-serif;color:white;padding:16px;text-align:center;}}
.trophy{{font-size:5rem;animation:bounce 0.5s infinite;}}
@keyframes bounce{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-15px)}}}}
</style>
<div>
<div class="trophy">🏆</div>
<h2 style="color:#10b981;margin:8px 0">YOU ESCAPED!</h2>
<p style="color:#ccc">The Quantum Monster has been defeated!</p>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;max-width:400px;margin:12px auto;">
<div style="background:#1e293b;border-radius:10px;padding:12px;">
<div style="font-size:1.5rem;font-weight:bold;color:#10b981">{mins}:{secs:02d}</div>
<div style="font-size:0.7rem;color:#888">TIME</div>
</div>
<div style="background:#1e293b;border-radius:10px;padding:12px;">
<div style="font-size:1.5rem;font-weight:bold;color:#f59e0b">+{bonus_xp}</div>
<div style="font-size:0.7rem;color:#888">SPEED BONUS XP</div>
</div>
<div style="background:#1e293b;border-radius:10px;padding:12px;">
<div style="font-size:1.5rem;font-weight:bold;color:#4f46e5">+{total_xp}</div>
<div style="font-size:0.7rem;color:#888">TOTAL XP</div>
</div>
</div>
</div>
""", height=280)
        if st.button("🔄 Play Again!", key="escape_reset", type="primary"):
            st.session_state.escape_started = False
            st.session_state.escape_complete = False
            st.rerun()
        return

    # Timer
    elapsed = int(time.time() - st.session_state.escape_start_time)
    remaining = max(0, TIME_LIMIT - elapsed)
    mins_left = remaining // 60
    secs_left = remaining % 60
    time_pct = remaining / TIME_LIMIT
    time_color = "#10b981" if time_pct > 0.5 else "#f59e0b" if time_pct > 0.25 else "#ef4444"

    st.markdown(
        f"<div style='background:{time_color}15;border:2px solid {time_color};"
        f"border-radius:10px;padding:10px;text-align:center;margin-bottom:12px'>"
        f"<span style='font-size:1.5rem;font-weight:bold;color:{time_color}'>"
        f"⏱️ {mins_left}:{secs_left:02d} remaining</span>"
        f"<span style='color:#888;font-size:0.8rem;margin-left:12px'>"
        f"{len(st.session_state.escape_solved)}/5 doors unlocked</span>"
        f"</div>",
        unsafe_allow_html=True
    )

    if remaining == 0:
        st.error("⏰ TIME'S UP! The Quantum Monster broke through! Try again!")
        if st.button("🔄 Try Again", key="escape_timeout"):
            st.session_state.escape_started = False
            st.rerun()
        return

    # Door progress display
    door_cols = st.columns(5)
    for i, (col, puz) in enumerate(zip(door_cols, PUZZLES)):
        with col:
            solved = puz["id"] in st.session_state.escape_solved
            c = puz["color"]
            st.markdown(
                f"<div style='background:{'%s20' % c if solved else '#1e293b'};"
                f"border:2px solid {'%s' % c if solved else '#334155'};"
                f"border-radius:10px;padding:8px;text-align:center'>"
                f"<div style='font-size:1.5rem'>{'🔓' if solved else '🔒'}</div>"
                f"<div style='font-size:0.65rem;color:{'%s' % c if solved else '#888'}'>Door {i+1}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.markdown("---")

    # Find current unsolved puzzle
    current_puzzle = None
    for puz in PUZZLES:
        if puz["id"] not in st.session_state.escape_solved:
            current_puzzle = puz
            break

    if current_puzzle is None:
        st.session_state.escape_complete = True
        bonus_xp = max(0, 100 - elapsed // 3)
        st.session_state.xp = st.session_state.get("xp", 0) + bonus_xp
        st.session_state.badges = st.session_state.get("badges", []) + ["🏃 Escape Artist"]
        st.balloons()
        st.rerun()
        return

    puz = current_puzzle
    color = puz["color"]

    st.markdown(
        f"<div style='background:{color}15;border:2px solid {color}60;"
        f"border-radius:14px;padding:20px;margin:8px 0'>"
        f"<h3 style='color:{color};margin:0 0 8px'>{puz['title']}</h3>"
        f"<p style='color:#ccc;margin:0;font-size:0.92rem;line-height:1.6'>{puz['desc']}</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    hint_shown = puz["id"] in st.session_state.escape_hints
    col1, col2 = st.columns([3, 1])
    with col1:
        if puz["type"] == "multiple_choice":
            ans = st.radio("Choose:", puz["options"], key=f"escape_{puz['id']}")
        else:
            ans = st.text_input("Your answer:", key=f"escape_{puz['id']}", placeholder="Type here...")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if "hint" in puz and not hint_shown:
            if st.button("💡 Hint (-5 XP)", key=f"hint_{puz['id']}"):
                st.session_state.escape_hints.add(puz["id"])
                st.session_state.xp = max(0, st.session_state.get("xp", 0) - 5)
                st.rerun()

    if hint_shown and "hint" in puz:
        st.info(f"💡 {puz['hint']}")

    if st.button("🔓 Unlock Door!", key=f"submit_{puz['id']}", type="primary"):
        correct = False
        if puz["type"] == "multiple_choice":
            correct = puz["options"].index(ans) == puz["answer"]
        else:
            correct = str(ans).upper().strip() == str(puz["answer"]).upper().strip()

        if correct:
            st.session_state.escape_solved.add(puz["id"])
            xp = puz["xp"]
            st.session_state.xp = st.session_state.get("xp", 0) + xp
            st.success(f"🔓 DOOR UNLOCKED! +{xp} XP — {puz['solved_msg']}")
            st.rerun()
        else:
            st.error("❌ Wrong code! The door stays locked. Try again!")
