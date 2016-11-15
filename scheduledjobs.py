
from flaskapp import app
from flaskapp.core import db
from flaskapp.events.models import Event
from datetime import datetime, date

# from apscheduler.schedulers.background import BackgroundScheduler

# scheduler = BackgroundScheduler()

# def event_status_check():
#     Check for events with status_id 100, active status.
#     events = Event.query.filter_by(status_id=100).all()
#
#     for event in events:
#         # If the event end_date has expired, change its status_id
#         # to 400, completed status.
#         if event.end_date <= datetime.utcnow():
#             event.status_id = 400
#
#             db.session.add(event)
#
#
#     # Commit the db session back.
#     db.session.commit()
#     print('This job runs every 30 seconds.')
#
# scheduler.add_job(event_status_check, 'interval', seconds=30)
#
# scheduler.start()

# from flask import Flask
from flask_apscheduler import APScheduler


# class Config(object):
#     JOBS = [
#         {
#             'id': 'job1',
#             'func': '__main__:job1',
#             'args': (),
#             'trigger': 'interval',
#             'seconds': 30
#         }
#     ]
#
#     SCHEDULER_VIEWS_ENABLED = True


def job1():
    print('This job runs every 30 seconds.')

# app = Flask(__name__)
# app.config.from_object(Config())
# app.debug = True

# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()

# app.run()

scheduler = APScheduler()
scheduler.init_app(app)

JOBS = [
    {
        'id': 'job1',
        'func': '__main__:job1',
        'args': (),
        'trigger': 'interval',
        'seconds': 30
    }
]

SCHEDULER_VIEWS_ENABLED = True

if __name__ == "__main__":
    scheduler.start()
