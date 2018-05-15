from apscheduler.schedulers.blocking import BlockingScheduler
from flask import json, current_app
from flaskapp import app
from flaskapp.core import db, mail
from flaskapp.users.models import User
from flaskapp.events.models import Category, Event, event_schema, Status, ItemCategory
from datetime import datetime, date, timedelta
from sqlalchemy import exc
from flask_mail import Message

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every minute.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

def low_interval_job():
    print('This job runs every 30 seconds.')

def test_job():
    with app.app_context():
        events = Event.query.filter_by(status_id=100).all()
        for event in events:
            print(event.status_id)

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

                for g in guests_data:
                    e = g.email
                    guest_message = Message()
                    guest_message.subject = "FlaskApp - Event Invite - " + event.name
                    guest_message.body = "You have been invited to the following event: " + event.name
                    # guest_message.html = render_template('/mails/event/event_invite.html', host=user.email, event_name=event.name, id=event.id)
                    guest_message.add_recipient(e)
                    # Send message
                    mail.send(guest_message)

                confmsg = Message()
                confmsg.subject = "FlaskApp - Event Invites Sent"
                confmsg.add_recipient(user.email)
                confmsg.body = "Event invites have been sent for the following event: " + event.name

                db.session.add(event)
                mail.send(confmsg)
            else:
                current_app.logger.info('Status 105, all invites sent.')


        # Commit the db session back.
        db.session.commit()

# sched.add_job(low_interval_job, 'interval', seconds=30)
# sched.add_job(test_job, 'interval', seconds=10) # This works when using local DB
sched.add_job(events_invites_status_check, 'interval', seconds=30)

sched.start()
