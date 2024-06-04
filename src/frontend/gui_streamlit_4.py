# src/frontend/streamlit_app.py
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
from scripts.extract_keyframes import extract_keyframes
from scripts.transcode_video import transcode_video
from scripts.transnet_scene_detection import detect_scenes
from scripts.analyze_content import analyze_with_clip
import clip
import torch
from PIL import Image

# Load CLIP model and preprocess
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

st.title("Video Analysis and Search Tool")

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ["Upload & Process", "Search & Recommendations"])

if options == "Upload & Process":
    st.header("Upload & Process Videos")
    
    video_file = st.file_uploader("Upload Video", type=["mp4"])
    if video_file is not None:
        video_path = os.path.join("data/raw", video_file.name)
        with open(video_path, "wb") as f:
            f.write(video_file.getbuffer())
        
        st.write("Video uploaded successfully.")
        
        if st.button("Extract Keyframes"):
            extract_keyframes(video_path, "data/processed/keyframes")
            st.write("Keyframes extracted successfully.")
        
        if st.button("Transcode Video"):
            transcode_video(video_path, os.path.join("data/processed/transcoded", video_file.name))
            st.write("Video transcoded successfully.")
        
        if st.button("Detect Scenes"):
            detect_scenes(video_path, "data/processed/scenes")
            st.write("Scenes detected successfully.")
        
        if st.button("Analyze with CLIP"):
            keyframe_dir = "data/processed/keyframes"
            keyframes = [os.path.join(keyframe_dir, f) for f in os.listdir(keyframe_dir)]
            for keyframe in keyframes:
                probs = analyze_with_clip(keyframe, model, preprocess)
                st.write(f"Analysis for {os.path.basename(keyframe)}: {probs}")

elif options == "Search & Recommendations":
    st.header("Search & Recommendations")
    
    search_query = st.text_input("Enter search query")
    if st.button("Search"):
        keyframe_dir = "data/processed/keyframes"
        keyframes = [os.path.join(keyframe_dir, f) for f in os.listdir(keyframe_dir)]
        
        text_features = clip.tokenize([search_query]).to(device)
        with torch.no_grad():
            text_features = model.encode_text(text_features)
        
        similarities = []
        for keyframe in keyframes:
            image = preprocess(Image.open(keyframe)).unsqueeze(0).to(device)
            with torch.no_grad():
                image_features = model.encode_image(image)
            similarity = torch.cosine_similarity(text_features, image_features)
            similarities.append((keyframe, similarity.item()))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        for keyframe, sim in similarities[:5]:
            st.image(keyframe, caption=f"Similarity: {sim:.4f}")
    
    if st.button("Show Recommendations"):
        # Placeholder for recommendation logic, could be based on previous analyses
        st.write("Recommendations functionality coming soon.")
