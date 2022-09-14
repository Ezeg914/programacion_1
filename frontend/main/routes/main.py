
from flask import Blueprint, render_template
# Create a Blueprint object
app = Blueprint('main', __name__, url_prefix='/')


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/upload_poema')
def add_poem():
    return render_template('upload poema.html')

