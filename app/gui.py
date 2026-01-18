import tkinter as tk
from tkinter import scrolledtext
import tkinter.ttk as ttk
import threading
from .utils import resource_path, log, WAKE_PHRASE
from .speech import speak, listen_for_wakeword, play_wake_sound
from .actions import wake_screen, open_apps, tile_windows, snap_window
import pyautogui
import time

log_text = None
status_label = None
stop_event = threading.Event()
listening_thread = None
is_listening = False

def main(stop_event):
    speak("System online.", log_text)
    log("JARVIS is now listening...", log_text)

    while not stop_event.is_set():
        if stop_event.is_set():
            break
        command = listen_for_wakeword(log_text)
        if stop_event.is_set():
            break

        if WAKE_PHRASE in command:
            log("[+] WAKE PHRASE DETECTED", log_text)
            
            play_wake_sound(log_text)
            
            time.sleep(1)
            
            wake_screen(log_text)
            speak("Wake command accepted.", log_text)
            open_apps(log_text)
            tile_windows(log_text)
            speak("All systems ready.", log_text)
            time.sleep(1)  
            snap_window("Spotify", [], log_text)
            pyautogui.press('space')
            # Continue listening after wake
            speak("Listening for next command...", log_text)

def create_gui():
    root = tk.Tk()
    root.title("JARVIS Assistant")
    root.geometry("700x500")
    root.resizable(True, True)
    root.configure(bg='#2b2b2b')

    # Set window icon
    try:
        root.iconbitmap(resource_path('icon.ico'))
    except:
        pass  # Icon not found, use default

    # Style for dark mode
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TLabel', background='#2b2b2b', foreground='white', font=('Segoe UI', 10))
    style.configure('TButton', background='#4a4a4a', foreground='white', font=('Segoe UI', 10), relief='flat', borderwidth=0)
    style.map('TButton', background=[('active', '#5a5a5a')])
    style.configure('TFrame', background='#2b2b2b')

    # Title label
    title_label = ttk.Label(root, text="Mini-Jarvis Workspace Automation", font=('Segoe UI', 16, 'bold'))
    title_label.pack(pady=10)

    # Developer label
    dev_label = ttk.Label(root, text="Developed by kaya0s", font=('Segoe UI', 8))
    dev_label.pack(pady=5)

    # Status label
    status_label = ttk.Label(root, text="Status: Idle", font=('Segoe UI', 12))
    status_label.pack(pady=5)

    # Toggle button
    def toggle():
        global is_listening
        if is_listening:
            deactivate()
        else:
            activate()

    toggle_button = ttk.Button(root, text="Activate", command=toggle)
    toggle_button.pack(pady=10)

    def activate():
        global is_listening, listening_thread
        if listening_thread and listening_thread.is_alive():
            log("Already listening.", log_text)
            return
        stop_event.clear()
        listening_thread = threading.Thread(target=lambda: main(stop_event), daemon=True)
        listening_thread.start()
        status_label.config(text="Status: Listening")
        toggle_button.config(text="Deactivate")
        is_listening = True
        log("Activated JARVIS.", log_text)

    def deactivate():
        global is_listening
        stop_event.set()
        status_label.config(text="Status: Stopped")
        toggle_button.config(text="Activate")
        is_listening = False
        log("Deactivated JARVIS.", log_text)

    # Log text with dark styling
    log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, bg='#1e1e1e', fg='white', insertbackground='white', font=('Consolas', 9))
    log_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    log_text.insert(tk.END, "Welcome to JARVIS Assistant.\nSystem starting...\n")

    # Start automatically
    activate()

    root.mainloop()

# Note: main function is defined in main.py, but referenced here. Actually, better to move main to main.py and import it.
# For now, I'll assume main is in main.py