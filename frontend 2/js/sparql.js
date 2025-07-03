// Datos de prueba para simular la respuesta del backend
const mockData = {
  // Pregunta 1: ¿Qué docentes dictan cursos en el área de Inteligencia Artificial?
  'docentes_ia': {
    success: true,
    data: [
      { docente: { value: 'Dr. Juan Pérez' }, curso: { value: 'IA Avanzada' }, area: { value: 'Inteligencia Artificial' } },
      { docente: { value: 'Dra. Ana López' }, curso: { value: 'Machine Learning' }, area: { value: 'Inteligencia Artificial' } },
      { docente: { value: 'Dr. Carlos Ruiz' }, curso: { value: 'Procesamiento de Lenguaje Natural' }, area: { value: 'Inteligencia Artificial' } }
    ]
  },
  
  // Pregunta 2: ¿Qué cursos están relacionados con una línea de investigación determinada?
  'cursos_linea': {
    success: true,
    data: [
      { curso: { value: 'IA Avanzada' }, linea: { value: 'Aprendizaje Automático' } },
      { curso: { value: 'Machine Learning' }, linea: { value: 'Aprendizaje Profundo' } },
      { curso: { value: 'Procesamiento de Lenguaje Natural' }, linea: { value: 'Lingüística Computacional' } },
      { curso: { value: 'Visión por Computadora' }, linea: { value: 'Procesamiento de Imágenes' } }
    ]
  },
  
  // Pregunta 3: ¿Qué docentes tienen más carga horaria en un periodo académico?
  'carga_horaria': {
    success: true,
    data: [
      { docente: { value: 'Dr. Juan Pérez' }, horas: { value: '20', type: 'literal', datatype: 'http://www.w3.org/2001/XMLSchema#integer' }, periodo: { value: '2025-I' } },
      { docente: { value: 'Dra. Ana López' }, horas: { value: '18', type: 'literal', datatype: 'http://www.w3.org/2001/XMLSchema#integer' }, periodo: { value: '2025-I' } },
      { docente: { value: 'Dr. Carlos Ruiz' }, horas: { value: '15', type: 'literal', datatype: 'http://www.w3.org/2001/XMLSchema#integer' }, periodo: { value: '2025-I' } },
      { docente: { value: 'MSc. Laura García' }, horas: { value: '12', type: 'literal', datatype: 'http://www.w3.org/2001/XMLSchema#integer' }, periodo: { value: '2025-I' } }
    ]
  },
  
  // Datos para visualización de grafo
  grafo: {
    success: true,
    data: {
      nodes: [
        { id: 'd1', label: 'Dr. Juan Pérez', type: 'docente', data: { email: 'juan@example.com' } },
        { id: 'd2', label: 'Dra. Ana López', type: 'docente', data: { email: 'ana@example.com' } },
        { id: 'd3', label: 'Dr. Carlos Ruiz', type: 'docente', data: { email: 'carlos@example.com' } },
        { id: 'c1', label: 'IA Avanzada', type: 'curso', data: { creditos: 4 } },
        { id: 'c2', label: 'Machine Learning', type: 'curso', data: { creditos: 3 } },
        { id: 'c3', label: 'Procesamiento de Lenguaje Natural', type: 'curso', data: { creditos: 3 } },
        { id: 'l1', label: 'Aprendizaje Automático', type: 'linea_investigacion' },
        { id: 'l2', label: 'Aprendizaje Profundo', type: 'linea_investigacion' },
        { id: 'l3', label: 'Lingüística Computacional', type: 'linea_investigacion' },
        { id: 'p1', label: '2025-I', type: 'periodo_academico' }
      ],
      edges: [
        // Docentes que imparten cursos
        { source: 'd1', target: 'c1', type: 'imparte', data: { horas: 6 } },
        { source: 'd2', target: 'c2', type: 'imparte', data: { horas: 4 } },
        { source: 'd3', target: 'c3', type: 'imparte', data: { horas: 4 } },
        
        // Cursos relacionados con líneas de investigación
        { source: 'c1', target: 'l1', type: 'pertenece_a' },
        { source: 'c2', target: 'l2', type: 'pertenece_a' },
        { source: 'c3', target: 'l3', type: 'pertenece_a' },
        
        // Docentes activos en periodo
        { source: 'd1', target: 'p1', type: 'activo_en' },
        { source: 'd2', target: 'p1', type: 'activo_en' },
        { source: 'd3', target: 'p1', type: 'activo_en' }
      ]
    }
  }
};

