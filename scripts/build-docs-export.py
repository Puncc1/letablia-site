#!/usr/bin/env python3
"""
build-docs-export.py — Génère ~/letablia-site/docs-export/ et un .zip pour outils externes.

Tout en HTML pour pouvoir être ouvert sans dépendance.
"""
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORT = ROOT / "docs-export"
DATA = json.loads((ROOT / "assets" / "data" / "products.json").read_text())
TODAY = datetime.now().strftime("%Y-%m-%d")

# ─────────────────────────── Style commun ────────────────────────────
COMMON_CSS = """
:root{
  --chene:#8A7560; --pierre:#B8AFA6; --mousse:#6B7C5F;
  --lin:#F2EDE8; --ebene:#2C2825;
}
*{box-sizing:border-box}
body{
  font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
  background:var(--lin); color:var(--ebene); margin:0; line-height:1.6;
}
.container{max-width:920px;margin:0 auto;padding:32px 24px}
h1,h2,h3{font-family:'Playfair Display',Georgia,serif;color:var(--ebene);letter-spacing:-0.02em}
h1{font-size:2.4rem;border-bottom:3px solid var(--chene);padding-bottom:12px;margin-top:0}
h2{font-size:1.8rem;margin-top:40px;color:var(--chene)}
h3{font-size:1.3rem;margin-top:28px}
code,pre{font-family:'JetBrains Mono',Consolas,monospace;font-size:0.92em}
pre{background:#fffbf5;border-left:4px solid var(--chene);padding:14px 18px;overflow-x:auto;border-radius:4px}
code{background:rgba(138,117,96,0.10);padding:2px 6px;border-radius:3px}
pre code{background:transparent;padding:0}
table{border-collapse:collapse;width:100%;margin:16px 0;background:#fff;border-radius:6px;overflow:hidden;box-shadow:0 1px 3px rgba(44,40,37,0.08)}
th,td{padding:10px 14px;text-align:left;border-bottom:1px solid var(--pierre);vertical-align:top}
th{background:var(--chene);color:var(--lin);font-weight:600;font-size:0.92em;text-transform:uppercase;letter-spacing:0.05em}
tr:last-child td{border-bottom:none}
.swatch{display:inline-block;width:18px;height:18px;border-radius:4px;vertical-align:middle;margin-right:8px;border:1px solid rgba(0,0,0,0.1)}
nav.toc{background:#fff;border:1px solid var(--pierre);border-radius:6px;padding:18px 24px;margin-bottom:24px}
nav.toc ul{margin:8px 0 0 0;padding-left:20px}
nav.toc li{margin:4px 0}
nav.toc a{color:var(--chene);text-decoration:none}
nav.toc a:hover{text-decoration:underline}
.tag{display:inline-block;background:var(--mousse);color:var(--lin);padding:2px 10px;border-radius:99px;font-size:0.78em;margin-right:6px;text-transform:uppercase;letter-spacing:0.05em}
.callout{background:rgba(107,124,95,0.10);border-left:4px solid var(--mousse);padding:12px 18px;margin:18px 0;border-radius:4px}
.callout strong{color:var(--mousse)}
.warning{background:rgba(140,63,50,0.08);border-left:4px solid #8C3F32;padding:12px 18px;margin:18px 0;border-radius:4px}
ul,ol{padding-left:24px}
li{margin:4px 0}
hr{border:none;border-top:1px solid var(--pierre);margin:32px 0}
.back{display:inline-block;margin-bottom:16px;color:var(--mousse);text-decoration:none;font-weight:600}
.back:hover{text-decoration:underline}
.product-card-preview{display:inline-block;width:280px;border:1px solid var(--pierre);border-radius:8px;overflow:hidden;margin:8px;background:#fff;vertical-align:top}
.product-card-preview .ribbon{background:rgba(138,117,96,0.06);height:60px;display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;font-size:0.7em;letter-spacing:0.15em;color:var(--chene)}
.product-card-preview .body{padding:16px}
.product-card-preview h4{font-family:'Playfair Display',serif;font-size:1.2em;margin:0 0 6px}
.product-card-preview .blurb{color:var(--pierre);font-size:0.88em;margin:0 0 10px}
.product-card-preview .price{font-family:'JetBrains Mono',monospace;color:var(--chene);font-weight:700}
"""

def page(title, body, with_back=True):
    back = '<a class="back" href="index.html">← Retour à l\'index</a>' if with_back else ''
    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — L'établ'IA · Documentation</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{COMMON_CSS}</style>
</head><body>
<div class="container">
{back}
{body}
</div></body></html>"""


# ─────────────────────────── 0. Index ────────────────────────────
def make_index():
    items = [
        ("01-architecture.html", "Architecture du site", "Structure des pages, dossiers, technologies"),
        ("02-design-system.html", "Design System V4", "Palette de couleurs, typographies, principes visuels"),
        ("03-vocabulaire-marque.html", "Vocabulaire de marque", "Mots à utiliser, mots à éviter, ton et voix"),
        ("04-politique-forge.html", "Politique « Satisfait ou Forgé »", "Règles de remboursement, support, garantie"),
        ("05-catalogue.html", "Catalogue produits", "11 systèmes forgés + 3 packs · prix, blurb, cibles"),
        ("06-personas-cibles.html", "Personas et cibles", "E-commerçant, Freelance, TPE généraliste"),
        ("07-ergonomie.html", "Ergonomie et chemins d'accès", "3 entrées : Famille, Outil, Recherche"),
        ("08-header-footer.html", "Header + Footer canoniques", "Code HTML à reproduire à l'identique"),
        ("09-composants.html", "Composants et cards", "Cards produit, cards bundle, dropdown"),
        ("10-scripts-build.html", "Scripts de construction", "products.json comme source unique"),
        ("11-fiches-produits.html", "Fiches produit", "Structure des 11 fiches détaillées"),
        ("12-pages-legales.html", "Pages légales", "CGV, mentions, confidentialité"),
        ("13-bugs-resolus.html", "12 bugs résolus 2026-05-04", "Diagnostic et corrections"),
    ]
    li = "\n".join(f'<li><a href="{href}">{title}</a> — <span style="color:var(--pierre)">{desc}</span></li>' for href, title, desc in items)

    body = f"""<h1>L'établ'IA — letablia.fr · Documentation complète</h1>
<p>Version au {TODAY}. Site en ligne : <a href="https://www.letablia.fr">letablia.fr</a>.</p>

<div class="callout">
<strong>Comment utiliser cette documentation</strong> :
Cette archive contient toute l'information nécessaire pour redessiner letablia.fr avec un outil externe (Figma, v0, Webflow, autre IA). Tout est en HTML pour ouverture sans dépendance.<br><br>
Si vous donnez ces fichiers à une IA de design, commencez par <code>02-design-system.html</code>, <code>03-vocabulaire-marque.html</code> et <code>05-catalogue.html</code>.
</div>

<h2>Sommaire</h2>
<nav class="toc">
<ul>{li}</ul>
</nav>

<h2>Sources brutes</h2>
<p>Le dossier <code>sources/</code> contient :</p>
<ul>
<li><code>products.json</code> — Source unique de vérité (prix, blurbs, tools, bundles, personas)</li>
<li><code>tailwind.config.js</code> — Configuration Tailwind avec palette V4 et typographies</li>
<li><code>header-canonique.html</code> — Code HTML du header à reproduire</li>
<li><code>footer-canonique.html</code> — Code HTML du footer à reproduire</li>
<li><code>burger-menu.js</code>, <code>search-modal.js</code>, <code>catalogue-filters.js</code>, <code>cookies.js</code> — Scripts JS</li>
<li><code>output.css</code> — CSS Tailwind compilé minifié</li>
</ul>

<h2>Le dossier exemples-fiches/</h2>
<p>Les 11 fiches produit complètes en HTML, exactement comme elles tournent sur letablia.fr.</p>

<hr>
<p style="color:var(--pierre);font-size:0.88em;text-align:center">
L'établ'IA — Forgé pour votre métier · {TODAY}
</p>
"""
    (EXPORT / "index.html").write_text(page("Documentation", body, with_back=False))


# ───────────────────────── 1. Architecture ──────────────────────────
def make_architecture():
    body = """<h1>01 · Architecture du site</h1>

<h2>Vue d'ensemble</h2>
<p>Site statique HTML + CSS + JS vanilla, déployé sur Vercel (suit deux branches : <code>main</code> et <code>master</code>).</p>

