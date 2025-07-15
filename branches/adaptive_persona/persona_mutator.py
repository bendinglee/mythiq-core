def adapt_persona(signal):
    if "angry" in signal:
        new_style = "calm"
    elif "excited" in signal:
        new_style = "balanced"
    else:
        new_style = "neutral"

    from branches.persona_settings.persona_manager import set_persona
    set_persona({ "style": new_style })
    from .evolution_tracker import track_style
    track_style(new_style)

    return { "adapted_style": new_style }
