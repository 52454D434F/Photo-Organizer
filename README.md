# Photo Organizer

This script automatically organizes photos in the `Photos/PhotosToProcess` directory by:
- Monitoring the folder for new files (folder watcher)
- Moving photos into year-based subfolders under `Photos` based on the date the photo was taken
- Using EXIF metadata (DateTimeOriginal) when available
- Falling back to file creation/modification date if EXIF data is not found
- Renaming files to `yyyymmdd_hhmmss.*` format when date information is available
- Detecting exact duplicate files using MD5 hash comparison
- Detecting similar images using perceptual hashing
- Moving exact duplicates to a `Duplicates` folder with unique naming (_A, _B, etc.)
- Saving similar images with _A, _B, etc. suffixes in the Photos folder
- Comparing image quality when files differ and keeping the better quality version

## Requirements
- Python 3.7 or higher
- [Pillow](https://python-pillow.org/) library for reading EXIF data and image processing
- [watchdog](https://python-watchdog.readthedocs.io/) library for folder monitoring
- [imagehash](https://github.com/JohannesBuchner/imagehash) library for perceptual hashing (similar image detection)
- [hashlib](https://docs.python.org/3/library/hashlib.html) library for MD5 hash calculation (built-in, no installation needed)

## Installation

1. Install Python from [python.org](https://www.python.org/downloads/).
2. Install the required Python packages by running:
   ```cmd
   pip install Pillow watchdog imagehash
   ```
   
   Or install them separately:
   ```cmd
   pip install Pillow
   pip install watchdog
   pip install imagehash
   ```
   
   Note: `imagehash` will automatically install its dependencies (numpy, scipy, PyWavelets).

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
- **Exact duplicate detection**: Compares files using MD5 hash to identify identical files
- **Similar image detection**: Uses perceptual hashing to detect visually similar images
- **Image quality comparison**: Compares resolution, file size, and color depth to keep the best version
- **Year-based organization**: Files are organized into year folders (e.g., `Photos/2024/`)

## Notes
- The script processes files in the `Photos/PhotosToProcess` directory.
- Files with dates are renamed and organized by year.
- Files without date information are moved to `Photos/NoDateFound` with their original filename.
- **Duplicate handling**:
  - Exact duplicates (same MD5 hash) are moved to `Photos/Duplicates` with unique naming.
  - Similar images (detected by perceptual hashing) are saved with `_A`, `_B`, etc. suffixes in the Photos folder.
  - Different images with the same filename are compared for quality; the better quality version is kept.
- The script will create destination folders as needed.
