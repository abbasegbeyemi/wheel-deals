import os

basedir = os.path.abspath(os.path.dirname(__file__))

PLATE_RECOGNISER_API_TOKEN = "e652d745db776a4506d673f7c21153771e532a43"


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
