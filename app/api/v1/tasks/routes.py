from flask import request
from app.api.v1.tasks import bp
from app.models import TaskCard
from datetime import datetime


def convert_to_date(data: str) -> datetime:
    """
    Convert dd/mm/yyyy to datetime object
    """

    return datetime.strptime(data, '%d/%m/%Y')


@bp.route('/', methods=['GET'])
def get_widget_data():
    """
    Get data for tasks widget
    """

    per_page = request.args.get('per_page', default=3, type=int)

    _tasks = []
    # Get paginated tasks:
    tasks = TaskCard.objects.order_by('-task_due_date').paginate(page=1, per_page=per_page)
    for task in tasks.items:
        _tasks.append(task)

    return {"tasks": _tasks}


@bp.route('/tasks_stat')
def get_tasks_stat():
    """
    Get tasks statistic in defined period
    """

    tasks = TaskCard.objects
    all_tasks = tasks.count()
    active_tasks = tasks.filter(task_status='Active').count()
    completed_tasks = tasks.filter(task_status='Completed').count()
    ended_tasks = tasks.filter(task_status='Ended').count()
    return {
        "tasks_stat": {
            "active_tasks": int((active_tasks / all_tasks) * 100),
            "completed_tasks": int((completed_tasks / all_tasks) * 100),
            "ended_tasks": int((ended_tasks / all_tasks) * 100)
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
