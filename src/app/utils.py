import datetime

import pytz


def get_utc_now():
    return (datetime.datetime.now(tz=pytz.UTC)
            .replace(tzinfo=None))
