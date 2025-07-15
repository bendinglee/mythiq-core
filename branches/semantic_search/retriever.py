def find_matches(query):
    sample = ["AI memory integration", "Goal chaining", "Persona modulation"]
    return [item for item in sample if query.lower() in item.lower()]
