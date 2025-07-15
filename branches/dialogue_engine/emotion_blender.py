def blend_emotion(text, current_emotion):
    if "sad" in text.lower():
        return f"Tone shifted from {current_emotion} to empathetic."
    if "angry" in text.lower():
        return f"Tone adjusted to firm resolution."
    return f"Continuing with {current_emotion} tone."
