# Synology DSM Package - Photo Organizer

This directory contains the files needed to build a Synology DSM package (.spk file) for the Photo Organizer application.

## Package Structure

```
package/
├── INFO                    # Package metadata
├── scripts/
│   ├── installer           # Installation script
│   ├── uninstaller         # Uninstallation script
│   └── start-stop-status   # Service control script
└── package/
    ├── organize_photos.py  # Main application script
    └── README.md           # Application documentation
```

## Building the Package

### On Linux/macOS:
```bash
chmod +x build_package.sh
./build_package.sh
```

### On Windows:
```powershell
.\build_package.ps1
```

This will create a `photo-organizer.spk` file that can be installed on Synology NAS.

## Installation on Synology

1. Copy the `photo-organizer.spk` file to your Synology NAS
2. Open **Package Center** in DSM
3. Click **Manual Install** (or go to Settings > Trust Level and allow unsigned packages)
4. Select the `photo-organizer.spk` file
5. Follow the installation wizard

## Package Details

- **Package Name**: photo-organizer
- **Version**: 1.0.0
- **Architecture**: x86_64 (Intel/AMD 64-bit)
- **DSM Version**: 7.0+
- **Dependencies**: Python 3

## Installation Paths

- Application: `/var/packages/photo-organizer/target/`
- Source Photos: `/var/packages/photo-organizer/target/Photos/PhotosToProcess/`
- Organized Photos: `/var/packages/photo-organizer/target/Photos/`
- Logs: `/var/packages/photo-organizer/var/photo-organizer.log`
- PID File: `/var/packages/photo-organizer/var/photo-organizer.pid`

## Service Management

The package can be started/stopped via:
- **Package Center**: Open the package and use Start/Stop buttons
- **Command Line**: 
  ```bash
  /var/packages/photo-organizer/etc/service.sh start
  /var/packages/photo-organizer/etc/service.sh stop
  /var/packages/photo-organizer/etc/service.sh status
  ```

## Notes

- The package requires Python 3 to be installed (available via Package Center)
- Python dependencies (Pillow, watchdog, imagehash) will be installed automatically
- The service runs in the background and monitors the PhotosToProcess folder
- Photos are automatically organized by year based on EXIF data or file dates

## Troubleshooting

- Check logs: `cat /var/packages/photo-organizer/var/photo-organizer.log`
- Verify Python: `python3 --version`
- Check service status: `/var/packages/photo-organizer/etc/service.sh status`
- Ensure directories exist: `ls -la /var/packages/photo-organizer/target/Photos/`

