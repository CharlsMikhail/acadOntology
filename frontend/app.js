// Configuración de la API
const API_BASE_URL = 'http://localhost:5000/api';

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', () => {
    // Configurar modales
    const modal = new bootstrap.Modal(document.getElementById('docenteModal'), {
        backdrop: 'static',
        keyboard: false
    });

    // Añadir listener para el botón de cerrar
    document.getElementById('docenteModal').addEventListener('hidden.bs.modal', () => {
        clearDocenteForm();
    });

    loadGraph(); // Cargar el grafo automáticamente en el dashboard
    loadDocentes();
    setupEventListeners();
});

// Funciones para manejar loading
function showLoading() {
    const loading = document.getElementById('loading');
    loading.style.display = 'inline-block';
}

function hideLoading() {
    const loading = document.getElementById('loading');
    loading.style.display = 'none';
}

// Consultas predefinidas
const PREDEFINED_QUERIES = {
    'docentes-ia': `PREFIX : <http://cramsoft.org/academico#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT DISTINCT ?nombreDocente
WHERE {
  ?docente rdf:type :Docente .
  ?docente :dicta ?curso .
  ?curso rdf:type :Curso .
  ?curso :relacionadoConLinea ?linea .
  ?linea rdf:type :LineaInvestigacion .
  ?linea rdfs:label "Inteligencia Artificial" .
  ?docente foaf:name ?nombreDocente .
}`,
    'cursos-software': `PREFIX : <http://cramsoft.org/academico#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?nombreCurso ?codigoCurso
WHERE {
  ?curso rdf:type :Curso .
  ?curso :relacionadoConLinea ?linea .
  ?linea rdf:type :LineaInvestigacion .
  ?linea rdfs:label "Ingeniería de Software" .
  ?curso rdfs:label ?nombreCurso .
  ?curso :codigo ?codigoCurso .
}`,
    'horas-docentes': `PREFIX : <http://cramsoft.org/academico#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?nombreDocente (SUM(xsd:integer(?horas)) AS ?totalHoras)
WHERE {
  ?asignacion rdf:type :AsignacionDocente .
  ?asignacion :asignadoEn ?periodo .
  ?periodo rdf:type :PeriodoAcademico .
  ?periodo rdfs:label "2025-I" .
  ?asignacion :asignadoA ?docente .
  ?docente rdf:type :Docente .
  ?docente foaf:name ?nombreDocente .
  ?asignacion :horasAsignadas ?horas .
}
GROUP BY ?docente ?nombreDocente
ORDER BY DESC(?totalHoras)
LIMIT 1`
};

function loadQuery(queryId) {
    const query = PREDEFINED_QUERIES[queryId];
    if (query) {
        document.getElementById('sparql-query').value = query;
    }
}

// Event Listeners
function setupEventListeners() {
    // Buscar docentes
    const searchInput = document.getElementById('docente-search');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(searchDocentes, 300));
    }

    // Navegación entre pestañas
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = e.target.getAttribute('data-bs-target').substring(1);
            showSection(target);
        });
    });
}

// Función para buscar docentes
async function searchDocentes() {
    const searchTerm = document.getElementById('docente-search').value.trim();
    if (!searchTerm) {
        loadDocentes();
        return;
    }

    try {
        showLoading();
        const response = await axios.get(`${API_BASE_URL}/docentes`, {
            params: {
                search: searchTerm
            }
        });
        renderDocentesTable(response.data.data);
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al buscar docentes');
    }
}

// Funciones auxiliares
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Dashboard
async function loadDashboardStats() {
    try {
        const response = await axios.get(`${API_BASE_URL}/docentes`);
        const docentes = response.data.data;
        
        // Actualizar estadísticas
        document.getElementById('docentes-count').textContent = docentes.length;
        
        // Renderizar lista de docentes
        renderDocentesList(docentes);
    } catch (error) {
        showError('Error al cargar estadísticas');
    }
}

