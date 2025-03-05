"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-04
"""
import datetime
from typing import Union


def apple_ts_to_datetime(apple_ts: float) -> Union[datetime.datetime, None]:
    """
    Converts an Apple Core Data timestamp to a human-readable datetime object.

    Apple timestamps represent seconds since 2001-01-01 00:00:00 UTC.

    :param apple_ts: Apple timestamp (seconds since 2001-01-01)
    :return: Converted datetime object in UTC, or None if the timestamp is invalid.
    """
    if apple_ts is None or apple_ts <= 0:
        return None  # Handle invalid timestamps

    apple_epoch = datetime.datetime(2001, 1, 1, tzinfo=datetime.UTC)
    return apple_epoch + datetime.timedelta(seconds=apple_ts)
