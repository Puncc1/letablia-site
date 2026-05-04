#!/usr/bin/env python3
"""
build-from-json.py — Source unique de vérité = assets/data/products.json
Régénère :
  - catalogue.html (grille + filtres compteurs)
  - 5 pages familles (grilles)
  - 11 fiches produit (price-badge + price)
  - index.html best-sellers
  - 3 pages packs

Usage : python3 scripts/build-from-json.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "assets" / "data" / "products.json"

with DATA.open() as f:
    DB = json.load(f)

PRODUCTS = {p["slug"]: p for p in DB["products"]}
BUNDLES = {b["slug"]: b for b in DB["bundles"]}
FAMILIES = {f["slug"]: f for f in DB["families"]}
TOOLS = {t["slug"]: t["label"] for t in DB["tools"]}

FAMILY_VERB_UPPER = {
    "vendre": "VENDRE",
    "automatisations": "AUTOMATISER",
    "tableaux-de-bord": "PILOTER",
    "modeles": "PRODUIRE",
    "guides-formations": "SÉCURISER",
}

TARGETS_LABEL = {
    "e-commerce": "E-commerçant",
    "freelance": "Freelance",
    "agence": "Agence",
    "formateur": "Formateur",
    "tpe-generaliste": "TPE généraliste",
}


def fmt_tools(tools_slugs):
    """Liste de slugs → 'Plateforme e-commerce · Tableur'"""
    return " · ".join(TOOLS.get(s, s) for s in tools_slugs)


def card_html(p, ribbon_label=None):
    """Construit une card produit harmonisée."""
    family_label = FAMILY_VERB_UPPER.get(p["family"], p["family"].upper())
    tools_label = fmt_tools(p["tools"])
    targets = " ".join(p.get("targets", []))
    tools_data = " ".join(p["tools"])
    return f'''
        <a href="{p["url"]}" class="product-card group block bg-lin border border-pierre/30 rounded-[8px] overflow-hidden hover:border-chene transition"
           data-family="{p["family"]}"
           data-tools="{tools_data}"
           data-targets="{targets}"
           data-price="{p["price"]}"
           data-title="{p["title"].lower()}"
           data-keywords="{p["keywords"]}">
          <div class="bg-chene-6 h-[100px] flex items-center justify-center">
            <span class="font-mono text-chene text-[11px] uppercase tracking-[2px]">{family_label}</span>
          </div>
          <div class="p-5">
            <p class="font-mono text-[11px] text-chene uppercase tracking-[1px] mb-2">{tools_label}</p>
            <h3 class="font-heading text-[22px] text-ebene mb-2 leading-[1.2]">{p["title"]}</h3>
            <p class="font-body text-[14px] text-pierre leading-[1.5] mb-4">{p["blurb"]}</p>
            <div class="flex items-center justify-between">
              <span class="font-mono text-[18px] text-chene font-semibold">{p["price"]} €</span>
              <span class="font-body text-[14px] text-mousse group-hover:underline">Voir →</span>
            </div>
          </div>
        </a>
    '''


def bundle_card_html(b):
    """Card bundle (visuel différencié)."""
    return f'''
        <a href="{b["url"]}" class="product-card pack-card group block bg-lin border-2 border-mousse rounded-[8px] overflow-hidden hover:shadow-md transition"
           data-family="bundle"
           data-tools="bundle"
           data-targets="{' '.join(b.get('targets', []))}"
           data-price="{b['price']}"
           data-title="{b['title'].lower()}"
           data-keywords="{b['keywords']}">
          <div class="bg-mousse h-[100px] flex items-center justify-center">
            <span class="font-mono text-lin text-[11px] uppercase tracking-[2px]">PACK · ÉCONOMIE {b['savings']} €</span>
          </div>
          <div class="p-5">
            <p class="font-mono text-[11px] text-mousse uppercase tracking-[1px] mb-2">{b["subtitle"]}</p>
            <h3 class="font-heading text-[22px] text-ebene mb-2 leading-[1.2]">{b["title"]}</h3>
            <p class="font-body text-[14px] text-pierre leading-[1.5] mb-4">{b["blurb"]}</p>
            <div class="flex items-center justify-between">
              <div>
                <span class="font-mono text-[18px] text-mousse font-semibold">{b["price"]} €</span>
                <span class="font-mono text-[12px] text-pierre line-through ml-2">{b["price_individual"]} €</span>
              </div>
              <span class="font-body text-[14px] text-mousse group-hover:underline">Voir →</span>
            </div>
          </div>
        </a>
    '''


# ───────────────────────── catalogue.html ─────────────────────────
def build_catalogue():
    from bs4 import BeautifulSoup

    path = ROOT / "catalogue.html"
    html = path.read_text()
    soup = BeautifulSoup(html, "html.parser")

    # Grille = bundles d'abord (mis en avant) + tous produits
    cards = []
    for b in DB["bundles"]:
        cards.append(bundle_card_html(b))
    for p in DB["products"]:
        cards.append(card_html(p))
    cards_html = "\n".join(cards)

    grid = soup.find("div", id="products-grid")
    if grid is None:
        print("⚠️  Pas de #products-grid trouvée dans catalogue.html")
        return
    grid.clear()
    grid.append(BeautifulSoup(cards_html, "html.parser"))
    new_html = str(soup)

    # Mettre à jour les compteurs de filtres (Famille / Outil / Prix / Cible)
    counts_family = {f["slug"]: 0 for f in DB["families"]}
    counts_tool = {t["slug"]: 0 for t in DB["tools"]}
    counts_target = {k: 0 for k in TARGETS_LABEL}
    counts_price = {"low": 0, "mid": 0, "high": 0}
    for p in DB["products"]:
        counts_family[p["family"]] = counts_family.get(p["family"], 0) + 1
        for t in p["tools"]:
            counts_tool[t] = counts_tool.get(t, 0) + 1
        for tg in p.get("targets", []):
            counts_target[tg] = counts_target.get(tg, 0) + 1
        if p["price"] <= 19:
            counts_price["low"] += 1
        elif p["price"] <= 49:
            counts_price["mid"] += 1
        else:
            counts_price["high"] += 1

    # Regex helper pour update count d'un input filter
    def update_count(html, axis, value, count):
        # Pattern : input...data-axis="X"...value="Y"... ... <span class="text-pierre">(N)</span>
        pat = re.compile(
            rf'(data-axis="{axis}"\s+value="{re.escape(value)}"[^>]*>[^<]*<span class="text-pierre">\()\d+(\)</span>)'
        )
        return pat.sub(rf'\g<1>{count}\g<2>', html)

    for slug, n in counts_family.items():
        new_html = update_count(new_html, "family", slug, n)
    for slug, n in counts_tool.items():
        new_html = update_count(new_html, "tools", slug, n)
    for slug, n in counts_target.items():
        new_html = update_count(new_html, "targets", slug, n)
    for slug, n in counts_price.items():
        new_html = update_count(new_html, "price", slug, n)

    # Régénérer entièrement le bloc filtres (Famille / Outil / Prix / Cible)
    new_html = rebuild_filters_block(new_html, counts_family, counts_tool, counts_target, counts_price)

    path.write_text(new_html)
    print(f"✅ catalogue.html régénéré ({len(DB['products'])} produits + {len(DB['bundles'])} packs)")


def rebuild_filters_block(html, cf, ct, ctg, cp):
    """Régénère le bloc <aside id='filters'>...</aside> via BeautifulSoup."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    aside = soup.find("aside", id="filters")
    if aside is None:
        return html

    parts = []
    parts.append('''<div class="md:sticky md:top-[88px] bg-lin border border-pierre/30 rounded-[8px] p-5 md:p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-heading text-[18px] text-ebene">Filtrer</h2>
            <button id="reset-filters" class="font-body text-[12px] text-pierre hover:text-chene">Réinitialiser</button>
          </div>''')

    parts.append('\n          <fieldset class="mb-5">\n            <legend class="font-mono text-[11px] uppercase tracking-[1px] text-chene mb-2">Famille</legend>')
    for f in DB["families"]:
        n = cf.get(f["slug"], 0)
        parts.append(f'\n            <label class="flex items-center gap-2 mb-1 font-body text-[14px] text-ebene cursor-pointer"><input type="checkbox" class="filter-cb" data-axis="family" value="{f["slug"]}"> {f["title"]} <span class="text-pierre">({n})</span></label>')
    parts.append('\n          </fieldset>')

    parts.append('\n          <fieldset class="mb-5">\n            <legend class="font-mono text-[11px] uppercase tracking-[1px] text-chene mb-2">Outil</legend>')
    for t in DB["tools"]:
        n = ct.get(t["slug"], 0)
        if n == 0:
            continue
        parts.append(f'\n            <label class="flex items-center gap-2 mb-1 font-body text-[14px] text-ebene cursor-pointer"><input type="checkbox" class="filter-cb" data-axis="tools" value="{t["slug"]}"> {t["label"]} <span class="text-pierre">({n})</span></label>')
    parts.append('\n          </fieldset>')

    parts.append('\n          <fieldset class="mb-5">\n            <legend class="font-mono text-[11px] uppercase tracking-[1px] text-chene mb-2">Prix</legend>')
    for bucket in DB["price_buckets"]:
        n = cp.get(bucket["slug"], 0)
        parts.append(f'\n            <label class="flex items-center gap-2 mb-1 font-body text-[14px] text-ebene cursor-pointer"><input type="checkbox" class="filter-cb" data-axis="price" value="{bucket["slug"]}" data-min="{bucket["min"]}" data-max="{bucket["max"]}"> {bucket["label"]} <span class="text-pierre">({n})</span></label>')
    parts.append('\n          </fieldset>')

    parts.append('\n          <fieldset>\n            <legend class="font-mono text-[11px] uppercase tracking-[1px] text-chene mb-2">Cible</legend>')
    for slug, label in TARGETS_LABEL.items():
        n = ctg.get(slug, 0)
        parts.append(f'\n            <label class="flex items-center gap-2 mb-1 font-body text-[14px] text-ebene cursor-pointer"><input type="checkbox" class="filter-cb" data-axis="targets" value="{slug}"> {label} <span class="text-pierre">({n})</span></label>')
    parts.append('\n          </fieldset>\n        </div>')

    aside.clear()
    aside.append(BeautifulSoup("".join(parts), "html.parser"))
    return str(soup)


