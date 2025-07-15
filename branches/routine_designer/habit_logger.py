_habit_log = {}

def log_habit(user_id, task):
    import time
    _habit_log.setdefault(user_id, []).append({ "task": task, "timestamp": time.time() })
    return { "logged": task }

def get_user_habits(user_id):
    return _habit_log.get(user_id, [])
