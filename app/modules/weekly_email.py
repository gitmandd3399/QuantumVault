"""
modules/weekly_email.py
────────────────────────
Weekly progress email system.
Parents sign up to receive Friday progress reports.
Uses Formspree for email delivery.
"""

import streamlit as st
import datetime
import json
import requests


def get_week_summary() -> dict:
    """Build a summary of the student's week."""
    xp = st.session_state.get("xp", 0)
    badges = st.session_state.get("badges", [])
    streak = st.session_state.get("streak_days", 1)
    completed = st.session_state.get("completed_activities", set())
    journal = st.session_state.get("journal_entries", [])
    level = st.session_state.get("level", "Elementary")

    from utils.security import get_level
    rank = get_level(xp)

    return {
        "xp": xp,
        "rank": rank,
        "badges": badges,
        "streak": streak,
        "activities_completed": len(completed),
        "journal_entries": len(journal),
        "current_module": str(level),
    }


def build_email_html(student_name: str, summary: dict) -> str:
    today = datetime.date.today().strftime("%B %d, %Y")
    badge_list = (
        "".join([f"<li>{b}</li>" for b in summary["badges"][-5:]])
        if summary["badges"]
        else "<li>Keep learning to earn badges!</li>"
    )

    return f"""
<!DOCTYPE html>
<html>
<body style="font-family:sans-serif;background:#f8f7ff;margin:0;padding:20px;">
<div style="max-width:600px;margin:0 auto;background:white;border-radius:16px;
    overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.1);">

    <!-- Header -->
    <div style="background:linear-gradient(135deg,#4F46E5,#7C6DFA);
        padding:32px;text-align:center;">
        <div style="font-size:2.5rem;">🔐</div>
        <h1 style="color:white;margin:8px 0;font-size:1.5rem;">
            QuantumVault Academy
        </h1>
        <p style="color:rgba(255,255,255,0.8);margin:0;font-size:0.9rem;">
            Weekly Progress Report — {today}
        </p>
    </div>

    <!-- Greeting -->
    <div style="padding:24px 32px;">
        <h2 style="color:#1e1b4b;margin:0 0 8px;">
            Great week, {student_name}! 🎉
        </h2>
        <p style="color:#6b7280;font-size:0.9rem;line-height:1.6;">
            Here is a summary of your post-quantum cryptography learning this week.
            Keep up the amazing work!
        </p>
    </div>

    <!-- Stats -->
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1px;
        background:#e5e7eb;margin:0 32px;">
        <div style="background:white;padding:20px;text-align:center;">
            <div style="font-size:2rem;font-weight:bold;color:#4F46E5;">
                {summary["xp"]}
            </div>
            <div style="font-size:0.75rem;color:#6b7280;text-transform:uppercase;
                letter-spacing:1px;">Total XP</div>
        </div>
        <div style="background:white;padding:20px;text-align:center;">
            <div style="font-size:2rem;font-weight:bold;color:#10b981;">
                {summary["streak"]}
            </div>
            <div style="font-size:0.75rem;color:#6b7280;text-transform:uppercase;
                letter-spacing:1px;">Day Streak 🔥</div>
        </div>
        <div style="background:white;padding:20px;text-align:center;">
            <div style="font-size:2rem;font-weight:bold;color:#f59e0b;">
                {summary["activities_completed"]}
            </div>
            <div style="font-size:0.75rem;color:#6b7280;text-transform:uppercase;
                letter-spacing:1px;">Activities Done</div>
        </div>
    </div>

    <!-- Rank -->
    <div style="padding:20px 32px;">
        <div style="background:#eef2ff;border-radius:10px;padding:16px;
            display:flex;align-items:center;gap:12px;">
            <div style="font-size:2rem;">🏅</div>
            <div>
                <div style="font-weight:bold;color:#4F46E5;">
                    Current Rank: {summary["rank"]}
                </div>
                <div style="font-size:0.85rem;color:#6b7280;">
                    Keep earning XP to reach the next rank!
                </div>
            </div>
        </div>
    </div>

    <!-- Badges -->
    <div style="padding:0 32px 20px;">
        <h3 style="color:#1e1b4b;margin:0 0 12px;">🏆 Badges Earned</h3>
        <ul style="color:#374151;font-size:0.9rem;line-height:1.8;
            padding-left:20px;">
            {badge_list}
        </ul>
    </div>

    <!-- What they learned -->
    <div style="background:#f0fdf4;margin:0 32px;border-radius:10px;
        padding:16px;margin-bottom:20px;">
        <h3 style="color:#065f46;margin:0 0 8px;">📚 What They Are Learning</h3>
        <p style="color:#374151;font-size:0.85rem;line-height:1.6;margin:0;">
            {student_name} is studying <strong>post-quantum cryptography</strong> —
            the math that will protect the internet from quantum computers.
            They are learning about NIST-approved algorithms including
            <strong>Kyber (ML-KEM)</strong>, <strong>Dilithium (ML-DSA)</strong>,
            <strong>SPHINCS+ (SLH-DSA)</strong>, and <strong>Falcon (FN-DSA)</strong>.
            These are the actual standards the US government adopted in 2024!
        </p>
    </div>

    <!-- Journal entries -->
    {f'''
    <div style="padding:0 32px 20px;">
        <div style="background:#fff7ed;border-radius:10px;padding:16px;">
            <h3 style="color:#92400e;margin:0 0 8px;">✍️ Research Journal</h3>
            <p style="color:#374151;font-size:0.85rem;margin:0;">
                {student_name} wrote <strong>{summary["journal_entries"]} journal entries</strong>
                this week reflecting on their learning. This develops critical thinking
                and deepens understanding of complex concepts.
            </p>
        </div>
    </div>
    ''' if summary["journal_entries"] > 0 else ""}

    <!-- Footer -->
    <div style="background:#1e1b4b;padding:24px 32px;text-align:center;">
        <p style="color:rgba(255,255,255,0.7);font-size:0.8rem;margin:0 0 8px;">
            QuantumVault Academy — The First K-12 Post-Quantum Cryptography Platform
        </p>
        <p style="color:rgba(255,255,255,0.5);font-size:0.75rem;margin:0;">
            NIST FIPS 203 · 204 · 205 · 206 · COPPA Compliant · NSA GenCyber Eligible
        </p>
    </div>
</div>
</body>
</html>
"""


