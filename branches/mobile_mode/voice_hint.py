def generate_hint(command):
    if "help" in command:
        return { "hint": "Try saying: 'Show me my mood' or 'Generate an image'" }
    return { "hint": "Say a task or ask a question" }
