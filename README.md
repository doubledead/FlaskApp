# FlaskApp
Flask app using modular blueprints.

Features:
  -Flask-Security
  -Jinja2 templating
  -Embedded AngularJS

This webapp requires these programs: 

- Python 2.7.*
- pip
- virtualenv
- bower

#### 1. Activate virtualenv (ran at root of project)

	$ virtualenv env
	$ source env/bin/activate

#### 2. Install all required Python libraries

	$ pip install -r requirements.txt

#### 3. Install all required JS libraries

  $ cd static/
  $ bower install

#### 4. Run the Flask project (ran at root of project)

	$ python seed.py
  $ python run.py