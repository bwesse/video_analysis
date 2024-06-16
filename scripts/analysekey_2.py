import sqlite3
import torch
import clip
from PIL import Image
import numpy as np

def analyze_and_store_image_from_db():
    # Connect to the database
    conn = sqlite3.connect('../src/backend/database_2.db')
    cursor = conn.cursor()
    
    # Retrieve one image path and description from the database
    cursor.execute('SELECT id, path, description FROM Keyframes WHERE analysis_results IS NULL LIMIT 1')
    row = cursor.fetchone()
    
    if row is None:
        print("No images to analyze")
        return

    keyframe_id, image_path, description = row
    
    # Load the model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    
    # Load and preprocess the image
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    
    # Generate image embedding
    with torch.no_grad():
        image_embedding = model.encode_image(image).cpu().numpy()

    # Generate text embedding
    text = clip.tokenize([description]).to(device)
    with torch.no_grad():
        text_embedding = model.encode_text(text).cpu().numpy()

    # Concatenate image and text embeddings
    concatenated_embedding = np.concatenate((image_embedding, text_embedding), axis=1)
    
    # Convert the concatenated embedding to binary format
    concatenated_embedding_blob = concatenated_embedding.tobytes()
    
    # Update the database with the analysis results
    cursor.execute('''
        UPDATE Keyframes
        SET analysis_results = ?
        WHERE id = ?
    ''', (concatenated_embedding_blob, keyframe_id))
    
    conn.commit()
    conn.close()

    print(f"Analyzed and updated keyframe {keyframe_id}")

def main():
    while True:
        analyze_and_store_image_from_db()
        user_input = input("Do you want to analyze another image? (yes/no): ").strip().lower()
        if user_input != 'yes':
            break

if __name__ == "__main__":
    main()
