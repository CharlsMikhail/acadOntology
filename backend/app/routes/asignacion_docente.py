from flask import Blueprint, request, jsonify
from app.models.models import AsignacionDocente, Docente, Curso, PeriodoAcademico
from app.schemas import asignacion_docente_schema, asignaciones_docentes_schema
from app import db
from sqlalchemy.exc import IntegrityError

asignacion_docente_bp = Blueprint('asignacion_docente', __name__)

@asignacion_docente_bp.route('/', methods=['GET'])
def get_asignaciones():
    """Obtener todas las asignaciones de docentes"""
    try:
        asignaciones = AsignacionDocente.query.all()
        return jsonify({
            'success': True,
            'data': asignaciones_docentes_schema.dump(asignaciones)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@asignacion_docente_bp.route('/<int:asignacion_id>', methods=['GET'])
def get_asignacion(asignacion_id):
    """Obtener una asignación específica"""
    try:
        asignacion = AsignacionDocente.query.get_or_404(asignacion_id)
        return jsonify({
            'success': True,
            'data': asignacion_docente_schema.dump(asignacion)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@asignacion_docente_bp.route('/', methods=['POST'])
def create_asignacion():
    """Crear una nueva asignación de docente"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['docente_id', 'curso_id', 'periodo_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'El campo {field} es requerido'
                }), 400
        
        # Verificar que las entidades relacionadas existan
        docente = Docente.query.get(data['docente_id'])
        if not docente:
            return jsonify({
                'success': False,
                'error': 'El docente no existe'
            }), 400
        
        curso = Curso.query.get(data['curso_id'])
        if not curso:
            return jsonify({
                'success': False,
                'error': 'El curso no existe'
            }), 400
        
        periodo = PeriodoAcademico.query.get(data['periodo_id'])
        if not periodo:
            return jsonify({
                'success': False,
                'error': 'El período académico no existe'
            }), 400
        
        # Crear la asignación
        asignacion = AsignacionDocente(
            docente_id=data['docente_id'],
            curso_id=data['curso_id'],
            periodo_id=data['periodo_id'],
            horas_asignadas=data.get('horas_asignadas', 0)
        )
        
        db.session.add(asignacion)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': asignacion_docente_schema.dump(asignacion),
            'message': 'Asignación creada exitosamente'
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

@asignacion_docente_bp.route('/<int:asignacion_id>', methods=['PUT'])
def update_asignacion(asignacion_id):
    """Actualizar una asignación de docente"""
    try:
        asignacion = AsignacionDocente.query.get_or_404(asignacion_id)
        data = request.get_json()
        
        # Verificar que las entidades relacionadas existan si se van a actualizar
        if data.get('docente_id'):
            docente = Docente.query.get(data['docente_id'])
            if not docente:
                return jsonify({
                    'success': False,
                    'error': 'El docente no existe'
                }), 400
        
        if data.get('curso_id'):
            curso = Curso.query.get(data['curso_id'])
            if not curso:
                return jsonify({
                    'success': False,
                    'error': 'El curso no existe'
                }), 400
        
        if data.get('periodo_id'):
            periodo = PeriodoAcademico.query.get(data['periodo_id'])
            if not periodo:
                return jsonify({
                    'success': False,
                    'error': 'El período académico no existe'
                }), 400
        
        # Actualizar campos
        asignacion.docente_id = data.get('docente_id', asignacion.docente_id)
        asignacion.curso_id = data.get('curso_id', asignacion.curso_id)
        asignacion.periodo_id = data.get('periodo_id', asignacion.periodo_id)
        asignacion.horas_asignadas = data.get('horas_asignadas', asignacion.horas_asignadas)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': asignacion_docente_schema.dump(asignacion),
            'message': 'Asignación actualizada exitosamente'
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

@asignacion_docente_bp.route('/<int:asignacion_id>', methods=['DELETE'])
def delete_asignacion(asignacion_id):
    """Eliminar una asignación de docente"""
    try:
        asignacion = AsignacionDocente.query.get_or_404(asignacion_id)
        db.session.delete(asignacion)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Asignación eliminada exitosamente'
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

@asignacion_docente_bp.route('/por-docente/<int:docente_id>', methods=['GET'])
def get_asignaciones_por_docente(docente_id):
    """Obtener asignaciones de un docente específico"""
    try:
        asignaciones = AsignacionDocente.query.filter_by(docente_id=docente_id).all()
        return jsonify({
            'success': True,
            'data': asignaciones_docentes_schema.dump(asignaciones)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@asignacion_docente_bp.route('/por-periodo/<int:periodo_id>', methods=['GET'])
def get_asignaciones_por_periodo(periodo_id):
    """Obtener asignaciones de un período específico"""
    try:
        asignaciones = AsignacionDocente.query.filter_by(periodo_id=periodo_id).all()
        return jsonify({
            'success': True,
            'data': asignaciones_docentes_schema.dump(asignaciones)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@asignacion_docente_bp.route('/carga-horaria/<int:periodo_id>', methods=['GET'])
def get_carga_horaria_periodo(periodo_id):
    """Obtener carga horaria por docente en un período específico"""
    try:
        from sqlalchemy import func
        
        # Consulta para obtener carga horaria por docente
        carga_horaria = db.session.query(
            Docente.nombre,
            func.sum(AsignacionDocente.horas_asignadas).label('total_horas')
        ).join(
            AsignacionDocente, Docente.id == AsignacionDocente.docente_id
        ).filter(
            AsignacionDocente.periodo_id == periodo_id
        ).group_by(
            Docente.id, Docente.nombre
        ).order_by(
            func.sum(AsignacionDocente.horas_asignadas).desc()
        ).all()
        
        result = []
        for nombre, total_horas in carga_horaria:
            result.append({
                'docente': nombre,
                'total_horas': total_horas
            })
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 