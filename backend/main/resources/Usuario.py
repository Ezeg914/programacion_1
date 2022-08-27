from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import jwt_required
from main.auth.decorators import admin_required



class Usuario(Resource):
    #@jwt_required()
    def get(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        return usuario.to_json()
    
    #@jwt_required()
    def delete(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204
    
    #@jwt_required()
    def put(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key, value)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json() , 201

class Usuarios(Resource):
    #@admin_required
    def get(self):
        page = 1
        per_page = 10
        
        usuarios = db.session.query(UsuarioModel)
        
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == "nombre":
                    nombre = nombre.filter(UsuarioModel.nombre.like("%"+ value +"%"))
                if key == "email":
                    email = email.filter(UsuarioModel.email.like("%"+ value +"%"))
                if key == "sort_by":
                    if value == "nombre":
                        nombre = nombre.order_by(UsuarioModel.nombre)
                    if value == "nombre[des]":
                        nombre = nombre.order_by(UsuarioModel.nombre.desc())
                    if value == "email":
                        email = email.order_by(UsuarioModel.email)
                    if value == "email[desc]":
                        email = email.order_by(UsuarioModel.email.desc())
        
        usuarios = usuarios.paginate(page, per_page, True, 30)
        return jsonify({
            "poemas" : [usuarios.to_json_short() for usuarios in usuarios.items],
            "total" : usuarios.total,
            "pages" : usuarios.pages,
            "page" : page
            
            })
    
    #@admin_required
    def post(self):
        usuario = UsuarioModel.from_json(request.get_json())
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201
