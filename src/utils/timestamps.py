from datetime import datetime

from dateutil import tz


def get_current_datetime(timezone: str = "UTC") -> datetime:
    return datetime.fromtimestamp(int(datetime.now().timestamp()), tz.gettz(timezone))
