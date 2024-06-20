#!/usr/bin/env python3

import torch
import clip
from PIL import Image
import pandas as pd
import numpy as np
import sqlite3
import os

def main():
    # Load the model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    # Connect to the SQLite database
    db_path = r'C:\Users\benwe\Desktop\desktop\Uni\S4\videoAnalysis\src\backend\database_2.db'  # Update this with your actual database file path
    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
        return

    # Load the data from the database
    query = "SELECT id, path, description FROM your_table_name"  # Update your_table_name
    data = pd.read_sql_query(query, conn)

    # Function to get embeddings
    def get_embeddings(image_path, text):
        # Load and preprocess the image
        image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
        
        # Tokenize the text
        text = clip.tokenize([text]).to(device)
        
        # Get the embeddings
        with torch.no_grad():
            image_features = model.encode_image(image)
            text_features = model.encode_text(text)
        
        # Normalize the embeddings
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        
        # Concatenate the embeddings
        combined_embedding = torch.cat((image_features, text_features), dim=-1)
        return combined_embedding.cpu().numpy()

    # Apply the function to each row in the dataframe
    embeddings = []
    for index, row in data.iterrows():
        image_path = row['path']
        description = row['description']
        if os.path.exists(image_path):
            embedding = get_embeddings(image_path, description)
            embeddings.append((embedding.tobytes(), row['id']))

    # Save embeddings back to the database
    with conn:
        conn.executemany("UPDATE your_table_name SET combined_embedding = ? WHERE id = ?", embeddings)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
