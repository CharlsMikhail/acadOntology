# Documentación de la API de Ontología Académica

## Información General

- **Base URL**: `http://localhost:5000`
- **Versión**: 1.0.0
- **Formato de respuesta**: JSON
- **Autenticación**: No requerida (para desarrollo)

## Estructura de Respuestas

Todas las respuestas siguen el siguiente formato:

```json
{
  "success": true,
  "data": {...},
  "message": "Mensaje opcional"
}
```

En caso de error:

```json
{
  "success": false,
  "error": "Descripción del error"
}
```

## Endpoints

### 1. Gestión de Docentes

#### Obtener todos los docentes
```http
GET /api/docentes
```

**Respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre": "Dr. Juan Pérez",
      "grado_academico": "Doctorado en Ciencias de la Computación",
      "orcid": "0000-0001-2345-6789",
      "correo": "juan.perez@universidad.edu",
      "linea_investigacion_id": 1,
      "linea_investigacion": {
        "id": 1,
        "nombre": "Inteligencia Artificial"
      }
    }
  ]
}
```

#### Obtener docente específico
```http
GET /api/docentes/{id}
```

#### Crear nuevo docente
```http
POST /api/docentes
Content-Type: application/json

{
  "nombre": "Dr. Juan Pérez",
  "grado_academico": "Doctorado en Ciencias de la Computación",
  "orcid": "0000-0001-2345-6789",
  "correo": "juan.perez@universidad.edu",
  "linea_investigacion_id": 1
}
```

#### Actualizar docente
```http
PUT /api/docentes/{id}
Content-Type: application/json

{
  "nombre": "Dr. Juan Pérez Actualizado",
  "grado_academico": "Doctorado en Ciencias de la Computación",
  "orcid": "0000-0001-2345-6789",
  "correo": "juan.perez.actualizado@universidad.edu"
}
```

#### Eliminar docente
```http
DELETE /api/docentes/{id}
```

#### Buscar docentes
```http
GET /api/docentes/buscar?nombre=Juan&grado=Doctorado&linea_id=1
```

#### Perfil completo de docente
```http
GET /api/docentes/{id}/perfil-completo
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "nombre": "Dr. Juan Pérez",
    "grado_academico": "Doctorado en Ciencias de la Computación",
    "orcid": "0000-0001-2345-6789",
    "correo": "juan.perez@universidad.edu",
    "linea_investigacion_id": 1,
    "linea_investigacion": {
      "id": 1,
      "nombre": "Inteligencia Artificial"
    },
    "asignaciones": [
      {
        "id": 1,
        "curso": "Introducción a la Inteligencia Artificial",
        "periodo": "2025-I",
        "horas_asignadas": 4
      }
    ],
    "produccion_academica": [
      {
        "id": 1,
        "titulo": "Aplicación de Redes Neuronales en el Reconocimiento de Patrones",
        "tipo": "Artículo",
        "anio": 2024,
        "doi": "10.1000/ai.2024.001",
        "revista": "Journal of Artificial Intelligence"
      }
    ],
    "disponibilidad_horaria": [
      {
        "id": 1,
        "dia_semana": "Lunes",
        "hora_inicio": "08:00:00",
        "hora_fin": "12:00:00"
      }
    ]
  }
}
```

### 2. Gestión de Cursos

#### Obtener todos los cursos
```http
GET /api/cursos
```

#### Crear nuevo curso
```http
POST /api/cursos
Content-Type: application/json

{
  "nombre": "Introducción a la Inteligencia Artificial",
  "linea_investigacion_id": 1
}
```

#### Cursos por línea de investigación
```http
GET /api/cursos/por-linea/{linea_id}
```

### 3. Gestión de Líneas de Investigación

#### Obtener todas las líneas
```http
GET /api/lineas-investigacion
```

#### Crear nueva línea
```http
POST /api/lineas-investigacion
Content-Type: application/json

{
  "nombre": "Inteligencia Artificial"
}
```

#### Estadísticas de línea
```http
GET /api/lineas-investigacion/{id}/estadisticas
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "linea": {
      "id": 1,
      "nombre": "Inteligencia Artificial"
    },
    "estadisticas": {
      "num_docentes": 2,
      "num_cursos": 3
    }
  }
}
```

### 4. Gestión de Períodos Académicos

#### Obtener todos los períodos
```http
GET /api/periodos-academicos
```

#### Crear nuevo período
```http
POST /api/periodos-academicos
Content-Type: application/json

