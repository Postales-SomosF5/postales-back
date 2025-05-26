from app.utils.jwt_utils import admin_required, super_admin_required
from flask import Blueprint, jsonify, request
from app.models.emparejamiento import Emparejamiento
from app.models.user import Usuario
from app.extensions import db
from datetime import date

emparejamientos_bp = Blueprint('emparejamientos', __name__)

# POST /api/emparejamientos
@emparejamientos_bp.route('/emparejamientos', methods=['POST'])
@admin_required
def crear_emparejamiento():
    data = request.get_json()
    usuario_a_id = data.get('usuario_a_id')
    usuario_b_id = data.get('usuario_b_id')

    if not usuario_a_id or not usuario_b_id:
        return jsonify({"error": "Faltan IDs de usuario"}), 400

 # Obtener usuarios de la base de datos
    usuario_a = Usuario.query.get(usuario_a_id)
    usuario_b = Usuario.query.get(usuario_b_id)

    if not usuario_a or not usuario_b:
        return jsonify({"error": "Uno o ambos usuarios no existen"}), 404

    # Validación: sectores diferentes
    if usuario_a.sector_id == usuario_b.sector_id:
        return jsonify({"error": "Los usuarios deben ser de sectores diferentes"}), 400

    # Validación: uno con refuerzo y otro sin
    if usuario_a.refuerzo_linguistico == usuario_b.refuerzo_linguistico:
        return jsonify({"error": "Uno debe tener refuerzo_linguistico y el otro no"}), 400

    # Crear emparejamiento
    emp = Emparejamiento(
        usuario_a_id=usuario_a_id,
        usuario_b_id=usuario_b_id,
        fecha_emparejamiento=date.today(),
        estado=0
    )
    
    db.session.add(emp)
    db.session.commit()
    return jsonify(emp.to_dict()), 201

# GET /api/emparejamientos/lista
@emparejamientos_bp.route('/emparejamientos/lista', methods=['GET'])
@admin_required
def listar_emparejamientos():
    emparejamientos = Emparejamiento.query.all()
    resultado = [emparejamiento.to_dict() for emparejamiento in emparejamientos]
    return jsonify(resultado), 200

