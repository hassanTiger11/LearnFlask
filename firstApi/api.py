from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
@app.route("/<value>")
def hello_world(value = None):
    return render_template('index.html', value = value)

