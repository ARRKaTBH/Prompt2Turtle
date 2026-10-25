# 🐢 Prompt2Turtle

**Prompt2Turtle** is an AI-powered vector graphics generation engine built with Python. It leverages Groq's low-latency LLM API to translate natural language prompts into structured JSON execution plans. The engine dynamically calculates mathematical parametric equations ($x(t)$, $y(t)$), applies 2D matrix rotations, and renders organic shapes smoothly using Python's native `turtle` graphics library.

---

## ✨ Features

- **Dynamic Parametric Math Generation**: Rather than guessing pixel points, the LLM generates trigonometric functions in terms of variable $t$ for complex organic shapes (leaves, hearts, stars, spirals, etc.).
- **2D Rotation Matrix & Origin Alignment**: Applies 2D transformation matrices around the origin before translation to ensure shapes are accurately anchored and oriented without asymmetrical offsets.
- **Robust Model Selector**: Automatically fetches and filters active Groq text models while bypassing non-chat endpoints.
- **Tkinter Canvas Recovery**: Native error handling (`turtle.Terminator`) keeps the terminal CLI loop running even if the GUI window is manually closed.
- **Secure Key Management**: Keeps API keys safe using environment variable isolation via `python-dotenv`.

---

## 📁 Repository Structure

```text
Prompt2Turtle/
├── main.py          # Interactive CLI entry point and session handler
├── engine.py        # Core API client, schema, math evaluator, & Turtle renderer
├── .env.example     # Safe template for environment variables
├── .gitignore       # Ensures sensitive keys (.env) are not tracked by Git
└── requirements.txt # Project dependencies

🚀 Getting Started
1. Prerequisites
Python 3.8 or higher installed on your system.

A free Groq API Key.

2. Installation & Setup
Clone the repository:

Bash
git clone [https://github.com/ARRKaTBH/Prompt2Turtle.git](https://github.com/ARRKaTBH/Prompt2Turtle.git)
cd Prompt2Turtle

Install dependencies:

Bash
pip install -r requirements.txt
Configure your API Key:
Copy the .env.example file to create your local .env file:

Bash
cp .env.example .env
Open .env in a text editor and add your Groq API key:

Code snippet
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
🎯 Usage
Run the main application entry point:

Bash
python main.py
Example Prompts:
"draw a green leaf"

"draw a red heart floating above a blue rectangle"

"draw 2 yellow stars pointing upwards"

"type 'exit' to quit the application"
