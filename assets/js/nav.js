/**
 * Navigation mobile — Toggle menu burger
 * Léger (<1KB) et zéro dépendance
 */

const menuToggle = document.getElementById('menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');
const menuClose = document.getElementById('menu-close');

if (menuToggle && mobileMenu && menuClose) {
  menuToggle.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
    menuToggle.classList.toggle('open');
  });

  menuClose.addEventListener('click', () => {
    mobileMenu.classList.remove('open');
    menuToggle.classList.remove('open');
  });

  // Fermer le menu en cliquant sur un lien
  document.querySelectorAll('#mobile-menu a').forEach(link => {
    link.addEventListener('click', () => {
      mobileMenu.classList.remove('open');
      menuToggle.classList.remove('open');
    });
  });

  // Fermer en tapant Échap
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
      mobileMenu.classList.remove('open');
      menuToggle.classList.remove('open');
    }
  });
}
