# Manual de Usuario — acadOntology (Frontend)

Este manual describe cómo utilizar la interfaz web de acadOntology para la gestión y visualización de información académica.

## Acceso

Abre el archivo `index.html` en tu navegador web preferido o accede a la URL del servidor local si tienes un servidor HTTP corriendo.

---

## Menú Principal

El menú superior permite navegar entre las siguientes secciones:

- **Visualización Grafo**: Muestra un grafo interactivo de docentes, cursos, líneas de investigación, etc.
- **CRUD Docentes**: Permite agregar, editar, eliminar y exportar información de docentes.
- **Consultas SPARQL**: Ejecuta consultas SPARQL sobre el repositorio de datos y visualiza los resultados como grafo.

---

## 1. Visualización del Grafo

- **Propósito**: Permite explorar visualmente las relaciones entre docentes, cursos, líneas de investigación y otros elementos.
- **Interacción**: Puedes hacer zoom, mover nodos y ver etiquetas. Los colores distinguen el tipo de entidad.
- **Leyenda de colores**:
  - Azul: Docentes
  - Verde: Cursos
  - Amarillo: Líneas de investigación
  - Rojo: Producción académica
  - Morado: Períodos académicos
  - Celeste: Disponibilidad horaria
- **Indicadores**:
  - Si hay un error de red o de renderizado, se muestra un árbol jerárquico y los datos en formato JSON.

---

## 2. CRUD Docentes

- **Listado**: Muestra todos los docentes registrados.
- **Agregar Docente**: Haz clic en “Agregar Docente” y completa el formulario. Los campos obligatorios están marcados.
- **Editar Docente**: Haz clic en “Editar” en la fila del docente y modifica los datos.
- **Eliminar Docente**: Haz clic en “Eliminar” y confirma la acción.
- **Exportar Docente**: Haz clic en “Exportar” y elige el formato (RDF/XML, Turtle, JSON-LD) para descargar el perfil del docente.

---

## 3. Consultas SPARQL

- **Consulta libre**: Escribe o pega tu consulta SPARQL en el área de texto y haz clic en “Ejecutar Consulta”.
- **Consulta predefinida**: Haz clic en “Consulta Predefinida” para cargar una consulta de ejemplo.
- **Visualización**: Los resultados se muestran como un grafo interactivo (si es posible) o en formato árbol/JSON.

---

## Recomendaciones

- Usa navegadores modernos (Chrome, Firefox, Edge).
- Si no ves el grafo, revisa la conexión con el backend o recarga la página.
- Para soporte técnico, contacta al desarrollador del frontend.
