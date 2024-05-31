import os
import sys
import cv2
import numpy as np
import sqlite3
import tensorflow as tf
from PIL import Image
from efficientnet_pytorch import EfficientNet
import torch
from torchvision import transforms

# Add TransNetV2 directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../TransNetV2'))
from transnetv2 import TransNetV2

# Set up the database
def create_database():
    conn = sqlite3.connect('video_analysis.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS keyframes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_id TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        keyframe_path TEXT NOT NULL,
        analysis_data TEXT
    )
    ''')
    conn.commit()
    conn.close()

def extract_keyframes(video_path, output_dir, video_id):
    model = TransNetV2()
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    frames = np.array(frames)

    predictions = model.predict_frames(frames)
    shot_boundaries = np.where(predictions["predictions"][:, 1] > 0.5)[0]

    for timestamp in shot_boundaries:
        keyframe_path = os.path.join(output_dir, f"keyframe_{timestamp}.jpg")
        Image.fromarray(frames[timestamp]).save(keyframe_path)
        analyze_and_store_keyframe(keyframe_path, video_id, timestamp)

def analyze_and_store_keyframe(image_path, video_id, timestamp):
    model = EfficientNet.from_pretrained('efficientnet-b0')
    model.eval()
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_image = Image.open(image_path)
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)
    with torch.no_grad():
        output = model(input_batch)
    analysis_data = output.numpy().tolist()

    conn = sqlite3.connect('video_analysis.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO keyframes (video_id, timestamp, keyframe_path, analysis_data)
    VALUES (?, ?, ?, ?)
    ''', (video_id, timestamp, image_path, str(analysis_data)))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    video_path = 'data/V3C100/video1.mp4'
    output_dir = 'data/processed/keyframes'
    os.makedirs(output_dir, exist_ok=True)
    extract_keyframes(video_path, output_dir, 'video1')
