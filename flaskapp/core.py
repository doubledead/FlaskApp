# -*- coding: utf-8 -*-

# core module

from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_marshmallow import Marshmallow
from flask.ext.moment import Moment
from apscheduler.schedulers.background import BackgroundScheduler

#: Flask-SQLAlchemy extension instance
db = SQLAlchemy()

ma = Marshmallow()

#: Flask-Mail extension instance
mail = Mail()

#: Flask-Security extension instance
security = Security()

#: Moment.js integration within Jinja2
# https://blog.miguelgrinberg.com/post/flask-moment-flask-and-jinja2-integration-with-momentjs
moment = Moment()

scheduler = BackgroundScheduler()


class FlaskAppError(Exception):
    """Base application error class."""

    def __init__(self, msg):
        self.msg = msg


class FlaskAppFormError(Exception):
    """Raise when an error processing a form occurs."""

    def __init__(self, errors=None):
        self.errors = errors
