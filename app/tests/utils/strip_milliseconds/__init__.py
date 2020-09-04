from datetime import datetime as datetime_type


def strip_milliseconds(date: datetime_type) -> str:
    return date.strftime("%Y-%m-%d %H:%M:%S")
