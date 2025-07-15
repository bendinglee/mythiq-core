def evaluate_offer(price, features):
    score = len(features) * 10 / (price + 1)
    return round(score, 2)
