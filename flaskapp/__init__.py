from flask import Flask, render_template
from flaskapp.main.controllers import main
from flaskapp.admin.controllers import admin

app = Flask(__name__)

#app.config.from_object('config')

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')
