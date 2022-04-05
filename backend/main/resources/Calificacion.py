from flask_restful import Resource
from flask import request


CALIFICACION = {
    1: {'stars': '5 stars', 'calificacion':'ta bueno'},
    2: {'stars': '3 stars',  'calificacion':'neeee hay mejores'},
}


class Calificacion(Resource):
    def get(self, id):
        if int(id) in CALIFICACION:
            return CALIFICACION[int(id)]
        return '', 404

    def delete(self, id):
        if int(id) in CALIFICACION:
            del CALIFICACION[int(id)]
            return '', 204
        return '', 404
    
    def put(self, id):
        if int(id) in CALIFICACION:
            calificacion = CALIFICACION[int(id)]
            data = request.get_json()
            calificacion.update(data)
            return calificacion, 201
        return '', 404

class Calificaciones(Resource):
    def get(self):
        return CALIFICACION
   
    def post(self):
        calificacion = request.get_json()
        id = int(max(CALIFICACION.keys())) + 1
        CALIFICACION[id] = calificacion
        return CALIFICACION[id], 201
