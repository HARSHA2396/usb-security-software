# usb-security-software
# 🛡️ USB Port Management and Security Software

An advanced Windows/macOS-compatible application to control USB port access, designed to prevent unauthorized usage and data theft. Features include whitelisting, scheduling, real-time alerts, tamper detection, and role-based access.

---

## 📝 Overview

This software offers granular control over USB access for systems used in sensitive environments. Administrators can whitelist specific devices, schedule USB availability, enforce user roles, and monitor activities—all from a user-friendly GUI.

---

## 🚀 Features

- ✅ **USB Whitelisting** — Allow only trusted USB devices
- ⏰ **Access Scheduling** — Enable/disable USB during set time windows
- 🔐 **Role-Based Access** — Admin-level control and user restrictions
- 🚨 **Tamper Detection** — Alerts on unauthorized attempts or config changes
- 📊 **Activity Logging** — Track device activity and export logs (CSV format)
- 🔔 **Real-Time Alerts** — Popups and sound notifications for key events
- 🌓 **Dark Mode UI** — Modern, animated interface with toggleable dark mode
- 🔄 **Cross-Platform Compatibility** — Works on both Windows & macOS

---

## 🛠️ Technologies Used

- `Python 3`
- `PyQt6` (UI Framework)
- `SQLite3` (Local database)
- `Win32api`, `pyudev` (Hardware Interface)
- `matplotlib` (For USB activity graphs)
- `Custom encryption modules` (for secure logs & config)



## 📦 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/HARSHA2396/usb-security-app.git
   cd usb-security-software
   python file.py
