from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c30cdec540796525fe21a63113d6b863' # Protect against attacks, modifying cookies, cross-site attacks
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # /// is a relative path to the project directory 
db = SQLAlchemy(app) # create sqlalchemy database instance, classes/models are the database structures for SQLAlchemy
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # set the login route to tell @login_required where the login route is located
login_manager.login_message_category = 'info' # info is a bootstrap alert

from flaskblog import routes