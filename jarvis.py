import sys
import speech_recognition as sr
import subprocess
import time
import webbrowser
import pyautogui
import pyttsx3
import os
import ctypes
from datetime import datetime

WAKE_PHRASE = "wake up"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

# Ensure external binaries (like flac.exe) can be found
if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Prepend directly to PATH so bundled binaries take precedence
os.environ["PATH"] = base_path + os.pathsep + os.environ["PATH"]

import shutil
if shutil.which("flac"):
    print(f"[DEBUG] FLAC utility found: {shutil.which('flac')}")
else:
    print("[WARNING] FLAC utility not found in PATH!")
    if os.path.exists(os.path.join(base_path, "flac.exe")):
        print(f"[DEBUG] flac.exe exists at {os.path.join(base_path, 'flac.exe')}")

WAKE_SOUND_PATH = resource_path("jarvis.mp3") 
LISTEN_TIMEOUT = 5
PHRASE_TIME_LIMIT = 1.5

# Initialize pygame mixer for sound support
try:
    import pygame
    pygame.mixer.init()
except ImportError:
    pygame = None
    print("[!] Pygame not installed. Sound effects disabled.")

# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)

def speak(text):
    log(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def wake_screen():
    log("Waking screen...")
    ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)

def listen_for_wakeword():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        log("[+] Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=LISTEN_TIMEOUT,
                phrase_time_limit=PHRASE_TIME_LIMIT
            )
            log("[*] Audio captured, recognizing...")
        except sr.WaitTimeoutError:
            log("[-] Listening timed out (no speech)")
            return ""

    try:
        text = recognizer.recognize_google(audio).lower()
        log(f"[?] Recognized: \"{text}\"")
        return text
    except sr.UnknownValueError:
        log("[!] Could not understand audio")
        return ""
    except sr.RequestError as e:
        log(f"[!] Speech API error: {e}")
        return ""

def open_apps():
    log("Opening Spotify...")
    subprocess.Popen("spotify", shell=True)
    
    log("Opening VS Code...")
    vscode_path = os.path.expandvars(
        r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
    )
    if os.path.exists(vscode_path):
        subprocess.Popen(vscode_path, shell=True)

    time.sleep(1)

def play_wake_sound():
    if pygame and os.path.exists(WAKE_SOUND_PATH):
        try:
            log(f"♪ Playing wake sound: {WAKE_SOUND_PATH}")
            pygame.mixer.music.load(WAKE_SOUND_PATH)
            pygame.mixer.music.play()
        except Exception as e:
            log(f"[!] Error playing sound: {e}")
    else:
        if not pygame:
            log("[!] Pygame unavailable.")
        else:
            log(f"[!] Sound file not found at: {WAKE_SOUND_PATH}")

def snap_window(title, keys):
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
            log(f"Snapped {title} with keys {keys}")
            return
        time.sleep(0.2)
    log(f"Could not find window: {title}")

def tile_windows():
    log("Arranging windows...")

    # 1. Spotify -> Right Bottom
    snap_window("Spotify", ['right', 'down'])

    # 2. VS Code -> Left
    snap_window("Visual Studio Code", ['left'])

    # 3. Browser -> Right Top
    log("Opening ChatGPT...")
    webbrowser.open("https://chat.openai.com")
    
    time.sleep(1) 
    
    
    snap_window("ChatGPT", ['right', 'up'])



def main():
    speak("System online.")

    while True:
        command = listen_for_wakeword()

        if WAKE_PHRASE in command:
            log("[+] WAKE PHRASE DETECTED")
            
            play_wake_sound()
            
            time.sleep(1)
            
            wake_screen()
            speak("Wake command accepted.")
            open_apps()
            tile_windows()
            speak("All systems ready.")
            time.sleep(1)  
            snap_window("Spotify", [])
            pyautogui.press('space')
            break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("\n[!] Critical Error occurred. See details above.")
        input("Press Enter to exit...")