@emparejamientos_bp.route('/emparejamientos/auto', methods=['POST'])
@super_admin_required
def emparejamiento_automatico():
    usuarios = Usuario.query.all()

    # Separar en dos grupos según refuerzo lingüístico
    con_refuerzo = [u for u in usuarios if u.refuerzo_linguistico]
    sin_refuerzo = [u for u in usuarios if not u.refuerzo_linguistico]

    # Obtener emparejamientos actuales para evitar duplicados
    emparejamientos_actuales = Emparejamiento.query.all()
    emparejados_ids = set()
    for emp in emparejamientos_actuales:
        emparejados_ids.add(emp.usuario_a_id)
        emparejados_ids.add(emp.usuario_b_id)

    # Conteo de parejas por usuario (iniciar en 0 para todos)
    parejas_por_usuario = {u.id: 0 for u in usuarios}

    # Función para saber si dos usuarios ya están emparejados
    def ya_emparejado(id1, id2):
        for emp in emparejamientos_actuales:
            if (emp.usuario_a_id == id1 and emp.usuario_b_id == id2) or (emp.usuario_a_id == id2 and emp.usuario_b_id == id1):
                return True
        return False

    emparejamientos_creados = []

    # 1. Emparejar usuarios NO emparejados para que tengan al menos 1 pareja
    # Filtrar usuarios sin pareja aún (0 parejas)
    sin_pareja_con_refuerzo = [u for u in con_refuerzo if parejas_por_usuario[u.id] == 0]
    sin_pareja_sin_refuerzo = [u for u in sin_refuerzo if parejas_por_usuario[u.id] == 0]

    for u1 in sin_pareja_con_refuerzo:
        for u2 in sin_pareja_sin_refuerzo:
            if parejas_por_usuario[u1.id] >= 1:
                break
            if parejas_por_usuario[u2.id] >= 1:
                continue
            if u1.sector_id != u2.sector_id and not ya_emparejado(u1.id, u2.id):
                emp = Emparejamiento(
                    usuario_a_id=u1.id,
                    usuario_b_id=u2.id,
                    fecha_emparejamiento=date.today(),
                    estado=0
                )
                db.session.add(emp)
                emparejamientos_creados.append({"usuario_a": u1.to_dict(), "usuario_b": u2.to_dict()})
                parejas_por_usuario[u1.id] += 1
                parejas_por_usuario[u2.id] += 1
                sin_pareja_sin_refuerzo.remove(u2)
                break

    # 2. Intentar dar una segunda pareja a los usuarios que tengan solo 1 pareja (hasta max 2)
    # Para esto usamos listas completas, pero filtrando por parejas < 2
    con_refuerzo_disponibles = [u for u in con_refuerzo if parejas_por_usuario[u.id] < 2]
    sin_refuerzo_disponibles = [u for u in sin_refuerzo if parejas_por_usuario[u.id] < 2]

    # Intentamos emparejar todos contra todos con reglas y sin repetir emparejamientos
    for u1 in con_refuerzo_disponibles:
        if parejas_por_usuario[u1.id] >= 2:
            continue
        for u2 in sin_refuerzo_disponibles:
            if parejas_por_usuario[u2.id] >= 2:
                continue
            if u1.id == u2.id:
                continue  # No emparejar consigo mismo (por si acaso)
            if u1.sector_id != u2.sector_id and not ya_emparejado(u1.id, u2.id):
                emp = Emparejamiento(
                    usuario_a_id=u1.id,
                    usuario_b_id=u2.id,
                    fecha_emparejamiento=date.today(),
                    estado=0
                )
                db.session.add(emp)
                emparejamientos_creados.append({"usuario_a": u1.to_dict(), "usuario_b": u2.to_dict()})
                parejas_por_usuario[u1.id] += 1
                parejas_por_usuario[u2.id] += 1
                if parejas_por_usuario[u1.id] >= 2:
                    break

    # 3. Si quedan usuarios sin pareja, repetir emparejamientos permitiendo repetir usuarios ya emparejados
    # Esto para que nadie quede sin pareja (aunque se repitan usuarios)
    sin_pareja = [u for u in usuarios if parejas_por_usuario[u.id] == 0]

    # Volvemos a separar según refuerzo lingüístico
    sin_pareja_con_refuerzo = [u for u in sin_pareja if u.refuerzo_linguistico]
    sin_pareja_sin_refuerzo = [u for u in sin_pareja if not u.refuerzo_linguistico]

    # Aquí ya permitimos repetir emparejamientos previos, pero no con el mismo usuario (no consigo conmigo mismo)
    for u1 in sin_pareja_con_refuerzo:
        for u2 in sin_pareja_sin_refuerzo:
            if u1.sector_id != u2.sector_id and u1.id != u2.id:
                # Crear emparejamiento, aunque exista repetido
                emp = Emparejamiento(
                    usuario_a_id=u1.id,
                    usuario_b_id=u2.id,
                    fecha_emparejamiento=date.today(),
                    estado=0
                )
                db.session.add(emp)
                emparejamientos_creados.append({"usuario_a": u1.to_dict(), "usuario_b": u2.to_dict()})
                parejas_por_usuario[u1.id] += 1
                parejas_por_usuario[u2.id] += 1
                break  # Al menos una pareja ya tienen

    db.session.commit()

    if emparejamientos_creados:
        return jsonify({
            "mensaje": f"{len(emparejamientos_creados)} emparejamientos creados",
            "emparejamientos": emparejamientos_creados
        }), 201
    else:
        return jsonify({"mensaje": "No se encontraron usuarios compatibles para emparejar"}), 404

