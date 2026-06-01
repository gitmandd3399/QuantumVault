"""
modules/payments.py
───────────────────
Stripe payment integration for QuantumVault Academy.
Handles Classroom ($299), School ($999), and District (custom) plans.
"""

import streamlit as st
import stripe
import os

# ── Stripe setup ─────────────────────────────────────────────────────────────
def get_stripe_key():
    try:
        return st.secrets["STRIPE_SECRET_KEY"]
    except Exception:
        return os.getenv("STRIPE_SECRET_KEY", "")

# ── Pricing config ────────────────────────────────────────────────────────────
PLANS = {
    "classroom": {
        "name": "Classroom",
        "price": 29900,  # cents
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
    },
    "school": {
        "name": "School",
        "price": 99900,  # cents
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
    },
}


def create_checkout_session(plan_key: str, school_name: str, email: str):
    """Create a Stripe checkout session for the given plan."""
    stripe.api_key = get_stripe_key()
    plan = PLANS[plan_key]

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"QuantumVault Academy — {plan['name']} Plan",
                        "description": plan["description"],
                        "metadata": {
                            "plan": plan_key,
                            "school": school_name,
                        }
                    },
                    "unit_amount": plan["price"],
                    "recurring": {"interval": "year"},
                },
                "quantity": 1,
            }],
            mode="subscription",
            customer_email=email,
            success_url="https://gitmandd3399.github.io/QuantumVault/landing/index.html?payment=success",
            cancel_url="https://gitmandd3399.github.io/QuantumVault/landing/index.html?payment=cancelled",
            metadata={
                "plan": plan_key,
                "school": school_name,
            }
        )
        return session.url, None
    except stripe.error.StripeError as e:
        return None, str(e)
    except Exception as e:
        return None, str(e)


def render_pricing_page():
    """Full pricing and checkout page inside Streamlit."""
    st.title("💎 Choose Your Plan")
    st.markdown(
        "All plans include a **30-day free trial**. "
        "No credit card required for trial. Cancel anytime."
    )

    st.markdown("---")

    # ── Pricing cards ─────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)

    for col, (plan_key, plan) in zip([col1, col2, col3], PLANS.items()):
        with col:
            popular = plan.get("popular", False)
            color = plan["color"]

            st.markdown(
                f"""
                <div style="background:{color}10;border:{'2px' if popular else '1px'} 
                    solid {color}{'80' if popular else '30'};border-radius:12px;
                    padding:1.5rem;min-height:420px;position:relative;">
                    {'<div style="position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:'+color+';color:white;font-size:0.7rem;font-weight:600;padding:3px 12px;border-radius:100px;">Most Popular</div>' if popular else ''}
                    <div style="font-size:2rem;margin-bottom:0.5rem">{plan['emoji']}</div>
                    <h3 style="color:{color};margin:0 0 0.25rem">{plan['name']}</h3>
                    <p style="font-size:0.8rem;color:#888;margin:0 0 1rem">{plan['description']}</p>
                    <div style="margin-bottom:1rem">
                        <span style="font-size:2.5rem;font-weight:800;color:white">{plan['price_display']}</span>
                        <span style="font-size:0.85rem;color:#888">{plan['period']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            for feature in plan["features"]:
                st.markdown(f"✅ {feature}")

    st.markdown("---")

    # ── Checkout form ─────────────────────────────────────────────────────────
    st.markdown("### 🛒 Start Your Free Trial")
    st.markdown(
        "Fill in your details below. You won't be charged until "
        "after your 30-day free trial ends."
    )

    col1, col2 = st.columns(2)
    with col1:
        school_name = st.text_input(
            "School / Organization name",
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
            format_func=lambda x: f"{PLANS[x]['emoji']} {PLANS[x]['name']} — {PLANS[x]['price_display']}/year",
            key="payment_plan"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(
            "💡 **District plans** are custom priced. "
            "Select School and we'll contact you about district pricing."
        )

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "🚀 Start Free Trial →",
            key="start_trial",
            use_container_width=True
        ):
            if not school_name or not email:
                st.error("Please enter your school name and email address.")
            elif "@" not in email:
                st.error("Please enter a valid email address.")
            else:
                with st.spinner("Creating your checkout session..."):
                    checkout_url, error = create_checkout_session(
                        plan_choice, school_name, email
                    )
                if error:
                    st.error(f"Payment error: {error}")
                    st.info(
                        "Having trouble? Email us at "
                        "hello@quantumvaultacademy.com"
                    )
                else:
                    st.success("✅ Redirecting to secure checkout...")
                    st.markdown(
                        f'<meta http-equiv="refresh" content="2;url={checkout_url}">',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"[Click here if not redirected automatically]({checkout_url})"
                    )

    st.markdown("---")

    # ── Trust signals ─────────────────────────────────────────────────────────
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.markdown("🔒 **Secure**\nStripe encrypted payments")
    with t2:
        st.markdown("✅ **COPPA**\nCompliant platform")
    with t3:
        st.markdown("🎓 **Grant**\nNSA GenCyber eligible")
    with t4:
        st.markdown("↩️ **Refund**\n30-day money back")

    st.caption(
        "Payments processed securely by Stripe. "
        "QuantumVault Academy never stores credit card information. "
        "Cancel anytime from your account dashboard."
    )