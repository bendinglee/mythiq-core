agents = {}

# 🔗 Register an agent to the mesh
def connect_agent(data):
    agent_id = data.get("id", f"agent-{len(agents)+1}")
    agents[agent_id] = {
        "name": data.get("name", "Unnamed"),
        "url": data.get("url", "N/A"),
        "modules": data.get("modules", []),
        "personality": data.get("personality", {
            "tone": "Neutral",
            "style": "Default",
            "goal": "Unassigned"
        })
    }
    return {
        "connected": agent_id,
        "agent": agents[agent_id],
        "message": f"Agent '{agent_id}' successfully registered."
    }

# 📋 Get list of registered agent IDs
def list_agents():
    return list(agents.keys())

# 🔍 Get full agent details by ID
def get_agent_details(agent_id):
    return agents.get(agent_id, { "error": "Agent not found" })
