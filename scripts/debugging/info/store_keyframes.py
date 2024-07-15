import sqlite3
import os
from PIL import Image
import io

def create_database():
    conn = sqlite3.connect('simon_polly\data1\database_new.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Videos (
                      #id INTEGER PRIMARY KEY,
                      #path TEXT,
                      #description TEXT)''')
    
    # Drop the Keyframes table if it exists
    cursor.execute('DROP TABLE IF EXISTS Keyframes')
    
    cursor.execute('''CREATE TABLE Keyframes (
                      id INTEGER PRIMARY KEY,
                      video_id INTEGER,
                      frame_index INTEGER,
                      timestamp TEXT,
                      image BLOB,
                      path TEXT,
                      description TEXT,
                      image_embedding TEXT,
                        text_embedding TEXT,
                      FOREIGN KEY(video_id) REFERENCES Videos(id))''')
    conn.commit()
    conn.close()

def insert_keyframe(video_id, frame_index, image_path):
    conn = sqlite3.connect('simon_polly\data1\database_new.db')
    cursor = conn.cursor()

    # Open the image and resize it
    with Image.open(image_path) as img:
        img = img.resize((100, 100))  # Resize the image to 100x100 pixels
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        image_blob = img_byte_arr.getvalue()
    
    cursor.execute('''INSERT INTO Keyframes (video_id, frame_index, image, path)
                      VALUES (?, ?, ?, ?)''', (video_id, frame_index, image_blob, image_path))
    conn.commit()
    conn.close()

def parse_keyframe_info(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    parts = name.split('_')
    if len(parts) == 3 and parts[0] == 'keyframe':
        try:
            video_id = int(parts[1]) if parts[1].isdigit() else None
            frame_index = int(parts[2])
            return video_id, frame_index
        except ValueError:
            raise ValueError(f"Error parsing video ID or frame index from {base_name}")
    else:
        raise ValueError(f"Filename {base_name} does not match the expected format 'keyframe_<video_id>_<frame_index>.jpg'")

if __name__ == "__main__":
    create_database()
    
    # Replace with your actual directory path containing keyframes
    keyframe_directory = r'simon_polly/data1/processed/keyframes'
    
    for filename in os.listdir(keyframe_directory):
        if filename.endswith('.jpg'):
            file_path = os.path.join(keyframe_directory, filename)
            try:
                video_id, frame_index = parse_keyframe_info(file_path)
                if video_id is not None:
                    print(f"Processing {filename}: video_id={video_id}, frame_index={frame_index}")  # Debugging statement
                    insert_keyframe(video_id, frame_index, file_path)
                else:
                    print(f"Skipping {filename}: No valid video_id")  # Debugging statement for skipped files
            except ValueError as e:
                print(e)
