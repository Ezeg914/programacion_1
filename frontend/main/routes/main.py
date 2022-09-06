
from flask import Blueprint, render_template, url_for
from main.routes import usuario, poema
# Create a Blueprint object
app = Blueprint('main', __name__, url_prefix='/')

# Create a route for the home page
@app.route('/')
def index():
    return render_template('')

@app.route('/add_poema')
def add_poem():
    return render_template('')

@app.route('/login')
def login():
    return render_template('')