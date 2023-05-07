from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import MyUser, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

# REGISTER ROUTE -------------------------------------------------------------
@users.route("/register", methods=['GET', 'POST'])
def register(): 
    # gets redirected to homepage is user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

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
        return redirect(url_for('users.login')) # redirect to the home url 
    return render_template('register.html', title='Register', form=form)
# ----------------------------------------------------------------------------

# LOGIN ROUTE ----------------------------------------------------------------
@users.route("/login", methods=['GET', 'POST'])
def login(): 
    # gets redirected to homepage is user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
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
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
# ----------------------------------------------------------------------------

# LOGOUT ROUTE ---------------------------------------------------------------
@users.route("/logout")
def logout():
    # don't need to pass in the user, and clears remember me cookie if it was selected
    logout_user()
    return redirect(url_for('main.home'))
# ----------------------------------------------------------------------------

# ACCOUNT ROUTE --------------------------------------------------------------
@users.route("/account", methods=['GET', 'POST'])
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
            return redirect(url_for('users.account')) # causes the browser to send a GET request instead of POST request, ignores the 'are you sure' 
    elif request.method == 'GET': # fill in user's info on page load in the forms
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # set the image file to the current user's image file
    return render_template('account.html', title='Account', 
                           image_file=image_file, form=form)
# ----------------------------------------------------------------------------

# USER POSTS ROUTE -----------------------------------------------------------
@users.route('/user/<string:username>') 
def user_posts(username): 
    page = request.args.get('page', 1, type=int)
    user = MyUser.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)
# ----------------------------------------------------------------------------

# USER REQUEST RESET ROUTE ---------------------------------------------------
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # make sure that user is logged out
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        # get the user object from the email in the form
        user = MyUser.query.filter_by(email=form.email.data).first()
        # send the user an email with a token to reset their password
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password. Make sure check your inbox and spam folder.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)
# ----------------------------------------------------------------------------

# USER RESET PASSWORD ROUTE --------------------------------------------------
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # make sure that user is logged out
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = MyUser.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request')) # redirect to the reset request page
    # otherwise, create a form to reset the password
    form = ResetPasswordForm() 
    if form.validate_on_submit(): 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password # set the user's password to the hashed password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in.', 'success')
        return redirect (url_for('users.login')) 
    return render_template('reset_token.html', title='Reset Password', form=form) 
# -----------------------------------------------------------------------------