def adjust_routine(routine, feedback):
    if "too much" in feedback:
        return routine[:-1]
    if "add break" in feedback:
        routine.insert(1, { "time": "10:30", "task": "Rest" })
    return routine
