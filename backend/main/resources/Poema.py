from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemaModel
from datetime import *
from sqlalchemy import func
from flask_jwt_extended import jwt_required,  get_jwt_identity, get_jwt, verify_jwt_in_request
from main.auth.decorators import admin_required




class Poema(Resource):
     @jwt_required()
     def get(self, id):
         poema = db.session.query(PoemaModel).get_or_404(id)
         identity = get_jwt_identity()
         if identity:
            return poema.to_json()
         else:
            return poema.to_json_short()

     @jwt_required()
     def delete(self, id):
          poema = db.session.query(PoemaModel).get_or_404(id)
          identity = get_jwt_identity()
        
          jwt_data = get_jwt()

          if jwt_data['rol'] == 'admin' or poema.usuario_id == identity:
               db.session.delete(poema)
               db.session.commit()
               return '', 204
          else:
               return 'not permissions'

         
     @jwt_required()
     def put(self, id):
         poema = db.session.query(PoemaModel).get_or_404(id)
         data = request.get_json().items()
         for key, value in data:
             setattr(poema, key, value)
         db.session.add(poema)
         db.session.commit()
         return poema.to_json() , 201

class Poemas(Resource):
     def get(self):
          page = 1
          
          per_page = 10
          
          poemas = db.session.query(PoemaModel)
          #identity = get_jwt_identity()

          if request.get_json():
               filters = request.get_json().items()
               #if identity:
               poemas = db.session.query(PoemaModel).order_by(PoemaModel.date.desc())
               for key, value in filters:
                    if key == "page":
                         page = int(value)
                    if key == "per_page":
                         per_page = int(value)
                    if key == "titulo":
                         poemas = poemas.filter(PoemaModel.titulo.like("%"+value+"%"))
                    if key == "usuario_id":
                         poemas = poemas.filter(PoemaModel.usuario_id == value)
                    if key == "created[gt]":
                         poemas = poemas.filter(PoemaModel.date >= datetime.strptime(value, '%d-%m-%Y'))
                    if key == "created[lt]":
                         poemas = poemas.filter(PoemaModel.date <= datetime.strptime(value, '%d-%m-%Y'))                    
                    
                    
          poemas = poemas.paginate(page, per_page, False, 30)
          return jsonify({
               "poemas" : [poema.to_json() for poema in poemas.items],
               "total" : poemas.total,
               "pages" : poemas.pages,
               "page" : page
               
               })

     

         #poemas = db.session.query(PoemaModel).all()
         #return jsonify([poema.to_json() for poema in poemas])

     @jwt_required()
     def post(self):
          poema = PoemaModel.from_json(request.get_json())
          identity = get_jwt_identity()
          if identity:
               db.session.add(poema)
               db.session.commit()
               return poema.to_json(), 201
