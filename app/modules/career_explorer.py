"""
modules/career_explorer.py
PQC Career Explorer — interactive map of careers using post-quantum cryptography.
"""
import streamlit as st
import streamlit.components.v1 as components


CAREERS = [
    {
        "title": "🔐 Cryptographer",
        "salary": "$120,000-$200,000/yr",
        "growth": "Very High",
        "color": "#10b981",
        "education": "PhD in Mathematics or CS preferred",
        "companies": ["NSA", "NIST", "Google", "Microsoft", "IBM Research"],
        "skills": ["Abstract algebra", "Lattice math", "Python/C++", "Research writing"],
        "pqc_role": "Design and analyze post-quantum algorithms. Review NIST submissions. Build the math that protects the internet.",
        "day_in_life": "Morning: Review a proposed lattice reduction algorithm. Afternoon: Write proofs for a new signature scheme. Evening: Peer review a colleague's paper on NTRU variants.",
        "path": "Math degree → PhD → Research position → Published papers → Senior cryptographer",
    },
    {
        "title": "🛡️ Security Engineer",
        "salary": "$110,000-$180,000/yr",
        "growth": "Extremely High",
        "color": "#3b82f6",
        "education": "BS/MS in Computer Science or Cybersecurity",
        "companies": ["CloudFlare", "Apple", "Amazon", "Defense contractors", "Banks"],
        "skills": ["TLS implementation", "Key management", "Python/Rust/Go", "PKI"],
        "pqc_role": "Integrate Kyber and Dilithium into real systems. Migrate TLS from ECDH to ML-KEM. Test PQC libraries for vulnerabilities.",
        "day_in_life": "Morning: Code review for Kyber implementation in TLS library. Afternoon: Deploy hybrid PQC+classical to production. Evening: Write incident response plan for quantum threats.",
        "path": "CS degree → Security certifications (CISSP) → Junior engineer → Senior security engineer",
    },
    {
        "title": "⚛️ Quantum Computing Researcher",
        "salary": "$130,000-$220,000/yr",
        "growth": "Explosive",
        "color": "#8b5cf6",
        "education": "PhD in Physics, CS, or Electrical Engineering",
        "companies": ["IBM Quantum", "Google Quantum AI", "IonQ", "Quantinuum", "Microsoft"],
        "skills": ["Quantum mechanics", "Qiskit/Cirq", "Linear algebra", "Error correction"],
        "pqc_role": "Build the very computers that PQC defends against! Or research quantum error correction that determines when RSA actually breaks.",
        "day_in_life": "Morning: Run Shor's Algorithm on 20-qubit processor. Afternoon: Analyze error rates in new qubit design. Evening: Conference call with global quantum team.",
        "path": "Physics/CS degree → PhD → Postdoc → Research scientist at quantum lab",
    },
    {
        "title": "🏛️ Government Policy Analyst",
        "salary": "$80,000-$140,000/yr",
        "growth": "High",
        "color": "#f59e0b",
        "education": "BS in CS or Policy + technical background",
        "companies": ["NSA", "CISA", "NIST", "DHS", "Defense agencies"],
        "skills": ["Technical writing", "Policy analysis", "Risk assessment", "Communications"],
        "pqc_role": "Write the policies that require federal agencies to migrate to PQC. Assess national security risk. Implement NSM-10 requirements across government.",
        "day_in_life": "Morning: Briefing on quantum computing milestones from intelligence community. Afternoon: Draft PQC migration guidance for federal agencies. Evening: Congressional testimony preparation.",
        "path": "Technical degree → Security clearance → Government position → Policy leadership",
    },
    {
        "title": "💻 PQC Software Developer",
        "salary": "$100,000-$160,000/yr",
        "growth": "Very High",
        "color": "#ec4899",
        "education": "BS in Computer Science",
        "companies": ["Open Quantum Safe", "Signal", "ProtonMail", "Security startups"],
        "skills": ["C/C++/Rust", "Cryptographic libraries", "Side-channel analysis", "Testing"],
        "pqc_role": "Implement FIPS 203/204/205/206 in software libraries. Build liboqs. Ensure constant-time implementations to prevent side-channel attacks.",
        "day_in_life": "Morning: Fix timing side-channel in Kyber implementation. Afternoon: Write unit tests for ML-DSA. Evening: Submit pull request to liboqs open source project.",
        "path": "CS degree → Open source contributions to PQC libraries → Full-time developer",
    },
    {
        "title": "🎓 Educator / Professor",
        "salary": "$70,000-$130,000/yr",
        "growth": "Medium",
        "color": "#06b6d4",
        "education": "PhD in Mathematics or CS",
        "companies": ["Universities", "Community colleges", "EdTech companies", "Corporate training"],
        "skills": ["Teaching", "Curriculum design", "Research", "Communication"],
        "pqc_role": "Teach the next generation of cryptographers! Design PQC curricula like QuantumVault Academy. Write textbooks on post-quantum methods.",
        "day_in_life": "Morning: Lecture on Module-LWE to graduate students. Afternoon: Research new PQC pedagogy methods. Evening: Review student implementations of Kyber.",
        "path": "PhD → Postdoc → Assistant Professor → Tenure → Full Professor",
    },
]


