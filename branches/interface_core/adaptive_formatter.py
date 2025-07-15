def format_output(text, mode="default"):
    if mode == "mobile":
        return text[:80] + "…" if len(text) > 80 else text
    if mode == "voice":
        return text.replace("\n", " ").replace("...", "")
    return text
