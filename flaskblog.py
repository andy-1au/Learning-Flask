from flask import Flask
app = Flask(__name__)

@app.route("/") # default
@app.route("/home") # also home, two routes are handled by the same function below
def home(): 
    return "<h1>This is a home page!</h1>"

@app.route("/about")
def about():
    return "<h1> About Page</h1>"



if __name__ == '__main__':
    app.run(debug=True) # run via python [app.py]