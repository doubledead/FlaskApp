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

                user = User.query.filter_by(id=event.user_id).first_or_404()
                confmsg = Message()
                confmsg.subject = "FlaskApp - Event Ended"
                confmsg.add_recipient(user.email)
                confmsg.body = "The following event has ended: " + event.name

                db.session.add(event)
                mail.send(confmsg)
            else:
                current_app.logger.info('Status 105, no expired events.')


        # Commit the db session back.
        db.session.commit()


def events_invites_status_check():
    with app.app_context():
        # Check for events with status_id 100, active status.
        events = Event.query.filter_by(status_id=100).all()

        for event in events:
            # If the event invite status ID is 1, change to 2 and send mail invites
            if event.end_date >= datetime.utcnow() and event.invite_status_id == 1:
                event.invite_status_id = 2
                current_app.logger.info('Sending mail invites for Event ID: %s', event.id)

                user = User.query.filter_by(id=event.user_id).first_or_404()

                guests_data = event.guests
                # Guest invite email
                # guest_message = Message()
                # guest_message.subject = "FlaskApp - Event Invite - " + event.name
                # guest_message.body = "You have been invited to the following event: " + event.name

                for g in guests_data:
                    e = g.email
                    guest_message = Message()
                    guest_message.subject = "FlaskApp - Event Invite - " + event.name
                    guest_message.body = "You have been invited to the following event: " + event.name
                    guest_message.add_recipient(e)
                    # Send message
                    mail.send(guest_message)

                confmsg = Message()
                confmsg.subject = "FlaskApp - Event Invites Sent"
                confmsg.add_recipient(user.email)
                confmsg.body = "Event invites have been sent for the following event: " + event.name

                db.session.add(event)
                mail.send(confmsg)
                # mail.send(guest_message)
            else:
                current_app.logger.info('Status 105, all invites sent.')


        # Commit the db session back.
        db.session.commit()
