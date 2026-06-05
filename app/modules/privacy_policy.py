import streamlit as st
import datetime

TODAY = datetime.date.today().strftime("%B %d, %Y")

def render_privacy_policy():
    st.title("🔒 Privacy Policy")
    st.caption(f"Last updated: {TODAY}")

    st.markdown("""
## Summary
QuantumVault Academy collects minimal data, never sells it, and complies with COPPA and FERPA.

---

## 1. Who We Are
**QuantumVault Academy** teaches post-quantum cryptography to K-12 students.

- **General:** hello@quantumvaultacademy.com
- **Privacy:** privacy@quantumvaultacademy.com

---

## 2. What We Collect

**From Teachers:**
- Name, email, and school name
- Payment info — processed by Stripe, we never see card numbers

**From Students:**
- Username or display name (real names not required)
- XP points, badges, quiz scores, modules completed

**We do NOT collect:**
- Student email addresses
- Physical addresses
- Photos or biometric data
- Social Security Numbers

---

## 3. How We Use It
- Provide the educational service
- Track student progress and award achievements
- Send teacher weekly reports (opt-in only)
- Respond to support requests

**We never sell data or use it for advertising.**

---

## 4. COPPA — Children Under 13
Schools act as the authorized agent for parental consent.

**Parent rights:**
- Review your child's data
- Request corrections or deletion
- Opt out of future collection

Email privacy@quantumvaultacademy.com — we respond within 30 days.

---

## 5. FERPA Compliance
- We operate as a School Official with legitimate educational interest
- Student records used for educational purposes only
- Schools retain full control of student data at all times
- Data deleted within 60 days of contract termination

---

## 6. Third Party Services

| Provider | Purpose | Data Shared |
|---|---|---|
| Stripe | Payment processing | Billing info only |
| Anthropic | AI Tutor | Student questions (anonymized) |
| Formspree | Feedback forms | Teacher email and feedback text |
| Streamlit Cloud | App hosting | All app data (SOC 2 compliant) |

**We never sell student data. Ever.**

---

## 7. Security
- HTTPS/TLS 1.3 encryption for all data in transit
- Streamlit Cloud SOC 2 Type II compliant hosting
- Stripe PCI DSS compliant payment processing
- Bandit security score: 0 HIGH / 0 MEDIUM / 0 LOW
- Rate limiting on all authentication endpoints
- Input sanitization on all user-facing fields

---

## 8. Your Rights
- **Access** your data at any time
- **Correct** inaccurate information
- **Delete** your data — honored within 30 days
- **Export** your data in a readable format

Email privacy@quantumvaultacademy.com to exercise any right.

---

## 9. Data Retention
- Student progress data: deleted within 60 days of account closure
- Teacher accounts: retained while subscription is active
- Payment records: 7 years required by tax law (stored by Stripe)
- Deletion requests honored within 30 days

---

## 10. Policy Changes
We post updates with a new effective date. For material changes we notify administrators by email.
Continued use after 30 days constitutes acceptance.
    """)

    st.success(f"Questions? Email privacy@quantumvaultacademy.com | Last updated {TODAY}")


def render_terms_of_service():
    st.title("📋 Terms of Service")
    st.caption(f"Last updated: {TODAY}")

    st.markdown("""
## Summary
By using QuantumVault Academy you agree to these terms.
We own the content. You own your student data. 30-day money-back guarantee.

---

## 1. Acceptance
By accessing QuantumVault Academy you agree to be bound by these terms.
If using on behalf of a school, you represent that you have authority to bind that organization.

---

## 2. Permitted Use

**You may:**
- Use the platform for classroom instruction
- Download achievement certificates for students
- Share the app URL with students and parents

**You may not:**
- Resell or sublicense the platform
- Reverse engineer the software
- Share login credentials with unauthorized users
- Use automated bots or scrapers

---

## 3. Payment and Refunds
- Subscriptions billed annually in USD via Stripe
- **30-day money-back guarantee** for new subscribers
- No refunds after 30 days except at our discretion
- Cancel anytime — access continues until end of billing period
- Data exported or deleted within 60 days of cancellation

---

## 4. Acceptable Use

Do NOT use QuantumVault Academy to:
- Harass, bully, or harm other users
- Post inappropriate or illegal content
- Attempt to hack or exploit the service
- Impersonate other users or staff
- Violate any applicable laws

AI Tutor misuse will result in immediate account suspension.

---

## 5. Intellectual Property

**QuantumVault Academy owns:** All curriculum, games, educational materials, software, and branding.

**You own:** Student journal entries, written work, and your school data.

NIST PQC standards (FIPS 203-206) are US government public domain publications.

---

## 6. Disclaimers
- Cryptographic demos are teaching tools only — not for production use
- We aim for 99.9% uptime but do not guarantee uninterrupted access
- Our total liability is limited to amounts paid in the prior 12 months

---

## 7. Governing Law
These terms are governed by the laws of the **State of California**, United States.
Disputes shall be resolved in the courts of California.

---

## 8. Contact

**QuantumVault Academy LLC**
- General: hello@quantumvaultacademy.com
- Legal: legal@quantumvaultacademy.com
    """)

    st.success(f"Questions? Email hello@quantumvaultacademy.com | Last updated {TODAY}")
