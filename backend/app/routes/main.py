from flask import Blueprint, jsonify
from app import db
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal de la API"""
    return {
        'message': 'API de Ontología Académica',
        'version': '1.0.0',
        'description': 'Sistema de gestión académica con ontologías OWL y consultas SPARQL',
        'endpoints': {
            'docentes': '/api/docentes',
            'cursos': '/api/cursos',
            'lineas_investigacion': '/api/lineas-investigacion',
            'periodos_academicos': '/api/periodos-academicos',
            'asignaciones_docentes': '/api/asignaciones-docentes',
            'produccion_academica': '/api/produccion-academica',
            'disponibilidad_horaria': '/api/disponibilidad-horaria',
            'sparql': '/api/sparql',
            'rdf_export': '/api/rdf',
            'visualizacion': '/api/visualizacion'
        },
        'documentation': {
            'swagger': '/swagger',
            'redoc': '/redoc'
        }
    }

@main_bp.route('/health')
def health_check():
    """Verificación de salud de la API"""
    try:
        # Verificar conexión a la base de datos
        db.session.execute('SELECT 1')
        return {
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }, 500 