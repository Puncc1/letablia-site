#!/usr/bin/env python3
"""
inject-canonical-shell.py — Injecte header + footer canoniques sur toutes les pages.

Cohérence demandée par Raphaël (bug #6) : header + footer identiques partout.
Inclut aussi :
  - bug #9 : dropdown header avec délai propre (pas opacity-0/invisible CSS pur, mais JS hover)
  - bug #10 : emojis ⚡ 📈 ◯ ◇ ▣ remplacés par SVG icons inline
  - bug #12 : pas de chemins doublés (suppression du lien "Voir tout le catalogue" redondant)

Usage : python3 scripts/inject-canonical-shell.py
"""
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent

# SVG icons compacts pour les 5 familles (24×24)
SVG_AUTO = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-2 -mt-0.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
SVG_VEND = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-2 -mt-0.5"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>'
SVG_PILOT = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-2 -mt-0.5"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>'
SVG_PROD = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-2 -mt-0.5"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>'
SVG_SECU = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-2 -mt-0.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'

CANONICAL_HEADER = f'''<header class="sticky top-0 z-40 bg-lin border-b border-pierre/30 h-[72px]">
      <div class="max-w-[1280px] mx-auto px-4 md:px-8 h-full flex items-center justify-between gap-4">
        <a href="/" class="font-display text-2xl text-chene whitespace-nowrap">L'établ'IA</a>

        <nav class="hidden md:flex items-center gap-7">
          <div class="relative group" data-dropdown>
            <a href="/catalogue.html" class="font-body text-base text-ebene hover:text-chene flex items-center gap-1 cursor-pointer transition py-2">
              Catalogue
              <svg width="10" height="10" viewBox="0 0 10 10" fill="none" class="opacity-60 group-hover:opacity-100"><path d="M1 3L5 7L9 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
            <div class="absolute top-full left-0 pt-1 w-[260px] opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity duration-150 pointer-events-none group-hover:pointer-events-auto" data-dropdown-menu>
              <div class="bg-lin border border-pierre/30 rounded-[8px] shadow-md py-2">
                <a href="/produits/automatisations/" class="block px-4 py-2 font-body text-[14px] text-ebene hover:bg-chene-6 hover:text-chene transition">{SVG_AUTO}Automatiser</a>
                <a href="/produits/vendre/" class="block px-4 py-2 font-body text-[14px] text-ebene hover:bg-chene-6 hover:text-chene transition">{SVG_VEND}Vendre</a>
                <a href="/produits/tableaux-de-bord/" class="block px-4 py-2 font-body text-[14px] text-ebene hover:bg-chene-6 hover:text-chene transition">{SVG_PILOT}Piloter</a>
                <a href="/produits/modeles/" class="block px-4 py-2 font-body text-[14px] text-ebene hover:bg-chene-6 hover:text-chene transition">{SVG_PROD}Produire</a>
                <a href="/produits/guides-formations/" class="block px-4 py-2 font-body text-[14px] text-ebene hover:bg-chene-6 hover:text-chene transition">{SVG_SECU}Sécuriser</a>
              </div>
            </div>
          </div>

          <a href="/a-propos.html" class="font-body text-base text-ebene hover:text-chene transition">À propos</a>
          <a href="/faq.html" class="font-body text-base text-ebene hover:text-chene transition">FAQ</a>
          <a href="/contact.html" class="font-body text-base text-ebene hover:text-chene transition">Contact</a>
        </nav>

        <div class="hidden md:flex items-center gap-3">
          <button id="search-trigger" aria-label="Rechercher (⌘K)" class="text-pierre hover:text-chene transition p-2 rounded hover:bg-chene-6">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="8" cy="8" r="5.5" stroke="currentColor" stroke-width="1.5"/><path d="M12.5 12.5L16 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          </button>
          <a href="/diagnostic.html" class="bg-mousse text-lin font-semibold text-[14px] rounded-[6px] px-5 py-[10px] hover:opacity-90 transition whitespace-nowrap">Diagnostic gratuit</a>
        </div>

        <div class="md:hidden flex items-center gap-2">
          <button id="search-trigger-mobile" data-search-trigger aria-label="Rechercher" class="text-pierre p-2">
            <svg width="20" height="20" viewBox="0 0 18 18" fill="none"><circle cx="8" cy="8" r="5.5" stroke="currentColor" stroke-width="1.5"/><path d="M12.5 12.5L16 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          </button>
          <button id="menu-toggle" class="flex flex-col gap-[5px] p-1" aria-label="Ouvrir le menu">
            <span class="block w-6 h-[2px] bg-ebene"></span>
            <span class="block w-6 h-[2px] bg-ebene"></span>
            <span class="block w-6 h-[2px] bg-ebene"></span>
          </button>
        </div>
      </div>
    </header>

    <div id="mobile-menu" class="fixed inset-0 z-50 bg-lin flex-col items-center justify-center hidden">
      <button id="menu-close" class="absolute top-6 right-4 font-body text-2xl text-ebene leading-none p-2" aria-label="Fermer le menu">&times;</button>
      <nav class="flex flex-col items-center gap-6 mb-10 text-center">
        <a href="/catalogue.html" class="font-heading text-2xl text-ebene hover:text-chene">Catalogue</a>
        <div class="flex flex-col items-center gap-2 font-body text-base text-pierre">
          <a href="/produits/automatisations/" class="hover:text-chene">{SVG_AUTO}Automatiser</a>
          <a href="/produits/vendre/" class="hover:text-chene">{SVG_VEND}Vendre</a>
          <a href="/produits/tableaux-de-bord/" class="hover:text-chene">{SVG_PILOT}Piloter</a>
          <a href="/produits/modeles/" class="hover:text-chene">{SVG_PROD}Produire</a>
          <a href="/produits/guides-formations/" class="hover:text-chene">{SVG_SECU}Sécuriser</a>
        </div>
        <div class="border-t border-pierre/30 w-32 my-3"></div>
        <a href="/a-propos.html" class="font-body text-lg text-ebene hover:text-chene">À propos</a>
        <a href="/faq.html" class="font-body text-lg text-ebene hover:text-chene">FAQ</a>
        <a href="/contact.html" class="font-body text-lg text-ebene hover:text-chene">Contact</a>
      </nav>
      <a href="/diagnostic.html" class="bg-mousse text-lin font-semibold rounded-[6px] px-7 py-[14px] hover:opacity-90">Diagnostic gratuit</a>
    </div>'''


