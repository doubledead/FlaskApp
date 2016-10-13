from flask import Blueprint, render_template
from flask import request, redirect, url_for, json, current_app
from ..core import db
from flask_security import login_required, current_user
from datetime import datetime
from .forms import CreateEntryForm, UpdateEntryForm
from .models import Entry, Tag
from sqlalchemy import exc

entries = Blueprint('entries', __name__, template_folder='templates')

@entries.route('/')
@login_required
def index():
    user_id = current_user.id
    entries = Entry.query.filter_by(user_id=user_id)

    return render_template('entries/entries.html', entries=entries)

@entries.route('/')
@login_required
def display_entries():
    user_id = current_user.id
    entries = Entry.query.filter_by(user_id=user_id)

    return render_template("entries/entries.html", entries=entries)

@entries.route('/create', methods=['GET', 'POST'])
@login_required
def create_entry():
    form = CreateEntryForm(request.form)

    if request.method == 'POST' and form.validate():
        title = form.title.data
        post_date = form.post_date.data
        body = form.body.data
        user_id = current_user.id
        entry = Entry(title, post_date, body, user_id)

        try:
            db.session.add(entry)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)


        return redirect(url_for('entries.display_entries'))

    return render_template("entries/create.html", form=form)

@entries.route('/<entry_id>', methods=['GET'])
@login_required
def show(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()

    tags = entry.tags

    return render_template("entries/show.html", entry=entry, tags=tags)

@entries.route('/edit/<entry_id>', methods=['GET', 'POST'])
@login_required
def update(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()

    form = UpdateEntryForm()
    if request.method == "POST" and form.validate():
        entry.title = form.title.data
        entry.post_date = form.post_date.data
        entry.body = form.body.data

        try:
            db.session.commit()
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)

        return redirect(url_for('entries.show', entry_id=entry.id))
    elif request.method != "POST":
        form.title.data = entry.title
        form.post_date.data = entry.post_date
        form.body.data = entry.body

    return render_template("entries/edit.html", entry=entry, form=form)

@entries.route('/delete/<entry_id>', methods=['GET', 'POST'])
@login_required
def delete(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    user_id = current_user.id
    if user_id == entry.user_id:
        try:
            db.session.delete(entry)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)

        return redirect(url_for('entries.display_entries'))

    return redirect(url_for('entries.display_entries'))


# Endpoint for AngularJS to hit
@entries.route('/createjs', methods=['GET', 'POST'])
@login_required
def create():
    # http://flask.pocoo.org/docs/0.11/api/#flask.Request.get_json
    data = request.get_json()

    title = data['title']
    # post_date = data['post_date']
    post_date = datetime.utcnow()
    body = data['body']
    user_id = current_user.id
    tags_data = data['tags']
    entry = Entry(title=title, post_date=post_date, body=body, user_id=user_id)

    # current_app.logger.info('Tags %s.', (tags))
    # print(data)
    # print(tags_data)

    # tags is a list of dict objects, a dictionary list

    # This does not work consistently because dictionaries
    # are unordered
    # for t in tags_data:
    #     tt = t.items()
    #
    #     c = tt[0][1]
    #     d = tt[1][1]
    #     tag = Tag(category=c,description=d)
    #     entry.tags.append(tag)

    # tags_data is JSON format
    for ttt in tags_data:
        cat = ttt['category']
        des = ttt['description']
        tag = Tag(category=cat, description=des)
        entry.tags.append(tag)


    try:
        db.session.add(entry)
        db.session.commit()
        return json.dumps({'status':'OK'})
    except exc.SQLAlchemyError as e:
        current_app.logger.error(e)

        return redirect(url_for('entries.create_event'))
        return json.dumps({'status':'Error'})

    return redirect(url_for('entries.display_entries'))
