from datetime import datetime, timedelta

def human_readable_timedelta(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours}h {minutes}m"


def get_time_left(expires_at: datetime) -> str:
    now = datetime.utcnow()
    if expires_at > now:
        return human_readable_timedelta(expires_at - now)
    return "0m"
