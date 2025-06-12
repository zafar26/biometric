from setuptools import setup

APP = ['cubezix_attendance_sync_tool.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5', 'requests'],
    # 'iconfile': 'your_icon.icns',  # optional
    'plist': {
        'CFBundleName': 'Cubezix Attendance',
        'CFBundleDisplayName': 'Cubezix Attendance',
        'CFBundleIdentifier': 'com.cubezix.attendance',
        'CFBundleVersion': '0.1.0',
        'LSUIElement': True  # ✅ THIS HIDES THE DOCK/TERMINAL WINDOW
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