{
  "nombre": "2025-I",
  "fecha_inicio": "2025-01-15",
  "fecha_fin": "2025-05-30"
}
```

#### Período académico actual
```http
GET /api/periodos-academicos/actual
```

### 5. Gestión de Asignaciones de Docentes

#### Obtener todas las asignaciones
```http
GET /api/asignaciones-docentes
```

#### Crear nueva asignación
```http
POST /api/asignaciones-docentes
Content-Type: application/json

{
  "docente_id": 1,
  "curso_id": 1,
  "periodo_id": 1,
  "horas_asignadas": 4
}
```

#### Asignaciones por docente
```http
GET /api/asignaciones-docentes/por-docente/{docente_id}
```

#### Carga horaria por período
```http
GET /api/asignaciones-docentes/carga-horaria/{periodo_id}
```

**Respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "docente": "Dr. Juan Pérez",
      "total_horas": 7
    },
    {
      "docente": "Dra. María García",
      "total_horas": 7
    }
  ]
}
```

### 6. Gestión de Producción Académica

#### Obtener toda la producción
```http
GET /api/produccion-academica
```

#### Crear nueva producción
```http
POST /api/produccion-academica
Content-Type: application/json

{
  "docente_id": 1,
  "tipo": "Artículo",
  "titulo": "Aplicación de Redes Neuronales en el Reconocimiento de Patrones",
  "anio": 2024,
  "revista": "Journal of Artificial Intelligence",
  "doi": "10.1000/ai.2024.001",
  "enlace": "https://doi.org/10.1000/ai.2024.001"
}
```

#### Producción por docente
```http
GET /api/produccion-academica/por-docente/{docente_id}
```

#### Estadísticas de producción
```http
GET /api/produccion-academica/estadisticas
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "total_producciones": 5,
    "por_tipo": [
      {
        "tipo": "Artículo",
        "cantidad": 3
      },
      {
        "tipo": "Libro",
        "cantidad": 1
      },
      {
        "tipo": "Ponencia",
        "cantidad": 1
      }
    ],
    "por_anio": [
      {
        "anio": 2024,
        "cantidad": 4
      },
      {
        "anio": 2023,
        "cantidad": 1
      }
    ]
  }
}
```

### 7. Gestión de Disponibilidad Horaria

#### Obtener todas las disponibilidades
```http
GET /api/disponibilidad-horaria
```

#### Crear nueva disponibilidad
```http
POST /api/disponibilidad-horaria
Content-Type: application/json

{
  "docente_id": 1,
  "dia_semana": "Lunes",
  "hora_inicio": "08:00",
  "hora_fin": "12:00"
}
```

#### Disponibilidad por docente
```http
GET /api/disponibilidad-horaria/por-docente/{docente_id}
```

#### Horario semanal del docente
```http
GET /api/disponibilidad-horaria/horario-semanal/{docente_id}
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "docente": {
      "id": 1,
      "nombre": "Dr. Juan Pérez"
    },
    "horario_semanal": {
      "Lunes": [
        {
          "id": 1,
          "hora_inicio": "08:00:00",
          "hora_fin": "12:00:00"
        }
      ],
      "Martes": [
        {
          "id": 2,
          "hora_inicio": "14:00:00",
          "hora_fin": "18:00:00"
        }
      ],
      "Miércoles": [],
      "Jueves": [],
      "Viernes": [],
      "Sábado": [],
      "Domingo": []
    }
  }
}
```

### 8. Consultas SPARQL

#### Ejecutar consulta personalizada
```http
POST /api/sparql/query
Content-Type: application/json

{
  "query": "PREFIX acad: <http://cramsoft.org/ontologia#acad#> SELECT ?docente ?nombre WHERE { ?docente a acad:Docente ; foaf:name ?nombre }"
}
```

#### Docentes por área
```http
GET /api/sparql/docentes-por-area?area=Inteligencia%20Artificial
```

#### Cursos por línea de investigación
```http
GET /api/sparql/cursos-por-linea?linea=Machine%20Learning
```

#### Carga horaria por período
```http
GET /api/sparql/carga-horaria-periodo?periodo=2025-I
```

