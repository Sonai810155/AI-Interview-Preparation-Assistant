import sqlite3

def create_table():
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT,
            question TEXT,
            answer TEXT,
            feedback TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_interview(domain, question, answer, feedback):
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO interview_history (domain, question, answer, feedback)
        VALUES (?, ?, ?, ?)
    """, (domain, question, answer, feedback))

    conn.commit()
    conn.close()
def get_history():
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    cursor.execute("SELECT domain, question, answer, feedback FROM interview_history")

    data = cursor.fetchall()

    conn.close()
    return data