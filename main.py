from tkinter import *
from tkinter import ttk, scrolledtext, messagebox, filedialog
import requests
from PIL import Image, ImageTk
import pyttsx3
import speech_recognition as sr
from fpdf import FPDF

# --- Claude 3 Haiku via OpenRouter API ---
API_KEY = "YOUR_API_KEY"
MODEL = "anthropic/claude-3-haiku"

conversation_history = []  # To store (prompt, response) pairs

# Initialize Text-to-Speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 160)
voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voice', voices[1].id)  # female

def get_ai_response(prompt, category, role):
    if category == "Summarization":
        prompt = f"Summarize this text:\n{prompt}"
    elif category == "Code Help":
        prompt = f"Help me with this code issue:\n{prompt}"
    elif category == "Grammar Check":
        prompt = f"Correct the grammar of this:\n{prompt}"
    elif category == "General":
        prompt = f"Explain:\n{prompt}"
    if role and role != "None":
        prompt = f"As a {role}, respond to the following:\n{prompt}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://chat.openai.com",
        "X-Title": "Prompt Companion Tool",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

def speak_response():
    text = response_box.get("1.0", END).strip()
    if text:
        tts_engine.say(text)
        tts_engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Speak Now", "Listening... Speak your prompt.")
        audio = recognizer.listen(source)
    try:
        prompt = recognizer.recognize_google(audio)
        prompt_entry.insert(END, prompt)
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Could not understand audio.")
    except sr.RequestError:
        messagebox.showerror("Error", "Speech Recognition request failed.")

def export_to_pdf():
    if not conversation_history:
        messagebox.showwarning("No History", "No conversation to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for i, (prompt, response) in enumerate(conversation_history, 1):
        pdf.multi_cell(0, 10, f"Prompt {i}: {prompt}\nResponse {i}: {response}\n", border=0)
    pdf.output(file_path)
    messagebox.showinfo("Exported", f"Conversation exported to {file_path}")

def send_prompt():
    user_input = prompt_entry.get("1.0", END).strip()
    if not user_input:
        messagebox.showwarning("Input Error", "Please enter a prompt.")
        return
    category = category_var.get()
    role = role_var.get()
    response_box.delete("1.0", END)
    response_box.insert(END, "Thinking...\n")
    root.update()
    response = get_ai_response(user_input, category, role)
    response_box.delete("1.0", END)
    response_box.insert(END, response)
    conversation_history.append((user_input, response))

def on_enter(e): e.widget.config(bg="#5a9bd5")
def on_leave(e): e.widget.config(bg=e.widget.default_bg)

# --- UI Setup ---
root = Tk()
root.title("Prompt Companion Tool")
root.geometry("800x800")
root.configure(bg="#f0f8ff")

# Icon
try:
    img = Image.open("/mnt/data/ai_icon.png").resize((50, 50))
    icon = ImageTk.PhotoImage(img)
    Label(root, image=icon, bg="#f0f8ff").pack(pady=10)
except:
    Label(root, text="🤖", font=("Arial", 36), bg="#f0f8ff").pack(pady=10)

Label(root, text="Hi, I'm your AI Companion 👋", font=("Arial", 18, "bold"), fg="#1e3d59", bg="#f0f8ff").pack()
Label(root, text="Prompt Companion Tool", font=("Arial", 16, "bold"), fg="#2f4f4f", bg="#f0f8ff").pack(pady=(0, 10))

frame = Frame(root, bg="#f0f8ff")
frame.pack(pady=10)

Label(frame, text="Prompt Category:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, padx=5)
category_var = StringVar()
category_dropdown = ttk.Combobox(frame, textvariable=category_var,
                                 values=["General", "Summarization", "Code Help", "Grammar Check"],
                                 state="readonly", width=18)
category_dropdown.set("General")
category_dropdown.grid(row=0, column=1, padx=5)

Label(frame, text="Respond As (Role):", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=2, padx=5)
role_var = StringVar()
role_dropdown = ttk.Combobox(frame, textvariable=role_var,
                             values=["None", "Teacher", "Doctor", "Programmer", "Counselor", "Chef", "Poet"],
                             state="readonly", width=18)
role_dropdown.set("None")
role_dropdown.grid(row=0, column=3, padx=5)

Label(root, text="Enter your prompt:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
prompt_entry = Text(root, height=5, width=90, wrap=WORD, font=("Arial", 11))
prompt_entry.pack(padx=20, pady=5)

Label(root, text="AI Response:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
response_box = scrolledtext.ScrolledText(root, height=20, width=90, wrap=WORD,
                                         font=("Arial", 11), padx=10, pady=10,
                                         bg="#fffaf0", fg="#000000")
response_box.pack(padx=20, pady=5)

button_frame = Frame(root, bg="#f0f8ff")
button_frame.pack(pady=10)

buttons = [
    ("🎤 Voice Input", speech_to_text, "#fdd835"),
    ("Generate Response", send_prompt, "#4682b4"),
    ("🔊 Speak Response", speak_response, "#98fb98"),
    ("Export to PDF", export_to_pdf, "#b0e0e6"),
    ("Clear", lambda: [prompt_entry.delete("1.0", END), response_box.delete("1.0", END)], "#dcdcdc"),
    ("Exit", root.destroy, "#f08080")
]

for i, (label, cmd, color) in enumerate(buttons):
    btn = Button(button_frame, text=label, font=("Arial", 12), command=cmd, bg=color,
                 padx=10, pady=5, width=16)
    btn.default_bg = color
    btn.grid(row=0, column=i, padx=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

root.mainloop()
