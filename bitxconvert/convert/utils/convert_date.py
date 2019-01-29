from datetime import datetime
import pytz


def float_hour_to_time(fh):
    h, r = divmod(fh, 1)
    m, r = divmod(r*60, 1)
    return (
        int(h),
        int(m),
        int(r*60),
    )


def get_date_time(value):
    dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(value) - 2)
    hour, minute, second = float_hour_to_time(value % 1)
    dt = dt.replace(hour=hour, minute=minute, second=second)
    dt_str = dt.astimezone(pytz.utc)
    return dt_str.strftime("%Y-%m-%d %H:%M:%S")
