import sqlite3

# ---------- Database Initialization ----------
def init_db():
    conn = sqlite3.connect("hiring_assistant.db")
    cursor = conn.cursor()

    # Candidate Info Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            experience INTEGER,
            position TEXT,
            location TEXT,
            tech_stack TEXT
        )
    ''')

    # Responses Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            question TEXT,
            answer TEXT,
            FOREIGN KEY(candidate_id) REFERENCES candidates(id)
        )
    ''')

    conn.commit()
    conn.close()

# ---------- Insert Functions ----------
def insert_candidate(name, email, phone, experience, position, location, tech_stack):
    conn = sqlite3.connect("hiring_assistant.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO candidates (name, email, phone, experience, position, location, tech_stack)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, phone, experience, position, location, tech_stack))

    candidate_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return candidate_id

def insert_response(candidate_id, question, answer):
    conn = sqlite3.connect("hiring_assistant.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO responses (candidate_id, question, answer)
        VALUES (?, ?, ?)
    ''', (candidate_id, question, answer))

    conn.commit()
    conn.close()

# ---------- Fetch Functions ----------
def get_all_candidates():
    conn = sqlite3.connect("hiring_assistant.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidates")
    rows = cursor.fetchall()

def get_candidate_by_id(candidate_id):
    conn = sqlite3.connect("hiring_assistant.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
    row = cursor.fetchone()
    conn.close()
    return row

