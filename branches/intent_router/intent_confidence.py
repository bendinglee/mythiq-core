def intent_confidence(intent, text):
    return 90 if intent != "fallback" else 40
