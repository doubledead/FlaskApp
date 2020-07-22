# -*- coding: utf-8 -*-

# core module

from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_marshmallow import Marshmallow
from flask_moment import Moment
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO


db = SQLAlchemy()
ma = Marshmallow()
mail = Mail()
security = Security()
moment = Moment()
scheduler = APScheduler()
socketio = SocketIO()


class FlaskAppError(Exception):
    """Base application error class."""

    def __init__(self, msg):
        self.msg = msg


class FlaskAppFormError(Exception):
    """Raise when an error processing a form occurs."""

    def __init__(self, errors=None):
        self.errors = errors
