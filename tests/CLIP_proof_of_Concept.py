import torch
import clip
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def generate_image_embedding(image_path):
    # Preprocess the image
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    # Generate the image embedding
    with torch.no_grad():
        image_embedding = model.encode_image(image)
    # Normalize the embedding
    image_embedding = image_embedding / image_embedding.norm(dim=-1, keepdim=True)
    return image_embedding.cpu().numpy()

def save_embedding(embedding, file_path):
    # Save the embedding to a file
    np.savetxt(file_path, embedding)

def load_embedding(file_path):
    # Load the embedding from a file
    return np.loadtxt(file_path).reshape(1, -1)

def compare_embeddings(embedding1, embedding2):
    # Compute the cosine similarity between two embeddings
    similarity_score = cosine_similarity(embedding1, embedding2)
    return similarity_score[0][0]

# Generate and save the embedding for a new image
image_path = "testimage.png"
embedding = generate_image_embedding(image_path)
save_embedding(embedding, "new_image_embedding.txt")

# Load a previously stored embedding
stored_embedding = load_embedding("stored_image_embedding.txt")

# Compare the new image embedding with the stored embedding
similarity_score = compare_embeddings(embedding, stored_embedding)
print(f"Similarity score: {similarity_score}")
