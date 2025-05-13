from flask import Blueprint, request, jsonify
from app.models import db, Cita
from datetime import datetime

api = Blueprint('api', __name__)

@api.route('/')
@api.route('/dashboard')
def index():
    return '<h1>API de Citas Médicas - Corriendo</h1>'

# GET todas las citas
@api.route('/citas', methods=['GET'])
def listar_citas():
    citas = Cita.query.all()
    data = [
        {
            'id': cita.id,
            'fecha_hora': cita.fecha_hora.strftime('%Y-%m-%d %H:%M'),
            'medico_id': cita.medico_id,
            'paciente_id': cita.paciente_id,
            'motivo': cita.motivo,
            'estado': cita.estado
        }
        for cita in citas
    ]
    return jsonify(data), 200

# GET cita por ID
@api.route('/citas/<int:id>', methods=['GET'])
def obtener_cita(id):
    cita = Cita.query.get_or_404(id)
    data = {
        'id': cita.id,
        'fecha_hora': cita.fecha_hora.strftime('%Y-%m-%d %H:%M'),
        'medico_id': cita.medico_id,
        'paciente_id': cita.paciente_id,
        'motivo': cita.motivo,
        'estado': cita.estado,
        'observaciones': cita.observaciones
    }
    return jsonify(data), 200

# POST crear nueva cita
@api.route('/citas', methods=['POST'])
def crear_cita():
    data = request.get_json()
    try:
        cita = Cita(
            fecha_hora=datetime.strptime(data['fecha_hora'], '%Y-%m-%d %H:%M'),
            medico_id=data['medico_id'],
            paciente_id=data['paciente_id'],
            motivo=data['motivo'],
            estado=data.get('estado', 'Agendada'),
            observaciones=data.get('observaciones', '')
        )
        db.session.add(cita)
        db.session.commit()
        return jsonify({'message': 'Cita creada', 'id': cita.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# PUT actualizar cita
@api.route('/citas/<int:id>', methods=['PUT'])
def actualizar_cita(id):
    cita = Cita.query.get_or_404(id)
    data = request.get_json()

    if 'fecha_hora' in data:
        cita.fecha_hora = datetime.strptime(data['fecha_hora'], '%Y-%m-%d %H:%M')
    cita.medico_id = data.get('medico_id', cita.medico_id)
    cita.paciente_id = data.get('paciente_id', cita.paciente_id)
    cita.motivo = data.get('motivo', cita.motivo)
    cita.estado = data.get('estado', cita.estado)
    cita.observaciones = data.get('observaciones', cita.observaciones)

    db.session.commit()
    return jsonify({'message': 'Cita actualizada', 'id': cita.id}), 200

# DELETE eliminar cita
@api.route('/citas/<int:id>', methods=['DELETE'])
def eliminar_cita(id):
    cita = Cita.query.get_or_404(id)
    db.session.delete(cita)
    db.session.commit()
    return jsonify({'message': 'Cita eliminada', 'id': cita.id}), 200