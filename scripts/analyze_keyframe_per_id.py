import warnings
import logging
from PIL import Image
import clip
import torch
import os
import sqlite3
import numpy as np

warnings.filterwarnings("ignore", category=UserWarning, module='torch.nn.functional')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_keyframes(video_id, keyframes_dir):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    analysis_results = []
    for filename in os.listdir(keyframes_dir):
        if filename.startswith(f'keyframe_{video_id}_') and filename.endswith('.jpg'):
            image_path = os.path.join(keyframes_dir, filename)
            image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
            with torch.no_grad():
                image_features = model.encode_image(image).cpu().numpy()
                analysis_results.append((filename, image_features))
                logging.info(f"Analyzed keyframe: {filename}")
    return analysis_results

def process_keyframes_for_video(video_id):
    keyframes_dir = '../data/keyframes/'
    db_path = '../video_analysis.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    analysis_results = analyze_keyframes(video_id, keyframes_dir)
    for filename, image_features in analysis_results:
        frame_index = int(filename.split('_')[-1].split('.')[0])
        cursor.execute('INSERT OR REPLACE INTO Keyframes (video_id, frame_index, analysis_results) VALUES (?, ?, ?)', 
                       (video_id, frame_index, sqlite3.Binary(image_features.tobytes())))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    video_id = int(input("Enter the video ID to process: "))
    process_keyframes_for_video(video_id)
