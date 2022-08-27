from .. import db


class Calificacion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    puntaje = db.Column(db.Integer, nullable = False)
    comentario = db.Column(db.String(100), nullable = False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    poema_id = db.Column(db.Integer,  db.ForeignKey('poema.id'), nullable = False)
    
    usuario = db.relationship('Usuario',back_populates="calificacion",uselist=False,single_parent=True)
    poema = db.relationship('Poema',back_populates="calificacion",uselist=False,single_parent=True)


    
    def __repr__(self):
        return '<calificacion: %r %r %r %r >' % (self.puntaje, self.comentario, self.usuario_id, self.poema_id)    

    
    def to_json(self):
        calificacion_json = {
            'id': self.id,
            'puntaje': int(self.puntaje),
            'comentario': str(self.comentario),
            'usuario_id': self.usuario.to_json(),
            'poema_id': self.poema.to_json_short()
        }
        return calificacion_json
    
    def to_json_short(self):
        calificacion_json = {
            'id': self.id,
            'puntaje': int(self.puntaje),
            'comentario': str(self.comentario),
            'usuario_id': self.usuario.to_json(),
            'poema_id': self.poema.to_json_short()
        }
        return calificacion_json

    
    @staticmethod
    def from_json(calificacion_json):
        id = calificacion_json.get('id')
        puntaje = calificacion_json.get('puntaje')
        comentario = calificacion_json.get('comentario')
        usuario_id = calificacion_json.get('usuario_id')
        poema_id = calificacion_json.get('poema_id')
        return Calificacion(id=id,
                    puntaje=puntaje,
                    comentario=comentario,
                    usuario_id=usuario_id,
                    poema_id=poema_id
                    )