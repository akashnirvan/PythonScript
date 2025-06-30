# 🤖 Jarvis Voice Assistant

Welcome to **Jarvis**, your personal AI-powered voice assistant. Whether you're just starting out in development or looking to build something meaningful with Python, this assistant is built to make your journey exciting, hands-on, and deeply rewarding.

This project blends voice recognition, GUI design, AI search (via Gemini), and desktop automation — all wrapped in a beginner-friendly interface.

---

## 🚀 What Can Jarvis Do?

| Mode                   | Description                                                                                            |
| ---------------------- | ------------------------------------------------------------------------------------------------------ |
| 🎙 Wake Word Mode      | Jarvis listens for the word "hello" and then activates listening automatically.                        |
| ⚡ Instant Command Mode | Jarvis listens instantly without needing any wake word. You can adjust how long it listens (1–10 sec). |
| 💬 Chat Mode           | No microphone needed. Just type your commands and get responses via Gemini AI.                         |

---

## 💻 Who Is This For?

* 🧒 **Beginners** who want to learn real-world Python projects
* 🎙 Creators interested in building voice assistants
* 🧠 Curious minds who want to mix GUI + AI + automation
* 💼 Developers who want to package apps as `.exe` files

If you’ve ever wanted to **build your own Jarvis** — this is your start.

---

## 🧰 Tech Stack Used

* **Python 3.8+**
* `tkinter` (GUI)
* `speech_recognition` (Voice commands)
* `pyttsx3` (Text-to-Speech)
* `requests` (API calling)
* `pyaudio` (Microphone input)
* Gemini AI (via Google API)

---

## 📦 Installation Guide

> If you want to run from Python (dev mode), follow these steps:

### 1. Clone the Repository(Make sure git is installed)

```bash
cd path/to/your/folder
```
```
git clone https://github.com/akashnirvan/Assistant.git
```
```
cd Assistant
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

#### If `pyaudio` gives errors (common for beginners):

```bash
pip install pipwin
pipwin install pyaudio
```

---
## Some Tweak
```env
WAKER=hello
API_KEY = AIzaSyAEey2pCZn7pnWMsI1lEZ0UivR39l_9dhs
MAX_MESSAGES =10
```
* <b>you can edit WAKER so that it start to respond by your prefer word</b>
* <b>add a Api keys of a gemini </b>
* <b>Max message is for how many message it shows in a chat then delete previous one<b>
## ▶️ Running the Assistant

```bash
python Assistant.py
```

You’ll see a GUI window with three buttons:

* **Wake Word Mode**
* **Instant Command Mode** (includes a slider to control how long it listens)
* **Chat Mode** (input + send button)

---

## 🔐 Gemini AI Setup

This assistant uses **Google Gemini API** to answer queries smartly.

### How to Get Your API Key:

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google Account
3. Copy your API key
4. Paste it in the code like this:

```python
API_KEY = "your-api-key-here"
```

Now Jarvis can answer any question using Gemini’s AI engine.

---

## 🧪 Sample Commands You Can Try

| Command                    | Action                                 |
| -------------------------- | -------------------------------------- |
| `open youtube.com`         | Opens YouTube in your browser          |
| `search latest tech news`  | Searches Google for "latest tech news" |
| `answer me what is python` | Gemini AI gives a short answer         |
| `stop`                     | Gracefully shuts down the assistant    |

In **Chat Mode**, you can type the same commands instead of speaking.

---

## 🪄 Build `.exe` File (Windows Users)

If you want to make a standalone `.exe` file:

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Create Executable

```bash
pyinstaller --onefile --noconsole jarvis_gui.py
```

Your `.exe` will appear in the `/dist` folder. You can now share it without requiring Python.

---

## 🌟 Bonus Features

* Message bubbles appear in chat-style layout (like WhatsApp)
* Gemini answers are cleaned (no long markdown or bullets)
* All commands are logged in the UI in a beautiful way
* Uses threading so voice loop doesn’t freeze your GUI

---

## 🧠 Beginner Tips

* Don’t worry if voice doesn’t work at first — check your mic permissions
* Always test with headphones to avoid mic feedback
* Start with Chat Mode if you're not confident speaking
* This project helps you understand **event loops**, **threading**, **APIs**, and **desktop UI design**

---

## 🧑‍💻 Author & Credits

Built with ❤️ by \[Your Name]

Feel free to fork, modify, or extend this to make it your own AI-powered system.

If this project helped you, consider giving a ⭐ on GitHub.

---

## 📜 License

This project is open-source and free to use for personal or educational purposes.
