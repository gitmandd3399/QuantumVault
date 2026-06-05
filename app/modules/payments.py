"""
modules/payments.py
───────────────────
Stripe payment integration for QuantumVault Academy.
"""

import streamlit as st
import os
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False


def get_stripe_key():
    try:
        return st.secrets["STRIPE_SECRET_KEY"]
    except Exception:
        return os.getenv("STRIPE_SECRET_KEY", "")


PLANS = {
    "free": {
        "name": "Free Trial",
        "price": 0,
        "price_display": "$0",
        "period": "forever",
        "description": "Try QuantumVault with one grade level",
        "features": [
            "1 grade level module (your choice)",
            "Up to 10 students",
            "All mini games",
            "Leaderboard access",
            "No credit card required",
        ],
        "color": "#6b7280",
        "emoji": "🆓",
        "popular": False,
    },
    "classroom": {
        "name": "Classroom",
        "price": 49900,
        "price_display": "$499",
        "period": "/year",
        "description": "Single teacher, one grade level",
        "features": [
            "One grade level module",
            "Up to 35 students",
            "All mini games and AI Tutor",
            "Leaderboard access",
            "Progress tracking dashboard",
            "Email support",
            "30-day free trial",
        ],
        "color": "#3b82f6",
        "emoji": "🍎",
        "popular": False,
    },
    "school": {
        "name": "School",
        "price": 199900,
        "price_display": "$1,999",
        "period": "/year",
        "description": "Whole school, all three grade levels",
        "features": [
            "All three grade modules (K-12)",
            "Unlimited students",
            "All mini games and AI Tutor",
            "School-wide leaderboard",
            "Teacher dashboard with analytics",
            "Priority support",
            "Custom school branding",
            "NSA GenCyber grant eligible",
            "30-day free trial",
        ],
        "color": "#7c6dfa",
        "emoji": "🏫",
        "popular": True,
    },
    "per_student": {
        "name": "Per Student",
        "price": 500,
        "price_display": "$5",
        "period": "/student/year",
        "description": "Flexible per-student pricing (min 30 students)",
        "features": [
            "All three grade modules",
            "All mini games and AI Tutor",
            "School-wide leaderboard",
            "Teacher dashboard",
            "Minimum 30 students ($150/yr)",
            "Scales with your school",
            "30-day free trial",
        ],
        "color": "#10b981",
        "emoji": "🎓",
        "popular": False,
    },
    "grant": {
        "name": "Grant Package",
        "price": 249900,
        "price_display": "$2,499",
        "period": "/year",
        "description": "Full school plus grant writing support",
        "features": [
            "Everything in School plan",
            "Grant writing assistance letter",
            "FERPA compliance documentation",
            "Dedicated onboarding session",
            "NSA GenCyber application support",
            "Custom implementation plan",
            "Priority dedicated support",
        ],
        "color": "#f59e0b",
        "emoji": "📝",
        "popular": False,
    },
    "district": {
        "name": "District",
        "price": None,
        "price_display": "$15,000+",
        "period": "/year",
        "description": "Multiple schools, centralized admin",
        "features": [
            "Everything in Grant Package",
            "Unlimited schools",
            "District admin dashboard",
            "SSO integration",
            "Custom FERPA compliance docs",
            "Dedicated account manager",
            "White-label option available",
            "Custom pricing $15,000-50,000/yr",
        ],
        "color": "#ec4899",
        "emoji": "🌐",
        "popular": False,
    },
}


def create_checkout_session(plan_key, school_name, email):
    stripe.api_key = get_stripe_key()
    plan = PLANS[plan_key]
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "QuantumVault Academy — " + plan["name"] + " Plan",
                        "description": plan["description"],
                    },
                    "unit_amount": plan["price"],
                    "recurring": {"interval": "year"},
                },
                "quantity": 1,
            }],
            mode="subscription",
            customer_email=email,
            success_url="https://gitmandd3399.github.io/QuantumVault/landing/index.html?payment=success",
            cancel_url="https://gitmandd3399.github.io/QuantumVault/landing/index.html",
            metadata={"plan": plan_key, "school": school_name}
        )
        return session.url, None
    except Exception as e:
        return None, str(e)


