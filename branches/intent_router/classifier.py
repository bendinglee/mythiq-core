def classify_intent(text):
    lower = text.lower()
    if "math" in lower:
        return "math"
    if "translate" in lower:
        return "translation"
    return "fallback"
