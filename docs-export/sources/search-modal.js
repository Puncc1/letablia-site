// Search modal global letablia.fr V4 — Cmd+K / / / clic ⌕
(function () {
  let products = null;
  let modalOpen = false;
  let selectedIdx = -1;

  // Charger products.json (lazy)
  async function loadProducts() {
    if (products) return products;
    try {
      const r = await fetch('/assets/data/products.json');
      const data = await r.json();
      products = data.products.filter(p => p.url && p.title);
      return products;
    } catch (e) {
      console.warn('[search] products.json indispo', e);
      products = [];
      return products;
    }
  }

  function familyLabel(slug) {
    const map = {
      'automatisations': 'Automatiser',
      'vendre': 'Vendre',
      'tableaux-de-bord': 'Piloter',
      'modeles': 'Produire',
      'guides-formations': 'Sécuriser'
    };
    return map[slug] || slug;
  }

  function search(q) {
    if (!q.trim()) return [];
    const ql = q.toLowerCase();
    const scored = products.map(p => {
      let score = 0;
      const title = p.title.toLowerCase();
      const kw = (p.keywords || '').toLowerCase();
      const tools = (p.tools || []).join(' ').toLowerCase();

      if (title.includes(ql)) score += 100;
      if (title.startsWith(ql)) score += 50;
      tools.split(' ').forEach(t => { if (t.includes(ql)) score += 30; });
      if (kw.includes(ql)) score += 10;
      if ((p.blurb || '').toLowerCase().includes(ql)) score += 5;
      return { product: p, score };
    });
    return scored.filter(s => s.score > 0).sort((a, b) => b.score - a.score).slice(0, 8);
  }

  function buildModal() {
    const html = `
      <div id="search-modal" class="fixed inset-0 z-[100] hidden items-start justify-center pt-20 px-4 bg-ebene/80 backdrop-blur-sm">
        <div class="w-full max-w-[600px] bg-lin border border-pierre/30 rounded-[12px] shadow-xl overflow-hidden">
          <div class="flex items-center gap-3 px-5 py-4 border-b border-pierre/30">
            <span class="text-pierre text-xl">⌕</span>
            <input id="search-modal-input" type="search" placeholder="Cherchez un système, un outil…" class="flex-1 bg-transparent border-none outline-none font-body text-[16px] text-ebene placeholder-pierre" autocomplete="off" autofocus />
            <button id="search-modal-close" class="font-mono text-[12px] text-pierre uppercase tracking-[1px] px-2 py-1 border border-pierre/30 rounded hover:border-chene">Esc</button>
          </div>
          <div id="search-modal-results" class="max-h-[420px] overflow-y-auto p-2"></div>
          <div class="px-5 py-3 border-t border-pierre/30 font-mono text-[11px] text-pierre flex items-center gap-4">
            <span><kbd class="bg-pierre/10 px-1 rounded">↑</kbd> <kbd class="bg-pierre/10 px-1 rounded">↓</kbd> naviguer</span>
            <span><kbd class="bg-pierre/10 px-1 rounded">↵</kbd> ouvrir</span>
            <span class="ml-auto"><kbd class="bg-pierre/10 px-1 rounded">⌘K</kbd> ou <kbd class="bg-pierre/10 px-1 rounded">/</kbd></span>
          </div>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', html);
  }

  function renderResults(q, results) {
    const container = document.getElementById('search-modal-results');
    if (!q.trim()) {
      container.innerHTML = `
        <p class="px-3 py-8 text-center font-body text-[14px] text-pierre">
          Tapez le nom d'un système, d'un outil (Shopify, Notion…), ou un mot-clé.
        </p>
      `;
      selectedIdx = -1;
      return;
    }
    if (results.length === 0) {
      container.innerHTML = `
        <p class="px-3 py-8 text-center font-body text-[14px] text-pierre">
          Aucun système ne correspond à "${q}". Essayez "stock", "shopify", "crm"…
        </p>
      `;
      selectedIdx = -1;
      return;
    }
    container.innerHTML = results.map((r, i) => `
      <a href="${r.product.url}" class="search-result block px-3 py-3 rounded hover:bg-chene-6 ${i === selectedIdx ? 'bg-chene-6' : ''}" data-idx="${i}">
        <p class="font-mono text-[10px] uppercase tracking-[1px] text-chene mb-1">${familyLabel(r.product.family)} · ${(r.product.tools || []).slice(0, 2).join(' · ')}</p>
        <h3 class="font-heading text-[18px] text-ebene leading-[1.2]">${r.product.title} <span class="font-mono text-[14px] text-chene ml-2">${r.product.price} €</span></h3>
        <p class="font-body text-[13px] text-pierre leading-[1.4] mt-1">${r.product.blurb || ''}</p>
      </a>
    `).join('');
  }

  let lastResults = [];

  function open() {
    if (modalOpen) return;
    modalOpen = true;
    document.getElementById('search-modal').classList.remove('hidden');
    document.getElementById('search-modal').classList.add('flex');
    document.body.style.overflow = 'hidden';
    setTimeout(() => document.getElementById('search-modal-input').focus(), 50);
    loadProducts().then(() => renderResults('', []));
  }

  function close() {
    if (!modalOpen) return;
    modalOpen = false;
    document.getElementById('search-modal').classList.remove('flex');
    document.getElementById('search-modal').classList.add('hidden');
    document.body.style.overflow = '';
    selectedIdx = -1;
  }

  function init() {
    buildModal();
    const modal = document.getElementById('search-modal');
    const input = document.getElementById('search-modal-input');
    const closeBtn = document.getElementById('search-modal-close');

    closeBtn.addEventListener('click', close);
    modal.addEventListener('click', (e) => { if (e.target === modal) close(); });

    input.addEventListener('input', async () => {
      await loadProducts();
      lastResults = search(input.value);
      selectedIdx = lastResults.length > 0 ? 0 : -1;
      renderResults(input.value, lastResults);
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { e.preventDefault(); close(); }
      else if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (lastResults.length === 0) return;
        selectedIdx = (selectedIdx + 1) % lastResults.length;
        renderResults(input.value, lastResults);
      }
      else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (lastResults.length === 0) return;
        selectedIdx = (selectedIdx - 1 + lastResults.length) % lastResults.length;
        renderResults(input.value, lastResults);
      }
      else if (e.key === 'Enter') {
        e.preventDefault();
        if (selectedIdx >= 0 && lastResults[selectedIdx]) {
          window.location.href = lastResults[selectedIdx].product.url;
        }
      }
    });

    // Triggers globaux
    document.addEventListener('keydown', (e) => {
      // Cmd+K / Ctrl+K
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        modalOpen ? close() : open();
      }
      // / quand pas dans input
      else if (e.key === '/' && !modalOpen) {
        const tag = (document.activeElement || {}).tagName;
        if (tag !== 'INPUT' && tag !== 'TEXTAREA') {
          e.preventDefault();
          open();
        }
      }
      // Esc
      else if (e.key === 'Escape' && modalOpen) {
        close();
      }
    });

    // Tous les boutons/liens avec data-search-trigger ou id=search-trigger
    document.querySelectorAll('[data-search-trigger], #search-trigger').forEach(el => {
      el.addEventListener('click', (e) => { e.preventDefault(); open(); });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
