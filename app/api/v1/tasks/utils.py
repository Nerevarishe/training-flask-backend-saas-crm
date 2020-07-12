from app.models import TaskCard
from datetime import datetime, timedelta

PREV_WEEK = "prevWeek"
THIS_WEEK = "thisWeek"
NEXT_WEEK = "nextWeek"

PREV_MONTH = "prevMonth"
THIS_MONTH = "thisMonth"
NEXT_MONTH = "nextMonth"


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


def filter_period(period, per_page=3):
    current_date = datetime.now()

    # Filter for TasksWidget
    if period == PREV_WEEK:
        prev_week_date = current_date - timedelta(days=7)
        first_day_of_prev_week = prev_week_date - timedelta(days=prev_week_date.isoweekday() % 7)
        last_day_of_prev_week = first_day_of_prev_week + timedelta(days=6)
        return TaskCard.objects(task_due_date__gte=first_day_of_prev_week,
                                task_due_date__lte=last_day_of_prev_week) \
            .order_by('-task_due_date').paginate(page=1, per_page=per_page)

        # return TaskCard.objects.order_by('-task_due_date').paginate(page=1, per_page=per_page)

    # Filter for TaskStatWidget
    if period == PREV_MONTH:
        last_day_of_current_month = last_day_of_month(current_date)
        prev_month_date = last_day_of_current_month - timedelta(days=last_day_of_current_month.day)
        last_day_of_prev_month = last_day_of_month(prev_month_date)
        first_day_of_prev_month = prev_month_date.replace(day=1)
        return TaskCard.objects(task_due_date__gte=first_day_of_prev_month,
                                task_due_date__lte=last_day_of_prev_month)

    if period == THIS_MONTH:
        last_day_of_current_month = last_day_of_month(current_date)
        first_day_of_current_month = datetime.now().replace(day=1)
        return TaskCard.objects(task_due_date__gte=first_day_of_current_month,
                                task_due_date__lte=last_day_of_current_month)

    if period == NEXT_MONTH:
        last_day_of_current_month = last_day_of_month(current_date)
        next_month_date = last_day_of_current_month + timedelta(days=last_day_of_current_month.day)
        last_day_of_next_month = last_day_of_month(next_month_date)
        first_day_of_next_month = next_month_date.replace(day=1)
        return TaskCard.objects(task_due_date__gte=first_day_of_next_month,
                                task_due_date__lte=last_day_of_next_month)
