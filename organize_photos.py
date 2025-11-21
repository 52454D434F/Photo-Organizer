import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

# Source and destination directories
SOURCE_DIR = r"Photos\PhotosToProcess"
DEST_DIR = r"Photos"

# Ensure destination directory exists
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_exif_taken_date(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'DateTimeOriginal':
                    return value
    except Exception as e:
        print(f"Error reading EXIF from {image_path}: {e}")
    return None

def move_photos_by_date():
    for filename in os.listdir(SOURCE_DIR):
        file_path = os.path.join(SOURCE_DIR, filename)
        if os.path.isfile(file_path):
            taken_date = get_exif_taken_date(file_path)
            if taken_date:
                # Format: 'YYYY:MM:DD HH:MM:SS'
                date_part = taken_date.split(' ')[0].replace(':', '-')
                year, month, day = date_part.split('-')
                dest_folder = os.path.join(DEST_DIR, year, month, day)
            else:
                dest_folder = os.path.join(DEST_DIR, 'UnknownDate')
            ensure_dir(dest_folder)
            dest_path = os.path.join(dest_folder, filename)
            print(f"Moving {filename} to {dest_path}")
            shutil.move(file_path, dest_path)

if __name__ == "__main__":
    move_photos_by_date()
