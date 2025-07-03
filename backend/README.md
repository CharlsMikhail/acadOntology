# API de Ontología Académica

Sistema de gestión académica con ontologías OWL y consultas SPARQL para la gestión de docentes, cursos, líneas de investigación y producción académica.

## Características

- **Registro y gestión de docentes**: nombre, grados académicos, cursos dictados, líneas de investigación, producción académica, disponibilidad horaria
- **Ontologías OWL**: Modelado semántico de entidades como Docente, Curso, Línea de Investigación, Periodo Académico, Asignación Docente
- **Generación automática de RDF**: Direct mapping desde base de datos relacional PostgreSQL
- **Consultas SPARQL**: Consultas semánticas para análisis académico
- **Exportación e interoperabilidad**: Formatos RDF/XML, Turtle y JSON-LD
- **Visualización semántica**: Grafos interactivos de relaciones entre entidades
- **Interoperabilidad con estándares**: FOAF, Dublin Core, BIBO

## Tecnologías

- **Backend**: Flask (Python)
- **Base de datos**: PostgreSQL
- **ORM**: SQLAlchemy
- **Serialización**: Marshmallow
- **RDF**: rdflib
- **SPARQL**: SPARQLWrapper
- **CORS**: Habilitado para cualquier host

## Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd backend
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
Crear archivo `.env` en la raíz del proyecto:
```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/acadontology
SECRET_KEY=tu-clave-secreta-aqui
```

5. **Configurar base de datos PostgreSQL**
```sql
-- Crear base de datos
CREATE DATABASE acadontology;

-- Ejecutar DDL proporcionado
-- (Ver sección de Estructura de Base de Datos)
```

6. **Ejecutar la aplicación**
```bash
python run.py
```

La API estará disponible en `http://localhost:5000`

## Estructura de Base de Datos

### Tablas principales

```sql
-- Tabla: línea de investigación
CREATE TABLE linea_investigacion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla: docente
CREATE TABLE docente (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    grado_academico VARCHAR(50),
    orcid VARCHAR(25),
    correo VARCHAR(100),
    linea_investigacion_id INT REFERENCES linea_investigacion(id)
);

-- Tabla: curso
CREATE TABLE curso (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    linea_investigacion_id INT REFERENCES linea_investigacion(id)
);

-- Tabla: periodo académico
CREATE TABLE periodo_academico (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE
);

-- Tabla: asignación docente
CREATE TABLE asignacion_docente (
    id SERIAL PRIMARY KEY,
    docente_id INT REFERENCES docente(id),
    curso_id INT REFERENCES curso(id),
    periodo_id INT REFERENCES periodo_academico(id),
    horas_asignadas INT
);

-- Tabla: producción académica
CREATE TABLE produccion_academica (
    id SERIAL PRIMARY KEY,
    docente_id INT REFERENCES docente(id),
    tipo VARCHAR(50),
    titulo TEXT NOT NULL,
    anio INT,
    revista TEXT,
    doi TEXT,
    enlace TEXT
);

-- Tabla: disponibilidad horaria
CREATE TABLE disponibilidad_horaria (
    id SERIAL PRIMARY KEY,
    docente_id INT REFERENCES docente(id),
    dia_semana VARCHAR(10),
    hora_inicio TIME,
    hora_fin TIME
);
```

## Endpoints de la API

### 1. Gestión de Docentes
- `GET /api/docentes` - Obtener todos los docentes
- `GET /api/docentes/{id}` - Obtener docente específico
- `POST /api/docentes` - Crear nuevo docente
- `PUT /api/docentes/{id}` - Actualizar docente
- `DELETE /api/docentes/{id}` - Eliminar docente
- `GET /api/docentes/buscar` - Buscar docentes por criterios
- `GET /api/docentes/{id}/perfil-completo` - Perfil completo del docente

### 2. Gestión de Cursos
- `GET /api/cursos` - Obtener todos los cursos
- `GET /api/cursos/{id}` - Obtener curso específico
- `POST /api/cursos` - Crear nuevo curso
- `PUT /api/cursos/{id}` - Actualizar curso
- `DELETE /api/cursos/{id}` - Eliminar curso
- `GET /api/cursos/buscar` - Buscar cursos por criterios
- `GET /api/cursos/por-linea/{linea_id}` - Cursos por línea de investigación

### 3. Gestión de Líneas de Investigación
- `GET /api/lineas-investigacion` - Obtener todas las líneas
- `GET /api/lineas-investigacion/{id}` - Obtener línea específica
- `POST /api/lineas-investigacion` - Crear nueva línea
- `PUT /api/lineas-investigacion/{id}` - Actualizar línea
- `DELETE /api/lineas-investigacion/{id}` - Eliminar línea
- `GET /api/lineas-investigacion/buscar` - Buscar líneas por criterios
- `GET /api/lineas-investigacion/{id}/estadisticas` - Estadísticas de línea

