# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~
    Manager module
"""

from flask_script import Manager
from flask import json, current_app

from flaskapp import app
from flaskapp.core import db, mail
from flaskapp.users.models import User
from flaskapp.events.models import Category, Event, event_schema, Status, ItemCategory
from datetime import datetime, date, timedelta
from sqlalchemy import exc

manager = Manager(app)

@manager.command
def populate():
    # Event Status
    status_active = Status(name='Active', status_code=100)
    status_inactive = Status(name='Archived', status_code=200)
    status_cancelled = Status(name='Cancelled', status_code=300)
    status_completed = Status(name='Completed', status_code=400)
    status_archived = Status(name='Inactive', status_code=500)
    status_postponed = Status(name='Postponed', status_code=600)
    # Event Category
    category_custom = Category(active=True, name='Custom', status_code=100)
    category_meeting = Category(active=True, name='Meeting', status_code=200)
    category_party = Category(active=True, name='Party', status_code=300)
    category_team_building_exercise = Category(active=True, name='Team Building Exercise', status_code=400)
    # Event Item Categories
    item_category_custom = ItemCategory(active=True, name='Custom', code=100)
    item_category_type1 = ItemCategory(active=True, name='Type 1', code=101)
    item_category_type2 = ItemCategory(active=True, name='Type 2', code=102)
    item_category_type3 = ItemCategory(active=True, name='Type 3', code=103)

    # Add Categories to DB session
    db.session.add(category_custom)
    db.session.add(category_meeting)
    db.session.add(category_party)
    db.session.add(category_team_building_exercise)

    # Add Status' to DB session
    db.session.add(status_active)
    db.session.add(status_inactive)
    db.session.add(status_cancelled)
    db.session.add(status_completed)
    db.session.add(status_archived)
    # Commit session
    db.session.commit()

@manager.command
def create_test_users():
    # test_user = User(email='user@test.com', password='123456', active=True)
    test_user = User(email='user@test.com',
                     password='123456',
                     active=True,
                     birth_date=date.today(),
                     first_name='User',
                     last_name='Test')
    test_user2 = User(email='user2@test.com',
                      password='123456',
                      active=True,
                      birth_date=date.today(),
                      first_name='User2',
                      last_name='Test')
    test_user3 = User(email='user3@test.com',
                      password='123456',
                      active=True,
                      birth_date=date.today(),
                      first_name='User3',
                      last_name='Test')
    test_user4 = User(email='user4@test.com',
                      password='123456',
                      active=True,
                      birth_date=date.today(),
                      first_name='User4',
                      last_name='Test')

    db.session.add(test_user)
    db.session.add(test_user2)
    db.session.add(test_user3)
    db.session.add(test_user4)
    db.session.commit()


## event_status_check has been automated but will remain here for reference
@manager.command
def event_status_check():
    # Check for events with status_id 100, active status.
    events = Event.query.filter_by(status_id=100).all()

    for event in events:
        # If the event end_date has expired, change its status_id
        # to 400, completed status.
        if event.end_date <= datetime.utcnow():
            event.status_id = 400

            # event_creator = User.query.filter_by(id=event.user_id)
            # confmsg = Message()
            # confmsg.add_recipient(event_creator.email)
            # confmsg.body = "The following event has ended: " + event.name

            try:
                db.session.add(event)
                # mail.send(confmsg)
                print("Event Status Check: Success")
            except exc.SQLAlchemyError as e:
                current_app.logger.error(e)
                print("Event Status Check: Error")


    # Commit the db session back.
    db.session.commit()


@manager.command
def event_archive_check():
    events = Event.query.filter_by(status_id=400).all()
    margin = timedelta(days = 3)

    for event in events:
        if event.end_date < margin:
            event.status_id = 500
            db.session.add(event)
            print("ID:")
            print(event.id)

    try:
        db.session.commit()
        print("Archive check: Success")
    except exc.SQLAlchemyError as e:
        # Email errors.
        current_app.logger.error(e)
        print("Archive check: Error")




if __name__ == "__main__":
    manager.run()
