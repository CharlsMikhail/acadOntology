# Memoria Técnica Descriptiva - Backend

## 1. Introducción

Este documento describe la arquitectura, componentes y decisiones técnicas del backend para la gestión académica universitaria, orientado a interoperabilidad semántica y visualización avanzada.

---

## 2. Arquitectura General

- **Framework:** Flask (Python)
- **ORM:** SQLAlchemy
- **Serialización:** Marshmallow
- **Base de datos:** Relacional (PostgreSQL/MySQL/SQLite, según despliegue)
- **Triple Store:** Apache Jena Fuseki
- **Ontología:** OWL personalizada, extendida con FOAF, DC, BIBO
- **Exportación semántica:** RDF/XML, Turtle, JSON-LD
- **Visualización:** vis.js (consumido por el frontend)

---

## 3. Componentes Principales

### a) Modelos y Esquemas
- Modelos SQLAlchemy para Docente, Curso, Línea de Investigación, Área, Período Académico, Asignación Docente, Producción Académica, Disponibilidad Horaria.
- Relaciones muchos a muchos (docente-línea, curso-línea, docente-producción).
- Esquemas Marshmallow para serialización/deserialización.

### b) API REST
- CRUD completo para todas las entidades.
- Endpoints de búsqueda y perfil completo.
- Endpoints de visualización de grafo y estadísticas.

### c) Integración Semántica
- Servicio RDF (`RDFService`) que genera el grafo RDF a partir de la base de datos relacional (direct mapping).
- Exportación de perfiles de docente en RDF/XML, Turtle y JSON-LD.
- Endpoints SPARQL para consultas semánticas (predefinidas y personalizadas).
- Sincronización automática con Apache Jena tras operaciones CRUD relevantes.

### d) Visualización
- Endpoints que devuelven nodos y relaciones para grafo interactivo (vis.js), usando la base de datos relacional.

---

## 4. Sincronización con Apache Jena

- Cada vez que se crea, edita o elimina un docente, el backend regenera el RDF de toda la base y lo sube al endpoint `/data` de Jena.
- Esto asegura que el triple store siempre refleje el estado actual de la base relacional.
- La integración se realiza mediante HTTP POST con `Content-Type: application/rdf+xml`.

---

## 5. Exportación de Perfiles RDF

- Los endpoints `/api/rdf/perfil/docente/<id>/(xml|turtle|jsonld)` generan un grafo RDF solo con la información del docente solicitado y sus relaciones.
- Se usan los mismos namespaces y URIs definidos en la ontología OWL.

---

## 6. Consultas SPARQL

- El backend expone endpoints para ejecutar consultas SPARQL sobre el triple store.
- Consultas predefinidas y personalizadas permiten responder preguntas académicas complejas.

---

## 7. Decisiones de Diseño

- **Direct Mapping:** Se optó por mapping directo (no R2RML) para mantener la sincronización simple y eficiente.
- **Sincronización global tras CRUD:** Se regenera el RDF completo tras cada cambio relevante para garantizar consistencia.
- **Visualización desacoplada:** El grafo para vis.js se construye desde la base relacional para máxima flexibilidad y performance.
- **Exportación granular:** Los perfiles RDF de docentes se generan bajo demanda, no como parte del dump global.

---

## 8. Seguridad y Despliegue

- El backend no implementa autenticación por defecto (recomendado agregar en producción).
- Puede desplegarse en cualquier entorno compatible con Flask y Python 3.8+.

---

## 9. Futuras Mejoras

- Soporte para R2RML y mapping declarativo.
- Sincronización incremental con Jena.
- Endpoints de exportación RDF para otras entidades.
- Mejoras en la gestión de errores y validación avanzada.

---

## 10. Contacto

Para soporte técnico, contactar al equipo de desarrollo backend. 