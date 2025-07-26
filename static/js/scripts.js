
function openDeleteModal(entradaId, entradaTitulo) {
  // Mostrar el título en el modal
  document.getElementById('modalEntryTitle').textContent = entradaTitulo;

  // Cambiar la URL del formulario al endpoint de eliminar
  const form = document.getElementById('deleteForm');
  form.action = `/delete_entrada/${entradaId}/`;  


  // Mostrar el modal
  document.getElementById('deleteModal').classList.remove('hidden');
}

function closeDeleteModal() {
  document.getElementById('deleteModal').classList.add('hidden');
}

