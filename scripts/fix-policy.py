#!/usr/bin/env python3
"""
fix-policy.py — Harmonise la politique « Satisfait ou Forgé ».

Règle officielle (Voice Bible + ADR-005) :
  « Satisfait ou Forgé : on corrige avant de rembourser.
    Pas de remboursement sans justification. »

Bug #5 Raphaël 2026-05-04.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    # Phrases incorrectes "sans justification" / "sans question"
    (
        r"satisfait ou remboursé, sans justification",
        "« Satisfait ou Forgé » : on corrige avant de rembourser",
    ),
    (
        r"satisfait ou remboursé,? sans justification",
        "« Satisfait ou Forgé » : on corrige avant de rembourser",
    ),
    (
        r"remboursement intégral sous 14 jours, sans justification",
        "politique « Satisfait ou Forgé » : on corrige avant de rembourser",
    ),
    (
        r"remboursement intégral sans justification",
        "politique « Satisfait ou Forgé » : on corrige avant de rembourser",
    ),
    (
        r"14 jours pour changer d'avis, remboursement intégral sans justification",
        "Politique « Satisfait ou Forgé » : si le système ne fonctionne pas comme décrit, on corrige ensemble. Remboursement uniquement si la correction n'aboutit pas, sous 14 jours",
    ),
    (
        r"remboursement intégral sous 14 jours, sans question",
        "politique « Satisfait ou Forgé » : on corrige avant de rembourser",
    ),
    (
        r"remboursé sans question",
        "remboursé après tentative de correction",
    ),
    (
        r"satisfait ou remboursé sans question",
        "« Satisfait ou Forgé »",
    ),
]

# Phrase canonique d'encart
CANONICAL_BLOCK = """<div class="bg-chene-6 border-l-4 border-mousse rounded-[6px] p-4 my-6 font-body text-[14px] text-ebene leading-[1.6]">
<strong>Politique « Satisfait ou Forgé »</strong> : si le système ne fonctionne pas comme décrit dans son environnement de prérequis, nous corrigeons ensemble. Le remboursement intégral n'intervient que si la correction n'aboutit pas, sous 14 jours via le mode de paiement initial.
</div>"""


def fix_file(path: Path) -> bool:
    text = path.read_text()
    original = text
    for pattern, replacement in REPLACEMENTS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    if text != original:
        path.write_text(text)
        return True
    return False


def main():
    files = list(ROOT.glob("**/*.html"))
    files = [p for p in files if "node_modules" not in str(p) and ".bak" not in p.name]
    modified = 0
    for path in files:
        if fix_file(path):
            print(f"✅ {path.relative_to(ROOT)}")
            modified += 1
    print(f"\n{modified}/{len(files)} fichiers harmonisés")


if __name__ == "__main__":
    main()