# ───────────────────────── pages familles ─────────────────────────
def build_familles():
    """Régénère les 5 pages familles via BeautifulSoup pour fiabilité."""
    from bs4 import BeautifulSoup

    for fam_slug in FAMILY_VERB_UPPER:
        path = ROOT / "produits" / fam_slug / "index.html"
        if not path.exists():
            print(f"⚠️  Page famille manquante : {path}")
            continue

        html = path.read_text()
        soup = BeautifulSoup(html, "html.parser")
        family_products = [p for p in DB["products"] if p["family"] == fam_slug]

        # Trouver le H2 "Les N systèmes de cette famille" puis sa grille suivante
        target_grid = None
        for h2 in soup.find_all("h2"):
            txt = h2.get_text(strip=True).lower()
            if "système" in txt and ("cette famille" in txt or "famille" in txt):
                # Chercher la prochaine div.grid à partir de h2
                node = h2
                while node:
                    node = node.find_next_sibling()
                    if node and node.name == "div" and "grid" in (node.get("class") or []):
                        target_grid = node
                        break
                if not target_grid:
                    # Chercher dans le parent
                    parent = h2.parent
                    if parent:
                        target_grid = parent.find("div", class_="grid")
                break

        if not target_grid:
            # fallback : 1ère div.grid sur la page
            target_grid = soup.find("div", class_="grid")

        if not target_grid:
            print(f"⚠️  Pas de grille trouvée dans {fam_slug}, skip")
            continue

        # Mettre à jour le H2 avec le bon nombre
        if h2 := soup.find(lambda t: t.name == "h2" and "système" in t.get_text().lower() and "famille" in t.get_text().lower()):
            n = len(family_products)
            h2.string = f"Les {n} système{'s' if n > 1 else ''} de cette famille"

        # Vider la grille et y insérer les nouvelles cards
        target_grid.clear()
        cards_soup = BeautifulSoup(
            "\n".join(card_html(p) for p in family_products),
            "html.parser",
        )
        target_grid.append(cards_soup)

        path.write_text(str(soup))
        print(f"✅ {fam_slug} régénéré ({len(family_products)} produits)")


