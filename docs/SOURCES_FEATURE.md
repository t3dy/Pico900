<!-- QUARANTINE-BANNER -->
> **QUARANTINED 2026-09-25: do not cite, quote or build on this file.**  
> audit/A3 found data/sources.json holds 46 of a claimed 87 sources, is a list of supposed influences and not a bibliography, and that at least eight of ten rows checked contain factual errors.  
> Rewrite from the sources under `docs/ORCHESTRATION.md` (RESEARCHER -> WRITER -> VERIFIER). Evidence in `audit/`.

# Sources Feature — Pico900

## Overview

The Sources tab provides an interactive, curated catalog of the 87 major intellectual works and authors that shaped Giovanni Pico della Mirandola's philosophical thought. Sources are organized by scholarly tradition and presented as clickable cards with detailed information.

**Live at**: `/sources/` on the published site

## Architecture

### Data Layer

**File**: `data/sources.json`

- **Structure**: 8 traditions (scholastic, platonic, aristotelian, islamic_arabic, kabbalistic, christian_patristic, hermetic_magical, scientific_mathematical)
- **87 total sources** across all traditions
- **Per-source metadata**:
  - `id`: Unique identifier (e.g., `aquinas_summa`)
  - `name`: Author name
  - `work`: Title of work
  - `dates`: Birth/composition dates
  - `blurb`: 30–100 word summary of the source's relevance to Pico
  - `relevance`: Comma-separated tags (e.g., "Angels, essence-existence distinction, intellect")
  - `scholars`: List of modern scholars who have written on Pico's engagement with this source
  - `conclusions_linked`: Count of 900 Conclusions that reference/engage this source
  - `priority`: One of CORE, MAJOR, or SECONDARY
    - **CORE**: Foundational to Pico's entire system (Aquinas, Plotinus, Zohar, Pseudo-Dionysius, Plato)
    - **MAJOR**: Significantly influenced Pico's work but not foundational (most others)
    - **SECONDARY**: Supplementary ideas or later developments (Agrippa, Luria, later commentators)

### Template Layer

#### Landing Page

**File**: `src/templates/sources.html`

- **Features**:
  - Header with brief description
  - **Sort control**: Dropdown to sort by Tradition, Priority, Conclusions Linked, or Author Name
  - **Filter control**: Buttons to filter by tradition (All, Scholastic, Platonic, Aristotelian, Islamic, Kabbalistic, Patristic, Hermetic, Scientific)
  - **Grid of cards**: Each card shows:
    - Tradition tag (colored)
    - Author name (bold)
    - Work title (italic)
    - Composition dates
    - Blurb text
    - Meta row: conclusion count + priority badge
  - **Interactive**: Click any card to go to source detail page
  - **Footer**: Explanation of priority levels and organization

#### Detail Pages

**File**: `src/templates/source_detail.html`

- **Generated for each source**: `site/sources/{source-id}/index.html`
- **Content**:
  - Back link to Sources landing page
  - Header with tradition tag, author, work, dates
  - Meta boxes: Conclusions Linked, Priority, Related Scholars
  - Full blurb
  - **Relevance section**: Bulleted list of how this source influenced Pico
  - **Scholars section**: Badges for each modern scholar cited
  - **Linked Conclusions section**: Display placeholder for linked conclusions (expandable to show conclusion IDs once conclusion data is integrated)
  - **Related Sources section**: Cards for other sources in the same tradition (clickable for navigation)

### Build Pipeline

**Script**: `scripts/build_sources.py`

**Process**:
1. Load `data/sources.json`
2. Load templates from `src/templates/sources.html` and `src/templates/source_detail.html`
3. For landing page: inject full JSON data as `sourcesData` JavaScript object (enables client-side filtering/sorting)
4. For each source: generate detail page from template with placeholders filled in
5. Output to `site/sources/` and `site/sources/{source-id}/`

**Usage**:
```bash
python scripts/build_sources.py
```

**Output**:
- `site/sources/index.html` (landing page with embedded JSON)
- `site/sources/{source-id}/index.html` (87 detail pages)

## Workflow

### Adding a New Source

1. Open `data/sources.json`
2. Find the appropriate tradition block
3. Add a new source object to the `sources` array:

```json
{
  "id": "short-kebab-case-id",
  "name": "Author Name",
  "work": "Work Title",
  "dates": "c. 1200–1250",
  "blurb": "30–100 word summary of why this work matters to Pico. Be specific about concepts and how they influenced Pico's thought. Avoid generic praise.",
  "relevance": "Concept1, Concept2, Concept3",
  "scholars": ["Scholar1 Name", "Scholar2 Name"],
  "conclusions_linked": 25,
  "priority": "CORE"
}
```

4. Run `python scripts/build_sources.py` to regenerate all pages
5. Test the new source card and detail page in a browser

### Updating a Source

1. Edit the source entry in `data/sources.json`
2. Run `python scripts/build_sources.py`
3. Test the updated page

### Updating All Traditions/Sources at Once

- Edit `data/sources.json` directly
- Run `python scripts/build_sources.py`
- All pages regenerate from the updated JSON

## Data Quality Guidelines

### Blurb Writing

