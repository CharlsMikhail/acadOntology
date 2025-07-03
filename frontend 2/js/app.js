// Navegación SPA
function showSection(section) {
  document.getElementById('section-grafo').style.display = section === 'grafo' ? '' : 'none';
  document.getElementById('section-docentes').style.display = section === 'docentes' ? '' : 'none';
  document.getElementById('section-sparql').style.display = section === 'sparql' ? '' : 'none';
}
document.getElementById('nav-grafo').onclick = () => showSection('grafo');
document.getElementById('nav-docentes').onclick = () => {
  showSection('docentes');
  if (window.loadDocentes) window.loadDocentes();
};
document.getElementById('nav-sparql').onclick = () => showSection('sparql');
// Inicializar por defecto
showSection('grafo');
