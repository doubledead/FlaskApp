from flask import Blueprint, render_template
from flask import request, redirect, url_for, json, current_app
from ..core import db, mail
from flask_mail import Message
from flask_security import login_required, current_user
from datetime import datetime
from .forms import NewEventForm, UpdateEventForm, UpdateItemForm, SubItemForm
from .models import Event, event_schema, Guest, Item, item_schema, Subitem, subitem_schema
from sqlalchemy import exc
from ..utils import representsint

events = Blueprint('events', __name__, template_folder='templates')

@events.route('/')
@login_required
def index():
    user_id = current_user.id

    # All events belonging to current user.
    # events_user = Event.query.filter_by(user_id=user_id)

    # All active events belonging to current user.
    events_active = Event.query.filter_by(user_id=user_id, status_id=100)
    events_active_count = events_active.count()

    # events_active_all = Event.query.filter_by(status_id=100)

    # Events current user is a guest of
    events_invited = Event.query.filter(Event.guests.any(Guest.email.contains(current_user.email)))

    # Events invited to that are active
    events_invited_active = events_invited.filter_by(status_id=100)
    events_invited_active_count = events_invited_active.count()

    # Events belonging to current user with status 400, completed.
    events_completed = Event.query.filter_by(user_id=user_id, status_id=400).all()

    return render_template('events/events.html',
                           events_active=events_active,
                           events_active_count=events_active_count,
                           events_invited_active=events_invited_active,
                           events_invited_active_count=events_invited_active_count,
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

        # Guest invite email
        guestmsg = Message()
        guestmsg.subject = "FlaskApp - Event Invite - " + name
        guestmsg.body = "You have been invited to the following event: " + name


        # Iterate through guest email addresses
        for g in guests_data:
            e = g['email']

            guest = Guest(active=True, email=e)
            event.guests.append(guest)
            guestmsg.add_recipient(e)


        # Iterate through items
        for i in items_data:
            if i['category_id'] and representsint(i['category_id']):
                item_category_id = int(i['category_id'])
            else:
                item_category_id = 100

            if i['name'] == "":
                item_name = "Blank"
            else:
                item_name = i['name']

            if i['quantity'] and representsint(i['quantity']):
                item_quantity = int(i['quantity'])
            else:
                item_quantity = 1

            item = Item(active=True,
                        category_id=item_category_id,
                        name=item_name,
                        quantity=item_quantity,
                        quantity_claimed=0)
            event.items.append(item)

        msg = Message()
        msg.subject = "FlaskApp - Event Created: " + name
        msg.add_recipient(current_user.email)

        msg.body = "Event created: " + name


        try:
            db.session.add(event)
            db.session.commit()
            # mail.send(msg)
            # mail.send(guestmsg)
            return json.dumps({'status':'OK'})
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)
            return json.dumps({'status':'Error'})

    return render_template("events/create.html")


@events.route('/<event_id>', methods=['GET', 'POST'])
@login_required
def show(event_id):
    if request.method =="GET":
        u_id = current_user.id
        event = Event.query.filter_by(id=event_id).first_or_404()
        guests = event.guests

        return render_template("events/show.html", event=event, guests=guests, u_id=u_id)

# Endpoint for Jinja2 template
@events.route('/view/<event_id>', methods=['GET', 'POST'])
@login_required
def view(event_id):
    if request.method =="GET":
        user_id = current_user.id
        event = Event.query.filter_by(id=event_id).first_or_404()

        guests = event.guests

        items = event.items

        form = SubItemForm()

        return render_template("events/view.html", event=event, guests=guests, items=items, user_id=user_id, form=form)


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

@events.route('/item/<item_id>', methods=['GET'])
@login_required
def showitem(item_id):
    if request.method == "GET":
        user_id = current_user.id
        item = Item.query.filter_by(id=item_id).first_or_404()

        subitems = item.subitems

        return render_template("events/items/show.html", item=item, subitems=subitems, user_id=user_id)


@events.route('/getitems', methods=['GET', 'POST'])
@login_required
def getitems():
    if request.method == "POST":
        data = request.get_json()
        param_id = data['paramId']

        u_id = current_user.id

        event = Event.query.filter_by(id=param_id).first_or_404()
        items_data = event.items

        if event.user_id != u_id:
            for item in items_data:
                for i in xrange(len(item.subitems) - 1, -1, -1):
                    subitem = item.subitems[i]
                    if subitem.user_id != u_id:
                        # print subitem_schema.dump(item.subitems[i]).data
                        #### Something is happening here with multiple users.
                        del item.subitems[i]

            items = item_schema.dump(items_data).data
        else:
            items = item_schema.dump(event.items).data


        # Package data payload into a Python dictionary
        payload = {"u_Id" : u_id, "items_data" : items, "status" : "OK"}

        return json.dumps(payload)


