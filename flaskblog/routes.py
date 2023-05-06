from datetime import datetime
import secrets
import os 

from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import MyUser, Post
from flask_login import login_user, current_user, logout_user, login_required

# HOME ROUTE -----------------------------------------------------------------
@app.route('/') # default
@app.route('/home') # also home, two routes are handled by the same function below
def home(): 
    page = request.args.get('page', 1, type=int) # get the page number from the url, default to 1, and type is int
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # 5 posts per page, ordered by most recent data
    # posts = Post.query.order_by(Post.date_posted.desc()).all() # Query all posts from db in descending order by date_posted
    return render_template('home.html', posts=posts)
# ----------------------------------------------------------------------------

# ABOUT ROUTE ----------------------------------------------------------------
@app.route("/about")
def about():
    return render_template('about.html', title='About')
# ----------------------------------------------------------------------------

# REGISTER ROUTE -------------------------------------------------------------
@app.route("/register", methods=['GET', 'POST'])
def register(): 
    # gets redirected to homepage is user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm() # create an instance of the class
    # validate_on_submit() is linked to form.submit() in the html file
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
# ----------------------------------------------------------------------------

# LOGIN ROUTE ----------------------------------------------------------------
@app.route("/login", methods=['GET', 'POST'])
def login(): 
    # gets redirected to homepage is user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm() # create an instance of the class
    # validate_on_submit() is linked to form.submit() in the html file
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
# ----------------------------------------------------------------------------

# LOGOUT ROUTE ---------------------------------------------------------------
@app.route("/logout")
def logout():
    # don't need to pass in the user, and clears remember me cookie if it was selected
    logout_user()
    return redirect(url_for('home'))
# ----------------------------------------------------------------------------

# SAVE PICTURE FUNCTION ------------------------------------------------------
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
# ----------------------------------------------------------------------------

# ACCOUNT ROUTE --------------------------------------------------------------
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    # validate_on_submit() is linked to form.submit() in the html file
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
# ----------------------------------------------------------------------------

# NEW POST ROUTE -------------------------------------------------------------
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    # validate_on_submit() is linked to form.submit() in the html file
    if form.validate_on_submit():
        # author is a backref in the Post model, gives us access to the entire user and it's attributes
        post = Post(title=form.title.data, content=form.content.data, author=current_user) 
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend="New Post")
# ----------------------------------------------------------------------------

# POST/ID ROUTE --------------------------------------------------------------
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) # if the post doesn't exist, return 404, otherwise return the post
    return render_template('post.html', title=post.title, post=post)
# ----------------------------------------------------------------------------

# UPDATE POST ROUTE ----------------------------------------------------------
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) # if the post doesn't exist, return 404, otherwise return the post
    # first check if the author of the post is the current_user
    if post.author != current_user: 
        abort(403) # 403 is a HTTP response for a forbidden route
    form = PostForm() 
    # validate_on_submit() is linked to form.submit() in the html file
    if form.validate_on_submit(): 
        post.title = form.title.data
        post.content = form.content.data
        # update the date posted to the current time so posts are can be sorted by most recent
        post.date_posted = datetime.utcnow() 
        db.session.commit() # no need to add since it's already in the db, just updating
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id)) # redirect to the post page
    elif request.method == 'GET':
        # fill in form with the current post data
        form.title.data = post.title 
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', 
                           form=form, legend="Update Post")
# ----------------------------------------------------------------------------

# DELETE POST ROUTE ---------------------------------------------------------- 
@app.route("/post/<int:post_id>/delete", methods=['POST']) # only allow post requests because we don't want users to be able to go to the url and delete posts
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) # if the post doesn't exist, return 404, otherwise return the post
    # first check if the author of the post is the current_user
    if post.author != current_user: 
        abort(403) # 403 is a HTTP response for a forbidden route
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home')) # redirect to the home page
# ----------------------------------------------------------------------------

# USER POSTS ROUTE -----------------------------------------------------------
@app.route('/user/<str:username>') 
def user_posts(username): 
    page = request.args.get('page', 1, type=int)
    user = MyUser.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date.posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)
# ----------------------------------------------------------------------------

