import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='torch.nn.functional')

from PIL import Image
import clip
import torch
import os
import sqlite3

def analyze_keyframes(video_id, keyframes_dir):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    
    keyframe_texts = ["description1", "description2"]  # Default text prompts for CLIP
    text = clip.tokenize(keyframe_texts).to(device)

    analysis_results = []
    for filename in os.listdir(keyframes_dir):
        if filename.endswith(f'{video_id}.jpg'):
            image_path = os.path.join(keyframes_dir, filename)
            image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
            with torch.no_grad():
                image_features = model.encode_image(image)
                text_features = model.encode_text(text)
                logits_per_image, logits_per_text = model(image, text)
                probs = logits_per_image.softmax(dim=-1).cpu().numpy()
                analysis_results.append((filename, probs))
    return analysis_results

def process_all_keyframes():
    keyframes_dir = 'C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/data/keyframes/'
    db_path = 'C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/video_analysis.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM Videos')
    video_ids = cursor.fetchall()

    for video_id in video_ids:
        video_id = video_id[0]
        analysis_results = analyze_keyframes(video_id, keyframes_dir)
        for filename, probs in analysis_results:
            frame_index = int(filename.split('_')[-1].split('.')[0])
            cursor.execute('INSERT OR REPLACE INTO Keyframes (video_id, frame_index, analysis_results) VALUES (?, ?, ?)', (video_id, frame_index, probs.tobytes()))
        conn.commit()
    conn.close()

if __name__ == "__main__":
    process_all_keyframes()
