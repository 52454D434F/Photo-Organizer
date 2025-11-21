# Photo Organizer

This script organizes photos in the `Photos/PhotosToProcess` directory by moving them into subfolders under `Photos` based on the date the photo was taken (using EXIF metadata). If a photo does not have EXIF date information, it will be moved to a folder named `UnknownDate`.

## Requirements
- Python 3.7 or higher
- [Pillow](https://python-pillow.org/) library for reading EXIF data

## Installation

1. Install Python from [python.org](https://www.python.org/downloads/).
2. Install the required Python package Pillow by running:
   ```cmd
   pip install pillow
   ```

## Usage
1. Place your photos in the `Photos/PhotosToProcess` directory.
2. Run the script:
   ```cmd
   python organize_photos.py
   ```
3. The photos will be moved into subfolders under `Photos` based on their taken date.

## Notes
- The script only processes files in the `Photos/PhotosToProcess` directory.
- If a photo does not have EXIF date information, it will be moved to `Photos/UnknownDate`.
- The script will create destination folders as needed.
