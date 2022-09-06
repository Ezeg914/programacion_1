from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CalificacionModel
from flask_jwt_extended import jwt_required
from main.auth.decorators import admin_required


class Calificacion(Resource):
    @jwt_required()
    def get(self, id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        return calificacion.to_json()
    
    @admin_required
    @jwt_required()
    def delete(self, id):
         calificacion = db.session.query(CalificacionModel).get_or_404(id)
         db.session.delete(calificacion)
         db.session.commit()
         return '', 204
    @jwt_required()
    def put(self, id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(calificacion, key, value)
        db.session.add(calificacion)
        db.session.commit()
        return calificacion.to_json() , 201

class Calificaciones(Resource):
    @jwt_required()
    def get(self):
        page = 1
        per_page = 10
        Calificaciones = db.session.query(CalificacionModel)
        
        
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == "page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)
                if key == "calificacion":
                    calificacion = calificacion.filter(CalificacionModel.calificacion == value)
                if key == "comentario":
                    comentario = comentario.filter(CalificacionModel.comentario.like("%" + value + "%"))
                if key == "usuario":
                    usuario_id = usuario_id.filter(CalificacionModel.usuario_id == value)
                if key == "poema":
                    poema_id = poema_id.filter(CalificacionModel.poema_id == value)                
                if key == "sort_by":
                    if value == "calificacion":
                        calificacion = calificacion.order_by(CalificacionModel.calificacion)
                    if value == "calificacion[desc]":
                        calificacion = calificacion.order_by(CalificacionModel.calificacion.desc())
                    if value == "usuario":
                        usuario = usuario.order_by(CalificacionModel.usuario_id)
                    if value == "usuario[des]":
                        usuario = usuario.order_by(CalificacionModel.usuario_id.desc())
                    if value == "poema":
                        poema = poema.order_by(CalificacionModel.poema_id)
                    if value == "poema[des]":
                        poema = poema.order_by(CalificacionModel.poema_id.desc())
                        
                
        Calificaciones = Calificaciones.paginate(page, per_page, True, 30)
        return jsonify({
            "calificaciones" : [calificaciones.to_json() for calificaciones in Calificaciones.items],
            "total" : Calificaciones.total,
            "pages" : Calificaciones.pages,
            "page" : page
            
            })

    @jwt_required()
    def post(self):
        calificacion = CalificacionModel.from_json(request.get_json())
        db.session.add(calificacion)
        db.session.commit()
        return calificacion.to_json(), 201
