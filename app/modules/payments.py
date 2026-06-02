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
    st.title("💎 Choose Your Plan")
    st.markdown(
        "All plans include a **30-day free trial**. "
        "No credit card required for trial. Cancel anytime."
    )
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for i, (plan_key, plan) in enumerate(PLANS.items()):
        with cols[i]:
            color = plan["color"]
            if plan["popular"]:
                st.success("⭐ Most Popular")

            st.markdown(
                plan["emoji"] + " **" + plan["name"] + "**"
            )
            st.markdown(
                "**" + plan["price_display"] + "**" + plan["period"]
            )
            st.caption(plan["description"])
            st.markdown("---")
            for feature in plan["features"]:
                st.markdown("✅ " + feature)

    st.markdown("---")
    st.markdown("### 🛒 Start Your Free Trial")
    st.markdown(
        "Fill in your details below. "
        "You will not be charged until after your 30-day free trial ends."
    )

    col1, col2 = st.columns(2)
    with col1:
        school_name = st.text_input(
            "School name",
            placeholder="Lincoln Elementary School",
            key="payment_school"
        )
        email = st.text_input(
            "Your email address",
            placeholder="teacher@school.edu",
            key="payment_email"
        )
    with col2:
        plan_choice = st.selectbox(
            "Select your plan",
            ["classroom", "school", "per_student", "grant", "district"],
            format_func=lambda x: PLANS[x]["emoji"] + " " + PLANS[x]["name"] + " — " + PLANS[x]["price_display"],
            key="payment_plan"
        )
        if plan_choice == "district":
            st.info("District plans are custom priced at $15,000-50,000/yr. Select District and we will contact you within 24 hours.")
        elif plan_choice == "per_student":
            st.info("Per-student pricing: $5/student/yr with a minimum of 30 students ($150/yr minimum).")
        elif plan_choice == "grant":
            st.info("Grant Package includes grant writing assistance for NSA GenCyber and other cybersecurity education grants.")

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Free Trial", key="start_trial", use_container_width=True):
            if not school_name or not email:
                st.error("Please enter your school name and email.")
            elif "@" not in email:
                st.error("Please enter a valid email address.")
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
                        "[Click here to go to checkout](" + checkout_url + ")"
                    )

    st.markdown("---")
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.markdown("🔒 **Secure**\n\nStripe encrypted")
    with t2:
        st.markdown("✅ **COPPA**\n\nCompliant platform")
    with t3:
        st.markdown("🎓 **Grant**\n\nNSA GenCyber eligible")
    with t4:
        st.markdown("↩️ **Refund**\n\n30-day money back")

    st.caption(
        "Payments processed securely by Stripe. "
        "QuantumVault Academy never stores credit card information."
    )
