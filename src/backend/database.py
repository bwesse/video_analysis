import sqlite3

def create_database(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS keyframes
                 (id INTEGER PRIMARY KEY, video_id TEXT, frame_id INTEGER, analysis TEXT)''')
    conn.commit()
    conn.close()

def store_analysis(db_path, video_id, frame_id, analysis):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO keyframes (video_id, frame_id, analysis) VALUES (?, ?, ?)",
              (video_id, frame_id, analysis))
    conn.commit()
    conn.close()
