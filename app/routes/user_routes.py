# app/routes/user_routes.py
from app.utils.jwt_utils import login_required, admin_required, super_admin_required
from flask import Blueprint, request, jsonify
from app.models.user import Usuario
from app.extensions import db

user_bp = Blueprint('user', __name__)

# GET /api/users - Obtener todos los usuarios
@user_bp.route('/', methods=['GET'])
@super_admin_required
def get_users():
    usuarios = Usuario.query.all()
    resultado = [usuario.to_dict() for usuario in usuarios]
    return jsonify(resultado), 200

# GET /api/users/<id> - Obtener un usuario por ID
@user_bp.route('/<int:user_id>', methods=['GET'])
@super_admin_required
def get_user(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario.to_dict()), 200

# POST /api/users - Crear un nuevo usuario
@user_bp.route('/', methods=['POST'])
@admin_required
def create_user():
    data = request.get_json()
    if not data.get('email') or not data.get('contrasena'):
        return jsonify({"error": "Email y contraseña obligatorios"}), 400

    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Usuario ya existe"}), 400

    nuevo_usuario = Usuario(
        nombre=data.get('nombre'),
        apellido=data.get('apellido'),
        email=data['email'],
        rol_id=data.get('rol_id'),
        centro_id=data.get('centro_id'),
        sector_id=data.get('sector_id'),
        refuerzo_linguistico=data.get('refuerzo_linguistico'),
        penascal_rol=data.get('penascal_rol'),
        fecha_alta=data.get('fecha_alta'),
        fecha_baja=data.get('fecha_baja')
    )

    nuevo_usuario.set_password(data['contrasena'])

    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify(nuevo_usuario.to_dict()), 201

# PUT /api/users/<id> - Actualizar un usuario existente
@user_bp.route('/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json()
    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.apellido = data.get('apellido', usuario.apellido)
    usuario.email = data.get('email', usuario.email)
    if 'contrasena' in data and data['contrasena']:
        usuario.set_password(data['contrasena'])
    usuario.rol_id = data.get('rol_id', usuario.rol_id)
    usuario.centro_id = data.get('centro_id', usuario.centro_id)
    usuario.sector_id = data.get('sector_id', usuario.sector_id)
    usuario.refuerzo_linguistico = data.get('refuerzo_linguistico', usuario.refuerzo_linguistico)
    usuario.penascal_rol = data.get('penascal_rol', usuario.penascal_rol)
    usuario.fecha_alta = data.get('fecha_alta', usuario.fecha_alta)
    usuario.fecha_baja = data.get('fecha_baja', usuario.fecha_baja)

    db.session.commit()
    return jsonify(usuario.to_dict()), 200

# DELETE /api/users/<id> - Eliminar un usuario
@user_bp.route('/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200

@user_bp.route('/borrar_todo', methods=['DELETE'])
@super_admin_required
def borrar_todo():
    usuarios_a_eliminar = Usuario.query.filter(Usuario.rol_id == 3).all()

    if not usuarios_a_eliminar:
        return jsonify({"mensaje": "No hay usuarios para eliminar"}), 200

    for usuario in usuarios_a_eliminar:
        db.session.delete(usuario)

    db.session.commit()
    return jsonify({"mensaje": "Usuarios eliminados, excepto el Super Admin"}), 200
