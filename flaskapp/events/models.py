from ..core import db
from datetime import datetime


events_invitees = db.Table(
    'events_invitees',
    db.Column('invitee_id', db.Integer(), db.ForeignKey('invitees.id')),
    db.Column('event_id', db.Integer(), db.ForeignKey('events.id')))

class Status(db.Model):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(225))
    description = db.Column(db.String(225))
    status = db.Column(db.Integer())

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(225))
    description = db.Column(db.String(225))


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # status = db.Column(db.Integer())
    title = db.Column(db.String(225))
    create_date = db.Column(db.DateTime())
    # last_edit_date = db.Column(db.DateTime())
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    address = db.Column(db.String(225))
    # city = db.Column(db.String(225))
    # state = db.Column(db.String(225))
    # zip_code = db.Column(db.String(225))
    # country = db.Column(db.String(225))

    # category_id = db.Column(db.ForeignKey('categories.id'))
    # category = db.relationship('Category',
    #                            backref=db.backref('events', lazy='dynamic'))
    #
    # invitees = db.relationship('Invitee',
    #                            secondary=events_invitees,
    #                            backref=db.backref('events', lazy='dynamic'))

    def __init__(self, title, user_id, address, start_date, end_date, create_date=None):
        self.title = title
        if create_date is None:
            create_date = datetime.utcnow()
        self.create_date = create_date
        self.start_date = start_date
        self.end_date = end_date
        self.user_id = user_id
        self.address = address

    def __repr__(self):
        return '<Event %r>' % (self.title)

class Invitee(db.Model):
    __tablename__ = 'invitees'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer(), db.ForeignKey('events.id'))
    email_address = db.Column(db.String(225))
    status = db.Column(db.Integer())
