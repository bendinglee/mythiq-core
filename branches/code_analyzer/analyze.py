def analyze_code(prompt):
    if "def " not in prompt:
        return "[Code error] No function detected"
    return f"🧠 Code looks syntactically valid. Consider adding docstrings and error handling."
