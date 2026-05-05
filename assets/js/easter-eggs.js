/**
 * L'établ'IA — Easter Eggs
 * Version : 1.0 — 2026-05-05
 *
 * Trois secrets pour les curieux :
 *   1. Logo cliqué 3× rapidement  → toast discret
 *   2. Konami code (↑↑↓↓←→←→BA)  → message caché
 *   3. Footer citation artisanale aléatoire au reload
 *
 * Vanilla JS — aucun tracking — idempotent
 */

(function () {
  'use strict';

  /* ── Idempotence ─────────────────────────────────────────── */
  if (window.__LE_EGGS__) return;
  window.__LE_EGGS__ = true;

  /* ── Palette (héritage V4/V5) ────────────────────────────── */
  var COLORS = {
    ebene   : '#2C2825',
    encre   : '#1B1815',
    lin     : '#F2EDE8',
    chene   : '#8A7560',
    pierre  : '#B8AFA6'
  };

  /* ═══════════════════════════════════════════════════════════
     UTILITAIRE — Toast sobre palette V4
     fade-in 300 ms · durée ~2700 ms · fade-out 300 ms → 3 s total
  ═══════════════════════════════════════════════════════════ */
  function showToast(message) {
    var existing = document.getElementById('le-toast-egg');
    if (existing) existing.remove();

    var toast = document.createElement('div');
    toast.id = 'le-toast-egg';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');

    Object.assign(toast.style, {
      position      : 'fixed',
      bottom        : '32px',
      right         : '32px',
      zIndex        : '9999',
      background    : COLORS.ebene,
      color         : COLORS.lin,
      border        : '1px solid ' + COLORS.chene,
      borderLeft    : '3px solid ' + COLORS.chene,
      borderRadius  : '4px',
      padding       : '14px 20px',
      fontFamily    : '"Inter", -apple-system, sans-serif',
      fontSize      : '13px',
      lineHeight    : '1.5',
      maxWidth      : '320px',
      boxShadow     : '0 4px 16px rgba(27,24,21,0.35)',
      opacity       : '0',
      transform     : 'translateY(6px)',
      transition    : 'opacity 300ms ease, transform 300ms ease',
      pointerEvents : 'none'
    });

    toast.textContent = message;
    document.body.appendChild(toast);

    /* Fade in */
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        toast.style.opacity   = '1';
        toast.style.transform = 'translateY(0)';
      });
    });

    /* Fade out puis suppression */
    setTimeout(function () {
      toast.style.opacity   = '0';
      toast.style.transform = 'translateY(6px)';
      setTimeout(function () {
        if (toast.parentNode) toast.remove();
      }, 300);
    }, 2700);
  }

  /* ═══════════════════════════════════════════════════════════
     EASTER EGG 1 — Logo cliqué 3× rapidement (≤ 900 ms)
  ═══════════════════════════════════════════════════════════ */
  (function initLogoTripleClick() {
    var clicks     = 0;
    var resetTimer = null;
    var DELAY      = 900;

    function onLogoClick(e) {
      var header = document.querySelector('header.le-header');
      if (!header) return;
      if (!header.contains(e.target)) return;
      if (!e.target.closest('.le-logo')) return;

      clicks++;
      clearTimeout(resetTimer);

      if (clicks >= 3) {
        clicks = 0;
        e.preventDefault();
        showToast("L’établi reconnaît les curieux.");
      } else {
        resetTimer = setTimeout(function () { clicks = 0; }, DELAY);
      }
    }

    document.addEventListener('click', onLogoClick, true);
  }());

  /* ═══════════════════════════════════════════════════════════
     EASTER EGG 2 — Konami code  ↑↑↓↓←→←→BA
  ═══════════════════════════════════════════════════════════ */
  (function initKonami() {
    var SEQUENCE = [
      'ArrowUp', 'ArrowUp',
      'ArrowDown', 'ArrowDown',
      'ArrowLeft', 'ArrowRight',
      'ArrowLeft', 'ArrowRight',
      'b', 'a'
    ];
    var index = 0;

    document.addEventListener('keydown', function (e) {
      var expected = SEQUENCE[index];
      var key = (e.key.length === 1) ? e.key.toLowerCase() : e.key;

      if (key === expected) {
        index++;
        if (index === SEQUENCE.length) {
          index = 0;
          showToast("Vous êtes du genre patient. Ça nous va.");
        }
      } else {
        index = (key === SEQUENCE[0]) ? 1 : 0;
      }
    });
  }());

  /* ═══════════════════════════════════════════════════════════
     EASTER EGG 3 — Citation artisanale aléatoire en footer
  ═══════════════════════════════════════════════════════════ */
  (function initFooterCitation() {
    var CITATIONS = [
      "« On forge ce qu’on aurait voulu acheter. »",
      "« Un système, c’est comme un meuble : on le sent quand il tient. »",
      "« Le silence d’un atelier qui marche. »",
      "« Pas de promesse qu’on ne pourrait pas tenir. »",
      "« Le bon outil au bon endroit, c’est déjà la moitié du travail. »",
      "« Mieux vaut un système qui dort qu’un client qui s’inquiète. »",
      "« On dit non plus souvent qu’oui. C’est le métier. »",
      "« L’établi est ouvert. La porte aussi. »"
    ];

    function injectCitation() {
      if (document.getElementById('le-footer-citation')) return;

      var footer = document.querySelector('footer.le-footer');
      if (!footer) return;

      var bottom = footer.querySelector('.le-footer-bottom');
      if (!bottom) return;

      var quote = CITATIONS[Math.floor(Math.random() * CITATIONS.length)];

      var el = document.createElement('div');
      el.id = 'le-footer-citation';
      Object.assign(el.style, {
        maxWidth      : '1280px',
        margin        : '0 auto',
        padding       : '0 24px 20px',
        fontFamily    : '"Playfair Display", Georgia, serif',
        fontStyle     : 'italic',
        fontSize      : '13px',
        color         : COLORS.pierre,
        opacity       : '0.75',
        textAlign     : 'center',
        letterSpacing : '0.01em',
        lineHeight    : '1.6'
      });
      el.textContent = quote;

      footer.insertBefore(el, bottom);
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', injectCitation);
    } else {
      injectCitation();
    }
  }());

}());
