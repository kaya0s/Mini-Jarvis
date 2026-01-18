import sys
import os
import shutil
from app.utils import resource_path
from app.gui import create_gui

# Ensure external binaries (like flac.exe) can be found
if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Prepend directly to PATH so bundled binaries take precedence
os.environ["PATH"] = base_path + os.pathsep + os.environ["PATH"]

if shutil.which("flac"):
    print(f"[DEBUG] FLAC utility found: {shutil.which('flac')}")
else:
    print("[WARNING] FLAC utility not found in PATH!")
    if os.path.exists(os.path.join(base_path, "flac.exe")):
        print(f"[DEBUG] flac.exe exists at {os.path.join(base_path, 'flac.exe')}")

if __name__ == "__main__":
    try:
        create_gui()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("\n[!] Critical Error occurred. See details above.")
        input("Press Enter to exit...")