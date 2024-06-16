import sqlite3
import os
import torch
import clip
from PIL import Image
import numpy as np
from tqdm import tqdm

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
                      environment TEXT,
                      subjects TEXT,
                      dominant_color TEXT,
                      combined_embedding BLOB,
                      FOREIGN KEY(video_id) REFERENCES Videos(id))''')
    conn.commit()
    conn.close()

def fetch_keyframes_from_db():
    conn = sqlite3.connect('../src/backend/database_2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, path, description FROM Keyframes WHERE description IS NOT NULL")
    keyframes = cursor.fetchall()
    conn.close()
    return keyframes

def generate_clip_embeddings(image_path, description, model, preprocess, device):
    # Load and preprocess image
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    
    # Tokenize description
    text = clip.tokenize([description]).to(device)
    
    # Generate embeddings
    with torch.no_grad():
        image_embedding = model.encode_image(image).cpu().numpy()
        text_embedding = model.encode_text(text).cpu().numpy()
    
    # Combine embeddings by concatenation
    combined_embedding = np.concatenate((image_embedding, text_embedding), axis=1)
    
    return combined_embedding

def store_embeddings_to_db(keyframe_id, combined_embedding):
    conn = sqlite3.connect('../src/backend/database_2.db')
    cursor = conn.cursor()
    cursor.execute("""UPDATE Keyframes 
                      SET combined_embedding = ? 
                      WHERE id = ?""",
                   (combined_embedding.tobytes(), keyframe_id))
    conn.commit()
    conn.close()

def main():
    # Ensure the database and tables are created
    create_database()

    # Load CLIP model and preprocessing
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    
    # Fetch keyframes from database
    keyframes = fetch_keyframes_from_db()

    for keyframe in tqdm(keyframes, desc="Processing Keyframes"):
        keyframe_id, image_path, description = keyframe
        
        if os.path.exists(image_path):
            try:
                combined_embedding = generate_clip_embeddings(image_path, description, model, preprocess, device)
                store_embeddings_to_db(keyframe_id, combined_embedding)
                print(f"Updated keyframe {keyframe_id} with combined embedding.")
            except Exception as e:
                print(f"Error processing {image_path} for keyframe {keyframe_id}: {e}")
        else:
            print(f"Image path {image_path} does not exist for keyframe {keyframe_id}.")

if __name__ == "__main__":
    main()
