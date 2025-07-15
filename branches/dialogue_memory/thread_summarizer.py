def summarize_thread(turns):
    topics = set()
    for turn in turns:
        if "dream" in turn["user"]:
            topics.add("imagination")
        if "strategy" in turn["user"]:
            topics.add("planning")
        if "emotion" in turn["user"]:
            topics.add("sentiment")
    return { "topics": list(topics), "total_turns": len(turns) }
