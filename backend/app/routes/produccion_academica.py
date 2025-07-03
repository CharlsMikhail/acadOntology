from flask import Blueprint, request, jsonify
from app.models.models import ProduccionAcademica, Docente
from app.schemas import produccion_academica_schema, producciones_academicas_schema
from app import db
from sqlalchemy.exc import IntegrityError

produccion_academica_bp = Blueprint('produccion_academica', __name__)

@produccion_academica_bp.route('/', methods=['GET'])
def get_producciones():
    """Obtener toda la producción académica"""
    try:
        producciones = ProduccionAcademica.query.all()
        return jsonify({
            'success': True,
            'data': producciones_academicas_schema.dump(producciones)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@produccion_academica_bp.route('/<int:produccion_id>', methods=['GET'])
def get_produccion(produccion_id):
    """Obtener una producción académica específica"""
    try:
        produccion = ProduccionAcademica.query.get_or_404(produccion_id)
        return jsonify({
            'success': True,
            'data': produccion_academica_schema.dump(produccion)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@produccion_academica_bp.route('/', methods=['POST'])
def create_produccion():
    """Crear una nueva producción académica"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('titulo'):
            return jsonify({
                'success': False,
                'error': 'El título es requerido'
            }), 400
        
        if not data.get('docente_id'):
            return jsonify({
                'success': False,
                'error': 'El docente_id es requerido'
            }), 400
        
        # Verificar que el docente existe
        docente = Docente.query.get(data['docente_id'])
        if not docente:
            return jsonify({
                'success': False,
                'error': 'El docente no existe'
            }), 400
        
        # Crear la producción académica
        produccion = ProduccionAcademica(
            docente_id=data['docente_id'],
            tipo=data.get('tipo'),
            titulo=data['titulo'],
            anio=data.get('anio'),
            revista=data.get('revista'),
            doi=data.get('doi'),
            enlace=data.get('enlace')
        )
        
        db.session.add(produccion)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': produccion_academica_schema.dump(produccion),
            'message': 'Producción académica creada exitosamente'
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

@produccion_academica_bp.route('/<int:produccion_id>', methods=['PUT'])
def update_produccion(produccion_id):
    """Actualizar una producción académica"""
    try:
        produccion = ProduccionAcademica.query.get_or_404(produccion_id)
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('titulo'):
            return jsonify({
                'success': False,
                'error': 'El título es requerido'
            }), 400
        
        # Verificar que el docente existe si se va a actualizar
        if data.get('docente_id'):
            docente = Docente.query.get(data['docente_id'])
            if not docente:
                return jsonify({
                    'success': False,
                    'error': 'El docente no existe'
                }), 400
        
        # Actualizar campos
        produccion.docente_id = data.get('docente_id', produccion.docente_id)
        produccion.tipo = data.get('tipo', produccion.tipo)
        produccion.titulo = data['titulo']
        produccion.anio = data.get('anio', produccion.anio)
        produccion.revista = data.get('revista', produccion.revista)
        produccion.doi = data.get('doi', produccion.doi)
        produccion.enlace = data.get('enlace', produccion.enlace)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': produccion_academica_schema.dump(produccion),
            'message': 'Producción académica actualizada exitosamente'
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

@produccion_academica_bp.route('/<int:produccion_id>', methods=['DELETE'])
def delete_produccion(produccion_id):
    """Eliminar una producción académica"""
    try:
        produccion = ProduccionAcademica.query.get_or_404(produccion_id)
        db.session.delete(produccion)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Producción académica eliminada exitosamente'
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

@produccion_academica_bp.route('/por-docente/<int:docente_id>', methods=['GET'])
def get_producciones_por_docente(docente_id):
    """Obtener producción académica de un docente específico"""
    try:
        producciones = ProduccionAcademica.query.filter_by(docente_id=docente_id).all()
        return jsonify({
            'success': True,
            'data': producciones_academicas_schema.dump(producciones)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@produccion_academica_bp.route('/buscar', methods=['GET'])
def buscar_producciones():
    """Buscar producción académica por criterios"""
    try:
        titulo = request.args.get('titulo', '')
        tipo = request.args.get('tipo', '')
        anio = request.args.get('anio', '')
        docente_id = request.args.get('docente_id', '')
        
        query = ProduccionAcademica.query
        
        if titulo:
            query = query.filter(ProduccionAcademica.titulo.ilike(f'%{titulo}%'))
        if tipo:
            query = query.filter(ProduccionAcademica.tipo.ilike(f'%{tipo}%'))
        if anio:
            query = query.filter(ProduccionAcademica.anio == int(anio))
        if docente_id:
            query = query.filter(ProduccionAcademica.docente_id == int(docente_id))
        
        producciones = query.all()
        
        return jsonify({
            'success': True,
            'data': producciones_academicas_schema.dump(producciones)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@produccion_academica_bp.route('/estadisticas', methods=['GET'])
def get_estadisticas_produccion():
    """Obtener estadísticas de producción académica"""
    try:
        from sqlalchemy import func
        
        # Total de producciones
        total_producciones = ProduccionAcademica.query.count()
        
        # Producciones por tipo
        producciones_por_tipo = db.session.query(
            ProduccionAcademica.tipo,
            func.count(ProduccionAcademica.id).label('cantidad')
        ).filter(
            ProduccionAcademica.tipo.isnot(None)
        ).group_by(
            ProduccionAcademica.tipo
        ).all()
        
        # Producciones por año
        producciones_por_anio = db.session.query(
            ProduccionAcademica.anio,
            func.count(ProduccionAcademica.id).label('cantidad')
        ).filter(
            ProduccionAcademica.anio.isnot(None)
        ).group_by(
            ProduccionAcademica.anio
        ).order_by(
            ProduccionAcademica.anio.desc()
        ).all()
        
        return jsonify({
            'success': True,
            'data': {
                'total_producciones': total_producciones,
                'por_tipo': [{'tipo': tipo, 'cantidad': cantidad} for tipo, cantidad in producciones_por_tipo],
                'por_anio': [{'anio': anio, 'cantidad': cantidad} for anio, cantidad in producciones_por_anio]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 