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

    return app
