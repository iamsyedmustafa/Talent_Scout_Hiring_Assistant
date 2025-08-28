import streamlit as st
from groq import Groq

# Load API key and model from Streamlit secrets
MODEL = st.secrets.get("MODEL", "llama-3.1-8b-instant")
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)

def ask_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_questions(tech_stack: str, num_questions: int = 5):
    """
    Generate a fixed number of clean technical questions for a given tech stack.
    """
    prompt = (
        f"Generate exactly {num_questions} concise technical interview questions for a candidate skilled in {tech_stack}. "
        "Do NOT include any introductory text. Number them if you want, but only return the questions, one per line."
    )

    try:
        response_text = ask_llm(prompt)

        # Split lines and clean them
        questions = []
        for line in response_text.split("\n"):
            line = line.strip()
            if not line:
                continue
            # Remove numbering like "1." or "- "
            if line[0].isdigit() and line[1] in [".", ")"]:
                line = line.split(maxsplit=1)[1]
            elif line.startswith("- "):
                line = line[2:]
            questions.append(line)

        # Ensure max num_questions
        return questions[:num_questions]

    except Exception as e:
        print(f"LLM Error: {e}")
        # Fallback questions
        return [f"Sample question {i+1} on {tech_stack}" for i in range(num_questions)]


