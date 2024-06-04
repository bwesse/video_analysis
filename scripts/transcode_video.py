import subprocess
import os

def transcode_video(input_path, output_path):
    command = f"ffmpeg -i {input_path} -vf scale=640:360 {output_path}"
    subprocess.run(command, shell=True)

def transcode_videos(video_directory):
    for root, _, files in os.walk(video_directory):
        for file in files:
            if file.endswith('.mp4'):
                input_path = os.path.join(root, file)
                output_path = input_path.replace('.mp4', '_small.mp4')
                transcode_video(input_path, output_path)

if __name__ == "__main__":
    video_directory = '../data/V3C1-100/'
    transcode_videos(video_directory)
