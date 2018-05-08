
# Settings

DEBUG = True
use_reloader=False
TESTING = False

CACHE_TYPE = 'simple'

## SQLite Connection
# SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
## PostgreSQL local connection
SQLALCHEMY_DATABASE_URI = 'postgresql://puser:Password1@localhost/devdb1'
SECRET_KEY = 'a9eec0e0-23b7-4788-9a92-318347b9a39a'

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Mail
# Required for Flask-Security registration to function properly
MAIL_DEFAULT_SENDER = 'service@loveschaos.com'
MAIL_SERVER = 'smtp.mailgun.org'
MAIL_PORT = 25
MAIL_USE_TLS = True
# Personal Media Template email configs
MAIL_USERNAME = 'postmaster@mg.loveschaos.com'
MAIL_PASSWORD = '05f20eb390515bce00f8d19d7fb5bbd5'

# Flask-Security
# User Model confirmed_at needs to be uncommented
SECURITY_CONFIRMABLE = False # Prod change
SECURITY_CHANGEABLE = True
SECURITY_RECOVERABLE = True
SECURITY_REGISTERABLE = True
SECURITY_POST_CHANGE_VIEW = '/user'
SECURITY_POST_LOGIN_VIEW = '/main'
SECURITY_POST_LOGOUT_VIEW = '/'
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False # Prod change
SECURITY_POST_REGISTER_VIEW = '/main'
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_TRACKABLE = True
SECURITY_PASSWORD_SALT = 'Some_salt'
SECURITY_EMAIL_SENDER = 'service@loveschaos.com'

# Configure logging
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Flask-APScheduler
JOBS = [
    # {
    #     'id': 'job1',
    #     'func': 'flaskapp.apsjobs:events_check',
    #     'trigger': 'interval',
    #     'seconds': 30
    # },
    # {
    #     'id': 'job2',
    #     'func': 'flaskapp.apsjobs:events_invites_status_check',
    #     'trigger': 'interval',
    #     'seconds': 60
    # }
]
SCHEDULER_VIEWS_ENABLED = True
