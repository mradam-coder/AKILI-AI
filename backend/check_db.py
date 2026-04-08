import sqlite3

db_file = "akili_ai.db"

try:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("PRAGMA integrity_check;")
    result = cursor.fetchone()
    print("Integrity check result:", result[0])
    conn.close()
except sqlite3.DatabaseError as e:
    print("Database error:", e)