# design.md — L'établ'IA — Design System V1

> **INSTRUCTION POUR CLAUDE CODE**
>
> Tu DOIS lire ce fichier design.md AVANT de générer tout code HTML/CSS/Tailwind. Chaque couleur, chaque police, chaque espacement DOIT provenir de ce fichier. Si une instruction te demande un élément visuel non défini ici, utilise l'option la plus proche définie dans ce fichier. Ne génère JAMAIS un style qui viole les Contraintes Absolues (section 5). Aucune exception.

---

## 1. PALETTE DE COULEURS

### 1.1 Couleurs principales

| Variable CSS | Classe Tailwind | HEX | Usage |
|---|---|---|---|
| `--color-chene` | `chene` | `#8A7560` | Couleur principale. Fond bouton principal, liens texte, accents, titres importants, prix, bordures d'accentuation, tagline. |
| `--color-pierre` | `pierre` | `#A09889` | Couleur secondaire. Sous-titres discrets, bordures de cartes, séparateurs, icônes inactives, texte footer secondaire, légendes. |
| `--color-mousse` | `mousse` | `#7A8E7A` | Accent ponctuel. États de succès, confirmations, encadrés info (prérequis), badges. Usage parcimonieux uniquement. |
| `--color-lin` | `lin` | `#F4F0EA` | Neutre clair. Fond principal de toutes les pages. Texte sur fond foncé (boutons, sections Ébène). Remplace le blanc pur. |
| `--color-ebene` | `ebene` | `#3A3530` | Neutre foncé. Texte courant, fond de sections contrastées (hero chiffré, comment ça marche, footer). Remplace le noir pur. |

### 1.2 Couleurs interdites

| Couleur | Code | Raison |
|---|---|---|
| Blanc pur | `#FFFFFF` | Interdit. Utiliser Lin `#F4F0EA` à la place. |
| Noir pur | `#000000` | Interdit. Utiliser Ébène `#3A3530` à la place. |
| Câble | `~#5BC0EB` | Réservé au logo et à la mascotte Blibot. Interdit dans l'interface. |
| Forge | `~#E08B3A` | Réservé au logo et à la mascotte Blibot. Interdit dans l'interface. |
| Toute autre couleur | — | Aucune couleur en dehors de cette palette n'est autorisée. |

### 1.3 Variantes d'opacité

| Variable CSS | Classe Tailwind | Valeur | Usage |
|---|---|---|---|
| `--color-chene-6` | `chene-6` | `#8A7560` à 6% opacité | Fond sections réassurance, blocs info. |
| `--color-chene-8` | `chene-8` | `#8A7560` à 8% opacité | Hover bouton secondaire, fond carte produit (optionnel). |
| `--color-pierre-10` | `pierre-10` | `#A09889` à 10% opacité | Fond cartes catégorie, fond cartes produit. |
| `--color-pierre-30` | `pierre-30` | `#A09889` à 30% opacité | Bordure du séparateur copyright (footer). |
| `--color-mousse-10` | `mousse-10` | `#7A8E7A` à 10% opacité | Encadré info (prérequis « pas nécessaire »). |
| `--color-ebene-80` | `ebene-80` | `#3A3530` à 80% opacité | Fond cartes bundle (sur fond Ébène). |
| `--color-lin-85` | `lin-85` | `#F4F0EA` à 85% opacité | Sous-titre sur fond Chêne (CTA final). |

### 1.4 Configuration Tailwind

```
// tailwind.config.js — section colors
colors: {
  'chene':      '#8A7560',
  'chene-6':    'rgba(138, 117, 96, 0.06)',
  'chene-8':    'rgba(138, 117, 96, 0.08)',
  'pierre':     '#A09889',
  'pierre-10':  'rgba(160, 152, 137, 0.10)',
  'pierre-30':  'rgba(160, 152, 137, 0.30)',
  'mousse':     '#7A8E7A',
  'mousse-10':  'rgba(122, 142, 122, 0.10)',
  'lin':        '#F4F0EA',
  'lin-85':     'rgba(244, 240, 234, 0.85)',
  'ebene':      '#3A3530',
  'ebene-80':   'rgba(58, 53, 48, 0.80)',
}
```

