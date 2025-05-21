from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    CORS(app)
    load_dotenv()

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)


    return app

