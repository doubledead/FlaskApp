from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from flaskapp import app
from flaskapp.core import db
from flaskapp.events.models import Category, Event, event_schema, Status
from datetime import datetime, date


jobstores = {
    'default': SQLAlchemyJobStore(url='postgres://nljweakzhspxaa:Cl3n7ipIY1AvTk1MLyslOfZgLz@ec2-54-235-111-59.compute-1.amazonaws.com:5432/dc4t9bjie4nrtc')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler()

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

scheduler.add_job(event_status_check, 'interval', seconds=30)

scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

scheduler.start()
