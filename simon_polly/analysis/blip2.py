import sqlite3
import os
from PIL import Image
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration

# Initialize model and processor once
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b").to(device)
model.eval()  # Set the model to evaluation mode

def generate_image_description(image_path):
    raw_image = Image.open(image_path).convert("RGB")
    inputs = processor(raw_image, return_tensors="pt").to(device)

    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=100)
    description = processor.decode(out[0], skip_special_tokens=True)
    return description

def update_all_keyframe_descriptions():
    conn = sqlite3.connect('simon_polly\data1\database_new.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, path FROM Keyframes WHERE description2 IS NULL OR description = ''")
    keyframes = cursor.fetchall()

    for keyframe in keyframes:
        keyframe_id, image_path = keyframe
        if os.path.exists(image_path):
            try:
                description = generate_image_description(image_path)
                cursor.execute("UPDATE Keyframes SET description2 = ? WHERE id = ?", (description, keyframe_id))
                conn.commit()
                print(f"Updated keyframe {keyframe_id} with description: {description}")
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
        else:
            print(f"Image path {image_path} does not exist.")

    conn.close()

if __name__ == "__main__":
    update_all_keyframe_descriptions()