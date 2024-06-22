import numpy as np
import sqlite3
import torch
import clip
from PIL import Image
import torch.nn as nn

def find_text_similarity(target_vector2, all_keyframes, device, preprocess, model, top_n=5):
    similarities = []
    text_features = target_vector2
    for id, frame_index, text_embedding, _ in all_keyframes:
        try:
            with torch.no_grad():
                image_preprocess = preprocess(Image.open(text_embedding)).unsqueeze(0).to(device)
                image_features = model.encode_image( image_preprocess)
                sim = nn.CosineSimilarity(image_features[0],text_features[0]).item()
                sim = (sim+1)/2
                similarities[text_embedding]=sim
        except Exception as e:
                print(f"Error processing keyframe {id}_{frame_index}: {e}")
    similarities.sort(key=lambda x: x[2], reverse=True)
    return similarities[:top_n]

def process_uploaded_image(uploaded_file, model, preprocess, device):
    image = Image.open(uploaded_file).convert("RGB")
    image_tensor = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_tensor)
        image_features = image_features.cpu().numpy()
    return image_features

def process_text_input(text_input, model, device):
    text = clip.tokenize([text_input]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text)
        text_features = text_features.cpu().numpy()
    return text_features

def load_clip_model():
    """
    Load the CLIP model and preprocessing function.
    
    Returns:
    model, preprocess: The CLIP model and preprocessing function.
    """

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess

def get_all_keyframes(db_path):
    """
    Retrieve all keyframes from the database.
    
    Parameters:
    db_path (str): The path to the database file.
    
    Returns:
    list: List of tuples containing (video_id, frame_index, analysis_results).
    """
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, frame_index, image_embedding, text_embedding FROM Keyframes")
    keyframes = cursor.fetchall()
    conn.close()
    return keyframes