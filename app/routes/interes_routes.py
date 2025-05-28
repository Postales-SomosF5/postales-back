from flask import Blueprint, jsonify
from app.models.interes import Interes
from app.utils.jwt_utils import admin_required

intereses_bp = Blueprint('intereses', __name__)

@intereses_bp.route('/intereses/lista', methods=['GET'])
@admin_required
def listar_intereses():
    intereses = Interes.query.all()
    resultado = [interes.to_dict() for interes in intereses]
    return jsonify(resultado), 200
