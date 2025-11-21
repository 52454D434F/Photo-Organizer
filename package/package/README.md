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

## Installation

This package is installed via Synology Package Center. The package will:
- Install Python dependencies (Pillow, watchdog, imagehash)
- Create necessary directories
- Set up the service to run automatically

## Configuration

The source directory is: `/var/packages/photo-organizer/target/Photos/PhotosToProcess`
The destination directory is: `/var/packages/photo-organizer/target/Photos`

Place your photos in the PhotosToProcess folder to have them automatically organized.

## Service Management

The service can be started/stopped via Package Center or using:
- Start: `/var/packages/photo-organizer/etc/service.sh start`
- Stop: `/var/packages/photo-organizer/etc/service.sh stop`
- Status: `/var/packages/photo-organizer/etc/service.sh status`

## Logs

Logs are available at: `/var/packages/photo-organizer/var/photo-organizer.log`

