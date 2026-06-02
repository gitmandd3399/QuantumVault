"""
modules/school_leaderboard.py
──────────────────────────────
School vs School leaderboard.
Schools compete nationally by average student XP.
Uses Streamlit's persistent storage.
"""

import streamlit as st
import datetime
import json


# Sample schools to make it feel alive from day one
SEED_SCHOOLS = [
    {"name": "Lincoln Elementary", "city": "Austin TX",        "xp": 4820, "students": 28, "grade": "K-5"},
    {"name": "Jefferson Middle",   "city": "Denver CO",         "xp": 6140, "students": 34, "grade": "6-8"},
    {"name": "Roosevelt High",     "city": "Seattle WA",        "xp": 8930, "students": 22, "grade": "9-12"},
    {"name": "Kennedy Academy",    "city": "Boston MA",         "xp": 5670, "students": 31, "grade": "K-12"},
    {"name": "Washington STEM",    "city": "Phoenix AZ",        "xp": 7210, "students": 19, "grade": "6-12"},
    {"name": "Franklin Tech",      "city": "Chicago IL",        "xp": 3890, "students": 42, "grade": "9-12"},
    {"name": "Madison Prep",       "city": "Nashville TN",      "xp": 5340, "students": 26, "grade": "6-8"},
    {"name": "Adams Cyber School", "city": "San Diego CA",      "xp": 9150, "students": 18, "grade": "9-12"},
    {"name": "Monroe Elementary",  "city": "Portland OR",       "xp": 4210, "students": 35, "grade": "K-5"},
    {"name": "Jackson Academy",    "city": "Miami FL",          "xp": 7680, "students": 23, "grade": "K-12"},
]


def get_schools() -> list:
    """Get all registered schools."""
    try:
        stored = st.session_state.get("school_lb_data")
        if stored:
            return json.loads(stored)
    except Exception:
        pass
    return SEED_SCHOOLS.copy()


def save_schools(schools: list):
    """Save schools to session state."""
    st.session_state.school_lb_data = json.dumps(schools)


def get_avg_xp(school: dict) -> float:
    return round(school["xp"] / max(school["students"], 1), 1)


