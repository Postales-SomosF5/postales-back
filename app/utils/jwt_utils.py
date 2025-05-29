from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except NoAuthorizationError:
            return jsonify({"mensaje": "Token faltante"}), 401
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['rol'] not in [2, 1]:
                return jsonify({'mensaje': 'Acceso denegado: se requiere rol de administrador'}), 403
            return f(*args, **kwargs)
        except NoAuthorizationError:
            return jsonify({"mensaje": "Token faltante"}), 401
    return decorated_function

def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['rol'] != 1:
                return jsonify({'mensaje': 'Acceso denegado: se requiere rol de super administrador'}), 403
            return f(*args, **kwargs)
        except NoAuthorizationError:
            return jsonify({"mensaje": "Token faltante"}), 401
    return decorated_function