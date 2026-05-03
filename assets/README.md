# Système de Design V3 — L'établ'IA / letablia.fr

## Vue d'ensemble

Ce dossier contient les ressources partagées pour **cohérence visuelle** du site letablia.fr :

- **`css/base.css`** — Système de design complet (variables, composants, grid, accessibilité)
- **`css/design-system.css`** — Alias pour compatibilité arrière (importe base.css)
- **`js/nav.js`** — Navigation mobile (menu burger, ~600 bytes)

### Principe

- **CSS Vanilla** avec custom properties `:root`
- **Mobile-first** responsif (64px → 1200px)
- **Pas de framework** (Tailwind, Bootstrap interdits)
- **Palette V3** artisan + alias générique pour compatibilité

---

## Variables CSS principales

### Palette V3 (noms métaphoriques)

```css
--v3-color-fond: #F6F1E8      /* Fond principal 80% */
--v3-color-ivoire: #FFFCF5    /* Cartes, boîtes */
--v3-color-papier: #E9DDC8    /* Sections secondaires */
--v3-color-graphite: #25221D  /* Texte principal */
--v3-color-brun: #6B4A2F      /* Titres H2/H3, accents */
--v3-color-cuivre: #B46A3C    /* CTA, badges → ACCENT PRIMARY */
--v3-color-vert: #3F6F5B      /* Validation, réassurance */
--v3-color-ardoise: #344E5C   /* Données, dashboards */
--v3-color-brique: #8C3F32    /* Alertes, limites */
--v3-color-ocre: #B88A2E      /* Métriques, tableaux */
```

### Alias générique (compatibilité)

```css
--chene: #8A7560      /* Accent alternative */
--pierre: #C5B9A8     /* Borders, séparateurs */
--mousse: #5C6E4A     /* Validation */
--lin: #F5F0E8        /* Fond claire */
--ebene: #1A1A1A      /* Texte foncé */
--blanc: #FFFFFF      /* Blanc pur */
```

### Typographies

```css
--font-titre: 'Zodiak', Georgia, serif           /* H1, H2, H3, badges */
--font-corps: 'Satoshi', system-ui, sans-serif   /* Body, p, labels */
--font-mono: 'JetBrains Mono', monospace         /* Code, données */
```

### Espacement & Dimensions

```css
--radius: 6px           /* Border-radius défaut */
--radius-sm: 4px        /* Petit */
--radius-lg: 8px        /* Grand */
--max-width: 1200px     /* Conteneur large */
--max-width-narrow: 900px
--shadow: 0 2px 8px rgba(0,0,0,0.08)
--shadow-md, --shadow-lg  /* Profondeur */
--transition-fast: 0.15s ease
--transition-normal: 0.2s ease
--transition-slow: 0.3s ease
```

---

## Composants réutilisables

### Conteneurs

| Classe | Usage |
|--------|-------|
| `.container` | Max 900px, padding auto (contenu principal) |
| `.container-wide` | Max 1200px (header, footer) |
| `.section-fond` | Fond principal #F6F1E8 |
| `.section-ivoire` | Boîtes claires #FFFCF5 |
| `.section-papier` | Sections secondaires #E9DDC8 |
| `.section-dark` | Texte clair sur foncé |
| `.section-cuivre` | CTA primaire full-width |

### Grilles

```html
<div class="grid-2">
  <div class="card">...</div>
  <div class="card">...</div>
</div>
```

- `.grid-2` → 1 col mobile, 2 cols @768px+
- `.grid-3` → 1 col mobile, 3 cols @768px+

### Cartes

```html
<div class="card card-with-border-left">
  <h3>Titre</h3>
  <p>Description...</p>
</div>
```

| Classe | Usage |
|--------|-------|
| `.card` | Boîte ivoire + shadow, hover lift |
| `.card-with-border-left` | Filet cuivre à gauche |
| `.card-with-border-top` | Filet cuivre en haut |
| `.card h3`, `.card p` | Couleurs auto appliquées |

### Boutons

```html
<a href="#" class="btn btn-primary">Obtenir ce système</a>
<button class="btn btn-secondary">Secondaire</button>
<button class="btn btn-dark">Foncé</button>
```

**Propriétés** : min 44×44px (accessibilité), focus visible, transitions

### Badges

```html
<span class="badge badge-cuivre">Stock bas</span>
<span class="badge badge-vert">Validation ✓</span>
<span class="badge badge-brique">Alerte !</span>
```

### Typographie utilitaires

| Classe | Utilité |
|--------|---------|
| `.text-center` | Centrage |
| `.text-cuivre`, `.text-brun`, etc. | Couleur texte |
| `.text-sm` | Font-size 0.875rem |
| `.text-lg` | Font-size 1.125rem |
| `.intro-text` | Intro centrée, couleur brun |

---

## Inventaire pages existantes

### Pages racine

| Page | Route | Lignes | Status |
|------|-------|--------|--------|
| **Accueil** | `/index.html` | ~1020 | ✅ V3 intégrée |
| **Catalogue** | `/catalogue.html` | ~1035 | ✅ V3 intégrée |
| **À propos** | `/a-propos.html` | ~700 | ✅ V3 intégrée |
| **FAQ** | `/faq.html` | ~620 | ✅ V3 intégrée |
| **Contact** | `/contact.html` | ~320 | ✅ V3 intégrée |
| **Mentions légales** | `/mentions-legales.html` | ~80 | ✅ V3 intégrée |

