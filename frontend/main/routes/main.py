
import requests
import json
from flask import Blueprint, render_template, make_response, request, redirect, url_for
# Create a Blueprint object
app = Blueprint('main', __name__, url_prefix='/')


@app.route('/')
def index():
    #if request.cookies.get('acces_token'):

    api_url = "http://127.0.0.1:8500/poemas"

    data = { "page": 1,"per_page" : 10 }
    #jwt = request.cookies.get("acces_token")

    headers = {"Content-Type" : "application/json"}
    #, "Authorization":"Bearer {}".format(jwt)
    #print (jwt)

    response = requests.get(api_url, json=data, headers=headers)
    print(response.status_code)
    print(response.text)

    #obtener poemas en json
    poemas = json.loads(response.text)
    print (poemas)

    return render_template('home.html', poemas=poemas["poemas"])
    #else:
        #return redirect(url_for('main.login'))

#@app.route('/login', methods=['GET','POST'])
#def login():
    #if request.method == 'POST':

        #api_url = "http://127.0.0.1:8500/auth/login"

        #data ={"email": "lauti@gmail.com","password": "12345d"}
        #email= request.form['email']
        #password= request.form['password']
        #print(email)
        #print(password)
        #print(request)
        #headers = {"Content-Type" : "application/json"}

        #response = requests.post(api_url, json = data, headers = headers)
        #print (response.status_code)
        #print(response.text)

        #token = json.loads(response.text)
        #token = token["access_token"]
        #print (token)

        #resp = make_response(render_template("login.html"))
        #resp.set_cookie("acces_token",token)

        #return resp
        #return render_template("login.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email= request.form['email']
        password= request.form['password']
        print(email)
        print(password)
        api_url = "http://127.0.0.1:8500/auth/login"

        data ={"email": email,"password": password}

        headers = {"Content-Type" : "application/json"}

        response = requests.post(api_url, json = data, headers = headers)
        if response.status_code == 200:

            print (response.status_code)
            print(response.text)

            token = json.loads(response.text)
            token = token["access_token"]
            print (token)

            resp = make_response(redirect(url_for("main.index")))
            resp.set_cookie("acces_token",token)
            return resp
        else:
            return render_template("login.html")
    return render_template("login.html")
    
    


@app.route('/upload_poema')
def add_poem():
    return render_template('upload_poema.html')

@app.route('/usuario')
def usuario():
    if request.cookies.get('acces_token'):

        return render_template('perfil.html')

    else:
        return redirect(url_for('main.login'))

@app.route('/usuario/<int:id>')
def profile(id):
    
    return render_template('perfil.html')

@app.route('/poema')
def add_poema():
    return render_template('poema.html')

@app.route('/poema/<int:id>')
def poema_view(id):
    return render_template('poema.html')
