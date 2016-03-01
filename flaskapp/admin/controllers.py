from flask import Blueprint, render_template
from flask import current_app, redirect, request, url_for
from flask_security.decorators import roles_required
from flaskapp.data.models import db
from sqlalchemy import exc


admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/')
@roles_required('admin')
def index():
    return render_template('admin_index.html')