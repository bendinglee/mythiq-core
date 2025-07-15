def resolve_trigger(input_text):
    if "translate" in input_text:
        return "translation_module"
    return "core_dispatcher"
