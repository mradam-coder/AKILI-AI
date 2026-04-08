import sqlite3

input_db = "akili_ai.db"
output_db = "akili_ai_recovered.db"

try:
    # Connect to the corrupted DB
    conn_in = sqlite3.connect(input_db)
    # Create a new DB
    conn_out = sqlite3.connect(output_db)

    # Backup (copies as much as possible)
    with conn_out:
        conn_in.backup(conn_out)

    print(f"Backup successful! Recovered DB: {output_db}")
except sqlite3.DatabaseError as e:
    print("Database error during backup:", e)
finally:
    conn_in.close()
    conn_out.close()