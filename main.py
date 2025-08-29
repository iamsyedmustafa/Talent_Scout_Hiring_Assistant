import streamlit as st
import gspread
from groq import Groq

# ------------------------------
# Load secrets from .streamlit/secrets.toml
# ------------------------------
service_account_info = st.secrets["gcp_service_account"]
google_sheet_name = st.secrets["general"]["google_sheet_name"]
groq_api_key = st.secrets["general"]["GROQ_API_KEY"]
model = st.secrets["general"]["MODEL"]

# ------------------------------
# Google Sheets Setup
# ------------------------------
gc = gspread.service_account_from_dict(service_account_info)
sh = gc.open(google_sheet_name)
worksheet = sh.sheet1  # use first sheet

# ------------------------------
# Groq Client Setup
# ------------------------------
client = Groq(api_key=groq_api_key)

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("🤖 TalentScout Hiring Assistant")

st.write("Welcome! Enter the tech stack and I'll generate interview questions for you.")

# Input for tech stack
tech_stack = st.text_input("Enter candidate's tech stack:")

if st.button("Generate Questions"):
    if not tech_stack.strip():
        st.warning("Please enter a tech stack first!")
    else:
        # Generate questions with Groq
        with st.spinner("Generating questions..."):
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI hiring assistant. Generate 8-10 technical interview questions based on the given tech stack."
                    },
                    {
                        "role": "user",
                        "content": f"Tech stack: {tech_stack}"
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )

            questions_text = response.choices[0].message["content"]
            st.session_state.questions = questions_text.split("\n")

# ------------------------------
# Display Questions & Collect Answers
# ------------------------------
if "questions" in st.session_state:
    st.subheader("Candidate Questions & Answers")

    answers = []
    for i, q in enumerate(st.session_state.questions, start=1):
        if q.strip():
            st.write(f"**Q{i}. {q.strip()}**")
            ans = st.text_area(f"Answer {i}", key=f"ans_{i}")
            answers.append((q.strip(), ans))

    if st.button("Submit Answers"):
        # Save answers to Google Sheet
        for q, a in answers:
            worksheet.append_row([tech_stack, q, a])

        st.success("✅ Answers submitted successfully to Google Sheet!")

