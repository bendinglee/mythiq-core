def detect_shift(turns):
    persona_changes = 0
    last_style = None
    for turn in turns:
        style = turn.get("style", "")
        if last_style and style != last_style:
            persona_changes += 1
        last_style = style
    return { "persona_shifts": persona_changes }
