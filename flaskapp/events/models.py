from ..core import db
from datetime import datetime


events_invitees = db.Table(
    'events_invitees',
    db.Column('invitee_id', db.Integer(), db.ForeignKey('invitees.id')),
    db.Column('event_id', db.Integer(), db.ForeignKey('events.id')))

# class Status(db.Model):
#     __tablename__ = 'statuses'
#
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(225))
#     description = db.Column(db.String(225))
#     status = db.Column(db.Integer())

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(225))
    description = db.Column(db.String(225))

class Invitee(db.Model):
    __tablename__ = 'invitees'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer(), db.ForeignKey('events.id'))
    email_address = db.Column(db.String(225))
    status = db.Column(db.Integer())


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer(), primary_key=True)
    status = db.Column(db.Integer())
    title = db.Column(db.String(225))
    address = db.Column(db.String(225))
    city = db.Column(db.String(225))
    state = db.Column(db.String(225))
    zip_code = db.Column(db.String(225))
    country = db.Column(db.String(225))
    start_date = db.Column(db.DateTime())
    last_edit_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    create_date = db.Column(db.DateTime())

    # category_id = db.Column(db.ForeignKey('categories.id'))
    # category = db.relationship('Category',
    #                            backref=db.backref('events', lazy='dynamic'))
    #
    invitees = db.relationship('Invitee',
                               secondary=events_invitees,
                               backref=db.backref('events', lazy='dynamic'))

    def __init__(self, status, title, address, city, state, zip_code, country,
                 start_date, end_date, last_edit_date, user_id, create_date=None):
        self.status = status
        self.title = title
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.start_date = start_date
        self.end_date = end_date
        self.last_edit_date = last_edit_date
        self.user_id = user_id
        if create_date is None:
            create_date = datetime.utcnow()
        self.create_date = create_date

    def __repr__(self):
        return '<Event %r>' % (self.title)
