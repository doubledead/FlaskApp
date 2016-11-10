from flask import Blueprint, render_template
from flask import request, redirect, url_for, json, current_app
from ..core import db
from flask_security import login_required, current_user
from datetime import datetime
from .forms import NewEventForm, UpdateEventForm, UpdateItemForm
from .models import Event, event_schema, Guest, Item, item_schema, Subitem
from sqlalchemy import exc

events = Blueprint('events', __name__, template_folder='templates')

@events.route('/')
@login_required
def index():
    user_id = current_user.id

    # All events belonging to current user.
    events_user = Event.query.filter_by(user_id=user_id)

    # All active events belonging to current user.
    events_active = Event.query.filter_by(user_id=user_id, status_id=100)
    events_active_count = events_active.count()

    # events_active_all = Event.query.filter_by(status_id=100)

    # This still needs to be filtered with status_id=100, active.
    events_invited = Event.query.filter(Event.guests.any(Guest.email.contains(current_user.email)))
    # events_invited = Event.query.filter(Event.guests.any(Guest.email.contains(current_user.email)))
    events_invited_count = events_invited.count()

    # events_invited_active= events_invited.query.filter_by(status_id=100)

    # Events belonging to current user with status 400, completed.
    events_completed = Event.query.filter_by(user_id=user_id, status_id=400).all()

    return render_template('events/events.html',
                           events_active=events_active,
                           events_active_count=events_active_count,
                           events_user=events_user,
                           events_invited=events_invited,
                           events_invited_count=events_invited_count,
                           events_completed=events_completed)

@events.route('/')
@login_required
def display_events():
    user_id = current_user.id
    events = Event.query.filter_by(user_id=user_id)

    return render_template("events/events.html", events=events)

# Flask WTForms Create endpoint
@events.route('/create_event', methods=['GET', 'POST'])
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

    return render_template("events/create_event.html", form=form)

# JSON format endpoint
@events.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "POST":
        data = request.get_json()

        address = data["address"]
        address_line_two = data["address_line_two"]
        category_id = data["category_id"]
        city = data["city"]
        country = data["country"]
        end_date = data["end_date"]
        guests_data = data["guests"]
        items_data = data["items"]
        last_edit_date = datetime.utcnow()
        name = data["name"]
        start_date = data["start_date"]
        state = data["state"]
        status_id = 100 # New event status
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

            event.items.append(item)

        try:
            db.session.add(event)
            db.session.commit()
            return json.dumps({'status':'OK'})
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)

            return redirect(url_for('events.create'))
            return json.dumps({'status':'Error'})

        return redirect(url_for('events.display_events'))

    return render_template("events/create.html")

@events.route('/<event_id>', methods=['GET', 'POST'])
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


#################### Items ################

@events.route('/getitems', methods=['GET', 'POST'])
@login_required
def getitems():
    if request.method == "POST":
        data = request.get_json()

        paramId = data["paramId"]

        event = Event.query.filter_by(id=paramId).first_or_404()

        # Serialize SQLAlchemy object to JSON
        serialized_event = event_schema.dump(event).data

        ##### Add user specific data payload.
        ##### All Subitems for Event creator only.
        ### One Subitem for Guests.

        # Package data payload into a Python dictionary
        payload = {"current_user_id" : current_user.id, "event_data" : serialized_event, "claimed_item_temp" : 0}

        # return dictionary as JSON object
        return json.dumps(payload)


@events.route('/item/<item_id>', methods=['GET'])
@login_required
def showitem(item_id):
    if request.method == "GET":
        user_id = current_user.id
        item = Item.query.filter_by(id=item_id).first_or_404()

        subitems = item.subitems

        return render_template("events/items/show.html", item=item, subitems=subitems, user_id=user_id)


@events.route('/updateitem', methods=['GET', 'POST'])
@login_required
def updateitem():
    if request.method == "POST":
        data = request.get_json()

        item_id = data['id']
        # subitem_qty_data = int(data['quantity_claimed'])
        subitem_qty_data = int(data['quantity_claimed_new'])
        ## Refer to getitems() notes above.
        # subitem_qty_data = 0

        item = Item.query.filter_by(id=item_id).first_or_404()
        item_max_qty = item.quantity
        item_claimed_current = item.quantity_claimed

        # Update existing Subitem.
        # Else, create new Subitem
        for i in item.subitems:
            if i.user_id == current_user.id:
                subitem = i
                subitem_qty_current = subitem.quantity

                if subitem_qty_data < subitem_qty_current:
                    subitem_qty_difference = (subitem_qty_current - subitem_qty_data)
                    subitem.quantity = subitem_qty_data

                    item.quantity_claimed = item_claimed_current - subitem_qty_difference
                elif subitem_qty_data > subitem_qty_current:
                    subitem_qty_difference = (subitem_qty_data - subitem_qty_current)

                    if (item_claimed_current + subitem_qty_difference) <= item_max_qty:
                        subitem.quantity = subitem_qty_current + subitem_qty_difference
                        item.quantity_claimed = (item_claimed_current + subitem_qty_difference)
                    else:
                        print('Quantity being claimed exceeds max. Value will remain unchanged.')
                        return json.dumps({'status':'code:3'})


                # Append updated Subitem to Item's Subitems
                item.subitems.append(subitem)
                try:
                    db.session.add(item)
                    db.session.commit()
                    print('Subitem updated.')
                    return json.dumps({'status':'OK'})
                except exc.SQLAlchemyError as e:
                    current_app.logger.error(e)
                    return json.dumps({'status':'Error'})

                break
        else:
            if (item_claimed_current + subitem_qty_data) <= item_max_qty:
                subitem = Subitem(quantity=subitem_qty_data,user_id=current_user.id)
                item.subitems.append(subitem)
                item.quantity_claimed = item_claimed_current + subitem_qty_data
                # print("Subitem added.")
                try:
                    db.session.add(item)
                    db.session.commit()
                    print('Subitem added.')
                    return json.dumps({'status':'OK'})
                except exc.SQLAlchemyError as e:
                    current_app.logger.error(e)
                    return json.dumps({'status':'Error'})
            else:
                print('Quantity being claimed exceeds max. Item not created.')
                return json.dumps({'status':'code:3'})


        # This will be for handling multiple items at once.
        # for i in data:
        #     item_id = i['id']
        #     item = Item.query.filter_by(id=item_id).first_or_404()
        #
        #     subitem_quantity = i['quantity_claimed']
        #
        #     subitem = Subitem(quantity=subitem_quantity,user_id=current_user.id)
        #
        #     item.subitems.append(subitem)
        #     db.session.add(item)


