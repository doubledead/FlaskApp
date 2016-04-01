from flask import Blueprint, render_template
from flask import current_app, redirect, request, url_for
from flask_security.decorators import roles_required
from flask_security import login_required
from flaskapp.cache import cache
from flaskapp.data.models import db
from sqlalchemy import exc


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
@login_required
def index():
    return render_template('main.html')