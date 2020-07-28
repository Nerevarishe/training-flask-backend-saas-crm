from app.models import TaskCard
from app.utils import last_day_of_month
from datetime import datetime, timedelta

PREV_WEEK = "prevWeek"
THIS_WEEK = "thisWeek"
NEXT_WEEK = "nextWeek"

PREV_MONTH = "prevMonth"
THIS_MONTH = "thisMonth"
NEXT_MONTH = "nextMonth"


def filter_period(period, date=None, per_page=3):
    current_date = datetime.utcnow()

    # Filter for TasksWidget
    if period == PREV_WEEK:
        prev_week_date = current_date - timedelta(days=7)
        first_day_of_prev_week = prev_week_date - timedelta(days=prev_week_date.isoweekday() % 7)
        first_day = first_day_of_prev_week
        last_day_of_prev_week = first_day_of_prev_week + timedelta(days=6)
        if date:
            first_day_of_prev_week = first_day_of_prev_week.replace(day=date)
            last_day_of_prev_week = last_day_of_prev_week.replace(day=date)
        tasks = TaskCard.objects(task_due_date__gte=first_day_of_prev_week, task_due_date__lte=last_day_of_prev_week)
        all_tasks = tasks.count()
        completed_tasks = tasks.filter(task_status='Completed').count()

        return tasks.order_by('-task_due_date').paginate(page=1,
                                                         per_page=per_page), first_day, all_tasks, completed_tasks

    elif period == THIS_WEEK:
        first_day_of_this_week = current_date - timedelta(days=current_date.isoweekday() % 7)
        first_day = first_day_of_this_week
        last_day_of_this_week = first_day_of_this_week + timedelta(days=6)
        if date:
            first_day_of_this_week = first_day_of_this_week.replace(day=date, month=current_date.month)
            last_day_of_this_week = last_day_of_this_week.replace(day=date, month=current_date.month)
        tasks = TaskCard.objects(task_due_date__gte=first_day_of_this_week, task_due_date__lte=last_day_of_this_week)
        all_tasks = tasks.count()
        completed_tasks = tasks.filter(task_status='Completed').count()
        return tasks.order_by('-task_due_date').paginate(page=1,
                                                         per_page=per_page), first_day, all_tasks, completed_tasks

    elif period == NEXT_WEEK:
        next_week_date = current_date + timedelta(days=7)
        first_day_of_next_week = next_week_date - timedelta(days=current_date.isoweekday() % 7)
        first_day = first_day_of_next_week
        last_day_of_next_week = first_day_of_next_week + timedelta(days=6)
        if date:
            first_day_of_next_week = first_day_of_next_week.replace(day=date)
            last_day_of_next_week = last_day_of_next_week.replace(day=date)
        tasks = TaskCard.objects(task_due_date__gte=first_day_of_next_week, task_due_date__lte=last_day_of_next_week)
        all_tasks = tasks.count()
        completed_tasks = tasks.filter(task_status='Completed').count()
        return tasks.order_by('-task_due_date').paginate(page=1,
                                                         per_page=per_page), first_day, all_tasks, completed_tasks

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
