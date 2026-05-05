# letablia-site — Site web L'établ'IA

Site marketing de L'établ'IA. Déployé sur Vercel.

## Pages

| Fichier | URL |
|---------|-----|
| `index.html` | https://letablia.fr |
| `catalogue.html` | /catalogue |
| `a-propos.html` | /a-propos |
| `faq.html` | /faq |
| `contact.html` | /contact |
| `mentions-legales.html` | /mentions-legales |

## Stack
- HTML/CSS statique + Tailwind CSS
- Déploiement : Vercel (`vercel.json`)

## Développement

```bash
cd /home/raphael/letablia-site

# Compiler Tailwind CSS
npx tailwindcss -i styles/input.css -o styles/output.css --watch

# Déployer sur Vercel
vercel deploy
# OU
vercel --prod
```

## Fichiers clés
- `styles/input.css` → source Tailwind
- `styles/output.css` → CSS compilé (ne pas modifier manuellement)
- `tailwind.config.js` → config couleurs/thème L'établ'IA
- `vercel.json` → config déploiement