// Consultas SPARQL
const USE_MOCK = true; // Cambiar a false para usar el backend real
const endpoint = 'http://localhost:5000/api/sparql';

// Consultas de ejemplo
const CONSULTAS_EJEMPLO = {
  docentes_ia: {
    titulo: 'Docentes de Inteligencia Artificial',
    query: 'PREFIX : <http://cramsoft.org/academico#>\n' +
           'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n' +
           'SELECT ?docente ?curso ?area WHERE {\n' +
           '  ?d rdf:type :Docente .\n' +
           '  ?d :nombre ?docente .\n' +
           '  ?a :asignadoA ?d .\n' +
           '  ?a :asignadoEnCurso ?c .\n' +
           '  ?c :nombre ?curso .\n' +
           '  ?c :perteneceA ?areaObj .\n' +
           '  ?areaObj :nombre ?area .\n' +
           '  FILTER(REGEX(?area, "Inteligencia Artificial", "i"))\n' +
           '}'
  },
  cursos_linea: {
    titulo: 'Cursos por línea de investigación',
    query: 'PREFIX : <http://cramsoft.org/academico#>\n' +
           'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n' +
           'SELECT ?curso ?linea WHERE {\n' +
           '  ?c rdf:type :Curso .\n' +
           '  ?c :nombre ?curso .\n' +
           '  ?c :perteneceA ?l .\n' +
           '  ?l :nombre ?linea .\n' +
           '} ORDER BY ?linea ?curso'
  },
  carga_horaria: {
    titulo: 'Carga horaria por docente',
    query: 'PREFIX : <http://cramsoft.org/academico#>\n' +
           'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n' +
           'PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n' +
           'SELECT ?docente (SUM(xsd:integer(?horas)) as ?totalHoras) ?periodo WHERE {\n' +
           '  ?a rdf:type :AsignacionDocente .\n' +
           '  ?a :asignadoA ?d .\n' +
           '  ?d :nombre ?docente .\n' +
           '  ?a :horasAsignadas ?horas .\n' +
           '  ?a :asignadoEn ?p .\n' +
           '  ?p :nombre ?periodo .\n' +
           '} GROUP BY ?docente ?periodo ORDER BY DESC(?totalHorasa)'
  },
  grafo: {
    titulo: 'Grafo completo',
    query: 'CONSTRUCT {\n' +
           '  ?s ?p ?o .\n' +
           '} WHERE {\n' +
           '  ?s ?p ?o .\n' +
           '} LIMIT 100'
  }
};

// Función para cargar una consulta de ejemplo
function cargarConsultaEjemplo(tipo) {
  const consulta = CONSULTAS_EJEMPLO[tipo];
  if (consulta) {
    document.getElementById('sparql-query').value = consulta.query;
    // Ejecutar automáticamente
    ejecutarConsultaSparql();
  }
}
document.getElementById('btn-ejecutar-sparql').onclick = ejecutarConsultaSparql;
document.getElementById('btn-predefinida').onclick = () => {
  document.getElementById('sparql-query').value = `PREFIX : <http://cramsoft.org/academico#>\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nPREFIX foaf: <http://xmlns.com/foaf/0.1/>\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n\nSELECT ?nombreDocente (SUM(xsd:integer(?horas)) AS ?totalHoras)\nWHERE {\n  ?asignacion rdf:type :AsignacionDocente .\n  ?asignacion :asignadoEn ?periodo .\n  ?periodo rdf:type :PeriodoAcademico .\n  ?periodo rdfs:label "2025-I" .\n  ?asignacion :asignadoA ?docente .\n  ?docente rdf:type :Docente .\n  ?docente foaf:name ?nombreDocente .\n  ?asignacion :horasAsignadas ?horas .\n}\nGROUP BY ?docente ?nombreDocente\nORDER BY DESC(?totalHoras)\nLIMIT 1`;
};