function renderDocentesList(docentes) {
    const tbody = document.getElementById('docentes-list');
    tbody.innerHTML = '';
    
    docentes.forEach(docente => {
        const lineasInvestigacion = docente.lineas_investigacion.map(li => li.nombre).join(', ');
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${docente.nombre}</td>
            <td>${docente.titulo}</td>
            <td>${docente.grado_academico}</td>
            <td>${docente.especialidad}</td>
            <td>${lineasInvestigacion}</td>
        `;
        tbody.appendChild(row);
    });
}

// Gestión de Docentes
async function loadDocentes(searchTerm = '') {
    try {
        const response = await axios.get(`${API_BASE_URL}/docentes`);
        renderDocentesTable(response.data.data);
    } catch (error) {
        showError('Error al cargar docentes');
    }
}

function renderDocentesTable(docentes) {
    const tbody = document.getElementById('docentes-table-body');
    tbody.innerHTML = '';
    
    docentes.forEach(docente => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${docente.nombre}</td>
            <td>${docente.titulo || '-'}</td>
            <td>${docente.grado_academico || '-'}</td>
            <td>${docente.especialidad || '-'}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editDocente(${docente.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteDocente(${docente.id})">
                    <i class="fas fa-trash"></i>
                </button>
                <div class="btn-group">
                    <button class="btn btn-sm btn-info" onclick="exportRdf(${docente.id}, 'xml')">
                        <i class="fas fa-file-xml"></i>
                    </button>
                    <button class="btn btn-sm btn-info" onclick="exportRdf(${docente.id}, 'turtle')">
                        <i class="fas fa-file-code"></i>
                    </button>
                    <button class="btn btn-sm btn-info" onclick="exportRdf(${docente.id}, 'jsonld')">
                        <i class="fas fa-file-alt"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Cargar líneas de investigación para el select
async function loadLineasInvestigacion() {
    try {
        const response = await axios.get(`${API_BASE_URL}/lineas_investigacion/`);
        const select = document.getElementById('docenteLineas');
        select.innerHTML = '';
        response.data.forEach(li => {
            const option = document.createElement('option');
            option.value = li.id;
            option.textContent = li.nombre;
            select.appendChild(option);
        });
    } catch (error) {
        showError('Error al cargar líneas de investigación');
    }
}

function showAddDocenteModal() {
    clearDocenteForm();
    loadLineasInvestigacion().then(() => {
        const modal = new bootstrap.Modal(document.getElementById('docenteModal'));
        modal.show();
        document.getElementById('docenteModal').style.display = 'block';
    });
}

function clearDocenteForm() {
    document.getElementById('docenteId').value = '';
    document.getElementById('docenteNombre').value = '';
    document.getElementById('docenteTitulo').value = '';
    document.getElementById('docenteEmail').value = '';
    document.getElementById('docenteGrado').value = '';
    document.getElementById('docenteEspecialidad').value = '';
    document.getElementById('docenteOrcid').value = '';
}

async function saveDocente() {
    const formData = {
        nombre: document.getElementById('docenteNombre').value,
        titulo: document.getElementById('docenteTitulo').value,
        email: document.getElementById('docenteEmail').value,
        grado_academico: document.getElementById('docenteGrado').value,
        especialidad: document.getElementById('docenteEspecialidad').value,
        orcid: document.getElementById('docenteOrcid').value
    };

    try {
        if (document.getElementById('docenteId').value) {
            await axios.put(`${API_BASE_URL}/docentes/${document.getElementById('docenteId').value}`, formData);
        } else {
            await axios.post(`${API_BASE_URL}/docentes/`, formData);
        }
        closeModal();
        loadDocentes();
        showSuccess('Docente guardado exitosamente');
    } catch (error) {
        showError('Error al guardar el docente');
    }
}

async function editDocente(id) {
    try {
        const response = await axios.get(`${API_BASE_URL}/docentes/${id}`);
        const docente = response.data;
        document.getElementById('docenteId').value = docente.id;
        document.getElementById('docenteNombre').value = docente.nombre;
        document.getElementById('docenteTitulo').value = docente.titulo;
        document.getElementById('docenteEmail').value = docente.email;
        document.getElementById('docenteGrado').value = docente.grado_academico;
        document.getElementById('docenteEspecialidad').value = docente.especialidad;
        document.getElementById('docenteOrcid').value = docente.orcid;
        showAddDocenteModal();
    } catch (error) {
        showError('Error al cargar el docente');
    }
}

async function deleteDocente(id) {
    if (!confirm('¿Está seguro de eliminar este docente?')) return;
    
    try {
        await axios.delete(`${API_BASE_URL}/docentes/${id}`);
        loadDocentes();
        showSuccess('Docente eliminado exitosamente');
    } catch (error) {
        showError('Error al eliminar el docente');
    }
}

// Visualización de Grafo
let network;

async function loadGraph() {
    try {
        showLoading();
        const response = await axios.get(`${API_BASE_URL}/visualizacion/grafo-completo`);
        const data = response.data.data;
        if (!network) {
            initializeGraph();
        }
        // Nodos
        const nodes = new vis.DataSet(data.nodes.map(node => {
            const type = node.type.toLowerCase();
            let title = '';
            if (type === 'docente') {
                const d = node.data || {};
                title = `<div class='node-info'><h6>${node.label}</h6><p><strong>Grado Académico:</strong> ${d.grado_academico || 'N/A'}</p><p><strong>Email:</strong> ${d.email || 'N/A'}</p><p><strong>ORCID:</strong> ${d.orcid || 'N/A'}</p></div>`;
            } else if (type === 'curso') {
                title = `<div class='node-info'><h6>${node.label}</h6></div>`;
            } else if (type === 'linea_investigacion') {
                title = `<div class='node-info'><h6>${node.label}</h6></div>`;
            } else if (type === 'periodo_academico') {
                title = `<div class='node-info'><h6>${node.label}</h6></div>`;
            } else if (type === 'produccion_academica') {
                const d = node.data || {};
                title = `<div class='node-info'><h6>${node.label}</h6><p><strong>Revista:</strong> ${d.revista || 'N/A'}</p><p><strong>Año:</strong> ${d.anio_publicacion || d.ano || 'N/A'}</p><p><strong>DOI:</strong> ${d.doi || 'N/A'}</p></div>`;
            } else if (type === 'disponibilidad_horaria') {
                const d = node.data || {};
                title = `<div class='node-info'><h6>${node.label}</h6><p><strong>Descripción:</strong> ${d.descripcion || node.label || 'N/A'}</p></div>`;
            }
            return {
                id: node.id,
                label: node.label,
                group: type,
                shape: type === 'docente' ? 'image' : 'dot',
                image: type === 'docente' ? 'https://via.placeholder.com/50' : undefined,
                font: { size: 14, color: '#333' },
                title
            };
        }));
        // Aristas
        const edges = new vis.DataSet(data.edges.map(edge => {
            let label = edge.type;
            let title = edge.type;
            if (edge.type === 'dicta' && edge.data && edge.data.horas_asignadas) {
                label = `${edge.type}\n${edge.data.horas_asignadas}h`;
                title = `${edge.type} (${edge.data.horas_asignadas} horas)`;
            }
            return {
                from: edge.source,
                to: edge.target,
                label,
                font: { size: 12, color: '#666' },
                title
            };
        }));
        network.setData({ nodes, edges });
        network.setOptions({
            groups: {
                docente: { color: { background: '#1976D2', border: '#1565C0', highlight: { background: '#42A5F5', border: '#1565C0' } }, size: 30 },
                linea_investigacion: { color: { background: '#4CAF50', border: '#388E3C', highlight: { background: '#66BB6A', border: '#388E3C' } }, size: 20 },
                curso: { color: { background: '#2196F3', border: '#1976D2', highlight: { background: '#42A5F5', border: '#1976D2' } }, size: 20 },
                periodo_academico: { color: { background: '#FFC107', border: '#F57C00', highlight: { background: '#FFD740', border: '#F57C00' } }, size: 20 },
                produccion_academica: { color: { background: '#9C27B0', border: '#7B1FA2', highlight: { background: '#BA68C8', border: '#7B1FA2' } }, size: 15 },
                disponibilidad_horaria: { color: { background: '#00BCD4', border: '#0097A7', highlight: { background: '#4DD0E1', border: '#0097A7' } }, size: 15 }
            },
            physics: { enabled: true, barnesHut: { gravitationalConstant: -8000, centralGravity: 0.3, springLength: 95, springConstant: 0.04, damping: 0.09, avoidOverlap: 0.1 } },
            interaction: { hover: true, tooltipDelay: 200 },
            layout: { hierarchical: false }
        });
        hideLoading();
    } catch (error) {
        hideLoading();
        console.error('Error al cargar el grafo:', error);
        showError('Error al cargar el grafo');
    }
}

                }
            },
            interaction: {
                hover: true,
                tooltipDelay: 200
            },
            layout: {
                hierarchical: false
            }
        });
        
        // Añadir tooltip para los nodos
        network.on('hoverNode', function (params) {
            const node = nodes.get(params.node);
            if (node && node.title) {
                const tooltip = document.createElement('div');
                tooltip.className = 'vis-tooltip';
                tooltip.innerHTML = node.title;
                document.body.appendChild(tooltip);
                
                const rect = network.canvas.body.clientToImage({
                    x: params.pointer.DOM.x,
                    y: params.pointer.DOM.y
                });
                
                tooltip.style.left = (rect.x + 10) + 'px';
                tooltip.style.top = (rect.y + 10) + 'px';
            }
        });
        
        network.on('blurNode', function (params) {
            const tooltip = document.querySelector('.vis-tooltip');
            if (tooltip) {
                document.body.removeChild(tooltip);
            }
        });
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al cargar el grafo');
    }
}

// Exportación RDF
async function exportRdf(docenteId, format) {
    try {
        const response = await axios.get(`${API_BASE_URL}/rdf/export/${format.toLowerCase()}`, {
            params: { docente_id: docenteId }
        });
        const blob = new Blob([response.data], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `docente_${docenteId}_${format.toLowerCase()}.${format.toLowerCase()}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        showError('Error al exportar el RDF');
    }
}

// Consultas SPARQL
async function executeSparqlQuery() {
    const query = document.getElementById('sparql-query').value;
    if (!query.trim()) {
        showError('Por favor ingrese una consulta SPARQL');
        return;
    }

    try {
        const response = await axios.post(`${API_BASE_URL}/sparql/`, { query });
        renderSparqlResults(response.data);
    } catch (error) {
        showError('Error al ejecutar la consulta SPARQL');
    }
}

function renderSparqlResults(results) {
    // Limpiar contenedores
    document.getElementById('sparql-table-results').innerHTML = '';
    document.getElementById('sparql-graph-container').innerHTML = '';

    // Mostrar resultados en tabla
    if (results && results.length > 0) {
        const table = document.createElement('table');
        table.className = 'table table-striped';
        
        // Encabezados
        const headers = Object.keys(results[0]);
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Filas
        const tbody = document.createElement('tbody');
        results.forEach(result => {
            const row = document.createElement('tr');
            headers.forEach(header => {
                const td = document.createElement('td');
                td.textContent = result[header];
                row.appendChild(td);
            });
            tbody.appendChild(row);
        });
        table.appendChild(tbody);
        
        document.getElementById('sparql-table-results').appendChild(table);
    } else {
        document.getElementById('sparql-table-results').innerHTML = '<p>No se encontraron resultados</p>';
    }

    // Mostrar resultados en grafo si hay datos relacionados
    if (results && results.length > 0) {
        const nodes = new vis.DataSet([]);
        const edges = new vis.DataSet([]);

        // Crear nodos y bordes para cada resultado
        results.forEach((result, index) => {
            // Crear nodos para cada campo
            Object.keys(result).forEach(key => {
                const value = result[key];
                if (!nodes.get(value)) {
                    nodes.add({
                        id: value,
                        label: `${key}: ${value}`,
                        group: key
                    });
                }
            });

            // Crear bordes entre campos relacionados
            const keys = Object.keys(result);
            for (let i = 0; i < keys.length - 1; i++) {
                const from = result[keys[i]];
                const to = result[keys[i + 1]];
                if (from !== to) {
                    edges.add({
                        from: from,
                        to: to,
                        label: keys[i + 1]
                    });
                }
            }
        });

        // Inicializar grafo de resultados
        const container = document.getElementById('sparql-graph-container');
        const data = {
            nodes: nodes,
            edges: edges
        };

        const options = {
            nodes: {
                shape: 'dot',
                size: 15
            },
            edges: {
                color: '#000',
                arrows: { to: true }
            },
            physics: {
                enabled: true
            }
        };

        new vis.Network(container, data, options);
    }
}

// Consultas SPARQL
async function executeSparqlQuery(query) {
    try {
        const response = await axios.post(`${API_BASE_URL}/sparql/`, { query });
        renderSparqlResults(response.data);
    } catch (error) {
        showError('Error al ejecutar la consulta SPARQL');
    }
}

function renderSparqlResults(results) {
    const resultsContainer = document.getElementById('sparql-results');
    resultsContainer.innerHTML = '';
    
    if (results && results.length > 0) {
        const table = document.createElement('table');
        table.className = 'table table-striped';
        
        // Encabezados
        const headers = Object.keys(results[0]);
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Filas
        const tbody = document.createElement('tbody');
        results.forEach(result => {
            const row = document.createElement('tr');
            headers.forEach(header => {
                const td = document.createElement('td');
                td.textContent = result[header];
                row.appendChild(td);
            });
            tbody.appendChild(row);
        });
        table.appendChild(tbody);
        
        resultsContainer.appendChild(table);
    } else {
        resultsContainer.innerHTML = '<p>No se encontraron resultados</p>';
    }
}

// Exportación RDF
async function exportRdf(format) {
    try {
        const response = await axios.get(`${API_BASE_URL}/rdf/export/${format.toLowerCase()}`);
        const blob = new Blob([response.data], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `academic_${format.toLowerCase()}.${format.toLowerCase()}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        showError('Error al exportar el RDF');
    }
}

// Utilidades
function showError(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger fade-in';
    alert.textContent = message;
    document.body.insertBefore(alert, document.body.firstChild);
    setTimeout(() => alert.remove(), 5000);
}

function showSuccess(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success fade-in';
    alert.textContent = message;
    document.body.insertBefore(alert, document.body.firstChild);
    setTimeout(() => alert.remove(), 5000);
}

function closeModal() {
    document.getElementById('docenteModal').classList.remove('show');
    document.getElementById('docenteModal').style.display = 'none';
}
