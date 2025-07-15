def train_agent(agent_id, lesson):
    return {
        "target": agent_id,
        "lesson_sent": lesson,
        "status": "training initialized"
    }
