from .. import db


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    rol = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    
    poema = db.relationship("Poema", back_populates="usuario",cascade="all, delete-orphan")
    calificacion = db.relationship("Calificacion", back_populates="usuario",cascade="all, delete-orphan")

    def __repr__(self):
        return '<usuario: %r %r %r %r >' % (self.nombre, self.password, self.rol, self.email)    

    
    def to_json(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'password': str(self.password),
            'rol': str(self.rol),
            'email': str(self.email)
        }
        return usuario_json
    
    
    def to_json_short(self):
        usuario_json = {
            'id': self.id,
            'email': str(self.email)
        }
    
    @staticmethod
    def from_json(usuario_json):
        id = usuario_json.get('id')
        nombre = usuario_json.get('nombre')
        password = usuario_json.get('password')
        rol = usuario_json.get('rol')
        email = usuario_json.get('email')
        return Usuario(id=id,
                    nombre=nombre,
                    password=password,
                    rol=rol,
                    email=email
                    )