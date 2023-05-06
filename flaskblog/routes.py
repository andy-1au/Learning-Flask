from flask import Flask, render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import MyUser, Post
from flask_login import login_user, current_user, logout_user, login_required

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
    # gets redirected to homepage is user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm() # create an instance of the class
    if form.validate_on_submit(): # if everything in the form is correct
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # hash the password in the form on validate, and decode it to a string
        user = MyUser(username=form.username.data, email=form.email.data, password=hashed_password) # generate new user using the info passed into form
        db.session.add(user)
        db.session.commit()

        # flash message is a one time thing, so if the page is refreshed, then it will disappear
        flash(f'Your account has been created! You are now able to log in.', 'success') # success is a bootstrap class to style this alert
        # .data is the just data submitted in the username section of the form
        return redirect(url_for('login')) # redirect to the home url 
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login(): 
    # gets redirected to homepage is user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm() # create an instance of the class
    if form.validate_on_submit(): # same thing here
        user = MyUser.query.filter_by(email=form.email.data).first()
        # if the user exist and the password entered is the same as the hashed password in the db
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # if remember is checked, then true 
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # use get method to avoid 'next key ' 
            #DNE returns null if DNE
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    # don't need to pass in the user, and clears remember me cookie if it was selected
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
