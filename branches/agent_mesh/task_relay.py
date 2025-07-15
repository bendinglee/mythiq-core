from .agent_registry import agents

# 🚦 Relay a task to a known agent in the mesh
def relay_task(task):
    agent_id = task.get("target")
    instruction = task.get("task", "")
    payload = task.get("payload", {})

    if agent_id not in agents:
        return {
            "status": "error",
            "message": f"Agent '{agent_id}' not found.",
            "available_agents": list(agents.keys())
        }

    agent = agents[agent_id]
    return {
        "status": "relayed",
        "to": agent_id,
        "task": instruction,
        "agent_signature": {
            "name": agent.get("name"),
            "modules": agent.get("modules"),
            "personality": agent.get("personality")
        },
        "payload": payload,
        "message": f"Task '{instruction}' routed to agent '{agent_id}' successfully."
    }
