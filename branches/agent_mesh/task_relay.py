def relay_task(task):
    agent_id = task.get("target")
    instruction = task.get("task", "")
    from .agent_registry import agents
    if agent_id in agents:
        return { "to": agent_id, "task": instruction }
    return { "error": "Agent not found" }