<table>
<tr><th>Couche</th><th>Choix technique</th><th>Justification</th></tr>
<tr><td>Frontend</td><td>HTML statique</td><td>Performance, SEO, simplicité, pas de framework JS</td></tr>
<tr><td>CSS</td><td>Tailwind CSS v3.4 compilé</td><td>Utility-first, palette personnalisée V4, ~18KB minifié</td></tr>
<tr><td>JavaScript</td><td>Vanilla, scripts isolés</td><td>Pas de bundler, chaque script &lt; 200 lignes, defer</td></tr>
<tr><td>Hébergement</td><td>Vercel</td><td>Gratuit, déploiement git auto, headers sécurité</td></tr>
<tr><td>Source de vérité</td><td>products.json</td><td>Prix, blurbs, tools, bundles, personas — régénéré par script Python</td></tr>
</table>

<h2>Structure des dossiers</h2>
<pre><code>letablia-site/
├── index.html              # Home — hero + 5 familles + 3 personas + 3 best-sellers
├── catalogue.html          # Catalogue — 14 cards (11 produits + 3 packs) + filtres
├── a-propos.html           # À propos
├── faq.html                # FAQ
├── contact.html            # Contact
├── diagnostic.html         # Formulaire diagnostic 6 champs
├── cgv.html                # Conditions générales de vente
├── mentions-legales.html
├── confidentialite.html
│
├── produits/               # 5 pages catégories familles
│   ├── automatisations/    # « Automatiser »
│   ├── vendre/             # « Vendre »
│   ├── tableaux-de-bord/   # « Piloter »
│   ├── modeles/            # « Produire »
│   └── guides-formations/  # « Sécuriser »
│
├── packs/                  # 3 pages bundles (économie 18 €/pack)
│   ├── e-commerce/
│   ├── freelance/
│   └── tpe-conformite/
│
├── signal-de-vente/        # Fiches produit (chemin court)
├── gardien-de-stock/
├── sequenceur-post-achat/
├── collecteur-avis/
├── carnet-forge/
│
├── produit/                # Fiches produit (chemin long, héritage)
│   ├── relance-prospects/
│   ├── mini-crm-notion/
│   ├── dashboard-tresorerie/
│   ├── cyber-hygiene-tpe/
│   ├── kit-facturation-2026/
│   └── agent-tri-email/
│
├── assets/
│   ├── css/cookies.css     # Bannière cookies V4 RGPD
│   ├── data/products.json  # SOURCE UNIQUE
│   └── js/
│       ├── burger-menu.js       # Menu mobile
│       ├── catalogue-filters.js # Filtres + tri + URL params
│       ├── search-modal.js      # Cmd+K / / / clic ⌕ — fuzzy search
│       └── cookies.js           # Bannière cookies
│
├── styles/
│   ├── input.css           # Tailwind directives
│   └── output.css          # CSS compilé (18KB minifié)
│
├── scripts/                # Scripts Python de build
│   ├── build-from-json.py        # Régénère catalogue + 5 familles + prix
│   ├── anonymize-brands.py       # Sed marques → catégories génériques
│   ├── inject-canonical-shell.py # Header + footer uniformes
│   └── fix-policy.py             # Politique « Satisfait ou Forgé »
│
├── tailwind.config.js      # Palette V4 + typographies
├── package.json            # Scripts npm (build:css, watch:css)
└── vercel.json             # Headers sécurité Vercel
</code></pre>

<h2>Comportements clés</h2>
<ul>
<li><strong>Source unique</strong> : Toutes les pages dérivent de <code>products.json</code>. On ne copie-colle JAMAIS un prix, un blurb ou un nom d'outil. On régénère.</li>
<li><strong>Anonymisation marques</strong> : Aucune marque tierce ne doit apparaître côté visiteur. <code>Shopify → plateforme e-commerce</code>, <code>Notion → application de prise de notes</code>, etc.</li>
<li><strong>Bilingue catalogue</strong> : 3 chemins d'accès — Famille (5), Outil (7 catégories), Recherche (Cmd+K).</li>
<li><strong>Header + footer canoniques</strong> : Identiques sur les 40 pages, injectés par script.</li>
</ul>
"""
    (EXPORT / "01-architecture.html").write_text(page("Architecture", body))


# ─────────────────────────── 2. Design System ───────────────────────────
def make_design_system():
    body = """<h1>02 · Design System V4</h1>

<h2>Palette officielle</h2>
<p>Source : <code>~/etablia/système/SESSION-FONDATRICE-2026-05-03.md</code> D15 + <code>fabrique/projets/letablia-v3/design/design-system-v4.md</code>.</p>

<table>
<tr><th>Nom</th><th>Hex</th><th>Rôle</th><th>Aperçu</th></tr>
<tr><td><code>chene</code></td><td><code>#8A7560</code></td><td>Primaire — liens, icônes, prix, accents</td><td><span class="swatch" style="background:#8A7560"></span>Bois travaillé</td></tr>
<tr><td><code>pierre</code></td><td><code>#B8AFA6</code></td><td>Neutre — textes secondaires, séparateurs</td><td><span class="swatch" style="background:#B8AFA6"></span>Beige minéral</td></tr>
<tr><td><code>mousse</code></td><td><code>#6B7C5F</code></td><td>Action — CTA, états actifs, validation</td><td><span class="swatch" style="background:#6B7C5F"></span>Vert mousse</td></tr>
<tr><td><code>lin</code></td><td><code>#F2EDE8</code></td><td>Surface — cartes, fond hero, sections</td><td><span class="swatch" style="background:#F2EDE8"></span>Lin clair</td></tr>
<tr><td><code>ebene</code></td><td><code>#2C2825</code></td><td>Texte — titres, corps, contrastes forts</td><td><span class="swatch" style="background:#2C2825"></span>Ébène profond</td></tr>
</table>

<h3>Variantes alpha (overlays)</h3>
<table>
<tr><th>Nom</th><th>Couleur</th><th>Rôle</th></tr>
<tr><td><code>chene-6</code></td><td>rgba(138,117,96,0.06)</td><td>Background subtil sur cards inactives</td></tr>
<tr><td><code>chene-8</code></td><td>rgba(138,117,96,0.08)</td><td>Hover light</td></tr>
<tr><td><code>chene-15</code></td><td>rgba(138,117,96,0.15)</td><td>Borders accent</td></tr>
<tr><td><code>pierre-30</code></td><td>rgba(184,175,166,0.30)</td><td>Borders standard</td></tr>
<tr><td><code>mousse-10</code></td><td>rgba(107,124,95,0.10)</td><td>Background bloc CTA secondaire</td></tr>
<tr><td><code>ebene-80</code></td><td>rgba(44,40,37,0.80)</td><td>Texte body</td></tr>
</table>

<h2>Typographies</h2>
<table>
<tr><th>Stack</th><th>Police</th><th>Usage</th></tr>
<tr><td><code>font-heading</code> / <code>font-display</code></td><td>Playfair Display 400/700</td><td>Titres H1-H4, logo « L'établ'IA », accents éditoriaux</td></tr>
<tr><td><code>font-body</code></td><td>Inter 400/500/600/700</td><td>Corps de texte, navigation, boutons</td></tr>
<tr><td><code>font-mono</code></td><td>JetBrains Mono 400/500</td><td>Prix, ribbons, méta-données, étiquettes UPPERCASE</td></tr>
</table>

<h3>Letter spacing</h3>
<ul>
<li><code>letter-spacing:-0.02em</code> sur titres serif (resserrement éditorial)</li>
<li><code>letter-spacing:0.05em à 0.15em</code> sur ribbons UPPERCASE en mono</li>
</ul>

<h2>Principes visuels</h2>

<h3>Esprit « Atelier d'artisan numérique »</h3>
<ul>
<li>Palette terreuse, matérielle (bois, lin, mousse, pierre) — pas de néon, pas de flashy</li>
<li>Serif éditorial (Playfair) sur titres pour ancrer l'aspect « fait main »</li>
<li>Mono sur prix et étiquettes pour le contraste « registre comptable d'artisan »</li>
<li>Espaces blancs généreux — site qui respire, pas dense</li>
<li>Bordures fines (1px) plutôt qu'ombres marquées</li>
<li>Border-radius modérés (6-8px) — pas de pilule UI moderne</li>
</ul>

<h3>À ÉVITER</h3>
<div class="warning">
<strong>Anti-patterns visuels (incident DR-7 2026-05-02)</strong> :
<ul>
<li>Jamais de gradients colorés flashy</li>
<li>Jamais de glassmorphism ou neumorphism</li>
<li>Jamais d'ombres dramatiques (max <code>shadow-md</code>)</li>
<li>Jamais d'emoji décoratif dans le contenu — uniquement des SVG icons inline</li>
<li>Jamais de typo Google Sans / Roboto / Open Sans — toujours Inter + Playfair Display + JetBrains Mono</li>
<li>Jamais de bleu corporate / orange startup — toujours la palette terreuse</li>
</ul>
</div>

