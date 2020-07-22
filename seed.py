from flaskapp import create_app
from flaskapp.core import db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
