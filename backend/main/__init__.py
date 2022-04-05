import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
import main.resources as resources
api = Api()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    api.add_resource(resources.PoemasResource, '/poemas')
    api.add_resource(resources.PoemaResource, '/poema/<id>')
    api.add_resource(resources.CalificacionesResource, '/calificaciones')
    api.add_resource(resources.CalificacionResource, '/calificacion/<id>')
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuarioResource, '/usuario/<id>')
    api.init_app(app)
    return app