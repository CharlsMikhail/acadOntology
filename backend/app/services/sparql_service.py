from SPARQLWrapper import SPARQLWrapper, JSON
import requests
from app.services.rdf_service import RDFService
from app.models.models import Docente, Curso, LineaInvestigacion, AsignacionDocente, PeriodoAcademico
from app import db
from sqlalchemy import func

class SPARQLService:
    def __init__(self):
        self.sparql_endpoint = "http://localhost:3030/acadontology/query"
        self.rdf_service = RDFService()
    
    def query_docentes_por_area(self, area):
        """
        Consulta: ¿Qué docentes dictan cursos en el área de {area}?
        """
        query = f"""
        PREFIX acad: <http://cramsoft.org/academico#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?docente ?nombre ?grado ?orcid
        WHERE {{
            ?docente a acad:Docente ;
                    foaf:name ?nombre .
            OPTIONAL {{ ?docente acad:gradoAcademico ?grado }}
            OPTIONAL {{ ?docente acad:orcid ?orcid }}
            ?docente acad:dicta ?curso .
            ?curso acad:relacionadoConLinea ?linea .
            ?linea rdfs:label ?lineaNombre .
            FILTER(CONTAINS(LCASE(?lineaNombre), LCASE("{area}")))
        }}
        ORDER BY ?nombre
        """
        
        return self._execute_sparql_query(query)
    
    def query_cursos_por_linea(self, linea_investigacion):
        """
        Consulta: ¿Qué cursos están relacionados con una línea de investigación determinada?
        """
        query = f"""
        PREFIX acad: <http://cramsoft.org/academico#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?curso ?nombre ?linea
        WHERE {{
            ?curso a acad:Curso ;
                  acad:nombre ?nombre ;
                  acad:relacionadoConLinea ?linea .
            ?linea rdfs:label ?lineaNombre .
            FILTER(CONTAINS(LCASE(?lineaNombre), LCASE("{linea_investigacion}")))
        }}
        ORDER BY ?nombre
        """
        
        return self._execute_sparql_query(query)
    
    def query_docentes_carga_horaria(self, periodo):
        """
        Consulta: ¿Qué docentes tienen más carga horaria en un periodo académico?
        """
        query = f"""
        PREFIX acad: <http://cramsoft.org/academico#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        SELECT ?docente ?nombre ?totalHoras
        WHERE {{
            ?docente a acad:Docente ;
                    foaf:name ?nombre .
            ?asignacion a acad:AsignacionDocente ;
                       acad:asignadoEn ?periodo ;
                       acad:horasAsignadas ?horas .
            ?periodo acad:nombre ?periodoNombre .
            FILTER(?periodoNombre = "{periodo}")
            
            {{
                SELECT ?docente (SUM(?horas) AS ?totalHoras)
                WHERE {{
                    ?docente a acad:Docente .
                    ?asignacion a acad:AsignacionDocente ;
                               acad:asignadoEn ?periodo ;
                               acad:horasAsignadas ?horas .
                    ?periodo acad:nombre ?periodoNombre .
                    FILTER(?periodoNombre = "{periodo}")
                }}
                GROUP BY ?docente
            }}
        }}
        ORDER BY DESC(?totalHoras)
        """
        
        return self._execute_sparql_query(query)
    
    def query_produccion_academica_docente(self, docente_id):
        """
        Consulta: ¿Qué producción académica tiene un docente específico?
        """
        query = f"""
        PREFIX acad: <http://cramsoft.org/academico#>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX bibo: <http://purl.org/ontology/bibo/>
        
        SELECT ?produccion ?titulo ?tipo ?anio ?doi ?revista
        WHERE {{
            ?docente a acad:Docente .
            FILTER(STRENDS(STR(?docente), "Docente_{docente_id}"))
            ?docente acad:tieneProduccion ?produccion .
            ?produccion dcterms:title ?titulo .
            OPTIONAL {{ ?produccion dcterms:type ?tipo }}
            OPTIONAL {{ ?produccion dcterms:date ?anio }}
            OPTIONAL {{ ?produccion acad:doi ?doi }}
            OPTIONAL {{ ?produccion dcterms:publisher ?revista }}
        }}
        ORDER BY DESC(?anio)
        """
        
        return self._execute_sparql_query(query)
    
    def query_disponibilidad_docente(self, docente_id):
        """
        Consulta: ¿Cuál es la disponibilidad horaria de un docente?
        """
        query = f"""
        PREFIX acad: <http://cramsoft.org/academico#>
        
        SELECT ?disponibilidad ?dia ?horaInicio ?horaFin
        WHERE {{
            ?docente a acad:Docente .
            FILTER(STRENDS(STR(?docente), "Docente_{docente_id}"))
            ?docente acad:tieneDisponibilidad ?disponibilidad .
            ?disponibilidad acad:diaSemana ?dia .
            ?disponibilidad acad:horaInicio ?horaInicio .
            ?disponibilidad acad:horaFin ?horaFin .
        }}
        ORDER BY ?dia ?horaInicio
        """
        
        return self._execute_sparql_query(query)
    
    def query_lineas_investigacion_docentes(self):
        """
        Consulta: ¿Cuántos docentes hay por línea de investigación?
        """
        query = """
        PREFIX acad: <http://cramsoft.org/academico#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?linea ?nombreLinea (COUNT(?docente) AS ?numDocentes)
        WHERE {
            ?linea a acad:LineaInvestigacion ;
                   rdfs:label ?nombreLinea .
            ?docente a acad:Docente ;
                    acad:perteneceLinea ?linea .
        }
        GROUP BY ?linea ?nombreLinea
        ORDER BY DESC(?numDocentes)
        """
        
        return self._execute_sparql_query(query)
    
    def query_by_property(self, clase_objetivo, propiedad, valor, es_id=True, label_propiedad=None):
        """
        Consulta generalizada: Devuelve instancias de una clase objetivo filtradas por una propiedad (por ID o por label).
        - clase_objetivo: nombre de la clase (ej: 'Curso', 'Docente')
        - propiedad: nombre de la propiedad de objeto (ej: 'perteneceAArea', 'relacionadoConLinea')
        - valor: el valor a filtrar (ej: 'area2' o 'Ingeniería de Software')
        - es_id: True si el valor es un ID (ej: area2), False si es un label
        - label_propiedad: nombre de la propiedad de label (ej: 'rdfs:label' o 'acad:nombre')
        """
        ns = "http://cramsoft.org/academico#"
        prefix = "PREFIX acad: <http://cramsoft.org/academico#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nPREFIX foaf: <http://xmlns.com/foaf/0.1/>\n"
        clase_uri = f"acad:{clase_objetivo}"
        prop_uri = f"acad:{propiedad}"
        
        if es_id:
            # Filtrar por URI
            valor_uri = f"acad:{valor}"
            filter_line = f"?instancia {prop_uri} {valor_uri} ."
        else:
            # Filtrar por label
            label_prop = label_propiedad or "rdfs:label"
            filter_line = f"?relacionado {label_prop} \"{valor}\" .\n?instancia {prop_uri} ?relacionado ."
        
        query = f"""
        {prefix}
        SELECT DISTINCT ?instancia ?label
        WHERE {{
            ?instancia a {clase_uri} .
            ?instancia rdfs:label ?label .
            {filter_line}
        }}
        ORDER BY ?label
        """
        return self._execute_sparql_query(query)
    
    def _execute_sparql_query(self, query):
        """
        Ejecuta una consulta SPARQL en el endpoint de Apache Jena
        """
        try:
            sparql = SPARQLWrapper(self.sparql_endpoint)
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            return results
        except Exception as e:
            print(f"Error ejecutando consulta SPARQL: {e}")
            # Fallback a consultas SQL si el endpoint SPARQL no está disponible
            return self._fallback_sql_query(query)
    
    def _fallback_sql_query(self, query):
        """
        Fallback a consultas SQL cuando el endpoint SPARQL no está disponible
        """
        if "docentes dictan cursos en el área" in query or "docentes_por_area" in query:
            # Extraer área de la consulta
            area = query.split('"')[1] if '"' in query else ""
            return self._sql_docentes_por_area(area)
        elif "cursos están relacionados con una línea" in query or "cursos_por_linea" in query:
            linea = query.split('"')[1] if '"' in query else ""
            return self._sql_cursos_por_linea(linea)
        elif "docentes tienen más carga horaria" in query or "carga_horaria" in query:
            periodo = query.split('"')[1] if '"' in query else ""
            return self._sql_docentes_carga_horaria(periodo)
        else:
            return {"results": {"bindings": []}}
    
    def _sql_docentes_por_area(self, area):
        """Consulta SQL equivalente para docentes por área"""
        query = db.session.query(Docente).join(
            AsignacionDocente, Docente.id == AsignacionDocente.docente_id
        ).join(
            Curso, AsignacionDocente.curso_id == Curso.id
        ).join(
            LineaInvestigacion, Curso.linea_investigacion_id == LineaInvestigacion.id
        ).filter(
            LineaInvestigacion.nombre.ilike(f'%{area}%')
        ).distinct().all()
        
        results = []
        for docente in query:
            results.append({
                "docente": {"value": f"http://cramsoft.org/academico#Docente_{docente.id}"},
                "nombre": {"value": docente.nombre},
                "grado": {"value": docente.grado_academico or ""},
                "orcid": {"value": docente.orcid or ""}
            })
        
        return {"results": {"bindings": results}}
    
    def _sql_cursos_por_linea(self, linea):
        """Consulta SQL equivalente para cursos por línea"""
        query = db.session.query(Curso, LineaInvestigacion).join(
            LineaInvestigacion, Curso.linea_investigacion_id == LineaInvestigacion.id
        ).filter(
            LineaInvestigacion.nombre.ilike(f'%{linea}%')
        ).all()
        
        results = []
        for curso, linea_inv in query:
            results.append({
                "curso": {"value": f"http://cramsoft.org/academico#Curso_{curso.id}"},
                "nombre": {"value": curso.nombre},
                "linea": {"value": linea_inv.nombre}
            })
        
        return {"results": {"bindings": results}}
    
    def _sql_docentes_carga_horaria(self, periodo):
        """Consulta SQL equivalente para carga horaria por periodo"""
        query = db.session.query(
            Docente.nombre,
            func.sum(AsignacionDocente.horas_asignadas).label('total_horas')
        ).join(
            AsignacionDocente, Docente.id == AsignacionDocente.docente_id
        ).join(
            PeriodoAcademico, AsignacionDocente.periodo_id == PeriodoAcademico.id
        ).filter(
            PeriodoAcademico.nombre == periodo
        ).group_by(
            Docente.id, Docente.nombre
        ).order_by(
            func.sum(AsignacionDocente.horas_asignadas).desc()
        ).all()
        
        results = []
        for nombre, total_horas in query:
            results.append({
                "docente": {"value": f"http://cramsoft.org/academico#Docente_{nombre}"},
                "nombre": {"value": nombre},
                "totalHoras": {"value": str(total_horas), "datatype": "http://www.w3.org/2001/XMLSchema#integer"}
            })
        
        return {"results": {"bindings": results}} 