def render_career_explorer():
    st.title("🗺️ PQC Career Explorer")
    st.markdown(
        "🚀 **Post-quantum cryptography is creating thousands of new jobs.** "
        "Every company, government agency, and research lab needs PQC experts right now. "
        "Explore careers that use the skills you are learning in QuantumVault Academy!"
    )

    if "career_selected" not in st.session_state:
        st.session_state.career_selected = 0

    # Career grid
    st.markdown("### 🎯 Choose a Career Path")
    career_cols = st.columns(3)
    for i, career in enumerate(CAREERS):
        with career_cols[i % 3]:
            selected = i == st.session_state.career_selected
            c = career["color"]
            st.markdown(
                f"<div style='background:{'%s20' % c if selected else '#1e293b'};"
                f"border:{'2px solid ' + c if selected else '1px solid #334155'};"
                f"border-radius:12px;padding:14px;text-align:center;margin:4px 0;cursor:pointer'>"
                f"<div style='font-size:1.8rem;margin-bottom:4px'>{career['title'].split()[0]}</div>"
                f"<div style='font-weight:bold;color:{c};font-size:0.85rem'>{' '.join(career['title'].split()[1:])}</div>"
                f"<div style='font-size:0.75rem;color:#888;margin-top:4px'>{career['salary'].split('-')[0]}+</div>"
                f"<div style='font-size:0.7rem;color:{'#10b981' if career['growth']=='Explosive' else '#3b82f6'};margin-top:2px'>"
                f"📈 {career['growth']}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
            if st.button("Explore", key=f"career_{i}", use_container_width=True):
                st.session_state.career_selected = i
                st.rerun()

    st.markdown("---")

    career = CAREERS[st.session_state.career_selected]
    c = career["color"]

    st.markdown(
        f"<div style='background:{c}12;border:2px solid {c}50;"
        f"border-radius:16px;padding:20px;margin:8px 0'>"
        f"<h2 style='color:{c};margin:0 0 4px'>{career['title']}</h2>"
        f"<div style='display:flex;gap:12px;flex-wrap:wrap;margin:8px 0'>"
        f"<span style='background:{c}20;color:{c};padding:3px 10px;border-radius:100px;font-size:0.78rem;font-weight:bold'>💰 {career['salary']}</span>"
        f"<span style='background:#10b98120;color:#10b981;padding:3px 10px;border-radius:100px;font-size:0.78rem;font-weight:bold'>📈 {career['growth']} Growth</span>"
        f"<span style='background:#3b82f620;color:#3b82f6;padding:3px 10px;border-radius:100px;font-size:0.78rem'>🎓 {career['education']}</span>"
        f"</div>"
        f"<p style='color:#ccc;margin:8px 0;font-size:0.9rem;line-height:1.6'>{career['pqc_role']}</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🏢 Companies Hiring:**")
        for company in career["companies"]:
            st.markdown(f"• {company}")

        st.markdown("**🛠️ Key Skills Needed:**")
        for skill in career["skills"]:
            st.markdown(f"• {skill}")

    with col2:
        st.markdown("**📅 A Day in the Life:**")
        st.markdown(
            f"<div style='background:#1e293b;border-radius:10px;padding:12px;"
            f"font-size:0.85rem;color:#ccc;line-height:1.6'>{career['day_in_life']}</div>",
            unsafe_allow_html=True
        )
        st.markdown("**🗺️ Career Path:**")
        st.markdown(
            f"<div style='background:{c}10;border-left:3px solid {c};"
            f"padding:8px 12px;border-radius:0 8px 8px 0;font-size:0.82rem;color:#ccc'>"
            f"{career['path']}</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("### 🎯 Career Quiz — Is This Right for You?")
    questions = [
        ("Do you enjoy solving math puzzles?", ["Love it!", "It's OK", "Not really", "I hate math"]),
        ("What sounds more interesting to you?", ["Building software", "Breaking things (ethically)", "Research and theory", "Teaching others"]),
        ("How long are you willing to study?", ["4 years (BS)", "6 years (BS+MS)", "8+ years (PhD)", "Self-taught"]),
    ]
    if "career_q" not in st.session_state:
        st.session_state.career_q = 0
    if "career_answers" not in st.session_state:
        st.session_state.career_answers = []

    if st.session_state.career_q < len(questions):
        q, opts = questions[st.session_state.career_q]
        st.markdown(f"**Q{st.session_state.career_q+1}:** {q}")
        for opt in opts:
            if st.button(opt, key=f"cq_{st.session_state.career_q}_{opt}", use_container_width=True):
                st.session_state.career_answers.append(opt)
                st.session_state.career_q += 1
                st.rerun()
    else:
        st.success("🎉 You have explored PQC careers! +10 XP")
        if st.button("✅ Mark Explored! +10 XP", key="career_done"):
            st.session_state.xp = st.session_state.get("xp", 0) + 10
            st.session_state.badges = st.session_state.get("badges", []) + ["🗺️ Career Explorer"]
            st.session_state.career_q = 0
            st.session_state.career_answers = []
            st.rerun()
