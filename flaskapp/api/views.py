from flask import Blueprint, jsonify
from flask_cors import CORS

api = Blueprint('api', __name__, template_folder='templates')
CORS(api)


@api.route('/')
def index():
    data = {
        'title': 'Welcome to Angular-Python App',
        'message': 'This is an example integration between Angular and Python!'
    }
    return jsonify(data)
