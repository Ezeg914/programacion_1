from flask import request, jsonify, Blueprint
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import create_access_token

# Blueprint para acceder a los métodos de autenticación
auth = Blueprint('auth', __name__, url_prefix='/auth')


# Método de logueo
@auth.route('/login', methods=['POST'])
def login():
    # Busca al usuario en la db por mail
    usuario = db.session.query(UsuarioModel).filter(
        UsuarioModel.email == request.get_json().get("email")).first_or_404()

    # Valida la contraseña
    p = request.get_json().get("password")
    print(f'Debug: {p}. Type: {type(p)}')
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