# ───────────────────────── prix sur fiches produit ─────────────────────────
def update_product_prices():
    for p in DB["products"]:
        # Calculer le chemin physique du fichier (slug peut contenir produit/...)
        if p["slug"].startswith("produit/"):
            file_path = ROOT / p["slug"] / "index.html"
        else:
            file_path = ROOT / p["slug"] / "index.html"

        if not file_path.exists():
            print(f"⚠️  Fiche produit manquante : {file_path}")
            continue

        html = file_path.read_text()
        new_html = html

        # Remplacer price-badge et price
        new_html = re.sub(
            r'(<div class="price-badge">)[^<]*(</div>)',
            rf'\g<1>{p["price"]} €\g<2>',
            new_html,
        )
        new_html = re.sub(
            r'(<p class="price">)[^<]*(</p>)',
            rf'\g<1>{p["price"]} €\g<2>',
            new_html,
        )

        if new_html != html:
            file_path.write_text(new_html)
            print(f"✅ Prix synchronisé : {p['slug']} → {p['price']} €")
        else:
            print(f"   {p['slug']} : prix déjà à jour ({p['price']} €)")


# ───────────────────────── pages packs ─────────────────────────
PACK_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — L'établ'IA</title>
<meta name="description" content="{blurb}">
<link rel="stylesheet" href="/styles/output.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
</head>
<body class="bg-lin font-body text-ebene antialiased">
{header}

