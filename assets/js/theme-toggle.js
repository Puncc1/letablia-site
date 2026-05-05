/*!
 * L'établ'IA — theme-toggle.js
 * Mode « Lumière de l'établi » — jour/nuit
 *
 * - Lit localStorage('letablia-theme')
 * - Fallback sur prefers-color-scheme
 * - Toggle soleil/lune dans le header
 * - Transition 0.3s (activée uniquement après chargement initial)
 */
(function () {
  'use strict';

  var KEY = 'letablia-theme';
  var BTN = '[data-theme-btn]';

  /* ── helpers ────────────────────────────────────────────────── */
  function getStored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function store(theme) {
    try { localStorage.setItem(KEY, theme); } catch (e) {}
  }

  /* ── appliquer le thème sur <html> ───────────────────────────── */
  function applyTheme(theme) {
    var root = document.documentElement;
    root.setAttribute('data-theme', theme);
    var isDark = (theme === 'dark');
    document.querySelectorAll(BTN).forEach(function (btn) {
      btn.setAttribute('aria-label',
        isDark
          ? 'Activer la lumière forte (mode jour)'
          : 'Activer la lumière douce (mode nuit)');
      btn.setAttribute('aria-pressed', isDark ? 'true' : 'false');
    });
  }

  /* ── toggle ─────────────────────────────────────────────────── */
  function toggle() {
    var current = document.documentElement.getAttribute('data-theme') || 'light';
    var next = (current === 'dark') ? 'light' : 'dark';
    applyTheme(next);
    store(next);
  }

  /* ── init (attacher les listeners) ─────────────────────────── */
  function init() {
    /* Activer les transitions CSS maintenant que la page est chargée */
    document.documentElement.classList.add('theme-ready');

    document.querySelectorAll(BTN).forEach(function (btn) {
      btn.addEventListener('click', toggle);
      btn.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggle();
        }
      });
    });

    /* Synchroniser l'état aria avec le thème actuel */
    var current = document.documentElement.getAttribute('data-theme') || 'light';
    applyTheme(current);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
