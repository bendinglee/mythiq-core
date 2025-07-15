_skill_log = []

def log_skill_score(payload):
    import time
    entry = {
        "skill": payload.get("skill", "unknown"),
        "score": payload.get("score", 0),
        "note": payload.get("note", ""),
        "timestamp": time.time()
    }
    _skill_log.append(entry)
    return { "logged": entry }

def get_latest_scores():
    from collections import defaultdict
    scores = defaultdict(list)
    for e in _skill_log[-50:]:
        scores[e["skill"]].append(e["score"])
    return { skill: sum(vals)/len(vals) for skill, vals in scores.items() if vals }
