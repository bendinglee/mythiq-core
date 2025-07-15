_users = {}

def login_user(name):
    _users[name] = { "id": name, "persona": {} }
    return { "user": name }