---

## 2. TYPOGRAPHIES

### 2.1 Import Google Fonts

```
https://fonts.googleapis.com/css2?family=Bitter:wght@400;500;700&family=DM+Serif+Display&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&display=swap
```

### 2.2 Familles et fallbacks

| Variable CSS | Police | Fallback | Classe Tailwind |
|---|---|---|---|
| `--font-heading` | `Bitter` | `Georgia, serif` | `font-heading` |
| `--font-body` | `Source Sans 3` | `system-ui, sans-serif` | `font-body` |
| `--font-display` | `DM Serif Display` | `Georgia, serif` | `font-display` |

### 2.3 Configuration Tailwind

```
// tailwind.config.js — section fontFamily
fontFamily: {
  'heading': ['Bitter', 'Georgia', 'serif'],
  'body':    ['Source Sans 3', 'system-ui', 'sans-serif'],
  'display': ['DM Serif Display', 'Georgia', 'serif'],
}
```

### 2.4 Échelle typographique complète

| Rôle | Police | Graisse | Taille desktop | Taille mobile | Interligne | Couleur par défaut | Classe Tailwind (taille) |
|---|---|---|---|---|---|---|---|
| H1 — Titre principal | Bitter | Bold (700) | 36–40px | 28px | 1.2 | Ébène `#3A3530` | `text-4xl` desktop / `text-3xl` mobile |
| H2 — Titre de section | Bitter | Bold (700) | 28–32px | 22px | 1.2 | Ébène `#3A3530` | `text-3xl` desktop / `text-2xl` mobile |
| H3 — Titre carte / sous-section | Bitter | Medium (500) | 20–24px | 18px | 1.2 | Ébène `#3A3530` | `text-xl` desktop / `text-lg` mobile |
| Corps | Source Sans 3 | Regular (400) | 16–18px | 16px | 1.6 | Ébène `#3A3530` | `text-base` ou `text-lg` |
| Corps emphase | Source Sans 3 | Semibold (600) | 16–18px | 16px | 1.6 | Ébène `#3A3530` | `text-base font-semibold` |
| Légendes / micro-texte | Source Sans 3 | Regular (400) | 12–14px | 12px | 1.6 | Pierre `#A09889` | `text-xs` ou `text-sm` |
| Catégorie label | Source Sans 3 | Semibold (600) | 13px | 13px | 1.6 | Chêne `#8A7560` | `text-xs font-semibold uppercase` |
| Tagline / nom de marque | DM Serif Display | Regular (400) | 24px | 20px | 1.2 | Chêne `#8A7560` | `text-2xl` desktop / `text-xl` mobile |
| Chiffres-clés | DM Serif Display | Regular (400) | 48–64px | 36px | 1.0 | Chêne `#8A7560` | `text-5xl` à `text-6xl` desktop / `text-4xl` mobile |
| Prix | DM Serif Display | Regular (400) | 24–32px | 24px | 1.0 | Chêne `#8A7560` | `text-2xl` à `text-3xl` |

### 2.5 Règle d'usage des polices

- **Bitter** : tous les titres (H1, H2, H3). Jamais dans le corps de texte.
- **Source Sans 3** : tout le texte courant, boutons, légendes, navigation. Police par défaut.
- **DM Serif Display** : réservée strictement au logotype, à la tagline « Forgé pour votre métier », aux chiffres-clés et aux prix. Jamais dans les titres de section ni dans le corps de texte.
- Maximum 2 polices par page (Bitter + Source Sans 3). DM Serif Display intervient uniquement pour les éléments listés ci-dessus.

---

## 3. ESPACEMENTS

### 3.1 Espacements entre sections

| Élément | Desktop | Mobile | Variable CSS |
|---|---|---|---|
| Espacement vertical entre sections | 80–120px | 48px | `--spacing-section` |
| Marge entre titre et sous-titre | 12–16px | 12px | `--spacing-title-subtitle` |
| Marge entre sous-titre et corps | 16–24px | 16px | `--spacing-subtitle-body` |
| Marge entre corps et CTA | 24–32px | 24px | `--spacing-body-cta` |

