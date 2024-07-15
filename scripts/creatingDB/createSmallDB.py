import sqlite3
import os

# Step 1: Define the path to your keyframes and the database name
keyframes_path = 'simon_polly\data1\keyframes'
database_name = 'simon_polly\data1\SmallDatabase.db'

# Step 2: Connect to the database (it will create the database if it doesn't exist)
conn = sqlite3.connect(database_name)
c = conn.cursor()

# Step 3: Create a table
c.execute('''CREATE TABLE IF NOT EXISTS keyframe_images
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              path TEXT,
              image BLOB,
              image_embedding BLOB)''')

# Step 4: Insert data into the table
for root, dirs, files in os.walk(keyframes_path):
    for file in files:
        file_path = os.path.join(root, file)
        with open(file_path, 'rb') as f:
            img_blob = f.read()
        # Omitting the generation and insertion of embeddings
        c.execute("INSERT INTO keyframe_images (path, image, image_embedding) VALUES (?, ?, ?)",
                  (file_path, img_blob, None))  # Passing None for the embeddings

# Step 5: Commit changes and close the connection
conn.commit()
conn.close()