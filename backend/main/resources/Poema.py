from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemaModel
from datetime import *
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required

class Poema(Resource):
     @jwt_required
     def get(self, id):
         poema = db.session.query(PoemaModel).get_or_404(id)
         return poema.to_json()
     @jwt_required
     def delete(self, id):
         poema = db.session.query(PoemaModel).get_or_404(id)
         db.session.delete(poema)
         db.session.commit()
         return '', 204
     @jwt_required
     def put(self, id):
         poema = db.session.query(PoemaModel).get_or_404(id)
         data = request.get_json().items()
         for key, value in data:
             setattr(poema, key, value)
         db.session.add(poema)
         db.session.commit()
         return poema.to_json() , 201

class Poemas(Resource):
     @jwt_required
     def get(self):
          page = 1
          
          per_page = 10
          
          poemas = db.session.query(PoemaModel)
          if request.get_json():
               filters = request.get_json().items()
               for key, value in filters:
                    if key == "page":
                         page = int(value)
                    if key == "per_page":
                         per_page = int(value)
                    if key == "titulo":
                         poemas = poemas.filter(PoemaModel.titulo.like("%"+value+"%"))
                    if key == "usuario":
                         poemas = poemas.filter(PoemaModel.usuario == value)
                    if key == "created[gt]":
                         poemas = poemas.filter(PoemaModel.date >= datetime.strptime(value, '%d-%m-%Y'))
                    if key == "created[lt]":
                         poemas = poemas.filter(PoemaModel.date <= datetime.strptime(value, '%d-%m-%Y'))                    
                    if key == "sort_by":
                         if value == "calificaciones":
                              poemas = poemas.outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).order_by(func.avg(PoemaModel.score))
                         if value == "calificaciones[desc]":
                              poemas = poemas.outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).order_by(func.avg(PoemaModel.score).desc())
                         if value == "usuario":
                              poemas = poemas.order_by(PoemaModel.usuario)
                         if value == "usuario[desc]":
                              poemas = poemas.order_by(PoemaModel.usuario.desc())
                         if value == "date":
                              poemas = poemas.order_by(PoemaModel.date)
                         if value == "date[desc]":
                              poemas = poemas.order_by(PoemaModel.date.desc())
                    
                    
          poemas = poemas.paginate(page, per_page, False, 30)
          return jsonify({
               "poemas" : [poema.to_json_short() for poema in poemas.items],
               "total" : poemas.total,
               "pages" : poemas.pages,
               "page" : page
               
               })

     

         #poemas = db.session.query(PoemaModel).all()
         #return jsonify([poema.to_json() for poema in poemas])

     @jwt_required
     def post(self):
         poema = PoemaModel.from_json(request.get_json())
         db.session.add(poema)
         db.session.commit()
         return poema.to_json(), 201
