from flask import Flask
app = Flask(__name__)

@app.route("/") # root page of the website
def hello(): 
    return "<h1>Hello World!</h1>"

@app.route("/home") # test home page
def home(): 
    return "<h1>This is a home page!</h1>"




if __name__ == '__main__':
    app.run(debug=True) # run via python [app.py]