from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, bcrypt
from app.models.user import Usuario
from datetime import datetime
from flask_jwt_extended import create_access_token

from flask_mail import Message
from app.extensions import mail

auth_bp = Blueprint('auth', __name__) 

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data.get('email') or not data.get('contrasena'):
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({"error": "El usuario ya existe"}), 400

    fecha_alta = data.get('fecha_alta') or datetime.utcnow().date()
    fecha_baja = data.get('fecha_baja') or None

    nuevo_usuario = Usuario(
        nombre=data.get('nombre'),
        apellido=data.get('apellido'),
        email=data['email'],
        rol_id=data.get('rol_id'),
        centro_id=data.get('centro_id'),
        sector_id=data.get('sector_id'),
        refuerzo_linguistico=data.get('refuerzo_linguistico'),
        penascal_rol=data.get('penascal_rol'),
        fecha_alta=fecha_alta,
        fecha_baja=fecha_baja
    )

    nuevo_usuario.set_password(data['contrasena'])

    try:
        db.session.add(nuevo_usuario)
        db.session.commit()

        # Envío de correo de confirmación
        msg = Message(
            subject="Registro exitoso",
            recipients=[nuevo_usuario.email],
            body=f"Hola {nuevo_usuario.nombre}, tu registro en la plataforma se ha realizado correctamente.\n\nGracias por unirte."
        )
        # mail.send(msg)

        return jsonify({"mensaje": "Usuario registrado correctamente y correo enviado"}), 201

    except Exception as e:
        db.session.rollback()
        print("ERROR REGISTRO:", str(e))  # Esto te lo mostrará en consola
        return jsonify({
            "error": "Error en el servidor al registrar usuario.",
            "detalle": str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data.get('email') or not data.get('contrasena'):
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    usuario = Usuario.query.filter_by(email=data['email']).first()

    if not usuario or not usuario.check_password(data['contrasena']):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Generar token JWT
    access_token = create_access_token(
        identity=str(usuario.id),
        additional_claims={
            'user': usuario.email,
            'rol': usuario.rol_id
        }
    )

    return jsonify({
        "mensaje": "Login exitoso", 
        "usuario_id": usuario.id, 
        "rol": usuario.rol_id,
        "access_token": access_token
    }), 200
