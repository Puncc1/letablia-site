// Filtres + tri catalogue letablia.fr V4
(function () {
  const grid = document.getElementById('products-grid');
  const cards = Array.from(grid.querySelectorAll('.product-card'));
  const filterCbs = Array.from(document.querySelectorAll('.filter-cb'));
  const searchInput = document.getElementById('search-input');
  const sortSelect = document.getElementById('sort-select');
  const visibleCount = document.getElementById('visible-count');
  const emptyState = document.getElementById('empty-state');
  const resetBtns = [
    document.getElementById('reset-filters'),
    document.getElementById('reset-filters-empty'),
  ].filter(Boolean);
  const filtersToggle = document.getElementById('filters-toggle');
  const filtersAside = document.getElementById('filters');

  function getActiveFilters() {
    const f = { family: [], tools: [], targets: [], price: [] };
    filterCbs.forEach(cb => {
      if (cb.checked) {
        if (cb.dataset.axis === 'price') {
          f.price.push({ min: +cb.dataset.min, max: +cb.dataset.max });
        } else {
          f[cb.dataset.axis].push(cb.value);
        }
      }
    });
    return f;
  }

  function matchesFilters(card, filters, search) {
    // Search match
    if (search) {
      const haystack = (card.dataset.title + ' ' + card.dataset.keywords + ' ' + card.dataset.tools).toLowerCase();
      if (!haystack.includes(search)) return false;
    }
    // Family
    if (filters.family.length > 0 && !filters.family.includes(card.dataset.family)) return false;
    // Tools
    if (filters.tools.length > 0) {
      const cardTools = card.dataset.tools.split(' ');
      if (!filters.tools.some(t => cardTools.includes(t))) return false;
    }
    // Targets
    if (filters.targets.length > 0) {
      const cardTargets = card.dataset.targets.split(' ');
      if (!filters.targets.some(t => cardTargets.includes(t))) return false;
    }
    // Price
    if (filters.price.length > 0) {
      const price = +card.dataset.price;
      if (!filters.price.some(p => price >= p.min && price <= p.max)) return false;
    }
    return true;
  }

  function sortCards(cards, mode) {
    const arr = cards.slice();
    if (mode === 'price-asc') {
      arr.sort((a, b) => +a.dataset.price - +b.dataset.price);
    } else if (mode === 'price-desc') {
      arr.sort((a, b) => +b.dataset.price - +a.dataset.price);
    } else if (mode === 'title-asc') {
      arr.sort((a, b) => a.dataset.title.localeCompare(b.dataset.title));
    }
    return arr;
  }

  function applyFilters() {
    const filters = getActiveFilters();
    const search = searchInput.value.trim().toLowerCase();
    const sortMode = sortSelect.value;

    let visible = 0;
    cards.forEach(card => {
      const ok = matchesFilters(card, filters, search);
      card.style.display = ok ? '' : 'none';
      if (ok) visible++;
    });

    // Tri (réordonner les visibles dans le DOM)
    const sortedVisibleCards = sortCards(cards.filter(c => c.style.display !== 'none'), sortMode);
    sortedVisibleCards.forEach(c => grid.appendChild(c));

    visibleCount.textContent = visible;
    emptyState.classList.toggle('hidden', visible > 0);
    grid.classList.toggle('hidden', visible === 0);

    // Update URL avec params
    const params = new URLSearchParams();
    if (filters.family.length) params.set('famille', filters.family.join(','));
    if (filters.tools.length) params.set('outil', filters.tools.join(','));
    if (filters.targets.length) params.set('cible', filters.targets.join(','));
    if (filters.price.length) params.set('prix', filters.price.map(p => p.min + '-' + p.max).join(','));
    if (search) params.set('q', search);
    if (sortMode !== 'default') params.set('tri', sortMode);
    const newUrl = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
    window.history.replaceState({}, '', newUrl);
  }

  function loadFromUrl() {
    const params = new URLSearchParams(window.location.search);
    const fams = params.get('famille');
    if (fams) fams.split(',').forEach(v => {
      const cb = filterCbs.find(c => c.dataset.axis === 'family' && c.value === v);
      if (cb) cb.checked = true;
    });
    const tools = params.get('outil');
    if (tools) tools.split(',').forEach(v => {
      const cb = filterCbs.find(c => c.dataset.axis === 'tools' && c.value === v);
      if (cb) cb.checked = true;
    });
    const targets = params.get('cible');
    if (targets) targets.split(',').forEach(v => {
      const cb = filterCbs.find(c => c.dataset.axis === 'targets' && c.value === v);
      if (cb) cb.checked = true;
    });
    const q = params.get('q');
    if (q) searchInput.value = q;
    const tri = params.get('tri');
    if (tri) sortSelect.value = tri;
  }

  function resetAll() {
    filterCbs.forEach(cb => cb.checked = false);
    searchInput.value = '';
    sortSelect.value = 'default';
    applyFilters();
  }

  // Listeners
  filterCbs.forEach(cb => cb.addEventListener('change', applyFilters));
  searchInput.addEventListener('input', () => {
    clearTimeout(searchInput._timer);
    searchInput._timer = setTimeout(applyFilters, 100);
  });
  sortSelect.addEventListener('change', applyFilters);
  resetBtns.forEach(btn => btn.addEventListener('click', resetAll));

  // Mobile : toggle filtres
  if (filtersToggle) {
    filtersAside.classList.add('hidden', 'md:block');
    filtersToggle.addEventListener('click', () => {
      filtersAside.classList.toggle('hidden');
    });
  }

  loadFromUrl();
  applyFilters();
})();
