from .. import db
from sqlalchemy.sql import func
import datetime
import statistics


class Poema(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100), nullable = False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    body = db.Column(db.String(100), nullable = False)
    date = db.Column(db.DateTime,nullable = False, default=datetime.datetime.now())
    
    usuario = db.relationship('Usuario',back_populates="poema",uselist=False,single_parent=True)
    calificacion = db.relationship('Calificacion',back_populates="poema",cascade = "all, delete-orphan")

    
    
    def __repr__(self):
        return '<poema: %r %r %r %r >' % (self.titulo, self.usuario_id, self.body, self.date)    

    def poema_puntaje(self):
        calificacion_poema = []
        if len(self.calificacion) == 0:
            mean = 0
            
        else:
            for calificacion in self.calificacion:
                puntaje = calificacion.puntaje
                calificacion_poema.append(puntaje)
            return statistics.mean(calificacion_poema)

    
    def to_json(self):
        poema_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'usuario_id': self.usuario.to_json(),
            'body': str(self.body),
            'date': str(self.date.strftime("%d-%m-%Y")),
            'calificacion': [calificacion.to_json_short() for calificacion in self.calificacion],
            'puntaje': self.poema_puntaje()
        
        }
        return poema_json

    
    def to_json_short(self):
        poema_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'body': str(self.body),
        }
        return poema_json
    
    @staticmethod
    def from_json(poema_json):
        id = poema_json.get('id')
        titulo = poema_json.get('titulo')
        usuario_id = poema_json.get('usuario_id')
        body = poema_json.get('body')
        return Poema(id=id,
                    titulo=titulo,
                    usuario_id=usuario_id,
                    body=body,
                    )