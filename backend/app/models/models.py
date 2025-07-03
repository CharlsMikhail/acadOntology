from app import db
from sqlalchemy import Table, UniqueConstraint

# =============================================
# TABLAS DE RELACIONES MANY-TO-MANY
# =============================================

docentes_lineas_investigacion = Table('docentes_lineas_investigacion', db.Model.metadata,
    db.Column('docente_id', db.Integer, db.ForeignKey('docentes.id'), primary_key=True),
    db.Column('linea_investigacion_id', db.Integer, db.ForeignKey('lineas_investigacion.id'), primary_key=True)
)

cursos_lineas_investigacion = Table('cursos_lineas_investigacion', db.Model.metadata,
    db.Column('curso_id', db.Integer, db.ForeignKey('cursos.id'), primary_key=True),
    db.Column('linea_investigacion_id', db.Integer, db.ForeignKey('lineas_investigacion.id'), primary_key=True)
)

docentes_producciones_academicas = Table('docentes_producciones_academicas', db.Model.metadata,
    db.Column('docente_id', db.Integer, db.ForeignKey('docentes.id'), primary_key=True),
    db.Column('produccion_academica_id', db.Integer, db.ForeignKey('producciones_academicas.id'), primary_key=True)
)

# =============================================
# TABLAS PRINCIPALES
# =============================================

class Area(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    
    # Relaciones
    lineas_investigacion = db.relationship('LineaInvestigacion', backref='area', lazy=True)
    cursos = db.relationship('Curso', backref='area', lazy=True)

class LineaInvestigacion(db.Model):
    __tablename__ = 'lineas_investigacion'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    
    # Relaciones (muchos a muchos)
    docentes = db.relationship('Docente', secondary=docentes_lineas_investigacion, back_populates='lineas_investigacion')
    cursos = db.relationship('Curso', secondary=cursos_lineas_investigacion, back_populates='lineas_investigacion')

class PeriodoAcademico(db.Model):
    __tablename__ = 'periodos_academicos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.Text)
    
    __table_args__ = (UniqueConstraint('anio', 'semestre', name='_anio_semestre_uc'),)
    
    # Relaciones
    asignaciones = db.relationship('AsignacionDocente', backref='periodo_academico', lazy=True)

class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    creditos = db.Column(db.Integer, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    
    # Relaciones
    asignaciones = db.relationship('AsignacionDocente', backref='curso', lazy=True)
    lineas_investigacion = db.relationship('LineaInvestigacion', secondary=cursos_lineas_investigacion, back_populates='cursos')

class Docente(db.Model):
    __tablename__ = 'docentes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    titulo = db.Column(db.String(20))
    email = db.Column(db.String(255), unique=True)
    grado_academico = db.Column(db.String(255))
    especialidad = db.Column(db.String(255))
    orcid = db.Column(db.String(50))
    
    # Relaciones
    lineas_investigacion = db.relationship('LineaInvestigacion', secondary=docentes_lineas_investigacion, back_populates='docentes')
    asignaciones = db.relationship('AsignacionDocente', backref='docente', lazy=True)
    producciones_academicas = db.relationship('ProduccionAcademica', secondary=docentes_producciones_academicas, back_populates='autores')
    disponibilidades = db.relationship('DisponibilidadHoraria', backref='docente', lazy=True)

class DisponibilidadHoraria(db.Model):
    __tablename__ = 'disponibilidades_horarias'
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

class AsignacionDocente(db.Model):
    __tablename__ = 'asignaciones_docentes'
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodos_academicos.id'), nullable=False)
    horas_asignadas = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.Text)

class ProduccionAcademica(db.Model):
    __tablename__ = 'producciones_academicas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(500), nullable=False)
    doi = db.Column(db.String(100))
    fecha_publicacion = db.Column(db.Date)
    revista = db.Column(db.String(255))
    anio_publicacion = db.Column(db.Integer)
    
    # Relaciones
    autores = db.relationship('Docente', secondary=docentes_producciones_academicas, back_populates='producciones_academicas')
