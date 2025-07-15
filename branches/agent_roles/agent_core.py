def simulate(payload):
    role = payload.get("role", "advisor")
    tone = payload.get("tone", "wise")
    task = payload.get("task", "analyze problem")

    return {
        "role": role,
        "tone": tone,
        "task": task,
        "response": f"[{role.upper()}]: Executing task with {tone} tone → Insightful output for: {task}"
    }
