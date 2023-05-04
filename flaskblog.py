from flask import Flask
app = Flask(__name__)

@app.route("/") # root page of the website
def hello(): 
    return "Hello World!"

@app.route("/home") # test home page
def home(): 
    return "This is a home page!"