<main>
  <!-- Breadcrumb -->
  <nav class="max-w-[1280px] mx-auto px-4 md:px-8 py-4 font-mono text-[12px] text-pierre">
    <a href="/" class="hover:text-chene">Accueil</a> · <a href="/catalogue.html" class="hover:text-chene">Catalogue</a> · <span class="text-ebene">{title}</span>
  </nav>

  <!-- Hero -->
  <section class="bg-lin py-12 px-4">
    <div class="max-w-[920px] mx-auto text-center">
      <p class="font-mono text-[12px] uppercase tracking-[2px] text-mousse mb-3">PACK · ÉCONOMIE {savings} €</p>
      <h1 class="font-heading text-[36px] md:text-[44px] text-ebene leading-[1.15] mb-4">{title}</h1>
      <p class="font-body text-[18px] text-ebene/80 leading-[1.6] mb-6">{blurb}</p>
      <div class="flex items-center justify-center gap-4 mb-8">
        <span class="font-mono text-[36px] text-mousse font-semibold">{price} €</span>
        <span class="font-mono text-[18px] text-pierre line-through">{price_individual} €</span>
      </div>
      <a href="/contact.html?sujet=pack-{slug}" class="inline-block bg-mousse text-lin font-semibold rounded-[6px] px-8 py-[14px] hover:opacity-90 transition">Forger ce pack →</a>
      <p class="font-body text-[13px] text-pierre mt-3">Paiement unique · Guides inclus · Accompagnement personnalisé</p>
    </div>
  </section>

  <!-- Contenu du pack -->
  <section class="bg-lin py-12 px-4 border-t border-pierre/20">
    <div class="max-w-[1100px] mx-auto">
      <h2 class="font-heading text-[28px] text-ebene mb-8 text-center">Ce qui est inclus</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
        {included_cards}
      </div>
    </div>
  </section>

  <!-- Pourquoi un pack -->
  <section class="bg-chene-6 py-12 px-4 border-t border-pierre/20">
    <div class="max-w-[920px] mx-auto">
      <h2 class="font-heading text-[28px] text-ebene mb-6 text-center">Pourquoi un pack ?</h2>
      <ul class="space-y-3 font-body text-[16px] text-ebene/85 leading-[1.6]">
        <li>· <strong>Économie immédiate</strong> : {savings} € de moins que les achats séparés.</li>
        <li>· <strong>Cohérence d'usage</strong> : trois systèmes choisis pour fonctionner ensemble, pas en silo.</li>
        <li>· <strong>Installation guidée</strong> : un seul guide d'installation cohérent, pas trois manuels.</li>
        <li>· <strong>Politique « Satisfait ou Forgé »</strong> : on corrige avant de rembourser.</li>
      </ul>
    </div>
  </section>

  <!-- CTA final -->
  <section class="bg-lin py-12 px-4 border-t border-pierre/20">
    <div class="max-w-[720px] mx-auto text-center">
      <h2 class="font-heading text-[28px] text-ebene mb-4">Prêt à forger votre pack ?</h2>
      <p class="font-body text-[16px] text-ebene/80 mb-6">Une question avant ? Le diagnostic gratuit est là pour ça.</p>
      <div class="flex flex-col md:flex-row gap-3 md:gap-4 justify-center">
        <a href="/contact.html?sujet=pack-{slug}" class="bg-mousse text-lin font-semibold rounded-[6px] px-7 py-[14px] hover:opacity-90 transition">Forger ce pack — {price} €</a>
        <a href="/diagnostic.html" class="bg-transparent text-ebene border-2 border-ebene font-semibold rounded-[6px] px-7 py-[14px] hover:bg-ebene hover:text-lin transition">Diagnostic gratuit</a>
      </div>
    </div>
  </section>
