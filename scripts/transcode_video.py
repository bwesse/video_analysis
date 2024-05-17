import subprocess
import os

def transcode_video(input_path, output_path):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-vf', 'scale=320:240',
        output_path
    ]
    subprocess.run(command)

if __name__ == "__main__":
    input_path = "data/V3C100/video1.mp4"
    output_path = "data/processed/transcoded/video1_small.mp4"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    transcode_video(input_path, output_path)
