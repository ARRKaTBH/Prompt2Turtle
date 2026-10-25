import os
import turtle
from groq import Groq
import engine

# Load the API key from a local .env file if available.
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.isfile(env_path):
    with open(env_path, encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                name, value = line.split("=", 1)
                os.environ.setdefault(name.strip(), value.strip().strip("\"'"))

api_key = os.getenv("GROQ_API_KEY")

# Prompt user for API key if missing
if not api_key:
    api_key = input("Enter your Groq API Key (gsk_...): ").strip()

client = Groq(api_key=api_key)

print("Fetching active Groq models...")
selected_model = engine.get_active_model(client)
print(f"Using model: {selected_model}\n")

screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.title("Prompt2Turtle Engine")

t = turtle.Turtle()

while True:
    user_prompt = input("\nWhat do you want to draw? (or type 'exit' to quit): ").strip()
    if user_prompt.lower() in ["exit", "quit"]:
        break

    try:
        t.clear()
        t.reset()
    except Exception:
        screen = turtle.Screen()
        screen.setup(width=600, height=600)
        t = turtle.Turtle()

    print("Generating drawing plan...")
    try:
        plan = engine.generate_plan(client, selected_model, user_prompt)
        engine.render_drawing(plan, t, screen)
    except Exception as e:
        print(f"Error executing prompt: {e}")

turtle.done()