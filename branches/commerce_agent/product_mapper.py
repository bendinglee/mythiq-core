def map_query_to_category(query):
    if "laptop" in query:
        return "electronics"
    elif "running shoes" in query:
        return "sportswear"
    return "general"
