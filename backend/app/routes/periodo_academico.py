from flask import Blueprint, request, jsonify
from app.models.models import PeriodoAcademico
from app.schemas import periodo_academico_schema, periodos_academicos_schema
from app import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

periodo_academico_bp = Blueprint('periodo_academico', __name__)

@periodo_academico_bp.route('/', methods=['GET'])
def get_periodos_academicos():
    """Obtener todos los períodos académicos"""
    try:
        periodos = PeriodoAcademico.query.all()
        return jsonify({
            'success': True,
            'data': periodos_academicos_schema.dump(periodos)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@periodo_academico_bp.route('/<int:periodo_id>', methods=['GET'])
def get_periodo_academico(periodo_id):
    """Obtener un período académico específico"""
    try:
        periodo = PeriodoAcademico.query.get_or_404(periodo_id)
        return jsonify({
            'success': True,
            'data': periodo_academico_schema.dump(periodo)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@periodo_academico_bp.route('/', methods=['POST'])
def create_periodo_academico():
    """Crear un nuevo período académico"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        
        # Convertir fechas si se proporcionan
        fecha_inicio = None
        fecha_fin = None
        
        if data.get('fecha_inicio'):
            try:
                fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Formato de fecha_inicio inválido. Use YYYY-MM-DD'
                }), 400
        
        if data.get('fecha_fin'):
            try:
                fecha_fin = datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Formato de fecha_fin inválido. Use YYYY-MM-DD'
                }), 400
        
        # Crear el período académico
        periodo = PeriodoAcademico(
            nombre=data['nombre'],
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
        db.session.add(periodo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': periodo_academico_schema.dump(periodo),
            'message': 'Período académico creado exitosamente'
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

@periodo_academico_bp.route('/<int:periodo_id>', methods=['PUT'])
def update_periodo_academico(periodo_id):
    """Actualizar un período académico"""
    try:
        periodo = PeriodoAcademico.query.get_or_404(periodo_id)
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        
        # Convertir fechas si se proporcionan
        if data.get('fecha_inicio'):
            try:
                fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Formato de fecha_inicio inválido. Use YYYY-MM-DD'
                }), 400
        else:
            fecha_inicio = periodo.fecha_inicio
        
        if data.get('fecha_fin'):
            try:
                fecha_fin = datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Formato de fecha_fin inválido. Use YYYY-MM-DD'
                }), 400
        else:
            fecha_fin = periodo.fecha_fin
        
        # Actualizar campos
        periodo.nombre = data['nombre']
        periodo.fecha_inicio = fecha_inicio
        periodo.fecha_fin = fecha_fin
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': periodo_academico_schema.dump(periodo),
            'message': 'Período académico actualizado exitosamente'
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

@periodo_academico_bp.route('/<int:periodo_id>', methods=['DELETE'])
def delete_periodo_academico(periodo_id):
    """Eliminar un período académico"""
    try:
        periodo = PeriodoAcademico.query.get_or_404(periodo_id)
        db.session.delete(periodo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Período académico eliminado exitosamente'
        }), 200
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'No se puede eliminar el período académico porque tiene registros relacionados'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@periodo_academico_bp.route('/buscar', methods=['GET'])
def buscar_periodos_academicos():
    """Buscar períodos académicos por criterios"""
    try:
        nombre = request.args.get('nombre', '')
        anio = request.args.get('anio', '')
        
        query = PeriodoAcademico.query
        
        if nombre:
            query = query.filter(PeriodoAcademico.nombre.ilike(f'%{nombre}%'))
        if anio:
            query = query.filter(PeriodoAcademico.nombre.ilike(f'%{anio}%'))
        
        periodos = query.all()
        
        return jsonify({
            'success': True,
            'data': periodos_academicos_schema.dump(periodos)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@periodo_academico_bp.route('/actual', methods=['GET'])
def get_periodo_actual():
    """Obtener el período académico actual"""
    try:
        from datetime import date
        hoy = date.today()
        
        # Buscar período que incluya la fecha actual
        periodo = PeriodoAcademico.query.filter(
            PeriodoAcademico.fecha_inicio <= hoy,
            PeriodoAcademico.fecha_fin >= hoy
        ).first()
        
        if not periodo:
            # Si no hay período actual, devolver el más reciente
            periodo = PeriodoAcademico.query.order_by(
                PeriodoAcademico.fecha_inicio.desc()
            ).first()
        
        if periodo:
            return jsonify({
                'success': True,
                'data': periodo_academico_schema.dump(periodo)
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró ningún período académico'
            }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 