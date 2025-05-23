from flask import Blueprint, jsonify
from app.models.emparejamiento import Emparejamiento

emparejamientos_bp = Blueprint('emparejamientos', __name__)

@emparejamientos_bp.route('/emparejamientos/lista', methods=['GET'])
def listar_emparejamientos():
    emparejamientos = Emparejamiento.query.all()
    resultado = [emparejamiento.to_dict() for emparejamiento in emparejamientos]
    return jsonify(resultado), 200
