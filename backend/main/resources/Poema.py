from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemaModel
from datetime import *
from sqlalchemy import func

class Poema(Resource):
    def get(self, id):
         poema = db.session.query(PoemaModel).get_or_404(id)
         return poema.to_json()

    def delete(self, id):
         poema = db.session.query(PoemaModel).get_or_404(id)
         db.session.delete(poema)
         db.session.commit()
         return '', 204
    
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
                         if value == "qualifications":
                              poemas = poemas.outerjoin(PoemaModel.qualifications).group_by(PoemaModel.id).order_by(func.avg(PoemaModel.score))
                         if value == "qualifications[desc]":
                              poemas = poemas.outerjoin(PoemaModel.qualifications).group_by(PoemaModel.id).order_by(func.avg(PoemaModel.score).desc())
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


    def post(self):
         poema = PoemaModel.from_json(request.get_json())
         db.session.add(poema)
         db.session.commit()
         return poema.to_json(), 201
