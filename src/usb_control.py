import os

def enable_usb():
    """Enable USB storage devices without time restriction"""
    os.system("reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v Start /t REG_DWORD /d 3 /f")
    print("✅ USB storage enabled.")

def disable_usb():
    """Disable USB storage devices"""
    os.system("reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v Start /t REG_DWORD /d 4 /f")
    print("🚫 USB storage disabled.")

if __name__ == "__main__":
    choice = input("Enable or Disable USB? (E/D): ").strip().lower()
    if choice == "e":
        enable_usb()
    elif choice == "d":
        disable_usb()
    else:
        print("❌ Invalid option! Please enter 'E' to enable or 'D' to disable.")
