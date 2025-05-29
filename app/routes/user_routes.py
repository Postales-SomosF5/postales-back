# app/routes/user_routes.py
from app.utils.jwt_utils import login_required, admin_required, super_admin_required
from flask import Blueprint, request, jsonify
from app.models.user import Usuario
# from app.models.rol import Rol
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

# GET /api/usuarios - Obtener todos los usuarios
@user_bp.route('/', methods=['GET'])
@super_admin_required
def get_users():
    usuarios = Usuario.query.all()
    resultado = [usuario.to_dict() for usuario in usuarios]
    return jsonify(resultado), 200

# GET /api/usuarios/<id> - Obtener un usuario por ID
@user_bp.route('/<int:user_id>', methods=['GET'])
# @super_admin_required
def get_user(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario.to_dict()), 200

# POST /api/usuarios - Crear un nuevo usuario
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

# PUT /api/usuarios/<id> - Actualizar un usuario existente
@user_bp.route('/<int:user_id>', methods=['PATCH'])
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

# DELETE /api/usuarios/borrar_todo - Eliminar todos los usuarios
@user_bp.route('/borrar_todo', methods=['DELETE'])
@super_admin_required
def borrar_todo():
    usuarios_a_eliminar = Usuario.query.filter(Usuario.rol_id == 2).all()

    if not usuarios_a_eliminar:
        return jsonify({"mensaje": "No hay usuarios para eliminar"}), 200

    for usuario in usuarios_a_eliminar:
        db.session.delete(usuario)

    db.session.commit()
    return jsonify({"mensaje": "Usuarios eliminados, excepto los Admins"}), 200

@user_bp.route('/filtrar', methods=['GET'])
def filtrar_usuarios():
    centro_id = request.args.get('centro_id', type=int)
    sector_id = request.args.get('sector_id', type=int)

    query = Usuario.query

    if centro_id:
        query = query.filter_by(centro_id=centro_id)
    if sector_id:
        query = query.filter_by(sector_id=sector_id)

    usuarios = query.all()
    resultado = [u.to_dict() for u in usuarios]

    return jsonify(resultado), 200

@user_bp.route('/usuarios/<int:usuario_id>/intereses', methods=['GET'])
def obtener_intereses_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    intereses = [interes.to_dict() for interes in usuario.intereses]
    return jsonify(intereses), 200


@user_bp.route('/usuarios/<int:usuario_id>/intereses', methods=['GET'])
def obtener_intereses_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    intereses = [interes.to_dict() for interes in usuario.intereses]
    return jsonify(intereses), 200


# PUT /api/usuarios/<int:user_id>/rol - asignar rol a usuario (sólo el superadmin)

# @user_bp.route('/<int:user_id>/rol', methods=['PUT'])
# @super_admin_required
# def cambiar_rol_usuario(user_id):
#     current_user_id = get_jwt_identity()
#     current_user = Usuario.query.get(current_user_id)
#     if not current_user or current_user.rol_id != 1:
#         return jsonify({"error": "No autorizado"}), 403

#     usuario_objetivo = Usuario.query.get(user_id)
#     if not usuario_objetivo:
#         return jsonify({"error": "Usuario no encontrado"}), 404

#     data = request.get_json()
#     nuevo_rol_id = data.get("rol_id")
#     if not nuevo_rol_id:
#         return jsonify({"error": "Falta rol_id"}), 400

#     rol = Rol.query.get(nuevo_rol_id)
#     if not rol:
#         return jsonify({"error": "Rol no válido"}), 400

#     usuario_objetivo.rol_id = nuevo_rol_id
#     db.session.commit()

#     return jsonify({"mensaje": f"Rol cambiado a {rol.nombre} para el usuario {usuario_objetivo.nombre}"}), 200
