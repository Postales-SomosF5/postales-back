import os
from dotenv import load_dotenv
from datetime import timedelta
# class Config:
#     SECRET_KEY = os.getenv('SECRET_KEY', 'secret-flask')
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

# Configuración JWT
JWT_CONFIG = {
    'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY', 'clave-secreta-desarrollo'),  # Cambiar en producción
    'JWT_ACCESS_TOKEN_EXPIRES': timedelta(hours=1),
    'JWT_REFRESH_TOKEN_EXPIRES': timedelta(days=30)
}

# Configuración de seguridad
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
}


