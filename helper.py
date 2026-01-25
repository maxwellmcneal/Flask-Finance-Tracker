import datetime as dt
import zoneinfo as zi

DEFAULT_TIMEZONE = zi.ZoneInfo('US/Pacific')

def get_todays_date(timezone = DEFAULT_TIMEZONE):
    return dt.datetime.now(timezone).date()

def is_date_in_future(date):
    if date <= get_todays_date():
        return False
    return True