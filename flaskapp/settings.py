
# Settings

DEBUG = False
TESTING = False

CACHE_TYPE = 'simple'

## Heroku flaskapp-pro
SQLALCHEMY_DATABASE_URI = 'postgres://henizvlbiygjoa:Ze4ZM7v9ApX2CK0HFQAi8EpdX-@ec2-54-235-125-172.compute-1.amazonaws.com:5432/dfgb1crsk1t3d9'
# SQLALCHEMY_DATABASE_URI = 'postgres://aghyweatfnlblv:d37447d434c2f322f09988076a8ac4d9e3a9c6e4aa6cebfcce963c9d2d803b50@ec2-50-19-224-165.compute-1.amazonaws.com:5432/d6sthrt9kr6aal'
SECRET_KEY = 'a9eec0e0-23b7-4788-9a92-318347b9a39a'

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Mail
MAIL_DEFAULT_SENDER = 'service@loveschaos.com'
MAIL_SERVER = 'smtp.mailgun.org'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = 'postmaster@mg.loveschaos.com'
MAIL_PASSWORD = '05f20eb390515bce00f8d19d7fb5bbd5'

# Flask-Security
SECURITY_CONFIRMABLE = True
SECURITY_CHANGEABLE = True
SECURITY_RECOVERABLE = True
SECURITY_REGISTERABLE = True
SECURITY_POST_CHANGE_VIEW = '/user'
SECURITY_POST_LOGIN_VIEW = '/main'
SECURITY_POST_LOGOUT_VIEW = '/'
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = True
SECURITY_POST_REGISTER_VIEW = '/main/confirmation'
SECURITY_SEND_REGISTER_EMAIL = True
SECURITY_TRACKABLE = True
SECURITY_PASSWORD_SALT = 'Some_salt'
SECURITY_EMAIL_SENDER = 'service@loveschaos.com'

# Configure logging
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Flask-APScheduler
JOBS = [
    {
        'id': 'job1',
        'func': 'flaskapp.apsjobs:events_check',
        'trigger': 'interval',
        'seconds': 30
    },
    {
        'id': 'job2',
        'func': 'flaskapp.apsjobs:events_invites_status_check',
        'trigger': 'interval',
        'seconds': 60
    }
]
SCHEDULER_VIEWS_ENABLED = True
