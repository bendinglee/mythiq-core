def parse_agent_feedback(logs):
    if "confused" in logs:
        return "Reinforce fundamentals"
    elif "easy" in logs:
        return "Advance to next topic"
    return "Repeat module with examples"
