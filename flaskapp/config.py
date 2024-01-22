import os
import logging
from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    # sqlite :memory: identifier is the default if no filepath is present
    
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'flaskapp.log'
    LOGGING_LEVEL = logging.DEBUG
    CACHE_TYPE = 'simple'

     # Flask-Mail
     # Required for Flask-Security registration to function properly
    MAIL_DEFAULT_SENDER = 'info@flaskapp.us'
    MAIL_SERVER = 'smtp.mailgun.org'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'username'
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")

    # Flask-Security
    SECURITY_POST_LOGIN_VIEW = '/main'
    SECURITY_POST_LOGOUT_VIEW = '/'
    SECURITY_POST_REGISTER_VIEW = '/main'
    SECURITY_PASSWORD_SALT = getenv("SECURITY_PASSWORD_SALT")
    SECURITY_EMAIL_SENDER = 'service@test.com'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") 
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
        
    SECRET_KEY = getenv("SECRET_KEY")

    # Flask-Security
    SECURITY_CONFIRMABLE = False
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
        


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") 
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SECRET_KEY = getenv("SECRET_KEY")