def render_school_leaderboard():
    st.title("🏫 School vs School Leaderboard")
    st.markdown(
        "See how schools across the country rank in post-quantum cryptography education! "
        "Register your school to join the competition."
    )

    schools = get_schools()
    schools_sorted = sorted(schools, key=lambda s: get_avg_xp(s), reverse=True)

    # ── Top 3 podium ──────────────────────────────────────────────────────
    st.markdown("### 🏆 Top Schools This Month")
    if len(schools_sorted) >= 3:
        col1, col2, col3 = st.columns(3)
        medals = ["🥇", "🥈", "🥉"]
        colors = ["#f59e0b", "#9ca3af", "#cd7f32"]
        podium = [schools_sorted[1], schools_sorted[0], schools_sorted[2]]
        heights = ["160px", "200px", "140px"]

        for col, school, medal, color, height in zip(
            [col1, col2, col3], podium, ["🥈","🥇","🥉"], colors, heights
        ):
            with col:
                rank = schools_sorted.index(school) + 1
                st.markdown(
                    f"<div style='background:{color}20;border:2px solid {color};"
                    f"border-radius:12px;padding:16px;text-align:center;"
                    f"min-height:{height};display:flex;flex-direction:column;"
                    f"justify-content:center;'>"
                    f"<div style='font-size:2rem;margin-bottom:6px'>"
                    f"{'🥇' if rank==1 else '🥈' if rank==2 else '🥉'}</div>"
                    f"<div style='font-weight:bold;color:{color};font-size:0.95rem'>"
                    f"{school['name']}</div>"
                    f"<div style='font-size:0.78rem;color:#888;margin:3px 0'>"
                    f"{school['city']}</div>"
                    f"<div style='font-size:1.2rem;font-weight:bold;color:white;margin-top:6px'>"
                    f"{get_avg_xp(school)} avg XP</div>"
                    f"<div style='font-size:0.72rem;color:#888'>"
                    f"{school['students']} students</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

    st.markdown("---")

    # ── Full leaderboard table ────────────────────────────────────────────
    st.markdown("### 📊 Full Rankings")

    col1, col2, col3 = st.columns([1, 3, 2])
    with col1:
        grade_filter = st.selectbox(
            "Grade:",
            ["All", "K-5", "6-8", "9-12", "K-12", "6-12"],
            key="lb_grade_filter"
        )

    filtered = schools_sorted if grade_filter == "All" else [
        s for s in schools_sorted
        if s.get("grade", "") == grade_filter
    ]

    for i, school in enumerate(filtered):
        rank = i + 1
        avg = get_avg_xp(school)
        medal = "🥇" if rank==1 else "🥈" if rank==2 else "🥉" if rank==3 else f"#{rank}"
        color = "#f59e0b" if rank==1 else "#9ca3af" if rank==2 else "#cd7f32" if rank==3 else "#4f46e5"

        st.markdown(
            f"<div style='background:#1e293b;border:1px solid #334155;"
            f"border-radius:10px;padding:12px 16px;margin:5px 0;"
            f"display:flex;justify-content:space-between;align-items:center;'>"
            f"<div style='display:flex;align-items:center;gap:12px;'>"
            f"<span style='font-size:1.2rem;min-width:36px;color:{color}'>{medal}</span>"
            f"<div>"
            f"<div style='font-weight:bold;color:white'>{school['name']}</div>"
            f"<div style='font-size:0.78rem;color:#888'>"
            f"📍 {school['city']} · {school.get('grade','K-12')} · "
            f"{school['students']} students</div>"
            f"</div>"
            f"</div>"
            f"<div style='text-align:right'>"
            f"<div style='font-size:1.2rem;font-weight:bold;color:{color}'>"
            f"{avg}</div>"
            f"<div style='font-size:0.7rem;color:#888'>avg XP</div>"
            f"</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ── Register school ───────────────────────────────────────────────────
    st.markdown("### 🏫 Register Your School")
    st.markdown(
        "Add your school to the leaderboard! "
        "Your school's average XP will be tracked as students learn."
    )

    col1, col2 = st.columns(2)
    with col1:
        school_name = st.text_input(
            "School name:",
            placeholder="Lincoln Elementary School",
            key="reg_school_name"
        )
        school_city = st.text_input(
            "City and State:",
            placeholder="Austin TX",
            key="reg_school_city"
        )
    with col2:
        school_grade = st.selectbox(
            "Grade levels:",
            ["K-5", "6-8", "9-12", "K-12", "6-12"],
            key="reg_school_grade"
        )
        school_students = st.number_input(
            "Number of students:",
            min_value=1, max_value=500,
            value=25,
            key="reg_school_students"
        )

    current_xp = st.session_state.get("xp", 0)

    if st.button("🏫 Register School!", key="reg_school", type="primary"):
        if not school_name or not school_city:
            st.error("Please enter your school name and city!")
        else:
            # Check if already registered
            existing = next(
                (s for s in schools if s["name"].lower() == school_name.lower()),
                None
            )
            if existing:
                # Update XP
                existing["xp"] = max(existing["xp"], current_xp * school_students)
                st.success(f"✅ Updated {school_name}'s score!")
            else:
                new_school = {
                    "name": school_name,
                    "city": school_city,
                    "xp": current_xp * school_students,
                    "students": school_students,
                    "grade": school_grade,
                    "registered": str(datetime.date.today()),
                }
                schools.append(new_school)
                save_schools(schools)
                rank = sorted(
                    schools, key=lambda s: get_avg_xp(s), reverse=True
                ).index(new_school) + 1
                st.success(
                    f"🎉 {school_name} registered! "
                    f"Starting rank: #{rank} out of {len(schools)} schools!"
                )
                st.balloons()

    st.markdown("---")

    # ── Stats ─────────────────────────────────────────────────────────────
    total_students = sum(s["students"] for s in schools)
    total_xp = sum(s["xp"] for s in schools)
    top_school = schools_sorted[0] if schools_sorted else None

    st.markdown("### 🌍 National Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏫 Schools", len(schools))
    with col2:
        st.metric("👥 Students", total_students)
    with col3:
        st.metric("⭐ Total XP", f"{total_xp:,}")
    with col4:
        if top_school:
            st.metric("🥇 Top School", top_school["name"].split()[0])
