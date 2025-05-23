from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde .env

app = Flask(__name__)

# Configura la URI de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define un modelo simple para prueba
class TestUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Ejecuta una prueba para crear la tabla
with app.app_context():
    try:
        db.create_all()
        print("✅ Conexión exitosa y tabla creada correctamente.")
    except Exception as e:
        print("❌ Error al conectar o crear tabla:")
        print(e)
