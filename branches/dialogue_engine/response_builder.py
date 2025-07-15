def generate_response(user_input):
    from branches.context_propagator.context_stitcher import build_context_prompt
    from branches.persona_settings.persona_manager import get_persona
    from .emotion_blender import blend_emotion

    context = build_context_prompt(user_input)
    persona = get_persona()
    tone = blend_emotion(user_input, persona["emotion"])

    return f"{tone}\nContext: {context[:120]}\n→ Thoughtful response."