### 4. Gestión de Períodos Académicos
- `GET /api/periodos-academicos` - Obtener todos los períodos
- `GET /api/periodos-academicos/{id}` - Obtener período específico
- `POST /api/periodos-academicos` - Crear nuevo período
- `PUT /api/periodos-academicos/{id}` - Actualizar período
- `DELETE /api/periodos-academicos/{id}` - Eliminar período
- `GET /api/periodos-academicos/buscar` - Buscar períodos por criterios
- `GET /api/periodos-academicos/actual` - Período académico actual

### 5. Gestión de Asignaciones de Docentes
- `GET /api/asignaciones-docentes` - Obtener todas las asignaciones
- `GET /api/asignaciones-docentes/{id}` - Obtener asignación específica
- `POST /api/asignaciones-docentes` - Crear nueva asignación
- `PUT /api/asignaciones-docentes/{id}` - Actualizar asignación
- `DELETE /api/asignaciones-docentes/{id}` - Eliminar asignación
- `GET /api/asignaciones-docentes/por-docente/{docente_id}` - Asignaciones por docente
- `GET /api/asignaciones-docentes/por-periodo/{periodo_id}` - Asignaciones por período
- `GET /api/asignaciones-docentes/carga-horaria/{periodo_id}` - Carga horaria por período

### 6. Gestión de Producción Académica
- `GET /api/produccion-academica` - Obtener toda la producción
- `GET /api/produccion-academica/{id}` - Obtener producción específica
- `POST /api/produccion-academica` - Crear nueva producción
- `PUT /api/produccion-academica/{id}` - Actualizar producción
- `DELETE /api/produccion-academica/{id}` - Eliminar producción
- `GET /api/produccion-academica/por-docente/{docente_id}` - Producción por docente
- `GET /api/produccion-academica/buscar` - Buscar producción por criterios
- `GET /api/produccion-academica/estadisticas` - Estadísticas de producción

### 7. Gestión de Disponibilidad Horaria
- `GET /api/disponibilidad-horaria` - Obtener todas las disponibilidades
- `GET /api/disponibilidad-horaria/{id}` - Obtener disponibilidad específica
- `POST /api/disponibilidad-horaria` - Crear nueva disponibilidad
- `PUT /api/disponibilidad-horaria/{id}` - Actualizar disponibilidad
- `DELETE /api/disponibilidad-horaria/{id}` - Eliminar disponibilidad
- `GET /api/disponibilidad-horaria/por-docente/{docente_id}` - Disponibilidad por docente
- `GET /api/disponibilidad-horaria/buscar` - Buscar disponibilidades por criterios
- `GET /api/disponibilidad-horaria/horario-semanal/{docente_id}` - Horario semanal del docente

### 8. Consultas SPARQL
- `POST /api/sparql/query` - Ejecutar consulta SPARQL personalizada
- `GET /api/sparql/docentes-por-area` - Docentes por área de conocimiento
- `GET /api/sparql/cursos-por-linea` - Cursos por línea de investigación
- `GET /api/sparql/carga-horaria-periodo` - Carga horaria por período
- `GET /api/sparql/produccion-docente/{docente_id}` - Producción de docente
- `GET /api/sparql/disponibilidad-docente/{docente_id}` - Disponibilidad de docente
- `GET /api/sparql/lineas-investigacion-docentes` - Docentes por línea de investigación
- `GET /api/sparql/consultas-predefinidas` - Lista de consultas predefinidas

### 9. Exportación RDF
- `POST /api/rdf/generate` - Generar RDF completo
- `GET /api/rdf/export/xml` - Exportar RDF en formato XML
- `GET /api/rdf/export/turtle` - Exportar RDF en formato Turtle
- `GET /api/rdf/export/jsonld` - Exportar RDF en formato JSON-LD
- `GET /api/rdf/docente/{docente_id}/perfil` - Exportar perfil de docente en RDF
- `GET /api/rdf/estadisticas` - Estadísticas del RDF generado
- `GET /api/rdf/formats` - Formatos de exportación disponibles

### 10. Visualización Semántica
- `GET /api/visualizacion/grafo-completo` - Grafo completo de relaciones
- `GET /api/visualizacion/grafo-docente/{docente_id}` - Grafo de relaciones de docente
- `GET /api/visualizacion/estadisticas-grafo` - Estadísticas del grafo
- `GET /api/visualizacion/tipos-nodos` - Tipos de nodos disponibles
- `GET /api/visualizacion/tipos-relaciones` - Tipos de relaciones disponibles

## Consultas SPARQL Ejemplo

### 1. Docentes por área de conocimiento
```sparql
PREFIX acad: <http://cramsoft.org/ontologia#acad#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT DISTINCT ?docente ?nombre ?grado
WHERE {
    ?docente a acad:Docente ;
            foaf:name ?nombre .
    OPTIONAL { ?docente acad:gradoAcademico ?grado }
    ?docente acad:dicta ?curso .
    ?curso acad:relacionadoConLinea ?linea .
    ?linea rdfs:label ?lineaNombre .
    FILTER(CONTAINS(LCASE(?lineaNombre), "inteligencia artificial"))
}
```

