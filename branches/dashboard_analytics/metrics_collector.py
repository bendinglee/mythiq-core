def collect_metrics():
    from branches.memory_core.session_tracker import _session_store
    from branches.self_learning.learning_log import get_learning_history
    from branches.persona_settings.persona_manager import get_persona
    from branches.task_executor.status_monitor import get_all_jobs

    sessions = len(_session_store)
    learning = get_learning_history()
    persona = get_persona()
    jobs = get_all_jobs()

    confidence = "92%" if sessions >= 5 else "71%"

    return {
        "sessions": sessions,
        "confidence_score": confidence,
        "current_mood": persona.get("emotion", "unknown"),
        "tasks_handled": len(jobs),
        "recent_jobs": jobs[-5:]
    }
