import os
import sys
from datetime import datetime

WAKE_PHRASE = "wake up"
LISTEN_TIMEOUT = 5
PHRASE_TIME_LIMIT = 1.5

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

WAKE_SOUND_PATH = resource_path("jarvis.mp3")

def log(message, log_text=None):
    timestamp = datetime.now().strftime("%H:%M:%S")
    msg = f"[{timestamp}] {message}"
    print(msg, flush=True)
    if log_text:
        log_text.insert('end', msg + '\n')
        log_text.see('end')