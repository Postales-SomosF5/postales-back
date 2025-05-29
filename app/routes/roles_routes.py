from flask import Blueprint, jsonify
from app.models.rol import Rol

rol_bp = Blueprint('rol', __name__, url_prefix='/api/roles')

@rol_bp.route('/', methods=['GET'])
def listar_roles():
    roles = Rol.query.all()
    return jsonify([{"id": r.id, "nombre": r.nombre} for r in roles])
