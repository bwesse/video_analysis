import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image
import os

def analyze_keyframe(image_path, model):
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    input_image = Image.open(image_path)
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)

    with torch.no_grad():
        output = model(input_batch)
    
    return output

if __name__ == "__main__":
    model = resnet50(pretrained=True)
    model.eval()
    keyframe_path = "data/processed/keyframes/keyframe_0.jpg"
    output = analyze_keyframe(keyframe_path, model)
    print(output)
