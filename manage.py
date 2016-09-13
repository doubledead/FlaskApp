# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~
    Manager module
"""

from flask.ext.script import Manager

from flaskapp import app
from flaskapp.core import db
from flaskapp.events.models import Event, Category, Status

manager = Manager(app)

@manager.command
def hello():
    print "hello"

@manager.command
def populate():
    status_active = Status(name='active', status_code=100)
    status_inactive = Status(name='inactive', status_code=200)

    db.session.add(status_active)
    db.session.add(status_inactive)
    db.session.commit()

if __name__ == "__main__":
    manager.run()
