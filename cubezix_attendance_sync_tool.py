from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import sys
from main_script import run_attendance_sync

class AttendanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cubezix Attendance Sync Tool")
        self.setFixedSize(400, 250)
        self.setWindowIcon(QIcon("cubezix_icon.png"))  # Optional icon
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 10)
        layout.setSpacing(15)

        # Title
        title_label = QLabel("Sync Biometric with ERPNExt")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        # Instructions
        instruction_label = QLabel("Click the button below to sync attendance.")
        instruction_label.setFont(QFont("Arial", 10))
        instruction_label.setAlignment(Qt.AlignCenter)

        # Status Label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: green; font-weight: bold;")

        # Button
        sync_button = QPushButton("Sync Now")
        sync_button.setStyleSheet("padding: 10px; font-size: 12px;")
        sync_button.clicked.connect(self.sync_attendance)

        # Footer
        footer_label = QLabel("Developed By Cubezix Technologies")
        footer_label.setFont(QFont("Arial", 8))
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: gray;")

        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(instruction_label)
        layout.addWidget(sync_button)
        layout.addWidget(self.status_label)
        layout.addStretch()
        layout.addWidget(footer_label)

        self.setLayout(layout)

    def sync_attendance(self):
        self.status_label.setText("Syncing... Please wait.")
        QApplication.processEvents()  # Forces UI to update

        result = run_attendance_sync()

        if result and "success" in result:
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            self.status_label.setText("✅ Sync successful!")
        elif result:
            self.status_label.setStyleSheet("color: orange; font-weight: bold;")
            self.status_label.setText(f"⚠ Response: {result}")
        else:
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.status_label.setText("❌ Sync failed. Please try again.")

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Optional modern theme
    window = AttendanceApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()