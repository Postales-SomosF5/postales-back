from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

@app.route('/api/hello')
def hello():
    return jsonify(message="¡Hola desde Flask!")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
