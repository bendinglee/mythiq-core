_cached_trends = [
    "AI ethics debate",
    "Open-source LLM accelerators",
    "Synthetic media legislation"
]

def get_trends():
    return _cached_trends[-3:]

def update_trend(trend):
    _cached_trends.append(trend)
    return _cached_trends[-3:]
