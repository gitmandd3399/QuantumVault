import streamlit as st
import datetime
import json

TRIAL_GAMES = ["code_shield", "cipher_quest"]  # pqc_python_lab parked
TRIAL_DAYS = 7

def _user_email():
    return st.session_state.get("user_email") or st.session_state.get("email")


def start_trial(game_key: str):
    """Start 7-day trial for a game if never started for this ACCOUNT (persists across logins)."""
    from modules import users as _users
    trial_key = "trial_start_" + game_key
    email = _user_email()
    if email:
        existing = _users.get_trial_start(email, game_key)
        if existing:
            st.session_state[trial_key] = existing
            return
        now = datetime.datetime.utcnow().isoformat()
        _users.set_trial_start(email, game_key, now)
        st.session_state[trial_key] = now
    else:
        if trial_key not in st.session_state:
            st.session_state[trial_key] = datetime.datetime.utcnow().isoformat()

def get_trial_days_left(game_key: str) -> int:
    """Returns days left in trial. -1 if never started. Checks the ACCOUNT record first."""
    from modules import users as _users
    trial_key = "trial_start_" + game_key
    if trial_key not in st.session_state:
        email = _user_email()
        if email:
            existing = _users.get_trial_start(email, game_key)
            if existing:
                st.session_state[trial_key] = existing
    if trial_key not in st.session_state:
        return -1
    start = datetime.datetime.fromisoformat(st.session_state[trial_key])
    elapsed = (datetime.datetime.utcnow() - start).days
    return max(0, TRIAL_DAYS - elapsed)

def is_trial_active(game_key: str) -> bool:
    """Returns True if trial is still active."""
    days_left = get_trial_days_left(game_key)
    return days_left > 0 or days_left == -1

def trial_gate(game_key: str, game_name: str) -> bool:
    """
    Call at top of each trial game.
    Returns True if user can play, False if trial expired and not paid.
    Also starts trial on first visit.
    """
    plan = st.session_state.get("plan_type", "free")
    if plan == "paid":
        return True

    # Trials require a logged-in account (prevents reload/incognito trial farming)
    if not _user_email():
        st.markdown(
            "<div style='background:#071520;border:2px solid #1d4ed8;border-radius:16px;"
            "padding:26px;text-align:center;margin:16px 0'>"
            "<div style='font-size:2.6rem;margin-bottom:8px'>🎁</div>"
            "<h3 style='color:#60a5fa;margin-bottom:6px'>" + game_name + " — Free 7-Day Trial</h3>"
            "<p style='color:#94a3b8;margin-bottom:4px'>Sign in with your email to unlock your free trial.<br>"
            "One trial per account — no credit card needed.</p>"
            "</div>",
            unsafe_allow_html=True
        )
        return False

    # Start trial on first visit
    trial_key = "trial_start_" + game_key
    if trial_key not in st.session_state:
        start_trial(game_key)
        days_left = TRIAL_DAYS
    else:
        days_left = get_trial_days_left(game_key)

    if days_left > 0:
        # Show trial banner
        st.markdown(
            "<div style='background:#1a1a00;border:1px solid #fbbf24;border-radius:8px;"
            "padding:6px 12px;margin-bottom:8px;text-align:center;font-size:11px;color:#fbbf24'>"
            "🎁 FREE TRIAL — <b>" + str(days_left) + " day" + ("s" if days_left != 1 else "") +
            " remaining</b> | Upgrade to keep access after trial ends"
            "</div>",
            unsafe_allow_html=True
        )
        return True
    else:
        # Trial expired
        st.markdown(
            "<div style='background:#071520;border:2px solid #1d4ed8;border-radius:16px;"
            "padding:30px;text-align:center;margin:20px 0'>"
            "<div style='font-size:3rem;margin-bottom:10px'>⏰</div>"
            "<h2 style='color:#60a5fa;margin-bottom:8px'>" + game_name + " — Trial Ended</h2>"
            "<p style='color:#94a3b8;margin-bottom:16px'>"
            "Your 7-day free trial has ended.<br>"
            "Upgrade to continue playing all 3 AI coding games!</p>"
            "</div>",
            unsafe_allow_html=True
        )
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("🚀 Upgrade to Keep Playing", type="primary",
                         use_container_width=True, key="trial_upgrade_" + game_key):
                st.session_state.level = "💎 Pricing & Plans"
                st.rerun()
            st.markdown(
                "<div style='text-align:center;margin-top:6px;font-size:10px;color:#475569'>"
                "School license from $1,999/yr · 30-day money-back guarantee"
                "</div>",
                unsafe_allow_html=True
            )
        return False
