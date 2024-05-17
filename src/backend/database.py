import sqlite3

def create_database():
    conn = sqlite3.connect('data/video_analysis.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS keyframes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_id TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        keyframe_path TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analysis_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyframe_id INTEGER NOT NULL,
        analysis_data TEXT NOT NULL,
        FOREIGN KEY (keyframe_id) REFERENCES keyframes (id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
