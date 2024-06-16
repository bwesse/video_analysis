import sqlite3
import os

def check_database_connection():
    db_path = '../video_analysis.db'
    if os.path.exists(db_path):
        print(f"Database found at {db_path}")
    else:
        print(f"Database not found at {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
    tables = cursor.fetchall()
    conn.close()
    print(f"Tables in the database: {tables}")

if __name__ == "__main__":
    check_database_connection()
