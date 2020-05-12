from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """Model for a user who logs in to the app"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}(name:{self.firstname} {self.lasttname})"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class CarMake(db.Model):
    """Model for the car makes"""
    __tablename__ = 'car_makes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    models = db.relationship('CarModel', backref='make', lazy='dynamic')

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"


class CarModel(db.Model):
    """Model for the car models"""
    __tablename__ = 'car_models'
    id = db.Column(db.Integer, primary_key=True)
    make_id = db.Column(db.Integer, db.ForeignKey('car_makes.id'))
    name = db.Column(db.String(64))

    def __str__(self):
        return f"{self.__class__.__name__}({self.make.name} {self.name})"
