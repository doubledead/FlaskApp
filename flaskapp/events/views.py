from flask import Blueprint, render_template
from flask import request, redirect, url_for, json, current_app
from ..core import db
from flask_security import login_required, current_user
from datetime import datetime
from .forms import NewEventForm, UpdateEventForm, UpdateItemForm, UpdateSubItemForm
from .models import Event, event_schema, Guest, guest_schema, Item, item_schema, Subitem, subitem_schema
from sqlalchemy import exc
from ..helpers import JsonSerializer

events = Blueprint('events', __name__, template_folder='templates')

@events.route('/')
@login_required
def index():
    user_id = current_user.id
    events = Event.query.filter_by(user_id=user_id)

    events_count = events.count()


    events_invited = Event.query.filter(Event.guests.any(Guest.email.contains(current_user.email)))
    events_invited_count = events_invited.count()
    # events_invited = Guest.query.filter(Guest.events.any(email=current_user.email)).all()

    # events_invited = Event.query.filter_by(id=user_id).first().guests

    return render_template('events/events.html', events=events, events_count=events_count,
                           events_invited=events_invited, events_invited_count=events_invited_count)

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
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zip_code = form.zip_code.data
        country = form.country.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        last_edit_date = datetime.utcnow()
        name = form.name.data
        user_id = current_user.id
        # category = Category(name='event', status_code=100)
        # status = Status(name='active', status_code=100)
        category_id = 100
        status_id = 100
        event = Event(address, city, state, zip_code, country, start_date,
                      end_date, last_edit_date, name, user_id, status_id, category_id)

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
    if request.method =="GET":
        user_id = current_user.id
        event = Event.query.filter_by(id=event_id).first_or_404()

        guests = event.guests

        items = event.items

        return render_template("events/show.html", event=event, guests=guests, items=items, user_id=user_id)

@events.route('/update/<event_id>', methods=['GET', 'POST'])
@login_required
def update(event_id):
    event = Event.query.filter_by(id=event_id).first_or_404()

    user_id = current_user.id
    form = UpdateEventForm()
    if request.method == "POST" and form.validate():
        event.address = form.address.data
        event.city = form.city.data
        event.country = form.country.data
        event.end_date = form.end_date.data
        event.last_edit_date = datetime.utcnow()
        event.name = form.name.data
        event.start_date = form.start_date.data
        event.state = form.state.data
        event.user_id = user_id
        event.zip_code = form.zip_code.data

        try:
            db.session.commit()
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)

        return redirect(url_for('events.show', event_id=event.id))
    elif request.method != "POST":
        form.address.data = event.address
        form.city.data = event.city
        form.country.data = event.country
        form.end_date.data = event.end_date
        form.name.data = event.name
        form.start_date.data = event.start_date
        form.state.data = event.state
        form.zip_code.data = event.zip_code

    return render_template("events/update.html", event=event, form=form)

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

@events.route('/gettest', methods=['GET', 'POST'])
@login_required
def gettest():
    if request.method == "POST":
        data = request.get_json()

        testId = data["testId"]

        event = Event.query.filter_by(id=testId).first_or_404()
        guests = event.guests
        # dict_data = event.__dict__
        print(guests)

        # for e in dict_data:
        #     # ee = e.items()
        #     print(e)

        # Serialize SQLAlchemy object to JSON
        dump_data = event_schema.dump(event).data
        # dump_data = guest_schema.dump(event.guests).data

        # return json.dumps(event.name)
        return json.dumps(dump_data)

# Endpoint for JSMVCApp to hit
@events.route('/createjs', methods=['POST'])
@login_required
def create():
    if request.method == "POST":
        data = request.get_json()

        address = data["address"]
        address_line_two = data["address_line_two"]
        # category = Category(name='Test', status_code=100)
        category_id = 100
        city = data["city"]
        country = data["country"]
        # end_date = data["end_date"]
        end_date = datetime.utcnow()
        guests_data = data["guests"]
        items_data = data["items"]
        last_edit_date = datetime.utcnow()
        name = data["name"]
        # start_date = data["start_date"]
        start_date = datetime.utcnow()
        state = data["state"]
        # status = Status(name='active', status_code=100)
        status_id = 100
        user_id = current_user.id
        zip_code = data["zip_code"]
        event = Event(address=address, address_line_two=address_line_two, category_id=category_id, city=city,
                      country=country,end_date=end_date, last_edit_date=last_edit_date,
                      name=name, start_date=start_date, state=state, status_id=status_id,
                      user_id=user_id, zip_code=zip_code)

        for g in guests_data:
            e = g['email']

            guest = Guest(email=e)
            event.guests.append(guest)

        for i in items_data:
            item_category = i['category']
            item_name = i['name']
            item_quantity = i['quantity']

            item = Item(category=item_category,name=item_name, quantity=item_quantity, quantity_claimed=0)

            subitem = Subitem(quantity=3,user_id=current_user.id)
            subitem2 = Subitem(quantity=6,user_id=current_user.id)
            item.subitems.append(subitem)
            item.subitems.append(subitem2)

            event.items.append(item)

        try:
            db.session.add(event)
            db.session.commit()
            return json.dumps({'status':'OK'})
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)

            return redirect(url_for('events.create_event'))
            return json.dumps({'status':'Error'})

    return redirect(url_for('events.display_events'))

#################### Items ################
@events.route('/item/<item_id>', methods=['GET'])
@login_required
def showitem(item_id):
    item = Item.query.filter_by(id=item_id).first_or_404()

    subitems = item.subitems

    return render_template("events/items/show.html", item=item, subitems=subitems)

@events.route('/item/update/<item_id>', methods=['GET', 'POST'])
@login_required
def updateitem(item_id):
    item = Item.query.filter_by(id=item_id).first_or_404()


    return render_template("events/items/update.html", item=item)

@events.route('item/subitem/update/<subitem_id>', methods=['GET', 'POST'])
@login_required
def updatesubitem(subitem_id):
    subitem = Subitem.query.filter_by(id=subitem_id).first_or_404()
    subitems = subitem.subitems

    form = UpdateSubItemForm()
    if request.method == "POST" and form.validate():

        for subitem in subitems:
            subitem.quantity = form.quantity.data
            subitem.user_id = current_user.id


        # item.quantity = form.quantity.data
        # item.user_id = current_user.id

        try:
            db.session.commit()
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)

        return redirect(url_for('events.claim', subitem_id=subitem.id))
    elif request.method != "POST":
        form.quantity.data = subitem.quantity

    return render_template("events/items/subitems/update.html", subitem=subitem, form=form)
