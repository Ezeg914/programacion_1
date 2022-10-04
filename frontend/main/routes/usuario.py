from flask import Blueprint, render_template,request


author = Blueprint('user', __name__, url_prefix='/usuario')

@author.route('/')
def index():
    return render_template('perfil.html')


@author.route('/usuario/<int:id>')
def profile(id):
    return render_template('perfil.html')