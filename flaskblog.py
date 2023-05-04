from flask import Flask
app = Flask(__name__)

@app.route("/") # test home page
def home(): 
    return "<h1>This is a home page!</h1>"

@app.route("/about")
def about():
    return "<h1> About Page</h1>"



if __name__ == '__main__':
    app.run(debug=True) # run via python [app.py]