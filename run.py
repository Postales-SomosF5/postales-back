from app import create_app
from werkzeug.serving import WSGIRequestHandler

# Configurar el manejador de solicitudes para ignorar errores de protocolo
WSGIRequestHandler.protocol_version = "HTTP/1.1"

app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True, 
        host='0.0.0.0', 
        port=5000,
        ssl_context=None  # Deshabilita explícitamente SSL
    )
