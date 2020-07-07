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


# chat_member = db.Table(
#     'chat_member',
#     db.Column('chat_id', db.Integer(), db.ForeignKey('chat.id')),
#     db.Column('member_id', db.Integer(), db.ForeignKey('member.id')))
#
# chat_message = db.Table(
#     'chat_message',
#     db.Column('chat_id', db.Integer(), db.ForeignKey('chat.id')),
#     db.Column('message_id', db.Integer(), db.ForeignKey('message.id')))


class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    email = db.Column(db.String(225))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    rsvp_flag = db.Column(db.Boolean(), default=False)
    user_id = db.Column(db.Integer())

    def __init__(self, active, email, first_name, last_name, rsvp_flag, user_id):
        self.active = active
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.rsvp_flag = rsvp_flag
        self.user_id = user_id


class GuestSchema(ma.ModelSchema):
    class Meta:
        model = Guest

# guest_schema = GuestSchema(many=True)
guest_schema = GuestSchema()


class Subitem(db.Model):
    __tablename__ = 'subitems'

    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    quantity = db.Column(db.Integer())
    user_id = db.Column(db.Integer())

    def __init__(self, active, quantity, user_id):
        self.active = active
        self.quantity = quantity
        self.user_id = user_id


class SubitemSchema(ma.ModelSchema):
    class Meta:
        model = Subitem

# subitem_schema = SubitemSchema(many=True)
subitem_schema = SubitemSchema()


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    category_id = db.Column(db.Integer())
    name = db.Column(db.String(225))
    quantity = db.Column(db.Integer())
    quantity_claimed = db.Column(db.Integer())
    user_id = db.Column(db.Integer())

    # Many-to-many
    subitems = db.relationship('Subitem', secondary=items_subitems,
                            backref=db.backref('items', lazy='joined'))

    def __init__(self, active, category_id, name, quantity, quantity_claimed, user_id):
        self.active = active
        self.category_id = category_id
        self.name = name
        self.quantity = quantity
        self.quantity_claimed = quantity_claimed
        self.user_id = user_id

    def __repr__(self):
        return 'Item %r>' % self.name


class ItemSchema(ma.ModelSchema):
    subitems = fields.Nested('SubitemSchema', default=None, many=True)

    class Meta:
        model = Item


item_schema = ItemSchema(many=True)


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    address = db.Column(db.String(225))
    address_line_two = db.Column(db.String(225))
    category_id = db.Column(db.Integer())
    city = db.Column(db.String(225))
    create_date = db.Column(db.DateTime())
    country = db.Column(db.String(225))
    description = db.Column(db.String(425))
    end_date = db.Column(db.DateTime())
    invite_status_id = db.Column(db.Integer())
    last_edit_date = db.Column(db.DateTime())
    last_host_view = db.Column(db.DateTime())
    name = db.Column(db.String(225))
    start_date = db.Column(db.DateTime())
    state = db.Column(db.String(225))
    status_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    zip_code = db.Column(db.String(225))

    # Many-to-many
    # https://github.com/mattupstate/overholt/blob/master/overholt/stores/models.py
    guests = db.relationship('Guest', secondary=events_guests,
                               backref=db.backref('events', lazy='joined'))

    # Many-to-many
    items = db.relationship('Item', secondary=events_items,
                            backref=db.backref('events', lazy='joined'))

    def __init__(self, active, address, address_line_two, category_id, city, country,
                 description, end_date, invite_status_id, last_edit_date, last_host_view, name,
                 start_date, state, status_id, user_id, zip_code, create_date=None):
        self.active = active
        self.address = address
        self.address_line_two = address_line_two
        self.category_id = category_id
        self.city = city
        self.country = country
        if create_date is None:
            create_date = datetime.utcnow()
        self.create_date = create_date
        self.description = description
        self.end_date = end_date
        self.invite_status_id = invite_status_id
        self.last_edit_date = last_edit_date
        self.last_host_view = last_host_view
        self.name = name
        self.start_date = start_date
        self.state = state
        self.status_id = status_id
        self.user_id = user_id
        self.zip_code = zip_code

    def __repr__(self):
        return '<Event %r>' % (self.name)


