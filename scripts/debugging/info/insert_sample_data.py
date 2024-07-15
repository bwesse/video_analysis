import sqlite3
import os

def insert_sample_data():
    db_path = '../video_analysis.db'
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO Videos (path, description) VALUES (?, ?)', 
                   ('data/V3C1-100/00102/00102.mp4', 'Sample description'))
    conn.commit()
    conn.close()
    print("Sample data inserted.")

if __name__ == "__main__":
    insert_sample_data()
