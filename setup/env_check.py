import torch
import cv2
import tensorflow as tf
import numpy as np
import pandas as pd
import sklearn
import sqlite3
import subprocess

def check_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("FFmpeg version:\n", result.stdout.decode('utf-8').split('\n')[0])
    except FileNotFoundError:
        print("FFmpeg is not installed or not found in PATH.")

# PyTorch Check
print("CUDA available:", torch.cuda.is_available())
print("CUDA version:", torch.version.cuda)
print("Number of GPUs:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("GPU Name:", torch.cuda.get_device_name(0))

# Other Library Checks
print("OpenCV version:", cv2.__version__)
print("TensorFlow version:", tf.__version__)
print("Num GPUs Available for TensorFlow: ", len(tf.config.experimental.list_physical_devices('GPU')))
print("NumPy version:", np.__version__)
print("Pandas version:", pd.__version__)
print("Scikit-learn version:", sklearn.__version__)
print("PyTorch version:", torch.__version__)

# Check SQLite
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('SELECT SQLITE_VERSION()')
data = cursor.fetchone()
print("SQLite version:", data[0])
conn.close()

# Check FFmpeg
check_ffmpeg()
