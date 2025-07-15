def execute_safe(trigger):
    try:
        return f"Executed {trigger}"
    except:
        return "Fallback execution"
