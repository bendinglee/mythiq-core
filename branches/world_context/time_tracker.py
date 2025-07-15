import datetime

def get_timestamp():
    now = datetime.datetime.utcnow()
    return {
        "utc": now.isoformat(),
        "day": now.strftime("%A"),
        "hour": now.hour,
        "greeting": "Good evening" if now.hour >= 18 else "Good morning" if now.hour < 12 else "Good afternoon"
    }
