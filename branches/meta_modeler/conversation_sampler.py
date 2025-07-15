def sample_for_training(turns):
    return [
        { "input": t["user"], "output": t["ai"] }
        for t in turns
    ]
