from flask import Blueprint, request, jsonify
from app.models.models import LineaInvestigacion
from app.schemas import linea_investigacion_schema, lineas_investigacion_schema
from app import db
from sqlalchemy.exc import IntegrityError

linea_investigacion_bp = Blueprint('linea_investigacion', __name__)

@linea_investigacion_bp.route('/', methods=['GET'])
def get_lineas_investigacion():
    """Obtener todas las líneas de investigación"""
    try:
        lineas = LineaInvestigacion.query.all()
        return jsonify({
            'success': True,
            'data': lineas_investigacion_schema.dump(lineas)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@linea_investigacion_bp.route('/<int:linea_id>', methods=['GET'])
def get_linea_investigacion(linea_id):
    """Obtener una línea de investigación específica"""
    try:
        linea = LineaInvestigacion.query.get_or_404(linea_id)
        return jsonify({
            'success': True,
            'data': linea_investigacion_schema.dump(linea)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@linea_investigacion_bp.route('/', methods=['POST'])
def create_linea_investigacion():
    """Crear una nueva línea de investigación"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        
        # Crear la línea de investigación
        linea = LineaInvestigacion(nombre=data['nombre'])
        
        db.session.add(linea)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': linea_investigacion_schema.dump(linea),
            'message': 'Línea de investigación creada exitosamente'
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

@linea_investigacion_bp.route('/<int:linea_id>', methods=['PUT'])
def update_linea_investigacion(linea_id):
    """Actualizar una línea de investigación"""
    try:
        linea = LineaInvestigacion.query.get_or_404(linea_id)
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        
        # Actualizar campos
        linea.nombre = data['nombre']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': linea_investigacion_schema.dump(linea),
            'message': 'Línea de investigación actualizada exitosamente'
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

@linea_investigacion_bp.route('/<int:linea_id>', methods=['DELETE'])
def delete_linea_investigacion(linea_id):
    """Eliminar una línea de investigación"""
    try:
        linea = LineaInvestigacion.query.get_or_404(linea_id)
        db.session.delete(linea)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Línea de investigación eliminada exitosamente'
        }), 200
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'No se puede eliminar la línea de investigación porque tiene registros relacionados'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@linea_investigacion_bp.route('/buscar', methods=['GET'])
def buscar_lineas_investigacion():
    """Buscar líneas de investigación por criterios"""
    try:
        nombre = request.args.get('nombre', '')
        
        query = LineaInvestigacion.query
        
        if nombre:
            query = query.filter(LineaInvestigacion.nombre.ilike(f'%{nombre}%'))
        
        lineas = query.all()
        
        return jsonify({
            'success': True,
            'data': lineas_investigacion_schema.dump(lineas)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@linea_investigacion_bp.route('/<int:linea_id>/estadisticas', methods=['GET'])
def get_estadisticas_linea(linea_id):
    """Obtener estadísticas de una línea de investigación"""
    try:
        linea = LineaInvestigacion.query.get_or_404(linea_id)
        
        # Contar docentes
        num_docentes = len(linea.docentes)
        
        # Contar cursos
        num_cursos = len(linea.cursos)
        
        return jsonify({
            'success': True,
            'data': {
                'linea': linea_investigacion_schema.dump(linea),
                'estadisticas': {
                    'num_docentes': num_docentes,
                    'num_cursos': num_cursos
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 