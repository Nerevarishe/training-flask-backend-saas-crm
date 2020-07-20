from datetime import datetime, timedelta
from app.models import Deal
from app.utils import current_quarter, last_day_of_month

# Filter values
YEARLY = "yearly"
QUARTERLY = "quarterly"
MONTHLY = "monthly"
WEEKLY = "weekly"


def filter_period(period):
    current_date = datetime.now()
    if period == YEARLY:
        first_date_of_year = current_date.replace(day=1, month=1)
        last_date_of_year = current_date.replace(day=31, month=12)
        return Deal.objects(deal_date__gte=first_date_of_year, deal_date__lte=last_date_of_year)

    elif period == QUARTERLY:
        quarter = current_quarter(current_date)
        first_date_of_current_quarter = None
        last_date_of_current_quarter = None
        if quarter == 1:
            first_date_of_current_quarter = current_date.replace(day=1, month=1)
            last_date_of_current_quarter = current_date.replace(day=31, month=3)
        elif quarter == 2:
            first_date_of_current_quarter = current_date.replace(day=1, month=4)
            last_date_of_current_quarter = current_date.replace(day=30, month=6)
        elif quarter == 3:
            first_date_of_current_quarter = current_date.replace(day=1, month=7)
            last_date_of_current_quarter = current_date.replace(day=30, month=9)
        elif quarter == 4:
            first_date_of_current_quarter = current_date.replace(day=1, month=10)
            last_date_of_current_quarter = current_date.replace(day=31, month=12)

        return Deal.objects(deal_date__gte=first_date_of_current_quarter, deal_date__lte=last_date_of_current_quarter)

    elif period == MONTHLY:
        first_date_of_current_month = current_date.replace(day=1)
        last_date_of_current_month = last_day_of_month(current_date)

        return Deal.objects(deal_date__gte=first_date_of_current_month, deal_date__lte=last_date_of_current_month)

    elif period == WEEKLY:
        first_date_of_current_week = current_date - timedelta(days=current_date.weekday())
        last_date_of_current_week = first_date_of_current_week + timedelta(days=6)

        return Deal.objects(deal_date__gte=first_date_of_current_week, deal_date__lte=last_date_of_current_week)