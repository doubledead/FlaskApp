from flask import Blueprint, render_template
from flask import request, redirect, url_for, json, current_app
from ..core import db
from flask_security import login_required, current_user
from datetime import datetime
from .forms import NewEventForm, UpdateEventForm
from .models import Category, Event, Guest, Status
from sqlalchemy import exc

events = Blueprint('events', __name__, template_folder='templates')

@events.route('/')
@login_required
def index():
    user_id = current_user.id
    events = Event.query.filter_by(user_id=user_id)


    events_invited = Event.query.filter(Event.guests.any(Guest.email.contains(current_user.email)))
    # events_invited = Guest.query.filter(Guest.events.any(email=current_user.email)).all()

    # events_invited = Event.query.filter_by(id=user_id).first().guests

    return render_template('events/events.html', events=events, events_invited=events_invited)

@events.route('/')
@login_required
def display_events():
    user_id = current_user.id
    events = Event.query.filter_by(user_id=user_id)

    return render_template("events/events.html", events=events)

@events.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = NewEventForm(request.form)

    if request.method == 'POST' and form.validate():
        title = form.title.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zip_code = form.zip_code.data
        country = form.country.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        last_edit_date = datetime.utcnow()
        user_id = current_user.id
        category = Category(name='event', status_code=100)
        status = Status(name='active', status_code=100)
        event = Event(title, address, city, state, zip_code, country,
                      start_date, end_date, last_edit_date, user_id, status, category)

        try:
            db.session.add(event)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)

        return redirect(url_for('events.display_events'))

    return render_template("events/create.html", form=form)

@events.route('/<event_id>', methods=['GET'])
@login_required
def show(event_id):
    event = Event.query.filter_by(id=event_id).first_or_404()

    guests = event.guests

    return render_template("events/show.html", event=event, guests=guests)

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

# Endpoint for JSMVCApp to hit
@events.route('/createjs', methods=['POST'])
@login_required
def create():
    if request.method == "POST":
        data = request.get_json()

        address = data["address"]
        category = Category(name='Test', status_code=100)
        city = data["city"]
        country = data["country"]
        # end_date = data["end_date"]
        end_date = datetime.utcnow()
        guests_data = data["guests"]
        last_edit_date = datetime.utcnow()
        # start_date = data["start_date"]
        start_date = datetime.utcnow()
        state = data["state"]
        status = Status(name='active', status_code=100)
        title = data["title"]
        user_id = current_user.id
        zip_code = data["zip_code"]
        event = Event(address=address, category=category, city=city,
                      country=country,end_date=end_date, last_edit_date=last_edit_date,
                      start_date=start_date,state=state, status=status, title=title,
                      user_id=user_id, zip_code=zip_code)

        for g in guests_data:
            e = g['email']

            guest = Guest(email=e)
            event.guests.append(guest)

        try:
            db.session.add(event)
            db.session.commit()
            return json.dumps({'status':'OK'})
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)

            return redirect(url_for('events.create_event'))
            return json.dumps({'status':'Error'})

    return redirect(url_for('events.display_events'))
