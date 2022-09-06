from flask import Blueprint, render_template

# Create a Blueprint object
poema = Blueprint('poema', __name__, url_prefix='/poema')

poemas = [{"id":0 , 'title': 'Poem 1', 'body': 'body del peoma 1'}]

@poema.route('/')
def index():
    return render_template('')


# Create a route for the home page
@poema.route('/poem/<int:id>')
def poem_view(id):
    return render_template('poem_view.html', poem=poems[id])