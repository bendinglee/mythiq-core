def switch_style(text, theme="dark"):
    if theme == "minimal":
        return f"[Minimal]\n{text}"
    if theme == "branded":
        return f"[Mythiq Style 🌌]\n{text}"
    return text
