from flask import Blueprint, render_template, flash
from flask import current_app, redirect, request, url_for
from flask_security.decorators import roles_required
from flask_security import login_required
from flaskapp.main.forms.entry_forms import CreateEntryForm
from flaskapp.cache import cache
from flaskapp.data.models import Entry, db
from sqlalchemy import exc


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
@login_required
def index():
    return render_template('main.html')

@main.route('/entries/')
@login_required
@cache.cached(300)
def display_entries():
  entries = [entry for entry in Entry.query.all()]
  current_app.logger.info('Displaying all entries.')

  return render_template("entries.html", entries=entries)

@main.route('/entry/create', methods=['GET', 'POST'])
@login_required
def create_entry():
  form = CreateEntryForm(request.form)
  if request.method == 'POST' and form.validate():
    title = form.title.data
    body = form.body.data
    current_app.logger.info('Adding a new entry %s.', (title))
    entry = Entry(title, body)

    try:
      db.session.add(entry)
      db.session.commit()
      cache.clear()
    except exc.SQLAlchemyError as e:
      current_app.logger.error(e)

      return redirect(url_for('main.create_entry'))

    return redirect(url_for('main.display_entries'))

  return render_template("create_entry.html", form=form)