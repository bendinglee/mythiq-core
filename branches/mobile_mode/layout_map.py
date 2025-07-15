def mobile_format(text):
    return text[:80] + "…" if len(text) > 80 else text