<h2>Espacements et tailles</h2>
<ul>
<li>Container max-widths : <code>max-w-[720px]</code> (texte long), <code>max-w-[1100px]</code> (sections classiques), <code>max-w-[1280px]</code> (header + grille)</li>
<li>Padding sections : <code>py-12 md:py-20</code></li>
<li>Padding horizontal : <code>px-4 md:px-8</code></li>
<li>Gap grille produits : <code>gap-5</code> (20px)</li>
<li>Hauteur header : <code>h-[72px]</code></li>
</ul>

<h2>Composants clés</h2>
<ul>
<li><strong>Card produit</strong> : ribbon (mono uppercase) + titre serif + blurb body + prix mono + flèche →</li>
<li><strong>Card bundle</strong> : ribbon mousse (PACK · ÉCONOMIE Y €) + prix barré individuel à côté du prix réduit</li>
<li><strong>Bouton primaire</strong> : <code>bg-mousse text-lin</code> (CTA principal)</li>
<li><strong>Bouton secondaire</strong> : <code>border-2 border-ebene text-ebene</code> (CTA alternatif)</li>
<li><strong>Lien d'icône</strong> : <code>text-pierre hover:text-chene</code></li>
</ul>

<h2>Accessibilité</h2>
<ul>
<li>Contraste minimum AA : ebene/lin = 13.5:1 (AAA)</li>
<li>Focus visible : ring 2px mousse/20 sur inputs</li>
<li>aria-label sur tous les boutons icône</li>
<li>Hiérarchie H1 → H2 → H3 respectée</li>
</ul>
"""
    (EXPORT / "02-design-system.html").write_text(page("Design System V4", body))


# ───────────────────────── 3. Vocabulaire de marque ──────────────────────
def make_vocab():
    body = """<h1>03 · Vocabulaire de marque</h1>

<div class="callout">
<strong>Règle absolue</strong> : on ne cite JAMAIS de marque tierce. Toujours utiliser la catégorie générique.
</div>

