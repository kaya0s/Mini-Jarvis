import subprocess
import time
import webbrowser
import pyautogui
import os
import ctypes
from .utils import log

def wake_screen(log_text=None):
    log("Waking screen...", log_text)
    ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)

def open_apps(log_text=None):
    log("Opening Spotify...", log_text)
    subprocess.Popen("spotify", shell=True)
    
    log("Opening VS Code...", log_text)
    vscode_path = os.path.expandvars(
        r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
    )
    if os.path.exists(vscode_path):
        subprocess.Popen(vscode_path, shell=True)

    time.sleep(1)

def snap_window(title, keys, log_text=None):
    """
    Helper to find a window by title and apply snap keys.
    Retries for up to 3 seconds if window is not found immediately.
    """
    max_retries = 15
    for _ in range(max_retries):
        wins = pyautogui.getWindowsWithTitle(title)
        if wins:
            win = wins[0]
            try:
                win.activate()
            except:
                pass
            time.sleep(0.1)
            for k in keys:
                pyautogui.hotkey('win', k)
                time.sleep(0.1)
            log(f"Snapped {title} with keys {keys}", log_text)
            return
        time.sleep(0.2)
    log(f"Could not find window: {title}", log_text)

def tile_windows(log_text=None):
    log("Arranging windows...", log_text)

    # 1. Spotify -> Right Bottom
    snap_window("Spotify", ['right', 'down'], log_text)

    # 2. VS Code -> Left
    snap_window("Visual Studio Code", ['left'], log_text)

    # 3. Browser -> Right Top
    log("Opening ChatGPT...", log_text)
    webbrowser.open("https://chat.openai.com")
    
    time.sleep(1) 
    
    
    snap_window("ChatGPT", ['right', 'up'], log_text)