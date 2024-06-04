import sqlite3
import os

def list_video_ids():
    db_path = 'C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/video_analysis.db'
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    print(f"Connecting to database at {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id, description FROM Videos')
    results = cursor.fetchall()
    conn.close()

    if not results:
        print("No records found in the Videos table.")
        return

    print(f"Found {len(results)} records in the Videos table.")
    for video_id, description in results:
        print(f"Video ID: {video_id}, Description: {description}")

if __name__ == "__main__":
    list_video_ids()
