from datetime import datetime
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

# NEW POST ROUTE -------------------------------------------------------------
@posts.route("/post/new", methods=['GET', 'POST'])
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
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend="New Post")
# ----------------------------------------------------------------------------

# POST/ID ROUTE --------------------------------------------------------------
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) # if the post doesn't exist, return 404, otherwise return the post
    return render_template('post.html', title=post.title, post=post)
# ----------------------------------------------------------------------------

# UPDATE POST ROUTE ----------------------------------------------------------
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id)) # redirect to the post page
    elif request.method == 'GET':
        # fill in form with the current post data
        form.title.data = post.title 
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', 
                           form=form, legend="Update Post")
# ----------------------------------------------------------------------------

# DELETE POST ROUTE ---------------------------------------------------------- 
@posts.route("/post/<int:post_id>/delete", methods=['POST']) # only allow post requests because we don't want users to be able to go to the url and delete posts
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) # if the post doesn't exist, return 404, otherwise return the post
    # first check if the author of the post is the current_user
    if post.author != current_user: 
        abort(403) # 403 is a HTTP response for a forbidden route
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home')) # redirect to the home page
# ----------------------------------------------------------------------------