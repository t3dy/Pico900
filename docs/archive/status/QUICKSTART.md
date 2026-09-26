# Pico900 — Quick Start Guide

## TL;DR

```bash
# Build the site
cd C:\Dev\Pico900
python scripts/build_site.py

# Test locally (option 1: HTTP server)
cd site
python -m http.server 8000
# Open http://localhost:8000/

# Deploy to GitHub Pages
git push origin main
```

Live: https://t3dy.github.io/Pico900/

---

## The Setup

- **What**: Digital edition of Pico's 900 Conclusions with facing-page Latin/English text, scholarly commentary, and search
- **Where**: Static HTML site on GitHub Pages (`t3dy/Pico900`)
- **Who built it**: Generator script (`scripts/build_site.py`) + styling (`src/css/`)
- **Current scope**: S3 (11 Averroist conclusions) ✅ Ready for production

## Build Command

```bash
cd C:\Dev\Pico900
python scripts/build_site.py
```

**Output**: Site in `site/` directory (all files, ~600KB)

**Time**: <1 second

## Test Locally

### With HTTP Server (Recommended)
```bash
cd C:\Dev\Pico900\site
python -m http.server 8000
```
Then open: `http://localhost:8000/`

### Direct (May have CSS issues on `file://`)
```
file:///C:/Dev/Pico900/site/index.html
```

## What to Test

1. **Index page** — All 11 conclusions visible
2. **Search** — Type "intellect" → filters cards
3. **Heretical filter** — Check box → only S3.C002 shows
4. **Click a card** → opens conclusion page
5. **Facing page** — Latin (left) + English (right)
6. **Next/Prev buttons** → navigation works
7. **Mobile view** — Resize browser → stacks correctly
8. **No errors** — Open F12 Console → nothing red

## Deploy to GitHub

```bash
git add scripts/ src/
git commit -m "S3 website proof-of-concept"
git push origin main
```

**Result**: Site live at https://t3dy.github.io/Pico900/ (wait 1-2 min)

## Project Structure

```
data/conclusions/
├── S1/  (95 Neoplatonic; data ready, building Phase 3)
├── S3/  (11 Averroist; LIVE ✅)
├── S4/  (12 Avicennist; data ready, building Phase 4)
└── S7/  (25 Hermetic; data ready, building Phase 5)

scripts/
└── build_site.py  (Generates HTML from JSON)

src/css/
├── edition.css     (Nav, typography, base styles)
└── conclusions.css (Facing-page, cards, filters)

site/  (Generated; gitignored)
├── index.html
├── about/index.html
├── conclusions/S3_C001.html ... S3_C011.html
└── css/
```

## Key Files

| File | What It Is |
|------|-----------|
| `scripts/build_site.py` | Generates the site |
| `src/css/edition.css` | Styles (nav, fonts, base) |
| `src/css/conclusions.css` | Styles (facing-page, cards, mobile) |
| `data/conclusions/S3/*.json` | Conclusion data (11 files) |
| `DEPLOY_STATE.md` | Configuration + status |
| `DEPLOYMENT_GUIDE.md` | Full build/test/deploy instructions |
| `HANDOVER_S3_WEBSITE_BUILD.md` | What was built, how to use it |

## Common Tasks

### Rebuild the site
```bash
python scripts/build_site.py
```

### Update styling
1. Edit `src/css/*.css`
2. Run `python scripts/build_site.py` (copies CSS to site/)
3. Test locally, then push

### Add more conclusions (Phase 3+)
1. Put S1/S4/S7 JSON in `data/conclusions/S1/` etc.
2. Run `python scripts/build_site.py`
3. Index automatically includes all sections

### Fix a conclusion's content
1. Edit `data/conclusions/S3/entry_S3.C00X.json`
2. Run `python scripts/build_site.py`
3. Conclusion page regenerated

## Documentation

- **DEPLOY_STATE.md** — Configuration, deployment details
- **DEPLOYMENT_GUIDE.md** — Step-by-step build/test/deploy guide with troubleshooting
- **HANDOVER_S3_WEBSITE_BUILD.md** — Full technical overview of what was built
- **CLAUDE.md** — Project context, sourcing strategy, phases

## Timeline

| Phase | Scope | Status |
|-------|-------|--------|
| Phase 0 | Heretical essay | In progress |
| Phase 1 | Infrastructure, scholars | Complete |
| **Phase 2** | **S1 sourcing** | **In progress** |
| Phase 3 | Build S1 pages | Waiting for Phase 2 |
| Phase 4 | S4 build | Waiting |
| Phase 5 | S7 build | Waiting |
| Phase 6 | Heretical essay integration | Waiting |

## Contact

See `CLAUDE.md` and `docs/` for full project context, research sources, and workflow.

---

**The site is ready. Run `python scripts/build_site.py` to rebuild anytime.**
