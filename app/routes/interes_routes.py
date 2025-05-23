from flask import Blueprint, jsonify
from app.models.interes import Interes

intereses_bp = Blueprint('intereses', __name__)

@intereses_bp.route('/intereses/lista', methods=['GET'])
def listar_intereses():
    intereses = Interes.query.all()
    resultado = [interes.to_dict() for interes in intereses]
    return jsonify(resultado), 200
