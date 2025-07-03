from app import ma
from app.models.models import (
    Docente, Curso, LineaInvestigacion, PeriodoAcademico, 
    AsignacionDocente, ProduccionAcademica, DisponibilidadHoraria, Area
)

class AreaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Area
        include_fk = True
    id = ma.auto_field()
    nombre = ma.auto_field()
    descripcion = ma.auto_field()

class LineaInvestigacionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = LineaInvestigacion
        include_fk = True
    id = ma.auto_field()
    nombre = ma.auto_field()
    descripcion = ma.auto_field()
    area = ma.Nested(AreaSchema, only=("id", "nombre"))

class CursoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Curso
        include_fk = True
    id = ma.auto_field()
    nombre = ma.auto_field()
    codigo = ma.auto_field()
    creditos = ma.auto_field()
    area = ma.Nested(AreaSchema, only=("id", "nombre"))
    lineas_investigacion = ma.Nested(LineaInvestigacionSchema, many=True, only=("id", "nombre"))

class DocenteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Docente
        include_fk = True
    id = ma.auto_field()
    nombre = ma.auto_field()
    titulo = ma.auto_field()
    email = ma.auto_field()
    grado_academico = ma.auto_field()
    especialidad = ma.auto_field()
    orcid = ma.auto_field()
    lineas_investigacion = ma.Nested(LineaInvestigacionSchema, many=True, only=("id", "nombre"))

class PeriodoAcademicoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PeriodoAcademico
        include_fk = True
    id = ma.auto_field()
    nombre = ma.auto_field()
    anio = ma.auto_field()
    semestre = ma.auto_field()
    descripcion = ma.auto_field()

class AsignacionDocenteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = AsignacionDocente
        include_fk = True
    id = ma.auto_field()
    horas_asignadas = ma.auto_field()
    descripcion = ma.auto_field()
    docente = ma.Nested(DocenteSchema, only=("id", "nombre"))
    curso = ma.Nested(CursoSchema, only=("id", "nombre", "codigo"))
    periodo_academico = ma.Nested(PeriodoAcademicoSchema, only=("id", "nombre"))

class ProduccionAcademicaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProduccionAcademica
        include_fk = True
    id = ma.auto_field()
    titulo = ma.auto_field()
    doi = ma.auto_field()
    fecha_publicacion = ma.auto_field()
    revista = ma.auto_field()
    anio_publicacion = ma.auto_field()
    autores = ma.Nested(DocenteSchema, many=True, only=("id", "nombre"))

class DisponibilidadHorariaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = DisponibilidadHoraria
        include_fk = True
    id = ma.auto_field()
    descripcion = ma.auto_field()
    docente = ma.Nested(DocenteSchema, only=("id", "nombre"))

# Instancias de esquemas
area_schema = AreaSchema()
areas_schema = AreaSchema(many=True)
linea_investigacion_schema = LineaInvestigacionSchema()
lineas_investigacion_schema = LineaInvestigacionSchema(many=True)
curso_schema = CursoSchema()
cursos_schema = CursoSchema(many=True)
docente_schema = DocenteSchema()
docentes_schema = DocenteSchema(many=True)
periodo_academico_schema = PeriodoAcademicoSchema()
periodos_academicos_schema = PeriodoAcademicoSchema(many=True)
asignacion_docente_schema = AsignacionDocenteSchema()
asignaciones_docentes_schema = AsignacionDocenteSchema(many=True)
produccion_academica_schema = ProduccionAcademicaSchema()
producciones_academicas_schema = ProduccionAcademicaSchema(many=True)
disponibilidad_horaria_schema = DisponibilidadHorariaSchema()
disponibilidades_horarias_schema = DisponibilidadHorariaSchema(many=True) 