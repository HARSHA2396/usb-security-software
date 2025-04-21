import subprocess
import time
import json
import os
import sys
from usb_control import disable_usb, enable_usb
from database import log_usb_event
from PyQt6.QtWidgets import QApplication, QMessageBox
from playsound import playsound
from plyer import notification  # Fixed Notification Issue

# Initialize QApplication (Required for QMessageBox)
app = QApplication(sys.argv)

WHITELIST_FILE = "whitelist.json"
previous_devices = set()
blocked_devices = set()  # Store currently blocked USBs

def show_notification(title, message):
    """Display a Windows toast notification using Plyer"""
    notification.notify(
        title=title,
        message=message,
        app_name="USB Security",
        timeout=5  # Notification disappears after 5 seconds
    )

def load_whitelist():
    """Load whitelist from JSON file"""
    try:
        with open(WHITELIST_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_whitelist(allowed_devices):
    """Save updated whitelist to JSON file"""
    with open(WHITELIST_FILE, "w") as file:
        json.dump(allowed_devices, file, indent=4)

def get_connected_usb():
    """Get a list of connected USB devices and detect insertions/removals"""
    global previous_devices
    devices = subprocess.check_output("wmic diskdrive get SerialNumber", shell=True)
    current_devices = {device.strip() for device in devices.decode().split("\n")[1:-1] if device.strip()}

    # Detect USB Insertion
    new_devices = current_devices - previous_devices
    if new_devices:
        for device in new_devices:
            show_notification("USB Inserted", f"USB device {device} connected.")

    # Detect USB Removal
    removed_devices = previous_devices - current_devices
    if removed_devices:
        for device in removed_devices:
            show_notification("USB Removed", f"USB device {device} disconnected.")
            if device in blocked_devices:
                blocked_devices.remove(device)  # Remove from blocked list when unplugged

    previous_devices = current_devices  # Update device list
    return list(current_devices)

def play_alert():
    """Play alert sound when unauthorized USB is detected"""
    try:
        alert_path = os.path.abspath("assets/alert.mp3")  # Get full path
        if os.path.exists(alert_path):
            playsound(alert_path)  # Play the MP3 file
        else:
            print(f"Error: Sound file not found at {alert_path}")
    except Exception as e:
        print(f"Error playing sound: {e}")

def show_popup():
    """Show a popup when unauthorized USB is detected"""
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setWindowTitle("USB Blocked")
    msg_box.setText("Unauthorized USB detected! USB ports have been disabled.")
    msg_box.setInformativeText("Do you want to re-enable USB manually?")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    result = msg_box.exec()

    if result == QMessageBox.StandardButton.Yes:
        enable_usb()
        log_usb_event("User re-enabled USB after unauthorized access.")

def monitor_usb():
    """Continuously check for unauthorized USB devices"""
    global blocked_devices
    while True:
        whitelist = load_whitelist()
        connected_devices = get_connected_usb()
        unauthorized_devices = {device for device in connected_devices if device not in whitelist}

        # Detect new unauthorized USBs (that were not previously blocked)
        new_unauthorized_devices = unauthorized_devices - blocked_devices

        if new_unauthorized_devices:
            print(f"Unauthorized USB detected! Blocking: {new_unauthorized_devices}")
            play_alert()  # Play alert sound
            log_usb_event(f"Unauthorized USB detected: {new_unauthorized_devices}. USB disabled.")
            disable_usb()
            show_notification("USB Blocked", "An unauthorized USB device was detected and blocked.")
            show_popup()
            blocked_devices.update(new_unauthorized_devices)  # Add to blocked list

        # Remove devices from the blocked list if they are no longer connected
        blocked_devices.intersection_update(unauthorized_devices)

        time.sleep(10) #Check every 10 seconds

if __name__ == "__main__":
    monitor_usb()
