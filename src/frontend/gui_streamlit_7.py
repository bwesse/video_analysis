import streamlit as st
import sqlite3
from PIL import Image
import os
import numpy as np
from streamlit_drawable_canvas import st_canvas
import torch
import clip
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize
import cv2
from quickdraw import QuickDrawDataGroup, QuickDrawData

# Ensure the script can find the database file
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'video_analysis.db'))

# Load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

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

def compute_clip_features(image):
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)
    return image_features.cpu().numpy()

def extract_frame_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    cap.release()
    if success:
        # Convert the frame (BGR to RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(frame)
    else:
        return None

def search_similar_videos(features):
    conn = load_database()
    cursor = conn.cursor()
    cursor.execute('SELECT id, path, description FROM Videos')
    videos = cursor.fetchall()
    
    similar_videos = []
    for video in videos:
        video_id, video_path, description = video
        # Extract a frame from the video
        video_image = extract_frame_from_video(video_path)
        if video_image is not None:
            video_features = compute_clip_features(video_image)
            similarity = np.dot(features, video_features.T).flatten()[0]
            similar_videos.append((video_id, similarity, description))
    
    similar_videos.sort(key=lambda x: x[1], reverse=True)  # Sort by similarity
    conn.close()
    return similar_videos

def quickdraw_guess(image):
    categories = ['cat', 'dog', 'house', 'tree', 'car', 'bicycle']  # Add categories as needed
    best_guess = None
    highest_score = -1
    for category in categories:
        qd = QuickDrawDataGroup(category)
        drawings = qd.drawings
        for drawing in drawings:
            drawing_image = drawing.get_image().convert("RGB").resize((224, 224))
            drawing_features = compute_clip_features(drawing_image)
            image_features = compute_clip_features(image)
            similarity = np.dot(image_features, drawing_features.T).flatten()[0]
            if similarity > highest_score:
                best_guess = category
                highest_score = similarity
    return best_guess

st.title("Video Search System")

# Drawing canvas section
st.subheader("Draw and Search")
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=2,
    stroke_color="#000",
    background_color="#FFF",
    update_streamlit=True,
    height=150,
    width=150,
    drawing_mode="freedraw",
    key="canvas"
)

if canvas_result.image_data is not None:
    image = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert("RGB")
    image = image.resize((224, 224))
    
    # Guess what the drawing is using Quick, Draw!
    guess = quickdraw_guess(image)
    st.write(f"Quick, Draw! guess: **{guess}**")
    
    if st.button("Use this guess for video search"):
        # Use the guessed label to search for similar videos
        video_results = search_videos_by_description(guess)
        if video_results:
            st.write(f"Found {len(video_results)} result(s) for '{guess}':")
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
            st.write(f"No results found for '{guess}'.")

st.title("Text Search for Videos")
query = st.text_input("Search for video content or description:")
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

    video_id = st.selectbox("Select Video ID for Playback", [video[0] for video in video_results])
    if video_id:
        video_path = get_video_path(video_id)
        st.video(video_path)
        st.write(f"**Description:** {get_video_description(video_id)}")
