from datetime import datetime
# from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return MyUser.query.get(int(user_id))
    

class MyUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False) # max 20 chars, must be unique, and can't be empty (null)
    email=db.Column(db.String(120), unique=True, nullable=False) 
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # doesn't have to be unique, can have default image
    password = db.Column(db.String(60), nullable=False) # hashed into 60 chars via algo, don't need to be unique, people can have the same password
    posts = db.relationship('Post', backref='author', lazy=True) 
    # posts attrib has a relationship to the Post class/model, 
    # backref is like adding another column to the Post model, use 'author' attrib to get the user's info, who created the post
    # lazy=True loads all data in one go, so that we can get all of the posts by one user
    # Function for printing out the user object

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec) # create a serializer object
        return s.dumps({'user_id': self.id}).decode('utf-8') # return a token that expires in 30 mins, and the user id
    
    @staticmethod # don't expect self as an argument
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id'] # get the user id from the token
        except:
            return None # if the token is invalid, return None
        return MyUser.query.get(user_id) # if the token is valid, return the user object with the user id

    def __repr__(self): 
        return f"MyUser('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # no () for datetime.utcnow bc we want to pass in the func as the arg and not the current time
    content = db.Column(db.Text, nullable=False)
    user_id =  db.Column(db.Integer, db.ForeignKey('my_user.id'), nullable=False) 
    # this is directly linked the user id in user table
    # user.id is lowercase because it's a direct reference to the user table/column which is default lc
    
    def __repr__(self): 
        return f"MyUser('{self.title}', '{self.date_posted}')" # don't need to post content, could be super long, just want a short description when printing these objects