### 3.2 Conteneurs

| Élément | Desktop | Mobile | Variable CSS |
|---|---|---|---|
| Largeur max du contenu | 1200px | 100% | `--container-max` |
| Padding horizontal du conteneur | centré auto | 16px de chaque côté | `--container-padding` |
| Largeur max texte seul (colonne étroite) | 720px | 100% - 32px | `--container-narrow` |

### 3.3 Composants

| Élément | Desktop | Mobile | Variable CSS |
|---|---|---|---|
| Padding interne des cartes | 24px | 16px | `--card-padding` |
| Espacement entre cartes (gap grille) | 24px | 16px | `--card-gap` |
| Padding interne des boutons | 14px 28px | 14px 24px | `--btn-padding` |
| Padding bouton compact (header) | 10px 20px | 10px 20px | `--btn-padding-compact` |
| Padding interne blocs info/réassurance | 20–24px | 16px | `--block-padding` |

### 3.4 Breakpoint responsive

| Breakpoint | Valeur | Comportement |
|---|---|---|
| Mobile → Desktop | 768px | Sous 768px : colonnes empilées, tailles mobile, padding 16px latéral. |

### 3.5 Règles mobile spécifiques

- Toutes les dispositions 2 ou 3 colonnes → colonne unique sous 768px.
- Cartes empilées verticalement avec gap de 16px.
- Boutons → pleine largeur (`width: 100%`).
- Deux boutons côte à côte → empilés verticalement.
- Header → menu hamburger (icône 3 barres Ébène). Menu ouvert : fond Lin, liens centrés verticalement.
- Footer → 3 colonnes empilées, logo et tagline centrés.

---

## 4. COMPOSANTS

### 4.1 Bouton principal

| Propriété | Valeur |
|---|---|
| Fond | Chêne `#8A7560` |
| Texte | Lin `#F4F0EA` |
| Police | Source Sans 3 Semibold 16px |
| Padding | 14px 28px (mobile : 14px 24px) |
| Border-radius | 6px |
| Bordure | aucune |
| Hover | Chêne assombri (opacité 90%) |
| Ombre | aucune |
| Dégradé | aucun |

### 4.2 Bouton secondaire

| Propriété | Valeur |
|---|---|
| Fond | transparent |
| Texte | Chêne `#8A7560` |
| Police | Source Sans 3 Semibold 16px |
| Bordure | Chêne `#8A7560` solid 1px |
| Padding | 14px 28px (mobile : 14px 24px) |
| Border-radius | 6px |
| Hover | fond Chêne à 8% opacité (`rgba(138, 117, 96, 0.08)`) |
| Ombre | aucune |
| Dégradé | aucun |

### 4.3 Bouton secondaire inversé (fond foncé)

| Propriété | Valeur |
|---|---|
| Fond | Lin `#F4F0EA` |
| Texte | Chêne `#8A7560` |
| Police | Source Sans 3 Semibold 16px |
| Padding | 14px 28px |
| Border-radius | 6px |
| Bordure | aucune |
| Ombre | aucune |

### 4.4 Bouton compact (header)

| Propriété | Valeur |
|---|---|
| Fond | Chêne `#8A7560` |
| Texte | Lin `#F4F0EA` |
| Police | Source Sans 3 Semibold 16px |
| Padding | 10px 20px |
| Border-radius | 6px |

### 4.5 Liens texte

| Propriété | Valeur |
|---|---|
| Couleur | Chêne `#8A7560` |
| Hover | soulignement (text-decoration: underline) |
| Police | hérite du contexte parent |

### 4.6 Liens de navigation — header

| Propriété | Valeur |
|---|---|
| Couleur | Ébène `#3A3530` |
| Hover | Chêne `#8A7560` |
| Police | Source Sans 3 Regular 16px |

### 4.7 Liens de navigation — footer

