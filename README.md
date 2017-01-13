# FlaskApp
Flask app using modular blueprints.

Features:

- Flask-Security
- Jinja2 templating
- Embedded AngularJS

This webapp requires these programs: 

- Python 2.7.*
- pip
- virtualenv
- bower

#### 1. Activate virtualenv (run at root of project)

	$ virtualenv env
	$ source env/bin/activate

#### 2. Install all required Python libraries

	$ pip install -r requirements.txt

#### 3. Install SQLite(or postgreSQL, depending on connection) test data (run at root of project)

    $ python seed.py

#### 4. Run the Flask project (run at root of project)

    $ python run.py
