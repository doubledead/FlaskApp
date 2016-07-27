# -*- coding: utf-8 -*-
"""
    flaskapp.entries.forms
    ~~~~~~~~~~~~~~~~~~~~~
    Entries forms
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField, DateField, DateTimeField
from wtforms import validators

class CreateEntryForm(Form):
    # title = TextField('Title', [validators.Length(min=1, max=70)])
    title = StringField('Title', [
        validators.DataRequired(),
        validators.Length(min=1, max=70)
    ])
    body = TextAreaField('Body', [
        validators.DataRequired(),
        validators.Length(min=1, max=300)
    ])
    post_date = DateField('Post Date', [validators.DataRequired()], format='%m-%d-%Y')

class UpdateEntryForm(Form):
    title = StringField('Title', [
        validators.DataRequired(),
        validators.Length(min=1, max=70)
    ])
    body = TextAreaField('Body', [
        validators.DataRequired(),
        validators.Length(min=1, max=300)
    ])
    post_date = DateField('Post Date', [validators.DataRequired()], format='%m-%d-%Y')
