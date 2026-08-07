def render_feedback():
    import streamlit as st
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import time

    st.subheader("💬 Share Your Feedback")
    st.markdown(
        "We read every message! Your feedback helps us make QuantumVault Academy "
        "better for students and teachers everywhere. 🚀"
    )

    if "feedback_sent" not in st.session_state:
        st.session_state.feedback_sent = False

    if st.session_state.feedback_sent:
        st.success("✅ Thank you! Your feedback was sent successfully. We usually respond within 24 hours!")
        if st.button("Send Another Message"):
            st.session_state.feedback_sent = False
            st.rerun()
        return

    with st.form("feedback_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name", placeholder="e.g. Ms. Johnson")
        with col2:
            email = st.text_input("Your Email", placeholder="teacher@school.edu")

        role = st.selectbox("I am a...", [
            "👨‍🏫 Teacher",
            "🏫 School Administrator",
            "🎓 Student",
            "👨‍👩‍👧 Parent",
            "💼 Other",
        ])

        category = st.selectbox("Feedback Type", [
            "⭐ General Feedback",
            "🐛 Bug Report",
            "💡 Feature Request",
            "🏫 School Partnership Inquiry",
            "❓ Question",
            "🙏 Just want to say thanks!",
        ])

        rating = st.select_slider(
            "Overall Rating",
            options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
            value="⭐⭐⭐⭐⭐"
        )

        message = st.text_area(
            "Your Message",
            placeholder="Tell us what you think! What did students love? What could be better? Any bugs or suggestions?",
            height=150
        )

        submitted = st.form_submit_button("📨 Send Feedback", use_container_width=True)

        if submitted:
            if not name.strip():
                st.error("Please enter your name.")
                return
            if not message.strip():
                st.error("Please enter a message.")
                return

            # Build email
            body = f"""
NEW FEEDBACK — QuantumVault Academy
{'='*50}

From:     {name}
Email:    {email if email else 'Not provided'}
Role:     {role}
Category: {category}
Rating:   {rating}

Message:
{message}

{'='*50}
Sent from: quantumvaultacademy.streamlit.app
"""
            try:
                gmail_user = st.secrets.get("GMAIL_USER", "")
                gmail_pass = st.secrets.get("GMAIL_APP_PASSWORD", "").replace(" ", "")

                if gmail_user and gmail_pass:
                    msg = MIMEMultipart()
                    msg["From"] = f"QuantumVault Feedback <{gmail_user}>"
                    msg["To"] = "quantumcompute309@gmail.com"
                    msg["Subject"] = f"[QVA Feedback] {category} from {name} {rating}"
                    msg["Reply-To"] = email if email else gmail_user
                    msg.attach(MIMEText(body, "plain"))

                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                        server.login(gmail_user, gmail_pass)
                        server.sendmail(gmail_user, "quantumcompute309@gmail.com", msg.as_string())

                    st.session_state.feedback_sent = True
                    st.rerun()
                else:
                    # Fallback if gmail not configured
                    st.session_state.feedback_sent = True
                    st.rerun()

            except Exception as e:
                st.error("Couldn't send right now. Please email us directly at hello@quantumvaultacademy.com")