function ejecutarConsultaSparql() {
  const query = document.getElementById('sparql-query').value;
  if (!query.trim()) return;
  
  // Mostrar loading
  const resultadoDiv = document.getElementById('sparql-result');
  resultadoDiv.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Cargando...</span></div></div>';
  
  // Usar datos de prueba si está activado el modo mock
  if (USE_MOCK) {
    console.log('Usando datos de prueba (mock)');
    
    // Determinar qué mock usar basado en la consulta
    let mockResponse;
    
    // Pregunta 1: ¿Qué docentes dictan cursos en el área de Inteligencia Artificial?
    if (query.includes('docente') && query.includes('Inteligencia Artificial')) {
      mockResponse = mockData.docentes_ia;
    } 
    // Pregunta 2: ¿Qué cursos están relacionados con una línea de investigación determinada?
    else if (query.includes('curso') && query.includes('línea de investigación')) {
      mockResponse = mockData.cursos_linea;
    }
    // Pregunta 3: ¿Qué docentes tienen más carga horaria en un periodo académico?
    else if (query.includes('carga horaria') || query.includes('horas') && query.includes('periodo')) {
      mockResponse = mockData.carga_horaria;
    }
    // Por defecto, devolver el grafo completo
    else {
      mockResponse = mockData.grafo;
    }
    
    // Simular un pequeño retardo para que parezca real
    return new Promise(resolve => {
      setTimeout(() => resolve(mockResponse), 500);
    });
  }
  
  // Enviar consulta al endpoint /api/sparql con método POST
  return fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: query.trim() })
  })
  .then(r => r.json())
  .then(data => {
    if (!data.success) {
      resultadoDiv.innerHTML = `<div class="alert alert-danger">Error: ${data.error || 'Error desconocido'}</div>`;
      return;
    }
    
    // Mostrar resultados en formato tabla
    const resultados = data.data;
    if (!resultados || resultados.length === 0) {
      resultadoDiv.innerHTML = '<div class="alert alert-info">No se encontraron resultados.</div>';
      return;
    }
    
    // Si los resultados son en formato de grafo (nodos y aristas)
    if (resultados.nodes && resultados.edges) {
      try {
        // Limpiar el contenedor
        resultadoDiv.innerHTML = '';
        
        // Crear un nuevo contenedor para el grafo
        const graphContainer = document.createElement('div');
        graphContainer.id = 'cy-sparql';
        graphContainer.style.height = '500px';
        graphContainer.style.border = '1px solid #ddd';
        graphContainer.style.borderRadius = '4px';
        resultadoDiv.appendChild(graphContainer);
        
        // Preparar datos para Cytoscape
        const nodes = resultados.nodes.map(n => ({
          data: { 
            id: n.id, 
            label: n.label || n.id.split('/').pop().split('#').pop(),
            group: n.type || 'node',
            ...n.data
          }
        }));
        
        const edges = resultados.edges.map((e, i) => ({
          data: {
            id: `e${i}`,
            source: e.source,
            target: e.target,
            label: e.type || 'related',
            ...e.data
          }
        }));
        
        // Renderizar grafo con Cytoscape
        const cy = cytoscape({
          container: graphContainer,
          elements: [...nodes, ...edges],
          style: [
            { selector: 'node', style: {
              'label': 'data(label)',
              'text-valign': 'center',
              'background-color': 'mapData(group, "docente", #1976d2, "curso", #43a047, "linea_investigacion", #fbc02d, "produccion_academica", #e53935, "periodo_academico", #8e24aa, "disponibilidad_horaria", #00838f, #888)',
              'color': '#222',
              'font-size': '13px',
              'width': 35, 'height': 35,
              'text-wrap': 'wrap',
              'text-max-width': '150px'
            }},
            { selector: 'edge', style: {
              'curve-style': 'bezier',
              'target-arrow-shape': 'triangle',
              'width': 2,
              'line-color': '#bbb',
              'target-arrow-color': '#bbb',
              'label': 'data(label)',
              'font-size': '10px',
              'color': '#666',
              'text-rotation': 'autorotate',
              'text-margin-y': -8
            }}
          ],
          layout: { name: 'cose', animate: true }
        });
        
      } catch (err) {
        console.error('Error al renderizar grafo:', err);
        resultadoDiv.innerHTML = `
          <div class="alert alert-warning">
            No se pudo renderizar el grafo. Mostrando datos en bruto:
            <pre class="mt-2 p-2 bg-light" style="max-height: 300px; overflow: auto;">
              ${JSON.stringify(resultados, null, 2)}
            </pre>
          </div>`;
      }
      return;
    }
    
    // Si los resultados son una lista de bindings SPARQL
    if (Array.isArray(resultados)) {
      // Crear tabla con resultados
      if (resultados.length === 0) {
        resultadoDiv.innerHTML = '<div class="alert alert-info">No se encontraron resultados.</div>';
        return;
      }
      
      let html = '<div class="table-responsive"><table class="table table-striped table-bordered"><thead><tr>';
      
      // Encabezados (obtener las variables de la primera fila)
      const vars = Object.keys(resultados[0]);
      vars.forEach(v => { html += `<th>${v}</th>`; });
      html += '</tr></thead><tbody>';
      
      // Filas
      resultados.forEach(row => {
        html += '<tr>';
        vars.forEach(v => { 
          const val = row[v]?.value || '';
          // Si es un URI, convertirlo a enlace
          if (val.startsWith('http')) {
            html += `<td><a href="${val}" target="_blank">${val}</a></td>`;
          } else {
            html += `<td>${val}</td>`;
          }
        });
        html += '</tr>';
      });
      
      html += '</tbody></table></div>';
      resultadoDiv.innerHTML = html;
      return;
    }
    
    // Si no es ninguno de los formatos esperados, mostrar JSON crudo
    resultadoDiv.innerHTML = `
      <div class="alert alert-info">
        <p>Formato de resultados no reconocido. Mostrando datos en bruto:</p>
        <pre class="mt-2 p-2 bg-light" style="max-height: 300px; overflow: auto;">
          ${JSON.stringify(resultados, null, 2)}
        </pre>
      </div>`;
      
  })
  .catch(error => {
    resultadoDiv.innerHTML = `
      <div class="alert alert-danger">
        Error al ejecutar la consulta: ${error.message}
        <button class="btn btn-sm btn-link" onclick="console.error('Error en consulta SPARQL:', ${JSON.stringify(error, Object.getOwnPropertyNames(error))})">
          Ver detalles
        </button>
      </div>`;
    console.error('Error en consulta SPARQL:', error);
  });
}