| Propriété | Valeur |
|---|---|
| Couleur | Lin `#F4F0EA` |
| Hover | Chêne `#8A7560` |
| Police | Source Sans 3 Regular 16px |

### 4.8 Carte standard (produit, catégorie)

| Propriété | Valeur |
|---|---|
| Fond | Lin `#F4F0EA` |
| Bordure | Pierre `#A09889` solid 1px |
| Border-radius | 8px |
| Padding | 24px (mobile : 16px) |
| Ombre | aucune |

### 4.9 Carte catégorie (variante fond clair)

| Propriété | Valeur |
|---|---|
| Fond | Pierre à 10% opacité (`rgba(160, 152, 137, 0.10)`) |
| Bordure | Pierre `#A09889` solid 1px |
| Border-radius | 6px |
| Padding | 24px (mobile : 16px) |

### 4.10 Carte bundle (fond foncé)

| Propriété | Valeur |
|---|---|
| Fond | Ébène à 80% opacité (`rgba(58, 53, 48, 0.80)`) |
| Bordure | Chêne `#8A7560` solid 1px |
| Border-radius | 8px |
| Padding | 24px |

### 4.11 Bloc réassurance

| Propriété | Valeur |
|---|---|
| Fond | Chêne à 6% opacité (`rgba(138, 117, 96, 0.06)`) |
| Bordure | aucune |
| Border-radius | 6px |
| Padding | 24px (mobile : 16px) |

### 4.12 Encadré info Mousse (prérequis)

| Propriété | Valeur |
|---|---|
| Fond | Mousse à 10% opacité (`rgba(122, 142, 122, 0.10)`) |
| Bordure gauche | Mousse `#7A8E7A` solid 3px |
| Border-radius | 4px |
| Padding | 20–24px (mobile : 16px) |

### 4.13 Cadre capture de résultat (placeholder)

| Propriété | Valeur |
|---|---|
| Fond | Lin `#F4F0EA` |
| Bordure | Pierre `#A09889` solid 1px |
| Border-radius | 8px |
| Padding | 24px |

### 4.14 Bordures spécifiques

| Élément | Style |
|---|---|
| Séparateur sous titre de catégorie | Pierre `#A09889` solid 1px, largeur 60px |
| Bordure basse header | Pierre `#A09889` solid 1px |
| Séparateur copyright footer | Pierre à 30% opacité solid 1px |
| Bordure basse question FAQ | Pierre `#A09889` solid 1px |

### 4.15 Rayons de bordure — référence

| Élément | Border-radius |
|---|---|
| Boutons | 6px |
| Cartes (produit, catégorie, bundle) | 8px |
| Blocs info / réassurance | 6px |
| Cadres capture de résultat | 8px |
| Encadré Mousse (prérequis) | 4px |
| Maximum absolu | 8px — ne jamais dépasser |

---

## 5. CONTRAINTES ABSOLUES — RÈGLES ANTI-AI-SLOP

**Ces règles sont ABSOLUES et SANS EXCEPTION. Toute violation est un défaut critique.**

### INTERDICTIONS

