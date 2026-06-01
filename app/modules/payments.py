"""
modules/payments.py
───────────────────
Stripe payment integration for QuantumVault Academy.
"""

import streamlit as st
import stripe
import os


def get_stripe_key():
    try:
        return st.secrets["STRIPE_SECRET_KEY"]
    except Exception:
        return os.getenv("STRIPE_SECRET_KEY", "")


PLANS = {
    "classroom": {
        "name": "Classroom",
        "price": 29900,
        "price_display": "$299",
        "period": "/year",
        "description": "Single teacher, one grade level",
        "features": [
            "One grade level module",
            "Up to 35 students",
            "All mini games",
            "Leaderboard access",
            "Email support",
            "30-day free trial",
        ],
        "color": "#3b82f6",
        "emoji": "🍎",
        "popular": False,
    },
    "school": {
        "name": "School",
        "price": 99900,
        "price_display": "$999",
        "period": "/year",
        "description": "Whole school, all three grade levels",
        "features": [
            "All three grade modules",
            "Unlimited students",
            "All mini games",
            "School-wide leaderboard",
            "Teacher dashboard",
            "Priority support",
            "Custom school branding",
            "30-day free trial",
        ],
        "color": "#7c6dfa",
        "emoji": "🏫",
        "popular": True,
    },
    "district": {
        "name": "District",
        "price": None,
        "price_display": "Custom",
        "period": "",
        "description": "Multiple schools, centralized admin",
        "features": [
            "Everything in School",
            "Unlimited schools",
            "District admin dashboard",
            "SSO integration",
            "FERPA compliance docs",
            "Dedicated account manager",
            "Grant writing assistance",
        ],
        "color": "#10b981",
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
            ["classroom", "school"],
            format_func=lambda x: PLANS[x]["emoji"] + " " + PLANS[x]["name"] + " — " + PLANS[x]["price_display"] + "/year",
            key="payment_plan"
        )
        st.info("District plans are custom priced. Select School and we will contact you.")

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