def render_pricing_page():
    st.title("💎 QuantumVault Academy — Pricing")
    st.markdown(
        "The **only K-12 platform** teaching NIST post-quantum cryptography standards. "
        "All plans include a 30-day free trial. No credit card required."
    )

    # ── Free tier quick signup ───────────────────────────────────────────
    if st.session_state.get("plan_type", "free") == "free" and not st.session_state.get("free_module"):
        st.success("🆓 **Start for free — no credit card required!**")
        col1, col2 = st.columns([2,1])
        with col1:
            free_mod = st.selectbox(
                "Choose your free grade level module:",
                ["🟢 Elementary (K-5)", "🟡 Middle School (6-8)", "🔴 High School (9-12)"],
                key="free_mod_select"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Start Free", type="primary", key="start_free"):
                st.session_state.free_module = free_mod
                st.session_state.plan_type = "free"
                st.success("Free plan activated! Enjoy your free module.")
                st.rerun()
        st.markdown("---")

    # ── Trust bar ─────────────────────────────────────────────────────────
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.markdown(
            "<div style='background:#1e293b;border:1px solid #334155;border-radius:8px;"
            "padding:10px;text-align:center;'>"
            "<div style='font-size:1.5rem'>🔒</div>"
            "<div style='font-size:0.75rem;font-weight:bold;color:#a5b4fc'>COPPA Compliant</div>"
            "<div style='font-size:0.7rem;color:#888'>Student data protected</div>"
            "</div>", unsafe_allow_html=True
        )
    with t2:
        st.markdown(
            "<div style='background:#1e293b;border:1px solid #334155;border-radius:8px;"
            "padding:10px;text-align:center;'>"
            "<div style='font-size:1.5rem'>🎓</div>"
            "<div style='font-size:0.75rem;font-weight:bold;color:#a5b4fc'>NSA GenCyber</div>"
            "<div style='font-size:0.7rem;color:#888'>Grant eligible</div>"
            "</div>", unsafe_allow_html=True
        )
    with t3:
        st.markdown(
            "<div style='background:#1e293b;border:1px solid #334155;border-radius:8px;"
            "padding:10px;text-align:center;'>"
            "<div style='font-size:1.5rem'>↩️</div>"
            "<div style='font-size:0.75rem;font-weight:bold;color:#a5b4fc'>30-Day Trial</div>"
            "<div style='font-size:0.7rem;color:#888'>No credit card needed</div>"
            "</div>", unsafe_allow_html=True
        )
    with t4:
        st.markdown(
            "<div style='background:#1e293b;border:1px solid #334155;border-radius:8px;"
            "padding:10px;text-align:center;'>"
            "<div style='font-size:1.5rem'>⚛️</div>"
            "<div style='font-size:0.75rem;font-weight:bold;color:#a5b4fc'>NIST Aligned</div>"
            "<div style='font-size:0.7rem;color:#888'>FIPS 203/204/205/206</div>"
            "</div>", unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("### Choose Your Plan")

    # ── Main pricing cards ─────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)

    MAIN_PLANS = ["classroom", "school", "grant"]
    COLS = [col1, col2, col3]

    for col, plan_key in zip(COLS, MAIN_PLANS):
        plan = PLANS[plan_key]
        color = plan["color"]
        popular = plan.get("popular", False)
        with col:
            if popular:
                st.markdown(
                    f"<div style='background:{color};color:white;text-align:center;"
                    f"border-radius:8px 8px 0 0;padding:5px;font-size:0.75rem;"
                    f"font-weight:bold;'>⭐ MOST POPULAR</div>",
                    unsafe_allow_html=True
                )
            border_width = "2px" if popular else "1px"
            st.markdown(
                f"<div style='background:{color}10;border:{border_width} solid {color}50;"
                f"border-radius:{'0 0 10px 10px' if popular else '10px'};"
                f"padding:1.25rem;'>"
                f"<div style='font-size:2rem;margin-bottom:4px'>{plan['emoji']}</div>"
                f"<h3 style='color:{color};margin:0 0 4px'>{plan['name']}</h3>"
                f"<p style='color:#888;font-size:0.78rem;margin:0 0 12px'>{plan['description']}</p>"
                f"<div style='margin-bottom:12px'>"
                f"<span style='font-size:2.2rem;font-weight:800;color:white'>{plan['price_display']}</span>"
                f"<span style='font-size:0.8rem;color:#888'>{plan['period']}</span>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True
            )
            for feature in plan["features"]:
                st.markdown(
                    f"<div style='font-size:0.8rem;padding:3px 0;color:#ccc'>"
                    f"✅ {feature}</div>",
                    unsafe_allow_html=True
                )
            st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Additional plans ───────────────────────────────────────────────────
    st.markdown("### More Options")
    col1, col2 = st.columns(2)

    OTHER_PLANS = ["per_student", "district"]
    for col, plan_key in zip([col1, col2], OTHER_PLANS):
        plan = PLANS[plan_key]
        color = plan["color"]
        with col:
            st.markdown(
                f"<div style='background:{color}10;border:1px solid {color}40;"
                f"border-radius:10px;padding:1.25rem;'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
                f"<div>"
                f"<div style='font-size:1.5rem'>{plan['emoji']}</div>"
                f"<h4 style='color:{color};margin:4px 0'>{plan['name']}</h4>"
                f"<p style='color:#888;font-size:0.75rem;margin:0'>{plan['description']}</p>"
                f"</div>"
                f"<div style='text-align:right'>"
                f"<span style='font-size:1.8rem;font-weight:800;color:white'>{plan['price_display']}</span>"
                f"<div style='font-size:0.72rem;color:#888'>{plan['period']}</div>"
                f"</div>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True
            )
            for feature in plan["features"]:
                st.markdown(
                    f"<div style='font-size:0.78rem;padding:2px 0;color:#ccc'>"
                    f"✅ {feature}</div>",
                    unsafe_allow_html=True
                )
            st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Checkout form ──────────────────────────────────────────────────────
    st.markdown("### 🚀 Start Your Free Trial")
    st.markdown(
        "Fill in your details below. You will not be charged "
        "until after your 30-day free trial ends."
    )

    col1, col2 = st.columns(2)
    with col1:
        school_name = st.text_input(
            "School or Organization Name",
            placeholder="Lincoln Elementary School",
            key="payment_school"
        )
        email = st.text_input(
            "Your Email Address",
            placeholder="teacher@school.edu",
            key="payment_email"
        )
    with col2:
        plan_choice = st.selectbox(
            "Select Your Plan",
            ["classroom", "school", "per_student", "grant", "district"],
            format_func=lambda x: PLANS[x]["emoji"] + " " + PLANS[x]["name"] + " — " + PLANS[x]["price_display"],
            key="payment_plan"
        )
        selected_plan = PLANS[plan_choice]
        st.markdown(
            f"<div style='background:{selected_plan['color']}10;"
            f"border:1px solid {selected_plan['color']}40;"
            f"border-radius:8px;padding:10px;margin-top:8px;'>"
            f"<div style='font-size:0.8rem;color:#ccc'>{selected_plan['description']}</div>"
            f"<div style='font-size:1.1rem;font-weight:bold;color:white;margin-top:4px'>"
            f"{selected_plan['price_display']}{selected_plan['period']}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    if plan_choice == "district":
        st.info("District pricing is custom ($15,000-50,000/yr). Submit your info and we will contact you within 24 hours.")
    elif plan_choice == "per_student":
        students = st.number_input("Number of students", min_value=30, max_value=10000, value=100, step=10)
        annual = students * 5
        st.success(f"Your annual cost: **${annual:,}/yr** for {students} students")

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Free Trial →", key="start_trial", use_container_width=True, type="primary"):
            if not school_name or not email:
                st.error("Please enter your school name and email address.")
            elif "@" not in email:
                st.error("Please enter a valid email address.")
            elif plan_choice == "district":
                st.success(
                    "Thank you! We will contact you within 24 hours to discuss "
                    "district pricing and implementation."
                )
            else:
                with st.spinner("Creating your checkout session..."):
                    checkout_url, error = create_checkout_session(
                        plan_choice, school_name, email
                    )
                if error:
                    st.error("Payment error: " + error)
                    st.info("Having trouble? Email hello@quantumvaultacademy.com")
                else:
                    st.success("Redirecting to secure checkout...")
                    st.markdown(
                        f"[Click here if not redirected]({checkout_url})"
                    )

    st.markdown("---")
    st.caption(
        "Payments processed securely by Stripe. "
        "QuantumVault Academy never stores credit card information. "
        "Cancel anytime. Questions? Email hello@quantumvaultacademy.com"
    )


def handle_stripe_webhook(payload: bytes, sig_header: str) -> dict:
    """Verify Stripe webhook signature before processing events."""
    import logging
    import streamlit as _st
    webhook_secret = _st.secrets.get("STRIPE_WEBHOOK_SECRET", "")
    if not webhook_secret:
        logging.warning("STRIPE_WEBHOOK_SECRET not configured!")
        return {"error": "Webhook secret not set"}
    try:
        import stripe as _stripe
        event = _stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        logging.info(f"Stripe webhook verified: {event['type']}")
        return {"success": True, "type": event["type"]}
    except ValueError as e:
        logging.error(f"Invalid Stripe payload: {e}")
        return {"error": "Invalid payload"}
    except Exception as e:
        logging.error(f"Stripe signature failed: {e}")
        return {"error": "Signature verification failed"}
