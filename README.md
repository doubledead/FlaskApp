# FlaskApp
Fullstack Flask app using modular blueprints.

Features:

- Flask-Security
- Jinja2 templating
- Embedded AngularJS

## Dependencies

    Database

    - PostgreSQL 11+

    Flask Web API Server

	- Python ^3.6.*
	- pip
	- virtualenv

#### 1. Create Python virtual environment

	$ python3 -m venv .venv

#### 2. Activate virtual environment

	$ source .venv/bin/activate

#### 3. Install all required Python libraries

	$ pip3 install -r requirements.txt

#### 4. Install SQLite(or postgreSQL, depending on connection) test data (run at root of project)

    $ python3 seed.py
	$ python3 manage.py populate
	$ python3 manage.py create_test_users

#### 5. Run the Flask project (run at root of project)

    $ python3 run.py
