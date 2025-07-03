from flask import Blueprint, request, jsonify
from app.models.models import Docente, LineaInvestigacion, ProduccionAcademica
from app.schemas import docente_schema, docentes_schema
from app import db
from sqlalchemy.exc import IntegrityError
from app.services.rdf_service import RDFService
import requests

docente_bp = Blueprint('docente', __name__)

JENA_DATA_ENDPOINT = 'http://localhost:3030/acadontology/data'  # Ajusta si tu endpoint es diferente

# --- Utilidad para sincronizar el triple store ---
def sync_triple_store():
    rdf_service = RDFService()
    rdf_xml = rdf_service.generate_rdf_from_database().serialize(format='xml')
    # Borra y sube el nuevo RDF al dataset de Jena
    headers = {'Content-Type': 'application/rdf+xml'}
    requests.post(JENA_DATA_ENDPOINT, data=rdf_xml, headers=headers)

@docente_bp.route('/', methods=['GET'])
def get_docentes():
    """Obtener todos los docentes"""
    try:
        docentes = Docente.query.all()
        return jsonify({
            'success': True,
            'data': docentes_schema.dump(docentes)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@docente_bp.route('/<int:docente_id>', methods=['GET'])
def get_docente(docente_id):
    """Obtener un docente específico"""
    try:
        docente = Docente.query.get_or_404(docente_id)
        return jsonify({
            'success': True,
            'data': docente_schema.dump(docente)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@docente_bp.route('/', methods=['POST'])
def create_docente():
    """Crear un nuevo docente"""
    try:
        data = request.get_json()
        if not data.get('nombre'):
            return jsonify({'success': False, 'error': 'El nombre es requerido'}), 400
        docente = Docente(
            nombre=data['nombre'],
            titulo=data.get('titulo'),
            email=data.get('email'),
            grado_academico=data.get('grado_academico'),
            especialidad=data.get('especialidad'),
            orcid=data.get('orcid')
        )
        # Relaciones muchos a muchos: líneas de investigación
        if data.get('lineas_investigacion_ids'):
            lineas = LineaInvestigacion.query.filter(LineaInvestigacion.id.in_(data['lineas_investigacion_ids'])).all()
            docente.lineas_investigacion = lineas
        # Relaciones muchos a muchos: producción académica
        if data.get('producciones_academicas_ids'):
            producciones = ProduccionAcademica.query.filter(ProduccionAcademica.id.in_(data['producciones_academicas_ids'])).all()
            docente.producciones_academicas = producciones
        db.session.add(docente)
        db.session.commit()
        sync_triple_store()
        return jsonify({'success': True, 'data': docente_schema.dump(docente), 'message': 'Docente creado exitosamente'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Error de integridad en la base de datos'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@docente_bp.route('/<int:docente_id>', methods=['PUT'])
def update_docente(docente_id):
    """Actualizar un docente"""
    try:
        docente = Docente.query.get_or_404(docente_id)
        data = request.get_json()
        if not data.get('nombre'):
            return jsonify({'success': False, 'error': 'El nombre es requerido'}), 400
        docente.nombre = data['nombre']
        docente.titulo = data.get('titulo', docente.titulo)
        docente.email = data.get('email', docente.email)
        docente.grado_academico = data.get('grado_academico', docente.grado_academico)
        docente.especialidad = data.get('especialidad', docente.especialidad)
        docente.orcid = data.get('orcid', docente.orcid)
        # Actualizar relaciones muchos a muchos
        if data.get('lineas_investigacion_ids') is not None:
            lineas = LineaInvestigacion.query.filter(LineaInvestigacion.id.in_(data['lineas_investigacion_ids'])).all()
            docente.lineas_investigacion = lineas
        if data.get('producciones_academicas_ids') is not None:
            producciones = ProduccionAcademica.query.filter(ProduccionAcademica.id.in_(data['producciones_academicas_ids'])).all()
            docente.producciones_academicas = producciones
        db.session.commit()
        sync_triple_store()
        return jsonify({'success': True, 'data': docente_schema.dump(docente), 'message': 'Docente actualizado exitosamente'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Error de integridad en la base de datos'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@docente_bp.route('/<int:docente_id>', methods=['DELETE'])
def delete_docente(docente_id):
    """Eliminar un docente"""
    try:
        docente = Docente.query.get_or_404(docente_id)
        db.session.delete(docente)
        db.session.commit()
        sync_triple_store()
        return jsonify({'success': True, 'message': 'Docente eliminado exitosamente'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'No se puede eliminar el docente porque tiene registros relacionados'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@docente_bp.route('/buscar', methods=['GET'])
def buscar_docentes():
    """Buscar docentes por criterios"""
    try:
        nombre = request.args.get('nombre', '')
        grado = request.args.get('grado', '')
        linea_id = request.args.get('linea_id', '')
        query = Docente.query
        if nombre:
            query = query.filter(Docente.nombre.ilike(f'%{nombre}%'))
        if grado:
            query = query.filter(Docente.grado_academico.ilike(f'%{grado}%'))
        if linea_id:
            query = query.join(Docente.lineas_investigacion).filter(LineaInvestigacion.id == linea_id)
        docentes = query.all()
        return jsonify({'success': True, 'data': docentes_schema.dump(docentes)}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@docente_bp.route('/<int:docente_id>/perfil-completo', methods=['GET'])
def get_perfil_completo(docente_id):
    """Obtener perfil completo de un docente con todas sus relaciones"""
    try:
        docente = Docente.query.get_or_404(docente_id)
        perfil = docente_schema.dump(docente)
        perfil['asignaciones'] = [
            {
                'id': a.id,
                'curso': a.curso.nombre,
                'periodo': a.periodo_academico.nombre,
                'horas_asignadas': a.horas_asignadas
            } for a in docente.asignaciones
        ]
        perfil['producciones_academicas'] = [
            {
                'id': p.id,
                'titulo': p.titulo,
                'doi': p.doi,
                'revista': p.revista,
                'anio_publicacion': p.anio_publicacion
            } for p in docente.producciones_academicas
        ]
        perfil['disponibilidades'] = [
            {
                'id': d.id,
                'descripcion': d.descripcion
            } for d in docente.disponibilidades
        ]
        return jsonify({'success': True, 'data': perfil}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
