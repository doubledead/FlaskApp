from ..core import db
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

entries_tags = db.Table(
    'entries_tags',
    db.Column('entry_id', db.Integer(), db.ForeignKey('entries.id')),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tags.id')))

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(225))

class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    post_date = db.Column(db.DateTime())
    body = db.Column(db.String(300))
    create_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    tags = db.relationship('Tag',
                                 secondary=entries_tags,
                                 backref=db.backref('entries', lazy='joined'))

    def __init__(self, title, post_date, body, user_id, create_date=None):
        self.title = title
        self.post_date = post_date
        self.body = body
        self.user_id = user_id
        if create_date is None:
            create_date = datetime.utcnow()
        self.create_date = create_date

    def __repr__(self):
        return '<Entry %r>' % self.title

