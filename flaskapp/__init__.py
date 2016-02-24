from flask import Flask, render_template
from flaskapp.utils import get_instance_folder_path
from flaskapp.main.controllers import main
from flaskapp.admin.controllers import admin

app = Flask(__name__,
            instance_path=get_instance_folder_path(),
            instance_relative_config=True,
            template_folder='templates')

app.config.from_object('config')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

@app.route('/')
def home():
    return render_template('index.html')

app.register_blueprint(main, url_prefix='/main')
app.register_blueprint(admin, url_prefix='/admin')
