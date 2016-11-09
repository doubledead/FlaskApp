# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~
    Manager module
"""

from flask.ext.script import Manager
from flask import json, current_app

from flaskapp import app
from flaskapp.core import db
from flaskapp.users.models import User
from flaskapp.events.models import Category, Event, event_schema, Status
from datetime import datetime, date
from sqlalchemy import exc

manager = Manager(app)

@manager.command
def hello():
    print "hello"

@manager.command
def populate():
    status_active = Status(name='active', status_code=100)
    status_inactive = Status(name='inactive', status_code=200)
    status_cancelled = Status(name='cancelled', status_code=300)
    status_completed = Status(name='completed', status_code=400)

    db.session.add(status_active)
    db.session.add(status_inactive)
    db.session.add(status_cancelled)
    db.session.add(status_completed)
    db.session.commit()

@manager.command
def create_test_users():
    test_user = User(email='user@test.com', password='123456', active=True, birth_date=date.today())

    db.session.add(test_user)
    db.session.commit()

@manager.command
def events_test():
    # event = Event.query.filter_by(status_id=100).first_or_404()
    # event.status_id = 400

    # db.session.add(event)
    # db.session.commit()

    ## events = Event.query.all()

    # serialized_events = json.dumps(event_schema.dump(events).data)
    # serialized_events = event_schema.dump(events).data


    # This works.
    # for e in db.session.query(Event).all():
    #     print e.__dict__

    # Using db.session instead of Event works
    # events = db.session.query(Event).all()

    # This works
    events = Event.query.filter_by(status_id=100).all()

    # for e in events:
    #     print e.__dict__

    for e in events:
        # dict_event = e.__dict__
        # print event_dict["name"]

        if e.end_date <= datetime.utcnow():
            # print json.dumps(event_schema.dump(e).data)

            e.status_id = 400

            try:
                db.session.add(e)
                print 'Success'
            except exc.SQLAlchemyError as e:
                current_app.logger.error(e)
                print 'Error'


    db.session.commit()


if __name__ == "__main__":
    manager.run()
