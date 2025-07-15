_learning_log = []

def log_training_event(data):
    _learning_log.append({
        "timestamp": __import__("time").time(),
        "event": data
    })
    return True

def get_learning_history():
    return _learning_log[-10:]
