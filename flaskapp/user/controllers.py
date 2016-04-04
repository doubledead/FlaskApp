from flask import Blueprint, render_template, flash
from flask import current_app, redirect, request, url_for
from flask_security.decorators import roles_required
from flask_security import login_required
from flaskapp.data.models import db
from sqlalchemy import exc


user = Blueprint('user', __name__, template_folder='templates')


@user.route('/')
@login_required
# @roles_required('admin')
def index():
    return render_template('user_profile.html')