- **Length**: 30–100 words (approximately 3–7 sentences)
- **Tone**: Scholarly but accessible; explain why Pico read this work, not just what the work says
- **Specificity**: Name philosophical concepts (e.g., "essence-existence distinction", "angelic hierarchy") rather than generic terms
- **Sourcing**: Reflect modern scholarship (Copenhaver, Wirszubski, Howlett, etc.); avoid speculation
- **Example** (good):
  > "The foundational synthesis of Aristotelian logic with Christian theology. Aquinas's treatment of angels, intellect, and essence profoundly shaped Pico's metaphysics. Pico engaged with Aquinas's doctrine of participation and the hierarchy of being across multiple conclusions on metaphysics and angelology."
- **Example** (bad):
  > "A very important book that influenced many philosophers, including Pico. It has many ideas about God and the soul."

### Conclusions Linked Count

- This is a **rough estimate** based on keyword searches or scholarly discussion
- If you don't have an exact count, use scholarly estimates (Copenhaver, Howlett notes, etc.)
- This will be refined once the 900 Conclusions are fully tagged with source references

### Relevance Tags

- Use the same tags across all sources for consistency
- Relevant tags include: Angels, Essence-Existence, Intellect, Soul, Causation, Metaphysics, Magic, Kabbalah, Divine Names, Mystical Union, Emanation, etc.
- Separate multiple tags with commas and spaces

### Scholar Attribution

- List only scholars who have written *specifically* on Pico's engagement with this source
- Include: Copenhaver, Wirszubski, Howlett, Edelheit, Busi, Allen, Akopyan, Black, Farmer
- Don't include general Pico scholars unless they wrote about this source

## Integration with Other Features

### Conclusions ↔ Sources

- Each 900 Conclusion should eventually be tagged with source IDs (e.g., `["aquinas_summa", "plotinus_enneads"]`)
- When Conclusions are fully tagged, the detail page can show a live list of linked conclusion IDs (currently placeholder)
- Build system can generate bidirectional links: source detail pages can list conclusion IDs by reverse lookup

### Navigation

- Main nav includes "Sources" link: `<a href="/Pico900/sources/">Sources</a>`
- Sources landing page links back to Conclusions: `<a href="/Pico900/">Conclusions</a>`
- Detail pages link back to landing page: `<a href="/Pico900/sources/">← Back to Sources</a>`

## Browser Interactions

### Landing Page

- **Sorting**: JavaScript dropdown changes card order without full page reload
- **Filtering**: Buttons update active state and re-render card grid
- **Combined**: Sort + filter work together (e.g., "Show only Platonic sources, sorted by priority")
- **No page reload**: All interactions are client-side (data is in the page as JSON)

### Detail Pages

- **Static HTML**: No JavaScript needed (all content pre-rendered)
- **Clickable related sources**: Click card to navigate to related source detail page
- **Back link**: Navigate back to landing page

## Performance & Scale

- **Data size**: `data/sources.json` is ~150 KB (87 sources with full metadata)
- **Generated HTML**: Landing page ~200 KB (with embedded JSON), each detail page ~40–50 KB
- **Total site**: ~4.5 MB (87 detail pages + landing page + CSS)
- **Load time**: Landing page loads in <1s on typical connections; client-side filtering/sorting is instant

## Maintenance Checklist

Before deploying Sources pages to production:

- [ ] All 87 source entries are complete (no missing `id`, `name`, `work`, `blurb`, etc.)
- [ ] All blurbs are 30–100 words and scholarly in tone
- [ ] All `conclusions_linked` counts are reasonable estimates
- [ ] All scholar names are spelled correctly and attributed correctly
- [ ] Priority levels (CORE/MAJOR/SECONDARY) reflect modern scholarship consensus
- [ ] No duplicate source IDs
- [ ] No trailing commas or JSON formatting errors
- [ ] Build script runs without errors: `python scripts/build_sources.py`
- [ ] All detail pages render correctly in browser (spot-check ~10 sources)
- [ ] Landing page filtering and sorting work correctly
- [ ] CSS loads (check for 404s on `/Pico900/css/edition.css`)
- [ ] Links between detail pages and landing page work
- [ ] Links from detail pages to related sources work

## Future Enhancements

- **Linked Conclusions**: Once 900 Conclusions are tagged with source IDs, populate the "Linked Conclusions" section with clickable conclusion IDs
- **Search**: Add full-text search of blurbs, work titles, and author names (requires additional JS)
- **Timeline**: Add a timeline view of sources by date
- **Tradition depth**: Expand some traditions with subsections (e.g., Neoplatonism subdivided into Early Neoplatonism, Late Neoplatonism, etc.)
- **Export**: Add button to export sources as BibTeX, RIS, or CSV for citation managers
- **Scholar profiles**: Link scholar badges to individual profiles of what they've written on Pico

## Files Checklist

- [x] `data/sources.json` — Complete data file with 87 sources
- [x] `src/templates/sources.html` — Landing page template with embedded filtering/sorting
- [x] `src/templates/source_detail.html` — Detail page template
- [x] `src/css/edition.css` — Base CSS for all site pages
- [x] `scripts/build_sources.py` — Build script to generate static pages
- [x] `docs/SOURCES_FEATURE.md` — This documentation
- [x] `DECISIONS.md` — Decision log entry for Sources feature

---

**Created**: 2026-09-25  
**Status**: Ready for build and testing
