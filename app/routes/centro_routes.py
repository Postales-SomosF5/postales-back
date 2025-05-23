from flask import Blueprint, jsonify
from app.models.centro import Centro

centros_bp = Blueprint('centros', __name__)

@centros_bp.route('/centros/lista', methods=['GET'])
def listar_centros():
    centros = Centro.query.all()
    resultado = [centro.to_dict() for centro in centros]
    return jsonify(resultado), 200
