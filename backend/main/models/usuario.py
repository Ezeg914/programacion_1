from .. import db
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(100), nullable=False, default="usuario")
    email = db.Column(db.String(100), nullable=False)

    poema = db.relationship("Poema", back_populates="usuario", cascade="all, delete-orphan")
    calificacion = db.relationship("Calificacion", back_populates="usuario", cascade="all, delete-orphan")

    @property
    def plain_password(self):
        raise AttributeError('Password cant be read')

    @plain_password.setter
    def plain_password(self, secret):
        self.password = generate_password_hash(secret)

    # Método que compara una contraseña en texto plano con el hash guardado en la db
    def check_password(self, secret):
        return check_password_hash(str(self.password), str(secret))

    def __repr__(self):
        return '<usuario: %r %r %r %r >' % (self.nombre, self.password, self.rol, self.email)

    def to_json(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            # 'password': str(self.password),
            'rol': str(self.rol),
            'email': str(self.email)
        }
        return usuario_json

    def to_json_short(self):
        usuario_json = {
            'id': self.id,
            'nombre': self.nombre,
            'email': str(self.email),
            'password': str(self.password),
        }
        return usuario_json

    @staticmethod
    def from_json(usuario_json):
        id = usuario_json.get('id')
        nombre = usuario_json.get('nombre')
        password = usuario_json.get('password')
        rol = usuario_json.get('rol')
        email = usuario_json.get('email')
        return Usuario(id=id,
                       nombre=nombre,
                       plain_password=password,
                       rol=rol,
                       email=email
                       )
