# Pico900 Deployment Guide

## Status: Ready to Deploy

**Build Date**: 2026-09-26  
**Pages**: 929 conclusions + index + about page  
**Size**: 4.6MB  
**Target**: https://t3dy.github.io/Pico900  

## Quick Deploy to GitHub Pages

1. Copy generated site to docs folder:
   ```bash
   Copy-Item -Recurse site docs -Force
   ```

2. Commit and push:
   ```bash
   git add docs/
   git commit -m "Deploy Pico900: All 929 conclusions with full apparatus"
   git push origin main
   ```

3. Wait 1-2 minutes for GitHub to rebuild, then visit:
   https://t3dy.github.io/Pico900

## What's Deployed

- 929 conclusion pages with facing Latin/English text
- Full-text search (client-side JavaScript)
- Philosophical charge/defense for each conclusion
- Scholar citations (98.6% coverage)
- Responsive design for mobile and desktop
- Previous/next navigation between conclusions
- Index page with conclusion listings
- About page with project information

## Test Locally First

```bash
cd site
python -m http.server 8000
# Visit: http://localhost:8000
```

Verify:
- Index page loads and is searchable
- Click a conclusion and verify page displays correctly
- Navigation buttons work
- Styles are applied
- Mobile view works (resize browser)

## If Deployment Fails

1. Check GitHub Pages settings: https://github.com/t3dy/Pico900/settings/pages
2. Verify branch is `main` and folder is `/docs`
3. Check that docs/ folder exists locally with site content
4. Clear browser cache (Ctrl+Shift+R)

## Rebuild All 929 Pages

```bash
# Remove old build
rm -rf site

# Rebuild from JSON
python scripts/build_html_site.py

# Copy to deployment folder
Copy-Item -Recurse site docs -Force
```

All page paths automatically configured for /Pico900/ GitHub Pages base.

## Done!

The website is production-ready. All 929 conclusions have translations and scholarly apparatus. Just copy to docs/ and push to GitHub.
