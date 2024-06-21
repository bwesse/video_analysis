import torch
import clip
from PIL import Image
import numpy as np
import sqlite3

# Step 1: Setup
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Step 2: Database connection
conn = sqlite3.connect('simon_polly\data1\SmallDatabase.db')
c = conn.cursor()
# Ensure table exists
#c.execute('''CREATE TABLE IF NOT EXISTS image_embedding (id INTEGER PRIMARY KEY, embedding BLOB)''')

# Assuming there's a table named 'images' with columns 'id' and 'image_path'
def fetch_and_process_images():
    # Fetch all image paths and text descriptions from the database
    c.execute("SELECT id, path, description FROM keyframe_images")
    records = c.fetchall()

    for record in records:
        image_id, image_path, text_description = record
        try:
            # Process image
            image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
            with torch.no_grad():
                image_features = model.encode_image(image)
                image_features = image_features.cpu().numpy()

            # Process text
            text = clip.tokenize([text_description]).to(device)
            with torch.no_grad():
                text_features = model.encode_text(text)
                text_features = text_features.cpu().numpy()

            # Store embeddings
            c.execute("UPDATE keyframe_images SET image_embedding = ?, text_embedding = ? WHERE id = ?", 
                      (image_features.tobytes(), text_features.tobytes(), image_id))
        except Exception as e:
            print(f"Error processing record {image_id}: {e}")

    conn.commit()

# Call the function to process and store embeddings
fetch_and_process_images()

# Cleanup
conn.close()