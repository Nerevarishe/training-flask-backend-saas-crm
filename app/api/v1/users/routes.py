from . import bp
from app.models import User


@bp.route('/', methods=['GET'])
def get_all_users():
    user_list = []
    users = User.objects

    for user in users:
        user_list.append(user)

    return {"users": user_list}
