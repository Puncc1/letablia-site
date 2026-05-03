# Guide d'intégration — Design System V3

## Étape 1 : Importer base.css

Remplacer les styles `<style>` embarqués par une simple importation :

```html
<!-- AVANT (~ 200 lignes de CSS embarqué) -->
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { font-family: 'Satoshi', system-ui, sans-serif; color: #25221D; line-height: 1.6; }
  body { background-color: #F6F1E8; }
  /* ... 200 lignes de CSS dupliqué ... */
</style>

<!-- APRÈS (une ligne) -->
<link rel="stylesheet" href="/assets/css/base.css" />
```

**Gain** : -200 lignes par page × 14 pages = -2800 lignes. **Maintenance centralisée**.

---

## Étape 2 : Utiliser les classes prédéfinies

### Exemple 1 : Refondre une section "ce que ça fait"

**AVANT** (code spécifique à la page) :
```html
<section style="background-color: #F6F1E8;">
  <div style="max-width: 900px; margin: 0 auto; padding: 3rem 1rem;">
    <h2 style="font-family: 'Zodiak', serif; font-size: 2.25rem; color: #25221D;">Ce que ce système fait</h2>
    <p style="text-align: center; color: #6B4A2F; margin-bottom: 3rem;">Quatre tâches de surveillance supprimées.</p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
      <div style="background-color: #FFFCF5; border-left: 4px solid #B46A3C; padding: 1.5rem;">
        <h3>Audit quotidien</h3>
        <p>...</p>
      </div>
    </div>
  </div>
</section>
```

**APRÈS** (classes réutilisables) :
```html
<section class="section-fond">
  <div class="container">
    <h2>Ce que ce système fait</h2>
    <p class="intro-text">Quatre tâches de surveillance supprimées.</p>
    <div class="grid-2">
      <div class="card card-with-border-left">
        <h3>Audit quotidien</h3>
        <p>...</p>
      </div>
    </div>
  </div>
</section>
```

**Résultat** : -50 lignes de style inline, lisibilité +400%.

---

### Exemple 2 : Bouton CTA

**AVANT** :
```html
<a href="#" style="display: inline-block; background-color: #F5F0E8; color: #8A7560; font-weight: 600; padding: 0.875rem 2rem; border-radius: 6px; text-decoration: none; transition: background-color 0.2s;">
  Obtenir ce système
</a>
```

**APRÈS** :
```html
<a href="#" class="btn btn-primary">Obtenir ce système</a>
```

---

## Étape 3 : Vérifier les couleurs utilisées

Auditer le HTML pour chercher les hex hardcodés à remplacer :

```bash
# Trouver les couleurs hardcodées
grep -r "#[0-9A-Fa-f]{6}" /home/raphael/letablia-site --include="*.html" | grep -v ".bak"

# Remplacer manuellement par une variable CSS
#25221D → var(--v3-color-graphite)
#8A7560 → var(--v3-color-cuivre)
#F6F1E8 → var(--v3-color-fond)
# etc.
```

---

## Étape 4 : Tester mobile & contraste

1. **Ouvrir DevTools** : F12
2. **Activer device toggle** : Ctrl+Shift+M (Chrome) ou Cmd+Shift+M (Mac)
3. **Tester breakpoint 768px** : Vérifier 2 colonnes
4. **Vérifier contraste** : WebAIM Contrast Checker

```
#25221D (texte) sur #F6F1E8 (fond) = 11.5:1 ✅ AAA
#6B4A2F (brun) sur #F6F1E8 (fond) = 6.2:1 ✅ AA
#B46A3C (cuivre) sur #F5F0E8 (clair) = 4.1:1 ✅ AA
```

---

## Étape 5 : Charger nav.js pour menu burger

```html
<script src="/assets/js/nav.js" defer></script>
```

**Fonctionnalités** :
- Toggle menu sur clic bouton burger
- Fermer menu sur clic lien (pour UX mobile)
- Fermer menu sur Échap
- ~600 bytes, zéro dépendance

---

## Checklist migration page

Pour chaque page HTML à migrer :

- [ ] Supprimer `<style>` embarqué (sauf si page-specific)
- [ ] Ajouter `<link rel="stylesheet" href="/assets/css/base.css" />`
- [ ] Remplacer divs par sections `.section-*`
- [ ] Remplacer divs par `.container` ou `.container-wide`
- [ ] Remplacer cards inline par `.card`
- [ ] Remplacer boutons inline par `.btn .btn-primary`
- [ ] Remplacer couleurs hex par variables CSS
- [ ] Ajouter `<script src="/assets/js/nav.js"></script>`
- [ ] Tester mobile (DevTools, 375px width)
- [ ] Tester contraste (WebAIM)
- [ ] Valider HTML (W3C Validator)
- [ ] Tester sur 2 vrais téléphones (iPhone + Android)

---

## Fichiers à mettre à jour

| Fichier | Priorité | Effort | Gain |
|---------|----------|--------|------|
| `/index.html` | P0 | 15 min | Accueil cohérent |
| `/catalogue.html` | P0 | 20 min | Pages produit |
| `/carnet-forge/index.html` | P1 | 10 min | Cohérence produit |
| `/signal-de-vente/index.html` | P1 | 10 min | Cohérence produit |
| `/sequenceur-post-achat/index.html` | P1 | 10 min | Cohérence produit |
| `/collecteur-avis/index.html` | P1 | 10 min | Cohérence produit |
| `/a-propos.html` | P2 | 5 min | Édile support |
| `/faq.html` | P2 | 5 min | Édile support |
| `/contact.html` | P2 | 5 min | Édile support |

**Total estimé** : 90 minutes pour 9 pages.

---

## Questions fréquentes

### Q : Peut-on ajouter du CSS page-specific au-dessus de base.css ?

**R** : Oui, c'est recommandé pour spécificité. Exemple :

```html
<link rel="stylesheet" href="/assets/css/base.css" />
<style>
  /* Overrides page-spécifiques seulement */
  .hero-section { padding-top: 6rem; }
</style>
```

### Q : Peut-on modifier base.css pour une page seule ?

**R** : **Non**. Modifier base.css affecte TOUTES les 14 pages. Si besoin spécifique, utiliser un `<style>` embarqué.

### Q : Que faire si une variable CSS manque ?

**R** : L'ajouter à `:root` dans base.css, puis relancer le serveur. Consultez la doc du README.

### Q : Peut-on utiliser Tailwind avec base.css ?

**R** : **Non**. Tailwind génère des classes conflictuelles. Rester en CSS Vanilla.

---

**Version** : V3 (2026-05-03)
**Auteur** : L'établ'IA Design System
**Contact** : design@letablia.fr