class EventSchema(ma.ModelSchema):
    guests = fields.Nested('GuestSchema', default=None, many=True)
    items = fields.Nested('ItemSchema', default=None, many=True)

    class Meta:
        model = Event


event_schema = EventSchema()


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    name = db.Column(db.String(225))
    status_code = db.Column(db.Integer())

    def __init__(self, active, name, status_code):
        self.active = active
        self.name = name
        self.status_code = status_code

        def __repr__(self):
            return 'Category %r>' % self.name


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category


category_schema = CategorySchema()


class ItemCategory(db.Model):
    __tablename__ = 'item_categories'

    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    name = db.Column(db.String(225))
    code = db.Column(db.Integer())

    def __init__(self, active, name, code):
        self.active = active
        self.name = name
        self.code = code

        def __repr__(self):
            return 'ItemCategory %r>' % self.name


class ItemCategorySchema(ma.ModelSchema):
    class Meta:
        model = ItemCategory


item_category_schema = ItemCategorySchema()


class Status(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(225))
    status_code = db.Column(db.Integer())

    def __init__(self, name, status_code):
        self.name = name
        self.status_code = status_code

        def __repr__(self):
            return 'Status %r>' % self.name


class StatusSchema(ma.ModelSchema):
    class Meta:
        model = Status

status_schema = StatusSchema()


class InviteStatus(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(225))
    status_code = db.Column(db.Integer())

    def __init__(self, name, status_code):
        self.name = name
        self.status_code = status_code

        def __repr__(self):
            return 'Status %r>' % self.name


class InviteStatusSchema(ma.ModelSchema):
    class Meta:
        model = InviteStatus

invite_status_schema = InviteStatusSchema()


# class Member(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     chat_id = db.Column(db.Integer())
#     name = db.Column(db.String(225))
#     status_code = db.Column(db.Integer())
#     user_id = db.Column(db.Integer())
#
#     def __init__(self, chat_id, name, status_code, user_id):
#         chat_id = chat_id
#         self.name = name
#         self.status_code = status_code
#         self.user_id = user_id
#
#         def __repr__(self):
#             return 'Status %r>' % self.name
#
#
# class MemberSchema(ma.ModelSchema):
#     class Meta:
#         model = Member
#
#
# member_schema = MemberSchema()
#
#
# class Message(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     chat_id = db.Column(db.Integer())
#     created_at = db.Column(db.DateTime())
#     status_code = db.Column(db.Integer())
#     text = db.Column(db.String(225))
#     user_id = db.Column(db.Integer())
#
#     def __init__(self, chat_id, status_code, text, user_id, created_at=None):
#         self.chat_id = chat_id
#         if created_at is None:
#             created_at = datetime.utcnow()
#         self.status_code = status_code
#         self.text = text
#         self.user_id = user_id
#
#         def __repr__(self):
#             return 'Status %r>' % self.status_code
#
#
# class MessageSchema(ma.ModelSchema):
#     class Meta:
#         model = Message
#
#
# message_schema = MessageSchema()
#
#
# class Chat(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(225))
#     party_id = db.Column(db.Integer())
#     status_code = db.Column(db.Integer())
#
#     members = db.relationship('Member', secondary=chat_member,
#                                backref=db.backref('chat', lazy='joined'))
#
#     messages = db.relationship('Message', secondary=chat_message,
#                                  backref=db.backref('chat', lazy='joined'))
#
#     def __init__(self, name, party_id, status_code):
#         self.name = name
#         self.party_id = party_id
#         self.status_code = status_code
#
#         def __repr__(self):
#             return 'Status %r>' % self.name
#
#
# class ChatSchema(ma.ModelSchema):
#     members = fields.Nested('MemberSchema', default=None, many=True)
#     messages = fields.Nested('MessageSchema', default=None, many=True)
#
#     class Meta:
#         model = Chat
#
#
# chat_schema = ChatSchema()
