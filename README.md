# Photo Organizer

This script automatically organizes photos in the `Photos/PhotosToProcess` directory by:
- Monitoring the folder for new files (folder watcher)
- Moving photos into year-based subfolders under `Photos` based on the date the photo was taken
- Using EXIF metadata (DateTimeOriginal) when available
- Falling back to file creation/modification date if EXIF data is not found
- Renaming files to `yyyymmdd_hhmmss.*` format when date information is available
- Detecting duplicate files using MD5 hash comparison
- Moving duplicates to a `Duplicates` folder with unique naming (_A, _B, etc.)

## Requirements
- Python 3.7 or higher
- [Pillow](https://python-pillow.org/) library for reading EXIF data
- [watchdog](https://python-watchdog.readthedocs.io/) library for folder monitoring
- [hashlib](https://docs.python.org/3/library/hashlib.html) library for MD5 hash calculation (built-in, no installation needed)

## Installation

1. Install Python from [python.org](https://www.python.org/downloads/).
2. Install the required Python packages by running:
   ```cmd
   pip install Pillow watchdog
   ```
   
   Or install them separately:
   ```cmd
   pip install Pillow
   pip install watchdog
   ```

## Usage
1. Place your photos in the `Photos/PhotosToProcess` directory.
2. Run the script:
   ```cmd
   python organize_photos.py
   ```
3. The script will:
   - Process any existing photos in the folder
   - Start monitoring the folder for new files
   - Automatically organize new photos as they are added
4. Press `Ctrl+C` to stop the folder watcher.

## Features
- **Automatic folder monitoring**: Continuously watches for new files
- **EXIF date extraction**: Uses photo metadata when available
- **File date fallback**: Uses file creation/modification date if EXIF is missing
- **Smart file renaming**: Renames files to `yyyymmdd_hhmmss.*` format based on date
- **Duplicate detection**: Compares files using MD5 hash to identify duplicates
- **Year-based organization**: Files are organized into year folders (e.g., `Photos/2024/`)

## Notes
- The script processes files in the `Photos/PhotosToProcess` directory.
- Files with dates are renamed and organized by year.
- Files without date information are moved to `Photos/NoDateFound` with their original filename.
- Duplicate files (same MD5 hash) are moved to `Photos/Duplicates` with unique naming.
- The script will create destination folders as needed.
