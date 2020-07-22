from flask import Blueprint, render_template, request
# from flaskapp import create_app

error = Blueprint('error', __name__, template_folder='templates')

# app = create_app()


@error.route('/')
def index():
    return render_template('index.html')


@error.errorhandler(403)
def page_forbidden():
    # app.logger.error('Page forbidden: %s', (request.path, 'Forbidden page access attempt.'))
    return render_template('errors/403.html'), 403


@error.errorhandler(404)
def page_not_found(e):
    # app.logger.error('Page not found: %s', (request.path, e))
    return render_template('errors/404.html'), 404


@error.errorhandler(500)
def internal_server_error(e):
    # app.logger.error('Server Error: %s', (request.path, e))
    return render_template('errors/500.html'), 500


@error.errorhandler(Exception)
def unhandled_exception(e):
    # app.logger.error('Unhandled Exception: %s', (request.path, e))
    return render_template('errors/500.html'), 500
