import datetime


def fromString(date_string, _format='%Y-%m-%d'):
    dt = datetime.datetime.strptime(date_string, _format)
    return datetime.date(dt.year, dt.month, dt.day)


def toString(date):
    return date.strftime('%Y-%m-%d')
