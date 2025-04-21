import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt
import qdarkstyle

class USBControlUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Advanced USB Security")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet(qdarkstyle.load_stylesheet())  # Apply Dark Mode

        layout = QVBoxLayout()

        self.title_label = QLabel("🔒 USB Security Control", self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.enable_button = QPushButton("Enable USB ✅")
        self.enable_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.enable_button.clicked.connect(self.enable_usb)

        self.disable_button = QPushButton("Disable USB 🚫")
        self.disable_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.disable_button.clicked.connect(self.disable_usb)

        self.toggle_theme_button = QPushButton("Toggle Light/Dark Mode 🌙")
        self.toggle_theme_button.setStyleSheet("font-size: 14px; padding: 8px;")
        self.toggle_theme_button.clicked.connect(self.toggle_theme)

        layout.addWidget(self.title_label)
        layout.addWidget(self.enable_button)
        layout.addWidget(self.disable_button)
        layout.addWidget(self.toggle_theme_button)

        self.setLayout(layout)

    def enable_usb(self):
        os.system("reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v Start /t REG_DWORD /d 3 /f")
        QMessageBox.information(self, "USB Enabled", "✅ USB ports have been enabled.")

    def disable_usb(self):
        os.system("reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v Start /t REG_DWORD /d 4 /f")
        QMessageBox.warning(self, "USB Disabled", "🚫 USB ports have been disabled.")

    def toggle_theme(self):
        """Toggle between Light and Dark mode"""
        if self.styleSheet():
            self.setStyleSheet("")  # Switch to Light Mode
        else:
            self.setStyleSheet(qdarkstyle.load_stylesheet())  # Switch to Dark Mode

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = USBControlUI()
    window.show()
    sys.exit(app.exec())
