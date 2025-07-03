from flask import Blueprint, request, jsonify
from app.services.rdf_service import RDFService
from app.models.models import (
    Docente, Curso, LineaInvestigacion, PeriodoAcademico, 
    AsignacionDocente, ProduccionAcademica, DisponibilidadHoraria
)
from app import db
from sqlalchemy import func
from SPARQLWrapper import SPARQLWrapper, JSON

visualizacion_bp = Blueprint('visualizacion', __name__)
rdf_service = RDFService()

JENA_SPARQL_ENDPOINT = 'http://localhost:3030/acadontology/query'

@visualizacion_bp.route('/grafo-completo', methods=['GET'])
def get_grafo_completo():
    """Obtener grafo completo de relaciones para visualización (usando la base de datos relacional)"""
    try:
        # Obtener todos los datos
        docentes = Docente.query.all()
        cursos = Curso.query.all()
        lineas = LineaInvestigacion.query.all()
        periodos = PeriodoAcademico.query.all()
        asignaciones = AsignacionDocente.query.all()
        producciones = ProduccionAcademica.query.all()
        disponibilidades = DisponibilidadHoraria.query.all()
        
        # Construir nodos
        nodes = []
        edges = []
        
        # Agregar nodos de docentes
        for docente in docentes:
            nodes.append({
                'id': f'docente_{docente.id}',
                'label': docente.nombre,
                'type': 'docente',
                'data': {
                    'grado_academico': docente.grado_academico,
                    'orcid': docente.orcid,
                    'email': docente.email
                }
            })
        
        # Agregar nodos de cursos
        for curso in cursos:
            nodes.append({
                'id': f'curso_{curso.id}',
                'label': curso.nombre,
                'type': 'curso'
            })
        
        # Agregar nodos de líneas de investigación
        for linea in lineas:
            nodes.append({
                'id': f'linea_{linea.id}',
                'label': linea.nombre,
                'type': 'linea_investigacion'
            })
        
        # Agregar nodos de períodos académicos
        for periodo in periodos:
            nodes.append({
                'id': f'periodo_{periodo.id}',
                'label': periodo.nombre,
                'type': 'periodo_academico'
            })
        
        # Agregar relaciones
        # Docente -> Línea de investigación (muchos a muchos)
        for docente in docentes:
            for linea in docente.lineas_investigacion:
                edges.append({
                    'source': f'docente_{docente.id}',
                    'target': f'linea_{linea.id}',
                    'type': 'pertenece_linea'
                })
        # Curso -> Línea de investigación (muchos a muchos)
        for curso in cursos:
            for linea in curso.lineas_investigacion:
                edges.append({
                    'source': f'curso_{curso.id}',
                    'target': f'linea_{linea.id}',
                    'type': 'relacionado_linea'
                })
        # Asignaciones: Docente -> Curso -> Período
        for asignacion in asignaciones:
            edges.append({
                'source': f'docente_{asignacion.docente_id}',
                'target': f'curso_{asignacion.curso_id}',
                'type': 'dicta',
                'data': {
                    'horas_asignadas': asignacion.horas_asignadas
                }
            })
            edges.append({
                'source': f'curso_{asignacion.curso_id}',
                'target': f'periodo_{asignacion.periodo_id}',
                'type': 'asignado_periodo'
            })
        # Producción académica: Docente -> Producción (muchos a muchos)
        for docente in docentes:
            for produccion in docente.producciones_academicas:
                nodes.append({
                    'id': f'produccion_{produccion.id}',
                    'label': produccion.titulo[:50] + '...' if len(produccion.titulo) > 50 else produccion.titulo,
                    'type': 'produccion_academica',
                    'data': {
                        'doi': produccion.doi,
                        'revista': produccion.revista,
                        'anio_publicacion': produccion.anio_publicacion
                    }
                })
                edges.append({
                    'source': f'docente_{docente.id}',
                    'target': f'produccion_{produccion.id}',
                    'type': 'tiene_produccion'
                })
        # Disponibilidad horaria: Docente -> Disponibilidad
        for disponibilidad in disponibilidades:
            nodes.append({
                'id': f'disponibilidad_{disponibilidad.id}',
                'label': disponibilidad.descripcion,
                'type': 'disponibilidad_horaria',
                'data': {
                    'descripcion': disponibilidad.descripcion
                }
            })
            edges.append({
                'source': f'docente_{disponibilidad.docente_id}',
                'target': f'disponibilidad_{disponibilidad.id}',
                'type': 'tiene_disponibilidad'
            })
        return jsonify({
            'success': True,
            'data': {
                'nodes': nodes,
                'edges': edges
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@visualizacion_bp.route('/grafo-docente/<int:docente_id>', methods=['GET'])
def get_grafo_docente(docente_id):
    """Obtener grafo de relaciones para un docente específico"""
    try:
        # Verificar que el docente existe
        docente = Docente.query.get_or_404(docente_id)
        
        nodes = []
        edges = []
        
        # Nodo del docente
        nodes.append({
            'id': f'docente_{docente.id}',
            'label': docente.nombre,
            'type': 'docente',
            'data': {
                'grado_academico': docente.grado_academico,
                'orcid': docente.orcid,
                'correo': docente.correo
            }
        })
        
        # Línea de investigación del docente
        if docente.linea_investigacion_id:
            linea = LineaInvestigacion.query.get(docente.linea_investigacion_id)
            if linea:
                nodes.append({
                    'id': f'linea_{linea.id}',
                    'label': linea.nombre,
                    'type': 'linea_investigacion'
                })
                edges.append({
                    'source': f'docente_{docente.id}',
                    'target': f'linea_{linea.id}',
                    'type': 'pertenece_linea'
                })
        
        # Cursos que dicta
        asignaciones = AsignacionDocente.query.filter_by(docente_id=docente_id).all()
        for asignacion in asignaciones:
            curso = Curso.query.get(asignacion.curso_id)
            if curso:
                nodes.append({
                    'id': f'curso_{curso.id}',
                    'label': curso.nombre,
                    'type': 'curso'
                })
                edges.append({
                    'source': f'docente_{docente.id}',
                    'target': f'curso_{curso.id}',
                    'type': 'dicta',
                    'data': {
                        'horas_asignadas': asignacion.horas_asignadas
                    }
                })
        
        # Producción académica
        producciones = ProduccionAcademica.query.filter_by(docente_id=docente_id).all()
        for produccion in producciones:
            nodes.append({
                'id': f'produccion_{produccion.id}',
                'label': produccion.titulo[:50] + '...' if len(produccion.titulo) > 50 else produccion.titulo,
                'type': 'produccion_academica',
                'data': {
                    'tipo': produccion.tipo,
                    'anio': produccion.anio,
                    'doi': produccion.doi
                }
            })
            edges.append({
                'source': f'docente_{docente.id}',
                'target': f'produccion_{produccion.id}',
                'type': 'tiene_produccion'
            })
        
        # Disponibilidad horaria
        disponibilidades = DisponibilidadHoraria.query.filter_by(docente_id=docente_id).all()
        for disponibilidad in disponibilidades:
            nodes.append({
                'id': f'disponibilidad_{disponibilidad.id}',
                'label': f"{disponibilidad.dia_semana} {disponibilidad.hora_inicio}-{disponibilidad.hora_fin}",
                'type': 'disponibilidad_horaria',
                'data': {
                    'dia_semana': disponibilidad.dia_semana,
                    'hora_inicio': str(disponibilidad.hora_inicio) if disponibilidad.hora_inicio else None,
                    'hora_fin': str(disponibilidad.hora_fin) if disponibilidad.hora_fin else None
                }
            })
            edges.append({
                'source': f'docente_{docente.id}',
                'target': f'disponibilidad_{disponibilidad.id}',
                'type': 'tiene_disponibilidad'
            })
        
        return jsonify({
            'success': True,
            'data': {
                'docente': {
                    'id': docente.id,
                    'nombre': docente.nombre,
                    'grado_academico': docente.grado_academico
                },
                'nodes': nodes,
                'edges': edges
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@visualizacion_bp.route('/estadisticas-grafo', methods=['GET'])
def get_estadisticas_grafo():
    """Obtener estadísticas del grafo para visualización"""
    try:
        # Contar entidades
        total_docentes = Docente.query.count()
        total_cursos = Curso.query.count()
        total_lineas = LineaInvestigacion.query.count()
        total_periodos = PeriodoAcademico.query.count()
        total_asignaciones = AsignacionDocente.query.count()
        total_producciones = ProduccionAcademica.query.count()
        total_disponibilidades = DisponibilidadHoraria.query.count()
        
        # Estadísticas de relaciones
        docentes_con_linea = Docente.query.filter(Docente.linea_investigacion_id.isnot(None)).count()
        cursos_con_linea = Curso.query.filter(Curso.linea_investigacion_id.isnot(None)).count()
        
        # Docentes con más asignaciones
        docentes_mas_asignaciones = db.session.query(
            Docente.nombre,
            func.count(AsignacionDocente.id).label('num_asignaciones')
        ).join(
            AsignacionDocente, Docente.id == AsignacionDocente.docente_id
        ).group_by(
            Docente.id, Docente.nombre
        ).order_by(
            func.count(AsignacionDocente.id).desc()
        ).limit(5).all()
        
        # Líneas con más docentes
        lineas_mas_docentes = db.session.query(
            LineaInvestigacion.nombre,
            func.count(Docente.id).label('num_docentes')
        ).join(
            Docente, LineaInvestigacion.id == Docente.linea_investigacion_id
        ).group_by(
            LineaInvestigacion.id, LineaInvestigacion.nombre
        ).order_by(
            func.count(Docente.id).desc()
        ).limit(5).all()
        
        return jsonify({
            'success': True,
            'data': {
                'entidades': {
                    'total_docentes': total_docentes,
                    'total_cursos': total_cursos,
                    'total_lineas_investigacion': total_lineas,
                    'total_periodos_academicos': total_periodos,
                    'total_asignaciones': total_asignaciones,
                    'total_producciones': total_producciones,
                    'total_disponibilidades': total_disponibilidades
                },
                'relaciones': {
                    'docentes_con_linea': docentes_con_linea,
                    'cursos_con_linea': cursos_con_linea,
                    'porcentaje_docentes_con_linea': round((docentes_con_linea / total_docentes * 100), 2) if total_docentes > 0 else 0,
                    'porcentaje_cursos_con_linea': round((cursos_con_linea / total_cursos * 100), 2) if total_cursos > 0 else 0
                },
                'ranking': {
                    'docentes_mas_asignaciones': [
                        {'nombre': nombre, 'asignaciones': num} 
                        for nombre, num in docentes_mas_asignaciones
                    ],
                    'lineas_mas_docentes': [
                        {'nombre': nombre, 'docentes': num} 
                        for nombre, num in lineas_mas_docentes
                    ]
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@visualizacion_bp.route('/tipos-nodos', methods=['GET'])
def get_tipos_nodos():
    """Obtener tipos de nodos disponibles para la visualización"""
    tipos_nodos = [
        {
            'id': 'docente',
            'nombre': 'Docente',
            'color': '#4CAF50',
            'descripcion': 'Profesores e investigadores'
        },
        {
            'id': 'curso',
            'nombre': 'Curso',
            'color': '#2196F3',
            'descripcion': 'Asignaturas y materias'
        },
        {
            'id': 'linea_investigacion',
            'nombre': 'Línea de Investigación',
            'color': '#FF9800',
            'descripcion': 'Áreas de investigación'
        },
        {
            'id': 'periodo_academico',
            'nombre': 'Período Académico',
            'color': '#9C27B0',
            'descripcion': 'Ciclos académicos'
        },
        {
            'id': 'produccion_academica',
            'nombre': 'Producción Académica',
            'color': '#F44336',
            'descripcion': 'Artículos, libros, ponencias'
        },
        {
            'id': 'disponibilidad_horaria',
            'nombre': 'Disponibilidad Horaria',
            'color': '#607D8B',
            'descripcion': 'Horarios disponibles'
        }
    ]
    
    return jsonify({
        'success': True,
        'data': tipos_nodos
    }), 200

@visualizacion_bp.route('/tipos-relaciones', methods=['GET'])
def get_tipos_relaciones():
    """Obtener tipos de relaciones disponibles para la visualización"""
    tipos_relaciones = [
        {
            'id': 'pertenece_linea',
            'nombre': 'Pertenece a Línea',
            'descripcion': 'Docente pertenece a línea de investigación'
        },
        {
            'id': 'relacionado_linea',
            'nombre': 'Relacionado con Línea',
            'descripcion': 'Curso relacionado con línea de investigación'
        },
        {
            'id': 'dicta',
            'nombre': 'Dicta',
            'descripcion': 'Docente dicta curso'
        },
        {
            'id': 'asignado_periodo',
            'nombre': 'Asignado en Período',
            'descripcion': 'Curso asignado en período académico'
        },
        {
            'id': 'tiene_produccion',
            'nombre': 'Tiene Producción',
            'descripcion': 'Docente tiene producción académica'
        },
        {
            'id': 'tiene_disponibilidad',
            'nombre': 'Tiene Disponibilidad',
            'descripcion': 'Docente tiene disponibilidad horaria'
        }
    ]
    
    return jsonify({
        'success': True,
        'data': tipos_relaciones
    }), 200 