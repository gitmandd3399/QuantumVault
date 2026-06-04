"""
modules/threat_thermometer.py
Quantum Threat Thermometer — visual dashboard showing quantum threat levels.
"""
import streamlit as st
import streamlit.components.v1 as components


def render_threat_thermometer():
    st.title("🌡️ Quantum Threat Thermometer")
    st.markdown(
        "📊 **How close are we to quantum computers breaking encryption?** "
        "Adjust the year slider to see how the threat level changes across different systems "
        "as quantum computing advances!"
    )

    year = st.slider("📅 Set the year:", 2025, 2040, 2025, key="thermo_year")

    SYSTEMS = [
        {"name": "🏦 Banking (RSA-2048)", "breaks_at": 2033, "color": "#ef4444",
         "action": "Migrate to ML-KEM NOW — harvest-now-decrypt-later attacks already happening!"},
        {"name": "🌐 HTTPS/TLS (ECDH)", "breaks_at": 2033, "color": "#ef4444",
         "action": "Deploy hybrid Kyber+ECDH TLS immediately — CloudFlare already doing this!"},
        {"name": "📧 Email (PGP/RSA)", "breaks_at": 2032, "color": "#ef4444",
         "action": "Switch to PQC email standards — most urgent for sensitive communications!"},
        {"name": "🏥 Medical Records (AES-256)", "breaks_at": 2045, "color": "#10b981",
         "action": "AES-256 is still safe — Grover gives sqrt speedup but 128-bit quantum security holds!"},
        {"name": "🔐 Kyber-768 (ML-KEM)", "breaks_at": 2100, "color": "#10b981",
         "action": "Quantum-safe! Module-LWE has no known quantum speedup — you are protected!"},
        {"name": "✍️ Code Signing (ECDSA)", "breaks_at": 2032, "color": "#f97316",
         "action": "Migrate to ML-DSA (Dilithium) for all code signing certificates ASAP!"},
        {"name": "🛡️ VPN (DH-2048)", "breaks_at": 2031, "color": "#ef4444",
         "action": "Most urgent! VPNs using classical DH are first to fall — upgrade to ML-KEM!"},
        {"name": "🌲 SPHINCS+ (Hash-based)", "breaks_at": 2100, "color": "#10b981",
         "action": "Quantum-safe forever — hash-based crypto survives even if lattices are broken!"},
    ]

    st.markdown("---")
    cols = st.columns(2)
    for i, sys in enumerate(SYSTEMS):
        years_left = sys["breaks_at"] - year
        threat = max(0, min(100, (year - 2025) / (sys["breaks_at"] - 2025) * 100))

        if years_left <= 0:
            level = "BROKEN"
            tcolor = "#ef4444"
            icon = "💀"
        elif years_left <= 5:
            level = "CRITICAL"
            tcolor = "#ef4444"
            icon = "🚨"
        elif years_left <= 10:
            level = "HIGH RISK"
            tcolor = "#f97316"
            icon = "⚠️"
        elif years_left <= 15:
            level = "MEDIUM"
            tcolor = "#f59e0b"
            icon = "⚡"
        else:
            level = "SAFE"
            tcolor = "#10b981"
            icon = "✅"

        with cols[i % 2]:
            bar_width = min(100, int(threat))
            st.markdown(
                f"<div style='background:#1e293b;border:1px solid #334155;"
                f"border-radius:12px;padding:14px;margin:6px 0'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px'>"
                f"<div style='font-size:0.85rem;font-weight:bold;color:white'>{sys['name']}</div>"
                f"<div style='font-size:0.75rem;font-weight:bold;color:{tcolor}'>{icon} {level}</div>"
                f"</div>"
                f"<div style='background:#0f172a;border-radius:6px;height:8px;overflow:hidden;margin-bottom:8px'>"
                f"<div style='height:100%;width:{bar_width}%;background:linear-gradient(to right,{sys['color']},{tcolor});border-radius:6px;transition:width 0.3s'></div>"
                f"</div>"
                f"<div style='font-size:0.72rem;color:#888;line-height:1.4'>{sys['action']}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.markdown("---")
    broken = sum(1 for s in SYSTEMS if year >= s["breaks_at"])
    safe = sum(1 for s in SYSTEMS if year < s["breaks_at"] - 10)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💀 Systems Broken", broken, delta=f"by {year}")
    with col2:
        st.metric("✅ Systems Safe", safe)
    with col3:
        st.metric("📅 Year", year, delta=f"{year-2025} years from now")

    if broken > 0:
        st.error(f"🚨 In {year}, {broken} system(s) are broken by quantum computers! "
                f"Migrate to Kyber (ML-KEM) and Dilithium (ML-DSA) immediately!")
    else:
        st.success(f"✅ In {year}, all systems are still holding. But migration should begin NOW "
                  f"due to harvest-now-decrypt-later attacks!")

    st.info(
        "📌 **Important:** These dates are estimates based on current quantum computing progress. "
        "NIST recommends completing migration by 2035. The harvest-now-decrypt-later threat "
        "means encrypted data stolen TODAY can be decrypted when quantum computers arrive!"
    )

    if st.button("✅ I understand the quantum timeline! +15 XP", key="thermo_done"):
        st.session_state.xp = st.session_state.get("xp", 0) + 15
        st.session_state.badges = st.session_state.get("badges", []) + ["🌡️ Threat Analyst"]
        st.success("+15 XP! Badge: Threat Analyst unlocked!")
