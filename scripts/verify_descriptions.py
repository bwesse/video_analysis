import sqlite3

def verify_descriptions():
    db_path = 'C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/video_analysis.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, description FROM Videos")
    videos = cursor.fetchall()
    
    for video_id, description in videos:
        print(f"Video ID: {video_id}, Description: {description}")
    
    conn.close()

if __name__ == "__main__":
    verify_descriptions()
