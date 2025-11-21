#!/bin/bash
# Bash script to build Synology DSM package
# This script creates a .spk file from the package directory

OUTPUT_NAME="${1:-photo-organizer.spk}"

echo "Building Synology DSM package..."

# Check if package directory exists
if [ ! -d "package" ]; then
    echo "Error: package directory not found!"
    exit 1
fi

# Create temporary build directory
BUILD_DIR="build"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "Copying package files..."

# Copy package structure
cp -r package/* "$BUILD_DIR/"

# Make scripts executable
echo "Setting script permissions..."
chmod +x "$BUILD_DIR/scripts/"*.sh 2>/dev/null || true

# Create SPK file using tar
echo "Creating package archive..."
cd "$BUILD_DIR"
tar -czf "../$OUTPUT_NAME" *
cd ..

# Cleanup
rm -rf "$BUILD_DIR"

echo ""
echo "Build complete!"
echo "Package file: $OUTPUT_NAME"
echo ""
echo "To install on Synology:"
echo "1. Copy $OUTPUT_NAME to your Synology NAS"
echo "2. Open Package Center"
echo "3. Click Manual Install"
echo "4. Select the $OUTPUT_NAME file"

