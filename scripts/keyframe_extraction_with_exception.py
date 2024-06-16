import torch
import cv2
import os
import numpy as np
import sys
import sqlite3
import logging
from glob import glob

# Disable warning
os.environ['TORCH_CUDNN_V8_API_DISABLED'] = '1'

# Add the path to the TransNetV2 directory
sys.path.append('C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/TransNetV2/inference-pytorch')

from transnetv2_pytorch import TransNetV2

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/data/processed/video_processing.log"),
                        logging.StreamHandler(sys.stdout)
                    ])

def process_video_in_batches(video_path, batch_size=100):
    logging.info(f"Processing video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_indices = []
    index = 0
    
    model = TransNetV2()
    state_dict = torch.load("C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/TransNetV2/inference-pytorch/transnetv2-pytorch-weights.pth")
    model.load_state_dict(state_dict)
    model.eval().cuda()
    
    scene_changes = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (48, 27))  # Resize frame to 48x27 as required by TransNetV2
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        frames.append(frame)
        frame_indices.append(index)
        index += 1

        # Process in batches
        if len(frames) == batch_size:
            batch = np.array(frames)
            input_video = torch.tensor(batch, dtype=torch.uint8).unsqueeze(0).cuda()
            with torch.no_grad():
                single_frame_pred, _ = model(input_video)
                single_frame_pred = torch.sigmoid(single_frame_pred).cpu().numpy()
                detected_changes = np.where(single_frame_pred > 0.5)[1]
                scene_changes.extend(frame_indices[i] for i in detected_changes)
            frames = []
            frame_indices = []

    # Process any remaining frames
    if frames:
        batch = np.array(frames)
        input_video = torch.tensor(batch, dtype=torch.uint8).unsqueeze(0).cuda()
        with torch.no_grad():
            single_frame_pred, _ = model(input_video)
            single_frame_pred = torch.sigmoid(single_frame_pred).cpu().numpy()
            detected_changes = np.where(single_frame_pred > 0.5)[1]
            scene_changes.extend(frame_indices[i] for i in detected_changes)
    
    cap.release()
    logging.info(f"Detected scene changes: {scene_changes}")
    return scene_changes

def process_all_videos():
    db_path = 'C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/src/backend/database_2.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id, path FROM Videos')
    videos = cursor.fetchall()
    conn.close()

    os.makedirs('C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/data/processed/keyframes/', exist_ok=True)

    base_path = 'C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/data'
    keyframes_dir = 'C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/data/processed/keyframes'
    
    for video_id, relative_video_path in videos:
        video_path = os.path.abspath(os.path.join(base_path, relative_video_path.replace('\\', '/')))
        if not os.path.exists(video_path):
            logging.warning(f"Video file {video_path} does not exist.")
            continue

        keyframe_pattern = f'{keyframes_dir}/keyframe_{video_id}_*.jpg'
        existing_keyframes = glob(keyframe_pattern)
        if existing_keyframes:
            logging.info(f"Keyframes for video ID {video_id} already exist. Skipping...")
            continue

        scene_changes = process_video_in_batches(video_path)
        logging.info(f"Total number of detected scene changes for video ID {video_id}: {len(scene_changes)}")
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        index = 0
        keyframe_interval = int(fps * 5)  # 5 seconds interval
        
        if not scene_changes:
            logging.info(f"No scene changes detected for video ID {video_id}. Saving keyframes every 5 seconds.")
            # If no scene changes are detected, save a keyframe every 5 seconds
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                if index % keyframe_interval == 0:
                    cv2.imwrite(f'C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/data/processed/keyframes/keyframe_{video_id}_{index}.jpg', frame)
                index += 1
        else:
            next_scene_frame_indices = iter(scene_changes[1:] + [None])  # Append None to handle the last frame
            next_frame_index = next(next_scene_frame_indices)

            for frame_index in scene_changes:
                # Save the keyframe after the scene transition
                while index <= frame_index:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    if index == frame_index:
                        # Save the frame immediately after the transition if available
                        if next_frame_index is not None and index + 1 < next_frame_index:
                            ret, frame = cap.read()
                            index += 1
                        cv2.imwrite(f'{keyframes_dir}/keyframe_{video_id}_{index}.jpg', frame)
                    index += 1
                next_frame_index = next(next_scene_frame_indices, None)
        
        cap.release()

        logging.info(f"Finished processing video ID {video_id}")

if __name__ == "__main__":
    process_all_videos()
