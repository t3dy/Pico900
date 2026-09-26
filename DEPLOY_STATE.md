# Deployment State — Pico900

**Live URL**: https://t3dy.github.io/Pico900  
**Repository**: https://github.com/t3dy/Pico900  
**Host**: GitHub Pages  
**Base path**: `/Pico900/`  
**Status**: S3 proof-of-concept ready (11 Averroist conclusions, facing-page layout, search/filter functional)  
**Last Built**: 2026-09-26  

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
- **Python version**: 3.8+

### What the Build Script Does

1. **Loads S3 conclusion data** from `data/conclusions/S3/*.json` (11 Averroist conclusions)
2. **Copies CSS files** from `src/css/` to `site/css/`
3. **Generates individual conclusion pages** with:
   - Facing-page layout (Latin left, English right)
   - Charge & Defense sections
   - Exegesis commentary
   - Scholar citations (2–4 per conclusion)
   - Heretical flagging and notes
   - Navigation (Previous/Next conclusion links)
4. **Generates index page** with:
   - Conclusion cards grid
   - Vanilla JS search functionality
   - Heretical conclusions filter
   - Full-text filtering by Latin/English text
5. **Generates about page** with project documentation
6. **All paths use `/Pico900/` base path** for GitHub Pages

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

## Site Structure (Generated)

```
site/
├── index.html              (Conclusions listing page with search/filter)
├── about/
│   └── index.html          (About & documentation page)
├── conclusions/
│   ├── S3_C001.html        (Prophecy in dreams — Averroist)
│   ├── S3_C002.html        (Monopsychism — Heretical)
│   ├── S3_C003.html        (Ultimate happiness & intellect union)
│   ├── S3_C004.html        (Soul particularity & unity of intellect)
│   ├── S3_C005.html        (Abstract being & first abstract)
│   ├── S3_C006.html        (Species generation: propagation vs putrefaction)
│   ├── S3_C007.html        (God as mover of the first heaven)
│   ├── S3_C008.html        (Celestial souls & substantial unity)
│   ├── S3_C009.html        (Heaven as simple body)
│   ├── S3_C010.html        (Modes of demonstration)
│   └── S3_C011.html        (Circular reasoning in demonstration)
├── css/
│   ├── edition.css         (Base styles, navigation, typography)
│   └── conclusions.css     (Facing-page layout, cards, controls)
└── sources/                (Existing sources feature)
```

## Implementation Status

### Completed (S3 Proof of Concept)

- [x] Static HTML generation from JSON data
- [x] Facing-page layout (Latin left, English right)
- [x] Charge & Defense sections
- [x] Exegesis commentary
- [x] Scholar citations (2–4 per conclusion, verified/cited/inferred confidence levels)
- [x] Heretical flagging with badge and notes
- [x] Tags and classification
- [x] Navigation (Previous/Next conclusion, Back to Home)
- [x] Index page with conclusion cards
- [x] Search functionality (vanilla JS, full-text)
- [x] Heretical filter (vanilla JS)
- [x] About page with documentation
- [x] Responsive design (mobile-friendly)
- [x] Print-friendly styles
- [x] All paths use /Pico900/ base path

### Next Phases (When Data Ready)

#### Phase 3 (S1 Neoplatonic — ~95 conclusions)
- Load S1 conclusion data from data/conclusions/S1/*.json
- Re-run `python scripts/build_site.py` to build all pages
- Sites will merge S1 + S3 with filtering by section

#### Phase 4 (S4 Avicennist — ~12 conclusions)
#### Phase 5 (S7 Hermetic — ~25 conclusions)

- Same build process for each section
- Final index will show all 4 sections with filtering

#### Phase 6 (Heretical Essay Integration)
- Add links from heretical conclusions (e.g., S3.C002) to Phase 0 heretical essay
- Q8 essay (epistemology of belief) links from S3.C002 monopsychism section

## Future Considerations

- If we ever need server-side search, move to Vercel (currently GitHub Pages only per workspace policy)
- If the dataset grows past static site viability, consider splitting into a server-backed portal (but this is *not* planned for 2026)
- Phase 3+ will automatically generate more pages; index page can filter by section or show all
