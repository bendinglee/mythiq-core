def track_success_patterns(entries):
    route_hits = {}
    for e in entries:
        route = e["route"]
        route_hits[route] = route_hits.get(route, 0) + 1

    best = max(route_hits, key=route_hits.get)
    return {
        "best_route": best,
        "route_distribution": route_hits
    }
