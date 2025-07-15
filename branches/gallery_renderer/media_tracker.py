_gallery = []

def log_media(prompt, result_url):
    _gallery.append({ "prompt": prompt, "url": result_url, "ts": __import__('time').time() })

def get_gallery():
    return _gallery[-10:]