def send_email_via_formspree(
    parent_email: str,
    student_name: str,
    html_content: str
) -> bool:
    """Send email via Formspree."""
    try:
        response = requests.post(
            "https://formspree.io/f/mredvlgp",
            data={
                "email": parent_email,
                "subject": f"QuantumVault Academy — Weekly Progress for {student_name}",
                "message": html_content,
                "_replyto": "hello@quantumvaultacademy.com",
            },
            headers={"Accept": "application/json"},
            timeout=10
        )
        return response.status_code == 200
    except Exception:
        return False


def render_weekly_email():
    st.title("📧 Weekly Progress Reports")
    st.markdown(
        "Sign up to receive weekly progress emails every Friday! "
        "Parents and teachers get a full summary of learning activity."
    )

    summary = get_week_summary()

    # ── Preview section ───────────────────────────────────────────────────
    tab1, tab2 = st.tabs(["📬 Sign Up", "👀 Preview Email"])

    with tab1:
        st.markdown("### 📬 Subscribe to Weekly Reports")
        st.markdown(
            "Enter your parent or guardian's email below. "
            "They will receive a progress report every Friday evening."
        )

        col1, col2 = st.columns(2)
        with col1:
            student_name = st.text_input(
                "Student name:",
                placeholder="Alex Smith",
                key="weekly_student_name"
            )
        with col2:
            parent_email = st.text_input(
                "Parent/Guardian email:",
                placeholder="parent@email.com",
                key="weekly_parent_email"
            )

        frequency = st.selectbox(
            "Report frequency:",
            ["Weekly (every Friday)", "Bi-weekly", "Monthly"],
            key="weekly_frequency"
        )

        st.markdown("**What the report includes:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("✅ Total XP earned")
            st.markdown("✅ Current rank and badges")
            st.markdown("✅ Day learning streak")
        with col2:
            st.markdown("✅ Activities completed")
            st.markdown("✅ What concepts were studied")
            st.markdown("✅ Journal entry count")

        st.markdown("---")

        if st.button("📧 Send Progress Report Now!", key="send_weekly", type="primary"):
            if not student_name:
                st.error("Please enter the student's name!")
            elif not parent_email or "@" not in parent_email:
                st.error("Please enter a valid email address!")
            else:
                with st.spinner("Generating and sending progress report..."):
                    html = build_email_html(student_name, summary)
                    success = send_email_via_formspree(
                        parent_email, student_name, html
                    )

                if success:
                    st.success(
                        f"✅ Progress report sent to {parent_email}! "
                        f"Check your inbox in a few minutes."
                    )
                    st.session_state.xp = st.session_state.get("xp", 0) + 5
                    st.toast("+5 XP for sharing your progress!")
                else:
                    st.warning(
                        "Email service unavailable right now. "
                        "Try again later or use the preview tab to copy the report."
                    )

        st.markdown("---")
        st.markdown("### 📊 Your Current Stats")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("⭐ XP", summary["xp"])
        with col2:
            st.metric("🏅 Rank", summary["rank"])
        with col3:
            st.metric("🔥 Streak", f"{summary['streak']} days")
        with col4:
            st.metric("✅ Activities", summary["activities_completed"])

    with tab2:
        st.markdown("### 👀 Email Preview")
        st.caption("This is what the weekly progress report looks like!")

        preview_name = st.text_input(
            "Preview with name:",
            value="Alex",
            key="preview_name"
        )

        html_preview = build_email_html(preview_name, summary)

        st.components.v1.html(html_preview, height=700, scrolling=True)

        st.download_button(
            label="📥 Download Email HTML",
            data=html_preview,
            file_name="QuantumVault_Progress_Report.html",
            mime="text/html",
            key="dl_email_html"
        )
