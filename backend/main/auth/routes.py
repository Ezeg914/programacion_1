from flask import request, jsonify, Blueprint
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import create_access_token
from main.mail.functions import sendMail

# Blueprint para acceder a los métodos de autenticación
auth = Blueprint('auth', __name__, url_prefix='/auth')


# Método de logueo
@auth.route('/login', methods=['POST'])
def login():
    # Busca al usuario en la db por mail
    usuario = db.session.query(UsuarioModel).filter(
        UsuarioModel.email == request.get_json().get("email")).first_or_404()

    # Valida la contraseña
    
    
    if usuario.check_password(request.get_json().get("password")):
        # Genera un nuevo token
        # Pasa el objeto usuario como identidad
        access_token = create_access_token(identity=usuario)
        # Devolver valores y token
        data = {
            'id': str(usuario.id),
            'email': usuario.email,
            'access_token': access_token
        }

        return data, 200
    else:
        return 'Incorrect password ', 401

@auth.route('/register', methods=['POST'])
def register():
    usuario = UsuarioModel.from_json(request.get_json())
    #Verificar si el mail ya existe en la db
    exists = db.session.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).scalar() is not None
    if exists:
        return 'Duplicated mail', 409
    else:
        try:
            #Agregar usuario a DB
            db.session.add(usuario)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return str(error), 409
        return usuario.to_json(), 201