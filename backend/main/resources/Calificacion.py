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
        calificaciones = db.session.query(CalificacionModel)
        
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == "page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)
                if key == "calificacion":
                    calificaciones = calificaciones.filter(CalificacionModel.calificacion == value)
                if key == "comentario":
                    calificaciones = calificaciones.filter(CalificacionModel.comentario.like("%" + value + "%"))
                if key == "usuario":
                    calificaciones = calificaciones.filter(CalificacionModel.usuario_id == value)
                if key == "poema_id":
                    calificaciones = calificaciones.filter(CalificacionModel.poema_id == value)                
      
                        
                
        calificaciones = calificaciones.paginate(page, per_page, True, 30)
        return jsonify({
            "calificaciones" : [calificacion.to_json() for calificacion in calificaciones.items],
            "total" : calificaciones.total,
            "pages" : calificaciones.pages,
            "page" : page
            
            })

    @jwt_required()
    def post(self):
        calificacion = CalificacionModel.from_json(request.get_json())
        db.session.add(calificacion)
        db.session.commit()
        return calificacion.to_json(), 201
