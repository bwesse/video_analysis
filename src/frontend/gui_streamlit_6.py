import streamlit as st
import sqlite3
from PIL import Image
import os
import numpy as np
import torch
import clip
from similarity_utils import cosine_similarity

# Ensure the script can find the database file
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'video_analysis.db'))

def load_database():
    conn = sqlite3.connect(db_path)
    return conn

def search_videos_by_description(query):
    conn = load_database()
    cursor = conn.cursor()
    cursor.execute('SELECT id, description FROM Videos WHERE description LIKE ?', ('%' + query + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

def get_video_path(video_id):
    conn = load_database()
    cursor = conn.cursor()
    cursor.execute('SELECT path FROM Videos WHERE id = ?', (video_id,))
    relative_path = cursor.fetchone()[0]
    conn.close()
    # Construct the absolute path
    video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', relative_path))
    return video_path

def get_video_description(video_id):
    conn = load_database()
    cursor = conn.cursor()
    cursor.execute('SELECT description FROM Videos WHERE id = ?', (video_id,))
    description = cursor.fetchone()[0]
    conn.close()
    return description

def get_keyframes(video_id):
    conn = load_database()
    cursor = conn.cursor()
    cursor.execute('SELECT frame_index, analysis_results FROM Keyframes WHERE video_id = ?', (video_id,))
    keyframes = cursor.fetchall()
    conn.close()
    return keyframes

def get_keyframe_image(video_id, frame_index):
    keyframe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'keyframes', f'keyframe_{video_id}_{frame_index}.jpg'))
    return keyframe_path

def get_all_keyframes():
    conn = load_database()
    cursor = conn.cursor()
    cursor.execute('SELECT video_id, frame_index, analysis_results FROM Keyframes')
    keyframes = cursor.fetchall()
    conn.close()
    return keyframes

def find_similar_keyframes(target_vector, all_keyframes, top_n=5):
    similarities = []
    for video_id, frame_index, analysis_results in all_keyframes:
        vector = np.frombuffer(analysis_results, dtype=np.float32)
        similarity = cosine_similarity(target_vector, vector)
        similarities.append((video_id, frame_index, similarity))
    similarities.sort(key=lambda x: x[2], reverse=True)
    return similarities[:top_n]

def process_uploaded_image(uploaded_file):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    
    image = Image.open(uploaded_file).convert("RGB")
    image_tensor = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_tensor).cpu().numpy()
    return image_features

st.title("Video Search System")

# Video search section
query = st.text_input("Search for video content or description:")
video_results = []
if query:
    video_results = search_videos_by_description(query)
    if video_results:
        st.write(f"Found {len(video_results)} result(s) for '{query}':")
        for video in video_results:
            video_id = video[0]
            description = video[1]
            st.write(f"**Video ID:** {video_id}")
            st.write(f"**Description:** {description}")
            
            # Fetch and display keyframes
            keyframe_results = get_keyframes(video_id)
            if keyframe_results:
                for frame_index, analysis_results in keyframe_results:
                    frame_path = get_keyframe_image(video_id, frame_index)
                    if os.path.exists(frame_path):
                        analysis_results = np.frombuffer(analysis_results, dtype=np.float32)
                        st.image(frame_path, caption=f"Keyframe {frame_index} - Analysis: {analysis_results}")
                    else:
                        st.write(f"Keyframe image {frame_index} not found at path: {frame_path}")
            else:
                st.write("No keyframes found for this video.")
    else:
        st.write(f"No results found for '{query}'.")

    st.title("Video Playback")
    video_id = st.selectbox("Select Video ID for Playback", [video[0] for video in video_results])
    if video_id:
        video_path = get_video_path(video_id)
        st.video(video_path)
        st.write(f"**Description:** {get_video_description(video_id)}")

# Similarity search section
st.title("Find Similar Keyframes")

uploaded_file = st.file_uploader("Upload a keyframe image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Keyframe", use_column_width=True)
    target_vector = process_uploaded_image(uploaded_file)
    all_keyframes = get_all_keyframes()
    similar_keyframes = find_similar_keyframes(target_vector, all_keyframes)

    st.write("Top similar keyframes:")
    for vid, idx, sim in similar_keyframes:
        frame_path = get_keyframe_image(vid, idx)
        if os.path.exists(frame_path):
            st.image(frame_path, caption=f"Video ID: {vid}, Frame Index: {idx}, Similarity: {sim:.4f}")
        else:
            st.write(f"Keyframe image {idx} for video {vid} not found at path: {frame_path}")
