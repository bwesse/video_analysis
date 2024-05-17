import cv2
import os

def extract_keyframes(video_path, output_dir):
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    count = 0
    while success:
        if count % 30 == 0:  # Extract one frame every 30 frames
            filename = os.path.join(output_dir, f"keyframe_{count}.jpg")
            cv2.imwrite(filename, frame)
        success, frame = cap.read()
        count += 1
    cap.release()

if __name__ == "__main__":
    video_path = "data/V3C100/video1.mp4"
    output_dir = "data/processed/keyframes"
    os.makedirs(output_dir, exist_ok=True)
    extract_keyframes(video_path, output_dir)
