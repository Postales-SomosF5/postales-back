from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, bcrypt
from app.models.user import Usuario

auth_bp = Blueprint('auth', __name__)  # nombre corregido

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data.get('email') or not data.get('contrasena'):
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({"error": "El usuario ya existe"}), 400

    nuevo_usuario = Usuario(
        nombre=data.get('nombre'),
        apellido=data.get('apellido'),
        email=data['email'],
        contrasena=generate_password_hash(data['contrasena']),
        rol_id=data.get('rol_id'),
        centro_id=data.get('centro_id'),
        sector_id=data.get('sector_id'),
        refuerzo_linguistico=data.get('refuerzo_linguistico'),
        penascal_rol=data.get('penascal_rol'),
        fecha_alta=data.get('fecha_alta'),
        fecha_baja=data.get('fecha_baja')
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data.get('email') or not data.get('contrasena'):
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    usuario = Usuario.query.filter_by(email=data['email']).first()

    if not usuario or not check_password_hash(usuario.contrasena, data['contrasena']):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Aquí luego se añadirá el JWT - Lo del TOKEN
    return jsonify({"mensaje": "Login exitoso", "usuario_id": usuario.id}), 200
