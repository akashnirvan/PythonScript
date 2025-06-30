import tkinter as tk
import speech_recognition as sr
import webbrowser
import pyttsx3
import threading
import requests
import re
from dotenv import load_dotenv
import os
import requests
load_dotenv()

API_KEY = os.getenv("API_KEY")
GEMINI_MODEL = "models/gemini-2.0-flash"
WAKER=os.getenv("WAKER")
listen_duration = 5  # Default time for instant mode listening

def clean_gemini_text(text):
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'^\s*[-•]\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def ask_gemini(prompt):
    short_prompt = f"{prompt}. Keep the answer short and clear in 3-4 lines only."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": short_prompt}]}]}
    try:
        res = requests.post(url, headers=headers, json=data)
        res.raise_for_status()
        response = res.json()
        return clean_gemini_text(response["candidates"][0]["content"]["parts"][0]["text"])
    except Exception as e:
        return f"Gemini error: {e}"

# --- GUI Setup ---
root = tk.Tk()
root.title("Assistant Chat UI")
root.geometry("420x560")
root.configure(bg="#111")

frame = tk.Frame(root, bg="#111")
frame.pack(fill="both", expand=True)

canvas = tk.Canvas(frame, bg="#111", highlightthickness=0)
scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#111")
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

message_bubbles = []
MAX_MESSAGES=os.getenv("MAX_MESSAGES") 

def add_message(message, is_user=False, disappear=False):
    bubble = tk.Label(
        scrollable_frame,
        text=message,
        bg="#00BFFF" if not is_user else "#444",
        fg="white",
        wraplength=300,
        justify="left" if not is_user else "right",
        anchor="w" if not is_user else "e",
        padx=10,
        pady=5,
        font=("Helvetica", 11),
        relief="ridge",
        bd=5
    )
    bubble.pack(anchor="w" if not is_user else "e", pady=4, padx=10)
    message_bubbles.append(bubble)
    if len(message_bubbles) > int(MAX_MESSAGES):
        old = message_bubbles.pop(0)
        old.destroy()
    if disappear:
        bubble.after(6000, lambda: (bubble.destroy(), message_bubbles.remove(bubble)))

# --- Speech Recognition and TTS ---
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    if not chat_mode:
        add_message(text)
        engine.say(text)
        engine.runAndWait()
    else:
        add_message(text)

def listen(timeout=5, phrase_time_limit=None):
    try:
        with sr.Microphone() as source:
            add_message("🎤 Adjusting for noise...")
            # recognizer.adjust_for_ambient_noise(source, duration=1)
            add_message("🎙️ Listening for speech...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            return audio
    except sr.WaitTimeoutError:
        add_message("❌ No speech detected (timeout).")
        return None
    except Exception as e:
        add_message(f"⚠️ Microphone error: {e}")
        return None

def recognize(audio):
    if not audio:
        return None
    try:
        text = recognizer.recognize_google(audio)
        add_message(text, is_user=True)
        return text.lower()
    except sr.UnknownValueError:
        add_message("❌ Could not understand the audio.")
        return None
    except sr.RequestError as e:
        add_message(f"⚠️ Google API error: {e}")
        speak("Speech service is unavailable.")
        return None

# --- Command Handler ---
def handle_command(command):
    if "open" in command:
        website = command.replace("open", "").strip()
        url = f"https://{website}" if "." in website else f"https://www.google.com/search?q={website}"
        webbrowser.open(url)
        speak(f"Opening {website}")
    elif command.startswith("answer me"):
        query = command.replace("answer me", "").strip()
        if query:
            add_message(f"🤔 Asking Gemini: {query}")
            answer = ask_gemini(query)
            add_message(answer)
            speak(answer)
        else:
            speak("Please provide a question after 'answer me'.")
    elif "search" in command:
        query = command.replace("search", "").strip()
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak(f"Searching for {query}")
    elif "stop" in command:
        speak("Goodbye!")
        root.destroy()
    else:
        speak("I didn’t understand that command.")

# --- Modes ---
wake_mode = False
instant_mode = False
chat_mode = False

def reset_modes():
    global wake_mode, instant_mode, chat_mode
    wake_mode = instant_mode = chat_mode = False
    input_bar.pack_forget()
    send_btn.pack_forget()

# --- Mode Buttons ---
def start_wake_mode():
    reset_modes()
    global wake_mode
    wake_mode = True
    threading.Thread(target=Assistant_loop, daemon=True).start()

def start_instant_mode():
    reset_modes()
    global instant_mode
    instant_mode = True
    threading.Thread(target=instant_listen_loop, daemon=True).start()

def start_chat_mode():
    reset_modes()
    global chat_mode
    chat_mode = True
    input_bar.pack(side="left", padx=5, pady=5, fill="x", expand=True)
    send_btn.pack(side="right", padx=5, pady=5)

def send_chat_command():
    command = input_bar.get().strip().lower()
    if command:
        add_message(command, is_user=True)
        input_bar.delete(0, tk.END)
        handle_command(command)
def update_listen_duration(val):
    global listen_duration
    listen_duration = val

# --- Loop Functions ---
def Assistant_loop():
    speak("Wake word mode activated.")
    while wake_mode:
        add_message(f"🔍 Say {WAKER} to wake me...") 
        wake_audio = listen(timeout=2, phrase_time_limit=2)
        wake_command = recognize(wake_audio)
        if wake_command and WAKER in wake_command:
            speak("How can I help you?")
            for _ in range(2):
                cmd_audio = listen(timeout=int(listen_duration))
                user_cmd = recognize(cmd_audio)
                if user_cmd:
                    handle_command(user_cmd)
                    break
                else:
                    speak("Sorry, I didn’t catch that.")
        elif wake_command and "stop" in wake_command:
            speak("Goodbye!")
            break

def instant_listen_loop():
    speak(f"Instant command mode activated. Listening for {listen_duration} seconds.")
    while instant_mode:
        audio = listen(timeout=listen_duration, phrase_time_limit=listen_duration)
        command = recognize(audio)
        if command:
            handle_command(command)

# --- Bottom Button Panel ---
button_panel = tk.Frame(root, bg="#111")
button_panel.pack(pady=10)
# Slider to control listen time (only for instant mode)
duration_label = tk.Label(root, text="🎚 Listen Duration (Instant Mode):", bg="#111", fg="white")
duration_label.pack(pady=(5, 0))

duration_slider = tk.Scale(root, from_=1, to=10, orient="horizontal", bg="#111", fg="white",
                           troughcolor="#333", highlightthickness=0, command=lambda val: update_listen_duration(int(val)))
duration_slider.set(listen_duration)
duration_slider.pack()


tk.Button(button_panel, text="🎙 Wake Word", command=start_wake_mode, bg="#333", fg="white", width=12).pack(side="left", padx=5)
tk.Button(button_panel, text="⚡ Instant Cmd", command=start_instant_mode, bg="#333", fg="white", width=12).pack(side="left", padx=5)
tk.Button(button_panel, text="💬 Chat Mode", command=start_chat_mode, bg="#333", fg="white", width=12).pack(side="left", padx=5)

# --- Chat Input Bar ---
input_bar = tk.Entry(root, font=("Helvetica", 12))
send_btn = tk.Button(root, text="Send", command=send_chat_command)

# --- Run GUI ---
root.mainloop()
