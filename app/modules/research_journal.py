"""
modules/research_journal.py
────────────────────────────
Student Research Journal with AI feedback.
Students write entries after completing activities.
"""

import streamlit as st
import datetime
import anthropic


PROMPTS = [
    "What did you learn about post-quantum cryptography today?",
    "Explain Kyber encryption in your own words.",
    "Why do we need to replace RSA with quantum-safe algorithms?",
    "What surprised you most about lattice mathematics?",
    "How would you explain the avalanche effect to a friend?",
    "What is the Learning With Errors problem and why is it hard?",
    "Which NIST PQC algorithm is your favorite and why?",
    "How does a digital signature prove authenticity?",
    "What would happen to the internet if quantum computers broke RSA tomorrow?",
    "How does Shor's Algorithm threaten classical cryptography?",
    "What is the difference between Kyber and Dilithium?",
    "Why did NIST choose lattice-based algorithms over other approaches?",
]


def get_ai_feedback(entry: str, prompt: str) -> str:
    """Get AI feedback on a journal entry."""
    try:
        client = anthropic.Anthropic(
            api_key=st.secrets.get("ANTHROPIC_API_KEY", "")
        )
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system=(
                "You are a friendly PQC teacher giving encouraging feedback on a student's "
                "research journal entry about post-quantum cryptography. "
                "Keep feedback to 3-4 sentences. Be encouraging and specific. "
                "Point out what they got right, gently correct any misconceptions, "
                "and suggest one thing to explore further. "
                "Never be discouraging. Always end with an encouraging phrase."
            ),
            messages=[{
                "role": "user",
                "content": (
                    f"Journal prompt: {prompt}\n\n"
                    f"Student's entry: {entry}\n\n"
                    f"Please give brief encouraging feedback."
                )
            }]
        )
        return response.content[0].text
    except Exception as e:
        return (
            "Great effort on your journal entry! Keep exploring PQC concepts — "
            "the more you write, the deeper your understanding grows. "
            "Try to include specific algorithm names and math concepts in future entries!"
        )


def render_research_journal():
    st.title("📖 Research Journal")
    st.markdown(
        "Write about what you are learning! "
        "Get AI feedback on your entries and earn XP for thoughtful writing."
    )

    # Initialize journal
    if "journal_entries" not in st.session_state:
        st.session_state.journal_entries = []

    xp = st.session_state.get("xp", 0)
    entries = st.session_state.journal_entries

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📝 Entries Written", len(entries))
    with col2:
        st.metric("⭐ XP from Journal", min(len(entries) * 15, 150))
    with col3:
        st.metric("🔥 Writing Streak", f"{min(len(entries), 7)} days")

    st.markdown("---")

    # Write new entry
    st.markdown("### ✍️ Write a New Entry")

    col1, col2 = st.columns([2, 1])
    with col1:
        today = datetime.date.today().strftime("%B %d, %Y")
        st.caption(f"📅 {today}")

        # Random prompt suggestion
        import random
        if "current_prompt" not in st.session_state:
            st.session_state.current_prompt = random.choice(PROMPTS)  # nosec B311

        st.info(f"💡 **Prompt suggestion:** {st.session_state.current_prompt}")

        if st.button("🎲 New Prompt", key="new_prompt"):
            st.session_state.current_prompt = random.choice(PROMPTS)  # nosec B311
            st.rerun()

    with col2:
        grade = st.selectbox(
            "Module:",
            ["Elementary", "Middle School", "High School"],
            key="journal_grade"
        )
        topic = st.selectbox(
            "Topic:",
            ["Kyber/LWE", "Dilithium", "SPHINCS+", "Falcon",
             "Lattice Math", "Hash Functions", "Quantum Threat",
             "NIST Standards", "Other"],
            key="journal_topic"
        )

    entry_text = st.text_area(
        "Your journal entry:",
        height=160,
        placeholder=(
            "Write at least 3 sentences about what you learned. "
            "Include specific algorithm names, math concepts, or examples. "
            "The more detail you include, the better your AI feedback will be!"
        ),
        key="journal_entry_text"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        get_feedback = st.checkbox("Get AI feedback on my entry", value=True, key="want_feedback")
    with col2:
        word_count = len(entry_text.split()) if entry_text else 0
        color = "#10b981" if word_count >= 30 else "#f59e0b" if word_count >= 15 else "#ef4444"
        st.markdown(
            f"<div style='color:{color};font-size:0.85rem;padding-top:8px;'>"
            f"📝 {word_count} words "
            f"({'Great!' if word_count >= 30 else 'Add more!' if word_count >= 15 else 'Too short'})"
            f"</div>",
            unsafe_allow_html=True
        )

    if st.button("📝 Save Entry", key="save_entry", type="primary"):
        if not entry_text or len(entry_text.strip()) < 20:
            st.error("Please write at least a few sentences!")
        else:
            feedback = ""
            if get_feedback:
                with st.spinner("Getting AI feedback..."):
                    feedback = get_ai_feedback(
                        entry_text,
                        st.session_state.current_prompt
                    )

            entry = {
                "date": today,
                "grade": grade,
                "topic": topic,
                "prompt": st.session_state.current_prompt,
                "text": entry_text,
                "feedback": feedback,
                "word_count": word_count,
            }

            st.session_state.journal_entries.insert(0, entry)

            # Award XP
            xp_earned = min(15 + (word_count // 10), 30)
            st.session_state.xp = st.session_state.get("xp", 0) + xp_earned
            st.success(f"✅ Entry saved! +{xp_earned} XP")

            if feedback:
                st.markdown("### 🤖 AI Feedback")
                st.info(feedback)

            # New prompt for next entry
            import random
            st.session_state.current_prompt = random.choice(PROMPTS)  # nosec B311
            st.balloons()

    st.markdown("---")

    # Past entries
    if entries:
        st.markdown("### 📚 Your Journal Entries")
        for i, entry in enumerate(entries):
            with st.expander(
                f"📅 {entry['date']} — {entry['topic']} ({entry['word_count']} words)",
                expanded=(i == 0)
            ):
                st.markdown(f"**Module:** {entry['grade']}  |  **Topic:** {entry['topic']}")
                st.markdown(f"**Prompt:** *{entry['prompt']}*")
                st.markdown("---")
                st.markdown(entry["text"])
                if entry.get("feedback"):
                    st.markdown("**🤖 AI Feedback:**")
                    st.info(entry["feedback"])

        st.markdown("---")

        # Export journal
        if st.button("📥 Export Journal as Text", key="export_journal"):
            export_text = f"QuantumVault Academy — Research Journal\n{'='*50}\n\n"
            for entry in entries:
                export_text += f"Date: {entry['date']}\n"
                export_text += f"Module: {entry['grade']} | Topic: {entry['topic']}\n"
                export_text += f"Prompt: {entry['prompt']}\n\n"
                export_text += f"{entry['text']}\n\n"
                if entry.get("feedback"):
                    export_text += f"AI Feedback: {entry['feedback']}\n"
                export_text += f"{'─'*40}\n\n"

            st.download_button(
                label="⬇️ Download Journal",
                data=export_text,
                file_name="QuantumVault_Journal.txt",
                mime="text/plain",
                key="dl_journal"
            )
    else:
        st.info(
            "No entries yet! Write your first journal entry above. "
            "The AI will give you personalized feedback on your writing."
        )
