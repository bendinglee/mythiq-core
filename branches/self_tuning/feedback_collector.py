_feedback_log = []

def update_score(data):
    import time
    score = {
        "timestamp": time.time(),
        "rating": data.get("rating", 0),
        "route": data.get("route"),
        "notes": data.get("notes", "")
    }
    _feedback_log.append(score)
    return { "message": "Score logged", "latest": score }
