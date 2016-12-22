"""
    flaskapp.apsjobs
    ~~~~~~~~~~~~~~~~
    flaskapp Flask-APScheduler job definitions.
"""

from datetime import datetime
from flask import current_app
from flaskapp import app
from .core import db, mail
from .models import Event, User
from flask_mail import Message


# def job1():
#     # This works.
#     with app.app_context():
#         current_app.logger.info('Flask-APScheduler testing. This runs every 30 seconds.')
#         print('Flask-APScheduler testing. This runs every 30 seconds.')


def events_check():
    with app.app_context():
        # Check for events with status_id 100, active status.
        events = Event.query.filter_by(status_id=100).all()

        for event in events:
            # If the event end_date has expired, change its status_id
            # to 400, completed status.
            if event.end_date <= datetime.utcnow():
                event.status_id = 400
                current_app.logger.info('Event expired. Status updated. Event ID: %s', event.id)

                event_creator = User.query.filter_by(id=event.user_id)

                confmsg = Message()
                confmsg.add_recipient(event_creator.email)
                confmsg.body = "The following event has ended: " + event.name

                db.session.add(event)
                mail.send(confmsg)
            else:
                current_app.logger.info('Status 105, no expired events.')


        # Commit the db session back.
        db.session.commit()
