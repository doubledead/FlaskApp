# -*- coding: utf-8 -*-
"""
    flaskproject.users.forms
    ~~~~~~~~~~~~~~~~~~~~~
    User forms
"""

from flask_wtf import Form
from wtforms import StringField, DateField, DateTimeField
from wtforms import validators

from flask_security.forms import RegisterForm, ConfirmRegisterForm

class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
    birth_date = DateField('Birth Date', [validators.DataRequired()], format='%m-%d-%Y')

class ExtendedRegisterForm(RegisterForm):
    birth_date = DateField('Birth Date', [validators.DataRequired()], format='%m-%d-%Y')



class EditProfileForm(Form):
    email = StringField('Email Address', [
        validators.DataRequired(),
        validators.Length(min=6, max=30)
    ])
    first_name = StringField('First Name', [validators.Length(max=70)])
    last_name = StringField('Last Name', [validators.Length(max=70)])
