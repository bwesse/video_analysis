import sqlite3

def create_database():
    conn = sqlite3.connect('../video_analysis.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Videos (
                      id INTEGER PRIMARY KEY,
                      path TEXT,
                      description TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Keyframes (
                      id INTEGER PRIMARY KEY,
                      video_id INTEGER,
                      frame_index INTEGER,
                      image BLOB,
                      analysis_results TEXT,
                      FOREIGN KEY(video_id) REFERENCES Videos(id))''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
