from flask import Blueprint, request, jsonify
from app.models.models import Curso, LineaInvestigacion
from app.schemas import curso_schema, cursos_schema
from app import db
from sqlalchemy.exc import IntegrityError

curso_bp = Blueprint('curso', __name__)

@curso_bp.route('/', methods=['GET'])
def get_cursos():
    """Obtener todos los cursos"""
    try:
        cursos = Curso.query.all()
        return jsonify({
            'success': True,
            'data': cursos_schema.dump(cursos)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@curso_bp.route('/<int:curso_id>', methods=['GET'])
def get_curso(curso_id):
    """Obtener un curso específico"""
    try:
        curso = Curso.query.get_or_404(curso_id)
        return jsonify({
            'success': True,
            'data': curso_schema.dump(curso)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@curso_bp.route('/', methods=['POST'])
def create_curso():
    """Crear un nuevo curso"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        
        # Verificar si la línea de investigación existe
        if data.get('linea_investigacion_id'):
            linea = LineaInvestigacion.query.get(data['linea_investigacion_id'])
            if not linea:
                return jsonify({
                    'success': False,
                    'error': 'La línea de investigación no existe'
                }), 400
        
        # Crear el curso
        curso = Curso(
            nombre=data['nombre'],
            linea_investigacion_id=data.get('linea_investigacion_id')
        )
        
        db.session.add(curso)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': curso_schema.dump(curso),
            'message': 'Curso creado exitosamente'
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

@curso_bp.route('/<int:curso_id>', methods=['PUT'])
def update_curso(curso_id):
    """Actualizar un curso"""
    try:
        curso = Curso.query.get_or_404(curso_id)
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        
        # Verificar si la línea de investigación existe
        if data.get('linea_investigacion_id'):
            linea = LineaInvestigacion.query.get(data['linea_investigacion_id'])
            if not linea:
                return jsonify({
                    'success': False,
                    'error': 'La línea de investigación no existe'
                }), 400
        
        # Actualizar campos
        curso.nombre = data['nombre']
        curso.linea_investigacion_id = data.get('linea_investigacion_id', curso.linea_investigacion_id)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': curso_schema.dump(curso),
            'message': 'Curso actualizado exitosamente'
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

@curso_bp.route('/<int:curso_id>', methods=['DELETE'])
def delete_curso(curso_id):
    """Eliminar un curso"""
    try:
        curso = Curso.query.get_or_404(curso_id)
        db.session.delete(curso)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Curso eliminado exitosamente'
        }), 200
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'No se puede eliminar el curso porque tiene registros relacionados'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@curso_bp.route('/buscar', methods=['GET'])
def buscar_cursos():
    """Buscar cursos por criterios"""
    try:
        nombre = request.args.get('nombre', '')
        linea_id = request.args.get('linea_id', '')
        
        query = Curso.query
        
        if nombre:
            query = query.filter(Curso.nombre.ilike(f'%{nombre}%'))
        if linea_id:
            query = query.filter(Curso.linea_investigacion_id == linea_id)
        
        cursos = query.all()
        
        return jsonify({
            'success': True,
            'data': cursos_schema.dump(cursos)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@curso_bp.route('/por-linea/<int:linea_id>', methods=['GET'])
def get_cursos_por_linea(linea_id):
    """Obtener cursos por línea de investigación"""
    try:
        cursos = Curso.query.filter_by(linea_investigacion_id=linea_id).all()
        return jsonify({
            'success': True,
            'data': cursos_schema.dump(cursos)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 