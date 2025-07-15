style_log = []

def track_style(style):
    style_log.append(style)

def get_style_stats():
    from collections import Counter
    return Counter(style_log[-100:])
