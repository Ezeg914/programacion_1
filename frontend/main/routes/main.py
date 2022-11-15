
import requests
import json
from flask import Blueprint, render_template, make_response, request, redirect, url_for, current_app
from . import functions as f
# Create a Blueprint object
app = Blueprint('main', __name__, url_prefix='/')


@app.route('/')
def index():
    data = { "page": 1,"per_page" : 10 }

    headers = f.get_headers(without_token=False)

    response = requests.get(f'{current_app.config["API_URL"]}/poemas', json=data, headers=headers)
    print(response.status_code)
    print(response.text)

    #obtener poemas en json
    poemas = json.loads(response.text)
    print (poemas)

    return render_template('home.html', poemas=poemas["poemas"])
    

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email= request.form['email']
        password= request.form['password']
        print(email)
        print(password)
        

        data ={"email": email,"password": password}

        headers = f.get_headers(without_token=False)

        response = requests.post(f'{current_app.config["API_URL"]}/auth/login', json = data, headers = headers)
        if response.status_code == 200:

            print (response.status_code)
            print(response.text)

            response = json.loads(response.text)
            token = response["access_token"]
            usuario_id = str(response["id"])
            print (token)

            resp = make_response(redirect(url_for("main.index")))
            resp.set_cookie("access_token",token)
            resp.set_cookie("id", usuario_id)

            return resp
        else:
            return render_template("login.html")
    return render_template("login.html")
    

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for("main.index")))
    resp.delete_cookie("access_token")
    resp.delete_cookie("id")
    return resp


@app.route('/upload', methods=['GET','POST'])
def add_poem():
    if request.cookies.get('access_token'):
        if request.method == 'POST':
            titulo = request.form['titulo']
            body = request.form['body']
            print(titulo)
            print(body)
            id = f.get_id()
            print(id)
            data = {"titulo": titulo, "usuario_id": id,  "body": body}
            print(data)
            
            headers = f.get_headers(without_token=False)

            if titulo != "" and body != "":
                response = requests.post(f'{current_app.config["API_URL"]}/poemas', json=data, headers=headers)
                print(response)
        
                if response.ok:
                    response = f.json_load(response)
                    return redirect(url_for('main.poema_view', id=response["id"]))
                else:
                    return redirect(url_for('main.add_poem'))
            else:
                return redirect(url_for('main.add_poem'))
        else:
            #Mostrar template
            return render_template('upload.html', jwt=f.get_jwt())
    else:
        return redirect(url_for('main.login'))
    




@app.route('/usuario')
def usuario():
    if request.cookies.get('access_token'):
        usuario = f.get_user(request.cookies.get('id'))
        usuario = json.loads(usuario.text)
        print(usuario)
        poemas = f.get_poemas_by_id(request.cookies.get('id'))
        print(poemas.text)
        poemas = json.loads(poemas.text)
  

        return render_template('perfil.html', usuario=usuario, poemas=poemas["poemas"])
    else:
        return redirect(url_for('main.login'))





@app.route('/delete/poema/<id>')
def delete_poema(id):
    if request.cookies.get('access_token'):
        
        f.delete_poema(id=id)
        return redirect(url_for('main.usuario'))
    else:
        return redirect(url_for('main.login'))

@app.route('/delete/calificacion/<id>')
def delete_calificacion(id):
    if request.cookies.get('access_token'):
        print(id)
        f.delete_comentario(id=id)
        return redirect(url_for('main.index'))
    else:
        return redirect(url_for('main.login'))


@app.route('/usuario/<int:id>')
def profile(id):
    if request.cookies.get('access_token'):
        usuario = f.get_user(id)
        print(usuario.text)
        usuario = json.loads(usuario.text)
        print(usuario)

        return render_template('perfil.html', usuario=usuario)
        
    else:
        return redirect(url_for('main.login'))

@app.route('/calificaciones/<int:id>', methods=['GET','POST'])
def cargar_calificaciones(id):
    if request.cookies.get('access_token'):
        if request.method == 'POST':
            puntaje = request.form['puntaje']
            comentario = request.form['comentario']
            print(puntaje)
            print(comentario)
            usuario_id = f.get_id()
            print(id)
            data = {"puntaje": puntaje, "usuario_id": usuario_id,  "comentario": comentario, "poema_id": id}
            print(data)
            
            headers = f.get_headers(without_token=False)
            if comentario != "" and puntaje != "":
                response = requests.post(f'{current_app.config["API_URL"]}/calificaciones', json=data, headers=headers)
                print(response)
        
                response = f.json_load(response)
                return redirect(url_for('main.poema_view', id=id))
            else:
                return redirect(url_for('main.poema_view'))






@app.route('/poema')
def add_poema():
    return render_template('poema.html')







@app.route('/poema/<int:id>')
def poema_view(id):
    if request.cookies.get('access_token'):
        poema = f.get_poema(id)
        print(poema.text)
        poema = json.loads(poema.text)
        calificacion = f.get_calificaciones_by_poema_id(id)
        print(calificacion.text)
        calificacion = json.loads(calificacion.text)
        
        #Mostrar template
        return render_template('poema.html', poema = poema, calificacion = calificacion["calificaciones"])
    
    else:
        return redirect(url_for('main.login'))

