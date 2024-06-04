import sqlite3
import numpy as np

def verify_keyframe_analysis(video_id):
    db_path = 'C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/video_analysis.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT video_id, frame_index, analysis_results FROM Keyframes WHERE video_id = ?", (video_id,))
    keyframes = cursor.fetchall()
    
    for video_id, frame_index, analysis in keyframes:
        analysis_results = np.frombuffer(analysis, dtype=np.float32)
        print(f"Video ID: {video_id}, Frame Index: {frame_index}, Analysis Results: {analysis_results}")
    
    conn.close()

if __name__ == "__main__":
    video_id = int(input("Enter the video ID to verify: "))
    verify_keyframe_analysis(video_id)
