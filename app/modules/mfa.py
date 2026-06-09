import streamlit as st
import random
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mfa_code(email: str, code: str) -> bool:
    try:
        gmail_user = st.secrets.get("GMAIL_USER", "")
        gmail_pass = st.secrets.get("GMAIL_APP_PASSWORD", "").replace(" ", "")
        if not gmail_user or not gmail_pass:
            return False

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "QuantumVault Academy — Login Code: " + code
        msg["From"] = "QuantumVault Academy <" + gmail_user + ">"
        msg["To"] = email

        text_body = "Your QuantumVault Academy login code is: " + code + "\nExpires in 5 minutes."

        html_body = """
<div style="font-family:Arial,sans-serif;max-width:480px;margin:0 auto;
    background:#020d14;color:white;border-radius:12px;overflow:hidden;">
    <div style="background:#1d4ed8;padding:20px;text-align:center;">
        <h2 style="margin:0;color:white">QuantumVault Academy</h2>
        <p style="margin:4px 0 0;color:#93c5fd;font-size:13px">Login Verification Code</p>
    </div>
    <div style="padding:24px;text-align:center;">
        <p style="color:#94a3b8;font-size:13px;">Your one-time code:</p>
        <div style="background:#071520;border:2px solid #3b82f6;border-radius:12px;
            padding:20px;letter-spacing:12px;font-size:2.5rem;font-weight:900;
            color:#60a5fa;font-family:monospace;margin:16px 0;">""" + code + """</div>
        <p style="color:#64748b;font-size:11px;">
            Expires in 5 minutes. Never share this code.
        </p>
    </div>
    <div style="background:#071520;padding:12px;text-align:center;
        font-size:10px;color:#334155;">
        QuantumVault Academy LLC · hello@quantumvaultacademy.com
    </div>
</div>"""

        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, email, msg.as_string())
        return True
    except Exception as e:
        import logging
        logging.error("MFA email failed: " + str(e))
        return False


def generate_code() -> str:
    return str(random.randint(100000, 999999))


def render_mfa_login():
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

    if st.session_state.mfa_verified:
        return True

    st.markdown(
        "<div style='text-align:center;padding:40px 20px 20px'>"
        "<div style='font-size:3rem;margin-bottom:10px'>🔐</div>"
        "<h1 style='color:#60a5fa;margin-bottom:6px;font-size:1.6rem'>QuantumVault Academy</h1>"
        "<p style='color:#64748b;font-size:12px;margin-bottom:0'>"
        "Protected with Multi-Factor Authentication</p>"
        "</div>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.mfa_step == "email":
            st.markdown("##### Enter your email to sign in")
            email = st.text_input(
                "Email address",
                placeholder="you@school.edu",
                key="mfa_email_input",
                label_visibility="collapsed"
            )
            if st.button("Send Verification Code", type="primary",
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
                        st.error("Could not send email. Contact hello@quantumvaultacademy.com")

            st.markdown("---")
            st.markdown(
                "<div style='text-align:center;font-size:10px;color:#334155'>"
                "No password needed — just your email!</div>",
                unsafe_allow_html=True
            )

        elif st.session_state.mfa_step == "code":
            elapsed = time.time() - (st.session_state.mfa_code_time or 0)
            remaining = max(0, int(300 - elapsed))

            if remaining == 0:
                st.warning("Code expired! Please request a new one.")
                if st.button("Request New Code", use_container_width=True):
                    st.session_state.mfa_step = "email"
                    st.session_state.mfa_code = None
                    st.rerun()
                return False

            mins = remaining // 60
            secs = remaining % 60
            email_addr = str(st.session_state.mfa_email)
            time_str = str(mins) + ":" + str(secs).zfill(2)
            st.info("Code sent to " + email_addr + " — expires in " + time_str)

            if st.session_state.mfa_attempts >= 5:
                st.error("Too many attempts. Please request a new code.")
                if st.button("Request New Code", use_container_width=True):
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
                if st.button("Verify Code", type="primary", use_container_width=True):
                    st.session_state.mfa_attempts += 1
                    if code_input.strip() == st.session_state.mfa_code:
                        st.session_state.mfa_verified = True
                        st.session_state.mfa_step = "done"
                        st.session_state.user_email = st.session_state.mfa_email
                        st.success("Verified! Welcome to QuantumVault Academy!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        left = 5 - st.session_state.mfa_attempts
                        st.error("Wrong code. " + str(left) + " attempts remaining.")
            with col_b:
                if st.button("Back", use_container_width=True):
                    st.session_state.mfa_step = "email"
                    st.session_state.mfa_code = None
                    st.rerun()

            st.markdown(
                "<div style='text-align:center;font-size:10px;color:#334155'>"
                "Check spam folder if you don't see the email.</div>",
                unsafe_allow_html=True
            )

    return st.session_state.mfa_verified
