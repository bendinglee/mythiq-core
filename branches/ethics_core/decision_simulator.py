def simulate_decision(option_a, option_b, values):
    def score(option):
        score = 0
        for key in option:
            score += option[key] * values.get(key, 1)
        return score

    score_a = score(option_a)
    score_b = score(option_b)

    return { "choice": "A" if score_a > score_b else "B", "score": { "A": score_a, "B": score_b } }
