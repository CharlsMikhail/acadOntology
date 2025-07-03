// CRUD Docentes y exportación
window.loadDocentes = function() {
  fetch('http://localhost:5000/api/docentes/')
    .then(r => r.json())
    .then(json => {
      if (!json.success) return;
      renderDocentesTable(json.data);
    });
};

function renderDocentesTable(docentes) {
  let html = `<table class="table table-bordered"><thead><tr><th>ID</th><th>Nombre</th><th>Título</th><th>Email</th><th>Grado</th><th>Especialidad</th><th>ORCID</th><th>Acciones</th></tr></thead><tbody>`;
  for (const d of docentes) {
    html += `<tr><td>${d.id}</td><td>${d.nombre}</td><td>${d.titulo||''}</td><td>${d.email||''}</td><td>${d.grado_academico||''}</td><td>${d.especialidad||''}</td><td>${d.orcid||''}</td><td>
      <button class='btn btn-sm btn-primary' onclick='editarDocente(${d.id})'>Editar</button>
      <button class='btn btn-sm btn-danger' onclick='eliminarDocente(${d.id})'>Eliminar</button>
      <div class="btn-group">
        <button class='btn btn-sm btn-outline-secondary dropdown-toggle' data-bs-toggle="dropdown">Exportar</button>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" href="#" onclick="exportarDocente(${d.id},'xml')">RDF/XML</a></li>
          <li><a class="dropdown-item" href="#" onclick="exportarDocente(${d.id},'turtle')">Turtle</a></li>
          <li><a class="dropdown-item" href="#" onclick="exportarDocente(${d.id},'jsonld')">JSON-LD</a></li>
        </ul>
      </div>
    </td></tr>`;
  }
  html += '</tbody></table>';
  document.getElementById('docentes-table-container').innerHTML = html;
}

// Agregar Docente
const modalDocente = new bootstrap.Modal(document.getElementById('modalDocente'));
document.getElementById('btn-nuevo-docente').onclick = () => {
  limpiarModalDocente();
  modalDocente.show();
};
document.getElementById('btn-guardar-docente').onclick = guardarDocente;

function limpiarModalDocente() {
  document.getElementById('form-docente').reset();
  document.getElementById('docente-id').value = '';
}

function editarDocente(id) {
  fetch(`http://localhost:5000/api/docente/${id}`)
    .then(r => r.json())
    .then(json => {
      if (!json.success) return;
      const d = json.data;
      document.getElementById('docente-id').value = d.id;
      document.getElementById('docente-nombre').value = d.nombre||'';
      document.getElementById('docente-titulo').value = d.titulo||'';
      document.getElementById('docente-email').value = d.email||'';
      document.getElementById('docente-grado').value = d.grado_academico||'';
      document.getElementById('docente-especialidad').value = d.especialidad||'';
      document.getElementById('docente-orcid').value = d.orcid||'';
      document.getElementById('docente-lineas').value = (d.lineas_investigacion_ids||[]).join(',');
      document.getElementById('docente-producciones').value = (d.producciones_academicas_ids||[]).join(',');
      modalDocente.show();
    });
}

function guardarDocente() {
  const id = document.getElementById('docente-id').value;
  const data = {
    nombre: document.getElementById('docente-nombre').value,
    titulo: document.getElementById('docente-titulo').value,
    email: document.getElementById('docente-email').value,
    grado_academico: document.getElementById('docente-grado').value,
    especialidad: document.getElementById('docente-especialidad').value,
    orcid: document.getElementById('docente-orcid').value,
    lineas_investigacion_ids: document.getElementById('docente-lineas').value.split(',').map(x => x.trim()).filter(x=>x),
    producciones_academicas_ids: document.getElementById('docente-producciones').value.split(',').map(x => x.trim()).filter(x=>x),
  };
  const method = id ? 'PUT' : 'POST';
  const url = `http://localhost:5000/api/docente/${id||''}`;
  fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
    .then(r => r.json())
    .then(json => {
      if (json.success) {
        modalDocente.hide();
        window.loadDocentes();
      } else {
        alert(json.error||'Error');
      }
    });
}

function eliminarDocente(id) {
  if (!confirm('¿Eliminar docente?')) return;
  fetch(`http://localhost:5000/api/docente/${id}`, { method: 'DELETE' })
    .then(r => r.json())
    .then(json => {
      if (json.success) window.loadDocentes();
      else alert(json.error||'Error');
    });
}

function exportarDocente(id, formato) {
  fetch(`http://localhost:5000/api/docente/${id}/perfil?format=${formato}`)
    .then(r => r.text())
    .then(text => {
      let ext = formato === 'turtle' ? 'ttl' : (formato === 'jsonld' ? 'jsonld' : 'rdf');
      let blob = new Blob([text], { type: formato === 'jsonld' ? 'application/ld+json' : (formato === 'turtle' ? 'text/turtle' : 'application/rdf+xml') });
      let a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `docente_${id}.${ext}`;
      a.click();
    });
}
