_log = []

def log_turn(user_text, ai_text, emotion="neutral", style="default"):
    import time
    _log.append({
        "user": user_text,
        "ai": ai_text,
        "emotion": emotion,
        "style": style,
        "ts": time.time()
    })

def get_recent_turns(n=5):
    return _log[-n:]
