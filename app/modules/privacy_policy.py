import streamlit as st
import datetime

TODAY = datetime.date.today().strftime("%B %d, %Y")

def render_privacy_policy():
    st.title("🔒 Privacy Policy")
    st.caption(f"Last updated: {TODAY}")
    st.info("QuantumVault Academy collects minimal data, never sells it, and complies with COPPA and FERPA.")

    with st.expander("1. Who We Are"):
        st.markdown(
            "**QuantumVault Academy** teaches post-quantum cryptography to K-12 students.\n\n"
            "**Contact:** hello@quantumvaultacademy.com\n\n"
            "**Privacy:** privacy@quantumvaultacademy.com"
        )
    with st.expander("2. What We Collect"):
        st.markdown(
            "**From Teachers:** Name, email, school name, payment info (via Stripe — we never see card numbers).\n\n"
            "**From Students:** Username, XP points, badges, quiz scores, modules completed.\n\n"
            "**We do NOT collect:** Student email addresses, physical addresses, photos, or biometric data."
        )
    with st.expander("3. How We Use It"):
        st.markdown(
            "- Provide the educational service\n"
            "- Track student progress and award achievements\n"
            "- Send teacher weekly reports (opt-in only)\n"
            "- Respond to support requests\n\n"
            "**We never sell data or use it for advertising.**"
        )
    with st.expander("4. COPPA — Children Under 13"):
        st.markdown(
            "Schools act as the authorized agent for parental consent under the school official exception.\n\n"
            "**Parent rights:**\n"
            "- Review your child's data\n"
            "- Request corrections\n"
            "- Request deletion\n\n"
            "Email privacy@quantumvaultacademy.com — we respond within 30 days."
        )
    with st.expander("5. FERPA Compliance"):
        st.markdown(
            "- We operate as a School Official with legitimate educational interest\n"
            "- Student records used for educational purposes only\n"
            "- Schools retain full control of student data\n"
            "- Data returned or deleted within 60 days of contract termination"
        )
    with st.expander("6. Third Party Services"):
        st.markdown(
            "| Provider | Purpose | Data Shared |\n"
            "|---|---|---|\n"
            "| Stripe | Payment processing | Billing info only |\n"
            "| Anthropic | AI Tutor | Student questions (anonymized) |\n"
            "| Formspree | Feedback forms | Teacher email + text |\n"
            "| Streamlit Cloud | App hosting | All app data (SOC 2) |\n\n"
            "**We never sell student data. Ever.**"
        )
    with st.expander("7. Security"):
        st.markdown(
            "- HTTPS/TLS 1.3 encryption for all data in transit\n"
            "- Streamlit Cloud SOC 2 Type II compliant hosting\n"
            "- Stripe PCI DSS compliant payment processing\n"
            "- Bandit security score: 0 HIGH / 0 MEDIUM / 0 LOW\n"
            "- Rate limiting on all authentication endpoints\n"
            "- Input sanitization on all user-facing fields"
        )
    with st.expander("8. Your Rights"):
        st.markdown(
            "You have the right to:\n"
            "- **Access** your data at any time\n"
            "- **Correct** inaccurate information\n"
            "- **Delete** your data (honored within 30 days)\n"
            "- **Export** your data in a readable format\n\n"
            "Email privacy@quantumvaultacademy.com to exercise any right."
        )
    with st.expander("9. Data Retention"):
        st.markdown(
            "- Student progress data: deleted within 60 days of account closure\n"
            "- Teacher accounts: retained while subscription is active\n"
            "- Payment records: 7 years (required by tax law, stored by Stripe)\n"
            "- Deletion requests honored within 30 days"
        )
    with st.expander("10. Policy Changes"):
        st.markdown(
            "We post updates with a new effective date. "
            "For material changes we notify administrators by email. "
            "Continued use after 30 days constitutes acceptance."
        )
    st.markdown("---")
    st.info(f"Questions? Email privacy@quantumvaultacademy.com | Last updated {TODAY}")


def render_terms_of_service():
    st.title("📋 Terms of Service")
    st.caption(f"Last updated: {TODAY}")
    st.info("By using QuantumVault Academy you agree to these terms. We own the content. You own your student data. 30-day money-back guarantee.")

    with st.expander("1. Acceptance"):
        st.markdown(
            "By accessing QuantumVault Academy you agree to be bound by these terms. "
            "If using on behalf of a school, you represent that you have authority to bind that organization."
        )
    with st.expander("2. Permitted Use"):
        st.markdown(
            "**You may:**\n"
            "- Use the platform for classroom instruction\n"
            "- Download achievement certificates for students\n"
            "- Share the app URL with students and parents\n\n"
            "**You may not:**\n"
            "- Resell or sublicense the platform\n"
            "- Reverse engineer the software\n"
            "- Share login credentials with unauthorized users\n"
            "- Use automated bots or scrapers"
        )
    with st.expander("3. Payment and Refunds"):
        st.markdown(
            "- Subscriptions billed annually in USD via Stripe\n"
            "- **30-day money-back guarantee** for new subscribers\n"
            "- No refunds after 30 days except at our discretion\n"
            "- Cancel anytime — access continues until end of billing period\n"
            "- Data exported or deleted within 60 days of cancellation"
        )
    with st.expander("4. Acceptable Use"):
        st.markdown(
            "Do NOT use QuantumVault Academy to:\n"
            "- Harass, bully, or harm other users\n"
            "- Post inappropriate or illegal content\n"
            "- Attempt to hack or exploit the service\n"
            "- Impersonate other users or staff\n"
            "- Violate any applicable laws\n\n"
            "AI Tutor misuse will result in immediate account suspension."
        )
    with st.expander("5. Intellectual Property"):
        st.markdown(
            "**QuantumVault Academy owns:** All curriculum, games, educational materials, software, and branding.\n\n"
            "**You own:** Student journal entries, written work, and your school's data.\n\n"
            "NIST PQC standards (FIPS 203-206) are US government public domain publications."
        )
    with st.expander("6. Disclaimers"):
        st.markdown(
            "- Cryptographic demos are **teaching tools only** — not for production use\n"
            "- We aim for 99.9% uptime but do not guarantee uninterrupted access\n"
            "- Our total liability is limited to amounts paid in the prior 12 months"
        )
    with st.expander("7. Governing Law"):
        st.markdown(
            "These terms are governed by the laws of the **State of California**, United States. "
            "Any disputes shall be resolved in the courts of California."
        )
    with st.expander("8. Contact"):
        st.markdown(
            "**QuantumVault Academy LLC**\n\n"
            "- General: hello@quantumvaultacademy.com\n"
            "- Legal: legal@quantumvaultacademy.com"
        )
    st.markdown("---")
    st.info(f"Questions? Email hello@quantumvaultacademy.com | Last updated {TODAY}")
