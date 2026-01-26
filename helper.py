import datetime as dt
from constants import DEFAULT_TIMEZONE

def get_todays_date(timezone = DEFAULT_TIMEZONE):
    return dt.datetime.now(timezone).date()

def is_date_in_future(date):
    if date <= get_todays_date():
        return False
    return True