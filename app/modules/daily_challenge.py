"""
modules/daily_challenge.py
───────────────────────────
Daily mini challenge system.
New challenge every day, resets at midnight.
Bonus XP for completion.
"""

import streamlit as st
import datetime
import hashlib
import streamlit.components.v1 as components

# 30 rotating challenges — one per day
CHALLENGES = [
    {"id":"c01", "title":"Speed Demon",        "desc":"Complete the Lock Puzzle in under 5 seconds!",                "xp":25, "type":"speed",   "icon":"⚡", "module":"Elementary → Lock Puzzle"},
    {"id":"c02", "title":"Word Hunter",         "desc":"Find all 7 words in the Word Search Level 1!",               "xp":20, "type":"puzzle",  "icon":"🔤", "module":"Elementary → Word Search"},
    {"id":"c03", "title":"Crossword King",      "desc":"Complete Crossword Level 1 without hints!",                  "xp":25, "type":"puzzle",  "icon":"✏️", "module":"Elementary → Crossword"},
    {"id":"c04", "title":"Block Catcher",       "desc":"Catch 20 safe blocks in Falling Blocks without missing one!", "xp":30, "type":"game",   "icon":"🧱", "module":"Elementary → Falling Blocks"},
    {"id":"c05", "title":"Zombie Slayer",       "desc":"Complete Wave 3 in Zombie Blast!",                           "xp":30, "type":"game",   "icon":"🧟", "module":"Elementary → Zombie Blast"},
    {"id":"c06", "title":"Story Master",        "desc":"Read all 5 chapters of Agent Pixel!",                        "xp":20, "type":"learn",  "icon":"📖", "module":"Elementary → Story Time"},
    {"id":"c07", "title":"Lattice Navigator",   "desc":"Collect all keys in Lattice Maze Level 1!",                  "xp":25, "type":"game",   "icon":"🌀", "module":"Middle School → Lattice Maze"},
    {"id":"c08", "title":"Hash Detective",      "desc":"Find the avalanche effect in the Hash Visualizer!",          "xp":20, "type":"learn",  "icon":"🔢", "module":"Middle School → Hash Visualizer"},
    {"id":"c09", "title":"Key Expert",          "desc":"Complete the Key Size Lab quiz with a perfect score!",       "xp":25, "type":"quiz",   "icon":"🔬", "module":"Middle School → Key Size Lab"},
    {"id":"c10", "title":"Quantum Racer",       "desc":"Run the RSA vs Kyber race and explain the result!",          "xp":20, "type":"learn",  "icon":"⚡", "module":"Middle School → Quantum Race"},
    {"id":"c11", "title":"Maze Master",         "desc":"Escape the Lattice Maze in under 3 minutes!",              "xp":30, "type":"game",   "icon":"🌀", "module":"Middle School → Lattice Maze"},
    {"id":"c12", "title":"Tower Defender",      "desc":"Survive Wave 5 in PQC Tower Defense!",                      "xp":35, "type":"game",   "icon":"🛡️", "module":"High School → Tower Defense"},
    {"id":"c13", "title":"Timeline Scholar",    "desc":"Study the full NIST PQC timeline!",                         "xp":20, "type":"learn",  "icon":"📅", "module":"High School → NIST Timeline"},
    {"id":"c14", "title":"Algorithm Analyst",   "desc":"Compare all 4 NIST algorithms in the Algorithm Lab!",       "xp":25, "type":"learn",  "icon":"⚖️", "module":"High School → Algorithm Lab"},
    {"id":"c15", "title":"Code Wizard",         "desc":"Run the LWE Python code and modify the noise parameter!",   "xp":30, "type":"code",   "icon":"💻", "module":"High School → Code It Yourself"},
    {"id":"c16", "title":"Math Level 1",        "desc":"Score 100% on Math Challenge Level 1!",                     "xp":25, "type":"math",   "icon":"🧮", "module":"High School → Math Challenge"},
    {"id":"c17", "title":"Math Level 2",        "desc":"Complete Math Challenge Level 2 — Prime Numbers!",          "xp":30, "type":"math",   "icon":"🔑", "module":"High School → Math Challenge"},
    {"id":"c18", "title":"Streak Keeper",       "desc":"Log in 3 days in a row to earn bonus XP!",                 "xp":40, "type":"streak", "icon":"🔥", "module":"Any module"},
    {"id":"c19", "title":"Card Collector",      "desc":"Unlock 3 trading cards in one session!",                    "xp":35, "type":"collect","icon":"🃏", "module":"Complete activities"},
    {"id":"c20", "title":"XP Grinder",          "desc":"Earn 50 XP in a single session!",                           "xp":30, "type":"xp",     "icon":"⭐", "module":"Any module"},
    {"id":"c21", "title":"Word Master",         "desc":"Complete Word Search Level 3!",                             "xp":30, "type":"puzzle", "icon":"🔤", "module":"Elementary → Word Search"},
    {"id":"c22", "title":"Wave Survivor",       "desc":"Survive 6 waves in Zombie Blast!",                         "xp":40, "type":"game",   "icon":"🧟", "module":"Middle School → Zombie Blast"},
    {"id":"c23", "title":"Zombie Veteran",      "desc":"Clear Wave 6 in Zombie Blast Medium!",                     "xp":40, "type":"game",   "icon":"🧟", "module":"Middle School → Zombie Blast"},
    {"id":"c24", "title":"Tower Master",        "desc":"Survive Wave 8 in PQC Tower Defense!",                     "xp":45, "type":"game",   "icon":"🛡️", "module":"High School → Tower Defense"},
    {"id":"c25", "title":"Lattice Expert",      "desc":"Complete Lattice Maze Level 6!",                           "xp":40, "type":"game",   "icon":"🌀", "module":"Middle School → Lattice Maze"},
    {"id":"c26", "title":"Block Champion",      "desc":"Reach Level 6 in Falling Blocks!",                         "xp":35, "type":"game",   "icon":"🧱", "module":"Elementary → Falling Blocks"},
    {"id":"c27", "title":"Threat Modeler",      "desc":"Complete the Threat Modeler in High School!",              "xp":25, "type":"learn",  "icon":"🛡️", "module":"High School → Threat Modeler"},
    {"id":"c28", "title":"Research Writer",     "desc":"Write a Research Journal entry in High School!",           "xp":25, "type":"learn",  "icon":"🔬", "module":"High School → Research Journal"},
    {"id":"c29", "title":"Math Level 3",        "desc":"Complete Math Challenge Level 3 — Matrix Math!",           "xp":40, "type":"math",   "icon":"🏗️", "module":"High School → Math Challenge"},
    {"id":"c30", "title":"Quantum Guardian",    "desc":"Earn 500 total XP — become a Quantum Guardian!",           "xp":100,"type":"epic",   "icon":"🛡️", "module":"All modules"},
]

