import numpy as np
import torch
from PIL import Image
from scipy.spatial.distance import cosine
import  sqlite3
import clip

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

conn = sqlite3.connect('simon_polly\data1\SmallDatabase.db')
c = conn.cursor()

def fetch_all_embeddings():
    try:
        c.execute("SELECT id, image_embedding FROM keyframe_images")
        embeddings = c.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        embeddings = []
    return embeddings

def compute_and_store_similarities():
    embeddings = fetch_all_embeddings()
    num_embeddings = len(embeddings)
    try:
        for i in range(num_embeddings):
            for j in range(i+1, num_embeddings):  # Ensure each pair is processed only once
                id1, emb1 = embeddings[i][0], np.frombuffer(embeddings[i][1], dtype=np.float32)
                id2, emb2 = embeddings[j][0], np.frombuffer(embeddings[j][1], dtype=np.float32)
                similarity = 1 - cosine(emb1.flatten(), emb2.flatten())
                
                # Assuming you have a table `image_similarities` with columns `image_id1`, `image_id2`, and `similarity`
                c.execute("INSERT INTO image_similarities (image_id1, image_id2, similarity) VALUES (?, ?, ?)", (id1, id2, similarity))
        conn.commit()  # Commit after all insertions
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()  # Rollback in case of error

# Don't forget to call the function
compute_and_store_similarities()