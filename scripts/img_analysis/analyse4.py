import sqlite3
import pandas as pd
import clip
import torch
from PIL import Image
import os

# Define the database path relative to the script's location
database_path = os.path.join(os.path.dirname(__file__), '../../src/backend/database_2.db')

# Function to check if the database file exists
def check_database_path(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The database file at {path} was not found.")
    return path

# Connect to your database
conn = sqlite3.connect(check_database_path(database_path))

# Load data into a DataFrame
query = "SELECT id, path, description FROM Keyframes LIMIT 5"  # Limit to 5 test images
df = pd.read_sql_query(query, conn)

# Load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Function to create image and text embeddings
def create_embeddings(image_path, description):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    text = clip.tokenize([description]).to(device)
    
    with torch.no_grad():
        image_embedding = model.encode_image(image)
        text_embedding = model.encode_text(text)
    
    return image_embedding, text_embedding

# Function to update database with embeddings
def update_database(ids, image_embeddings, combined_embeddings):
    for id, img_emb, comb_emb in zip(ids, image_embeddings, combined_embeddings):
        img_emb_blob = img_emb.cpu().numpy().tobytes()
        comb_emb_blob = comb_emb.cpu().numpy().tobytes()
        
        query = """
        UPDATE Keyframes
        SET image_embed = ?, combined_embedding = ?
        WHERE id = ?
        """
        conn.execute(query, (img_emb_blob, comb_emb_blob, id))
    conn.commit()

def main():
    # Initialize lists to store embeddings
    image_embeddings = []
    combined_embeddings = []
    ids = []

    # Iterate over the data and create embeddings
    for index, row in df.iterrows():
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), row['path']))
        image_embedding, text_embedding = create_embeddings(image_path, row['description'])
        combined_embedding = torch.cat((image_embedding, text_embedding), dim=1)  # Concatenating image and text embeddings
        
        image_embeddings.append(image_embedding)
        combined_embeddings.append(combined_embedding)
        ids.append(row['id'])

    # Convert lists to tensors
    image_embeddings = torch.cat(image_embeddings)
    combined_embeddings = torch.cat(combined_embeddings)

    # Update the database with the embeddings
    update_database(ids, image_embeddings, combined_embeddings)

    print("Embeddings for test images have been successfully stored in the database.")

if __name__ == "__main__":
    main()
    conn.close()
