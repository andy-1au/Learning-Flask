import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

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

app.config['MAIL_SERVER'] = 'smtp.googlemail.com' # smtp server for gmail
app.config['MAIL_PORT'] = 587 # port for gmail
app.config['MAIL_USE_TLS'] = True # encryption
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_USER") # email username
app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASS") # email password

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail(app)

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)