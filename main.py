import streamlit as st
from ai import generate_questions
import db

st.set_page_config(page_title="Talentscout - AI Hiring Assistant", page_icon="💼", layout="centered")

# ---------- Bootstrapping ----------
try:
    db.init_db()
except Exception as e:
    st.error("Google Sheets connection failed. Check your secrets and sheet name.")
    st.stop()

# ---------- Session State ----------
if "candidate_id" not in st.session_state:
    st.session_state.candidate_id = None
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "step" not in st.session_state:
    st.session_state.step = 1  # 1: Info form, 2: Q&A

st.title("💼 Talentscout - AI Hiring Assistant")

# ---------- Step 1: Candidate Info ----------
if st.session_state.step == 1:
    st.info("👋 I’m Talentscout. Please enter your details to begin your interview.")

    with st.form("candidate_form"):
        name = st.text_input("Full Name *")
        email = st.text_input("Email *")
        phone = st.text_input("Phone *")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1, value=0)
        position = st.text_input("Position Applied For *")
        location = st.text_input("Location *")
        tech_stack = st.text_area("Tech Stack (comma-separated) *", placeholder="Python, SQL, TensorFlow")

        submitted = st.form_submit_button("Save & Continue")

        if submitted:
            if all([name.strip(), email.strip(), phone.strip(), position.strip(), location.strip(), tech_stack.strip()]):
                cid = db.insert_candidate(
                    name.strip(), email.strip(), phone.strip(), int(experience),
                    position.strip(), location.strip(), tech_stack.strip()
                )
                st.session_state.candidate_id = cid
                st.session_state.info_saved = True
            else:
                st.error("⚠️ Please fill all required fields.")

    if st.session_state.get("info_saved"):
        st.success("✅ Your information has been saved.")
        st.info("Next, I’ll ask a few technical questions based on your tech stack.")
        if st.button("Okay, let's proceed!"):
            st.session_state.step = 2
            st.session_state.info_saved = False

# ---------- Step 2: Technical Q&A ----------
elif st.session_state.step == 2:
    candidate = db.get_candidate_by_id(st.session_state.candidate_id)
    if not candidate:
        st.error("Candidate not found. Please go back and re-enter details.")
        if st.button("Start Over"):
            st.session_state.step = 1
        st.stop()

    tech_stack = candidate[7]  # tech_stack column
    if not st.session_state.questions:
        st.session_state.questions = generate_questions(tech_stack, num_questions=8)

    if st.session_state.current_q < len(st.session_state.questions):
        q = st.session_state.questions[st.session_state.current_q]
        st.subheader(f"Q{st.session_state.current_q + 1}: {q}")

        answer = st.text_area("Your answer:", key=f"answer_{st.session_state.current_q}", height=150)

        cols = st.columns(2)
        with cols[0]:
            if st.button("Submit Answer"):
                if answer.strip():
                    db.insert_response(st.session_state.candidate_id, q, answer.strip())
                    st.session_state.answers[q] = answer.strip()
                    st.session_state.current_q += 1
                    st.experimental_rerun()
                else:
                    st.warning("⚠️ Please enter an answer before submitting.")
        with cols[1]:
            if st.button("Skip"):
                db.insert_response(st.session_state.candidate_id, q, "(skipped)")
                st.session_state.current_q += 1
                st.experimental_rerun()

    else:
        st.success("🎉 Thank you! Your responses have been recorded. We will reach out to you soon.")
        st.subheader("Your Answers Summary")
        for i, (q, a) in enumerate(st.session_state.answers.items(), start=1):
            st.markdown(f"**Q{i}: {q}**")
            st.markdown(f"**A:** {a}")
        if st.button("Start New Interview"):
            for k in ["candidate_id","questions","current_q","answers","step","info_saved"]:
                st.session_state.pop(k, None)
            st.session_state.step = 1
            st.experimental_rerun()


