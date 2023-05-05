from flask import Flask, render_template


app = Flask(__name__)

@app.route('/') # default
@app.route('/home') # also home, two routes are handled by the same function below
def home(): 
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True) # run via python [app.py]