#### Producción de docente
```http
GET /api/sparql/produccion-docente/1
```

#### Disponibilidad de docente
```http
GET /api/sparql/disponibilidad-docente/1
```

#### Docentes por línea de investigación
```http
GET /api/sparql/lineas-investigacion-docentes
```

#### Consultas predefinidas
```http
GET /api/sparql/consultas-predefinidas
```

### 9. Exportación RDF

#### Generar RDF completo
```http
POST /api/rdf/generate
```

#### Exportar RDF en XML
```http
GET /api/rdf/export/xml
```

#### Exportar RDF en Turtle
```http
GET /api/rdf/export/turtle
```

#### Exportar RDF en JSON-LD
```http
GET /api/rdf/export/jsonld
```

#### Exportar perfil de docente en RDF
```http
GET /api/rdf/docente/1/perfil?format=xml
GET /api/rdf/docente/1/perfil?format=turtle
GET /api/rdf/docente/1/perfil?format=jsonld
```

#### Estadísticas del RDF
```http
GET /api/rdf/estadisticas
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "total_triples": 150,
    "entidades": {
      "docentes": 5,
      "cursos": 10,
      "lineas_investigacion": 5,
      "periodos_academicos": 2,
      "asignaciones_docentes": 10,
      "produccion_academica": 5,
      "disponibilidad_horaria": 7
    },
    "namespaces": {
      "acad": "http://cramsoft.org/ontologia#acad#",
      "foaf": "http://xmlns.com/foaf/0.1/",
      "dcterms": "http://purl.org/dc/terms/",
      "bibo": "http://purl.org/ontology/bibo/"
    }
  }
}
```

#### Formatos disponibles
```http
GET /api/rdf/formats
```

### 10. Visualización Semántica

#### Grafo completo
```http
GET /api/visualizacion/grafo-completo
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "nodes": [
      {
        "id": "docente_1",
        "label": "Dr. Juan Pérez",
        "type": "docente",
        "data": {
          "grado_academico": "Doctorado en Ciencias de la Computación",
          "orcid": "0000-0001-2345-6789",
          "correo": "juan.perez@universidad.edu"
        }
      }
    ],
    "edges": [
      {
        "source": "docente_1",
        "target": "linea_1",
        "type": "pertenece_linea"
      }
    ]
  }
}
```

#### Grafo de docente específico
```http
GET /api/visualizacion/grafo-docente/1
```

#### Estadísticas del grafo
```http
GET /api/visualizacion/estadisticas-grafo
```

#### Tipos de nodos
```http
GET /api/visualizacion/tipos-nodos
```

#### Tipos de relaciones
```http
GET /api/visualizacion/tipos-relaciones
```

## Códigos de Estado HTTP

- `200 OK`: Operación exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Error en los datos de entrada
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error interno del servidor

## Ejemplos de Uso con cURL

### Crear un docente
```bash
curl -X POST http://localhost:5000/api/docentes \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Dr. Juan Pérez",
    "grado_academico": "Doctorado en Ciencias de la Computación",
    "orcid": "0000-0001-2345-6789",
    "correo": "juan.perez@universidad.edu",
    "linea_investigacion_id": 1
  }'
```

### Consultar docentes por área
```bash
curl "http://localhost:5000/api/sparql/docentes-por-area?area=Inteligencia%20Artificial"
```

### Exportar RDF en Turtle
```bash
curl -o acadontology.ttl http://localhost:5000/api/rdf/export/turtle
```

### Obtener grafo de visualización
```bash
curl http://localhost:5000/api/visualizacion/grafo-completo
```

## Notas Importantes

1. **CORS**: La API tiene CORS habilitado para cualquier host
2. **Validación**: Todos los endpoints validan los datos de entrada
3. **Relaciones**: Las entidades mantienen integridad referencial
4. **SPARQL**: Requiere Apache Jena Fuseki configurado
5. **RDF**: Se genera automáticamente desde la base de datos relacional

## Configuración de Apache Jena

Para usar las consultas SPARQL:

1. Instalar Apache Jena Fuseki
2. Crear dataset `acadontology`
3. Configurar endpoint en `http://localhost:3030/acadontology/query`
4. Cargar la ontología OWL en Fuseki

## Soporte

Para soporte técnico o preguntas sobre la API, contactar al equipo de desarrollo. 