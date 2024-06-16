# similarity_utils.py

import numpy as np

def cosine_similarity(v1, v2):
    """
    Compute the cosine similarity between two vectors.
    
    Parameters:
    v1 (numpy.ndarray): First vector.
    v2 (numpy.ndarray): Second vector.
    
    Returns:
    float: Cosine similarity between v1 and v2.
    """
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return dot_product / (norm_v1 * norm_v2)

def find_similar_keyframes(target_vector, all_keyframes, top_n=5):
    """
    Find the top N similar keyframes to the target vector using cosine similarity.
    
    Parameters:
    target_vector (numpy.ndarray): The target vector to compare against.
    all_keyframes (list): List of tuples containing (video_id, frame_index, analysis_results).
    top_n (int): The number of top similar keyframes to return.
    
    Returns:
    list: List of tuples containing (video_id, frame_index, similarity).
    """
    similarities = []
    for video_id, frame_index, analysis_results in all_keyframes:
        if analysis_results:
            try:
                vector = np.frombuffer(analysis_results, dtype=np.float32)
                similarity = cosine_similarity(target_vector, vector)
                similarities.append((video_id, frame_index, similarity))
            except Exception as e:
                print(f"Error processing keyframe {video_id}_{frame_index}: {e}")
        else:
            print(f"Analysis results for keyframe {video_id}_{frame_index} are empty or None.")
    similarities.sort(key=lambda x: x[2], reverse=True)
    return similarities[:top_n]

def process_uploaded_image(uploaded_file, model, preprocess, device):
    """
    Process an uploaded image file and generate its CLIP embedding.
    
    Parameters:
    uploaded_file: The uploaded image file.
    model: The CLIP model.
    preprocess: The CLIP preprocessing function.
    device (str): The device to run the model on.
    
    Returns:
    numpy.ndarray: The image embedding.
    """
    from PIL import Image
    image = Image.open(uploaded_file).convert("RGB")
    image_tensor = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_tensor).cpu().numpy()
    return image_features

def process_text_input(text_input, model, device):
    """
    Process a text input and generate its CLIP embedding.
    
    Parameters:
    text_input (str): The text input.
    model: The CLIP model.
    device (str): The device to run the model on.
    
    Returns:
    numpy.ndarray: The text embedding.
    """
    import clip
    text_tokens = clip.tokenize([text_input]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text_tokens).cpu().numpy()
    return text_features

def load_clip_model():
    """
    Load the CLIP model and preprocessing function.
    
    Returns:
    model, preprocess: The CLIP model and preprocessing function.
    """
    import torch
    import clip
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
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT video_id, frame_index, analysis_results FROM Keyframes')
    keyframes = cursor.fetchall()
    conn.close()
    return keyframes