TYPE_COLORS = {
    "speed":   "#f59e0b",
    "puzzle":  "#8b5cf6",
    "game":    "#10b981",
    "learn":   "#3b82f6",
    "quiz":    "#06b6d4",
    "code":    "#ec4899",
    "math":    "#f97316",
    "streak":  "#ef4444",
    "collect": "#fbbf24",
    "xp":      "#a3e635",
    "epic":    "#4f46e5",
}


def get_todays_challenge():
    """Get today's challenge based on the date."""
    today = datetime.date.today()
    day_num = (today - datetime.date(2024, 1, 1)).days
    idx = day_num % len(CHALLENGES)
    return CHALLENGES[idx]


def get_bonus_challenge():
    """Get a bonus challenge based on the week."""
    today = datetime.date.today()
    week_num = today.isocalendar()[1]
    idx = (week_num * 7) % len(CHALLENGES)
    return CHALLENGES[(idx + 15) % len(CHALLENGES)]


def is_challenge_complete(challenge_id: str) -> bool:
    today = str(datetime.date.today())
    key = f"challenge_done_{today}_{challenge_id}"
    return st.session_state.get(key, False)


def mark_challenge_complete(challenge_id: str):
    today = str(datetime.date.today())
    key = f"challenge_done_{today}_{challenge_id}"
    st.session_state[key] = True


