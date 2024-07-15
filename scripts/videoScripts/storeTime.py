import sqlite3
import os

def parse_timestamp_file(filepath):
    timestamps = {}
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            frame_part = parts[0].split(': ')[1]
            timestamp_part = parts[1].split(': ')[1].split()[0]
            frame_index = int(frame_part)
            timestamp = float(timestamp_part)
            timestamps[frame_index] = timestamp
    return timestamps

def update_database_with_timestamps(db_path, video_id, timestamps):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for frame_index, timestamp in timestamps.items():
        cursor.execute("""
            UPDATE keyframes
            SET timestamp = ?
            WHERE video_id = ? AND frame_index = ?
        """, (timestamp, video_id, frame_index))
    conn.commit()
    conn.close()

def main():
    db_path = 'simon_polly\data1\database_new.db'  # Update this with the actual path to your database
    directory_path = 'simon_polly/data1/processed/timestamps'  # Update this with the actual path to your timestamp files

    # Scan the directory for timestamp files and extract video IDs
    video_ids = []
    for filename in os.listdir(directory_path):
        if filename.startswith("keyframe_timestamps_") and filename.endswith(".txt"):
            video_id = filename[len("keyframe_timestamps_"):-len(".txt")]
            video_ids.append(video_id)

    for video_id in video_ids:
        filepath = os.path.join(directory_path, f'keyframe_timestamps_{video_id}.txt')
        if os.path.exists(filepath):
            timestamps = parse_timestamp_file(filepath)
            update_database_with_timestamps(db_path, video_id, timestamps)
        else:
            print(f"File {filepath} not found.")

if __name__ == "__main__":
    main()