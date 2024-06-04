

# Video Analysis Project

## Overview
This project focuses on content-based video retrieval using a subset of the V3C-1 dataset. It includes keyframe extraction, content analysis, and an interactive search interface via a Streamlit GUI.

## Directory Structure
```
video_analysis/
│
├── data/
│   ├── V3C100/
│   └── processed/
│       ├── keyframes/
│       └── transcoded/
├── models/
│   ├── pretrained/
│   └── custom/
├── notebooks/
├── scripts/
│   ├── analyze_keyframe_per_id.py
│   ├── analyze_keyframes_with_description.py
│   ├── analyze_keyframes.py
│   ├── check_database_connection.py
│   ├── create_database.py
│   ├── detect_shot_boundaries.py
│   ├── insert_sample_data.py
│   ├── list_keyframes.py
│   ├── list_video_ids.py
│   ├── store_analysis_results.py
│   ├── store_video_metadata.py
│   ├── transcode_video.py
│   ├── verify_descriptions.py
│   ├── verify_keyframe_analysis.py
│   ├── verify_video_id.py
│   └── __init__.py
├── setup/
│   ├── env_check.py
│   ├── environment.yml
│   └── pytorch_cuda_check.py
├── src/
│   ├── backend/
│   │   ├── database.py
│   │   └── 
│   ├── frontend/
│   │   ├── gui_streamlit ... .py
│   │   └── 
│   └── utils/
│       └── 
├── tests/
│   ├── test_extract_keyframes.py
│   └── test_analyze_content.py
├── .gitignore
├── README.md
├── requirements.txt
└── environment.yml
```

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


# Content-Based Video Retrieval System

## Project Overview
This project focuses on developing a content-based video retrieval system using a subset of the V3C-1 dataset. The system is designed to find small video segments of interest based on Known-Item Search (KIS) queries, which is a use case of the Video Browser Showdown (VBS).