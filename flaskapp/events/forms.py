# -*- coding: utf-8 -*-
"""
    flaskapp.events.forms
    ~~~~~~~~~~~~~~~~~~~~~
    Events forms
"""

from flask_wtf import Form
from wtforms import DateField, DateTimeField, IntegerField, StringField, SelectField, FieldList
from wtforms import validators


class UpdateEventForm(Form):
    name = StringField('Event Name', [
        validators.DataRequired(),
        validators.Length(min=1, max=30)
    ])
    address = StringField('Address', [
        validators.DataRequired(),
        validators.Length(min=1, max=70)
    ])
    address_line_two = StringField('', [
        validators.Length(max=30)
    ])
    city = StringField('City', [
        validators.DataRequired(),
        validators.Length(min=1, max=70)
    ])
    state = StringField('State', [
        validators.DataRequired(),
        validators.Length(min=1, max=70)
    ])
    zip_code = StringField('Zip Code', [
        validators.DataRequired(),
        validators.Length(min=1, max=70)
    ])
    country = StringField('Country', [
        validators.DataRequired(),
        validators.Length(min=1, max=70)
    ])
    start_date = DateField('Start Date', [validators.DataRequired()], format='%m-%d-%Y')
    status = SelectField(u'Status', coerce=int)
    end_date = DateField('End Date', [validators.DataRequired()], format='%m-%d-%Y')
    # birthdate = DateTimeField('Birth Date', format='%m/%d/%Y %I:%M:%S %p')
    # birthdate = DateField('Birth Date', format='%Y-%m-%d')
