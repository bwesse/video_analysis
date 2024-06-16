import sqlite3
import os
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

def create_database():
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
                      timestamp TEXT,
                      image BLOB,
                      path TEXT,
                      description TEXT,
                      analysis_results TEXT,
                      FOREIGN KEY(video_id) REFERENCES Videos(id))''')
    conn.commit()
    conn.close()

def generate_image_description(image_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

    raw_image = Image.open(image_path).convert("RGB")
    inputs = processor(raw_image, return_tensors="pt").to(device)

    out = model.generate(**inputs, max_new_tokens=100)  # Adjust max_new_tokens for longer descriptions
    description = processor.decode(out[0], skip_special_tokens=True)
    return description

def update_single_keyframe_description():
    conn = sqlite3.connect('../src/backend/database_2.db')
    cursor = conn.cursor()

    # Select one keyframe
    cursor.execute("SELECT id, path FROM Keyframes LIMIT 1")
    keyframe = cursor.fetchone()

    if keyframe:
        keyframe_id, image_path = keyframe
        if os.path.exists(image_path):
            try:
                description = generate_image_description(image_path)
                cursor.execute("UPDATE Keyframes SET description = ? WHERE id = ?", (description, keyframe_id))
                conn.commit()
                print(f"Updated keyframe {keyframe_id} with description: {description}")
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
        else:
            print(f"Image path {image_path} does not exist.")

    conn.close()

if __name__ == "__main__":
    create_database()  # Ensure the database and tables are created
    update_single_keyframe_description()
