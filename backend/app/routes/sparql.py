from flask import Blueprint, request, jsonify
from app.services.sparql_service import SPARQLService

sparql_bp = Blueprint('sparql', __name__)
sparql_service = SPARQLService()

@sparql_bp.route('/query', methods=['POST'])
def execute_sparql_query():
    """Ejecutar una consulta SPARQL personalizada"""
    try:
        data = request.get_json()
        
        if not data or not data.get('query'):
            return jsonify({
                'success': False,
                'error': 'La consulta SPARQL es requerida'
            }), 400
        
        query = data['query']
        results = sparql_service._execute_sparql_query(query)
        
        return jsonify({
            'success': True,
            'data': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sparql_bp.route('/docentes-por-area', methods=['GET'])
def query_docentes_por_area():
    """¿Qué docentes dictan cursos en el área de {area}?"""
    try:
        area = request.args.get('area', '')
        
        if not area:
            return jsonify({
                'success': False,
                'error': 'El parámetro "area" es requerido'
            }), 400
        
        results = sparql_service.query_docentes_por_area(area)
        
        return jsonify({
            'success': True,
            'data': results,
            'query': f'Docentes que dictan cursos en el área de {area}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sparql_bp.route('/cursos-por-linea', methods=['GET'])
def query_cursos_por_linea():
    """¿Qué cursos están relacionados con una línea de investigación determinada?"""
    try:
        linea = request.args.get('linea', '')
        
        if not linea:
            return jsonify({
                'success': False,
                'error': 'El parámetro "linea" es requerido'
            }), 400
        
        results = sparql_service.query_cursos_por_linea(linea)
        
        return jsonify({
            'success': True,
            'data': results,
            'query': f'Cursos relacionados con la línea de investigación: {linea}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sparql_bp.route('/carga-horaria-periodo', methods=['GET'])
def query_carga_horaria_periodo():
    """¿Qué docentes tienen más carga horaria en un periodo académico?"""
    try:
        periodo = request.args.get('periodo', '')
        
        if not periodo:
            return jsonify({
                'success': False,
                'error': 'El parámetro "periodo" es requerido'
            }), 400
        
        results = sparql_service.query_docentes_carga_horaria(periodo)
        
        return jsonify({
            'success': True,
            'data': results,
            'query': f'Carga horaria de docentes en el período: {periodo}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sparql_bp.route('/produccion-docente/<int:docente_id>', methods=['GET'])
def query_produccion_docente(docente_id):
    """¿Qué producción académica tiene un docente específico?"""
    try:
        results = sparql_service.query_produccion_academica_docente(docente_id)
        
        return jsonify({
            'success': True,
            'data': results,
            'query': f'Producción académica del docente ID: {docente_id}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sparql_bp.route('/disponibilidad-docente/<int:docente_id>', methods=['GET'])
def query_disponibilidad_docente(docente_id):
    """¿Cuál es la disponibilidad horaria de un docente?"""
    try:
        results = sparql_service.query_disponibilidad_docente(docente_id)
        
        return jsonify({
            'success': True,
            'data': results,
            'query': f'Disponibilidad horaria del docente ID: {docente_id}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sparql_bp.route('/lineas-investigacion-docentes', methods=['GET'])
def query_lineas_investigacion_docentes():
    """¿Cuántos docentes hay por línea de investigación?"""
    try:
        results = sparql_service.query_lineas_investigacion_docentes()
        
        return jsonify({
            'success': True,
            'data': results,
            'query': 'Distribución de docentes por línea de investigación'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@sparql_bp.route('/consultas-predefinidas', methods=['GET'])
def get_consultas_predefinidas():
    """Obtener lista de consultas SPARQL predefinidas"""
    consultas = [
        {
            'id': 'docentes_por_area',
            'nombre': 'Docentes por área',
            'descripcion': '¿Qué docentes dictan cursos en el área de Inteligencia Artificial?',
            'endpoint': '/api/sparql/docentes-por-area?area=Inteligencia Artificial',
            'metodo': 'GET',
            'parametros': ['area']
        },
        {
            'id': 'cursos_por_linea',
            'nombre': 'Cursos por línea de investigación',
            'descripcion': '¿Qué cursos están relacionados con una línea de investigación determinada?',
            'endpoint': '/api/sparql/cursos-por-linea?linea=Machine Learning',
            'metodo': 'GET',
            'parametros': ['linea']
        },
        {
            'id': 'carga_horaria_periodo',
            'nombre': 'Carga horaria por período',
            'descripcion': '¿Qué docentes tienen más carga horaria en un periodo académico?',
            'endpoint': '/api/sparql/carga-horaria-periodo?periodo=2025-I',
            'metodo': 'GET',
            'parametros': ['periodo']
        },
        {
            'id': 'produccion_docente',
            'nombre': 'Producción académica de docente',
            'descripcion': '¿Qué producción académica tiene un docente específico?',
            'endpoint': '/api/sparql/produccion-docente/1',
            'metodo': 'GET',
            'parametros': ['docente_id (en URL)']
        },
        {
            'id': 'disponibilidad_docente',
            'nombre': 'Disponibilidad horaria de docente',
            'descripcion': '¿Cuál es la disponibilidad horaria de un docente?',
            'endpoint': '/api/sparql/disponibilidad-docente/1',
            'metodo': 'GET',
            'parametros': ['docente_id (en URL)']
        },
        {
            'id': 'lineas_investigacion_docentes',
            'nombre': 'Docentes por línea de investigación',
            'descripcion': '¿Cuántos docentes hay por línea de investigación?',
            'endpoint': '/api/sparql/lineas-investigacion-docentes',
            'metodo': 'GET',
            'parametros': []
        },
        {
            'id': 'query_personalizada',
            'nombre': 'Consulta SPARQL personalizada',
            'descripcion': 'Ejecutar una consulta SPARQL personalizada',
            'endpoint': '/api/sparql/query',
            'metodo': 'POST',
            'parametros': ['query (en body JSON)']
        }
    ]
    
    return jsonify({
        'success': True,
        'data': consultas
    }), 200

@sparql_bp.route('/general-query', methods=['GET'])
def general_query():
    """Consulta generalizada por clase, propiedad y valor (por ID o por label)"""
    try:
        clase = request.args.get('clase')  # Ej: 'Curso'
        propiedad = request.args.get('propiedad')  # Ej: 'perteneceAArea'
        valor = request.args.get('valor')  # Ej: 'area2' o 'Ingeniería de Software'
        es_id = request.args.get('es_id', 'true').lower() == 'true'  # Por defecto True
        label_propiedad = request.args.get('label_propiedad')  # Opcional

        if not clase or not propiedad or not valor:
            return jsonify({
                'success': False,
                'error': 'Parámetros requeridos: clase, propiedad, valor'
            }), 400

        results = sparql_service.query_by_property(clase, propiedad, valor, es_id, label_propiedad)
        return jsonify({
            'success': True,
            'data': results,
            'query': f'Consulta generalizada: {clase} filtrado por {propiedad} = {valor} (es_id={es_id})'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 