import os
from dotenv import load_dotenv
# class Config:
#     SECRET_KEY = os.getenv('SECRET_KEY', 'secret-flask')
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# Cargar variables de entorno desde .env
load_dotenv()

#DB conection
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB'),
    'port': os.getenv('MYSQL_PORT')
}