def render_daily_challenge():
    st.title("🎯 Daily Challenges")
    st.markdown(
        "A new challenge appears every day at midnight! "
        "Complete them for bonus XP and special badges."
    )

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    midnight = datetime.datetime.combine(tomorrow, datetime.time.min)
    now = datetime.datetime.now()
    time_left = midnight - now
    hours = int(time_left.total_seconds() // 3600)
    mins = int((time_left.total_seconds() % 3600) // 60)

    st.markdown(
        f"<div style='background:#1e293b;border:1px solid #334155;"
        f"border-radius:8px;padding:8px 16px;display:inline-block;"
        f"font-size:0.85rem;color:#a5b4fc;margin-bottom:16px;'>"
        f"⏰ Resets in: <strong>{hours}h {mins}m</strong></div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Today's main challenge
    challenge = get_todays_challenge()
    bonus = get_bonus_challenge()
    color = TYPE_COLORS.get(challenge["type"], "#4f46e5")
    done = is_challenge_complete(challenge["id"])

    st.markdown("### 🌟 Today's Challenge")
    st.markdown(
        f"<div style='background:{color}15;border:2px solid {color}50;"
        f"border-radius:16px;padding:1.5rem;margin-bottom:1rem;'>"
        f"<div style='display:flex;justify-content:space-between;align-items:flex-start;'>"
        f"<div>"
        f"<div style='font-size:2.5rem;margin-bottom:8px'>{challenge['icon']}</div>"
        f"<h2 style='color:{color};margin:0 0 4px'>{challenge['title']}</h2>"
        f"<p style='color:#ccc;margin:0 0 8px;font-size:0.9rem'>{challenge['desc']}</p>"
        f"<div style='font-size:0.78rem;color:#888'>📍 {challenge['module']}</div>"
        f"</div>"
        f"<div style='text-align:right'>"
        f"<div style='font-size:2rem;font-weight:bold;color:{color}'>+{challenge['xp']}</div>"
        f"<div style='font-size:0.75rem;color:#888'>XP Reward</div>"
        f"<div style='margin-top:8px;background:{color}20;border:1px solid {color}50;"
        f"border-radius:100px;padding:3px 10px;font-size:0.72rem;color:{color};'>"
        f"{challenge['type'].upper()}</div>"
        f"</div>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    if done:
        st.success(f"✅ Challenge completed! +{challenge['xp']} XP earned today!")
    else:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info(f"Go to **{challenge['module']}** to complete this challenge!")
        with col2:
            if st.button(
                f"✅ Mark Complete! +{challenge['xp']} XP",
                key="complete_daily",
                type="primary"
            ):
                mark_challenge_complete(challenge["id"])
                st.session_state.xp = st.session_state.get("xp", 0) + challenge["xp"]
                if challenge["xp"] >= 50:
                    st.session_state.badges = st.session_state.get("badges", []) + [
                        f"🎯 {challenge['title']}"
                    ]
                st.success(f"🎉 +{challenge['xp']} XP! Come back tomorrow for a new challenge!")
                st.balloons()
                st.rerun()

    st.markdown("---")

    # Bonus challenge
    bonus_color = TYPE_COLORS.get(bonus["type"], "#4f46e5")
    bonus_done = is_challenge_complete(bonus["id"] + "_bonus")

    st.markdown("### ⚡ Bonus Challenge")
    st.markdown(
        f"<div style='background:{bonus_color}10;border:1px solid {bonus_color}40;"
        f"border-radius:12px;padding:1rem;margin-bottom:1rem;'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
        f"<div>"
        f"<span style='font-size:1.5rem'>{bonus['icon']}</span>"
        f"<strong style='color:{bonus_color};margin-left:8px'>{bonus['title']}</strong>"
        f"<div style='font-size:0.8rem;color:#888;margin-top:4px'>{bonus['desc']}</div>"
        f"</div>"
        f"<div style='font-size:1.5rem;font-weight:bold;color:{bonus_color}'>+{bonus['xp']} XP</div>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    if bonus_done:
        st.success("✅ Bonus challenge completed!")
    else:
        if st.button(
            f"✅ Complete Bonus! +{bonus['xp']} XP",
            key="complete_bonus"
        ):
            mark_challenge_complete(bonus["id"] + "_bonus")
            st.session_state.xp = st.session_state.get("xp", 0) + bonus["xp"]
            st.success(f"🎉 Bonus complete! +{bonus['xp']} XP!")
            st.rerun()

    st.markdown("---")

    # Challenge history / upcoming
    st.markdown("### 📅 Upcoming Challenges")
    st.caption("Preview the next 5 days of challenges")

    for i in range(1, 6):
        future_date = today + datetime.timedelta(days=i)
        day_num = (future_date - datetime.date(2024, 1, 1)).days
        future_challenge = CHALLENGES[day_num % len(CHALLENGES)]
        future_color = TYPE_COLORS.get(future_challenge["type"], "#4f46e5")

        st.markdown(
            f"<div style='background:#1e293b;border:1px solid #334155;"
            f"border-radius:8px;padding:8px 12px;margin:4px 0;"
            f"display:flex;justify-content:space-between;align-items:center;'>"
            f"<div>"
            f"<span style='font-size:0.8rem;color:#888'>"
            f"{future_date.strftime('%A %b %d')}</span>"
            f"<div style='font-size:0.85rem;font-weight:bold;color:{future_color}'>"
            f"{future_challenge['icon']} {future_challenge['title']}</div>"
            f"</div>"
            f"<div style='font-size:0.8rem;color:{future_color};font-weight:bold'>"
            f"+{future_challenge['xp']} XP</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("### 🏆 All 30 Challenges")
    st.caption("Complete all 30 to become a true Quantum Guardian!")

    done_count = sum(
        1 for c in CHALLENGES
        if st.session_state.get(
            f"challenge_done_{datetime.date.today()}_{c['id']}", False
        )
    )

    st.progress(done_count / len(CHALLENGES))
    st.caption(f"{done_count}/{len(CHALLENGES)} challenges completed today")

    for c in CHALLENGES:
        c_color = TYPE_COLORS.get(c["type"], "#4f46e5")
        c_done = is_challenge_complete(c["id"])
        st.markdown(
            f"<div style='opacity:{'1' if c_done else '0.6'};padding:4px 0;"
            f"display:flex;justify-content:space-between;align-items:center;'>"
            f"<span style='font-size:0.82rem;color:{'#10b981' if c_done else '#888'}'>"
            f"{'✅' if c_done else c['icon']} {c['title']} — {c['desc'][:50]}...</span>"
            f"<span style='font-size:0.78rem;color:{c_color};font-weight:bold'>"
            f"+{c['xp']} XP</span>"
            f"</div>",
            unsafe_allow_html=True
        )
