import secrets
import os 

from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import MyUser, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/') # default
@app.route('/home') # also home, two routes are handled by the same function below
def home(): 
    posts = Post.query.all() # Query all posts from db
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # creating a random hex for the name of the picture file
    _, f_ext = os.path.splitext(form_picture.filename) # split the file name and the extension
    picture_fn = random_hex + f_ext # concatenate the random hex and the extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) 
    
    output_size = (125, 125) # resize the image to 125x125, save time and storage
    i = Image.open(form_picture) 
    i.thumbnail(output_size) # resize the image
    i.save(picture_path) 
    
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit(): # if valid on submission, update the current user's data
            if form.picture.data:
                picture_file = save_picture(form.picture.data) # calls the save_picture() above, save the picture to the static folder
                current_user.image_file = picture_file # set the current user's image file to the picture file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            # post get redirect pattern --- refresh the page using 'GET'
            return redirect(url_for('account')) # causes the browser to send a GET request instead of POST request, ignores the 'are you sure' 
    elif request.method == 'GET': # fill in user's info on page load in the forms
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # set the image file to the current user's image file
    return render_template('account.html', title='Account', 
                           image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # author is a backref in the Post model, gives us access to the entire user and it's attributes
        post = Post(title=form.title.data, content=form.content.data, author=current_user) 
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) # if the post doesn't exist, return 404, otherwise return the post
    return render_template('post.html', title=post.title, post=post)

