from flask import Blueprint

bp = Blueprint("add_complex_data", __name__)

from . import routes
