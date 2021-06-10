from flask import *
'''
In this module I will study 
flask requests
'''
app = Flask(__name__)
'''
By default GET methods are always allowed
to allow POST we need to ass method parameter
to the route'''
@app.route("/")
def hell():
    return template_rendered("index.html", None)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

