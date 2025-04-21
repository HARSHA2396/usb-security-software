import os
import time
from usb_control import disable_usb
from database import log_usb_event
from playsound import playsound

# Path to the Windows Registry setting for USB
REGISTRY_KEY = "HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR"
EXPECTED_VALUE = "4"  # USB should be disabled

def check_tampering():
    """Check if USB settings were changed manually"""
    result = os.popen(f'reg query {REGISTRY_KEY} /v Start').read()
    if EXPECTED_VALUE not in result:
        print("⚠️ Security Alert: USB settings have been changed manually!")
        playsound("assets/alert.mp3")  # Play alert sound
        log_usb_event("⚠️ Security Alert: USB settings were changed manually!")
        disable_usb()  # Immediately re-disable USB

def monitor_tampering():
    """Continuously check for unauthorized registry changes"""
    while True:
        check_tampering()
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    monitor_tampering()
