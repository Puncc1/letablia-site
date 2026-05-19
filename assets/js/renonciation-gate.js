/*!
 * renonciation-gate.js — L'établ'IA — 2026-05-19
 * Art. L.221-28, 13° CGI — conformité juridique fiches produits
 *
 * Rôle :
 *   - Désactive tous les boutons d'achat tant que la case
 *     "Je renonce à mon droit de rétractation" n'est pas cochée.
 *   - Marque le timestamp de renonciation (localStorage) au moment du clic.
 *
 * Détection des boutons d'achat (sélecteur large) :
 *   - <a> ou <button> dont href|data-product-buy contient contact.html?p=
 *   - .btn-acheter, [data-product-buy]
 *   - <a href*="lemonsqueezy">
 *   - <button type="submit"> dans <form> avec action contact.html
 *
 * Sélecteur case : #renonciation-droit-retractation (peut exister plusieurs fois ;
 *   toutes les instances sont synchronisées).
 */
(function () {
  'use strict';

  var BUY_SELECTOR = [
    'a[href*="contact.html?p="]',
    'a[href*="lemonsqueezy"]',
    'a.btn-acheter',
    'button.btn-acheter',
    '[data-product-buy]'
  ].join(',');

  var CHECKBOX_SELECTOR = '#renonciation-droit-retractation, input[name="renonciation"]';
  var DISABLED_STYLE_KEY = '__renonciationGateStyled';

  function getCheckboxes() {
    return Array.prototype.slice.call(document.querySelectorAll(CHECKBOX_SELECTOR));
  }

  function getBuyButtons() {
    // Exclure les liens vers le catalogue/diagnostic (pas des achats finaux)
    var nodes = Array.prototype.slice.call(document.querySelectorAll(BUY_SELECTOR));
    return nodes.filter(function (el) {
      var href = (el.getAttribute('href') || '').toLowerCase();
      // Diagnostic et catalogue ne sont pas des achats
      if (href.indexOf('diagnostic') !== -1) return false;
      if (href.indexOf('catalogue') !== -1) return false;
      return true;
    });
  }

  function disable(el) {
    el.setAttribute('aria-disabled', 'true');
    el.setAttribute('data-renonciation-blocked', 'true');
    if (el.tagName === 'BUTTON' || el.tagName === 'INPUT') {
      el.disabled = true;
    }
    // Sauvegarder href original pour restore
    if (el.tagName === 'A' && el.hasAttribute('href') && !el.hasAttribute('data-href-original')) {
      el.setAttribute('data-href-original', el.getAttribute('href'));
      el.removeAttribute('href');
    }
    if (!el[DISABLED_STYLE_KEY]) {
      el.style.opacity = '0.45';
      el.style.cursor = 'not-allowed';
      el.style.pointerEvents = 'auto'; // garder pour capter le clic et avertir
      el[DISABLED_STYLE_KEY] = true;
    }
  }

  function enable(el) {
    el.removeAttribute('aria-disabled');
    el.removeAttribute('data-renonciation-blocked');
    if (el.tagName === 'BUTTON' || el.tagName === 'INPUT') {
      el.disabled = false;
    }
    if (el.tagName === 'A' && el.hasAttribute('data-href-original')) {
      el.setAttribute('href', el.getAttribute('data-href-original'));
      el.removeAttribute('data-href-original');
    }
    el.style.opacity = '';
    el.style.cursor = '';
    el.style.pointerEvents = '';
    el[DISABLED_STYLE_KEY] = false;
  }

  function syncCheckboxes(state) {
    getCheckboxes().forEach(function (cb) {
      if (cb.checked !== state) cb.checked = state;
    });
  }

  function applyState() {
    var checkboxes = getCheckboxes();
    var checked = checkboxes.some(function (cb) { return cb.checked; });
    var buttons = getBuyButtons();

    if (!buttons.length) {
      console.warn('[renonciation-gate] Aucun bouton d\'achat détecté sur cette page.');
    }
    if (!checkboxes.length) {
      console.warn('[renonciation-gate] Aucune case de renonciation détectée — boutons laissés actifs.');
      return;
    }

    buttons.forEach(function (b) {
      if (checked) {
        enable(b);
      } else {
        disable(b);
      }
    });

    if (checked) {
      try {
        localStorage.setItem('renonciation_timestamp', String(Date.now()));
      } catch (e) { /* localStorage indisponible (private mode) — non bloquant */ }
    }
  }

  function onCheckboxChange(e) {
    syncCheckboxes(e.target.checked);
    applyState();
  }

  function onBuyClick(e) {
    // Si bloqué, prévenir + scroller vers la case
    var el = e.currentTarget;
    if (el.getAttribute('data-renonciation-blocked') === 'true') {
      e.preventDefault();
      e.stopPropagation();
      var first = document.querySelector(CHECKBOX_SELECTOR);
      if (first) {
        try { first.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (_) { first.scrollIntoView(); }
        first.focus();
        // Animation visuelle
        var bloc = first.closest('.renonciation-bloc');
        if (bloc) {
          bloc.style.transition = 'box-shadow .3s';
          bloc.style.boxShadow = '0 0 0 3px rgba(200,165,116,.6)';
          setTimeout(function () { bloc.style.boxShadow = ''; }, 1200);
        }
      }
      return false;
    }
    // Achat autorisé : ajouter timestamp à l'URL si <a>
    try {
      if (el.tagName === 'A' && el.hasAttribute('href')) {
        var ts = localStorage.getItem('renonciation_timestamp') || String(Date.now());
        var sep = el.href.indexOf('?') === -1 ? '?' : '&';
        if (el.href.indexOf('renonciation_ts=') === -1) {
          el.href = el.href + sep + 'renonciation_ts=' + encodeURIComponent(ts);
        }
      }
    } catch (e) { /* non bloquant */ }
  }

  function init() {
    var checkboxes = getCheckboxes();
    checkboxes.forEach(function (cb) {
      cb.addEventListener('change', onCheckboxChange);
    });

    var buttons = getBuyButtons();
    buttons.forEach(function (b) {
      b.addEventListener('click', onBuyClick, true);
    });

    applyState();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
