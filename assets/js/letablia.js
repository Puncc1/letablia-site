/* L'établ'IA — utilitaires partagés
   - Charge products.json
   - Reveal au scroll
   - Recherche (overlay)
   - Burger mobile
   - Hydrate compteurs et liens
*/
(function(){
  // ---- Reveal ----
  const io = new IntersectionObserver(entries=>{
    entries.forEach(e=>{
      if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}
    });
  },{threshold:0.1, rootMargin:'0px 0px -60px 0px'});
  document.querySelectorAll('[data-reveal]').forEach(el=>io.observe(el));

  // ---- Burger mobile ----
  const burger = document.querySelector('[data-burger]');
  const mobile = document.querySelector('[data-mobile-menu]');
  if(burger && mobile){
    burger.addEventListener('click', ()=>mobile.classList.add('open'));
    mobile.querySelector('[data-mobile-close]')?.addEventListener('click',()=>mobile.classList.remove('open'));
  }

  // ---- Recherche overlay ----
  const searchBtn = document.querySelector('[data-search-btn]');
  const searchOverlay = document.querySelector('[data-search-overlay]');
  if(searchBtn && searchOverlay){
    const input = searchOverlay.querySelector('input');
    const results = searchOverlay.querySelector('[data-search-results]');
    const open = ()=>{searchOverlay.classList.add('open');setTimeout(()=>input.focus(),50)};
    const close = ()=>searchOverlay.classList.remove('open');
    searchBtn.addEventListener('click', open);
    searchOverlay.querySelector('[data-search-close]')?.addEventListener('click', close);
    document.addEventListener('keydown',e=>{
      if(e.key==='/' && !['INPUT','TEXTAREA'].includes(document.activeElement.tagName)){e.preventDefault();open()}
      if(e.key==='Escape')close();
    });
    // Search uses window.LE_DATA when available
    input?.addEventListener('input', ()=>{
      const q = input.value.trim().toLowerCase();
      const data = window.LE_DATA;
      if(!data || !q){results.innerHTML='';return}
      const tokens = q.split(/\s+/);
      const score = (p)=>{
        const hay = (p.title+' '+p.blurb+' '+(p.keywords||'')+' '+(p.tools||[]).join(' ')).toLowerCase();
        return tokens.every(t=>hay.includes(t)) ? 1 : 0;
      };
      const matched = data.products
        .map(p=>({p,s:score(p)}))
        .filter(x=>x.s>0)
        .slice(0,8);
      if(matched.length===0){results.innerHTML = `<div class="se-empty">Aucun résultat pour « ${q} »</div>`;return}
      results.innerHTML = matched.map(({p})=>{
        const fam = famClass(p.family);
        return `<a class="se-result fam-${fam}" href="produits/${slugFile(p)}">
          <span class="se-dot"></span>
          <span class="se-title">${p.title}</span>
          <span class="se-blurb">${p.blurb}</span>
          <span class="se-price">${p.price}€</span>
        </a>`;
      }).join('');
    });
  }

  // ---- Active link in header ----
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('[data-nav]').forEach(a=>{
    if(a.dataset.nav === path) a.classList.add('current');
  });

  // ---- Data loader ----
  // products.json is loaded inline by each page via window.LE_DATA = {...}
})();

function famClass(fam){
  return ({
    'automatisations':'automatiser',
    'vendre':'vendre',
    'tableaux-de-bord':'piloter',
    'modeles':'produire',
    'guides-formations':'securiser'
  })[fam] || 'automatiser';
}
function famLabel(fam){
  return ({
    'automatisations':'Automatiser',
    'vendre':'Vendre',
    'tableaux-de-bord':'Piloter',
    'modeles':'Produire',
    'guides-formations':'Sécuriser'
  })[fam] || 'Automatiser';
}
function slugFile(p){
  // produit/relance-prospects -> produit-relance-prospects.html
  return (p.slug.replace(/\//g,'-'))+'.html';
}
window.LE = {famClass, famLabel, slugFile};
