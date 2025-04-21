import os
import time
import sqlite3
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOG_DB = "usb_logs.db"

def log_file_transfer(file_path, action):
    """Log file transfer actions (copy/move/delete) to the database"""
    conn = sqlite3.connect(LOG_DB)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS file_transfers (timestamp TEXT, file TEXT, action TEXT)")
    cursor.execute("INSERT INTO file_transfers VALUES (datetime('now'), ?, ?)", (file_path, action))
    conn.commit()
    conn.close()

class USBFileHandler(FileSystemEventHandler):
    """Handles file changes in the USB drive"""
    
    def on_created(self, event):
        if not event.is_directory:
            print(f"File Copied to USB: {event.src_path}")
            log_file_transfer(event.src_path, "Copied to USB")

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"File Deleted from USB: {event.src_path}")
            log_file_transfer(event.src_path, "Deleted from USB")

def get_usb_drive():
    """Detects the first USB storage device or MTP device (Mobile Phone)"""
    # Detect USB storage drives (like flash drives)
    for drive in "DEFGHIJKLMNOPQRSTUVWXYZ":
        if os.path.exists(f"{drive}:\\"):
            return f"{drive}:\\"

    # Detect MTP devices (Mobile Phones)
    try:
        output = subprocess.check_output('wmic logicaldisk get caption', shell=True).decode()
        for line in output.split("\n"):
            if "MTP" in line or "Mobile" in line:
                return line.strip()
    except Exception as e:
        print(f"Error detecting USB devices: {e}")

    return None

def monitor_usb_files():
    """Monitor file transfers on USB or MTP devices"""
    usb_path = get_usb_drive()
    
    if not usb_path:
        print("No USB drive detected. Waiting for connection...")
        return

    print(f"Monitoring USB Device: {usb_path}")

    event_handler = USBFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=usb_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    monitor_usb_files()
