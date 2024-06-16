import os
import sqlite3

def create_database():
    #conn = sqlite3.connect('video_analysis.db')
    conn = sqlite3.connect('../src/backend/database_2.db')

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

def store_video_metadata(video_dir):
    conn = sqlite3.connect('../src/backend/database_2.db')
    cursor = conn.cursor()

    print(f"Walking through directory: {video_dir}")

    for root, _, files in os.walk(video_dir):
        print(f"Inspecting directory: {root}")
        for file in files:
            if file.endswith('.mp4'):
                video_path = os.path.join(root, file)
                description_path = video_path.replace('.mp4', '.description')
                print(f"Processing video: {video_path}")
                print(f"Looking for description: {description_path}")
                
                if os.path.exists(description_path):
                    with open(description_path, 'r', encoding='utf-8') as desc_file:
                        description = desc_file.read()
                    print(f"Description found: {description}")
                else:
                    print(f"Description not found for {video_path}")
                    description = "No description available"
                
                # Debug print statement to check insertion data
                print(f"Inserting video path: {video_path}, description: {description}")

                cursor.execute('INSERT INTO Videos (path, description) VALUES (?, ?)', (video_path, description))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    video_dir = '../data/V3C1-100/'
    create_database()
    store_video_metadata(video_dir)
    print("Metadata storage complete.")
