// Visualización principal del grafo
window.onload = function() {
  const container = document.getElementById('cy-grafo');
  container.innerHTML = '<div class="text-center my-5"><div class="spinner-border text-primary" role="status"></div><div>Cargando grafo...</div></div>';
  fetch('http://localhost:5000/api/visualizacion/grafo-completo')
    .then(r => r.json())
    .then(json => {
      if (!json.success) {
        container.innerHTML = '<div class="alert alert-danger">No se pudo cargar el grafo.</div>';
        return;
      }
      const nodes = json.data.nodes.map(n => ({ data: { id: n.id, label: n.label, group: n.type, ...n.data } }));
      const edges = json.data.edges.map(e => ({ data: { id: `${e.source}_${e.target}_${e.type}`.replace(/[^a-zA-Z0-9_]/g, ''), source: e.source, target: e.target, label: e.type, ...e.data } }));
      try {
        container.innerHTML = '';
        const cy = cytoscape({
          container,
          elements: [ ...nodes, ...edges ],
          style: [
            { selector: 'node', style: {
              'label': 'data(label)',
              'text-valign': 'center',
              'background-color': 'mapData(group, "docente", #1976d2, "curso", #43a047, "linea_investigacion", #fbc02d, "produccion_academica", #e53935, "periodo_academico", #8e24aa, "disponibilidad_horaria", #00838f, #888)' ,
              'color': '#222',
              'font-size': '13px',
              'width': 35, 'height': 35
            } },
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
            } }
          ],
          layout: { name: 'cose', animate: true }
        });
      } catch (err) {
        // Mostrar árbol HTML agrupado por área > línea > docente/curso
        container.innerHTML = '<div class="alert alert-warning">No se pudo renderizar el grafo.<br>Mostrando estructura jerárquica:</div>';
        container.appendChild(crearArbolAcademico(json.data.nodes, json.data.edges));
        // Muestra el JSON completo como string
        const pre = document.createElement('pre');
        pre.style.maxHeight = '300px';
        pre.style.overflow = 'auto';
        pre.style.background = '#f8f9fa';
        pre.style.fontSize = '11px';
        pre.innerText = JSON.stringify(json.data, null, 2);
        container.appendChild(pre);
      }
    })
    .catch(() => {
      container.innerHTML = '<div class="alert alert-danger">Error de red al cargar el grafo.</div>';
    });
};

// Construye un árbol HTML agrupado por Area > Linea > Curso/Docente
function crearArbolAcademico(nodes, edges) {
  // Agrupa nodos por tipo
  const nodosPorTipo = {};
  for (const n of nodes) {
    if (!nodosPorTipo[n.group]) nodosPorTipo[n.group] = {};
    nodosPorTipo[n.group][n.id] = n;
  }
  // Helper para buscar edges
  function findTargets(from, type) {
    return edges.filter(e => e.from === from && (!type || e.label === type)).map(e => e.to);
  }
  function findSources(to, type) {
    return edges.filter(e => e.to === to && (!type || e.label === type)).map(e => e.from);
  }
  // Crea elementos
  const ul = document.createElement('ul');

  // Áreas (si existen)
  if (nodosPorTipo['area']) {
    for (const areaId in nodosPorTipo['area']) {
      const area = nodosPorTipo['area'][areaId];
      const liArea = document.createElement('li');
      liArea.innerHTML = `<b>Área:</b> ${area.label}`;
      const ulLineas = document.createElement('ul');
      // Líneas de investigación bajo el área
      for (const lineaId in nodosPorTipo['linea_investigacion']) {
        const linea = nodosPorTipo['linea_investigacion'][lineaId];
        const areaDeLinea = findSources(lineaId, 'pertenece_area')[0];
        if (areaDeLinea === areaId) {
          ulLineas.appendChild(crearLiLinea(linea, nodosPorTipo, edges));
        }
      }
      if (ulLineas.childElementCount) liArea.appendChild(ulLineas);
      ul.appendChild(liArea);
    }
  } else if (nodosPorTipo['linea_investigacion']) {
    // Si no hay áreas, agrupa solo por líneas
    for (const lineaId in nodosPorTipo['linea_investigacion']) {
      const linea = nodosPorTipo['linea_investigacion'][lineaId];
      ul.appendChild(crearLiLinea(linea, nodosPorTipo, edges));
    }
  }
  return ul;
}

