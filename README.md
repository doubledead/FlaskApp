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

#### 1. Activate virtualenv (run at root of project)

	$ virtualenv env
	$ source env/bin/activate

#### 2. Install all required Python libraries

	$ pip3 install -r requirements.txt

#### 3. Install SQLite(or postgreSQL, depending on connection) test data (run at root of project)

    $ python3 seed.py

#### 4. Run the Flask project (run at root of project)

    $ python3 run.py
