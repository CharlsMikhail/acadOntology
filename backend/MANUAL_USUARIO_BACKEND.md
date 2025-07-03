# Manual de Usuario - Backend

## Descripción General

Este sistema backend permite la gestión académica universitaria, modelando entidades como Docente, Curso, Línea de Investigación, Área, Período Académico, Asignación Docente, Producción Académica y Disponibilidad Horaria. Expone una API REST y endpoints semánticos para interoperabilidad y visualización.

El backend está disponible en: `http://127.0.0.1:5000`

---

## 1. Acceso a la API

Todos los endpoints están bajo el prefijo `/api/`.

Ejemplo de acceso:
```
GET http://127.0.0.1:5000/api/docentes/
```

---

## 2. Gestión de Entidades (CRUD)

### Docentes
- Listar: `GET /api/docentes/`
- Consultar uno: `GET /api/docentes/<id>`
- Crear: `POST /api/docentes/`
- Modificar: `PUT /api/docentes/<id>`
- Eliminar: `DELETE /api/docentes/<id>`
- Buscar: `GET /api/docentes/buscar?nombre=...&grado=...&linea_id=...`
- Perfil completo: `GET /api/docentes/<id>/perfil-completo`

**Ejemplo de creación:**
```json
POST /api/docentes/
{
  "nombre": "Dra. Ana Torres",
  "titulo": "Dra.",
  "email": "ana@uni.edu",
  "grado_academico": "PhD en Ingeniería de Software",
  "especialidad": "Arquitectura de Software",
  "orcid": "0000-0004-1122-3344",
  "lineas_investigacion_ids": [1, 2],
  "producciones_academicas_ids": [3, 4]
}
```

### Áreas, Líneas, Cursos, Períodos, Asignaciones, Producciones, Disponibilidades
- Cada entidad tiene endpoints similares para listar, crear, editar, eliminar y buscar.
- Ver `/api/areas/`, `/api/lineas_investigacion/`, `/api/cursos/`, etc.

---

## 3. Visualización Semántica

- Grafo completo: `GET /api/visualizacion/grafo-completo`
  - Devuelve nodos y relaciones para graficar con vis.js.
- Grafo de docente: `GET /api/visualizacion/grafo-docente/<id>`
- Estadísticas del grafo: `GET /api/visualizacion/estadisticas-grafo`

---

## 4. Consultas SPARQL

- Ejecutar consulta personalizada: `POST /api/sparql/query` (body: `{ "query": "...SPARQL..." }`)
- Consultas predefinidas: `/api/sparql/docentes-por-area`, `/api/sparql/cursos-por-linea`, etc.

---

## 5. Exportación de Perfiles en RDF

- Exportar perfil de docente en RDF/XML: `GET /api/rdf/perfil/docente/<id>/xml`
- Exportar en Turtle: `GET /api/rdf/perfil/docente/<id>/turtle`
- Exportar en JSON-LD: `GET /api/rdf/perfil/docente/<id>/jsonld`

---

## 6. Sincronización con Triple Store (Apache Jena)

- Cada vez que se crea, edita o elimina un docente, el backend actualiza automáticamente el triple store semántico (Apache Jena) para reflejar los cambios.

---

## 7. Notas de Seguridad

- Los endpoints no requieren autenticación por defecto. Se recomienda protegerlos en producción.

---

## 8. Errores y Respuestas

- Todas las respuestas siguen el formato:
```json
{
  "success": true/false,
  "data": ...,
  "error": "..." (si aplica)
}
```

---

## 9. Contacto y Soporte

Para dudas técnicas, contactar al equipo de desarrollo backend. 