from flask import render_template, url_for, redirect, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)

# DEFAULT TO HOME ROUTE -------------------------------------------------------
@main.route('/')
def redirect_to_home():
    return redirect(url_for('main.home'))
# ----------------------------------------------------------------------------

# HOME ROUTE -----------------------------------------------------------------
@main.route('/home') # also home, two routes are handled by the same function below
def home(): 
    page = request.args.get('page', 1, type=int) # get the page number from the url, default to 1, and type is int
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # 5 posts per page, ordered by most recent data
    # posts = Post.query.order_by(Post.date_posted.desc()).all() # Query all posts from db in descending order by date_posted
    return render_template('home.html', posts=posts)
# ----------------------------------------------------------------------------

# ABOUT ROUTE ----------------------------------------------------------------
@main.route("/about")
def about():
    return render_template('about.html', title='About')
# ----------------------------------------------------------------------------