@events.route('/updateitems', methods=['GET', 'POST'])
@login_required
def updateitems():
    if request.method == "POST":
        data = request.get_json()
        u_id = current_user.id
        # response_payload will contain status codes for each item and subitem
        response_payload = {"item_codes" : []}

        # Need to add functionality for 'Unclaim' or user setting claimed amount
        # to 0.
        for i in data:
            item = Item.query.filter_by(id=i['id']).first_or_404()
            item_max_qty = item.quantity
            item_claimed_current = item.quantity_claimed

            subitem_data = i['subitems']
            subitems_user = []
            subitems_new = []

            for si_data in subitem_data:
                if si_data['user_id'] and si_data['user_id'] == u_id:
                    subitems_user.append(si_data)
                else:
                    subitems_new.append(si_data)

            for si_user in subitems_user:
                # This Subitem query needs to be a try/except
                subitem = Subitem.query.filter_by(id=si_user['id']).first_or_404()
                subitem_qty_current = subitem.quantity

                # Data validation on Subitem quantity with Utils function.
                if si_user['quantity'] and representsint(si_user['quantity']):
                    subitem_qty = int(si_user['quantity'])
                    if subitem_qty > 0:
                        subitem_qty_data = subitem_qty
                    elif subitem_qty <= 0:
                        print("Subitem quantity is 0 or less. Current quantity used.")
                        subitem_qty_data = subitem_qty_current
                else:
                    print("New Subitem quantity is NaN. Current quantity used.")
                    subitem_qty_data = subitem_qty_current

                # Begin math
                if subitem_qty_data < subitem_qty_current:
                    subitem_qty_difference = (subitem_qty_current - subitem_qty_data)
                    subitem.quantity = subitem_qty_data

                    item.quantity_claimed = item_claimed_current - subitem_qty_difference
                elif subitem_qty_data > subitem_qty_current:
                    subitem_qty_difference = (subitem_qty_data - subitem_qty_current)

                    item_claimed_subtotal = (item_claimed_current + subitem_qty_difference)

                    if item_claimed_subtotal <= item_max_qty:
                        subitem.quantity = (subitem_qty_current + subitem_qty_difference)
                        item.quantity_claimed = item_claimed_subtotal
                    else:
                        if item_claimed_subtotal > item_max_qty:
                            if item_claimed_current < item_max_qty:
                                item_claimed_max_diff = (item_max_qty - item_claimed_current)

                                subitem.quantity = (subitem_qty_current + item_claimed_max_diff)

                                item.quantity_claimed = (item_claimed_current + item_claimed_max_diff)
                                print ("Difference added.")
                            else:
                                print ("Quantity being claimed exceeds max. Value will remain unchanged. Code: 3")
                elif subitem_qty_data == subitem_qty_current:
                    print("Quantity matches current Subitem amount. No item change.")
                else:
                    print("Something broke.")
                    return json.dumps({'status':'code:6'})
                    break

                item.subitems.append(subitem)
                print("Subitem updated. Code: 1")

            # Handle new Subitems
            if not subitems_user:
                for subitem_new in subitems_new:
                    if subitem_new['quantity'] and representsint(subitem_new['quantity']):
                        subitem_qty = int(subitem_new['quantity'])
                        print("Subitem quantity is number.")
                        if subitem_qty > 0:
                            subitem_qty_data = subitem_qty

                            if (item_claimed_current + subitem_qty_data) <= item_max_qty:
                                subitem = Subitem(active=True, quantity=subitem_qty_data, user_id=u_id)

                                item.subitems.append(subitem)
                                item.quantity_claimed = item_claimed_current + subitem_qty_data
                                print("Subitem created. Code:1")
                            else:
                                if item_claimed_current < item_max_qty:
                                    item_claimed_max_diff = (item_max_qty - item_claimed_current)

                                    subitem = Subitem(active=True, quantity=item_claimed_max_diff, user_id=u_id)

                                    item.subitems.append(subitem)
                                    item.quantity_claimed = item_claimed_current + item_claimed_max_diff
                                    print("Subitem added. Difference added. Code:1")
                                else:
                                    print("Quantity being claimed exceeds max. Item not created.")
                        elif subitem_qty <= 0:
                            print("Subitem quantity is 0 or less. Subitem not created.")
                    else:
                        print("Subitem quantity is NaN. Subitem not created.")

            # Add updated SQLAlchemy Item to session
            db.session.add(item)
        else:
            try:
                db.session.commit()
                # Eventually return response_payload
                return json.dumps({'status':'OK'})
            except exc.SQLAlchemyError as e:
                current_app.logger.error(e)
                return json.dumps({'status':'Error'})


