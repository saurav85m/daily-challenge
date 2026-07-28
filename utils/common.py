from datetime import datetime
from zoneinfo import ZoneInfo


def get_india_timestamp():
    """
    Returns the current timestamp in Indian Standard Time.
    """
    return datetime.now(
        ZoneInfo("Asia/Kolkata")
    )