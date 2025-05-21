from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return {'message': 'Hola chamberos!!!'}, 200


@auth_bp.route("/test", methods=["GET"])
def test_route():
    return jsonify({"message": "Ruta de prueba funcionando"})


# Registro de usuario
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Validación básica
    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    # Aquí debemos guardar en la base de datos
    return jsonify({"message": f"Usuario {username} registrado correctamente"})

# Login de usuario
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Validación básica
    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    # Aquí deberías comprobar contra la base de datos
    return jsonify({"message": f"Bienvenido, {username}"})