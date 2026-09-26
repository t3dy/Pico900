# Deployment State — Pico900

**Live URL**: https://t3dy.github.io/Pico900  
**Repository**: https://github.com/t3dy/Pico900  
**Host**: GitHub Pages  
**Base path**: `/Pico900/`  
**Status**: Bootstrapping (no live build yet)  

## GitHub Pages Configuration

- **Repository**: `t3dy/Pico900` (public)
- **Branch**: `main`
- **Source**: `/` (root of repo)
- **Base URL**: `https://t3dy.github.io/Pico900/`
- **Asset paths**: All assets served with `/Pico900/` prefix (not just `/`)

## Build Environment

- **Build command**: `python scripts/build_site.py`
- **Output directory**: `site/` (gitignored; regenerated on each deploy)
- **No npm, no Node, no frameworks**: Vanilla HTML/CSS/JS only

## Known Gotchas

1. **Base path `/Pico900/`**: All CSS, JS, and image paths in the HTML must include this prefix. If a page 404s or doesn't load styles, the base path is wrong.
   - ✗ `<link rel="stylesheet" href="css/edition.css">`
   - ✓ `<link rel="stylesheet" href="/Pico900/css/edition.css">`

2. **Static generation**: The site is built once locally and committed to the repo. There is no server-side computation. All filtering/search happens in the browser with vanilla JS.

3. **Asset size**: Keep JSON data files small. The full 900-conclusion dataset should be <5MB. If it grows larger, split into conclusion chunks.

## Deployment Workflow

1. Build locally: `python scripts/build_site.py`
2. Test locally: Open `site/index.html` in a browser
3. Commit changes: `git add . && git commit -m "message"`
4. Push to GitHub: `git push origin main`
5. GitHub Actions will deploy automatically (or it's already published to Pages)

## Environment Variables

None required for GitHub Pages deployment. All configuration is in `data/` JSON files.

## Rollback

If a deployment breaks:
1. Revert the commit: `git revert <commit_hash>`
2. Force rebuild locally: `rm -rf site/ && python scripts/build_site.py`
3. Push: `git push origin main`

## Future Considerations

- If we ever need server-side search, move to Vercel (currently GitHub Pages only per workspace policy)
- If the dataset grows past static site viability, consider splitting into a server-backed portal (but this is *not* planned for 2026)
