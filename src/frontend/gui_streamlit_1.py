import streamlit as st
import cv2
import tempfile
import os

# Title of the app
st.title("Video Content Search")

# File uploader for video files
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    # Display the uploaded video
    st.video(uploaded_file)
    
    # OpenCV video capture
    cap = cv2.VideoCapture(tfile.name)
    
    st.text("Processing video...")

    # Extract keyframes (every nth frame)
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    frame_id = 0
    success = True
    keyframes_dir = tempfile.mkdtemp()
    while success:
        success, frame = cap.read()
        if frame_id % (frame_rate * 2) == 0:  # Extract a frame every 2 seconds
            if success:
                keyframe_path = os.path.join(keyframes_dir, f"frame_{frame_id}.jpg")
                cv2.imwrite(keyframe_path, frame)
                st.image(frame, caption=f"Keyframe at {frame_id//frame_rate} seconds")
        frame_id += 1
    
    cap.release()
    st.text("Video processing completed.")


