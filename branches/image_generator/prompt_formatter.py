import json
import os

def format_prompt(prompt, persona=None):
    style = persona.get("style", "realistic") if persona else "realistic"
    theme = persona.get("theme", "") if persona else ""

    try:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_path, "r") as f:
            config = json.load(f)
    except:
        config = {}

    modifiers = config.get("styles", {})
    style_modifier = modifiers.get(style, "high detail, cinematic lighting")

    full_prompt = f"{prompt}, {style_modifier}"
    if theme:
        full_prompt += f", Theme: {theme}"

    return full_prompt