1. **PAS de `box-shadow`** — Aucune ombre portée. Aucun `box-shadow` sur aucun élément. Pas de classe Tailwind `shadow-*`.
2. **PAS de `backdrop-filter`** — Aucun effet de verre, de flou, de glassmorphism. Pas de `blur()`, `saturate()`, ni aucune valeur de `backdrop-filter`.
3. **PAS de `linear-gradient` ni `radial-gradient`** — Aucun dégradé. Pas de classe Tailwind `bg-gradient-*`. Tous les fonds sont des couleurs pleines ou des couleurs avec opacité.
4. **PAS de `filter` ni `opacity` pour effets décoratifs** — Ne pas utiliser `filter: blur()`, `brightness()`, `contrast()` pour créer des effets visuels. L'opacité est autorisée UNIQUEMENT sur les variantes de couleur définies en section 1.3.
5. **PAS de `transform: scale()` ou `transform: rotate()` à des fins décoratives** — Aucune transformation visuelle décorative.
6. **PAS de couleur hors palette** — Chaque couleur utilisée DOIT être l'une des couleurs listées en section 1.1 ou 1.3. Aucune couleur inventée, aucun gris arbitraire, aucun bleu, rouge, ou autre teinte.
7. **PAS de blanc pur `#FFFFFF`** — Utiliser Lin `#F4F0EA`.
8. **PAS de noir pur `#000000`** — Utiliser Ébène `#3A3530`.
9. **PAS de typographie hors liste** — Seules Bitter, Source Sans 3 et DM Serif Display sont autorisées. Pas d'Arial, Helvetica, Inter, Roboto, ni aucune autre police.
10. **PAS de `border-radius` supérieur à 8px** — Le maximum absolu est 8px. Pas de `rounded-full`, `rounded-xl`, `rounded-2xl`, `rounded-3xl`. Pas de formes circulaires.
11. **PAS d'animations ni de transitions en V1** — Aucun `transition`, `animation`, `@keyframes`, `transform` animé. **Seule exception** : `transition: color 0.2s ease` sur les boutons au hover, et `transition: color 0.2s ease` sur les liens de navigation au hover.
12. **PAS d'emojis dans l'interface** — Aucun emoji dans le HTML rendu.
13. **PAS d'icônes décoratives en V1** — Pas d'icônes dans les cartes catégorie ni dans les blocs de réassurance. Le contenu textuel suffit.
14. **PAS de couleurs saturées ou vives** — Toute la palette est terreuse et désaturée. Si une couleur semble vive ou électrique, elle n'appartient pas à cette marque.

### AUTORISATIONS EXPLICITES

- Fonds plats en couleur de la palette uniquement.
- Bordures fines et discrètes (1px, couleur Pierre ou Chêne).
- Opacités sur les couleurs existantes pour créer de la profondeur (section 1.3 uniquement).
- `transition: color 0.2s ease` sur boutons et liens de navigation au hover.
- Soulignement (`text-decoration: underline`) sur les liens texte au hover.

---

## 6. HEADER & FOOTER

### 6.1 Header (toutes les pages)

| Propriété | Valeur |
|---|---|
| Fond | Lin `#F4F0EA` |
| Hauteur | 72px |
| Largeur contenu | max 1200px, centré |
| Position | sticky (fixe en haut) |
| Bordure basse | Pierre `#A09889` solid 1px |
| Logo (gauche) | Lockup horizontal : symbole IA + « L'établ'IA » en DM Serif Display Regular, couleur Chêne `#8A7560`. Lien vers `/` |
| Navigation (centre) | Source Sans 3 Regular 16px, couleur Ébène `#3A3530`. Hover : Chêne `#8A7560` |
| CTA (droite) | Bouton compact (voir section 4.4) → `/catalogue` |
| Mobile (< 768px) | Menu hamburger : icône 3 barres Ébène. Menu ouvert plein écran : fond Lin, liens centrés verticalement. CTA « Voir le catalogue » visible dans le menu. |

### 6.2 Footer (toutes les pages)

| Propriété | Valeur |
|---|---|
| Fond | Ébène `#3A3530` |
| Largeur contenu | max 1200px, centré |
| Disposition | 3 colonnes + ligne copyright |
| Colonne 1 | Lockup petit Lin `#F4F0EA` + tagline DM Serif Display Regular 14px Pierre `#A09889` |
| Colonne 2 | Titre « NAVIGATION » Source Sans 3 Semibold 13px Pierre uppercase + liens Source Sans 3 Regular 16px Lin |
| Colonne 3 | Titre « INFORMATIONS » Source Sans 3 Semibold 13px Pierre uppercase + liens Source Sans 3 Regular 16px Lin |
| Séparateur copyright | Pierre à 30% opacité, solid 1px |
| Copyright | Source Sans 3 Regular 12px Pierre `#A09889` |
| Mobile (< 768px) | 3 colonnes empilées, logo et tagline centrés |

---

*— Fin du fichier design.md — Version 1.0 — Mars 2026 —*
