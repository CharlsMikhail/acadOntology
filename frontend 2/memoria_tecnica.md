# Memoria Técnica Descriptiva — acadOntology (Frontend)

## 1. Descripción General

El frontend de acadOntology es una aplicación web desarrollada con HTML5, CSS3 (Bootstrap), y JavaScript puro. Permite la visualización, gestión y consulta de datos académicos mediante una interfaz moderna y fácil de usar.

## 2. Estructura de Archivos

- `index.html`: Página principal y punto de entrada de la SPA.
- `css/styles.css`: Estilos personalizados.
- `js/app.js`: Lógica de navegación y SPA.
- `js/grafo.js`: Visualización de grafos (Cytoscape.js), fallback a árbol HTML y JSON.
- `js/docentes.js`: CRUD y exportación de docentes.
- `js/sparql.js`: Consultas SPARQL y visualización de resultados.

## 3. Tecnologías Utilizadas

- **HTML5**: Estructura de la interfaz.
- **Bootstrap 5**: Componentes visuales y modales.
- **JavaScript ES6**: Lógica de la aplicación, manejo de eventos y peticiones.
- **Cytoscape.js**: Visualización de grafos interactivos.
- **Fetch API**: Comunicación con el backend REST y SPARQL.

## 4. Componentes y Funcionalidades

### a) Visualización de Grafo
- Utiliza Cytoscape.js para mostrar relaciones entre entidades.
- Layout automático, colores por tipo de nodo, etiquetas visibles.
- Si la visualización falla, muestra la estructura en árbol HTML y los datos en JSON.

### b) CRUD de Docentes
- Listado, alta, edición y baja de docentes mediante formularios y modales Bootstrap.
- Exportación de perfil de docente en RDF/XML, Turtle y JSON-LD usando endpoints REST.

### c) Consultas SPARQL
- Editor de consultas y botón para ejecutar.
- Visualización de resultados como grafo o, en caso de error, como árbol/JSON.
- Soporte para consultas predefinidas.

## 5. Integración y Comunicación

- El frontend consume endpoints REST y SPARQL proporcionados por el backend.
- No almacena datos localmente; depende completamente de las APIs del backend.

## 6. Consideraciones de Usabilidad

- Interfaz responsive y amigable.
- Indicadores visuales de carga y errores.
- Navegación tipo SPA sin recarga de página.

## 7. Dependencias Externas

- [Bootstrap 5](https://getbootstrap.com/)
- [Cytoscape.js](https://js.cytoscape.org/)

## 8. Instalación y Despliegue

1. Coloca la carpeta del frontend en el servidor web o abre `index.html` directamente en el navegador.
2. Asegúrate de que el backend esté corriendo y accesible en las URLs configuradas.
3. No requiere instalación de paquetes adicionales.

## 9. Mantenimiento y Extensión

- El código está modularizado por funcionalidad.
- Es sencillo agregar nuevas secciones, endpoints o mejorar la visualización.
- Para cambios mayores, edita los archivos JS correspondientes.

## 10. Autoría

Desarrollado por: [Tu nombre aquí]
Fecha: 2025-07-03
