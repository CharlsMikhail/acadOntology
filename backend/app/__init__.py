from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from dotenv import load_dotenv
from app.utils.cors_config import configure_cors

# Cargar variables de entorno
load_dotenv()

# Inicialización de la app Flask
 
db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    
    # Configuración CORS detallada
    configure_cors(app)
    
    # Configuración de la base de datos desde variables de entorno
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://usuario:password@localhost:5432/acadontology')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Inicializar extensiones
    db.init_app(app)
    ma.init_app(app)

    # Importar y registrar blueprints
    from app.routes.main import main_bp
    from app.routes.docente import docente_bp
    from app.routes.curso import curso_bp
    from app.routes.linea_investigacion import linea_investigacion_bp
    from app.routes.periodo_academico import periodo_academico_bp
    from app.routes.asignacion_docente import asignacion_docente_bp
    from app.routes.produccion_academica import produccion_academica_bp
    from app.routes.disponibilidad_horaria import disponibilidad_horaria_bp
    from app.routes.sparql import sparql_bp
    from app.routes.rdf_export import rdf_export_bp
    from app.routes.visualizacion import visualizacion_bp
    from app.routes.area import area_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(docente_bp, url_prefix='/api/docentes')
    app.register_blueprint(curso_bp, url_prefix='/api/cursos')
    app.register_blueprint(linea_investigacion_bp, url_prefix='/api/lineas-investigacion')
    app.register_blueprint(periodo_academico_bp, url_prefix='/api/periodos-academicos')
    app.register_blueprint(asignacion_docente_bp, url_prefix='/api/asignaciones-docentes')
    app.register_blueprint(produccion_academica_bp, url_prefix='/api/produccion-academica')
    app.register_blueprint(disponibilidad_horaria_bp, url_prefix='/api/disponibilidad-horaria')
    app.register_blueprint(sparql_bp, url_prefix='/api/sparql')
    app.register_blueprint(rdf_export_bp, url_prefix='/api/rdf')
    app.register_blueprint(visualizacion_bp, url_prefix='/api/visualizacion')
    app.register_blueprint(area_bp, url_prefix='/api/areas')

    return app
