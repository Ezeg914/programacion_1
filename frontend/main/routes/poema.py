from flask import Blueprint, render_template


poema = Blueprint('poema', __name__, url_prefix='/poema')

@poema.route('/')
def index():
    return render_template('poema.html')


@poema.route('/poema/<int:id>')
def poem_view(id):
    return render_template('poema.html')