import time
from datetime import datetime, timedelta
import datetime


def get_the_current_date_as_list():
    """ get the current date """
    get_the_date = str(datetime.date.today() - timedelta(days=1))
    current_date = get_the_date.split("-")
    return current_date


def get_the_current_date():
    """ get the current date """
    get_the_date = str(datetime.date.today())
    return get_the_date


def get_the_current_date_p():
    """ get the current date """
    get_the_date = str(datetime.date.today())
    current_date = get_the_date.split("-")
    return current_date
