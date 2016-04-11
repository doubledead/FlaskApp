from wtforms import Form, TextField, validators

class CreateEntryForm(Form):
  title = TextField('Title', [validators.Length(min=1, max=70)])
  body = TextField('Body', [validators.Length(min=1, max=300)])