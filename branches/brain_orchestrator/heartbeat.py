import time

def get_uptime():
    """
    Returns a structured uptime signal for Mythiq’s brain module.
    Timestamp only for now — you can expand with session tracking or boot duration.
    """
    return {
        "timestamp": time.time(),
        "uptime_message": "Brain core heartbeat active"
    }
