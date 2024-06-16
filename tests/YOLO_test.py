import torch
import os
from PIL import Image
from tqdm import tqdm

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def generate_image_description(image_path):
    # Perform object detection
    results = model(image_path)
    labels = results.names
    detections = results.pred[0]

    # Generate a textual description based on detected objects
    detected_objects = [labels[int(detection[5])] for detection in detections]
    description = ', '.join(detected_objects)
    
    return description

def process_keyframes(keyframe_dir, output_file):
    with open(output_file, 'w') as file:
        # Iterate over keyframe images in the directory
        for frame_file in tqdm(os.listdir(keyframe_dir)):
            if frame_file.endswith(('.png', '.jpg', '.jpeg')):
                frame_path = os.path.join(keyframe_dir, frame_file)
                
                # Generate description
                description = generate_image_description(frame_path)
                
                # Write description to the output file
                file.write(f"{frame_file}: {description}\n")

if __name__ == "__main__":
    # Directory containing keyframe images
    keyframe_dir = 'testimages'  # Change this to your keyframe directory
    output_file = 'yolo_keyframe_descriptions.txt'  # Output file to store descriptions
    
    process_keyframes(keyframe_dir, output_file)
