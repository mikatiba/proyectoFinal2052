from flask import request, jsonify, Blueprint
from app.models import db, Cita
from datetime import datetime

main = Blueprint('test_routes', __name__, url_prefix='/test')

@main.route('/citas', methods=['POST'])
def crear_cita_test():
    data = request.get_json()
    cita = Cita(
        fecha_hora=datetime.fromisoformat(data.get('fecha_hora')),
        motivo=data.get('motivo'),
        medico_id=data.get('medico_id'),
        paciente_id=data.get('paciente_id'),
        estado='Agendada'
    )
    db.session.add(cita)
    db.session.commit()
    return jsonify({'message': 'Cita creada correctamente'}), 200

@main.route('/citas', methods=['GET'])
def obtener_citas_test():
    citas = Cita.query.all()
    return jsonify([{
        'id': c.id,
        'fecha_hora': c.fecha_hora.isoformat(),
        'motivo': c.motivo,
        'estado': c.estado,
        'medico_id': c.medico_id,
        'paciente_id': c.paciente_id
    } for c in citas]), 200

@main.route('/citas/<int:id>', methods=['GET'])
def obtener_cita_por_id_test(id):
    cita = Cita.query.get_or_404(id)
    return jsonify({
        'id': cita.id,
        'fecha_hora': cita.fecha_hora.isoformat(),
        'motivo': cita.motivo,
        'estado': cita.estado,
        'medico_id': cita.medico_id,
        'paciente_id': cita.paciente_id
    }), 200

@main.route('/citas/<int:id>', methods=['PUT'])
def actualizar_cita_test(id):
    cita = Cita.query.get_or_404(id)
    data = request.get_json()

    cita.motivo = data.get('motivo', cita.motivo)
    cita.estado = data.get('estado', cita.estado)
    db.session.commit()

    return jsonify({'message': 'Cita actualizada'}), 200

@main.route('/citas/<int:id>', methods=['DELETE'])
def eliminar_cita_test(id):
    cita = Cita.query.get_or_404(id)
    db.session.delete(cita)
    db.session.commit()
    return jsonify({'message': 'Cita eliminada'}), 200