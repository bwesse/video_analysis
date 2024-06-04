import streamlit as st
from quickdraw import QuickDrawData
from PIL import Image
import io

st.title("Quick Draw Recognition")

# Create a canvas component
canvas = st.canvas(width=256, height=256, key="canvas")  # key for session state

# Button to Submit Drawing
if st.button("Recognize Drawing"):
    # Get drawing as an image
    image_data = canvas.image_data

    if image_data is not None:
        image = Image.open(io.BytesIO(image_data))

        # QuickDraw Recognition
        qd = QuickDrawData()
        recognized_word, confidence = qd.guess_drawing(image, return_confidence=True)

        # Display Results
        st.subheader("Recognition Results:")
        if recognized_word:
            st.write(f"Recognized Word: {recognized_word}")
            st.write(f"Confidence: {confidence:.2f}")  # Display confidence to 2 decimal places
        else:
            st.write("No word recognized.")
    else:
        st.warning("Please draw something on the canvas.")
