from flask import Blueprint, render_template
from flask import request, redirect, url_for, json, current_app
from ..core import db
from flask_security import login_required, current_user
from datetime import datetime
from .forms import CreateEventForm, UpdateEventForm
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
        status = 1
        title = form.title.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zip_code = form.zip_code.data
        country = form.country.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        last_edit_date = datetime.utcnow()
        user_id = user_id
        current_app.logger.info('Adding a new event %s.', (title))
        event = Event(status, title, address, city, state, zip_code,
                      country, start_date, end_date, last_edit_date, user_id)

        try:
            db.session.add(event)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)

        return redirect(url_for('events.display_events'))

    return render_template("events/create_event.html", form=form)

@events.route('/<event_id>', methods=['GET', 'POST'])
@login_required
def show(event_id):
    event = Event.query.filter_by(id=event_id).first_or_404()

    return render_template("events/show.html", event=event)

@events.route('/edit/<event_id>', methods=['GET', 'POST'])
@login_required
def update(event_id):
    event = Event.query.filter_by(id=event_id).first_or_404()

    user_id = current_user.id
    form = UpdateEventForm()
    if request.method == "POST" and form.validate():
        event.title = form.title.data
        event.address = form.address.data
        event.city = form.city.data
        event.state = form.state.data
        event.zip_code = form.zip_code.data
        event.country = form.country.data
        event.start_date = form.start_date.data
        event.end_date = form.end_date.data
        event.last_edit_date = datetime.utcnow()
        event.user_id = user_id

        try:
            db.session.commit()
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)

        return redirect(url_for('events.show', event_id=event.id))
    elif request.method != "POST":
        form.title.data = event.title
        form.address.data = event.address
        form.city.data = event.city
        form.state.data = event.state
        form.zip_code.data = event.zip_code
        form.country.data = event.country
        form.start_date.data = event.start_date
        form.end_date.data = event.end_date

    return render_template("events/edit.html", event=event, form=form)

@events.route('/delete/<event_id>', methods=['GET', 'POST'])
@login_required
def delete(event_id):
    event = Event.query.filter_by(id=event_id).first_or_404()
    user_id = current_user.id
    if user_id == event.user_id:
        try:
            db.session.delete(event)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)

        return redirect(url_for('events.display_events'))

    return redirect(url_for('events.display_events'))

# Endpoint for AngularJS to hit
@events.route('/createjs', methods=['GET', 'POST'])
@login_required
def create():
    data = request.json
    user_id = current_user.id

    status = 1
    title = data["title"]
    address = data["address"]
    city = data["city"]
    state = data["state"]
    zip_code = data["zip_code"]
    country = data["country"]
    start_date = data["start_date"]
    end_date = data["end_date"]
    last_edit_date = datetime.utcnow()
    user_id = user_id
    event = Event(statsy=status, title=title, address=address, city=city, state=state,
                  zip_code=zip_code, country=country, start_date=start_date,
                  end_date=end_date, last_edit_date=last_edit_date, user_id=user_id)

    try:
        db.session.commit()
        return json.dumps({'status':'OK'})
    except exc.SQLAlchemyError as e:
        current_app.logger.error(e)

        return redirect(url_for('events.create_event'))
        return json.dumps({'status':'Error'})

    return redirect(url_for('events.display_events'))
