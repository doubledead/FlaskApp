
from flaskapp import app
from flaskapp.core import db, scheduler
from flaskapp.events.models import Event
from datetime import datetime, date

# from apscheduler.schedulers.background import BackgroundScheduler

# scheduler = BackgroundScheduler()

def event_status_check():
    # Check for events with status_id 100, active status.
    # events = Event.query.filter_by(status_id=100).all()
    #
    # for event in events:
    #     # If the event end_date has expired, change its status_id
    #     # to 400, completed status.
    #     if event.end_date <= datetime.utcnow():
    #         event.status_id = 400
    #
    #         db.session.add(event)
    #
    #
    # # Commit the db session back.
    # db.session.commit()
    print('This job runs every 30 seconds.')

scheduler.add_job(event_status_check, 'interval', seconds=30)

scheduler.start()
