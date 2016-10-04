# -*- coding: utf-8 -*-
"""
    flaskapp.events.forms
    ~~~~~~~~~~~~~~~~~~~~~
    Events forms
"""

from flask_wtf import Form
from wtforms import DateField, DateTimeField, IntegerField, StringField
from wtforms import validators

class NewEventForm(Form):
    name = StringField('Name', [
        validators.DataRequired(),
        validators.Length(min=1, max=30)
    ])
    address = StringField('Address', [
        validators.DataRequired(),
        validators.Length(min=1, max=70)
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
    end_date = DateField('End Date', [validators.DataRequired()], format='%m-%d-%Y')

class UpdateEventForm(Form):
    name = StringField('name', [
        validators.DataRequired(),
        validators.Length(min=1, max=30)
    ])
    address = StringField('Address', [
        validators.DataRequired(),
        validators.Length(min=1, max=70)
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
    end_date = DateField('End Date', [validators.DataRequired()], format='%m-%d-%Y')
    # birthdate = DateTimeField('Birth Date', format='%m/%d/%Y %I:%M:%S %p')
    # birthdate = DateField('Birth Date', format='%Y-%m-%d')

class UpdateItemForm(Form):
    category = IntegerField('category', [
        validators.DataRequired(),
        validators.Length(min=1, max=3)
    ])
    name = StringField('Name', [
        validators.DataRequired(),
        validators.Length(min=1, max=70)
    ])
    quantity = IntegerField('quantity', [
        validators.DataRequired(),
        validators.Length(min=1, max=4)
    ])
    quantity_claimed = IntegerField('quantity_claimed', [
        validators.DataRequired(),
        validators.Length(min=1, max=4)
    ])

class UpdateSubItemForm(Form):
    quantity = IntegerField('quantity', [
        validators.DataRequired(),
        validators.Length(min=1, max=4)])
