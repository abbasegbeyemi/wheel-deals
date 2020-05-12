import os

basedir = os.path.abspath(os.path.dirname(__file__))

PLATE_RECOGNISER_API_TOKEN = "e652d745db776a4506d673f7c21153771e532a43"


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_DATABASE_URI = "postgres://riuqdpwpmaccqr:47dc38b05b263af1ace1d4dea6212fc302717ea9d60e97add443de84ab261f11@ec2-46-137-156-205.eu-west-1.compute.amazonaws.com:5432/dc2auqr27d21s3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
