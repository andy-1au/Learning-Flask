from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c30cdec540796525fe21a63113d6b863' # Protect against attacks, modifying cookies, cross-site attacks
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # /// is a relative path to the project directory 
db = SQLAlchemy(app) # create sqlalchemy database instance, classes/models are the database structures for SQLAlchemy

class User(db.Model):
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
    def __repr__(self): 
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # no () for datetime.utcnow bc we want to pass in the func as the arg and not the current time
    content = db.Column(db.Text, nullable=False)
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    # this is directly linked the user id in user table
    # user.id is lowercase because it's a direct reference to the user table/column which is default lc
    
    def __repr__(self): 
        return f"User('{self.title}', '{self.date_posted}')" # don't need to post content, could be super long, just want a short description when printing these objects

posts = [
    {
        'author': 'Andy Lau',
        'title': 'Blog Post 1',
        'content': 'This is my first blog post.',
        'date_posted': 'May 04, 2023',
    },
    {
        'author': 'Dennis Lam',
        'title': 'Blog Post 2',
        'content': 'Hi, my name is Dennis Lam.',
        'date_posted': 'May 04, 2023',
    }
]

@app.route('/') # default
@app.route('/home') # also home, two routes are handled by the same function below
def home(): 
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register(): 
    form = RegistrationForm() # create an instance of the class
    if form.validate_on_submit(): # if .validate_on_submit() returns true, call the flash() message function 
        # flash message is a one time thing, so if the page is refreshed, then it will disappear
        flash(f'Account created for {form.username.data}!', 'success') # success is a bootstrap class to style this alert
        # .data is the just data submitted in the username section of the form
        return redirect(url_for('home')) # redirect to the home url 
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login(): 
    form = LoginForm() # create an instance of the class
    if form.validate_on_submit(): # same thing here
        #temp test data before database
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':     
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    # for creating the .db file
    with app.app_context():
        db.create_all()
        app.run(debug=True) # run via python [app.py]