def apply_style(text):
    from branches.persona_settings.persona_manager import get_persona
    persona = get_persona()
    return f"[Style: {persona['style']}] {text}"
