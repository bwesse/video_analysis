import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import os

# Load the BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_image_caption(image_path):
    # Load and preprocess the image
    image = Image.open(image_path)
    inputs = processor(image, return_tensors="pt")
    
    # Generate the caption
    outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption

def process_images(image_directory, output_file):
    # Open the output file
    with open(output_file, 'w') as file:
        # Iterate over images in the directory
        for image_name in os.listdir(image_directory):
            image_path = os.path.join(image_directory, image_name)
            if os.path.isfile(image_path):
                try:
                    # Generate caption for each image
                    caption = generate_image_caption(image_path)
                    print(f"Image: {image_name}, Caption: {caption}")
                    # Write the image name and its caption to the file
                    file.write(f"{image_name}: {caption}\n")
                except Exception as e:
                    print(f"Error processing image {image_name}: {e}")

# Directory containing the images
image_directory = 'output_frames'
# Output text file to save the descriptions
output_file = 'image_descriptions.txt'

# Process the images and generate descriptions
process_images(image_directory, output_file)
