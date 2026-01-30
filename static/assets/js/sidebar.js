// Script para activar los links del sidebar mientras scrolleas
document.addEventListener('DOMContentLoaded', function() {
  // Obtener todos los links del sidebar
  const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
  
  if (sidebarLinks.length === 0) return;

  // Función para actualizar el link activo
  function updateActiveLink() {
    let scrollPosition = window.scrollY + 200; // Offset para detectar mejor

    sidebarLinks.forEach((link) => {
      // Obtener el elemento al que apunta el link
      const sectionId = link.getAttribute('href').substring(1); // Quitar el '#'
      const section = document.getElementById(sectionId);

      if (!section) {
        console.warn(`Sección con ID "${sectionId}" no encontrada`);
        return;
      }

      // Obtener posición del elemento
      const sectionTop = section.offsetTop;
      const sectionBottom = sectionTop + section.offsetHeight;

      // Verificar si el usuario está en esa sección
      if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
        // Remover 'active' de todos los links
        sidebarLinks.forEach((l) => l.classList.remove('active'));
        // Agregar 'active' al link actual
        link.classList.add('active');
      }
    });
  }

  // Actualizar al hacer scroll
  window.addEventListener('scroll', updateActiveLink, { passive: true });
  
  // Actualizar al cargar la página
  updateActiveLink();

  // Permitir click en los links para scroll suave
  sidebarLinks.forEach((link) => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href').substring(1);
      const targetElement = document.getElementById(targetId);
      
      if (targetElement) {
        // Scroll suave al elemento
        targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Actualizar el active después de un pequeño delay
        setTimeout(() => {
          updateActiveLink();
        }, 100);
      }
    });
  });
});
