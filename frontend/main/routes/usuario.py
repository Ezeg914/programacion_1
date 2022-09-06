from flask import Blueprint, render_template,request

# Create a Blueprint object
author = Blueprint('user', __name__, url_prefix='/usuario')

users = [
    {"id":0 , 'nombre': 'usuario 1', 'email': 'ezeg914@gmail.com'},
]

@author.route('/')
def index():
    return render_template('')

# Create a route for the home page
@author.route('/usuario/<int:id>')
def profile(id=0):
    return render_template('', usuario=usuarios[id])