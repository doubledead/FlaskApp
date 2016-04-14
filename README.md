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

#### 3. Install all required JS libraries

  $ cd static/
  $ bower install

#### 4. Install SQLite test data (run at root of project)

  $ python seed.py

#### 5. Run the Flask project (run at root of project)

  $ python run.py