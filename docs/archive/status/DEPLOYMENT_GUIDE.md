# Pico900 Deployment Guide

**Last Updated**: 2026-09-26  
**Live URL**: https://t3dy.github.io/Pico900  
**Repository**: https://github.com/t3dy/Pico900  

## Overview

Pico900 is a static website built from JSON conclusion data. The site is generated locally using a Python script and deployed to GitHub Pages. All CSS and JavaScript are vanilla (no frameworks), and all asset paths use the `/Pico900/` base path for GitHub Pages.

## Current Status

**Proof of Concept**: S3 (11 Averroist conclusions) is publication-ready and deployed.

- 11 conclusion pages with full scholarly apparatus
- Index page with search/filter functionality
- About page with documentation
- Facing-page layout (Latin left, English right)
- Heretical conclusion flagging
- Responsive design (mobile-friendly)

## Prerequisites

- Python 3.8+
- Git
- GitHub account with push access to `t3dy/Pico900`

## Build Process

### 1. Generate Site from Data

```bash
cd C:\Dev\Pico900
python scripts/build_site.py
```

This script:
- Loads all `.json` files from `data/conclusions/S3/` (and other sections when available)
- Generates individual conclusion pages in `site/conclusions/`
- Generates `site/index.html` and `site/about/index.html`
- Copies CSS files to `site/css/`

**Output**: All files in `site/` directory (gitignored)

### 2. Test Locally

Open the generated site in a browser:
- **Index page**: `file:///C:/Dev/Pico900/site/index.html`
- **Conclusion page**: `file:///C:/Dev/Pico900/site/conclusions/S3_C001.html`
- **About page**: `file:///C:/Dev/Pico900/site/about/index.html`

Test functionality:
- [ ] Index page loads with all conclusion cards
- [ ] Search bar filters by Latin/English text
- [ ] Heretical filter shows only flagged conclusions
- [ ] Conclusion pages display facing-page layout (Latin left, English right)
- [ ] Charge & Defense sections are present
- [ ] Scholar citations display with quotes
- [ ] Previous/Next navigation links work
- [ ] About page loads and displays correctly
- [ ] Mobile view is responsive (narrow viewport)
- [ ] No console errors (F12 → Console)

### 3. Commit Changes

```bash
cd C:\Dev\Pico900

# The site/ directory is gitignored, so only source changes are committed
git status
git add scripts/ src/ data/conclusions/
git commit -m "Build message: Describe what changed"
git log --oneline | head -5
```

### 4. Push to GitHub

```bash
git push origin main
```

This triggers GitHub Pages to serve the repository. The site is published at: **https://t3dy.github.io/Pico900/**

### 5. Verify Deployment

After pushing, wait 1–2 minutes for GitHub to publish, then visit:
- https://t3dy.github.io/Pico900/
- https://t3dy.github.io/Pico900/conclusions/S3_C001.html
- https://t3dy.github.io/Pico900/about/

Check that:
- [ ] Pages load without 404s
- [ ] CSS styling is applied (not just plain HTML)
- [ ] Images/assets load correctly
- [ ] Search and filters work
- [ ] Navigation links work

## Site Structure

```
C:\Dev\Pico900/
├── data/
│   ├── conclusions/
│   │   ├── S1/          (95 Neoplatonic; ready for Phase 3)
│   │   ├── S3/          (11 Averroist; currently live)
│   │   ├── S4/          (12 Avicennist; ready for Phase 4)
│   │   └── S7/          (25 Hermetic; ready for Phase 5)
│   └── scholarships/    (Intellectual sources catalog)
├── src/
│   ├── css/
│   │   ├── edition.css         (Base styles, nav, typography)
│   │   └── conclusions.css     (Facing-page layout, cards)
│   ├── js/                     (Currently empty; vanilla JS inline in HTML)
│   └── templates/              (Sources feature templates)
├── scripts/
│   ├── build_site.py           (Main build script)
│   └── [other build scripts]
├── site/                       (Generated; gitignored)
│   ├── index.html
│   ├── about/index.html
│   ├── conclusions/S3_C001.html through S3_C011.html
│   └── css/
├── DEPLOY_STATE.md             (This file)
└── DEPLOYMENT_GUIDE.md         (You are here)
```

## Adding New Conclusion Sections

When S1, S4, or S7 data is ready:

