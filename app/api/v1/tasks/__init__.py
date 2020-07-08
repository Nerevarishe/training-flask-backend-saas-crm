from flask import Blueprint

bp = Blueprint("tasks", __name__)

from app.api.v1.tasks import routes
