

# Video Analysis Project

By Simon Puchas, Tim Schumann & Ben Wesse


## Project Overview

The Video Analysis Project (VP) is a comprehensive system designed to allow users to search for video content from a subset of the V3C-1 dataset using text queries, short keyframes, or entire videos. This project leverages advanced machine learning models to extract and analyze keyframes from videos, generate descriptive metadata, and match these descriptions against a pre-built database to find the best results. The results are then displayed in a user-friendly web interface built with Streamlit.

## Information Flow

### User Input

1. **Text Query**: Users can input a text query directly into the search bar.
2. **Keyframe Query**: Users can upload a short keyframe.
3. **Video Query**: Users can upload a full video, from which keyframes will be extracted.

### Keyframe Extraction

For video queries, the system uses **TransNetV2** to detect and extract keyframes. This ensures that only the most relevant frames are analyzed, optimizing performance and accuracy.

### Keyframe Analysis

Once keyframes are extracted, they are analyzed using the **CLIP (Contrastive Language–Image Pretraining)** model. CLIP generates descriptive metadata for each keyframe, which is then used to match against the existing database.

### Database Comparison

The system utilizes a pre-built SQLite database containing descriptions of all videos previously processed as well as the embedding for each keyframe. The users text input or generated metadata from the user's keyframes is compared against this database to find the best matching videos.

### Result Display

The best matching results are displayed to the user through a **Streamlit** front-end. Streamlit is chosen for its simplicity and easy integration with Python-based tools, allowing for rapid development and deployment.

<div style="page-break-after: always;"></div>


## Tools Employed

### TransNetV2
- **Role**: Keyframe extraction from uploaded videos.
- **Purpose**: Efficiently detects scene boundaries to select the most relevant frames for analysis.

### CLIP
- **Role**: Keyframe analysis and embedding generation.
- **Purpose**: Converts images and text into high-dimensional embeddings in a shared semantic space. This allows for effective comparison between keyframes and text-based queries, enabling the system to find the most relevant keyframe matches from the database.

### SQLite
- **Role**: Storage and retrieval of video metadata.
- **Purpose**: A lightweight database solution to store and efficiently query video descriptions and metadata.

### Streamlit
- **Role**: Front-end web interface.
- **Purpose**: Provides an interactive and user-friendly platform for displaying search results.

### Python
- **Role**: Core programming language.
- **Purpose**: All scripts and applications are developed in Python, leveraging its extensive libraries for machine learning and web development.


## Directory Structure

- **data/**: Contains raw and processed video data.
  - **V3C100/**: Raw video dataset.
  - **processed/**: Processed video data including keyframes and transcoded videos.

- **models/**: Stores pretrained and custom machine learning models.
  - **pretrained/**: Pretrained models like TransNetV2 and CLIP.
  - **custom/**: Custom models developed for specific project needs.

- **notebooks/**: Jupyter notebooks for exploratory data analysis and prototyping.

- **scripts/**: Python scripts for various tasks including video processing, database management, and analysis.
  - **analyze_keyframe_per_id.py**: Analyze keyframes for a specific video ID.
  - **analyze_keyframes_with_description.py**: Analyze keyframes and generate descriptions.
  - **analyze_keyframes.py**: General keyframe analysis.
  - **check_database_connection.py**: Ensure database connection is established.
  - **create_database.py**: Script to create the SQLite database.
  - **detect_shot_boundaries.py**: Detect shot boundaries in videos.
  - **insert_sample_data.py**: Insert sample data into the database.
  - **list_keyframes.py**: List all keyframes in the database.
  - **list_video_ids.py**: List all video IDs in the database.
  - **store_analysis_results.py**: Store analysis results in the database.
  - **store_video_metadata.py**: Store video metadata in the database.
  - **transcode_video.py**: Transcode videos to a suitable format for processing.
  - **verify_descriptions.py**: Verify the accuracy of keyframe descriptions.
  - **verify_keyframe_analysis.py**: Verify the keyframe analysis process.
  - **verify_video_id.py**: Verify the video ID against the database.
  - **__init__.py**: Initialization script.

- **setup/**: Environment setup scripts.
  - **env_check.py**: Check environment configurations.
  - **environment.yml**: Environment configuration file.
  - **pytorch_cuda_check.py**: Check PyTorch and CUDA setup.

- **src/**: Source code for the project.
  - **backend/**: Backend logic including database interactions.
    - **database.py**: Database interaction logic.
  - **frontend/**: Frontend code for the Streamlit application.
    - **gui_streamlit.py**: Streamlit GUI implementation.
  - **utils/**: Utility functions and helpers.

- **tests/**: Unit and integration tests.
  - **test_extract_keyframes.py**: Test keyframe extraction functionality.
  - **test_analyze_content.py**: Test content analysis functionality.

- **.gitignore**: Git ignore file.
- **README.md**: Project README file.
- **requirements.txt**: Python dependencies.
- **environment.yml**: Environment configuration file.

## Conclusion

The Video Analysis Project integrates state-of-the-art machine learning models with a streamlined web interface to provide users with a powerful tool for video content search and analysis. The project leverages a combination of TransNetV2, CLIP, SQLite, and Streamlit, all orchestrated through Python scripts, to deliver an efficient and user-friendly experience.



<div style="page-break-after: always;"></div>


## Frontendmockup
<img src="doc\screenmockup.png" alt="screenmockup" style="width: 160mm; height: 250mm; margin: auto; display: block;">






## Setup Process

### Step 1: Install Anaconda
Download and install Anaconda from the [official website](https://www.anaconda.com/). Add Anaconda to your system's PATH during installation.

### Step 2: Create a Conda Environment
You can use the provided `environment.yml` file to create the environment:
```sh
conda env create -f setup/environment.yml
conda activate video_analysis_env
```

## Step 3: Configure VSCode to Use Conda Environment

1. Open VSCode.
2. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on macOS).
3. Type `Python: Select Interpreter` and select the interpreter for the `video_analysis_env` environment.
4. Add the following settings to the VSCode settings JSON file (`settings.json`):
   ```json
        {
            "redhat.telemetry.enabled": false,
            "files.autoSave": "afterDelay",
            "terminal.integrated.env.windows": {
                "PATH": "C:\\Users\\benwe\\Anaconda3;C:\\Users\\benwe\\Anaconda3\\Scripts;C:\\Users\\benwe\\Anaconda3\\Library\\bin;%PATH%"
            },
            "python.condaPath": "C:\\Users\\benwe\\Anaconda3\\Scripts\\conda.exe"
        }
        

   ```
   Replace `benwe` with your actual username.

## step 4: cuda installation
    
    https://developer.nvidia.com/cuda-downloads
    

### Step 4: Verify Installation
Run the environment check script to ensure all packages are installed correctly:
```sh
python setup/env_check.py
```


## Running the Project
1. **Extract Keyframes**: Run `scripts/extract_keyframes.py`.
2. **Analyze Content**: Run `scripts/analyze_content.py`.
3. **Start Streamlit App**: Navigate to the project directory and run the latest version of the gui:
   ```sh
   streamlit run src/frontend/gui_streamlit_X.py
   ```

## Running Tests
You can run tests to ensure the functionality of the components as well as see the basic functionality:
```sh
pytest tests/
```