### Pages produits (sous-dossiers)

| Produit | Route | Lignes | Status |
|---------|-------|--------|--------|
| **Gardien de Stock** | `/gardien-de-stock/` | ~520 | ✅ V3 intégrée |
| **Signal de Vente** | `/signal-de-vente/` | ~410 | ✅ V3 intégrée |
| **Séquenceur Post-Achat** | `/sequenceur-post-achat/` | ~480 | ✅ V3 intégrée |
| **Collecteur d'Avis** | `/collecteur-avis/` | ~420 | ✅ V3 intégrée |
| **Carnet du Forgé** | `/carnet-forge/` | ~350 | ⚠️ À migrer |
| **Exemple système** | `/produit/exemple-systeme.html` | ~180 | ⚠️ Template |

**Total** : 14 fichiers HTML publiques, ~6200 lignes. Toutes racines ✅, carnet-forge à mettre en cohérence.

---

## Règles d'utilisation

### 1️⃣ Importer base.css en `<head>`

```html
<link rel="stylesheet" href="/assets/css/base.css" />
<!-- OU pour compatibilité -->
<link rel="stylesheet" href="/assets/css/design-system.css" />
```

### 2️⃣ Structure HTML type

```html
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Titre | L'établ'IA</title>

    <!-- Fontes -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://api.fontshare.com" />
    <link href="https://api.fontshare.com/v2/css?f[]=zodiak@400,700&f[]=satoshi@400,500,700&display=swap" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />

    <!-- Design System -->
    <link rel="stylesheet" href="/assets/css/base.css" />
  </head>
  <body>
    <!-- Header sticky auto-inclus dans base.css -->
    <header>
      <div class="header-content">
        <a href="/" class="logo">L'établ'IA</a>
        <nav class="nav-desktop">
          <a href="/catalogue.html">Systèmes forgés</a>
          <a href="/contact.html">Contact</a>
        </nav>
        <a href="/catalogue.html" class="cta-desktop">Trouver mon système</a>
        <button class="menu-toggle" id="menu-toggle">
          <span></span><span></span><span></span>
        </button>
      </div>
    </header>

    <!-- Menu mobile -->
    <div id="mobile-menu">
      <button class="menu-close" id="menu-close">×</button>
      <nav><!-- liens --></nav>
    </div>

    <main>
      <!-- Contenu -->
    </main>

    <footer>
      <!-- Footer standard -->
    </footer>

    <!-- Navigation JS -->
    <script src="/assets/js/nav.js" defer></script>
  </body>
</html>
```

### 3️⃣ Sections colorées

Utilisez les classes `.section-*` pour les fonds :

```html
<section class="section-fond">
  <div class="container">
    <!-- Contenu -->
  </div>
</section>

<section class="section-papier">
  <!-- Section secondaire -->
</section>

<section class="section-cuivre">
  <h2>Obtenir ce système</h2>
  <a href="#" class="btn btn-primary">19 € — Commander</a>
</section>
```

### 4️⃣ Distribution des couleurs (règle 80/15/5)

```
80% : v3-color-fond + graphite (texte principal)
15% : v3-color-papier + brun (accents secondaires)
 5% : v3-color-cuivre (CTA unique par page)
```

---

## Breakpoints responsifs

| Breakpoint | Largeur | Usage |
|------------|---------|-------|
| Mobile | < 768px | 1 colonne, padding 1rem, font plus petit |
| Tablet+ | ≥ 768px | 2-3 colonnes, padding 5rem, font ajustée |
| Desktop | ≥ 1200px | Max-width 1200px appliqué |

Tous les `.grid-*` et sections respectent ces points de rupture.

---

## Accessibilité garanties

✅ **Contraste AA minimum** → Noir (#25221D) sur clair (#F6F1E8)  
✅ **Focus visibles** → Outline cuivre 2px sur tous les éléments interactifs  
✅ **Touch targets ≥ 44px** → Boutons, liens, contrôles  
✅ **Sémantique HTML** → `<header>`, `<main>`, `<footer>`, `<button>`  
✅ **Alt textes** → À ajouter dans chaque `<img>` par la page  
✅ **Labels** → Tous les inputs doivent avoir un `<label>`

---

## Intégration quick-start

### Nouvelle page produit

```bash
# 1. Créer /mon-produit/index.html
# 2. Copier le template HTML ci-dessus
# 3. Remplacer le contenu <main>
# 4. Appliquer classes : .section-fond, .container, .card, .btn-primary
# 5. Test mobile : DevTools F12, Ctrl+Shift+M
# 6. Vérifier contraste : WebAIM, WCAG AA
```

### Modifier le design système

⚠️ **TOUS les fichiers qui importent `/assets/css/base.css` seront mises à jour automatiquement.**

Modifier `:root` pour toucher :
- Palette (6 nouvelles couleurs)
- Typographies (charger nde nouvelles fontes)
- Espacements (--radius, --max-width)
- Transitions (--transition-*)

Puis redéployer une seule fois.

---

## Support & Questions

- Variables custom incomprises ? → Chercher dans `:root`
- Composant manquant ? → Combiner `.card` + `.grid-2` + `.badge`
- Classe conflictuelle ? → Utiliser **specificity** ou ajouter `.page-*` scope

---

**Version** : V3 (2026-05-03)  
**Auteur** : L'établ'IA Design System  
**Compatibilité** : Chrome 90+, Firefox 88+, Safari 14+, iOS 14+
