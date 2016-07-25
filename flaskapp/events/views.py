from flask import Blueprint, render_template
from flask import request, redirect, url_for, json, current_app
from ..core import db
from flask_security import login_required, current_user
from datetime import datetime
from .forms import CreateEventForm, EditEventForm
from .models import Event
from sqlalchemy import exc

events = Blueprint('events', __name__, template_folder='templates')

@events.route('/')
@login_required
def index():
    user_id = current_user.id
    events = Event.query.filter_by(user_id=user_id)

    return render_template('events/events.html', events=events)

@events.route('/')
@login_required
def display_events():
    user_id = current_user.id
    events = Event.query.filter_by(user_id=user_id)

    return render_template("events/events.html", events=events)

@events.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm(request.form)
    user_id = current_user.id

    if request.method == 'POST' and form.validate():
        title = form.title.data
        address = form.address.data
        # city = form.city.data
        # state = form.state.data
        # zip_code = form.zip.data
        # country = form.country.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        user_id = user_id
        current_app.logger.info('Adding a new event %s.', (title))
        # event = Event(title, address, city, state, zip_code,
        #               country, create_date, start_date, end_date, user_id)
        event = Event(title, address, start_date, end_date, user_id)

        try:
            db.session.add(event)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)

        return redirect(url_for('events.display_events'))

    return render_template("events/create_event.html", form=form)

# Endpoint for AngularJS to hit
@events.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    data = request.json
    user_id = current_user.id

    title = data["title"]
    body = data["body"]
    user_id = user_id
    event = Event(title=title, body=body, user_id=user_id)

    try:
        db.session.commit()
        return json.dumps({'status':'OK'})
    except exc.SQLAlchemyError as e:
        current_app.logger.error(e)

        return redirect(url_for('main.create_entry'))
        return json.dumps({'status':'Error'})

    return redirect(url_for('events.display_events'))
