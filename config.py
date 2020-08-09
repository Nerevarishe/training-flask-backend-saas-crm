import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'

    # Flask-MongoEngine Settings
    MONGODB_DB = os.environ.get('MONGODB_DB') or 'test'
    MONGODB_HOST = os.environ.get('MONGODB_HOST') or '10.0.0.1'
    MONGODB_PORT = os.environ.get('MONGODB_PORT') or 27017
    MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME') or ''
    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD') or ''


class TestConfig(Config):
    TESTING = True

    # Flask-MongoEngine Settings
    MONGODB_DB = 'test'
    MONGODB_HOST = os.environ.get('MONGODB_HOST') or '10.0.0.1'
