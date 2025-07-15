def infer_emotion(text):
    if "love" in text.lower():
        return "joyful"
    elif "hate" in text.lower():
        return "angry"
    elif "okay" in text.lower():
        return "calm"
    else:
        return "neutral"
