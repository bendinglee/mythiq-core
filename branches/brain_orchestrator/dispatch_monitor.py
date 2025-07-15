_dispatch_log = []

def log_dispatch(route, success=True):
    _dispatch_log.append({
        "route": route,
        "success": success,
        "timestamp": __import__("time").time()
    })

def get_dispatch_stats():
    total = len(_dispatch_log)
    failed = sum(1 for e in _dispatch_log if not e["success"])
    return {
        "total_dispatches": total,
        "failure_rate": round((failed / total) * 100, 2) if total else 0
    }
