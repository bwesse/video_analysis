from PIL import Image
import clip
import torch
import os
import sqlite3

def get_video_description(video_id):
    db_path = '../video_analysis.db'
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return None

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT description FROM Videos WHERE id = ?', (video_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        print(f"Found description for video_id {video_id}: {result[0]}")
        return result[0]
    else:
        print(f"No description found for video_id {video_id}")
        return None

def split_text(text, max_length=77):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        new_chunk = current_chunk + [word]
        tokenized_chunk = clip.tokenize(' '.join(new_chunk))[0]
        
        if len(tokenized_chunk) <= max_length:
            current_chunk = new_chunk
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}: {chunk}")

    return chunks

def analyze_keyframes_with_description(video_id, keyframes_dir):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    
    if video_id == 7:
        print(f"Skipping description for video_id {video_id} due to length issues.")
        keyframe_texts = ["description1", "description2"]
    else:
        description = get_video_description(video_id)
        if not description:
            return []

        description_chunks = split_text(description)
        keyframe_texts = description_chunks + ["description1", "description2"]
    
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

def process_specific_keyframes(video_id):
    keyframes_dir = '../data/keyframes/'
    analysis_results = analyze_keyframes_with_description(video_id, keyframes_dir)
    print(f"Analysis results for video ID {video_id}: {analysis_results}")

if __name__ == "__main__":
    # Replace with the specific video ID you want to test
    test_video_id = 18
    process_specific_keyframes(test_video_id)
