from flask import request, jsonify
from . import bp
from app.models import TaskCard
from datetime import timedelta
from .utils import filter_period, THIS_MONTH, THIS_WEEK

week_days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


@bp.route('/', methods=['GET'])
def get_widget_data():
    period = request.args.get('period', default=THIS_WEEK, type=str)
    date = request.args.get('date', default=None, type=int)
    per_page = request.args.get('per_page', default=3, type=int)

    _tasks = []
    # Get paginated tasks:
    tasks, first_day_of_week, all_tasks, completed_tasks = filter_period(period, date, per_page)

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

    return jsonify(
        {'task_cards': _tasks, 'week_days': _week_days, 'has_next': tasks.has_next, "tasks_in_period": all_tasks,
         'completed_tasks': completed_tasks})


@bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    to_status = request.args.get('change_status_to', default=None, type=str)
    if to_status == 'Completed' or 'Active':
        task = TaskCard.objects(id=task_id).get_or_404()
        task.task_status = to_status
        task.save()

        return {'msg': 'UPDATED', 'id': task_id}


@bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = TaskCard.objects(id=task_id).get_or_404()
    task.delete()
    return {'msg': 'DELETED', 'id': task_id}


@bp.route('/tasks_stat')
def get_tasks_stat():
    period = request.args.get("period", default=THIS_MONTH, type=str)
    tasks = filter_period(period)

    all_tasks = tasks.count()
    if all_tasks == 0:
        return {'tasks_stat': {
            "active_tasks": 0,
            "completed_tasks": 0,
            "ended_tasks": 0
        }}
    active_tasks = tasks.filter(task_status='Active').count()
    completed_tasks = tasks.filter(task_status='Completed').count()
    ended_tasks = tasks.filter(task_status='Ended').count()

    return {
        "tasks_stat": {
            "active_tasks": round((active_tasks / all_tasks) * 100),
            "completed_tasks": round((completed_tasks / all_tasks) * 100),
            "ended_tasks": round((ended_tasks / all_tasks) * 100)
        }
    }
