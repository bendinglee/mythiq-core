_gallery = []

# 🖼 Log media generation prompt + result
def log_media(prompt, result_url):
    _gallery.append({
        "prompt": prompt,
        "url": result_url,
        "ts": __import__('time').time()
    })

# 🔍 Return latest gallery items with fallback dev state
def get_gallery():
    if not _gallery:
        return [
            {"id": "img_001", "tag": "memory", "title": "Session Anchor", "timestamp": 1720800000},
            {"id": "img_002", "tag": "persona", "title": "Tone Shift Map", "timestamp": 1720803600}
        ]
    return _gallery[-10:]
