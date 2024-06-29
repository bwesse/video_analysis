import sqlite3
import os
import asyncio
import aiofiles
from PIL import Image
import io
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration

# Initialize model and processor once
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b").to(device)
model.eval()  # Set the model to evaluation mode

async def load_image(image_path):
    async with aiofiles.open(image_path, mode='rb') as f:
        image_data = await f.read()
    return Image.open(io.BytesIO(image_data)).convert("RGB")

async def generate_image_description(image_path):
    try:
        raw_image = await load_image(image_path)
        inputs = processor(raw_image, return_tensors="pt").to(device)

        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=100)
        description = processor.decode(out[0], skip_special_tokens=True)
        return description
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

async def process_keyframe(cursor, keyframe):
    keyframe_id, image_path = keyframe
    if os.path.exists(image_path):
        description = await generate_image_description(image_path)
        if description:
            cursor.execute("UPDATE Keyframes SET description2 = ? WHERE id = ?", (description, keyframe_id))
            print(f"Updated keyframe {keyframe_id} with description: {description}")
    else:
        print(f"Image path {image_path} does not exist.")

async def update_all_keyframe_descriptions():
    conn = sqlite3.connect('simon_polly/data1/database_new.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, path FROM Keyframes WHERE description2 IS NULL OR description2 = ''")
    keyframes = cursor.fetchall()

    tasks = [process_keyframe(cursor, keyframe) for keyframe in keyframes]
    await asyncio.gather(*tasks)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    asyncio.run(update_all_keyframe_descriptions())