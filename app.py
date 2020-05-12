import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from models import db, User

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
# Here we initialise the database and crete all the required tables
db.init_app(app)
db.app = app
# Initialise migration
migrate = Migrate(app, db)
# Initialise the login manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    """
    Given a user id, return a user from the database that matches.
    :param user_id: int
    :return: User object
    """
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
