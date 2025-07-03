from flask import Blueprint, request, jsonify
from app.models.models import DisponibilidadHoraria, Docente
from app.schemas import disponibilidad_horaria_schema, disponibilidades_horarias_schema
from app import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

disponibilidad_horaria_bp = Blueprint('disponibilidad_horaria', __name__)

@disponibilidad_horaria_bp.route('/', methods=['GET'])
def get_disponibilidades():
    """Obtener todas las disponibilidades horarias"""
    try:
        disponibilidades = DisponibilidadHoraria.query.all()
        return jsonify({
            'success': True,
            'data': disponibilidades_horarias_schema.dump(disponibilidades)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@disponibilidad_horaria_bp.route('/<int:disponibilidad_id>', methods=['GET'])
def get_disponibilidad(disponibilidad_id):
    """Obtener una disponibilidad horaria específica"""
    try:
        disponibilidad = DisponibilidadHoraria.query.get_or_404(disponibilidad_id)
        return jsonify({
            'success': True,
            'data': disponibilidad_horaria_schema.dump(disponibilidad)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@disponibilidad_horaria_bp.route('/', methods=['POST'])
def create_disponibilidad():
    """Crear una nueva disponibilidad horaria"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('docente_id'):
            return jsonify({
                'success': False,
                'error': 'El docente_id es requerido'
            }), 400
        
        if not data.get('dia_semana'):
            return jsonify({
                'success': False,
                'error': 'El día de la semana es requerido'
            }), 400
        
        # Verificar que el docente existe
        docente = Docente.query.get(data['docente_id'])
        if not docente:
            return jsonify({
                'success': False,
                'error': 'El docente no existe'
            }), 400
        
        # Convertir horas si se proporcionan
        hora_inicio = None
        hora_fin = None
        
        if data.get('hora_inicio'):
            try:
                hora_inicio = datetime.strptime(data['hora_inicio'], '%H:%M').time()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Formato de hora_inicio inválido. Use HH:MM'
                }), 400
        
        if data.get('hora_fin'):
            try:
                hora_fin = datetime.strptime(data['hora_fin'], '%H:%M').time()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Formato de hora_fin inválido. Use HH:MM'
                }), 400
        
        # Crear la disponibilidad horaria
        disponibilidad = DisponibilidadHoraria(
            docente_id=data['docente_id'],
            dia_semana=data['dia_semana'],
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )
        
        db.session.add(disponibilidad)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': disponibilidad_horaria_schema.dump(disponibilidad),
            'message': 'Disponibilidad horaria creada exitosamente'
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error de integridad en la base de datos'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@disponibilidad_horaria_bp.route('/<int:disponibilidad_id>', methods=['PUT'])
def update_disponibilidad(disponibilidad_id):
    """Actualizar una disponibilidad horaria"""
    try:
        disponibilidad = DisponibilidadHoraria.query.get_or_404(disponibilidad_id)
        data = request.get_json()
        
        # Verificar que el docente existe si se va a actualizar
        if data.get('docente_id'):
            docente = Docente.query.get(data['docente_id'])
            if not docente:
                return jsonify({
                    'success': False,
                    'error': 'El docente no existe'
                }), 400
        
        # Convertir horas si se proporcionan
        hora_inicio = disponibilidad.hora_inicio
        hora_fin = disponibilidad.hora_fin
        
        if data.get('hora_inicio'):
            try:
                hora_inicio = datetime.strptime(data['hora_inicio'], '%H:%M').time()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Formato de hora_inicio inválido. Use HH:MM'
                }), 400
        
        if data.get('hora_fin'):
            try:
                hora_fin = datetime.strptime(data['hora_fin'], '%H:%M').time()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Formato de hora_fin inválido. Use HH:MM'
                }), 400
        
        # Actualizar campos
        disponibilidad.docente_id = data.get('docente_id', disponibilidad.docente_id)
        disponibilidad.dia_semana = data.get('dia_semana', disponibilidad.dia_semana)
        disponibilidad.hora_inicio = hora_inicio
        disponibilidad.hora_fin = hora_fin
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': disponibilidad_horaria_schema.dump(disponibilidad),
            'message': 'Disponibilidad horaria actualizada exitosamente'
        }), 200
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error de integridad en la base de datos'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@disponibilidad_horaria_bp.route('/<int:disponibilidad_id>', methods=['DELETE'])
def delete_disponibilidad(disponibilidad_id):
    """Eliminar una disponibilidad horaria"""
    try:
        disponibilidad = DisponibilidadHoraria.query.get_or_404(disponibilidad_id)
        db.session.delete(disponibilidad)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Disponibilidad horaria eliminada exitosamente'
        }), 200
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error de integridad en la base de datos'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@disponibilidad_horaria_bp.route('/por-docente/<int:docente_id>', methods=['GET'])
def get_disponibilidades_por_docente(docente_id):
    """Obtener disponibilidad horaria de un docente específico"""
    try:
        disponibilidades = DisponibilidadHoraria.query.filter_by(docente_id=docente_id).all()
        return jsonify({
            'success': True,
            'data': disponibilidades_horarias_schema.dump(disponibilidades)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@disponibilidad_horaria_bp.route('/buscar', methods=['GET'])
def buscar_disponibilidades():
    """Buscar disponibilidades horarias por criterios"""
    try:
        docente_id = request.args.get('docente_id', '')
        dia_semana = request.args.get('dia_semana', '')
        
        query = DisponibilidadHoraria.query
        
        if docente_id:
            query = query.filter(DisponibilidadHoraria.docente_id == int(docente_id))
        if dia_semana:
            query = query.filter(DisponibilidadHoraria.dia_semana.ilike(f'%{dia_semana}%'))
        
        disponibilidades = query.all()
        
        return jsonify({
            'success': True,
            'data': disponibilidades_horarias_schema.dump(disponibilidades)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@disponibilidad_horaria_bp.route('/horario-semanal/<int:docente_id>', methods=['GET'])
def get_horario_semanal_docente(docente_id):
    """Obtener horario semanal completo de un docente"""
    try:
        # Verificar que el docente existe
        docente = Docente.query.get_or_404(docente_id)
        
        # Obtener todas las disponibilidades del docente
        disponibilidades = DisponibilidadHoraria.query.filter_by(docente_id=docente_id).all()
        
        # Organizar por día de la semana
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        horario_semanal = {}
        
        for dia in dias_semana:
            horario_semanal[dia] = []
        
        for disponibilidad in disponibilidades:
            if disponibilidad.dia_semana in horario_semanal:
                horario_semanal[disponibilidad.dia_semana].append({
                    'id': disponibilidad.id,
                    'hora_inicio': str(disponibilidad.hora_inicio) if disponibilidad.hora_inicio else None,
                    'hora_fin': str(disponibilidad.hora_fin) if disponibilidad.hora_fin else None
                })
        
        return jsonify({
            'success': True,
            'data': {
                'docente': {
                    'id': docente.id,
                    'nombre': docente.nombre
                },
                'horario_semanal': horario_semanal
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 