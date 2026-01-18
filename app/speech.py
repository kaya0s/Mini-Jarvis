import speech_recognition as sr
import pyttsx3
import pygame
import os
from .utils import resource_path, log, WAKE_SOUND_PATH, LISTEN_TIMEOUT, PHRASE_TIME_LIMIT

# Initialize pygame mixer for sound support
try:
    pygame.mixer.init()
except ImportError:
    pygame = None
    print("[!] Pygame not installed. Sound effects disabled.")

# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text, log_text=None):
    log(f"JARVIS: {text}", log_text)
    engine.say(text)
    engine.runAndWait()

def listen_for_wakeword(log_text=None):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        log("[+] Listening...", log_text)
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=LISTEN_TIMEOUT,
                phrase_time_limit=PHRASE_TIME_LIMIT
            )
            log("[*] Audio captured, recognizing...", log_text)
        except sr.WaitTimeoutError:
            log("[-] Listening timed out (no speech)", log_text)
            return ""

    try:
        text = recognizer.recognize_google(audio).lower()
        log(f"[?] Recognized: \"{text}\"", log_text)
        return text
    except sr.UnknownValueError:
        log("[!] Could not understand audio", log_text)
        return ""
    except sr.RequestError as e:
        log(f"[!] Speech API error: {e}", log_text)
        return ""

def play_wake_sound(log_text=None):
    if pygame and os.path.exists(WAKE_SOUND_PATH):
        try:
            log(f"♪ Playing wake sound: {WAKE_SOUND_PATH}", log_text)
            pygame.mixer.music.load(WAKE_SOUND_PATH)
            pygame.mixer.music.play()
        except Exception as e:
            log(f"[!] Error playing sound: {e}", log_text)
    else:
        if not pygame:
            log("[!] Pygame unavailable.", log_text)
        else:
            log(f"[!] Sound file not found at: {WAKE_SOUND_PATH}", log_text)