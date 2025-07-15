def detect_uncertainty(response):
    keywords = ["I don't know", "unsure", "perhaps", "maybe"]
    score = sum(1 for word in keywords if word in response.lower())
    return round((1 - score / len(keywords)) * 100, 2)