## Updates Subitem claimed amounts.
@events.route('/updateitem', methods=['GET', 'POST'])
@login_required
def updateitem():
    if request.method == "POST":
        data = request.get_json()

        u_id = current_user.id

        item_id = data['id']
        subitem_qty_data = int(data['quantity_claimed_new'])

        item = Item.query.filter_by(id=item_id).first_or_404()
        item_max_qty = item.quantity
        item_claimed_current = item.quantity_claimed

        # Update existing Subitem. Else, create new Subitem
        for i in item.subitems:
            if i.user_id == u_id:
                subitem = i
                subitem_qty_current = subitem.quantity

                if subitem_qty_data < subitem_qty_current:
                    subitem_qty_difference = (subitem_qty_current - subitem_qty_data)
                    subitem.quantity = subitem_qty_data

                    item.quantity_claimed = item_claimed_current - subitem_qty_difference
                elif subitem_qty_data > subitem_qty_current:
                    subitem_qty_difference = (subitem_qty_data - subitem_qty_current)

                    item_claimed_subtotal = (item_claimed_current + subitem_qty_difference)

                    if item_claimed_subtotal <= item_max_qty:
                        subitem.quantity = (subitem_qty_current + subitem_qty_difference)
                        item.quantity_claimed = item_claimed_subtotal
                    else:
                        if item_claimed_subtotal > item_max_qty:
                            if item_claimed_current < item_max_qty:
                                item_claimed_max_diff = (item_max_qty - item_claimed_current)
                                subitem.quantity = (subitem_qty_current + item_claimed_max_diff)
                                item.quantity_claimed = (item_claimed_current + item_claimed_max_diff)
                                print ("Difference added.")
                            else:
                                print ("Quantity being claimed exceeds max. Value will remain unchanged. Code: 3")
                                return json.dumps({'status':'code:3'})
                elif subitem_qty_data == subitem_qty_current:
                    print("Quantity matches current Subitem amount. Updated.")
                    subitem.quantity = subitem_qty_current
                    item.quantity_claimed = item_claimed_current
                else:
                    print("Something broke.")
                    return json.dumps({'status':'code:4'})
                    break


                item.subitems.append(subitem)
                try:
                    db.session.add(item)
                    db.session.commit()
                    print("Subitem updated. Code: 1")
                    return json.dumps({'status':'OK'})
                except exc.SQLAlchemyError as e:
                    current_app.logger.error(e)
                    return json.dumps({'status':'Error'})

                break
        else:
            if (item_claimed_current + subitem_qty_data) <= item_max_qty:
                subitem = Subitem(quantity=subitem_qty_data, user_id=u_id)
                item.subitems.append(subitem)
                item.quantity_claimed = item_claimed_current + subitem_qty_data
                try:
                    db.session.add(item)
                    db.session.commit()
                    print("Subitem added.")
                    return json.dumps({'status':'OK'})
                except exc.SQLAlchemyError as e:
                    current_app.logger.error(e)
                    return json.dumps({'status':'Error'})
            else:
                if item_claimed_current < item_max_qty:
                    item_claimed_max_diff = (item_max_qty - item_claimed_current)
                    subitem = Subitem(quantity=item_claimed_max_diff, user_id=u_id)
                    item.subitems.append(subitem)
                    item.quantity_claimed = item_claimed_current + item_claimed_max_diff
                    try:
                        db.session.add(item)
                        db.session.commit()
                        print("Subitem added. Difference added.")
                        return json.dumps({'status':'OK'})
                    except exc.SQLAlchemyError as e:
                        current_app.logger.error(e)
                        return json.dumps({'status':'Error'})
                else:
                    print("Quantity being claimed exceeds max. Item not created.")
                    return json.dumps({'status':'code:3'})
