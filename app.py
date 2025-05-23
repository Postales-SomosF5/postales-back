from flask import Flask, jsonify, request
import mysql.connector
import jwt
import datetime
from functools import wraps
from config import DB_CONFIG
from dotenv import load_dotenv
import os
import bcrypt
from flask_cors import CORS

# Cargar variables de entorno desde .env
load_dotenv()

# Crear aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_secret_key')
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# === DECORADORES DE ACCESO SEGÚN ROL ===

def login_required(f):
    """
    Requiere que el usuario tenga sesión iniciada.
    El token debe estar presente y válido.
    """

    return token_required(f) 

def admin_required(f):
    """
    Requiere que el usuario sea 'admin' o 'super_admin'.
    """
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user['rol'] not in ['admin', 'super_admin']:
            return jsonify({'mensaje': 'Acceso denegado: se requiere rol de administrador'}), 403
        return f(current_user, *args, **kwargs)
    return token_required(decorated)

def super_admin_required(f):
    """
    Requiere que el usuario sea 'super_admin'.
    """
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user['rol'] != 'super_admin':
            return jsonify({'mensaje': 'Acceso denegado: se requiere rol de super administrador'}), 403
        return f(current_user, *args, **kwargs)
    return token_required(decorated)


# === FUNCIONES AUXILIARES ===

def token_required(f):
    """
    Verifica que el token JWT esté presente y sea válido.
    Si es válido, extrae la información del usuario y su rol.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'mensaje': 'Token faltante'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = {
                'email': data['user'],
                'rol': data.get('rol', 'usuario')  # Si no hay rol, asume 'usuario'
            }
        except Exception as e:
            print("Error al decodificar token:", str(e))
            return jsonify({'mensaje': 'Token inválido'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


def get_db_connection():
    """
    Devuelve una conexión a la base de datos MySQL.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error de conexión a la base de datos: {err}")
        raise

# === RUTAS ===

@app.route('/registro', methods=['POST'])
@super_admin_required
def registrar_usuario(current_user):
    """
    Endpoint para registro de usuarios. Solo accesible por 'super_admin'.
    Guarda contraseña como hash y asigna rol predeterminado ('usuario').
    """
    datos = request.get_json()
    nombre = datos['nombre']
    email = datos['email']
    password = datos['password']
    rol = datos.get('rol', 'usuario')  # Por defecto: usuario normal

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'mensaje': 'El correo ya está en uso'}), 400

        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)",
            (nombre, email, hashed_password.decode('utf-8'), rol)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({'mensaje': 'Error al registrar usuario', 'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    """
    Inicia sesión y devuelve un token JWT con rol incluido.
    """
    datos = request.get_json()
    email = datos['email']
    password = datos['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario['password'].encode('utf-8')):
        token = jwt.encode({
            'user': usuario['email'],
            'rol': usuario['rol'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token})
    else:
        return jsonify({'mensaje': 'Credenciales inválidas'}), 401


@app.route('/perfil', methods=['GET'])
@login_required
def perfil(current_user):
    """
    Muestra el perfil del usuario autenticado.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, nombre, email, rol FROM usuarios WHERE email = %s", (current_user['email'],))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if usuario:
        return jsonify({'usuario': usuario}), 200
    else:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404


@app.route('/admin/dashboard', methods=['GET'])
@admin_required
def dashboard_admin(current_user):
    """
    Accesible solo para admins y super_admins.
    """
    return jsonify({'mensaje': f'Bienvenido al panel de administración, {current_user["email"]}'})


@app.route('/super-admin/configuraciones', methods=['GET'])
@super_admin_required
def configuraciones_super_admin(current_user):
    """
    Accesible solo para super_admin.
    """
    return jsonify({'mensaje': f'Configuraciones avanzadas - Acceso total, {current_user["email"]}'})


# === INICIAR SERVIDOR ===
if __name__ == '__main__':
    app.run(debug=True)