_turn_log = []

def log_turn(user_input, ai_response):
    import time
    _turn_log.append({
        "user": user_input,
        "ai": ai_response,
        "timestamp": time.time()
    })

def get_turns():
    return _turn_log[-5:]
