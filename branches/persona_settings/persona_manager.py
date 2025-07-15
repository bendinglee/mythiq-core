_active_persona = {
    "style": "neutral",
    "theme": "default",
    "emotion": "calm"
}

def set_persona(config):
    _active_persona.update(config)

def get_persona():
    return _active_persona
