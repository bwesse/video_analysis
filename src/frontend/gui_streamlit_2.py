import streamlit as st
import cv2
import os
import sqlite3
import tempfile
import sys

# Add the script and src/backend directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from analyze_content import analyze_keyframe
from database import create_database, store_analysis

# Initialize database
db_path = 'video_analysis.db'
create_database(db_path)

# Title of the app
st.title("Content-Based Video Retrieval System")

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
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    frame_id = 0
    success = True
    keyframes_dir = tempfile.mkdtemp()

    st.text("Processing video...")

    while success:
        success, frame = cap.read()
        if frame_id % (frame_rate * 2) == 0 and success:  # Extract a frame every 2 seconds
            keyframe_path = os.path.join(keyframes_dir, f"frame_{frame_id}.jpg")
            cv2.imwrite(keyframe_path, frame)
            st.image(frame, caption=f"Keyframe at {frame_id//frame_rate} seconds")
            analysis = analyze_keyframe(keyframe_path)
            store_analysis(db_path, os.path.basename(tfile.name), frame_id, str(analysis))
        frame_id += 1

    cap.release()
    st.text("Video processing completed.")

# Search functionality
query = st.text_input("Search for video content")

def search_database(query):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM keyframes WHERE analysis LIKE ?", ('%' + query + '%',))
    results = c.fetchall()
    conn.close()
    return results

if query:
    search_results = search_database(query)
    for result in search_results:
        st.write(result)
        frame_path = os.path.join(keyframes_dir, f"frame_{result[2]}.jpg")
        st.image(frame_path, caption=f"Keyframe at {result[2]//frame_rate} seconds")

# Function to simulate sending a selected item to the DRES server
def send_to_dres(item):
    # Implement the actual API call to DRES server here
    st.success(f"Item {item} sent to DRES for evaluation.")

# Button to send the selected item to DRES
if st.button("Send Selected Item to DRES"):
    if query:
        selected_item = search_results[0]  # Example: selecting the first item from the results
        send_to_dres(selected_item)
    else:
        st.warning("No items to send.")
