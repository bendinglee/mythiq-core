agents = {}

def connect_agent(data):
    agent_id = data.get("id")
    agents[agent_id] = { "name": data.get("name"), "url": data.get("url") }
    return { "connected": agent_id }

def list_agents():
    return list(agents.keys())
