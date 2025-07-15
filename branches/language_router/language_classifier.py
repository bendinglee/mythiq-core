def detect_lang(text):
    if text.strip().startswith("¿"):
        return "Spanish"
    if "bonjour" in text.lower():
        return "French"
    return "English"
