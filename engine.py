import json
import math
import turtle
from groq import Groq

SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "background": {"type": "string"},
        "commands": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "shape": {
                        "type": "string",
                        "enum": ["rectangle", "circle", "line", "polygon", "parametric"]
                    },
                    "color": {"type": "string"},
                    "x": {"type": "integer"},
                    "y": {"type": "integer"},
                    "width": {"type": "integer"},
                    "height": {"type": "integer"},
                    "radius": {"type": "integer"},
                    "x2": {"type": "integer"},
                    "y2": {"type": "integer"},
                    "rotation": {"type": "integer"},
                    "points": {"type": "array", "items": {"type": "array", "items": {"type": "integer"}}},
                    "x_formula": {"type": "string"},
                    "y_formula": {"type": "string"},
                    "t_start": {"type": "number"},
                    "t_end": {"type": "number"}
                },
                "required": ["shape", "color"]
            }
        }
    },
    "required": ["title", "background", "commands"]
}

def get_active_model(client):
    """Dynamically select a valid text chat model."""
    all_models = [m.id for m in client.models.list().data]
    chat_models = [
        m for m in all_models
        if not any(bad in m.lower() for bad in ["whisper", "audio", "vision", "guard", "embed", "safeguard", "canopylabs"])
    ]
    return chat_models[0] if chat_models else "llama-3.1-8b-instant"

def generate_plan(client, model, prompt):
    """Fetch structured drawing steps from Groq."""
    system_instruction = (
        "You are a mathematical vector graphic generator for Python Turtle.\n"
        "Canvas bounds: X: -200 to 200, Y: -200 to 200.\n"
        "Shapes: 'rectangle', 'circle', 'line', 'polygon', 'parametric'.\n"
        "For organic shapes, use 'parametric' with 'x_formula', 'y_formula' in terms of 't'.\n"
        "Return strictly JSON matching this schema:\n" + json.dumps(SCHEMA)
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )
    return json.loads(response.choices[0].message.content)

def render_drawing(plan, t, screen):
    """Render drawing commands on the Turtle canvas."""
    t.speed(4)
    screen.bgcolor(plan.get("background", "white"))

    for cmd in plan.get("commands", []):
        shape = cmd.get("shape")
        color = cmd.get("color", "black")
        x = cmd.get("x", 0)
        y = cmd.get("y", 0)

        t.penup()

        if shape == "parametric":
            x_eq = cmd.get("x_formula", "100 * cos(t)")
            y_eq = cmd.get("y_formula", "100 * sin(t)")
            t_start = cmd.get("t_start", 0)
            t_end = cmd.get("t_end", 6.28)
            rotation_deg = cmd.get("rotation", 0)
            rad = math.radians(rotation_deg)

            math_namespace = {
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "pi": math.pi, "sqrt": math.sqrt, "abs": abs,
                "exp": math.exp, "pow": math.pow
            }

            steps = 100
            final_points = []

            for i in range(steps + 1):
                t_val = t_start + (t_end - t_start) * (i / steps)
                math_namespace["t"] = t_val

                try:
                    rx = eval(x_eq, {"__builtins__": None}, math_namespace)
                    ry = eval(y_eq, {"__builtins__": None}, math_namespace)

                    rot_x = rx * math.cos(rad) - ry * math.sin(rad)
                    rot_y = rx * math.sin(rad) + ry * math.cos(rad)

                    final_points.append((x + rot_x, y + rot_y))
                except Exception:
                    break

            if final_points:
                t.goto(final_points[0][0], final_points[0][1])
                t.pendown()
                t.color(color)
                t.fillcolor(color)
                t.begin_fill()
                for px, py in final_points[1:]:
                    t.goto(px, py)
                t.end_fill()

        elif shape == "rectangle":
            w, h = cmd.get("width", 50), cmd.get("height", 50)
            t.goto(x - w / 2, y + h / 2)
            t.pendown()
            t.color(color)
            t.fillcolor(color)
            t.begin_fill()
            for _ in range(2):
                t.forward(w)
                t.right(90)
                t.forward(h)
                t.right(90)
            t.end_fill()

        elif shape == "circle":
            r = cmd.get("radius", 20)
            t.goto(x, y - r)
            t.pendown()
            t.color(color)
            t.fillcolor(color)
            t.begin_fill()
            t.circle(r)
            t.end_fill()

        elif shape == "line":
            x2, y2 = cmd.get("x2", 0), cmd.get("y2", 0)
            t.goto(x, y)
            t.pendown()
            t.pencolor(color)
            t.pensize(3)
            t.goto(x2, y2)
            t.pensize(1)

    t.hideturtle()