triggers = ["alert", "failure", "conflict"]

def is_priority(signal):
    return any(t in signal.lower() for t in triggers)
