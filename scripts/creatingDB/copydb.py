import sqlite3

# Define source and destination database paths
source_db_path = '..'
destination_db_path = '..'

# Define the rows to copy (e.g., by id)
ids_to_copy = (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26)

# Connect to the source database
source_conn = sqlite3.connect(source_db_path)
source_cursor = source_conn.cursor()

# Connect to the destination database
dest_conn = sqlite3.connect(destination_db_path)
dest_cursor = dest_conn.cursor()

# Create the table in the destination database (if it doesn't already exist)
create_table_sql = '''
CREATE TABLE IF NOT EXISTS keyframes (
    id INTEGER PRIMARY KEY,
    video_id INTEGER,
    frame_index INTEGER,
    timestamp TEXT,
    image BLOB,
    path TEXT,
    description TEXT,
    analysis_results TEXT,
    combined_embedding TEXT,
    image_embedding TEXT,
    text_embedding TEXT
);
'''
dest_cursor.execute(create_table_sql)

# Copy selected rows from source to destination
placeholders = ','.join('?' * len(ids_to_copy))
select_sql = f'''
SELECT id, video_id, frame_index, timestamp, image, path, description, analysis_results, combined_embedding, image_embedding, text_embedding
FROM keyframes
WHERE id IN ({placeholders})
'''

insert_sql = '''
INSERT INTO keyframes (id, video_id, frame_index, timestamp, image, path, description, analysis_results, combined_embedding, image_embedding, text_embedding)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''

# Fetch the selected rows from the source database
source_cursor.execute(select_sql, ids_to_copy)
rows_to_copy = source_cursor.fetchall()

# Insert the rows into the destination database
for row in rows_to_copy:
    dest_cursor.execute(insert_sql, row)

# Commit the transaction and close the connections
dest_conn.commit()
source_conn.close()
dest_conn.close()

print("Selected rows have been copied successfully.")
