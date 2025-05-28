from flask import Flask, jsonify  
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.centro_routes import centros_bp
from app.routes.sector_routes import sector_bp
from app.routes.interes_routes import intereses_bp
from app.routes.emparejamiento_routes import emparejamientos_bp
from .extensions import db, bcrypt 
import os
from flask_jwt_extended import JWTManager
from config import JWT_CONFIG, SECURITY_HEADERS, DB_CONFIG


def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') or "secreto"

    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    app.register_blueprint(centros_bp, url_prefix='/api')    
    
    app.register_blueprint(sector_bp, url_prefix='/api')    
    
    app.register_blueprint(intereses_bp, url_prefix='/api')    

     # Configuración de JWT
    app.config['JWT_SECRET_KEY'] = JWT_CONFIG['JWT_SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_CONFIG['JWT_ACCESS_TOKEN_EXPIRES']
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_CONFIG['JWT_REFRESH_TOKEN_EXPIRES']
    
    # Inicializar extensiones
    jwt = JWTManager(app)

    # Ruta de prueba en la raíz
    @app.route('/')
    def index():
        return jsonify({"mensaje": "Bienvenidx a la API de Chamberos wuwhuho"}), 200
    
    # Manejo de errores
    @app.after_request
    def add_security_headers(response):
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value
        return response

    return app
