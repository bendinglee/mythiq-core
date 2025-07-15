def switch_persona(p):
    from branches.persona_settings.persona_manager import set_persona
    set_persona(p)
    return { "persona": p }
