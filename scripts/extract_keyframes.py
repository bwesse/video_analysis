import cv2
import os

def extract_keyframes(video_path, output_dir, interval=30):
    cap = cv2.VideoCapture(video_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    frame_id = 0
    success = True
    while success:
        success, frame = cap.read()
        if frame_id % interval == 0 and success:
            keyframe_path = os.path.join(output_dir, f'frame_{frame_id}.jpg')
            cv2.imwrite(keyframe_path, frame)
        frame_id += 1
    cap.release()

'''
import cv2
import os

def extract_keyframes(video_path, output_dir):
    cap = cv2.VideoCapture(video_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    frame_id = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Logic to detect shot boundary and extract keyframe
        # Example: Save every nth frame as a keyframe
        if frame_id % 30 == 0:
            keyframe_path = os.path.join(output_dir, f'frame_{frame_id}.jpg')
            cv2.imwrite(keyframe_path, frame)
        frame_id += 1
    cap.release()
'''