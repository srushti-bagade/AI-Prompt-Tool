
````markdown
# 🧠 AI Prompt Companion Tool

An intelligent, desktop-based AI assistant built with Python.  
This tool lets users interact with AI using voice or text prompts, and receive responses from the Claude 3 Haiku model via OpenRouter API. It also supports PDF export, prompt categories, and a friendly GUI.

---

## 📌 Features

✨ Easy-to-use graphical interface with categorized prompts  
🎤 **Voice Input** using `speech_recognition`  
📢 **Text-to-Speech (TTS)** using `pyttsx3`  
🧠 AI responses powered by **Claude 3 Haiku** via **OpenRouter API**  
📄 **PDF Export** of full conversations  
📦 Organized code structure for easy extension  

---


## 🧰 Modules & Installation

### 🔧 Install Required Packages

Create a virtual environment (optional but recommended):

python -m venv venv
venv\Scripts\activate  # On Windows
````

Now install the dependencies:

```bash
pip install pyttsx3
pip install SpeechRecognition
pip install requests
pip install Pillow
pip install fpdf
```

Or install everything at once using `requirements.txt` (you can create it later):

```bash
pip install -r requirements.txt
```

### 🧾 Example `requirements.txt`:

```
pyttsx3
SpeechRecognition
requests
Pillow
fpdf
```

---

## 🔑 Setup OpenRouter API

1. Get your free API key from: [https://openrouter.ai](https://openrouter.ai)
2. Replace the placeholder in `main.py`:

   ```python
   API_KEY = "your_openrouter_api_key"
   MODEL = "anthropic/claude-3-haiku"
   ```

---

## 🚀 How to Run

After installing modules and setting your API key:

```bash
python main.py
```

You’ll see a GUI where you can:

* Enter or speak a prompt
* Select a prompt category (e.g., Q\&A, Summarize)
* Get an AI response
* Export the chat to PDF

---

## 📁 Project Structure

```
AI_PROMPT_TOOL/
├── main.py
├── screenshots/
│   ├──AI-Tool_UI
│   └── pdf_export.png......
├── exported_conversations/
├── requirements.txt
└── README.md
```

---

## ⭐ About the Author

Developed by **[Srushti Bagade](https://github.com/srushti-bagade)**
For academic/portfolio use – feel free to fork, use, and contribute!

---