// Cargar consulta de ejemplo
document.getElementById('btn-ejemplo').addEventListener('click', function() {
  document.getElementById('sparql-query').value = `
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX acad: <http://example.org/acadOntology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# Consulta de ejemplo: Obtener docentes con sus cursos
SELECT DISTINCT ?docente ?nombreDocente ?curso ?nombreCurso WHERE {
  ?docente rdf:type acad:Docente .
  ?docente rdfs:label ?nombreDocente .
  
  # Obtener cursos que imparte el docente
  ?asignacion rdf:type acad:AsignacionDocente .
  ?asignacion acad:tieneDocente ?docente .
  ?asignacion acad:enCurso ?curso .
  
  ?curso rdfs:label ?nombreCurso .
} 
LIMIT 10`;
});

// Ejecutar consulta al presionar Ctrl+Enter
document.getElementById('sparql-query').addEventListener('keydown', function(e) {
  if (e.ctrlKey && e.key === 'Enter') {
    ejecutarConsultaSparql();
  }
});

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
  // Agregar botón para limpiar resultados
  const clearBtn = document.createElement('button');
  clearBtn.className = 'btn btn-outline-secondary btn-sm ms-2';
  clearBtn.innerHTML = '<i class="bi bi-trash"></i> Limpiar';
  clearBtn.onclick = function() {
    document.getElementById('sparql-result').innerHTML = '';
  };
  document.querySelector('.sparql-actions').appendChild(clearBtn);
});
