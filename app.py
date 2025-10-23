"""
AI Translator Desktop App
-----------------------------------
Features:
- Text Translation (auto-detect or user-select source)
- Speech-to-Text
- Speech-to-Speech Translation
- Text-to-Speech Playback
- Real-Time Speech Translation (continuous)
- Saves Translation History (CSV)
- Modern Tkinter UI
Compatible with Python 3.13+
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from deep_translator import GoogleTranslator
from gtts import gTTS
from langdetect import detect
import speech_recognition as sr
import pyperclip
import threading
import csv
import time
import os
from playsound import playsound

# ---------------------- CONFIGURATION ----------------------
HISTORY_FILE = "translation_history.csv"

LANGUAGES = {
    'Auto Detect': 'auto',
    'English': 'en', 'French': 'fr', 'Spanish': 'es', 'German': 'de',
    'Italian': 'it', 'Portuguese': 'pt', 'Arabic': 'ar',
    'Chinese (Simplified)': 'zh-CN', 'Japanese': 'ja',
    'Korean': 'ko', 'Russian': 'ru'
}

# ---------------------- UTILITY FUNCTIONS ----------------------
def save_history(mode, source_lang, target_lang, source_text, translated_text):
    """Append translation event to CSV history."""
    file_exists = os.path.isfile(HISTORY_FILE)
    with open(HISTORY_FILE, "a", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["timestamp", "mode", "source_lang", "target_lang", "source_text", "translated_text"])
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            mode,
            source_lang,
            target_lang,
            source_text,
            translated_text
        ])

def detect_language(text):
    """Use langdetect to determine language code."""
    try:
        return detect(text)
    except:
        return "unknown"

def play_audio(file_path):
    """Play audio in a non-blocking thread."""
    threading.Thread(target=lambda: playsound(file_path)).start()

# ---------------------- TRANSLATION FUNCTIONS ----------------------
def translate_text():
    """Handle text translation based on user inputs."""
    text = input_text.get("1.0", tk.END).strip()
    src_lang_label = source_lang_var.get()
    tgt_lang_label = target_lang_var.get()
    target_lang = LANGUAGES[tgt_lang_label]

    if not text:
        messagebox.showwarning("Warning", "Please enter text to translate.")
        return

    # Detect language if set to auto
    if src_lang_label == 'Auto Detect':
        detected_lang = detect_language(text)
        src_lang_label = [k for k, v in LANGUAGES.items() if v == detected_lang]
        source_code = detected_lang if detected_lang != "unknown" else "auto"
    else:
        source_code = LANGUAGES[src_lang_label]

    try:
        translated = GoogleTranslator(source=source_code, target=target_lang).translate(text)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)
        save_history("text", source_code, target_lang, text, translated)
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed:\n{e}")

def copy_translation():
    """Copy translated text to clipboard."""
    translated = output_text.get("1.0", tk.END).strip()
    if translated:
        pyperclip.copy(translated)
        messagebox.showinfo("Copied", "Translation copied to clipboard!")

def text_to_speech():
    """Convert translated text to speech."""
    translated = output_text.get("1.0", tk.END).strip()
    target_lang = LANGUAGES[target_lang_var.get()]
    if not translated:
        messagebox.showwarning("Warning", "No translation available.")
        return
    try:
        tts = gTTS(translated, lang=target_lang)
        tts.save("translation.mp3")
        play_audio("translation.mp3")
    except Exception as e:
        messagebox.showerror("Error", f"Text-to-Speech failed:\n{e}")

def speech_to_text():
    """Convert spoken words to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Speak", "Please speak now...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, text)
        messagebox.showinfo("Speech Recognized", f"Detected: {text}")
    except Exception as e:
        messagebox.showerror("Error", f"Speech Recognition failed:\n{e}")

