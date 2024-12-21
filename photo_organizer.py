import hashlib
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# List of folders to monitor
MONITOR_FOLDERS = ["/ToProcess"]

def hash_file(file_path):
    """Generate SHA-256 hash for a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def hash_files():
    """Hash all files in the monitored folders and save to hash.log."""
    for folder in MONITOR_FOLDERS:
        log_file = Path(folder) / "hash.log"
        with open(log_file, "w") as log:
            for root, _, files in os.walk(folder):
                for file in files:
                    file_path = Path(root) / file
                    sha256 = hash_file(file_path)
                    log.write(f"{sha256} {file_path}\n")

def delete_duplicates():
    """Delete duplicate files based on hash values."""
    seen_hashes = {}
    for folder in MONITOR_FOLDERS:
        log_file = Path(folder) / "hash.log"
        if not log_file.exists():
            continue
        
        with open(log_file, "r") as log:
            for line in log:
                parts = line.strip().split(" ", 1)
                if len(parts) != 2:
                    continue
                sha256, file_path = parts
                file_path = Path(file_path)
                if sha256 in seen_hashes:
                    try:
                        file_path.unlink()
                        print(f"Deleted duplicate file: {file_path}")
                    except FileNotFoundError:
                        pass
                else:
                    seen_hashes[sha256] = True

class FolderMonitorHandler(FileSystemEventHandler):
    """Handler for monitoring file system changes."""
    def on_modified(self, event):
        if event.is_directory:
            return
        print(f"Change detected: {event.src_path}")
        hash_files()
        delete_duplicates()

def monitor_folders():
    """Monitor folders for changes."""
    observer = Observer()
    handler = FolderMonitorHandler()

    for folder in MONITOR_FOLDERS:
        observer.schedule(handler, folder, recursive=True)

    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Initial hashing and duplicate deletion
    hash_files()
    delete_duplicates()

    # Start monitoring for changes
    monitor_folders()
