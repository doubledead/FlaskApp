# -*- coding: utf-8 -*-
"""
    flaskapp.events.models
    ~~~~~~~~~~~~~~~~~~~~~~
    Event models
"""

from ..core import db, ma
from datetime import datetime
from marshmallow import fields


events_guests = db.Table(
    'events_guests',
    db.Column('event_id', db.Integer(), db.ForeignKey('events.id')),
    db.Column('guest_id', db.Integer(), db.ForeignKey('guests.id')))

events_items = db.Table(
    'events_items',
    db.Column('event_id', db.Integer(), db.ForeignKey('events.id')),
    db.Column('item_id', db.Integer(), db.ForeignKey('items.id')))

items_subitems = db.Table(
    'items_subitems',
    db.Column('item_id', db.Integer(), db.ForeignKey('items.id')),
    db.Column('subitem_id', db.Integer(), db.ForeignKey('subitems.id')))

class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(225))

    def __init__(self, email):
        self.email = email

class GuestSchema(ma.ModelSchema):
    class Meta:
        model = Guest

guest_schema = GuestSchema(many=True)

class Subitem(db.Model):
    __tablename__ = 'subitems'

    id = db.Column(db.Integer(), primary_key=True)
    quantity = db.Column(db.Integer())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, quantity, user_id):
        self.quantity = quantity
        self.user_id = user_id

class SubitemSchema(ma.ModelSchema):
    class Meta:
        model = Subitem

subitem_schema = SubitemSchema()

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(225))
    name = db.Column(db.String(225))
    quantity = db.Column(db.Integer())
    quantity_claimed = db.Column(db.Integer())

    # Many-to-many
    subitems = db.relationship('Subitem', secondary=items_subitems,
                            backref=db.backref('items', lazy='joined'))

    def __init__(self, category, name, quantity, quantity_claimed):
        self.category = category
        self.name = name
        self.quantity = quantity
        self.quantity_claimed = quantity_claimed

    def __repr__(self):
        return 'Item %r>' % (self.name)

class ItemSchema(ma.ModelSchema):
    # subitems = fields.Nested('SubitemSchema', default=None, many=True)
    class Meta:
        model = Item

item_schema = ItemSchema(many=True)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer(), primary_key=True)
    address = db.Column(db.String(225))
    address_line_two = db.Column(db.String(225))
    city = db.Column(db.String(225))
    create_date = db.Column(db.DateTime())
    country = db.Column(db.String(225))
    end_date = db.Column(db.DateTime())
    last_edit_date = db.Column(db.DateTime())
    name = db.Column(db.String(225))
    start_date = db.Column(db.DateTime())
    state = db.Column(db.String(225))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    zip_code = db.Column(db.String(225))

    # Status and Category - Simple Relationship
    # http://flask-sqlalchemy.pocoo.org/2.1/quickstart/
    # status_id = db.Column(db.ForeignKey('status.id'))
    # status = db.relationship('Status',
    #                          backref=db.backref('events', lazy='dynamic'))
    status_id = db.Column(db.Integer())

    # category_id = db.Column(db.ForeignKey('category.id'))
    # category = db.relationship('Category',
    #                            backref=db.backref('events', lazy='dynamic'))
    category_id = db.Column(db.Integer())

    # Many-to-many
    # https://github.com/mattupstate/overholt/blob/master/overholt/stores/models.py
    guests = db.relationship('Guest', secondary=events_guests,
                               backref=db.backref('events', lazy='joined'))

    # Many-to-many
    items = db.relationship('Item', secondary=events_items,
                            backref=db.backref('events', lazy='joined'))

    def __init__(self, address, address_line_two, category_id, city, country,
                 end_date, last_edit_date, name, start_date, state,
                 status_id, user_id, zip_code, create_date=None):
        self.address = address
        self.address_line_two = address_line_two
        self.category_id = category_id
        self.city = city
        self.country = country
        if create_date is None:
            create_date = datetime.utcnow()
        self.create_date = create_date
        self.end_date = end_date
        self.last_edit_date = last_edit_date
        self.name = name
        self.start_date = start_date
        self.state = state
        self.status_id = status_id
        self.user_id = user_id
        self.zip_code = zip_code

    def __repr__(self):
        return '<Event %r>' % (self.name)

class EventSchema(ma.ModelSchema):
    # guests = fields.Nested('GuestSchema', default=None, many=True)
    class Meta:
        model = Event

event_schema = EventSchema()

# class Category(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(225))
#     status_code = db.Column(db.Integer())
#
#     def __init__(self, name, status_code):
#         self.name = name
#         self.status_code = status_code
#
#         def __repr__(self):
#             return 'Category %r>' % self.name

# class Status(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(225))
#     status_code = db.Column(db.Integer())
#
#     def __init__(self, name, status_code):
#         self.name = name
#         self.status_code = status_code
#
#         def __repr__(self):
#             return 'Status %r>' % self.name
