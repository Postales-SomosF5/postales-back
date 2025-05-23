from flask import Blueprint, jsonify
from app.models.sector import Sector

sector_bp = Blueprint('sectores', __name__)

@sector_bp.route('/sectores/lista', methods=['GET'])
def listar_sectores():
    sectores = Sector.query.all()
    resultado = [sector.to_dict() for sector in sectores]
    return jsonify(resultado), 200
