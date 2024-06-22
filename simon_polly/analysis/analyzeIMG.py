import torch
import clip
from PIL import Image
import numpy as np
import sqlite3

# Step 1: Setup
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Step 2: Database connection
conn = sqlite3.connect('simon_polly\data1\database_2.db')
c = conn.cursor()
# Ensure table exists
#c.execute('''CREATE TABLE IF NOT EXISTS image_embedding (id INTEGER PRIMARY KEY, embedding BLOB)''')

# Assuming there's a table named 'images' with columns 'id' and 'image_path'
def fetch_and_process_images():
    # Fetch all image paths from the database
    c.execute("SELECT id, path FROM Keyframes")
    images = c.fetchall()

    for image_id, image_path in images:
        try:
            image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
            with torch.no_grad():
                image_features = model.encode_image(image)
                image_features = image_features.cpu().numpy()

            # Store embeddings
            c.execute("UPDATE Keyframes SET image_embedding = ? WHERE id = ?", (image_features.tobytes(), image_id))
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")

    conn.commit()

# Call the function to process and store embeddings
fetch_and_process_images()

# Cleanup
conn.close()