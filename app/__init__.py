from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from config import Config

db = MongoEngine()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    CORS(app)

    # Blueprints
    # Tasks
    from app.api.v1.tasks import bp as tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/api/v1/tasks')

    # Users
    from app.api.v1.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')

    return app
