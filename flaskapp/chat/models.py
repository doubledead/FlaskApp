from ..core import db, ma
from datetime import datetime
from marshmallow import fields


chat_member = db.Table(
    'chat_member',
    db.Column('chat_id', db.Integer(), db.ForeignKey('chat.id')),
    db.Column('member_id', db.Integer(), db.ForeignKey('member.id')))

chat_message = db.Table(
    'chat_message',
    db.Column('chat_id', db.Integer(), db.ForeignKey('chat.id')),
    db.Column('message_id', db.Integer(), db.ForeignKey('message.id')))


class Member(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    chat_id = db.Column(db.Integer(), nullable=True)
    email = db.Column(db.String(225), nullable=False)
    guest_id = db.Column(db.Integer(), nullable=False)
    name = db.Column(db.String(225), nullable=True)
    status_code = db.Column(db.Integer(), nullable=True)
    role_id = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.Integer(), nullable=True)

    def __init__(self, chat_id, email, guest_id, name, status_code, role_id, user_id):
        self.chat_id = chat_id
        self.email = email
        self.guest_id = guest_id
        self.name = name
        self.status_code = status_code
        self.role_id = role_id
        self.user_id = user_id

    def __repr__(self):
        return 'Member %r>' % self.id


class MemberSchema(ma.Schema):
    class Meta:
        model = Member


member_schema = MemberSchema()


class Message(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    chat_id = db.Column(db.Integer())
    created_at = db.Column(db.DateTime())
    status_code = db.Column(db.Integer())
    text = db.Column(db.String(225))
    member_id = db.Column(db.Integer())

    def __init__(self, chat_id, status_code, text, member_id, created_at=None):
        self.chat_id = chat_id
        if created_at is None:
            self.created_at = datetime.utcnow()
        self.status_code = status_code
        self.text = text
        self.member_id = member_id

    def __repr__(self):
        return 'Message %r>' % self.id


class MessageSchema(ma.Schema):
    class Meta:
        model = Message


message_schema = MessageSchema()


class Chat(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(225))
    party_id = db.Column(db.Integer(), nullable=False)
    status_code = db.Column(db.Integer(), nullable=True)

    members = db.relationship('Member', secondary=chat_member, backref=db.backref('chat', lazy='joined'))

    messages = db.relationship('Message', secondary=chat_message, backref=db.backref('chat', lazy='joined'))

    def __init__(self, name, party_id, status_code):
        self.name = name
        self.party_id = party_id
        self.status_code = status_code

    def __repr__(self):
        return 'Chat %r>' % self.id


class ChatSchema(ma.Schema):
    members = fields.Nested('MemberSchema', default=None, many=True)
    messages = fields.Nested('MessageSchema', default=None, many=True)

    class Meta:
        model = Chat


chat_schema = ChatSchema()