function crearLiLinea(linea, nodosPorTipo, edges) {
  const liLinea = document.createElement('li');
  liLinea.innerHTML = `<b>Línea:</b> ${linea.label}`;
  const ulLinea = document.createElement('ul');
  // Cursos relacionados
  for (const cursoId in nodosPorTipo['curso']||{}) {
    const curso = nodosPorTipo['curso'][cursoId];
    const lineasCurso = edges.filter(e => e.from === cursoId && e.label === 'relacionado_linea').map(e => e.to);
    if (lineasCurso.includes(linea.id)) {
      const liCurso = document.createElement('li');
      liCurso.innerHTML = `<b>Curso:</b> ${curso.label}`;
      ulLinea.appendChild(liCurso);
    }
  }
  // Docentes relacionados
  for (const docenteId in nodosPorTipo['docente']||{}) {
    const docente = nodosPorTipo['docente'][docenteId];
    const lineasDocente = edges.filter(e => e.from === docenteId && e.label === 'pertenece_linea').map(e => e.to);
    if (lineasDocente.includes(linea.id)) {
      ulLinea.appendChild(crearLiDocente(docente, nodosPorTipo, edges));
    }
  }
  if (ulLinea.childElementCount) liLinea.appendChild(ulLinea);
  return liLinea;
}

function crearLiDocente(docente, nodosPorTipo, edges) {
  const liDocente = document.createElement('li');
  liDocente.innerHTML = `<b>Docente:</b> ${docente.label}`;
  const ulDocente = document.createElement('ul');
  // Producción académica
  for (const prodId in nodosPorTipo['produccion_academica']||{}) {
    const prod = nodosPorTipo['produccion_academica'][prodId];
    const rel = edges.find(e => e.from === docente.id && e.to === prodId && e.label === 'tiene_produccion');
    if (rel) {
      const liProd = document.createElement('li');
      liProd.innerHTML = `<b>Producción:</b> ${prod.label}`;
      ulDocente.appendChild(liProd);
    }
  }
  // Disponibilidad horaria
  for (const dispId in nodosPorTipo['disponibilidad_horaria']||{}) {
    const disp = nodosPorTipo['disponibilidad_horaria'][dispId];
    const rel = edges.find(e => e.from === docente.id && e.to === dispId && e.label === 'tiene_disponibilidad');
    if (rel) {
      const liDisp = document.createElement('li');
      liDisp.innerHTML = `<b>Disponibilidad:</b> ${disp.label}`;
      ulDocente.appendChild(liDisp);
    }
  }
  // Asignaciones docentes (cursos y periodos)
  for (const cursoId in nodosPorTipo['curso']||{}) {
    const curso = nodosPorTipo['curso'][cursoId];
    const rel = edges.find(e => e.from === docente.id && e.to === curso.id && e.label === 'dicta');
    if (rel) {
      // Buscar periodo asignado
      const periodoEdge = edges.find(e => e.from === curso.id && e.label === 'asignado_periodo');
      let periodoLabel = '';
      if (periodoEdge && nodosPorTipo['periodo_academico'] && nodosPorTipo['periodo_academico'][periodoEdge.to]) {
        periodoLabel = ' (' + nodosPorTipo['periodo_academico'][periodoEdge.to].label + ')';
      }
      const liAsig = document.createElement('li');
      liAsig.innerHTML = `<b>Dicta:</b> ${curso.label}${periodoLabel}`;
      if (rel.data && rel.data.horas_asignadas) {
        liAsig.innerHTML += ` <span class='badge bg-info'>${rel.data.horas_asignadas}h</span>`;
      }
      ulDocente.appendChild(liAsig);
    }
  }
  if (ulDocente.childElementCount) liDocente.appendChild(ulDocente);
  return liDocente;
}

