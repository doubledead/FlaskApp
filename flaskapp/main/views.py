from flask import Blueprint, render_template

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    return render_template('main/main.html')


@main.route('/confirmation')
def post_confirmation():
    return render_template('main/post_registration.html')
