from flask import request, jsonify
from app.api.v1.tasks import bp
from app.models import TaskCard
from datetime import datetime, timedelta
from .utils import filter_period, THIS_MONTH, THIS_WEEK


def convert_to_date(data: str) -> datetime:
    """
    Convert dd/mm/yyyy to datetime object
    """

    return datetime.strptime(data, '%d/%m/%Y')


week_days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


@bp.route('/', methods=['GET'])
def get_widget_data():
    """
    Get data for tasks widget
    """

    period = request.args.get('period', default=THIS_WEEK, type=str)
    date = request.args.get('date', default=None, type=int)
    per_page = request.args.get('per_page', default=3, type=int)

    _tasks = []
    # Get paginated tasks:
    tasks, first_day_of_week = filter_period(period, date, per_page)
    for task in tasks.items:
        _tasks.append({"task": task, "user": task.assigned_by_user})

    _week_days = []
    i = 1
    for day in week_days:
        if day == 'Sun':
            _week_days.append({'week_day_name': day, 'week_day_date': first_day_of_week.day})
        else:
            _week_days.append({'week_day_name': day, 'week_day_date': (first_day_of_week + timedelta(days=i)).day})
            i += 1

    return jsonify({'task_cards': _tasks, 'week_days': _week_days})


@bp.route('/tasks_stat')
def get_tasks_stat():
    """
    Get tasks statistic in defined period
    """

    period = request.args.get("period", default=THIS_MONTH, type=str)
    tasks = filter_period(period)

    all_tasks = tasks.count()
    active_tasks = tasks.filter(task_status='Active').count()
    completed_tasks = tasks.filter(task_status='Completed').count()
    ended_tasks = tasks.filter(task_status='Ended').count()

    return {
        "tasks_stat": {
            "active_tasks": (active_tasks / all_tasks) * 100,
            "completed_tasks": (completed_tasks / all_tasks) * 100,
            "ended_tasks": (ended_tasks / all_tasks) * 100
        }
    }


@bp.route('/add_in_bulk', methods=['POST'])
def add_in_bulk():
    """
    Add data in bulk to db
    """

    tasks = request.get_json()

    for task in tasks:
        new_task = TaskCard()
        new_task.task_due_date = convert_to_date(task["task_due_date"])
        new_task.task_type = task["task_type"]
        new_task.task_status = task["task_status"]
        new_task.task_body = task["task_body"]
        new_task.save()

    return {"msg": "OK"}
