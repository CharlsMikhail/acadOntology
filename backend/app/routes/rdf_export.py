from flask import Blueprint, request, jsonify, Response
from app.services.rdf_service import RDFService
from app.models.models import Docente
from app import db
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, DCTERMS, XSD

rdf_export_bp = Blueprint('rdf_export', __name__)
rdf_service = RDFService()

@rdf_export_bp.route('/generate', methods=['POST'])
def generate_rdf():
    """Generar RDF completo desde la base de datos"""
    try:
        # Generar RDF desde la base de datos
        graph = rdf_service.generate_rdf_from_database()
        
        return jsonify({
            'success': True,
            'message': 'RDF generado exitosamente',
            'triples_count': len(graph)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@rdf_export_bp.route('/export/xml', methods=['GET'])
def export_rdf_xml():
    """Exportar RDF en formato XML"""
    try:
        # Generar RDF
        rdf_service.generate_rdf_from_database()
        xml_content = rdf_service.export_rdf_xml()
        
        response = Response(xml_content, mimetype='application/rdf+xml')
        response.headers['Content-Disposition'] = 'attachment; filename=acadontology.rdf'
        
        return response
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@rdf_export_bp.route('/export/turtle', methods=['GET'])
def export_rdf_turtle():
    """Exportar RDF en formato Turtle"""
    try:
        # Generar RDF
        rdf_service.generate_rdf_from_database()
        turtle_content = rdf_service.export_rdf_turtle()
        
        response = Response(turtle_content, mimetype='text/turtle')
        response.headers['Content-Disposition'] = 'attachment; filename=acadontology.ttl'
        
        return response
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@rdf_export_bp.route('/export/jsonld', methods=['GET'])
def export_rdf_jsonld():
    """Exportar RDF en formato JSON-LD"""
    try:
        # Generar RDF
        rdf_service.generate_rdf_from_database()
        jsonld_content = rdf_service.export_rdf_jsonld()
        
        response = Response(jsonld_content, mimetype='application/ld+json')
        response.headers['Content-Disposition'] = 'attachment; filename=acadontology.jsonld'
        
        return response
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@rdf_export_bp.route('/docente/<int:docente_id>/perfil', methods=['GET'])
def export_perfil_docente(docente_id):
    """Exportar perfil completo de un docente en formato RDF"""
    try:
        # Verificar que el docente existe
        docente = Docente.query.get_or_404(docente_id)
        
        # Generar RDF específico para el docente
        graph = rdf_service.generate_rdf_from_database()
        
        # Filtrar solo los triples relacionados con el docente
        from rdflib import URIRef
        docente_uri = URIRef(f"{rdf_service.ns}Docente_{docente_id}")
        
        # Obtener todos los triples que involucran al docente
        triples = []
        for s, p, o in graph:
            if s == docente_uri or o == docente_uri:
                triples.append((s, p, o))
        
        # Crear un nuevo grafo solo con los triples del docente
        from rdflib import Graph
        docente_graph = Graph()
        for triple in triples:
            docente_graph.add(triple)
        
        # Agregar los namespaces
        docente_graph.bind("acad", rdf_service.ns)
        docente_graph.bind("foaf", rdf_service.g.namespace_manager.namespaces()[1][1])
        docente_graph.bind("dcterms", rdf_service.g.namespace_manager.namespaces()[2][1])
        
        # Exportar en el formato solicitado
        format_type = request.args.get('format', 'xml')
        
        if format_type == 'turtle':
            content = docente_graph.serialize(format='turtle')
            mimetype = 'text/turtle'
            filename = f'docente_{docente_id}.ttl'
        elif format_type == 'jsonld':
            content = docente_graph.serialize(format='json-ld')
            mimetype = 'application/ld+json'
            filename = f'docente_{docente_id}.jsonld'
        else:  # xml por defecto
            content = docente_graph.serialize(format='xml')
            mimetype = 'application/rdf+xml'
            filename = f'docente_{docente_id}.rdf'
        
        response = Response(content, mimetype=mimetype)
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        return response
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@rdf_export_bp.route('/estadisticas', methods=['GET'])
def get_rdf_statistics():
    """Obtener estadísticas del RDF generado"""
    try:
        # Generar RDF
        graph = rdf_service.generate_rdf_from_database()
        
        # Contar diferentes tipos de entidades
        from rdflib import RDF, URIRef
        
        docentes = len(list(graph.subjects(RDF.type, rdf_service.ns.Docente)))
        cursos = len(list(graph.subjects(RDF.type, rdf_service.ns.Curso)))
        lineas = len(list(graph.subjects(RDF.type, rdf_service.ns.LineaInvestigacion)))
        periodos = len(list(graph.subjects(RDF.type, rdf_service.ns.PeriodoAcademico)))
        asignaciones = len(list(graph.subjects(RDF.type, rdf_service.ns.AsignacionDocente)))
        producciones = len(list(graph.subjects(RDF.type, rdf_service.ns.ProduccionAcademica)))
        disponibilidades = len(list(graph.subjects(RDF.type, rdf_service.ns.DisponibilidadHoraria)))
        
        return jsonify({
            'success': True,
            'data': {
                'total_triples': len(graph),
                'entidades': {
                    'docentes': docentes,
                    'cursos': cursos,
                    'lineas_investigacion': lineas,
                    'periodos_academicos': periodos,
                    'asignaciones_docentes': asignaciones,
                    'produccion_academica': producciones,
                    'disponibilidad_horaria': disponibilidades
                },
                'namespaces': {
                    'acad': str(rdf_service.ns),
                    'foaf': 'http://xmlns.com/foaf/0.1/',
                    'dcterms': 'http://purl.org/dc/terms/',
                    'bibo': 'http://purl.org/ontology/bibo/'
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@rdf_export_bp.route('/formats', methods=['GET'])
def get_available_formats():
    """Obtener formatos de exportación disponibles"""
    formats = [
        {
            'id': 'xml',
            'name': 'RDF/XML',
            'description': 'Formato XML estándar para RDF',
            'mime_type': 'application/rdf+xml',
            'extension': '.rdf',
            'endpoint': '/api/rdf/export/xml'
        },
        {
            'id': 'turtle',
            'name': 'Turtle',
            'description': 'Formato de texto legible para RDF',
            'mime_type': 'text/turtle',
            'extension': '.ttl',
            'endpoint': '/api/rdf/export/turtle'
        },
        {
            'id': 'jsonld',
            'name': 'JSON-LD',
            'description': 'Formato JSON para datos enlazados',
            'mime_type': 'application/ld+json',
            'extension': '.jsonld',
            'endpoint': '/api/rdf/export/jsonld'
        }
    ]
    
    return jsonify({
        'success': True,
        'data': formats
    }), 200

@rdf_export_bp.route('/perfil/docente/<int:docente_id>/xml', methods=['GET'])
def export_docente_rdf_xml(docente_id):
    """Exportar el perfil de un docente en RDF/XML"""
    return _export_docente_rdf(docente_id, 'xml')

@rdf_export_bp.route('/perfil/docente/<int:docente_id>/turtle', methods=['GET'])
def export_docente_rdf_turtle(docente_id):
    """Exportar el perfil de un docente en Turtle"""
    return _export_docente_rdf(docente_id, 'turtle')

@rdf_export_bp.route('/perfil/docente/<int:docente_id>/jsonld', methods=['GET'])
def export_docente_rdf_jsonld(docente_id):
    """Exportar el perfil de un docente en JSON-LD"""
    return _export_docente_rdf(docente_id, 'json-ld')

def _export_docente_rdf(docente_id, fmt):
    docente = Docente.query.get_or_404(docente_id)
    ns = Namespace("http://cramsoft.org/academico#")
    g = Graph()
    g.bind("acad", ns)
    g.bind("foaf", FOAF)
    g.bind("dcterms", DCTERMS)
    g.bind("bibo", Namespace("http://purl.org/ontology/bibo/"))
    # Nodo principal del docente
    docente_uri = URIRef(f"{ns}docente{docente.id}")
    g.add((docente_uri, RDF.type, ns.Docente))
    g.add((docente_uri, RDF.type, FOAF.Person))
    g.add((docente_uri, FOAF.name, Literal(docente.nombre)))
    if docente.titulo:
        g.add((docente_uri, FOAF.title, Literal(docente.titulo)))
    if docente.email:
        g.add((docente_uri, FOAF.mbox, Literal(docente.email)))
    if docente.grado_academico:
        g.add((docente_uri, ns.gradoAcademico, Literal(docente.grado_academico)))
    if docente.especialidad:
        g.add((docente_uri, ns.especialidad, Literal(docente.especialidad)))
    if docente.orcid:
        g.add((docente_uri, ns.orcid, Literal(docente.orcid)))
    # Líneas de investigación
    for linea in docente.lineas_investigacion:
        linea_uri = URIRef(f"{ns}linea{linea.id}")
        g.add((docente_uri, ns.perteneceLinea, linea_uri))
        g.add((linea_uri, RDF.type, ns.LineaInvestigacion))
        g.add((linea_uri, RDFS.label, Literal(linea.nombre)))
    # Producción académica
    for produccion in docente.producciones_academicas:
        prod_uri = URIRef(f"{ns}pub{produccion.id}")
        g.add((docente_uri, ns.tieneProduccion, prod_uri))
        g.add((prod_uri, RDF.type, ns.ProduccionAcademica))
        g.add((prod_uri, RDF.type, URIRef("http://purl.org/ontology/bibo/Document")))
        g.add((prod_uri, ns.titulo, Literal(produccion.titulo)))
        if produccion.doi:
            g.add((prod_uri, ns.doi, Literal(produccion.doi)))
        if produccion.fecha_publicacion:
            g.add((prod_uri, ns.fechaPublicacion, Literal(produccion.fecha_publicacion, datatype=XSD.date)))
        if produccion.revista:
            g.add((prod_uri, ns.revista, Literal(produccion.revista)))
        if produccion.anio_publicacion:
            g.add((prod_uri, DCTERMS.date, Literal(produccion.anio_publicacion, datatype=XSD.gYear)))
    # Disponibilidad horaria
    for disponibilidad in docente.disponibilidades:
        disp_uri = URIRef(f"{ns}disponibilidad{disponibilidad.id}")
        g.add((docente_uri, ns.tieneDisponibilidad, disp_uri))
        g.add((disp_uri, RDF.type, ns.DisponibilidadHoraria))
        g.add((disp_uri, RDFS.label, Literal(disponibilidad.descripcion)))
    # Asignaciones
    for asignacion in docente.asignaciones:
        asig_uri = URIRef(f"{ns}asignacion{asignacion.id}")
        g.add((docente_uri, ns.tieneAsignacion, asig_uri))
        g.add((asig_uri, RDF.type, ns.AsignacionDocente))
        g.add((asig_uri, ns.horasAsignadas, Literal(asignacion.horas_asignadas, datatype=XSD.integer)))
    # Serializar
    rdf_data = g.serialize(format=fmt)
    content_type = {
        'xml': 'application/rdf+xml',
        'turtle': 'text/turtle',
        'json-ld': 'application/ld+json'
    }[fmt]
    return Response(rdf_data, mimetype=content_type) 