</main>

{footer}
<script src="/assets/js/burger-menu.js" defer></script>
<script src="/assets/js/search-modal.js" defer></script>
<script src="/assets/js/cookies.js" defer></script>
</body>
</html>
"""


def build_packs():
    """Crée les pages /packs/<slug>/index.html depuis le template + le header/footer extraits d'index.html."""
    index = (ROOT / "index.html").read_text()
    # Extraire <header>...</header>
    m_h = re.search(r"<header[\s\S]*?</header>\s*<!--[^-]*?-->\s*<div id=\"mobile-menu\"[\s\S]*?</div>", index)
    if not m_h:
        m_h = re.search(r"<header[\s\S]*?</header>", index)
    header_html = m_h.group(0) if m_h else "<header></header>"

    # Extraire <footer>...</footer>
    m_f = re.search(r"<footer[\s\S]*?</footer>", index)
    footer_html = m_f.group(0) if m_f else "<footer></footer>"

    for b in DB["bundles"]:
        target_dir = ROOT / "packs" / b["slug"].replace("pack-", "")
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / "index.html"

        # Cards des produits inclus
        included_cards = []
        for prod_slug in b["products"]:
            p = PRODUCTS.get(prod_slug)
            if p:
                included_cards.append(card_html(p))
        included_html = "\n".join(included_cards)

        out = PACK_TEMPLATE.format(
            title=b["title"],
            blurb=b["blurb"],
            price=b["price"],
            price_individual=b["price_individual"],
            savings=b["savings"],
            slug=b["slug"],
            included_cards=included_html,
            header=header_html,
            footer=footer_html,
        )
        target.write_text(out)
        print(f"✅ Pack créé : {target.relative_to(ROOT)}")


# ───────────────────────── main ─────────────────────────
def main():
    print("=== build-from-json.py ===")
    build_catalogue()
    print()
    build_familles()
    print()
    update_product_prices()
    print()
    build_packs()
    print("\n✅ Tout régénéré depuis products.json")


if __name__ == "__main__":
    main()
