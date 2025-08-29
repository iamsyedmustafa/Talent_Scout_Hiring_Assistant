import streamlit as st
from groq import Groq

# Secrets: keep these in Streamlit Cloud → App settings → Secrets
MODEL = st.secrets.get("MODEL", "llama-3.1-8b-instant")
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)

def ask_llm(prompt: str) -> str:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return resp.choices[0].message.content

def generate_questions(tech_stack: str, num_questions: int = 8):
    """
    Generate a fixed number of clean technical questions for a given tech stack.
    """
    prompt = (
        f"Generate exactly {num_questions} concise, practical technical interview questions "
        f"for a candidate skilled in: {tech_stack}. "
        "Return ONLY the questions, one per line, no bullets, no explanations."
    )

    try:
        response_text = ask_llm(prompt)

        questions = []
        for raw in response_text.splitlines():
            line = raw.strip()
            if not line:
                continue
            # Strip common numbering formats like "1. ", "1) ", "- "
            if len(line) >= 3 and line[0].isdigit() and line[1] in {'.', ')'} and line[2] == ' ':
                line = line[3:].strip()
            elif line[:2] in {"- ", "• "}:
                line = line[2:].strip()
            questions.append(line)

        # Ensure exact count
        questions = [q for q in questions if q][:num_questions]
        # pad if the model returned fewer lines
        while len(questions) < num_questions:
            questions.append(f"Describe a real-world use of {tech_stack} #{len(questions)+1}")
        return questions

    except Exception as e:
        # Fallback questions
        return [f"Sample question {i+1} on {tech_stack}" for i in range(num_questions)]



