import streamlit as st
import sqlite3
from PIL import Image
import os
import numpy as np
import torch
import clip
from SimilaritySearch import    cosine_similarity, find_image_similarity, get_all_keyframes, process_uploaded_image, process_text_input, find_text_similarity, load_clip_model

# Ensure the script can find the database file
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'simon_polly\data1\database_new.db'))

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
    keyframe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','simon_polly', 'data1', 'processed', 'keyframes', f'keyframe_{video_id}_{frame_index}.jpg'))
    return keyframe_path

st.title("Video Search and Analysis System")

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
            
            keyframe_results = get_keyframes(video_id)
            if keyframe_results:
                for frame_index, analysis_results in keyframe_results:
                    frame_path = get_keyframe_image(video_id, frame_index)
                    if os.path.exists(frame_path):
                        analysis_results = np.frombuffer(analysis_results, dtype=np.float16)
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

st.title("Find Similar Keyframes")

uploaded_file = st.file_uploader("Upload a keyframe image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Keyframe", use_column_width=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    target_vector1 = process_uploaded_image(uploaded_file, model, preprocess, device)
    all_keyframes = get_all_keyframes(db_path)
    similar_keyframes = find_image_similarity(target_vector1, all_keyframes, device)

    st.write("Top similar keyframes:")
    for vid, idx, sim in similar_keyframes:
        frame_path = get_keyframe_image(vid, idx)
        if os.path.exists(frame_path):
            st.image(frame_path, caption=f"ID: {vid}, Frame Index: {idx}, Similarity: {sim:.4f}")
        else:
            st.write(f"Keyframe image {idx} for video_id {vid} not found at path: {frame_path}")

st.title("Search Keyframes by Text Description")

text_input = st.text_input("Enter a text description to find similar keyframes:")
if text_input:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    target_vector2 = process_text_input(text_input, model, device)
    all_keyframes = get_all_keyframes(db_path)
    similar_keyframes = find_text_similarity(target_vector2, all_keyframes, device, top_n=5)

    st.write("Top similar keyframes:")
    for vid, idx, sim in similar_keyframes:
        frame_path = get_keyframe_image(vid, idx)
        if os.path.exists(frame_path):
            st.image(frame_path, caption=f"ID: {vid}, Frame Index: {idx}, Similarity: {sim:.4f}")
        else:
            st.write(f"Keyframe image {idx} for video_id {vid} not found at path: {frame_path}")

st.write("""
Welcome to our **Video Search and Analysis System**. This platform allows you to search for video content based on descriptions, view keyframes, and find similar keyframes using state-of-the-art image analysis. Our system is designed to be user-friendly, professional, and minimalistic, ensuring you can efficiently find the content you need. Learn more about this project at [our GitHub](https://github.com/bwesse/VP.git).

### Features

1. **Search Videos by Description**:
   - Enter keywords or phrases related to the video content.
   - View a list of matching videos along with their descriptions.
   - Display keyframes from the selected video to get a visual summary of the content.

2. **Video Playback**:
   - Select a video from the search results for playback.
   - View video descriptions and watch the video directly within the platform.

3. **Find Similar Keyframes**:
   - Upload an image of a keyframe.
   - The system processes the image to find and display keyframes from the database that are visually similar.
   - This is particularly useful for identifying similar scenes or objects across different videos.

4. **Search Keyframes by Text Description**:
   - Enter a text description to find similar keyframes.
   - The system processes the text to find and display keyframes from the database that match the description.

Our platform is designed with a clean and minimalistic approach:
   - **Simple Navigation**: Easily access different features with intuitive navigation.
   - **Clear Layout**: Information is presented in a clear, concise manner to avoid clutter.
   - **Professional Aesthetic**: A polished look with professional styling ensures a pleasant user experience.

### Example Usage

1. **Searching for Videos**:
   - Enter "sunset" in the search bar.
   - Review the results and select a video ID to watch a video about sunsets.

2. **Finding Similar Keyframes**:
   - Upload an image of a beach scene.
   - View similar keyframes from various videos that also feature beach scenes.

3. **Searching Keyframes by Text Description**:
   - Enter "a cat sitting on a sofa."
   - View keyframes from the database that match this description.

By following these steps, you can leverage the full capabilities of our Video Search and Analysis System. Enjoy exploring and discovering new content efficiently!
""")
