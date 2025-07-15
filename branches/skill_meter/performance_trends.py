def get_skill_trends():
    from .score_comparator import _skill_log
    trends = {}
    for entry in _skill_log[-100:]:
        skill = entry["skill"]
        score = entry["score"]
        trends.setdefault(skill, []).append(score)

    spark = lambda lst: "".join("█" if s > 7 else "░" for s in lst[-10:])
    return { skill: spark(vals) for skill, vals in trends.items() }
