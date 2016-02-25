from flask import abort, Flask, render_template, request
from flaskapp.utils import get_instance_folder_path
from flaskapp.main.controllers import main
from flaskapp.admin.controllers import admin
from flaskapp.config import configure_app

app = Flask(__name__,
            instance_path=get_instance_folder_path(),
            instance_relative_config=True,
            template_folder='templates')

configure_app(app)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

@app.route('/')
def home():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
	app.logger.error('Page not found: %s', (request.path))
	return render_template('404.htm'), 4044

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.htm'), 500

app.register_blueprint(main, url_prefix='/main')
app.register_blueprint(admin, url_prefix='/admin')
