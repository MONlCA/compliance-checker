import os
import sys

# Adjust for PyInstaller
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    app_path = os.path.join(base_path, "app.py")
else:
    app_path = os.path.join(os.path.dirname(__file__), "app.py")

os.system(f"streamlit run '{app_path}'")