def speech_to_speech():
    """Convert speech directly to translated speech."""
    recognizer = sr.Recognizer()
    target_lang = LANGUAGES[target_lang_var.get()]
    with sr.Microphone() as source:
        messagebox.showinfo("Speak", "Please speak for translation...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        detected_lang = detect_language(text)
        translated = GoogleTranslator(source=detected_lang, target=target_lang).translate(text)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)
        tts = gTTS(translated, lang=target_lang)
        tts.save("speech_translation.mp3")
        play_audio("speech_translation.mp3")
        save_history("speech", detected_lang, target_lang, text, translated)
    except Exception as e:
        messagebox.showerror("Error", f"Speech→Speech failed:\n{e}")

def real_time_translation():
    """Continuously listen and translate speech in real-time."""
    recognizer = sr.Recognizer()
    target_lang = LANGUAGES[target_lang_var.get()]
    messagebox.showinfo("Real-Time Translation", "Listening... Speak clearly.")
    try:
        with sr.Microphone() as source:
            while True:
                audio = recognizer.listen(source, phrase_time_limit=5)
                try:
                    text = recognizer.recognize_google(audio)
                    detected_lang = detect_language(text)
                    translated = GoogleTranslator(source=detected_lang, target=target_lang).translate(text)
                    output_text.insert(tk.END, f"\nYou: {text}\n→ {translated}\n")
                    save_history("real-time", detected_lang, target_lang, text, translated)
                except sr.UnknownValueError:
                    continue
                except Exception:
                    continue
    except KeyboardInterrupt:
        messagebox.showinfo("Stopped", "Real-time translation stopped.")

# ---------------------- GUI SETUP ----------------------
app = tk.Tk()
app.title("AI Translator Desktop App")
app.geometry("700x650")
app.configure(bg="#f5f6fa")

# Title
tk.Label(app, text="AI Translator", font=("Segoe UI", 18, "bold"), bg="#f5f6fa").pack(pady=10)

# Language selectors
frame_lang = tk.Frame(app, bg="#f5f6fa")
frame_lang.pack(pady=10)

source_lang_var = tk.StringVar(value='Auto Detect')
target_lang_var = tk.StringVar(value='French')

tk.Label(frame_lang, text="Source Language:", bg="#f5f6fa").grid(row=0, column=0, padx=10)
source_menu = ttk.Combobox(frame_lang, textvariable=source_lang_var, values=list(LANGUAGES.keys()), state='readonly', width=25)
source_menu.grid(row=0, column=1)

tk.Label(frame_lang, text="Target Language:", bg="#f5f6fa").grid(row=0, column=2, padx=10)
target_menu = ttk.Combobox(frame_lang, textvariable=target_lang_var, values=list(LANGUAGES.keys()), state='readonly', width=25)
target_menu.grid(row=0, column=3)

# Input Text
tk.Label(app, text="Enter Text or Use Microphone:", bg="#f5f6fa").pack()
input_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=80, height=6)
input_text.pack(pady=5)

# Buttons
frame_buttons = tk.Frame(app, bg="#f5f6fa")
frame_buttons.pack(pady=10)

ttk.Button(frame_buttons, text="Translate Text", command=translate_text).grid(row=0, column=0, padx=5)
ttk.Button(frame_buttons, text="Copy Translation", command=copy_translation).grid(row=0, column=1, padx=5)
ttk.Button(frame_buttons, text="Text-to-Speech", command=text_to_speech).grid(row=0, column=2, padx=5)

# Speech Buttons
frame_speech = tk.Frame(app, bg="#f5f6fa")
frame_speech.pack(pady=10)

ttk.Button(frame_speech, text="Speech-to-Text", command=speech_to_text).grid(row=0, column=0, padx=10)
ttk.Button(frame_speech, text="Speech-to-Speech", command=speech_to_speech).grid(row=0, column=1, padx=10)
ttk.Button(frame_speech, text="Real-Time Speech Translation", command=lambda: threading.Thread(target=real_time_translation).start()).grid(row=0, column=2, padx=10)

# Output Text
tk.Label(app, text="Translated Text:", bg="#f5f6fa").pack()
output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=80, height=8)
output_text.pack(pady=5)

# Footer
tk.Label(app, text="Developed by Perry | AI Translator © 2025", font=("Segoe UI", 9), bg="#f5f6fa", fg="gray").pack(pady=5)

app.mainloop()
