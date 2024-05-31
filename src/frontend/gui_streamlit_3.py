import streamlit as st
import sqlite3
from PIL import Image

def get_keyframes(video_id=None, text_query=None):
    conn = sqlite3.connect('video_analysis.db')
    cursor = conn.cursor()
    if video_id:
        cursor.execute("SELECT * FROM keyframes WHERE video_id=?", (video_id,))
    elif text_query:
        cursor.execute("SELECT * FROM keyframes WHERE analysis_data LIKE ?", ('%' + text_query + '%',))
    else:
        cursor.execute("SELECT * FROM keyframes")
    keyframes = cursor.fetchall()
    conn.close()
    return keyframes

def main():
    st.title("Video Analysis Search and Inspection")

    search_option = st.sidebar.selectbox("Search by", ["Video ID", "Text Query"])
    if search_option == "Video ID":
        video_id = st.sidebar.text_input("Enter Video ID")
        keyframes = get_keyframes(video_id=video_id)
    else:
        text_query = st.sidebar.text_input("Enter Text Query")
        keyframes = get_keyframes(text_query=text_query)

    for keyframe in keyframes:
        st.write(f"Video ID: {keyframe[1]}, Timestamp: {keyframe[2]}")
        img = Image.open(keyframe[3])
        st.image(img, caption=f"Keyframe at {keyframe[2]}")
        if st.button(f"Send to DRES - Keyframe {keyframe[0]}"):
            st.write("Keyframe sent to DRES for evaluation")

if __name__ == "__main__":
    main()
