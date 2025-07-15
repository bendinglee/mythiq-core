_log = []

def mirror_request(source, key):
    _log.append({ "source": source, "key": key })
    return True

def view_mirror_log():
    return _log[-10:]
