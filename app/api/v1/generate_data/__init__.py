from flask import Blueprint

bp = Blueprint('generate_data', __name__)

from . import routes
