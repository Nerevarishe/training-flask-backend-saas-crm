from flask import request
from . import bp
from app.models import User, TaskCard
from random import choice

users = []
random_users = []


@bp.route("/", methods=['GET'])
def add_complex_data():
    db_users = User.objects()
    for user in db_users:
        users.append(user)
    for random_user in range(20):
        random_users.append(choice(users))

    db_tasks = TaskCard.objects()
    for card in db_tasks:
        card.assigned_by_user = choice(random_users)
        card.save()

    return {'msg': 'OK'}
