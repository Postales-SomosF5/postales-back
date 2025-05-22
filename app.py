# Importamos las librerías necesarias
from flask import Flask, jsonify, request
import mysql.connector  # Para conectar con MySQL
import jwt               # Para generar y verificar tokens JWT
import datetime          # Para establecer la expiración del token
from functools import wraps  # Para decoradores personalizados
from config import db_config   # Configuración de la base de datos
from dotenv import load_dotenv  # Para cargar variables desde .env
from datetime import datetime, timezone  # Añadir timezone a los imports
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Creamos la aplicación Flask
app = Flask(__name__)

# Configuramos una clave secreta que se usará para firmar los tokens JWT.
# Esta clave debe ser segura y única. En producción, no debe estar en el código.
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_secret_key')

# === DECORADOR: Requiere token válido para acceder a rutas protegidas ===
def token_required(f):
    """
    Este es un decorador que protege las rutas que lo usan.
    Solo permite ejecutar la función si se envía un token válido en el encabezado.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Buscamos el token en el encabezado "x-access-token"
        token = request.headers.get('x-access-token')

        if not token:
            return jsonify({'mensaje': 'Token faltante'}), 401

        try:
            # Decodificamos el token usando la clave secreta
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user']  # Extraemos el usuario del token
        except Exception as e:
            print("Error al decodificar el token:", str(e))
            return jsonify({'mensaje': 'Token inválido'}), 401

        # Si todo está bien, pasamos el usuario autenticado a la función original
        return f(current_user, *args, **kwargs)

    return decorated


# === FUNCIÓN AUXILIAR: Conectar a la base de datos ===
def get_db_connection():
    """
    Función auxiliar para conectarse a la base de datos MySQL
    usando la configuración definida en config.py
    """
    conn = mysql.connector.connect(**db_config)
    return conn


# === RUTA: Registro de nuevo usuario ===
@app.route('/registro', methods=['POST'])
def registrar_usuario():
    """
    Endpoint para registrar un nuevo usuario.
    Recibe nombre, email y password en formato JSON.
    Verifica si el correo ya existe y lo inserta en la base de datos.
    """

    # Obtenemos los datos del cuerpo de la solicitud (JSON)
    datos = request.get_json()
    nombre = datos['nombre']
    email = datos['email']
    password = datos['password']

    # Nos conectamos a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # dictionary=True devuelve resultados como diccionarios

    try:
        # Verificamos si ya existe un usuario con ese email
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'mensaje': 'El correo ya está en uso'}), 400

        # Insertamos el nuevo usuario en la tabla
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password)
        )
        conn.commit()  # Guardamos los cambios en la base de datos
        cursor.close()
        conn.close()

        return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201

    except Exception as e:
        conn.rollback()  # Deshacemos cualquier cambio si hubo error
        return jsonify({'mensaje': 'Error al registrar usuario', 'error': str(e)}), 500


# === RUTA: Iniciar sesión y devolver token JWT ===
@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint para iniciar sesión.
    Recibe email y contraseña, verifica contra la base de datos,
    y devuelve un token JWT si las credenciales son correctas.
    """

    datos = request.get_json()
    email = datos['email']
    password = datos['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Buscamos al usuario por su email
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    # Comprobamos si el usuario existe y si la contraseña coincide
    if usuario and usuario['password'] == password:
        # Generamos un token JWT con:
        # - El email del usuario
        # - Fecha de expiración (30 minutos)
        token = jwt.encode({
            'user': usuario['email'],
            'exp': datetime.now(timezone.utc) + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token})
    else:
        return jsonify({'mensaje': 'Credenciales inválidas'}), 401


# === RUTA: Perfil protegido con token ===
@app.route('/perfil', methods=['GET'])
@token_required
def perfil(current_user):
    """
    Endpoint protegido. Solo accesible con token válido.
    Devuelve información del usuario actual desde la base de datos.
    """

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Buscamos al usuario por su email (guardado en el token)
    cursor.execute("SELECT id, nombre, email FROM usuarios WHERE email = %s", (current_user,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if usuario:
        return jsonify({'usuario': usuario}), 200
    else:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404


# === INICIAR SERVIDOR ===
if __name__ == '__main__':
    """
    Punto de entrada del programa.
    Ejecutamos la aplicación Flask en modo debug.
    """
    app.run(debug=True)