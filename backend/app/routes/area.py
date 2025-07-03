from flask import Blueprint, request, jsonify
from app.models.models import Area
from app.schemas import area_schema, areas_schema
from app import db
from sqlalchemy.exc import IntegrityError

area_bp = Blueprint('area', __name__)

@area_bp.route('/', methods=['GET'])
def get_areas():
    """Obtener todas las áreas académicas"""
    try:
        areas = Area.query.all()
        return jsonify({
            'success': True,
            'data': areas_schema.dump(areas)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@area_bp.route('/<int:area_id>', methods=['GET'])
def get_area(area_id):
    """Obtener un área académica específica"""
    try:
        area = Area.query.get_or_404(area_id)
        return jsonify({
            'success': True,
            'data': area_schema.dump(area)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@area_bp.route('/', methods=['POST'])
def create_area():
    """Crear una nueva área académica"""
    try:
        data = request.get_json()
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        area = Area(nombre=data['nombre'], descripcion=data.get('descripcion'))
        db.session.add(area)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': area_schema.dump(area),
            'message': 'Área académica creada exitosamente'
        }), 201
    except IntegrityError:
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

@area_bp.route('/<int:area_id>', methods=['PUT'])
def update_area(area_id):
    """Actualizar un área académica"""
    try:
        area = Area.query.get_or_404(area_id)
        data = request.get_json()
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        area.nombre = data['nombre']
        area.descripcion = data.get('descripcion')
        db.session.commit()
        return jsonify({
            'success': True,
            'data': area_schema.dump(area),
            'message': 'Área académica actualizada exitosamente'
        }), 200
    except IntegrityError:
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

@area_bp.route('/<int:area_id>', methods=['DELETE'])
def delete_area(area_id):
    """Eliminar un área académica"""
    try:
        area = Area.query.get_or_404(area_id)
        db.session.delete(area)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Área académica eliminada exitosamente'
        }), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'No se puede eliminar el área porque tiene registros relacionados'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@area_bp.route('/buscar', methods=['GET'])
def buscar_areas():
    """Buscar áreas académicas por nombre"""
    try:
        nombre = request.args.get('nombre', '')
        query = Area.query
        if nombre:
            query = query.filter(Area.nombre.ilike(f'%{nombre}%'))
        areas = query.all()
        return jsonify({
            'success': True,
            'data': areas_schema.dump(areas)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 