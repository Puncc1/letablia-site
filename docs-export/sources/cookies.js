// Bannière Cookies L'établ'IA V4 — RGPD compliant
// Stockage : localStorage uniquement, pas de tracker externe
(function() {
  const KEY = 'letablia_cookies_consent';
  const VERSION = '1';

  function getConsent() {
    try {
      const data = JSON.parse(localStorage.getItem(KEY) || '{}');
      if (data.version !== VERSION) return null;
      return data;
    } catch (e) { return null; }
  }

  function setConsent(level) {
    localStorage.setItem(KEY, JSON.stringify({
      version: VERSION,
      level: level, // 'all' | 'essential' | 'rejected'
      timestamp: new Date().toISOString()
    }));
  }

  function showBanner() {
    if (getConsent()) return;
    const banner = document.createElement('div');
    banner.id = 'cookies-banner';
    banner.innerHTML = `
      <div class="cb-content">
        <p>
          <strong>Cookies & vie privée.</strong>
          Ce site utilise un stockage local minimal pour mémoriser vos préférences.
          Aucun tracker externe, aucune publicité.
          <a href="/confidentialite/">Politique de confidentialité</a>.
        </p>
        <div class="cb-actions">
          <button class="cb-btn cb-btn-primary" id="cb-accept">J'accepte</button>
          <button class="cb-btn cb-btn-secondary" id="cb-essential">Essentiel uniquement</button>
        </div>
      </div>
    `;
    document.body.appendChild(banner);
    document.getElementById('cb-accept').onclick = () => { setConsent('all'); banner.remove(); };
    document.getElementById('cb-essential').onclick = () => { setConsent('essential'); banner.remove(); };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', showBanner);
  } else {
    showBanner();
  }
})();
