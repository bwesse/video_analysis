import sqlite3

def verify_video_id(video_id):
    conn = sqlite3.connect('../video_analysis.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, description FROM Videos WHERE id = ?', (video_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        print(f"Video ID {video_id} exists with description: {result[1]}")
    else:
        print(f"Video ID {video_id} does not exist in the database.")

if __name__ == "__main__":
    video_id = 3  # Example video ID
    verify_video_id(video_id)
