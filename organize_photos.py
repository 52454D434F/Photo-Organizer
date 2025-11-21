import os
import shutil
import time
import hashlib
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Source and destination directories
SOURCE_DIR = r"Photos\PhotosToProcess"
DEST_DIR = r"Photos"

# Ensure destination directory exists
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_exif_taken_date(image_path):
    """Get EXIF DateTimeOriginal and return as datetime object."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'DateTimeOriginal':
                    # Format: 'YYYY:MM:DD HH:MM:SS'
                    try:
                        return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                    except ValueError:
                        print(f"Error parsing EXIF date format: {value}")
                        return None
    except Exception as e:
        print(f"Error reading EXIF from {image_path}: {e}")
    return None

def get_file_date(file_path):
    """Get the older of creation or modification date from file metadata and return as datetime object."""
    try:
        creation_time = os.path.getctime(file_path)
        modification_time = os.path.getmtime(file_path)
        # Use the older (earlier) date
        oldest_timestamp = min(creation_time, modification_time)
        return datetime.fromtimestamp(oldest_timestamp)
    except Exception as e:
        print(f"Error reading file date from {file_path}: {e}")
        return None

def get_file_modification_time(file_path):
    """Get the modification time of a file as datetime object."""
    try:
        modification_time = os.path.getmtime(file_path)
        return datetime.fromtimestamp(modification_time)
    except Exception as e:
        print(f"Error reading modification time from {file_path}: {e}")
        return None

def format_datetime_for_filename(dt):
    """Format datetime object as yyyymmdd_hhmmss."""
    return dt.strftime('%Y%m%d_%H%M%S')

def calculate_md5(file_path):
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error calculating MD5 for {file_path}: {e}")
        return None

def get_unique_duplicate_filename(duplicates_folder, base_filename):
    """Get a unique filename in the Duplicates folder by appending _A, _B, etc."""
    name, ext = os.path.splitext(base_filename)
    counter = 0
    suffix_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                     'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    # First try without suffix
    test_filename = base_filename
    test_path = os.path.join(duplicates_folder, test_filename)
    if not os.path.exists(test_path):
        return test_filename
    
    # Then try with _A, _B, etc.
    for letter in suffix_letters:
        test_filename = f"{name}_{letter}{ext}"
        test_path = os.path.join(duplicates_folder, test_filename)
        if not os.path.exists(test_path):
            return test_filename
    
    # If we run out of letters, use numbers
    counter = 1
    while True:
        test_filename = f"{name}_{counter}{ext}"
        test_path = os.path.join(duplicates_folder, test_filename)
        if not os.path.exists(test_path):
            return test_filename
        counter += 1

def process_photo(file_path):
    """Process a single photo file and move it to the appropriate date folder."""
    if not os.path.isfile(file_path):
        return
    
    # Wait a moment to ensure file is fully written (useful for large files being copied)
    time.sleep(0.5)
    
    original_filename = os.path.basename(file_path)
    file_ext = os.path.splitext(original_filename)[1]  # Get extension including dot
    
    # Try to get date from EXIF first
    photo_datetime = get_exif_taken_date(file_path)
    
    # If no EXIF data, try file metadata
    if not photo_datetime:
        photo_datetime = get_file_date(file_path)
    
    if photo_datetime:
        # We have a date, rename file to yyyymmdd_hhmmss.*
        new_filename = format_datetime_for_filename(photo_datetime) + file_ext
        year = photo_datetime.strftime('%Y')
        # month = photo_datetime.strftime('%m')
        # day = photo_datetime.strftime('%d')
        # dest_folder = os.path.join(DEST_DIR, year, month, day)
        dest_folder = os.path.join(DEST_DIR, year)
        dest_filename = new_filename
    else:
        # No date found, keep original filename and move to NoDateFound
        dest_folder = os.path.join(DEST_DIR, 'NoDateFound')
        dest_filename = original_filename
    
    ensure_dir(dest_folder)
    dest_path = os.path.join(dest_folder, dest_filename)
    
    # Check if destination file already exists
    if os.path.exists(dest_path):
        # Compare MD5 hashes to determine if it's a duplicate
        print(f"File {dest_filename} already exists at {dest_path}, comparing MD5 hashes...")
        source_hash = calculate_md5(file_path)
        dest_hash = calculate_md5(dest_path)
        
        if source_hash and dest_hash and source_hash == dest_hash:
            # Files are identical (duplicate), move to Duplicates folder
            duplicates_folder = os.path.join(DEST_DIR, 'Duplicates')
            ensure_dir(duplicates_folder)
            unique_filename = get_unique_duplicate_filename(duplicates_folder, dest_filename)
            duplicates_path = os.path.join(duplicates_folder, unique_filename)
            print(f"Files are identical (MD5 match). Moving duplicate to {duplicates_path}")
            try:
                shutil.move(file_path, duplicates_path)
            except Exception as e:
                print(f"Error moving duplicate {original_filename}: {e}")
            return
        else:
            # Files have different content (MD5 mismatch), check which file was modified
            print(f"File {dest_filename} exists but has different content (MD5 mismatch). Checking modification times...")
            source_mod_time = get_file_modification_time(file_path)
            dest_mod_time = get_file_modification_time(dest_path)
            
            if source_mod_time and dest_mod_time:
                # Determine which file is newer (modified)
                if source_mod_time > dest_mod_time:
                    # Source file is newer, move it to Duplicates
                    file_to_move = file_path
                    file_name = dest_filename
                    print(f"Source file is newer (modified: {source_mod_time}). Moving to Duplicates folder.")
                else:
                    # Destination file is newer, move it to Duplicates and keep source
                    file_to_move = dest_path
                    file_name = dest_filename
                    print(f"Destination file is newer (modified: {dest_mod_time}). Moving destination to Duplicates, keeping source.")
            else:
                # Fallback if we can't get modification times
                file_to_move = file_path
                file_name = dest_filename
                print(f"Unable to get modification times. Moving source file to Duplicates folder.")
            
            # Move the modified file to Duplicates folder
            duplicates_folder = os.path.join(DEST_DIR, 'Duplicates')
            ensure_dir(duplicates_folder)
            unique_filename = get_unique_duplicate_filename(duplicates_folder, file_name)
            duplicates_path = os.path.join(duplicates_folder, unique_filename)
            
            try:
                shutil.move(file_to_move, duplicates_path)
                print(f"Moved file to {duplicates_path}")
                
                # If we moved the destination file, now move the source to its place
                if file_to_move == dest_path:
                    try:
                        shutil.move(file_path, dest_path)
                        print(f"Moved source file to {dest_path}")
                    except Exception as e:
                        print(f"Error moving source file to destination: {e}")
            except Exception as e:
                print(f"Error moving file to Duplicates: {e}")
            return
    
    if photo_datetime:
        print(f"Moving {original_filename} to {dest_path} (renamed to {dest_filename})")
    else:
        print(f"Moving {original_filename} to {dest_path} (no date found, keeping original name)")
    
    try:
        shutil.move(file_path, dest_path)
    except Exception as e:
        print(f"Error moving {original_filename}: {e}")

def move_photos_by_date():
    """Process all existing photos in the source directory."""
    if not os.path.exists(SOURCE_DIR):
        print(f"Source directory {SOURCE_DIR} does not exist. Creating it...")
        ensure_dir(SOURCE_DIR)
        return
    
    for filename in os.listdir(SOURCE_DIR):
        file_path = os.path.join(SOURCE_DIR, filename)
        process_photo(file_path)

class PhotoHandler(FileSystemEventHandler):
    """Handler for file system events in the watched directory."""
    
    def on_created(self, event):
        """Called when a file or directory is created."""
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            process_photo(event.src_path)
    
    def on_moved(self, event):
        """Called when a file or directory is moved/renamed."""
        if not event.is_directory:
            print(f"File moved/renamed: {event.dest_path}")
            process_photo(event.dest_path)

def start_watching():
    """Start watching the source directory for new files."""
    if not os.path.exists(SOURCE_DIR):
        print(f"Source directory {SOURCE_DIR} does not exist. Creating it...")
        ensure_dir(SOURCE_DIR)
    
    print(f"Starting folder watcher for: {os.path.abspath(SOURCE_DIR)}")
    print("Press Ctrl+C to stop watching...")
    
    event_handler = PhotoHandler()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping folder watcher...")
        observer.stop()
    
    observer.join()
    print("Folder watcher stopped.")

if __name__ == "__main__":
    # Process any existing photos first
    print("Processing existing photos...")
    move_photos_by_date()
    print("Existing photos processed.\n")
    
    # Start watching for new files
    start_watching()
