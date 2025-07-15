def expand_interest(topic):
    mapping = {
        "AI": ["neural networks", "self-learning", "ethics"],
        "creativity": ["storytelling", "music synthesis", "worldbuilding"]
    }
    return mapping.get(topic, ["research", "innovation", "design"])
