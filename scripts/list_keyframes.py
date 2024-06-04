import sqlite3
import os

def list_keyframes():
    db_path = 'C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/video_analysis.db'
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    print(f"Connecting to database at {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT video_id, frame_index, analysis_results FROM Keyframes')
    results = cursor.fetchall()
    conn.close()

    if not results:
        print("No records found in the Keyframes table.")
        return

    print(f"Found {len(results)} records in the Keyframes table.")
    for video_id, frame_index, analysis_results in results:
        print(f"Video ID: {video_id}, Frame Index: {frame_index}, Analysis Results: {analysis_results}")

if __name__ == "__main__":
    list_keyframes()
