
import streamlit as st
import random
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mfa_code(email: str, code: str) -> bool:
    """Send MFA code via Gmail SMTP."""
    try:
        gmail_user = st.secrets.get("GMAIL_USER", "")
        gmail_pass = st.secrets.get("GMAIL_APP_PASSWORD", "").replace(" ", "")
        if not gmail_user or not gmail_pass:
            return False

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"QuantumVault Academy — Your Login Code: {code}"
        msg["From"] = f"QuantumVault Academy <{gmail_user}>"
        msg["To"] = email

        html = f"""
        <div style="font-family:Arial,sans-serif;max-width:480px;margin:0 auto;
            background:#020d14;color:white;border-radius:12px;overflow:hidden;">
            <div style="background:#1d4ed8;padding:20px;text-align:center;">
                <h2 style="margin:0;color:white">🔐 QuantumVault Academy</h2>
                <p style="margin:4px 0 0;color:#93c5fd;font-size:13px">Quantum-Safe Login Verification</p>
            </div>
            <div style="padding:24px;text-align:center;">
                <p style="color:#94a3b8;font-size:13px;margin-bottom:16px">
                    Your one-time verification code is:
                </p>
                <div style="background:#071520;border:2px solid #3b82f6;border-radius:12px;
                    padding:20px;letter-spacing:12px;font-size:2.5rem;font-weight:900;
                    color:#60a5fa;font-family:monospace;margin:16px 0;">
                    {code}
                </div>
                <p style="color:#64748b;font-size:11px;margin-top:16px;">
                    This code expires in <b style="color:#f59e0b">5 minutes</b>.<br>
                    Never share this code with anyone.<br>
                    If you didn't request this, ignore this email.
                </p>
            </div>
            <div style="background:#071520;padding:12px;text-align:center;
                font-size:10px;color:#334155;">
                QuantumVault Academy LLC · Las Vegas, NV · hello@quantumvaultacademy.com
            </div>
        </div>
        """

        text = f"Your QuantumVault Academy login code is: {code}\nExpires in 5 minutes."
        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, email, msg.as_string())
        return True
    except Exception as e:
        import logging
        logging.error(f"MFA email failed: {e}")
        return False

def generate_code() -> str:
    """Generate a 6-digit MFA code."""
    return str(random.randint(100000, 999999))

def render_mfa_login():
    """Render the email MFA login screen."""
    # Initialize session state
    if "mfa_step" not in st.session_state:
        st.session_state.mfa_step = "email"
    if "mfa_code" not in st.session_state:
        st.session_state.mfa_code = None
    if "mfa_code_time" not in st.session_state:
        st.session_state.mfa_code_time = None
    if "mfa_email" not in st.session_state:
        st.session_state.mfa_email = None
    if "mfa_attempts" not in st.session_state:
        st.session_state.mfa_attempts = 0
    if "mfa_verified" not in st.session_state:
        st.session_state.mfa_verified = False

    # Already verified
    if st.session_state.mfa_verified:
        return True

    # Centered login card
    st.markdown("""
        <div style='text-align:center;padding:40px 20px 20px'>
            <div style='font-size:3rem;margin-bottom:10px'>🔐</div>
            <h1 style='color:#60a5fa;margin-bottom:6px;font-size:1.6rem'>QuantumVault Academy</h1>
            <p style='color:#64748b;font-size:12px;margin-bottom:0'>
                Quantum-Safe Learning Platform<br>
                Protected with Multi-Factor Authentication
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.session_state.mfa_step == "email":
            st.markdown("##### 📧 Enter your email to sign in")
            email = st.text_input("Email address", placeholder="you@school.edu",
                                  key="mfa_email_input", label_visibility="collapsed")
            if st.button("📨 Send Verification Code", type="primary",
                        use_container_width=True, key="mfa_send"):
                if not email or "@" not in email or "." not in email:
                    st.error("Please enter a valid email address.")
                else:
                    code = generate_code()
                    sent = send_mfa_code(email, code)
                    if sent:
                        st.session_state.mfa_code = code
                        st.session_state.mfa_code_time = time.time()
                        st.session_state.mfa_email = email
                        st.session_state.mfa_step = "code"
                        st.session_state.mfa_attempts = 0
                        st.rerun()
                    else:
                        st.error("Could not send email. Please try again or contact hello@quantumvaultacademy.com")

            st.markdown("---")
            st.markdown(
                "<div style='text-align:center;font-size:10px;color:#334155'>"
                "🔐 Protected by post-quantum MFA · COPPA & FERPA compliant<br>"
                "No password needed — just your email!"
                "</div>", unsafe_allow_html=True
            )

        elif st.session_state.mfa_step == "code":
            # Check expiry
            elapsed = time.time() - (st.session_state.mfa_code_time or 0)
            remaining = max(0, int(300 - elapsed))

            if remaining == 0:
                st.warning("⏰ Code expired! Please request a new one.")
                if st.button("🔄 Request New Code", use_container_width=True):
                    st.session_state.mfa_step = "email"
                    st.session_state.mfa_code = None
                    st.rerun()
                return False

            st.markdown(f"##### 📱 Check your email")
            st.info(
            st.info("Code sent to " + str(st.session_state.mfa_email) + " — expires in " + str(remaining//60) + ":" + str(remaining%60).zfill(2))

            # Rate limiting
            if st.session_state.mfa_attempts >= 5:
                st.error("Too many attempts. Please request a new code.")
                if st.button("🔄 Request New Code", use_container_width=True):
                    st.session_state.mfa_step = "email"
                    st.session_state.mfa_code = None
                    st.rerun()
                return False

            code_input = st.text_input(
                "Enter 6-digit code",
                placeholder="000000",
                max_chars=6,
                key="mfa_code_input",
                label_visibility="collapsed"
            )

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ Verify Code", type="primary", use_container_width=True):
                    st.session_state.mfa_attempts += 1
                    if code_input.strip() == st.session_state.mfa_code:
                        st.session_state.mfa_verified = True
                        st.session_state.mfa_step = "done"
                        st.session_state.user_email = st.session_state.mfa_email
                        st.success("✅ Verified! Welcome to QuantumVault Academy!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        left = 5 - st.session_state.mfa_attempts
                        st.error(f"❌ Wrong code. {left} attempts remaining.")
            with col_b:
                if st.button("↩️ Back", use_container_width=True):
                    st.session_state.mfa_step = "email"
                    st.session_state.mfa_code = None
                    st.rerun()

            st.markdown("---")
            st.markdown(
                "<div style='text-align:center;font-size:10px;color:#334155'>"
                "Didn't get the email? Check your spam folder.<br>"
                "Still need help? Email hello@quantumvaultacademy.com"
                "</div>", unsafe_allow_html=True
            )

    return st.session_state.mfa_verified
