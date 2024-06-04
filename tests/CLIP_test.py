import clip
import torch
from PIL import Image
import os

# Load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Prepare the image and text
# Use forward slashes or double backslashes for the path
image_path = os.path.join("C:/Users/benwe/Desktop/desktop/Uni/S4/videoAnalysis/tests/testimage.png")
image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
text = clip.tokenize(["a dog", "banana", "tomato", "women", "chair"]).to(device)

# Image to text matching
with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)
    logits_per_image, logits_per_text = model(image, text)
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

print("Label probs:", probs)  # Prints the probabilities of each text description being relevant to the image

'''
# Text to image matching with multiple images
image_paths = ["image1.jpg", "image2.jpg"]
images = [preprocess(Image.open(image_path)).unsqueeze(0).to(device) for image_path in image_paths]
images = torch.cat(images, dim=0)

with torch.no_grad():
    image_features = model.encode_image(images)
    text_features = model.encode_text(text)
    logits_per_image, logits_per_text = model(images, text)
    probs = logits_per_text.softmax(dim=-1).cpu().numpy()

print("Image probs:", probs)  # Prints the probabilities of each image being relevant to the text description
'''
