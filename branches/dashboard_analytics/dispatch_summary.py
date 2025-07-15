def summarize_dispatch():
    from branches.task_executor.status_monitor import get_all_jobs
    jobs = get_all_jobs()
    success = sum(1 for j in jobs if j.get("status") == "completed")
    failed = sum(1 for j in jobs if j.get("status") == "failed")

    return {
        "total": len(jobs),
        "successful": success,
        "failed": failed,
        "success_rate": round(success / max(len(jobs), 1) * 100, 2)
    }
