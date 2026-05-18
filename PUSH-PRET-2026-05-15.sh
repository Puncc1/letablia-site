#!/usr/bin/env bash
# Push prod letablia-site — mission carte blanche 24h, 5 commits prêts
# Raphaël : `bash PUSH-PRET-2026-05-15.sh`
set -euo pipefail

cd "$(dirname "$0")"

echo "=== État local ==="
git status --short
git log --oneline -5
echo ""

echo "=== Commits prêts à pousser ==="
git log --oneline origin/main..HEAD 2>/dev/null || git log --oneline -5
echo ""

read -p "Pousser sur main ? (oui/non) : " confirm
if [[ "$confirm" != "oui" ]]; then
  echo "Annulé."
  exit 0
fi

# Push principal
git push origin HEAD:main

# Si Vercel suit master (per mémoire) :
echo ""
read -p "Pousser aussi sur master (Vercel deploy) ? (oui/non) : " confirm_master
if [[ "$confirm_master" == "oui" ]]; then
  git push origin HEAD:master
fi

echo ""
echo "=== Push effectué — vérifier Vercel deployment ==="
echo "Dashboard : https://vercel.com/letablia"
echo ""
echo "Vérifications post-deploy :"
echo "  curl -sI https://letablia.fr/produits/gardien-de-stock.html | grep -i canonical"
echo "  curl -s https://letablia.fr/robots.txt | grep -i GPTBot"
echo "  curl -s https://letablia.fr/sitemap.xml | head -3"
echo ""
echo "Rollback si besoin :"
echo "  git push origin HEAD~5:main --force-with-lease"
