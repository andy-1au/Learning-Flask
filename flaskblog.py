from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'c30cdec540796525fe21a63113d6b863' # Protect against attacks, modifying cookies, cross-site attacks

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
    app.run(debug=True) # run via python [app.py]