from flask import Blueprint

bp = Blueprint("users", __name__)

from app.api.v1.users import routes
