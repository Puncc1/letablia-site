#!/usr/bin/env python3
"""
anonymize-brands.py — Remplace toutes les marques citées par leurs catégories génériques.

Règle Raphaël 2026-05-04 : on ne cite AUCUNE marque, on dit le thème.
Voir HANDOFF-SITE-V4-11-BUGS-2026-05-04.md bug #3.

Usage : python3 scripts/anonymize-brands.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Ordre IMPORTANT : les remplacements plus spécifiques en premier
# (Google Sheets avant Sheets, WooCommerce avant Woo, etc.)
REPLACEMENTS = [
    # Variantes ECommerce
    (r"\bShopify\s*/\s*WooCommerce\b", "plateforme e-commerce"),
    (r"\bShopify\s*&\s*WooCommerce\b", "plateforme e-commerce"),
    (r"\bShopify\b", "plateforme e-commerce"),
    (r"\bWooCommerce\b", "plateforme e-commerce"),
    (r"\bShopify\s*·\s*Telegram\b", "Plateforme e-commerce · Notification"),
    # Tableurs
    (r"\bGoogle\s+Sheets\b", "tableur"),
    (r"\bGoogle-Sheets\b", "tableur"),
    (r"\bGoogleSheets\b", "tableur"),
    (r"\bSpreadsheets?\b", "tableur"),
    (r"\bSheets\b", "tableur"),
    (r"\bExcel\b", "tableur"),
    # Notes
    (r"\bNotion\b", "application de prise de notes"),
    # Email / messagerie
    (r"\bGmail\b", "messagerie électronique"),
    (r"\bOutlook\b", "messagerie électronique"),
    # Notification instantanée
    (r"\bTelegram\b", "messagerie instantanée"),
    (r"\bSlack\b", "messagerie d'équipe"),
    (r"\bDiscord\b", "messagerie d'équipe"),
    (r"\bWhatsApp\b", "messagerie instantanée"),
    # Service emailing
    (r"\bBrevo\b", "service d'emailing"),
    (r"\bMailchimp\b", "service d'emailing"),
    (r"\bSendinblue\b", "service d'emailing"),
    # Automatisation
    (r"\bMake\.com\b", "moteur d'automatisation"),
    (r"\bn8n\b", "moteur d'automatisation"),
    (r"\bZapier\b", "moteur d'automatisation"),
    # CRM
    (r"\bHubSpot\b", "CRM"),
    (r"\bSalesforce\b", "CRM"),
    (r"\bAirtable\b", "base de données"),
    # Capitalisations en titres mono (UPPERCASE)
    (r"SHOPIFY", "PLATEFORME E-COMMERCE"),
    (r"WOOCOMMERCE", "PLATEFORME E-COMMERCE"),
    (r"GOOGLE-SHEETS", "TABLEUR"),
    (r"GOOGLE SHEETS", "TABLEUR"),
    (r"NOTION", "PRISE DE NOTES"),
    (r"GMAIL", "MESSAGERIE"),
    (r"TELEGRAM", "NOTIFICATION"),
    (r"BREVO", "EMAILING"),
    (r"N8N", "AUTOMATISATION"),
    (r"EXCEL", "TABLEUR"),
]


def anonymize_file(path: Path) -> bool:
    """Anonymise un fichier. Retourne True si modifié."""
    original = path.read_text()
    text = original
    for pattern, replacement in REPLACEMENTS:
        text = re.sub(pattern, replacement, text)

    # Nettoyer les doublons "plateforme e-commerce / plateforme e-commerce"
    text = re.sub(r"plateforme e-commerce\s*/\s*plateforme e-commerce", "plateforme e-commerce", text)

    if text != original:
        path.write_text(text)
        return True
    return False


def main():
    html_files = list(ROOT.glob("**/*.html"))
    # Exclure backups et node_modules
    html_files = [
        p for p in html_files
        if "node_modules" not in str(p)
        and ".bak" not in p.name
        and "scripts/" not in str(p)
    ]

    modified = 0
    for path in html_files:
        if anonymize_file(path):
            print(f"✅ {path.relative_to(ROOT)}")
            modified += 1

    print(f"\n{modified}/{len(html_files)} fichiers modifiés")


if __name__ == "__main__":
    main()
