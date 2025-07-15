def evolve_style(feedback):
    mood = "neutral"
    rating = feedback.get("rating", 0)
    if rating > 8:
        mood = "joyful"
    elif rating < 4:
        mood = "serious"

    from branches.persona_settings.persona_manager import set_persona
    set_persona({ "emotion": mood })
    return { "new_emotion": mood }