1. Ensure JSON files are in `data/conclusions/S1/`, `data/conclusions/S4/`, or `data/conclusions/S7/`
2. Update `scripts/build_site.py` to load additional sections (if needed)
3. Run `python scripts/build_site.py`
4. Test locally
5. Commit and push

The index page will automatically include all conclusions from all sections.

## Customizing the Site

### Styling

- **Global styles** (nav, typography, responsive): `src/css/edition.css`
- **Conclusion-specific styles** (cards, facing-page, filters): `src/css/conclusions.css`

To update styling:
1. Edit `src/css/*.css`
2. Run `python scripts/build_site.py` (CSS files are copied to `site/`)
3. Test locally
4. Commit and push

### HTML Generation

The build script is in `scripts/build_site.py`. Key functions:

- `generate_conclusion_page()` — Creates individual conclusion pages
- `generate_index_page()` — Creates the index with conclusion cards
- `generate_about_page()` — Creates the about/documentation page

To customize HTML:
1. Edit function in `scripts/build_site.py`
2. Run the script
3. Test locally
4. Commit and push

## Troubleshooting

### Pages return 404

**Problem**: After pushing to GitHub, pages show 404 errors.

**Solution**: Check that the base path `/Pico900/` is in all CSS/JS/image URLs. The repository is published from `https://t3dy.github.io/Pico900/`, not `https://t3dy.github.io/`.

Look for incorrect paths like:
- ❌ `<link rel="stylesheet" href="css/edition.css">`
- ✅ `<link rel="stylesheet" href="/Pico900/css/edition.css">`

### CSS not loading locally

**Problem**: Styles don't appear when opening `file:///C:/Dev/Pico900/site/index.html`.

**Solution**: This is normal for `file://` URLs in some browsers due to CORS. Use a local server instead:

```bash
# Python 3
cd C:\Dev\Pico900\site
python -m http.server 8000

# Then open: http://localhost:8000/
```

### Missing files after build

**Problem**: HTML pages exist but some are missing.

**Solution**: Check that JSON files exist in `data/conclusions/S3/` (or other sections). The build script only creates pages for conclusions that have JSON data.

```bash
# Count JSON files in S3
Get-ChildItem -Path "C:\Dev\Pico900\data\conclusions\S3" -Filter "*.json" | Measure-Object
```

### Build script errors

**Problem**: `python scripts/build_site.py` fails with an error.

**Solution**: Check that:
1. Python 3.8+ is installed: `python --version`
2. All JSON files in `data/conclusions/S3/` are valid (no syntax errors)
3. Output directories exist (script creates them, but check `site/` and `site/conclusions/`)

## Full Deployment Checklist

- [ ] Data in `data/conclusions/S3/*.json` (or other sections) is complete and valid JSON
- [ ] Run `python scripts/build_site.py` successfully
- [ ] Test locally (all pages load, styling applied, no console errors)
- [ ] Check search/filter functionality works
- [ ] Check responsive design (mobile viewport)
- [ ] Check navigation between pages
- [ ] Commit changes to git: `git add scripts/ src/ && git commit -m "..."`
- [ ] Push to main: `git push origin main`
- [ ] Wait 1–2 minutes for GitHub Pages to publish
- [ ] Visit https://t3dy.github.io/Pico900/ and verify live site
- [ ] Test live pages (search, navigation, styling)

## Performance Notes

- **Page load**: Minimal (vanilla HTML/CSS/JS, no frameworks)
- **Search/filter**: Client-side only (instant, no server required)
- **Asset sizes**: CSS ~15KB, each page ~50KB
- **Total S3 site**: ~600KB (11 pages + CSS + HTML overhead)
- **All 4 sections (S1+S3+S4+S7)**: ~2MB (still well within static site limits)

## Support & Questions

For issues or questions:
1. Check `DEPLOY_STATE.md` for configuration details
2. Check `CLAUDE.md` for project context
3. Review `src/css/` for styling
4. Review `scripts/build_site.py` for generation logic

---

**Next Steps**

1. ✅ S3 proof-of-concept is live
2. 🔄 Phase 2: Complete S1 sourcing (Latin, translations, citations)
3. ⏳ Phase 3: Build S1 pages
4. ⏳ Phase 4: Complete S4 and build
5. ⏳ Phase 5: Complete S7 and build
6. ⏳ Phase 6: Integrate heretical essay with conclusion links
