# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

# from datetime import datetime

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'c30cdec540796525fe21a63113d6b863' # Protect against attacks, modifying cookies, cross-site attacks
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # /// is a relative path to the project directory 
# db = SQLAlchemy(app) # create sqlalchemy database instance, classes/models are the database structures for SQLAlchemy
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login' # set the login route to tell @login_required where the login route is located
# login_manager.login_message_category = 'info' # info is a bootstrap alert

# from flaskblog import routes

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c30cdec540796525fe21a63113d6b863'

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes
