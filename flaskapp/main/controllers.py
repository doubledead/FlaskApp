from flask import Blueprint, render_template
from flask_security import login_required
from flaskapp.data.models import db


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
@login_required
def index():
    return render_template('main.html')