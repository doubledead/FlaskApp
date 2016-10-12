# -*- coding: utf-8 -*-

# core module

from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_marshmallow import Marshmallow

#: Flask-SQLAlchemy extension instance
db = SQLAlchemy()

ma = Marshmallow()

#: Flask-Mail extension instance
mail = Mail()

#: Flask-Security extension instance
security = Security()


class FlaskAppError(Exception):
    """Base application error class."""

    def __init__(self, msg):
        self.msg = msg


class FlaskAppFormError(Exception):
    """Raise when an error processing a form occurs."""

    def __init__(self, errors=None):
        self.errors = errors
