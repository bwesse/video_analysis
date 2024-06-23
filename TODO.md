# still needs to be done

1. connecting to server

2. integrating a video replay

### time until 30th july
Create an evaluation of the performance for one of your content analysis methods (e.g., a
CNN) for five semantics (e.g., “car”, “parachute”, etc.) in one selected video in terms of
Recall with weighted averaging, including a confusion matrix until June 30, 2024. This can
be five different content classes if you use a CNN, five object classes if you use a regionbased CNN, or five different queries if you use CLIP, for example. Please note that for this
evaluation you will have to annotate your selected video with the corresponding
semantics. 

### end result
1. Interactively search for video content (e.g., keyframes and shots), either by a text-query,
content filtering, browsing, similarity search, and/or recommendations.
2. Inspect found items and play the corresponding video content (your system must
integrate a video player to check shots or videos).
3. Send a selected item (e.g., keyframe) to the DRES (Distributed Retrieval Evaluation Server)
for evaluation (see details below).



# this has been done
get the image embedding from clip and store it to the database.
clip can create embeddings for images and fo text. 
figure out how to save the em to the database - one the img embedding itself, one for the description and one concatenated versioon. 
whats the best way to store this embedding to then be able to do similaririty search
probably a vector and then do cosine siilarity -> see similarity_utils

get the saving to work on a daatabse with 5 images see smalltestdb

implement the search query in the gui. 

take the input image let it run through the steps and compare its embedding ot the database. 


possible addition
use yolo to label objects of interest in each image to enable wcategoriy filtering. 


pip install git+https://github.com/openai/CLIP.git
pip install torch torchvision
pip install numpy


