
# Settings

DEBUG = True
# Setting TESTING to True disables @login_required checks
TESTING = False

CACHE_TYPE = 'simple'

# SQLite Connection
# SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
# PostgreSQL Connection
# SQLALCHEMY_DATABASE_URI = 'postgresql://puser:Password1@localhost/devdb1'
# Heroku DB Connection
SQLALCHEMY_DATABASE_URI = 'postgres://nljweakzhspxaa:Cl3n7ipIY1AvTk1MLyslOfZgLz@ec2-54-235-111-59.compute-1.amazonaws.com:5432/dc4t9bjie4nrtc'
SECRET_KEY = 'a9eec0e0-23b7-4788-9a92-318347b9a39a'

# Flask-Mail
# Required for Flask-Security registration to function properly
MAIL_DEFAULT_SENDER = 'service@loveschaos.com'
MAIL_SERVER = 'smtp.mailgun.org'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = 'postmaster@app612f53d0a96248fdab12a8ad2f5cc871.mailgun.org'
MAIL_PASSWORD = '9115f88eef5f0426f65301afc351d97e'

# Flask-Security
SECURITY_CONFIRMABLE = False
# SECURITY_CONFIRMABLE = True
SECURITY_CHANGEABLE = True
SECURITY_REGISTERABLE = True
SECURITY_POST_CHANGE_VIEW = '/user'
SECURITY_POST_LOGIN_VIEW = '/main'
SECURITY_POST_LOGOUT_VIEW = '/'
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False # Prod change
SECURITY_POST_REGISTER_VIEW = '/main'
SECURITY_SEND_REGISTER_EMAIL = False
# SECURITY_SEND_REGISTER_EMAIL = True
SECURITY_TRACKABLE = True
