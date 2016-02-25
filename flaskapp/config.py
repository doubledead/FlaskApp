import os
import logging

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    # sqlite :memory: identifier is the default if no filepath is present
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Temp/flaskapp.db'


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

config = {
    "development": "flaskapp.config.DevelopmentConfig",
    "testing": "flaskapp.config.TestingConfig",
    "default": "flaskapp.config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLAKS_CONFIGURATION', 'default')
    app.config.from_object(config[config_name]) # object-based default configuration
    app.config.from_pyfile('config.cfg', silent=True) # instance-folders configuration