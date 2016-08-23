from flaskapp import app
from flaskapp.core import db
from flaskapp.events.models import Event, Category, Status

def populate_status():
    status_active = Status(name='active', description='active item', status_code=001)
    status_inactive = Status(name='inactive', description='inactive item', status_code=002)

    db.session.add(status_active)
    db.session.add(status_inactive)
    db.session.commit()

with app.app_context():

    populate_status()
