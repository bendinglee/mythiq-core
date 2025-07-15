def build_context_prompt(user_input):
    from branches.memory_core.session_tracker import current_session
    from branches.memory_core.recall import retrieve_entries
    from branches.persona_settings.persona_manager import get_persona
    sid = current_session()
    history = retrieve_entries(sid)[-3:]
    persona = get_persona()

    memory_context = "\n".join([str(entry["request"]) for entry in history])
    persona_style = f"[Style: {persona['style']} | Emotion: {persona['emotion']}]"
    return f"{persona_style}\nMemory:\n{memory_context}\nCurrent:\n{user_input}"