CANONICAL_FOOTER = '''<footer class="bg-ebene mt-12">
      <div class="max-w-[1200px] mx-auto px-4 pt-12 pb-6">
        <div class="flex flex-col gap-8 md:flex-row md:gap-0 md:justify-between">
          <div class="text-center md:text-left">
            <p class="font-display text-[20px] text-lin leading-snug">L'établ'IA</p>
            <p class="font-display text-[14px] text-pierre mt-1">Forgé pour votre métier</p>
          </div>

          <div>
            <p class="font-body font-semibold text-[13px] text-pierre uppercase tracking-[1px] mb-4">Catalogue</p>
            <ul class="flex flex-col gap-2">
              <li><a href="/catalogue.html" class="font-body text-base text-lin hover:text-chene transition">Tous les systèmes</a></li>
              <li><a href="/produits/automatisations/" class="font-body text-base text-lin hover:text-chene transition">Automatiser</a></li>
              <li><a href="/produits/vendre/" class="font-body text-base text-lin hover:text-chene transition">Vendre</a></li>
              <li><a href="/produits/tableaux-de-bord/" class="font-body text-base text-lin hover:text-chene transition">Piloter</a></li>
              <li><a href="/produits/modeles/" class="font-body text-base text-lin hover:text-chene transition">Produire</a></li>
              <li><a href="/produits/guides-formations/" class="font-body text-base text-lin hover:text-chene transition">Sécuriser</a></li>
            </ul>
          </div>

          <div>
            <p class="font-body font-semibold text-[13px] text-pierre uppercase tracking-[1px] mb-4">L'établ'IA</p>
            <ul class="flex flex-col gap-2">
              <li><a href="/a-propos.html" class="font-body text-base text-lin hover:text-chene transition">À propos</a></li>
              <li><a href="/faq.html" class="font-body text-base text-lin hover:text-chene transition">FAQ</a></li>
              <li><a href="/diagnostic.html" class="font-body text-base text-lin hover:text-chene transition">Diagnostic gratuit</a></li>
              <li><a href="/contact.html" class="font-body text-base text-lin hover:text-chene transition">Contact</a></li>
            </ul>
          </div>

          <div>
            <p class="font-body font-semibold text-[13px] text-pierre uppercase tracking-[1px] mb-4">Informations</p>
            <ul class="flex flex-col gap-2">
              <li><a href="/mentions-legales.html" class="font-body text-base text-lin hover:text-chene transition">Mentions légales</a></li>
              <li><a href="/cgv.html" class="font-body text-base text-lin hover:text-chene transition">CGV</a></li>
              <li><a href="/confidentialite.html" class="font-body text-base text-lin hover:text-chene transition">Confidentialité</a></li>
              <li><span class="font-body text-base text-pierre">contact@letablia.fr</span></li>
            </ul>
          </div>
        </div>

        <div class="mt-8 border-t border-[rgba(160,152,137,0.30)] pt-6 flex flex-col md:flex-row gap-3 md:items-center md:justify-between">
          <p class="font-body text-[12px] text-pierre">© 2026 L'établ'IA · Systèmes digitaux pour professionnels francophones · Paiement unique</p>
          <p class="font-body text-[12px] text-pierre">Politique « Satisfait ou Forgé » : on corrige avant de rembourser.</p>
        </div>
      </div>
    </footer>'''


def inject(path: Path) -> bool:
    html = path.read_text()
    soup = BeautifulSoup(html, "html.parser")

    # Remplacer header
    header = soup.find("header")
    mobile_menu = soup.find("div", id="mobile-menu")
    if header:
        # Reconstruire le header + mobile-menu en une seule string
        new_shell = BeautifulSoup(CANONICAL_HEADER, "html.parser")
        # Supprimer ancien mobile-menu
        if mobile_menu:
            mobile_menu.decompose()
        header.replace_with(new_shell)

    # Remplacer footer
    footer = soup.find("footer")
    if footer:
        footer.replace_with(BeautifulSoup(CANONICAL_FOOTER, "html.parser"))

    new_html = str(soup)
    if new_html != html:
        path.write_text(new_html)
        return True
    return False


def main():
    pages = []
    for p in ROOT.glob("**/*.html"):
        if "node_modules" in str(p) or ".bak" in p.name or "scripts/" in str(p):
            continue
        pages.append(p)

    modified = 0
    for path in pages:
        if inject(path):
            print(f"✅ {path.relative_to(ROOT)}")
            modified += 1
    print(f"\n{modified}/{len(pages)} pages mises à jour avec header + footer canoniques")


if __name__ == "__main__":
    main()
