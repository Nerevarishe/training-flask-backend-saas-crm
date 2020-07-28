from datetime import datetime, timedelta


def last_day_of_month(any_day: datetime):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


def current_quarter(date: datetime):
    current_month = date.month
    return (current_month - 1) // 3 + 1


def convert_to_date(data: str) -> datetime:
    """
    Convert dd/mm/yyyy to datetime object
    """

    return datetime.strptime(data, '%d/%m/%Y')