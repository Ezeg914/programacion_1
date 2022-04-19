from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemaModel


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
         poemas = db.session.query(PoemaModel).all()
         return jsonify([poema.to_json() for poema in poemas])


    def post(self):
         poema = PoemaModel.from_json(request.get_json())
         db.session.add(poema)
         db.session.commit()
         return poema.to_json(), 201
