_goal_log = []

def log_goal(text, steps, result):
    _goal_log.append({ "goal": text, "steps": steps, "executed": result })

def get_goal_log():
    return _goal_log[-5:]
