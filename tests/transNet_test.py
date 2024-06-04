import cv2
import numpy as np
import torch
import os
import sys
import matplotlib.pyplot as plt

# Add the path to the TransNetV2 directory
sys.path.append('../TransNetV2/inference-pytorch')

from transnetv2_pytorch import TransNetV2

def load_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (48, 27))  # Resize frame to 48x27 as required by TransNetV2
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        frames.append(frame)
    cap.release()
    return np.array(frames)

def main():
    # Load the TransNetV2 model
    model = TransNetV2()
    state_dict = torch.load("../TransNetV2/inference-pytorch/transnetv2-pytorch-weights.pth")
    model.load_state_dict(state_dict)
    model.eval().cuda()

    # Load video frames
    video_path = "C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/tests/testvid.mp4"
    frames = load_video(video_path)

    # Prepare the input
    input_video = torch.tensor(frames, dtype=torch.uint8).unsqueeze(0).cuda()  # Add batch dimension

    with torch.no_grad():
        # Predict scene changes
        single_frame_pred, all_frame_pred = model(input_video)
        
        single_frame_pred = torch.sigmoid(single_frame_pred).cpu().numpy()
        all_frame_pred = torch.sigmoid(all_frame_pred["many_hot"]).cpu().numpy()

    # Detect scene changes
    scene_changes = np.where(single_frame_pred > 0.5)[1]
    print("Detected scene changes at frames:", scene_changes)
    print(f"Total number of detected scene changes: {len(scene_changes)}")

    # Optional: Save frames with detected scene changes
    output_dir = "output_frames"
    os.makedirs(output_dir, exist_ok=True)
    for idx in scene_changes:
        cv2.imwrite(os.path.join(output_dir, f"frame_{idx}.jpg"), frames[idx])

    # Plotting the detected scene changes
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(len(single_frame_pred[0])), single_frame_pred[0], label='Scene Change Probability')
    plt.scatter(scene_changes, single_frame_pred[0, scene_changes], color='red', label='Detected Scenes')
    plt.xlabel('Frame Index')
    plt.ylabel('Probability')
    plt.legend()
    plt.title('Scene Change Detection')
    plt.show()

if __name__ == "__main__":
    main()
