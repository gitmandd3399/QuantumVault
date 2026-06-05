import streamlit as st
import datetime

TODAY = datetime.date.today().strftime("%B %d, %Y")

def render_privacy_policy():
    st.title("🔒 Privacy Policy")
    st.caption(f"Last updated: {TODAY}")
    st.info("QuantumVault Academy collects minimal data, never sells it, and complies with COPPA and FERPA.")
    with st.expander("1. Who We Are"):
        st.markdown("**QuantumVault Academy** teaches post-quantum cryptography to K-12 students. Contact: hello@quantumvaultacademy.com | Privacy: privacy@quantumvaultacademy.com")
    with st.expander("2. What We Collect"):
        st.markdown("**Teachers:** Name, email, school, payment info (via Stripe).\n\n**Students:** Username, XP, badges, quiz scores.\n\n**We do NOT collect:** Student emails, addresses, photos, or biometric data.")
    with st.expander("3. How We Use It"):
        st.markdown("- Provide the educational service\n- Track student progress\n- Send teacher reports (opt-in only)\n- **We never sell data or use it for advertising**")
    with st.expander("4. COPPA — Children Under 13"):
        st.markdown("Schools act as authorized agent for parental consent. Parents may request to review, correct, or delete their child data by emailing privacy@quantumvaultacademy.com. We respond within 30 days.")
    with st.expander("5. FERPA Compliance"):
        st.markdown("We operate as a School Official. Student records used for educational purposes only. Schools retain control of student data. Data deleted within 60 days of contract termination.")
    with st.expander("6. Third Parties"):
        st.markdown("Stripe (payments), Anthropic (AI Tutor), Formspree (feedback), Streamlit Cloud (hosting). **We never sell student data.**")
    with st.expander("7. Security"):
        st.markdown("HTTPS/TLS 1.3 encryption. SOC 2 hosting. PCI DSS payments. Bandit score: 0 HIGH / 0 MEDIUM. Rate limiting and input sanitization on all endpoints.")
    with st.expander("8. Your Rights"):
        st.markdown("Access, correct, delete, or export your data anytime. Email privacy@quantumvaultacademy.com — we respond within 30 days.")
    with st.expander("9. Data Retention"):
        st.markdown("Student data deleted within 60 days of account closure. Payment records kept 7 years (tax law). Deletion requests honored within 30 days.")
    with st.expander("10. Policy Changes"):
        st.markdown("We post updates with a new date and notify administrators by email for material changes.")
    st.markdown("---")
    st.info(f"Questions? Email privacy@quantumvaultacademy.com | Last updated {TODAY}")


def render_terms_of_service():
    st.title("📋 Terms of Service")
    st.caption(f"Last updated: {TODAY}")
    st.info("By using QuantumVault Academy you agree to these terms. We own the content. You own your student data. 30-day money-back guarantee.")
    with st.expander("1. Acceptance"):
        st.markdown("By accessing QuantumVault Academy you agree to these terms. Schools represent they have authority to bind their organization.")
    with st.expander("2. Permitted Use"):
        st.markdown("**You may:** Use for classroom instruction, download certificates, share the app URL.\n\n**You may not:** Resell, reverse engineer, share credentials, or use bots.")
    with st.expander("3. Payment and Refunds"):
        st.markdown("Billed annually via Stripe. **30-day money-back guarantee.** Cancel anytime — access until end of billing period. Data deleted within 60 days of cancellation.")
    with st.expander("4. Acceptable Use"):
        st.markdown("Do not harass users, post illegal content, hack the service, or impersonate others. AI Tutor misuse results in account suspension.")
    with st.expander("5. Intellectual Property"):
        st.markdown("QuantumVault Academy owns all curriculum, games, and software. You own student journal entries and your school data. NIST FIPS 203-206 are public domain.")
    with st.expander("6. Disclaimers"):
        st.markdown("Crypto demos are teaching tools only — not for production use. We aim for 99.9% uptime. Liability limited to amounts paid in prior 12 months.")
    with st.expander("7. Governing Law"):
        st.markdown("Governed by the laws of the State of California, United States.")
    with st.expander("8. Contact"):
        st.markdown("General: hello@quantumvaultacademy.com | Legal: legal@quantumvaultacademy.com")
    st.markdown("---")
    st.info(f"Questions? Email hello@quantumvaultacademy.com | Last updated {TODAY}")
