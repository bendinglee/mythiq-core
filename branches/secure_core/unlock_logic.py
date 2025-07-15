def unlock_data(token):
    if token == "magic123":
        from .vault_keeper import fetch_data
        return { "unlocked": fetch_data("private_routine") }
    return { "error": "Invalid token" }
