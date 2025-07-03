from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD, FOAF, DCTERMS
from app.models.models import (
    Docente, Curso, LineaInvestigacion, PeriodoAcademico, 
    AsignacionDocente, ProduccionAcademica, DisponibilidadHoraria, Area
)
from app import db

class RDFService:
    def __init__(self):
        self.g = Graph()
        self.ns = Namespace("http://cramsoft.org/academico#")
        self.g.bind("acad", self.ns)
        self.g.bind("foaf", FOAF)
        self.g.bind("dcterms", DCTERMS)
        self.g.bind("bibo", Namespace("http://purl.org/ontology/bibo/"))
        
    def generate_rdf_from_database(self):
        """Genera RDF completo desde la base de datos."""
        self.g = Graph()
        # Re-bind namespaces for the new graph
        self.g.bind("acad", self.ns)
        self.g.bind("foaf", FOAF)
        self.g.bind("dcterms", DCTERMS)
        self.g.bind("bibo", Namespace("http://purl.org/ontology/bibo/"))
        
        # Generar RDF para cada entidad
        self._generate_areas_rdf()
        self._generate_lineas_investigacion_rdf()
        self._generate_periodos_academicos_rdf()
        self._generate_cursos_rdf()
        self._generate_docentes_rdf()
        self._generate_disponibilidades_horarias_rdf()
        self._generate_producciones_academicas_rdf()
        self._generate_asignaciones_docentes_rdf()
        
        return self.g
    
    def _generate_areas_rdf(self):
        """Genera RDF para áreas académicas"""
        for item in Area.query.all():
            uri = URIRef(f"{self.ns}area{item.id}")
            self.g.add((uri, RDF.type, self.ns.Area))
            self.g.add((uri, RDFS.label, Literal(item.nombre)))
            if item.descripcion:
                self.g.add((uri, RDFS.comment, Literal(item.descripcion)))
    
    def _generate_lineas_investigacion_rdf(self):
        """Genera RDF para líneas de investigación"""
        for item in LineaInvestigacion.query.all():
            uri = URIRef(f"{self.ns}linea{item.id}")
            self.g.add((uri, RDF.type, self.ns.LineaInvestigacion))
            self.g.add((uri, RDFS.label, Literal(item.nombre)))
            if item.descripcion:
                self.g.add((uri, RDFS.comment, Literal(item.descripcion)))
            if item.area_id:
                area_uri = URIRef(f"{self.ns}area{item.area_id}")
                self.g.add((uri, self.ns.subAreaDe, area_uri))
    
    def _generate_periodos_academicos_rdf(self):
        """Genera RDF para períodos académicos"""
        for item in PeriodoAcademico.query.all():
            uri = URIRef(f"{self.ns}periodo{item.id}")
            self.g.add((uri, RDF.type, self.ns.PeriodoAcademico))
            self.g.add((uri, RDFS.label, Literal(item.nombre)))
            if item.anio: self.g.add((uri, self.ns.anio, Literal(item.anio, datatype=XSD.integer)))
            if item.semestre: self.g.add((uri, self.ns.semestre, Literal(item.semestre, datatype=XSD.integer)))
            if item.descripcion: self.g.add((uri, RDFS.comment, Literal(item.descripcion)))
    
    def _generate_cursos_rdf(self):
        """Genera RDF para cursos"""
        for item in Curso.query.all():
            uri = URIRef(f"{self.ns}curso{item.id}")
            self.g.add((uri, RDF.type, self.ns.Curso))
            self.g.add((uri, RDFS.label, Literal(item.nombre)))
            if item.codigo: self.g.add((uri, self.ns.codigo, Literal(item.codigo)))
            if item.creditos: self.g.add((uri, self.ns.creditos, Literal(item.creditos, datatype=XSD.integer)))
            if item.area_id:
                area_uri = URIRef(f"{self.ns}area{item.area_id}")
                self.g.add((uri, self.ns.perteneceAArea, area_uri))
            for linea in item.lineas_investigacion:
                linea_uri = URIRef(f"{self.ns}linea{linea.id}")
                self.g.add((uri, self.ns.relacionadoConLinea, linea_uri))
    
    def _generate_docentes_rdf(self):
        """Genera RDF para docentes"""
        for item in Docente.query.all():
            uri = URIRef(f"{self.ns}docente{item.id}")
            self.g.add((uri, RDF.type, self.ns.Docente))
            self.g.add((uri, RDF.type, FOAF.Person))
            self.g.add((uri, FOAF.name, Literal(item.nombre)))
            if item.titulo: self.g.add((uri, FOAF.title, Literal(item.titulo)))
            if item.email: self.g.add((uri, FOAF.mbox, Literal(item.email)))
            if item.grado_academico: self.g.add((uri, self.ns.gradoAcademico, Literal(item.grado_academico)))
            if item.especialidad: self.g.add((uri, self.ns.especialidad, Literal(item.especialidad)))
            if item.orcid: self.g.add((uri, self.ns.orcid, Literal(item.orcid)))
            for linea in item.lineas_investigacion:
                linea_uri = URIRef(f"{self.ns}linea{linea.id}")
                self.g.add((uri, self.ns.perteneceLinea, linea_uri))
    
    def _generate_disponibilidades_horarias_rdf(self):
        """Genera RDF para disponibilidad horaria"""
        for item in DisponibilidadHoraria.query.all():
            uri = URIRef(f"{self.ns}disponibilidad{item.id}")
            docente_uri = URIRef(f"{self.ns}docente{item.docente_id}")
            self.g.add((uri, RDF.type, self.ns.DisponibilidadHoraria))
            self.g.add((uri, RDFS.label, Literal(f"Disponibilidad de {item.docente.nombre}")))
            if item.descripcion: self.g.add((uri, RDFS.comment, Literal(item.descripcion)))
            self.g.add((docente_uri, self.ns.tieneDisponibilidad, uri))
    
    def _generate_producciones_academicas_rdf(self):
        """Genera RDF para producción académica"""
        for item in ProduccionAcademica.query.all():
            uri = URIRef(f"{self.ns}pub{item.id}")
            self.g.add((uri, RDF.type, self.ns.ProduccionAcademica))
            self.g.add((uri, RDF.type, URIRef("http://purl.org/ontology/bibo/Document")))
            if item.titulo: self.g.add((uri, self.ns.titulo, Literal(item.titulo)))
            if item.doi: self.g.add((uri, self.ns.doi, Literal(item.doi)))
            if item.fecha_publicacion: self.g.add((uri, self.ns.fechaPublicacion, Literal(item.fecha_publicacion, datatype=XSD.date)))
            if item.revista: self.g.add((uri, self.ns.revista, Literal(item.revista)))
            if item.anio_publicacion: self.g.add((uri, DCTERMS.date, Literal(item.anio_publicacion, datatype=XSD.gYear)))
            for autor in item.autores:
                autor_uri = URIRef(f"{self.ns}docente{autor.id}")
                self.g.add((autor_uri, self.ns.tieneProduccion, uri))
    
    def _generate_asignaciones_docentes_rdf(self):
        """Genera RDF para asignaciones de docentes"""
        for item in AsignacionDocente.query.all():
            uri = URIRef(f"{self.ns}asignacion{item.id}")
            docente_uri = URIRef(f"{self.ns}docente{item.docente_id}")
            curso_uri = URIRef(f"{self.ns}curso{item.curso_id}")
            periodo_uri = URIRef(f"{self.ns}periodo{item.periodo_id}")
            
            self.g.add((uri, RDF.type, self.ns.AsignacionDocente))
            if item.descripcion:
                self.g.add((uri, RDFS.label, Literal(item.descripcion)))
            
            # Relaciones
            self.g.add((uri, self.ns.asignadoA, docente_uri))
            self.g.add((docente_uri, self.ns.tieneAsignacion, uri)) # Inversa
            self.g.add((uri, self.ns.cursoDictadoEn, curso_uri))
            self.g.add((uri, self.ns.asignadoEn, periodo_uri))
            self.g.add((docente_uri, self.ns.dicta, curso_uri)) # Relación directa Docente-Curso
            
            if item.horas_asignadas:
                self.g.add((uri, self.ns.horasAsignadas, Literal(item.horas_asignadas, datatype=XSD.integer)))
    
    def export_rdf_xml(self):
        """Exporta el grafo RDF en formato XML"""
        return self.g.serialize(format='xml')
    
    def export_rdf_turtle(self):
        """Exporta el grafo RDF en formato Turtle"""
        return self.g.serialize(format='turtle')
    
    def export_rdf_jsonld(self):
        """Exporta el grafo RDF en formato JSON-LD"""
        return self.g.serialize(format='json-ld') 