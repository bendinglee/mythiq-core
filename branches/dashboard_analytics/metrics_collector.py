def collect_metrics():
    from branches.memory_core.session_tracker import _session_store
    from branches.self_learning.learning_log import get_learning_history
    from branches.persona_settings.persona_manager import get_persona
    sessions = len(_session_store)
    learning_events = get_learning_history()
    persona = get_persona()
    
    return {
        "sessions_active": sessions,
        "recent_learning_events": learning_events[-5:],
        "current_persona": persona,
        "status": "Mythiq is stable and evolving."
    }
