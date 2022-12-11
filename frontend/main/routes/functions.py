from flask import request, current_app, redirect, url_for
import requests, json

#--------------- Poems -----------------#

#Obtengo los poemas del poeta ayudandome del id del mismo.
def get_poemas_by_id(id, page = 1, perpage = 10):
    api_url = f'{current_app.config["API_URL"]}/poemas'
    # Envio de la pagina y cuantos datos por pagina.
    data = {"page": page, "perpage": perpage, "usuario_id": id}
    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    headers = get_headers(without_token = True)
    # Creamos el response y le enviamos el data y headers.
    return requests.get(api_url, json = data, headers = headers)


#Obtengo un poema en especifico.
def get_poema(id):
    api_url = f'{current_app.config["API_URL"]}/poema/{id}'
    headers = get_headers()
    return requests.get(api_url, headers=headers)


#Obtengo todos los poemas de la base de datos.
def get_poemas(api_url, page=1, perpage=3):
    api_url = f'{current_app.config["API_URL"]}/poemas'
    data = {"page": page, "perpage": perpage}
    headers = get_headers()
    return requests.get(api_url, json=data, headers=headers)

def delete_poema(id):
    api_url = f'{current_app.config["API_URL"]}/poema/{id}'
    headers = get_headers()
    return requests.delete(api_url, headers=headers)

def edit_poema(id, data):
    api_url = f'{current_app.config["API_URL"]}/poema/{id}'
    headers = get_headers()
    return requests.put(api_url, json = data, headers = headers)
#--------------- Poems -----------------#


#--------------- User -----------------#

#Obtengo los datos del usuario.
def get_user_info(id):
    api_url = f'{current_app.config["API_URL"]}/usuario/{id}'
    #Obtengo el jwt del logue e instancio el header y le agrego el jwt.
    headers = get_headers()

    #Creamos el response y le enviamos el data y headers
    return requests.get(api_url, headers=headers)


#Obtener un usuario en especifico.
def get_user(id):
    api_url = f'{current_app.config["API_URL"]}/usuario/{id}'
    headers = get_headers()
    return requests.get(api_url, headers=headers)


#Obtengo el nombre del usuario
def get_username(usuario_id):
    headers = get_headers()
    api_url = f'{current_app.config["API_URL"]}/usuario/{usuario_id}'
    response = requests.get(api_url, headers=headers)
    user = json.loads(response.text)
    return user["name"]

def delete_user(id):
    api_url = f'{current_app.config["API_URL"]}/usuario/{id}'
    headers = get_headers()
    return requests.delete(api_url, headers=headers)

#--------------- User -----------------#


#--------------- Calificaciones -----------------#

#Obtener las calificaciones de un poema en especifico.
def get_calificaciones_by_poema_id(id):
    api_url = f'{current_app.config["API_URL"]}/calificaciones'

    data = {"poema_id": id}
    headers = get_headers()
    return requests.get(api_url, json = data, headers = headers)

def get_calificacion(id):
    api_url = f'{current_app.config["API_URL"]}/calificacion/{id}'
    headers = get_headers()
    return requests.get(api_url, headers=headers)
#Esliminar calificacion
def delete_comentario(id):
    api_url = f'{current_app.config["API_URL"]}/calificacion/{id}'
    headers = get_headers()
    return requests.delete(api_url, headers=headers)

def edit_calificacion(id, data):
    api_url = f'{current_app.config["API_URL"]}/calificacion/{id}'
    headers = get_headers()
    return requests.put(api_url, json = data, headers = headers)

#--------------- Calificaciones -----------------#


#--------------- Utilidades -----------------#

#Obtengo el json txt.
def json_load(response):
    return json.loads(response.text)


#Obtengo el email del usuario
def get_headers(without_token = False):
    jwt = get_jwt()
    if jwt and without_token == False:
        return {"Content-Type" : "application/json", "Authorization": f"Bearer {jwt}"}
    else:
        return {"Content-Type" : "application/json"}


#Obtener el token desde response.
def get_jwt():
    return request.cookies.get("access_token")


#Obtener el id desde response.
def get_id():
    return request.cookies.get("id")


#Hacer redirect

def redirect_to(url):
    return redirect(url_for(url))
#--------------- Utilidades -----------------#