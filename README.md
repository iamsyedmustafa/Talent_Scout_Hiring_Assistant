# Talentscout - AI Hiring Assistant at PGAGI

Talentscout is an AI-powered interactive hiring assistant that automates candidate information collection and technical interviews. It generates technical questions dynamically based on the candidate's tech stack and stores responses in a SQLite database.

# Project Overview

Talentscout provides an interactive step-by-step process:

1. Greeting & Candidate Information
   - Greets the candidate and provides a brief overview of its purpose.
   - Collects details such as Name, Email, Phone, Years of Experience, Position Applied For, Location, and Tech Stack.

2. Technical Q&A
   - Generates 3–5 technical questions based on the candidate's tech stack using a Large Language Model (Groq LLM).
   - Candidate answers are stored securely in a SQLite database.

3. Confirmation & Summary
   - After submitting all answers, the system displays a summary message thanking the candidate and informing them about next steps.

# Features

- Interactive chatbot flow with greeting, info collection, Q&A, and summary.
- Dynamic technical question generation based on the declared tech stack.
- Multi-step interview flow with session state management.
- Responses stored securely in SQLite (`hiring_assistant.db`).
- Option to extend with admin panel for reviewing candidate responses.

# Technology Stack

- **Programming Language:** Python 3.x  
- **Frontend / UI:** Streamlit  
- **Database:** SQLite  
- **AI / Question Generation:** Groq LLM (`llama-3.1-8b-instant`)  
- **Environment Variables:** `.env` for API key and model settings  

# Project Structure

talent_scout/
├── main.py # Streamlit app (interactive chatbot)
├── ai.py # LLM-based technical question generator
├── db.py # SQLite database functions
├── hiring_assistant.db # SQLite database
├── .env # Groq API key and model info
├── requirements.txt # Python dependencies
└── README.md # Project documentation

# How to Run Locally

1. Clone the repository
```bash
git clone <your-repo-url>
cd talent_scout

2. Install dependencies
pip install -r requirements.txt

3. Create a .env file in the project root:
GROQ_API_KEY=your_groq_api_key_here
MODEL=llama-3.1-8b-instant

4. Run the Streamlit app
streamlit run main.py

5. Open the browser at http://localhost:8501 and interact with Talentscout.

# Database Schema

1. candidates table:
id, name, email, phone, experience, position, location, tech_stack

2. responses table:
id, candidate_id, question, answer

All candidate information and responses are stored in hiring_assistant.db.

# Prompt Design

Prompts are crafted to generate technical questions tailored to each candidate's declared tech stack.
Example: If a candidate lists Python and Django, the model generates questions related to Python programming and Django framework.
Prompts are clear and concise to ensure the LLM produces focused, relevant questions.

# Challenges & Solutions

Session Management: Ensured multi-step interview flow works using Streamlit session_state to maintain context.
Question Formatting: Split LLM responses into individual questions for consistent display.
Database Handling: Created modular functions in db.py to safely insert and fetch candidate data and responses.
Fallback Handling: Added default responses when candidates submit empty answers.

# Deployment

-Push the project to GitHub.
-Deploy using Streamlit Cloud:
-Connect your GitHub repo.
-Set environment variables (GROQ_API_KEY, MODEL).
-Click Deploy and share the generated link.
-Test the app online and ensure all functionalities work as expected.
