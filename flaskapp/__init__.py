from flask import Flask, render_template, request
from flask_security import SQLAlchemyUserDatastore, current_user
import logging
from .config import DevelopmentConfig

from flaskapp.utils import get_instance_folder_path
# from flaskapp.cache import cache

from .core import db, ma, mail, security, moment, scheduler
from .models import User, Role

from .users.forms import ExtendedRegisterForm, ExtendedConfirmRegisterForm

from flaskapp.main.views import main
from flaskapp.admin.views import admin
from flaskapp.users.views import user
from flaskapp.events.views import events


def create_app():
    app = Flask(__name__,
                instance_path=get_instance_folder_path(),
                instance_relative_config=True,
                template_folder='templates')

    app.config.from_object(DevelopmentConfig)

    # logging.basicConfig(format=app.config['LOGGING_FORMAT'],filename='logs.log',level=logging.DEBUG)

    # cache.init_app(app)

    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role),
                    register_form=ExtendedRegisterForm,
                    confirm_register_form=ExtendedConfirmRegisterForm)

    # Flask-APScheduler initialize and start.
    scheduler.init_app(app)
    scheduler.start()

    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    @app.context_processor
    def inject_user():
        return dict(user=current_user)


    @app.route('/')
    # @cache.cached(300)
    def home():
        return render_template('index.html')

    app.register_blueprint(main, url_prefix='/main')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(events, url_prefix='/events')

    return app