### 2. Carga horaria por período
```sparql
PREFIX acad: <http://cramsoft.org/ontologia#acad#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?docente ?nombre ?totalHoras
WHERE {
    ?docente a acad:Docente ;
            foaf:name ?nombre .
    ?asignacion a acad:AsignacionDocente ;
               acad:asignadoEn ?periodo ;
               acad:horasAsignadas ?horas .
    ?periodo acad:nombre "2025-I" .
    
    {
        SELECT ?docente (SUM(?horas) AS ?totalHoras)
        WHERE {
            ?docente a acad:Docente .
            ?asignacion a acad:AsignacionDocente ;
                       acad:asignadoEn ?periodo ;
                       acad:horasAsignadas ?horas .
            ?periodo acad:nombre "2025-I" .
        }
        GROUP BY ?docente
    }
}
ORDER BY DESC(?totalHoras)
```

## Ontología OWL

La ontología utiliza los siguientes namespaces:
- **acad**: `http://cramsoft.org/ontologia#acad#` (Ontología principal)
- **foaf**: `http://xmlns.com/foaf/0.1/` (Friend of a Friend)
- **dcterms**: `http://purl.org/dc/terms/` (Dublin Core)
- **bibo**: `http://purl.org/ontology/bibo/` (Bibliographic Ontology)

### Clases principales:
- `acad:Docente` (subclase de `foaf:Person`)
- `acad:Curso`
- `acad:LineaInvestigacion`
- `acad:PeriodoAcademico`
- `acad:AsignacionDocente`
- `acad:ProduccionAcademica` (subclase de `bibo:Document`)
- `acad:DisponibilidadHoraria`

### Propiedades principales:
- `acad:dicta` (Docente → Curso)
- `acad:perteneceLinea` (Docente → LineaInvestigacion)
- `acad:relacionadoConLinea` (Curso → LineaInvestigacion)
- `acad:asignadoEn` (AsignacionDocente → PeriodoAcademico)
- `acad:tieneProduccion` (Docente → ProduccionAcademica)
- `acad:gradoAcademico` (datatype property)
- `acad:orcid` (datatype property)
- `acad:horasAsignadas` (datatype property)

## Ejemplos de Uso

### 1. Crear un docente
```bash
curl -X POST http://localhost:5000/api/docentes \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Dr. Juan Pérez",
    "grado_academico": "Doctorado",
    "orcid": "0000-0001-2345-6789",
    "correo": "juan.perez@universidad.edu",
    "linea_investigacion_id": 1
  }'
```

### 2. Consultar docentes por área
```bash
curl "http://localhost:5000/api/sparql/docentes-por-area?area=Inteligencia%20Artificial"
```

### 3. Exportar RDF en Turtle
```bash
curl -o acadontology.ttl http://localhost:5000/api/rdf/export/turtle
```

### 4. Obtener grafo de visualización
```bash
curl http://localhost:5000/api/visualizacion/grafo-completo
```

## Configuración de Apache Jena

Para las consultas SPARQL, se requiere Apache Jena Fuseki:

1. **Descargar Apache Jena Fuseki**
2. **Configurar dataset**:
   - Crear dataset llamado `acadontology`
   - Configurar endpoint en `http://localhost:3030/acadontology/query`

3. **Cargar ontología OWL**:
   - Subir el archivo OWL a través de la interfaz web de Fuseki
   - URL: `http://localhost:3030/#/dataset/acadontology/`

## Desarrollo

### Estructura del proyecto
```
backend/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── models.py
│   ├── routes/
│   │   ├── docente.py
│   │   ├── curso.py
│   │   ├── linea_investigacion.py
│   │   ├── periodo_academico.py
│   │   ├── asignacion_docente.py
│   │   ├── produccion_academica.py
│   │   ├── disponibilidad_horaria.py
│   │   ├── sparql.py
│   │   ├── rdf_export.py
│   │   └── visualizacion.py
│   ├── services/
│   │   ├── rdf_service.py
│   │   └── sparql_service.py
│   └── schemas.py
├── requirements.txt
├── run.py
└── README.md
```

### Agregar nuevos endpoints

1. Crear archivo en `app/routes/`
2. Definir Blueprint
3. Registrar en `app/__init__.py`
4. Documentar en README

### Agregar nuevos modelos

1. Definir modelo en `app/models/models.py`
2. Crear esquema en `app/schemas.py`
3. Actualizar `RDFService` si es necesario
4. Crear endpoints correspondientes

## Licencia

Este proyecto está bajo la Licencia MIT.

## Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Contacto

Para preguntas o soporte, contactar a: [tu-email@dominio.com] 