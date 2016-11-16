
from flaskapp import app
from flaskapp.core import db
from flaskapp.events.models import Event
from datetime import datetime, date
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(filename='jobs.log',level=logging.DEBUG)

# sched = BackgroundScheduler()

sched = BlockingScheduler()

def event_status_check():
    # Check for events with status_id 100, active status.
    events = Event.query.filter_by(status_id=100).all()

    for event in events:
        # If the event end_date has expired, change its status_id
        # to 400, completed status.
        if event.end_date <= datetime.utcnow():
            event.status_id = 400

            db.session.add(event)


    # Commit the db session back.
    db.session.commit()
    print('This job runs every 30 seconds.')

# sched.add_job(event_status_check, 'interval', seconds=30)

# sched.start()

with app.app_context():
    sched.add_job(event_status_check, 'interval', seconds=30)

    sched.start()