<h2>Identité de marque</h2>
<table>
<tr><th>Élément</th><th>Forme officielle</th></tr>
<tr><td>Nom</td><td>L'établ'IA <em>(prononciation : « l'éta-bli-a »)</em></td></tr>
<tr><td>Tagline</td><td>Forgé pour votre métier</td></tr>
<tr><td>Sous-tagline</td><td>L'atelier des artisans du numérique</td></tr>
<tr><td>Domaine</td><td>letablia.fr</td></tr>
<tr><td>Couleurs sémantiques</td><td>Bois, terre, lin, mousse — palette d'atelier</td></tr>
<tr><td>Mascotte</td><td>Blibot (assistant d'installation, identité en cours de finalisation)</td></tr>
</table>

<h2>Mots à utiliser</h2>
<table>
<tr><th>Notre vocabulaire</th><th>Au lieu de…</th></tr>
<tr><td>système forgé</td><td>workflow, automation, template</td></tr>
<tr><td>forger</td><td>développer, créer, automatiser</td></tr>
<tr><td>atelier</td><td>plateforme, marketplace</td></tr>
<tr><td>professionnels francophones</td><td>PME, TPE, freelances (en mots-clés OK, en hero non)</td></tr>
<tr><td>artisan numérique</td><td>développeur, automaticien</td></tr>
<tr><td>compagnon (Blibot)</td><td>chatbot, assistant</td></tr>
<tr><td>livraison ZIP</td><td>téléchargement, fichiers</td></tr>
<tr><td>guide d'installation</td><td>tutoriel, doc</td></tr>
<tr><td>« Satisfait ou Forgé »</td><td>« Satisfait ou Remboursé »</td></tr>
</table>

<h2>Anonymisation des marques tierces</h2>
<p>Sur le site visiteur, jamais de nom d'éditeur. On utilise toujours la catégorie générique :</p>

<table>
<tr><th>Marque (interdit)</th><th>Catégorie générique</th></tr>
<tr><td>Shopify, WooCommerce, PrestaShop</td><td>plateforme e-commerce</td></tr>
<tr><td>Notion, Obsidian, Evernote</td><td>application de prise de notes</td></tr>
<tr><td>Excel, Google Sheets, Airtable, Numbers</td><td>tableur</td></tr>
<tr><td>Gmail, Outlook, ProtonMail</td><td>messagerie électronique</td></tr>
<tr><td>Telegram, WhatsApp, Signal</td><td>messagerie instantanée</td></tr>
<tr><td>Brevo, Mailchimp, Sendinblue</td><td>service d'emailing</td></tr>
<tr><td>n8n, Make, Zapier</td><td>moteur d'automatisation</td></tr>
<tr><td>HubSpot, Salesforce, Pipedrive</td><td>CRM</td></tr>
<tr><td>Slack, Discord, Microsoft Teams</td><td>messagerie d'équipe</td></tr>
<tr><td>PDF, Word, LibreOffice</td><td>document imprimable</td></tr>
</table>

<h2>Ton et voix</h2>
<ul>
<li><strong>Vouvoiement</strong> exclusif (sauf si Raphaël ouvre un espace privé un jour)</li>
<li>Ton <strong>artisanal mais précis</strong> — pas de marketing creux, pas non plus d'ingénieur froid</li>
<li>Phrases courtes plutôt que longues. Une idée = une phrase.</li>
<li>Pas d'emoji décoratif dans le contenu (mais SVG icons OK pour la nav)</li>
<li>Pas de superlatif gratuit (« incroyable », « révolutionnaire ») — préférer la précision (« 4h récupérées par semaine »)</li>
</ul>

<h2>Phrases canoniques</h2>
<table>
<tr><th>Contexte</th><th>Phrase</th></tr>
<tr><td>Hero principal</td><td>Des systèmes digitaux prêts à poser pour les petites entreprises.</td></tr>
<tr><td>Sous-titre hero</td><td>Automatisations, IA, systèmes prêts à poser, tableaux de bord et guides opérationnels — conçus pour récupérer du temps sans recruter une agence.</td></tr>
<tr><td>Réassurance pied home</td><td>Paiement unique · Guides inclus · Accompagnement personnalisé · Produits testés</td></tr>
<tr><td>Politique remboursement</td><td>« Satisfait ou Forgé » : on corrige avant de rembourser. Remboursement intégral si la correction n'aboutit pas, sous 14 jours.</td></tr>
<tr><td>Pré-requis (CGV)</td><td>L'établ'IA garantit le bon fonctionnement technique du système forgé tel que décrit sur la fiche produit, dans un environnement moteur d'automatisation conforme aux prérequis indiqués.</td></tr>
</table>

<h2>Position éthique IA (ADR-005)</h2>
<ul>
<li>Discrétion sans mensonge — on n'affiche pas « 100% IA assumé » ni « 100% humain »</li>
<li>Voice cloning Raphaël <strong>INTERDIT</strong></li>
<li>Humanizers obligatoires sur Tier 1 (vente direct), Tier 2 (LinkedIn), Tier 4 (CGV)</li>
<li>EU AI Act : marketing automatisé exempté, validation humaine obligatoire avant publication</li>
</ul>
"""
    (EXPORT / "03-vocabulaire-marque.html").write_text(page("Vocabulaire de marque", body))


# ─────────────────────────── 4. Politique forge ─────────────────────────
def make_policy():
    body = """<h1>04 · Politique « Satisfait ou Forgé »</h1>

<div class="callout">
<strong>Phrase canonique</strong> :
« Satisfait ou Forgé » — on corrige avant de rembourser. Remboursement intégral si la correction n'aboutit pas, sous 14 jours via le mode de paiement initial.
</div>

<h2>Principe</h2>
<p>L'établ'IA est un atelier d'artisan. Quand un client achète un système forgé, l'engagement est :</p>
<ol>
<li><strong>D'abord, on corrige</strong> : si le système ne fonctionne pas comme décrit dans son environnement de prérequis, nous travaillons ensemble pour le faire fonctionner.</li>
<li><strong>Ensuite, on rembourse — uniquement si la correction n'aboutit pas</strong> : intégralement, sous 14 jours, via le moyen de paiement initial.</li>
</ol>
<p>Ce n'est PAS « satisfait ou remboursé sans question ». C'est l'équivalent d'un artisan qui revient finir son travail.</p>

<h2>Ce qu'on ne dit JAMAIS</h2>
<div class="warning">
<ul>
<li>« Remboursement intégral sans justification »</li>
<li>« Satisfait ou remboursé sans question »</li>
<li>« 14 jours pour changer d'avis sans condition »</li>
<li>« Aucun risque, on rembourse tout »</li>
</ul>
Ces formulations propagent une politique qui n'est PAS la nôtre. Elles ont été propagées par erreur en mai 2026 et corrigées le 2026-05-04.
</div>

<h2>Conditions techniques</h2>
<p>Le remboursement est possible si :</p>
<ul>
<li>Le système ne fonctionne pas comme décrit sur sa fiche produit, ET</li>
<li>L'environnement client respecte les prérequis annoncés (versions, services tiers actifs, données accessibles), ET</li>
<li>L'établ'IA n'a pas pu rendre le système fonctionnel après tentative documentée de correction</li>
</ul>

<p>Le remboursement n'est PAS possible si :</p>
<ul>
<li>Le client a coché la case « renonciation au droit de rétractation » avant téléchargement (CGV)</li>
<li>Le délai de 14 jours est dépassé</li>
<li>Le client a modifié le système au-delà de l'usage prévu</li>
<li>Le client n'a pas répondu aux demandes de support pendant la phase de correction</li>
</ul>

<h2>Processus</h2>
<ol>
<li>Le client envoie un email à <code>contact@letablia.fr</code> avec son numéro de commande et la description du problème.</li>
<li>L'établ'IA répond sous 48 h ouvrables avec un diagnostic et une proposition de correction.</li>
<li>Phase de correction : durée variable selon la complexité, généralement &lt; 7 jours.</li>
<li>Si correction réussie : système livré et signé en réception.</li>
<li>Si correction échouée : remboursement déclenché sous 14 jours via le moyen de paiement initial.</li>
</ol>

<h2>Cadre légal</h2>
<p>Conforme aux articles L.217-4 à L.217-13 du Code de la consommation (garanties légales de conformité et vices cachés). Conforme à LemonSqueezy MoR (Merchant of Record) qui gère la transaction et la TVA UE.</p>

<h2>Pages où la politique apparaît</h2>
<ul>
<li><code>cgv.html</code> — section 10 (texte complet)</li>
<li><code>mentions-legales.html</code> — bloc « Garantie » (résumé)</li>
<li><code>index.html</code> — bloc « Satisfait ou Forgé » (encart hero)</li>
<li>Toutes fiches produit — bandeau pied de hero (« Politique Satisfait ou Forgé »)</li>
<li>Toutes pages — pied de page footer (rappel court)</li>
</ul>

<p>Le texte du footer canonique inclut systématiquement :</p>
<pre><code>Politique « Satisfait ou Forgé » : on corrige avant de rembourser.</code></pre>
"""
    (EXPORT / "04-politique-forge.html").write_text(page("Politique « Satisfait ou Forgé »", body))


# ─────────────────────────── 5. Catalogue ─────────────────────────────
def make_catalogue():
    rows = []
    for p in DATA["products"]:
        tools = " · ".join(t for t in p["tools"])
        targets = ", ".join(p.get("targets", []))
        family = next((f["title"] for f in DATA["families"] if f["slug"] == p["family"]), p["family"])
        rows.append(f'<tr><td><strong>{p["title"]}</strong><br><code>{p["url"]}</code></td><td><span class="tag">{family}</span></td><td>{tools}</td><td>{targets}</td><td><strong>{p["price"]} €</strong></td><td>{p["blurb"]}</td></tr>')
    products_table = "\n".join(rows)

    bundle_rows = []
    for b in DATA["bundles"]:
        included = "<br>".join(b["products"])
        bundle_rows.append(f'<tr><td><strong>{b["title"]}</strong><br><code>{b["url"]}</code></td><td>{b["subtitle"]}</td><td>{included}</td><td><strong>{b["price"]} €</strong> <span style="color:var(--pierre);text-decoration:line-through">{b["price_individual"]} €</span><br>Économie {b["savings"]} €</td><td>{b["blurb"]}</td></tr>')
    bundles_table = "\n".join(bundle_rows)

    body = f"""<h1>05 · Catalogue produits</h1>
<p>Source unique de vérité : <code>products.json</code> v{DATA["version"]}, mise à jour {DATA["updated"]}.</p>

<h2>11 systèmes forgés</h2>
<table>
<tr><th>Titre / URL</th><th>Famille</th><th>Outils</th><th>Cibles</th><th>Prix</th><th>Blurb</th></tr>
{products_table}
</table>

<h2>3 packs (bundles)</h2>
<table>
<tr><th>Titre / URL</th><th>Format</th><th>Inclus</th><th>Prix</th><th>Blurb</th></tr>
{bundles_table}
</table>

<h2>5 familles d'usage</h2>
<table>
<tr><th>Slug</th><th>Titre</th><th>Verbe d'action</th><th>Icon SVG</th></tr>
"""
    for f in DATA["families"]:
        body += f'<tr><td><code>{f["slug"]}</code></td><td><strong>{f["title"]}</strong></td><td>{f["verb"]}</td><td>{f["icon"]}</td></tr>\n'
    body += "</table>\n"

    body += "<h2>7 catégories d'outils (anonymisées)</h2>\n<table>\n<tr><th>Slug</th><th>Label visible</th></tr>\n"
    for t in DATA["tools"]:
        body += f'<tr><td><code>{t["slug"]}</code></td><td>{t["label"]}</td></tr>\n'
    body += "</table>\n"

    body += """
<h2>3 buckets de prix</h2>
<ul>
<li><strong>≤ 19 €</strong> — porte d'entrée (Signal de Vente à 9 €)</li>
<li><strong>20 – 49 €</strong> — gros du catalogue (10 produits)</li>
<li><strong>50 € et +</strong> — packs uniquement</li>
</ul>

<h2>Best-sellers (mis en avant sur la home)</h2>
<ul>
<li>Signal de Vente (9 €) — ticket d'entrée</li>
<li>Gardien de Stock (29 €) — produit phare e-commerce</li>
<li>Pack Cyber-Hygiène TPE (39 €) — réassurance + reglementaire</li>
</ul>
"""
    (EXPORT / "05-catalogue.html").write_text(page("Catalogue produits", body))


# ─────────────────────────── 6. Personas ─────────────────────────────
def make_personas():
    rows = []
    for pe in DATA["personas"]:
        rows.append(f'<tr><td><strong>{pe["title"]}</strong></td><td>{pe["subtitle"]}</td><td>{pe["blurb"]}</td><td><code>?cible={pe["filter"]["targets"][0]}</code></td></tr>')
    body = f"""<h1>06 · Personas et cibles</h1>

<h2>3 personas mis en avant sur la home</h2>
<table>
<tr><th>Titre</th><th>Sous-titre</th><th>Description</th><th>URL filtre catalogue</th></tr>
{chr(10).join(rows)}
</table>

<h2>Détail par persona</h2>

<h3>1. E-commerçant</h3>
<ul>
<li>Possède une boutique en ligne (plateforme e-commerce)</li>
<li>Volume : 10 commandes / semaine minimum pour rentabilité</li>
<li>Outils typiques : plateforme e-commerce + tableur + messagerie instantanée + service d'emailing</li>
<li><strong>Produits ciblés</strong> : Signal de Vente, Gardien de Stock, Séquenceur Post-Achat, Le Collecteur Avis</li>
<li><strong>Pack recommandé</strong> : Pack E-commerce Complet (49 €, économie 18 €)</li>
</ul>

<h3>2. Freelance / Solo / Agence</h3>
<ul>
<li>Travail commercial : prospection, devis, suivi, facturation</li>
<li>Stack légère : tableur, application de prise de notes, messagerie électronique</li>
<li>Frein principal : pas de temps pour relancer manuellement les prospects</li>
<li><strong>Produits ciblés</strong> : Mini CRM Prestataire, Relance Prospects, Agent Tri Email, Carnet Forge</li>
<li><strong>Pack recommandé</strong> : Pack Freelance Solo (119 €, économie 18 €)</li>
</ul>

<h3>3. TPE généraliste / Coach / Formateur / Consultant</h3>
<ul>
<li>Activité de service avec besoin de pilotage trésorerie</li>
<li>Échéance facturation électronique 2026 (obligatoire en France)</li>
<li>Besoin cyber-hygiène : phishing, sauvegardes, MFA</li>
<li><strong>Produits ciblés</strong> : Dashboard Trésorerie TPE, Kit Facturation Électronique 2026, Pack Cyber-Hygiène TPE</li>
<li><strong>Pack recommandé</strong> : Pack TPE Conformité 2026 (99 €, économie 18 €)</li>
</ul>

<h2>Cibles techniques (data-targets)</h2>
<table>
<tr><th>Slug</th><th>Label visible</th><th>Nombre de produits</th></tr>
<tr><td><code>e-commerce</code></td><td>E-commerçant</td><td>4 produits + 1 pack</td></tr>
<tr><td><code>freelance</code></td><td>Freelance</td><td>5 produits + 1 pack</td></tr>
<tr><td><code>agence</code></td><td>Agence</td><td>2 produits</td></tr>
<tr><td><code>formateur</code></td><td>Formateur</td><td>1 produit</td></tr>
<tr><td><code>tpe-generaliste</code></td><td>TPE généraliste</td><td>5 produits + 1 pack</td></tr>
</table>
"""
    (EXPORT / "06-personas-cibles.html").write_text(page("Personas et cibles", body))


# ─────────────────────────── 7. Ergonomie ─────────────────────────────
def make_ergonomie():
    body = """<h1>07 · Ergonomie et chemins d'accès</h1>

<div class="callout">
<strong>Théorie d'ergonomie Raphaël (2026-05-03)</strong> :
Le catalogue letablia.fr fonctionne comme Amazon / Etsy / Gumroad — le visiteur arrive avec une intention, il faut lui offrir 3 entrées pour atteindre le produit qui correspond.
</div>

<h2>Les 3 chemins d'accès</h2>

<h3>Chemin 1 — Par BESOIN (familles)</h3>
<p>Le visiteur sait ce qu'il VEUT FAIRE.</p>
<ul>
<li><strong>Automatiser</strong> — brancher des services entre eux pour économiser du temps</li>
<li><strong>Vendre</strong> — convertir et fidéliser ses clients</li>
<li><strong>Piloter</strong> — voir et décider sur des données fiables</li>
<li><strong>Produire</strong> — modèles et trames pour livrer plus vite</li>
<li><strong>Sécuriser</strong> — cyber-hygiène, conformité, RGPD</li>
</ul>
<p>URL : <code>/produits/&lt;slug&gt;/</code> · Affichage : page éditoriale + grille des produits de la famille.</p>

<h3>Chemin 2 — Par OUTIL (catégories génériques)</h3>
<p>Le visiteur sait avec QUOI il travaille.</p>
<ul>
<li>Plateforme e-commerce</li>
<li>Tableur</li>
<li>Application de prise de notes</li>
<li>Service d'emailing</li>
<li>Messagerie électronique</li>
<li>Messagerie instantanée</li>
<li>Document imprimable</li>
</ul>
<p>URL : <code>/catalogue.html?outil=&lt;slug&gt;</code> · Affichage : catalogue avec filtre activé.</p>

<h3>Chemin 3 — Par RECHERCHE (Cmd+K)</h3>
<p>Le visiteur sait CE QU'IL CHERCHE par mot-clé.</p>
<ul>
<li>Modal global recherche : <kbd>Cmd+K</kbd> / <kbd>/</kbd> / clic loupe ⌕</li>
<li>Fuzzy match sur titre, tools, keywords, blurb</li>
<li>Scoring pondéré : titre &gt; tools &gt; keywords &gt; blurb</li>
<li>Résultats live, navigation flèches haut/bas, Entrée pour ouvrir</li>
</ul>

<h2>Personas comme raccourcis</h2>
<p>3 cards persona sur la home qui pointent vers le catalogue avec filtre :</p>
<ul>
<li>« Vous êtes <strong>e-commerçant</strong> » → <code>/catalogue.html?cible=e-commerce</code></li>
<li>« Vous êtes <strong>freelance</strong> » → <code>/catalogue.html?cible=freelance</code></li>
<li>« Vous êtes <strong>TPE généraliste</strong> » → <code>/catalogue.html?cible=tpe-generaliste</code></li>
</ul>

<h2>Filtres du catalogue</h2>
<p>4 axes de filtre, combinables (AND entre axes, OR à l'intérieur d'un axe) :</p>
<ol>
<li><strong>Famille</strong> (5 valeurs) : Automatiser, Vendre, Piloter, Produire, Sécuriser</li>
<li><strong>Outil</strong> (7 valeurs) : catégories anonymisées</li>
<li><strong>Prix</strong> (3 buckets) : ≤ 19 €, 20-49 €, 50 € et +</li>
<li><strong>Cible</strong> (5 valeurs) : E-commerçant, Freelance, Agence, Formateur, TPE généraliste</li>
</ol>
<p>État des filtres synchronisé avec l'URL (deeplinkable). Bouton « Réinitialiser » + compteur de cards visibles.</p>

<h2>Tri</h2>
<p>Sélecteur en haut de la grille, options :</p>
<ul>
<li>Par défaut (ordre éditorial du catalogue)</li>
<li>Prix croissant</li>
<li>Prix décroissant</li>
<li>Alphabétique</li>
</ul>

<h2>Comportements UX clés</h2>
<ul>
<li><strong>Empty state</strong> : si 0 card visible, message « Aucun système ne correspond. <a>Réinitialiser les filtres</a> ».</li>
<li><strong>Mobile</strong> : aside filtres collapsible (fermée par défaut, bouton « Filtrer » la déploie).</li>
<li><strong>Burger menu mobile</strong> : plein écran, fermeture sur clic lien ou ESC.</li>
<li><strong>Dropdown header</strong> : zone tampon pt-1 + transition-opacity duration-150ms (évite la disparition trop rapide).</li>
<li><strong>Sticky header</strong> : reste visible au scroll, hauteur 72px.</li>
</ul>
"""
    (EXPORT / "07-ergonomie.html").write_text(page("Ergonomie et chemins d'accès", body))


# ────────────────────── 8. Header + Footer canoniques ─────────────────
def make_shell():
    header = (ROOT / "scripts" / "inject-canonical-shell.py").read_text()
    # Extraire le header et footer canoniques depuis le script
    import re
    m_h = re.search(r"CANONICAL_HEADER = f?'''(.*?)'''", header, re.DOTALL)
    m_f = re.search(r"CANONICAL_FOOTER = '''(.*?)'''", header, re.DOTALL)
    header_html = m_h.group(1) if m_h else "<!-- header non trouvé -->"
    footer_html = m_f.group(1) if m_f else "<!-- footer non trouvé -->"

    def escape(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    body = f"""<h1>08 · Header + Footer canoniques</h1>

<div class="callout">
Ces deux blocs sont identiques sur les 40 pages du site. Le script <code>scripts/inject-canonical-shell.py</code> les injecte automatiquement. Tout outil de redesign doit les reproduire à l'identique (ou en proposer une variation cohérente).
</div>

<h2>Header (sticky, h-72px)</h2>
<p>Composé de :</p>
<ul>
<li>Logo « L'établ'IA » (Playfair Display, chene)</li>
<li>Navigation desktop : dropdown Catalogue (5 familles avec SVG icons) + À propos + FAQ + Contact</li>
<li>Right side : bouton recherche (loupe SVG) + CTA « Diagnostic gratuit » (mousse)</li>
<li>Mobile : burger 3-lines + bouton recherche</li>
<li>Menu mobile plein écran : Catalogue → 5 familles + À propos + FAQ + Contact + CTA Diagnostic</li>
</ul>

<pre><code>{escape(header_html)}</code></pre>

<h2>Footer (mt-12, fond ebene)</h2>
<p>Composé de 4 colonnes :</p>
<ul>
<li><strong>Marque</strong> : « L'établ'IA » + tagline « Forgé pour votre métier »</li>
<li><strong>Catalogue</strong> : Tous les systèmes + 5 familles</li>
<li><strong>L'établ'IA</strong> : À propos + FAQ + Diagnostic gratuit + Contact</li>
<li><strong>Informations</strong> : Mentions légales + CGV + Confidentialité + email contact</li>
</ul>
<p>Pied : copyright + rappel politique « Satisfait ou Forgé ».</p>

<pre><code>{escape(footer_html)}</code></pre>

<h2>SVG icons des 5 familles</h2>
<p>Reproduits inline dans le dropdown (taille 14×14, stroke 2px) :</p>
<ul>
<li><strong>Automatiser</strong> : éclair (lightning bolt)</li>
<li><strong>Vendre</strong> : graphique en hausse (trending up)</li>
<li><strong>Piloter</strong> : boussole (compass)</li>
<li><strong>Produire</strong> : couches (layers / stack)</li>
<li><strong>Sécuriser</strong> : bouclier (shield)</li>
</ul>
<p>Source : Feather Icons (license MIT).</p>
"""
    (EXPORT / "08-header-footer.html").write_text(page("Header + Footer", body))


# ─────────────────────────── 9. Composants ────────────────────────────
def make_components():
    body = """<h1>09 · Composants et cards</h1>

<h2>Card produit standard</h2>
<p>Utilisée sur le catalogue, les pages familles, le cross-sell des fiches produit.</p>

<div style="display:flex;flex-wrap:wrap;gap:16px;margin:18px 0">
<div class="product-card-preview">
<div class="ribbon">VENDRE</div>
<div class="body">
<p style="font-family:'JetBrains Mono',monospace;font-size:0.7em;color:#8A7560;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 6px">Plateforme e-commerce · Notification</p>
<h4>Signal de Vente</h4>
<p class="blurb">Une notification instantanée à chaque commande de votre boutique en ligne.</p>
<div style="display:flex;justify-content:space-between;align-items:center"><span class="price">9 €</span><span style="font-size:0.88em;color:#6B7C5F">Voir →</span></div>
</div>
</div>
</div>

<h3>Code HTML</h3>
<pre><code>&lt;a href="/signal-de-vente/"
   class="product-card group block bg-lin border border-pierre/30 rounded-[8px] overflow-hidden hover:border-chene transition"
   data-family="vendre"
   data-tools="plateforme-ecommerce messagerie-instantanee"
   data-targets="e-commerce"
   data-price="9"
   data-title="signal de vente"
   data-keywords="alerte commande boutique en ligne notification temps reel"&gt;
  &lt;div class="bg-chene-6 h-[100px] flex items-center justify-center"&gt;
    &lt;span class="font-mono text-chene text-[11px] uppercase tracking-[2px]"&gt;VENDRE&lt;/span&gt;
  &lt;/div&gt;
  &lt;div class="p-5"&gt;
    &lt;p class="font-mono text-[11px] text-chene uppercase tracking-[1px] mb-2"&gt;Plateforme e-commerce · Notification&lt;/p&gt;
    &lt;h3 class="font-heading text-[22px] text-ebene mb-2 leading-[1.2]"&gt;Signal de Vente&lt;/h3&gt;
    &lt;p class="font-body text-[14px] text-pierre leading-[1.5] mb-4"&gt;Une notification instantanée à chaque commande de votre boutique en ligne.&lt;/p&gt;
    &lt;div class="flex items-center justify-between"&gt;
      &lt;span class="font-mono text-[18px] text-chene font-semibold"&gt;9 €&lt;/span&gt;
      &lt;span class="font-body text-[14px] text-mousse group-hover:underline"&gt;Voir →&lt;/span&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/a&gt;</code></pre>

<h2>Card bundle (pack)</h2>
<p>Variante visuelle pour les 3 packs : ribbon mousse, prix barré individuel.</p>

<div style="display:flex;flex-wrap:wrap;gap:16px;margin:18px 0">
<div class="product-card-preview" style="border:2px solid #6B7C5F">
<div class="ribbon" style="background:#6B7C5F;color:#F2EDE8">PACK · ÉCONOMIE 18 €</div>
<div class="body">
<p style="font-family:'JetBrains Mono',monospace;font-size:0.7em;color:#6B7C5F;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 6px">Bundle 3 systèmes</p>
<h4>Pack E-commerce Complet</h4>
<p class="blurb">Tout pour piloter votre boutique en ligne : alerte commandes, surveillance stock, collecte d'avis.</p>
<div style="display:flex;justify-content:space-between;align-items:center">
<div><span style="font-family:'JetBrains Mono',monospace;color:#6B7C5F;font-weight:700">49 €</span> <span style="font-family:'JetBrains Mono',monospace;font-size:0.78em;color:#B8AFA6;text-decoration:line-through;margin-left:6px">67 €</span></div>
<span style="font-size:0.88em;color:#6B7C5F">Voir →</span>
</div>
</div>
</div>
</div>

<h2>Boutons</h2>
<table>
<tr><th>Variante</th><th>Classes Tailwind</th><th>Usage</th></tr>
<tr><td><strong>Primaire</strong></td><td><code>bg-mousse text-lin font-semibold rounded-[6px] px-7 py-[14px] hover:opacity-90</code></td><td>CTA principal — Forger, Acheter, Diagnostic</td></tr>
<tr><td><strong>Secondaire</strong></td><td><code>bg-transparent text-ebene border-2 border-ebene rounded-[6px] px-7 py-[14px] hover:bg-ebene hover:text-lin</code></td><td>CTA alternatif — Voir le catalogue</td></tr>
<tr><td><strong>Lien fort</strong></td><td><code>bg-chene text-lin font-semibold rounded-[6px] px-7 py-[14px] hover:opacity-90</code></td><td>CTA hero principal</td></tr>
<tr><td><strong>Lien icône</strong></td><td><code>text-pierre hover:text-chene transition p-2 rounded hover:bg-chene-6</code></td><td>Recherche, menu</td></tr>
</table>

<h2>Encarts</h2>
<table>
<tr><th>Variante</th><th>Classes</th><th>Usage</th></tr>
<tr><td><strong>Réassurance</strong></td><td><code>bg-chene-6 rounded-[6px] p-6</code></td><td>Hero secondaire, blocs « Satisfait ou Forgé »</td></tr>
<tr><td><strong>Action</strong></td><td><code>bg-mousse-10 rounded-[8px] p-8</code></td><td>Bloc « Ce que je vérifie » dans diagnostic</td></tr>
<tr><td><strong>Border</strong></td><td><code>bg-lin border border-pierre/30 rounded-[8px] p-8</code></td><td>Cards info, formulaire diagnostic</td></tr>
<tr><td><strong>Forge</strong></td><td><code>bg-chene-6 border-l-4 border-mousse rounded-[6px] p-4</code></td><td>Bandeau politique « Satisfait ou Forgé »</td></tr>
</table>

<h2>Inputs de formulaire</h2>
<pre><code>&lt;input type="text"
       class="w-full font-body text-base text-ebene bg-lin-50 border border-pierre/30 rounded-[6px] px-4 py-3 focus:outline-none focus:border-mousse focus:ring-2 focus:ring-mousse/20 transition"&gt;</code></pre>

<h2>Breadcrumb</h2>
<pre><code>&lt;nav class="max-w-[1280px] mx-auto px-4 md:px-8 py-4 font-mono text-[12px] text-pierre"&gt;
  &lt;a href="/" class="hover:text-chene"&gt;Accueil&lt;/a&gt; · &lt;a href="/catalogue.html" class="hover:text-chene"&gt;Catalogue&lt;/a&gt; · &lt;span class="text-ebene"&gt;Signal de Vente&lt;/span&gt;
&lt;/nav&gt;</code></pre>
"""
    (EXPORT / "09-composants.html").write_text(page("Composants et cards", body))


# ─────────────────────────── 10. Scripts build ────────────────────────
def make_scripts_doc():
    body = """<h1>10 · Scripts de construction</h1>

<div class="callout">
<strong>Principe</strong> : <code>products.json</code> est la source unique. Tous les scripts régénèrent les pages à partir de ce JSON. <strong>On ne copie-colle JAMAIS un prix ou un blurb.</strong>
</div>

<h2>Pipeline de build</h2>
<pre><code># Modifier products.json (prix, blurb, tools, bundles)
nano assets/data/products.json

# Régénérer toutes les pages
python3 scripts/build-from-json.py

# Si on a ajouté/retiré du contenu marqué : anonymiser
python3 scripts/anonymize-brands.py

# Si on a modifié header/footer : injecter partout
python3 scripts/inject-canonical-shell.py

# Recompiler Tailwind après modif HTML (pour purger ou ajouter classes)
npm run build:css

# Pousser sur Vercel
git add -A
git commit -m "Update produits"
git push origin main && git push origin main:master
</code></pre>

<h2>scripts/build-from-json.py</h2>
<p>Régénère depuis <code>products.json</code> :</p>
<ul>
<li><strong>catalogue.html</strong> — grille 14 cards (3 packs + 11 produits) + filtres avec compteurs</li>
<li><strong>produits/&lt;famille&gt;/index.html</strong> × 5 — grille des produits de la famille</li>
<li><strong>fiches produit prix</strong> — synchronise <code>&lt;div class="price-badge"&gt;</code> et <code>&lt;p class="price"&gt;</code></li>
<li><strong>packs/&lt;slug&gt;/index.html</strong> × 3 — pages bundles avec produits inclus</li>
</ul>
<p>Utilise BeautifulSoup pour modifier le DOM proprement.</p>

<h2>scripts/anonymize-brands.py</h2>
<p>Sed massif sur tous les fichiers HTML pour remplacer les marques par leurs catégories génériques :</p>
<ul>
<li>Shopify → plateforme e-commerce</li>
<li>Notion → application de prise de notes</li>
<li>Excel, Google Sheets → tableur</li>
<li>Gmail, Outlook → messagerie électronique</li>
<li>Telegram, WhatsApp → messagerie instantanée</li>
<li>Brevo, Mailchimp → service d'emailing</li>
<li>n8n, Make, Zapier → moteur d'automatisation</li>
</ul>
<p>Inclut variantes UPPERCASE (RIBBONS) et patterns combinés (« Shopify/WooCommerce »).</p>

<h2>scripts/inject-canonical-shell.py</h2>
<p>Injecte le header + footer canoniques sur toutes les pages HTML. Utilise BeautifulSoup pour remplacer les balises <code>&lt;header&gt;</code> et <code>&lt;footer&gt;</code> proprement, sans toucher au reste de la page.</p>
<p>Inclut aussi le menu mobile plein écran.</p>

<h2>scripts/fix-policy.py</h2>
<p>Corrige les phrases incompatibles avec la politique « Satisfait ou Forgé » :</p>
<ul>
<li>« Remboursement intégral sans justification » → phrase canonique</li>
<li>« Satisfait ou remboursé sans question » → « Satisfait ou Forgé »</li>
<li>« 14 jours sans condition » → « Politique Satisfait ou Forgé : on corrige avant de rembourser »</li>
</ul>

<h2>npm run build:css</h2>
<p>Compile Tailwind CSS depuis <code>styles/input.css</code> vers <code>styles/output.css</code> avec purge automatique des classes inutilisées et minification.</p>
<p>Taille finale : ~18 KB minifié pour 40 pages.</p>

<h2>Hooks Git</h2>
<p>Le pre-commit hook <code>.git/hooks/pre-commit</code> vérifie :</p>
<ul>
<li>Aucune marque tierce non anonymisée</li>
<li>Aucun secret dans les commits (.env, tokens, mots de passe)</li>
<li>Aucun vocabulaire interdit (workflow / template / support humain / credential) — warnings non bloquants</li>
</ul>
"""
    (EXPORT / "10-scripts-build.html").write_text(page("Scripts de construction", body))


# ─────────────────────────── 11. Fiches produit ───────────────────────
def make_fiches():
    body = """<h1>11 · Structure des fiches produit</h1>

<h2>Anatomie type d'une fiche</h2>
<ol>
<li><strong>Header</strong> canonique (sticky, h-72px)</li>
<li><strong>Breadcrumb</strong> : Accueil · Catalogue · &lt;Famille&gt; · &lt;Titre&gt;</li>
<li><strong>Hero</strong> :
  <ul>
    <li>Ribbon famille (mono uppercase)</li>
    <li>Titre H1 (Playfair, 36-44px)</li>
    <li>Sous-titre / promesse en 1 phrase</li>
    <li>Prix (bouton « Forger ce système »)</li>
    <li>Bandeau réassurance « Politique Satisfait ou Forgé »</li>
  </ul>
</li>
<li><strong>Section « Comment ça marche »</strong> : 3 étapes ordonnées (chiffrées)</li>
<li><strong>Section « Ce qui est inclus »</strong> : liste des livrables ZIP</li>
<li><strong>Section « Pré-requis »</strong> : ce que le client doit avoir avant achat</li>
<li><strong>Section « Témoignages / cas d'usage »</strong> (si disponibles)</li>
<li><strong>Section « Questions fréquentes »</strong> : 4-6 Q/R</li>
<li><strong>Cross-sell</strong> : 2-3 cards « Vous pourriez aussi forger… »</li>
<li><strong>CTA final</strong> : bouton « Forger ce système — X € » + lien vers diagnostic gratuit</li>
<li><strong>Footer</strong> canonique</li>
</ol>

<h2>11 fiches produit complètes</h2>
<p>Le dossier <code>exemples-fiches/</code> contient les 11 fiches HTML telles qu'elles tournent sur letablia.fr. Voici la liste avec leurs URLs et leurs prix actuels :</p>

<table>
<tr><th>Titre</th><th>Famille</th><th>URL</th><th>Prix</th><th>Fichier exemple</th></tr>
"""
    for p in DATA["products"]:
        slug_short = p["slug"].split("/")[-1]
        body += f'<tr><td>{p["title"]}</td><td>{next((f["title"] for f in DATA["families"] if f["slug"] == p["family"]), "")}</td><td><code>{p["url"]}</code></td><td>{p["price"]} €</td><td><code>exemples-fiches/{slug_short}.html</code></td></tr>\n'
    body += """</table>

<h2>Variations par famille</h2>
<ul>
<li><strong>Automatiser</strong> : Insister sur le gain de temps mesurable, schéma de flux dans la fiche</li>
<li><strong>Vendre</strong> : Insister sur le ROI, témoignages, screenshots</li>
<li><strong>Piloter</strong> : Insister sur la clarté visuelle, screenshot du dashboard</li>
<li><strong>Produire</strong> : Insister sur la qualité du modèle livré, exemple PDF/template</li>
<li><strong>Sécuriser</strong> : Insister sur la conformité, RGPD, échéances légales</li>
</ul>

<h2>Conventions de prix</h2>
<ul>
<li><strong>9 €</strong> : ticket d'entrée ultra-simple (Signal de Vente uniquement)</li>
<li><strong>29 €</strong> : système simple à monter (Gardien, Séquenceur, Collecteur)</li>
<li><strong>39 €</strong> : système moyen ou pack documentaire (Cyber, Carnet, Kit Facturation, etc.)</li>
<li><strong>49 €</strong> : système complexe (Mini CRM, Relance Prospects)</li>
<li><strong>50 € et +</strong> : packs uniquement</li>
</ul>
"""
    (EXPORT / "11-fiches-produits.html").write_text(page("Fiches produit", body))


# ─────────────────────────── 12. Pages légales ─────────────────────────
def make_legal():
    body = """<h1>12 · Pages légales</h1>

<p>Trois pages obligatoires pour la conformité française et UE :</p>

<table>
<tr><th>Page</th><th>URL</th><th>Contenu</th></tr>
<tr><td>Mentions légales</td><td><code>/mentions-legales.html</code></td><td>Identité éditeur (entreprise individuelle Raphaël Olivi), hébergeur (Vercel + GitHub), garantie « Satisfait ou Forgé », limite de responsabilité</td></tr>
<tr><td>CGV</td><td><code>/cgv.html</code></td><td>11 sections : objet, identification éditeur, produits, prix, paiement (LemonSqueezy MoR), livraison, droit de rétractation, garanties légales, propriété intellectuelle, limites de responsabilité, politique « Satisfait ou Forgé »</td></tr>
<tr><td>Confidentialité</td><td><code>/confidentialite.html</code></td><td>RGPD, cookies, droits utilisateur, durées de conservation, sous-traitants (LemonSqueezy, Brevo, Vercel, Telegram), contact DPO</td></tr>
</table>

<h2>Bannière cookies V4</h2>
<p>Implémentée dans <code>assets/css/cookies.css</code> + <code>assets/js/cookies.js</code>. Conforme RGPD :</p>
<ul>
<li>Bannière au premier visite avec choix Accepter/Refuser/Personnaliser</li>
<li>Aucun cookie non-essentiel sans consentement</li>
<li>localStorage pour mémoriser le choix</li>
<li>Lien permanent en footer pour rouvrir les préférences</li>
</ul>

<h2>Headers sécurité Vercel</h2>
<p>Configurés dans <code>vercel.json</code> :</p>
<ul>
<li><code>X-Content-Type-Options: nosniff</code></li>
<li><code>X-Frame-Options: DENY</code></li>
<li><code>Referrer-Policy: strict-origin-when-cross-origin</code></li>
<li><code>Permissions-Policy</code> restrictif (no camera, no microphone, no geolocation)</li>
<li><code>Strict-Transport-Security: max-age=31536000; includeSubDomains</code></li>
</ul>

<h2>Cadre LemonSqueezy MoR</h2>
<p>L'établ'IA n'est pas le merchant of record. LemonSqueezy gère :</p>
<ul>
<li>La transaction et le paiement</li>
<li>La TVA selon le pays de l'acheteur (UE)</li>
<li>Les factures clients</li>
<li>Les remboursements (déclenchés par L'établ'IA selon politique)</li>
</ul>
<p>L'établ'IA reçoit le net (commission LemonSqueezy ~5% + frais Stripe).</p>
"""
    (EXPORT / "12-pages-legales.html").write_text(page("Pages légales", body))


# ─────────────────────────── 13. Bugs résolus ─────────────────────────
def make_bugs():
    body = """<h1>13 · 12 bugs résolus le 2026-05-04</h1>

<p>Liste exhaustive des bugs signalés par Raphaël et leurs corrections, dans l'ordre du commit <code>d7a7962</code>.</p>

<table>
<tr><th>#</th><th>Bug signalé</th><th>Correction</th></tr>
<tr><td>1</td><td>Blocs mal centrés (familles, besoins, systèmes)</td><td>Retrait de <code>base.css</code> (683 lignes) et <code>design-system.css</code> du Design System V3 obsolète qui surchargeaient Tailwind V4</td></tr>
<tr><td>2</td><td>Liens « Vous êtes... » personas ne renvoient rien</td><td>Filtre <code>?cible=X</code> testé avec Playwright : 5/6/6 cards visibles selon e-commerce/freelance/tpe-generaliste</td></tr>
<tr><td>3</td><td><strong>CRITIQUE</strong> Aucune marque ne devrait être citée</td><td>Sed massif anonymisation : Shopify→plateforme e-commerce, Notion→app prise notes, Excel→tableur, Gmail→messagerie, Telegram→notification, Brevo→service emailing, n8n→moteur d'automatisation</td></tr>
<tr><td>4</td><td>Bundles disparus</td><td><code>products.json</code> v2.0 contient 3 bundles (e-commerce 49€, freelance 119€, tpe-conformite 99€) + 3 pages packs créées</td></tr>
<tr><td>5</td><td>Politique remboursement « Satisfait ou Forgé » incohérente</td><td>Phrase canonique « on corrige avant de rembourser » harmonisée sur 8 pages + footer</td></tr>
<tr><td>6</td><td>Footer pas identique sur toutes les pages</td><td>Footer canonique 4 colonnes injecté sur 40 pages via <code>inject-canonical-shell.py</code></td></tr>
<tr><td>7</td><td>Site rame BEAUCOUP trop</td><td>Retrait base.css (683L) + design-system.css. CSS Tailwind compilé = 18 KB minifié</td></tr>
<tr><td>8</td><td>Diagnostic gratuit par mail = mauvaise idée</td><td>Formulaire HTML 6 champs (prénom, email, métier, tâche, stack, volume) avec endpoint Formspree</td></tr>
<tr><td>9</td><td>Dropdown header disparaît trop vite</td><td>Zone tampon <code>pt-1</code> + <code>transition-opacity duration-150</code> + <code>pointer-events</code> coordonné</td></tr>
<tr><td>10</td><td>Symboles ▣ ⚡ 📈 ◯ ◇ buggés</td><td>5 SVG icons inline (Feather Icons) : lightning, trending, compass, layers, shield</td></tr>
<tr><td>11</td><td><strong>CRITIQUE</strong> Prix contradictoires fiche vitrine vs fiche produit</td><td><code>products.json</code> = source unique. Script <code>build-from-json.py</code> régénère tout.</td></tr>
<tr><td>12</td><td>Chemins doublés dans le header</td><td>Suppression du lien « Voir tout le catalogue » dans le dropdown (le bouton parent va déjà à /catalogue.html)</td></tr>
</table>

<h2>Action restante côté Raphaël</h2>
<div class="warning">
Le formulaire de diagnostic utilise <code>https://formspree.io/f/diagnostic</code> comme placeholder. Il faut :
<ol>
<li>Créer un compte gratuit sur <a href="https://formspree.io">formspree.io</a> (50 envois/mois)</li>
<li>Récupérer le vrai ID du form (format <code>xyzaaaaa</code>)</li>
<li>Remplacer dans <code>diagnostic.html</code> ligne du form action</li>
</ol>
Alternative : utiliser un <code>mailto:diagnostic@letablia.fr</code> séparé du contact général.
</div>
"""
    (EXPORT / "13-bugs-resolus.html").write_text(page("12 bugs résolus", body))


# ─────────────────────────── Sources ──────────────────────────────────
def copy_sources():
    src = EXPORT / "sources"
    src.mkdir(exist_ok=True)
    # JSON
    shutil.copy2(ROOT / "assets" / "data" / "products.json", src / "products.json")
    # Tailwind config
    shutil.copy2(ROOT / "tailwind.config.js", src / "tailwind.config.js")
    # JS
    for js in ["burger-menu.js", "search-modal.js", "catalogue-filters.js", "cookies.js"]:
        if (ROOT / "assets" / "js" / js).exists():
            shutil.copy2(ROOT / "assets" / "js" / js, src / js)
    # CSS compilé
    if (ROOT / "styles" / "output.css").exists():
        shutil.copy2(ROOT / "styles" / "output.css", src / "output.css")
    # Cookies CSS
    if (ROOT / "assets" / "css" / "cookies.css").exists():
        shutil.copy2(ROOT / "assets" / "css" / "cookies.css", src / "cookies.css")

    # Header + footer canoniques en HTML extraits
    import re
    inj = (ROOT / "scripts" / "inject-canonical-shell.py").read_text()
    m_h = re.search(r"CANONICAL_HEADER = f?'''(.*?)'''", inj, re.DOTALL)
    m_f = re.search(r"CANONICAL_FOOTER = '''(.*?)'''", inj, re.DOTALL)
    if m_h:
        (src / "header-canonique.html").write_text(f"<!-- Header canonique letablia.fr V4 -->\n{m_h.group(1)}")
    if m_f:
        (src / "footer-canonique.html").write_text(f"<!-- Footer canonique letablia.fr V4 -->\n{m_f.group(1)}")

    # Scripts Python (référence)
    for sc in ["build-from-json.py", "anonymize-brands.py", "inject-canonical-shell.py", "fix-policy.py"]:
        if (ROOT / "scripts" / sc).exists():
            shutil.copy2(ROOT / "scripts" / sc, src / sc)

    print(f"✅ Sources copiées dans {src}/")


def copy_fiches():
    fiches = EXPORT / "exemples-fiches"
    fiches.mkdir(exist_ok=True)
    for p in DATA["products"]:
        slug = p["slug"]
        if slug.startswith("produit/"):
            src_path = ROOT / slug / "index.html"
        else:
            src_path = ROOT / slug / "index.html"
        if src_path.exists():
            short = slug.split("/")[-1]
            shutil.copy2(src_path, fiches / f"{short}.html")
            print(f"✅ Fiche : {short}.html")

    # Aussi : index, catalogue, 5 familles, 3 packs, diagnostic, a-propos, faq, contact, cgv, mentions
    for src_rel, name in [
        ("index.html", "00-home.html"),
        ("catalogue.html", "00-catalogue.html"),
        ("a-propos.html", "00-a-propos.html"),
        ("faq.html", "00-faq.html"),
        ("contact.html", "00-contact.html"),
        ("diagnostic.html", "00-diagnostic.html"),
        ("cgv.html", "00-cgv.html"),
        ("mentions-legales.html", "00-mentions-legales.html"),
        ("confidentialite.html", "00-confidentialite.html"),
        ("produits/automatisations/index.html", "famille-automatiser.html"),
        ("produits/vendre/index.html", "famille-vendre.html"),
        ("produits/tableaux-de-bord/index.html", "famille-piloter.html"),
        ("produits/modeles/index.html", "famille-produire.html"),
        ("produits/guides-formations/index.html", "famille-securiser.html"),
        ("packs/e-commerce/index.html", "pack-e-commerce.html"),
        ("packs/freelance/index.html", "pack-freelance.html"),
        ("packs/tpe-conformite/index.html", "pack-tpe-conformite.html"),
    ]:
        sp = ROOT / src_rel
        if sp.exists():
            shutil.copy2(sp, fiches / name)
            print(f"✅ Page : {name}")


# ─────────────────────────── ZIP ──────────────────────────────────────
def make_zip():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    zip_path = ROOT / f"letablia-docs-export-{timestamp}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in EXPORT.rglob("*"):
            if f.is_file():
                zf.write(f, arcname=f.relative_to(EXPORT.parent))
    return zip_path


# ─────────────────────────── Main ──────────────────────────────────────
def main():
    print("=== build-docs-export.py ===\n")
    make_index()
    print("✅ index.html")
    make_architecture()
    print("✅ 01-architecture.html")
    make_design_system()
    print("✅ 02-design-system.html")
    make_vocab()
    print("✅ 03-vocabulaire-marque.html")
    make_policy()
    print("✅ 04-politique-forge.html")
    make_catalogue()
    print("✅ 05-catalogue.html")
    make_personas()
    print("✅ 06-personas-cibles.html")
    make_ergonomie()
    print("✅ 07-ergonomie.html")
    make_shell()
    print("✅ 08-header-footer.html")
    make_components()
    print("✅ 09-composants.html")
    make_scripts_doc()
    print("✅ 10-scripts-build.html")
    make_fiches()
    print("✅ 11-fiches-produits.html")
    make_legal()
    print("✅ 12-pages-legales.html")
    make_bugs()
    print("✅ 13-bugs-resolus.html")
    print()
    copy_sources()
    print()
    copy_fiches()
    print()
    zip_path = make_zip()
    size_kb = zip_path.stat().st_size // 1024
    print(f"\n✅ ZIP créé : {zip_path} ({size_kb} KB)")


if __name__ == "__main__":
    main()
