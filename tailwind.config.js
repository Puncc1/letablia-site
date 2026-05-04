module.exports = {
  content: ["*.html", "**/*.html"],
  theme: {
    extend: {
      colors: {
        // Design System V4 OFFICIEL — palette matières premières
        // Source : SESSION-FONDATRICE-2026-05-03 D15 + design-system-v4.md
        'chene':      '#8A7560',  // Primaire — liens, icônes, prix, accents
        'chene-6':    'rgba(138, 117, 96, 0.06)',
        'chene-8':    'rgba(138, 117, 96, 0.08)',
        'chene-15':   'rgba(138, 117, 96, 0.15)',
        'pierre':     '#B8AFA6',  // Neutre — textes secondaires, séparateurs
        'pierre-10':  'rgba(184, 175, 166, 0.10)',
        'pierre-30':  'rgba(184, 175, 166, 0.30)',
        'pierre-50':  'rgba(184, 175, 166, 0.50)',
        'mousse':     '#6B7C5F',  // Action — CTA, états actifs, validation
        'mousse-10':  'rgba(107, 124, 95, 0.10)',
        'mousse-20':  'rgba(107, 124, 95, 0.20)',
        'lin':        '#F2EDE8',  // Surface — cartes, fond hero, sections
        'lin-85':     'rgba(242, 237, 232, 0.85)',
        'lin-50':     'rgba(242, 237, 232, 0.50)',
        'ebene':      '#2C2825',  // Texte — titres, corps, contrastes forts
        'ebene-80':   'rgba(44, 40, 37, 0.80)',
        'ebene-60':   'rgba(44, 40, 37, 0.60)',
      },
      fontFamily: {
        // Typographie V4 OFFICIELLE
        'heading': ['"Playfair Display"', 'Georgia', 'serif'],
        'body':    ['Inter', 'system-ui', 'sans-serif'],
        'display': ['"Playfair Display"', 'Georgia', 'serif'],
        'mono':    ['"JetBrains Mono"', 'monospace'],
      },
      letterSpacing: {
        'titre': '-0.02em',  // titres serif resserrés
      },
    },
  },
  plugins: [],
}
