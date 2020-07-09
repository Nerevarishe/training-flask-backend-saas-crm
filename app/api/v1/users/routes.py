from flask import request
from app.api.v1.users import bp
from app.models import User


@bp.route('/', methods=['GET'])
def get_all_users():
    """
    Get all users from DB
    """

    user_list = []
    users = User.objects

    for user in users:
        user_list.append(user)

    return {"users": user_list}


@bp.route('/add_in_bulk', methods=['POST'])
def add_in_bulk():
    """
    Add data in bulk to db
    """

    for user in request.get_json():
        new_user = User()
        new_user.username = user["username"]
        new_user.email = user["email"]
        new_user.avatar = user["avatar"]
        new_user.save()

    return {"msg": "OK"}
