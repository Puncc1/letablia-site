// Burger menu universal — robuste, defer-loaded
(function() {
  function init() {
    const toggle = document.getElementById('menu-toggle');
    const close = document.getElementById('menu-close');
    const menu = document.getElementById('mobile-menu');

    if (!toggle || !menu) {
      console.warn('[burger-menu] toggle ou menu absent dans le DOM');
      return;
    }

    function open() {
      menu.classList.remove('hidden');
      menu.style.display = 'flex';  // force display flex
      document.body.style.overflow = 'hidden';  // bloquer scroll body
    }
    function shut() {
      menu.classList.add('hidden');
      menu.style.display = 'none';
      document.body.style.overflow = '';
    }

    toggle.addEventListener('click', open);
    if (close) close.addEventListener('click', shut);

    // Fermer aussi sur clic d'un lien interne au menu
    menu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', shut);
    });

    // Fermer sur ESC
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && !menu.classList.contains('hidden')) shut();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
