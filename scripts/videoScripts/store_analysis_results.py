import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.analysis.analyzeAll import fetch_and_process_images
import sqlite3

def create_database():
    db_path = '../video_analysis.db'
    conn = sqlite3.connect(db_path)
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

def store_analysis_results(video_id, keyframes_dir, analysis_results):
    db_path = '../video_analysis.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Storing analysis results for video_id {video_id}")
    for filename, analysis in analysis_results:
        frame_index = int(filename.split('_')[-1].split('.')[0])
        image_path = os.path.join(keyframes_dir, filename)
        with open(image_path, 'rb') as file:
            image_data = file.read()
        cursor.execute('INSERT INTO Keyframes (video_id, frame_index, image, analysis_results) VALUES (?, ?, ?, ?)',
                       (video_id, frame_index, image_data, str(analysis)))
    
    conn.commit()
    conn.close()
    print("Analysis results stored.")

if __name__ == "__main__":
    video_id = 1  # Ensure this video ID exists in your Videos table
    keyframes_dir = '../data/keyframes/'
    analysis_results = fetch_and_process_images(video_id, keyframes_dir)
    store_analysis_results(video_id, keyframes_dir, analysis_results)
