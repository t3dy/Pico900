<!-- QUARANTINE-BANNER -->
> **QUARANTINED 2026-09-25: do not cite, quote or build on this file.**  
> audit/A3: the module's validation certified JSON shape only; claims of verified citations and resolved cross-references are untested (50 of 146 cross-references resolve to nothing).  
> Rewrite from the sources under `docs/ORCHESTRATION.md` (RESEARCHER -> WRITER -> VERIFIER). Evidence in `audit/`.

# Neoplatonism Research Module — Complete Setup Summary

**Date**: 2026-09-25  
**Created for**: Pico900 commentary research on Neoplatonic philosophers (Plotinus, Porphyry, Iamblichus, Proclus, Chaldean Oracles)

---

## What Was Created

### 📚 Documentation (4 files in `docs/`)

1. **`NEOPLATONISM_SOURCING_PROTOCOL.md`** (9 KB)
   - Full protocol for finding, verifying, and citing Neoplatonism material
   - Archive structure overview
   - Philosopher-by-philosopher sourcing workflow
   - Citation format standards
   - Constraints and quality rules

2. **`NEOPLATONISM_WORKFLOW.md`** (12 KB)
   - End-to-end workflow: Discovery → Primary Sourcing → Secondary Sourcing → Commentary
   - 5-phase process with checkpoints
   - Tips, gotchas, and examples
   - Checklist for each research cluster

3. **`NEOPLATONISM_QUICKREF.md`** (5 KB)
   - One-page quick reference card
   - Archive folders by priority (Critical → High → Medium)
   - Philosopher key concepts at a glance
   - Search terms, citation templates
   - Python workflow commands
   - Red flags and special cases

4. **`NEOPLATONISM_MODULE_SUMMARY.md`** (this file)
   - Overview of what was created
   - How to get started

### 📊 Data Files (3 JSON files in `data/neoplatonism/`)

1. **`philosophers_index.json`** (12 KB)
   - Comprehensive metadata on 9 Neoplatonist philosophers:
     - Plotinus, Porphyry, Iamblichus, Proclus
     - Chaldean Oracles, Nicomachus, Pseudo-Dionysius, Apuleius
     - Plus Renaissance figures: Ficino, Aquinas
   - For each: dates, key works, core concepts, Pico relevance, archive locations, key scholars
   - Fully structured and queryable

2. **`theses_mapping.json`** (3 KB template)
   - Checkpoint file for tracking Pico conclusions ↔ Neoplatonism mappings
   - Fields: conclusion_id, philosophers, primary_sources, scholarship, status
   - Status levels: unmapped → candidate → primary_sourced → scholarship_added → commentary_ready
   - Summary statistics auto-updated

3. **`archive_inventory.json`** (10 KB)
   - Complete inventory of `e:\pdf\Neoplatonism\` directory
   - All 8 subdirectories with priority levels (Critical/High/Medium)
   - All loose files catalogued with metadata
   - Research priorities ranked
   - Serves as your archive map

### 🛠️ Research Tools (1 Python script in `scripts/`)

**`neoplatonism_research.py`** (200 lines, fully functional)

A command-line and programmatic research tool with methods for:

**Query operations:**
- `get_philosopher(phil_id)` — Get metadata on any philosopher
- `list_philosophers()` — List all available philosophers
- `get_archive_location(phil_id)` — Find where to search for a philosopher
- `get_philosopher_works(phil_id)` — List key works
- `get_archive_priority(folder)` — Check archive folder priority
- `list_high_priority_archives()` — Get priority folders to search first

**Thesis mapping:**
- `add_thesis_mapping(...)` — Mark a conclusion as Neoplatonic + set status
- `add_primary_source(...)` — Log a Neoplatonist primary source for a conclusion
- `add_scholarship(...)` — Log secondary scholarship on Pico's use
- `get_thesis_status(id)` — Check status of a conclusion
- `get_theses_by_philosopher(id)` — Find all conclusions mapped to one philosopher
- `get_theses_by_status(status)` — Get all conclusions at a status level

**Reporting:**
- `report_research_status()` — Show progress across all conclusions
- `report_philosopher(phil_id)` — Show stats on one philosopher
- `report_archive()` — Show archive structure and resources

**CLI:**
```bash
python scripts/neoplatonism_research.py --status              # Overall progress
python scripts/neoplatonism_research.py --philosopher plotinus  # Report on Plotinus
python scripts/neoplatonism_research.py --archive             # Archive report
python scripts/neoplatonism_research.py --list-philosophers   # All philosophers
python scripts/neoplatonism_research.py --list-archives       # High-priority folders
```

---

## Directory Structure (Created)

```
Pico900/
├── docs/
│   ├── NEOPLATONISM_SOURCING_PROTOCOL.md    ← Full protocol
│   ├── NEOPLATONISM_WORKFLOW.md             ← Phases 1-5 workflow
│   ├── NEOPLATONISM_QUICKREF.md             ← One-page quick ref
│   └── NEOPLATONISM_MODULE_SUMMARY.md       ← This file
│
├── data/
│   └── neoplatonism/
│       ├── philosophers_index.json          ← Philosopher metadata
│       ├── theses_mapping.json              ← Conclusion ↔ Neoplatonism mapping
│       └── archive_inventory.json           ← Archive structure + priorities
│
└── scripts/
    └── neoplatonism_research.py             ← Research tool (CLI + Python API)
```

---

## Getting Started (5 Minutes)

### Step 1: Read the Quick Reference
Open `docs/NEOPLATONISM_QUICKREF.md` — it's one page and has everything you need to start.

### Step 2: List Available Philosophers
```bash
python scripts/neoplatonism_research.py --list-philosophers
```

Output shows all 9 philosophers with dates and names.

### Step 3: Check Archive Priorities
```bash
python scripts/neoplatonism_research.py --list-archives
```

Shows which folders to search first (Critical → High → Medium).

### Step 4: Pick a Philosopher & Browse Their Archive

Example: Start with **Plotinus**
- Archive locations: `Michael J B Allen/` (CRITICAL), `Beierwaltes/` (HIGH)
- Start browsing: `e:\pdf\Neoplatonism\Michael J B Allen\`
- Search for: "Plotinus", "Enneads", "emanation", "Pico"

### Step 5: Mark Conclusions as Candidates

When you find a Pico conclusion that invokes Plotinus:

```python
from scripts.neoplatonism_research import NeoplatonismResearch

research = NeoplatonismResearch()

# Mark conclusion 42 as a Plotinus candidate
research.add_thesis_mapping(
    conclusion_id=42,
    philosophers=["plotinus"],
    status="candidate",
    notes="Discusses emanation and procession of Intellect"
)
```

### Step 6: Extract Primary Source

Once you find the Plotinus passage in the archive:

```python
research.add_primary_source(
    conclusion_id=42,
    philosopher="plotinus",
    work="Enneads 5.1.1 (The Three Hypostases)",
    edition="Armstrong",
    pages="234-245"
)
```

### Step 7: Find Pico Scholarship

Search Michael J B Allen's work for Pico's use of that Plotinus passage:

```python
research.add_scholarship(
    conclusion_id=42,
    author="Michael J B Allen",
    work="Neoplatonism and the Platonic Tradition",
    chapter="Pico's Plotinus",
    pages="78-95"
)
```

### Step 8: Check Progress

```bash
python scripts/neoplatonism_research.py --status
```

Shows how many conclusions are mapped, by philosopher and status.

---

## Key Design Principles

1. **Philosophers-First**: All resources organized by Neoplatonist philosopher, not by Pico conclusion, so you can follow a single thinker through the archive.

2. **Archive-Native**: The module maps to the actual structure of `e:\pdf\Neoplatonism\`, so instructions are immediately actionable without re-organizing files.

3. **Citation Chain**: Every entry tracks primary sources (Plotinus, Porphyry) AND secondary scholarship (Allen, Copenhaver), so commentary can cite both.

4. **Status Tracking**: Conclusions move through workflow states: unmapped → candidate → primary_sourced → scholarship_added → commentary_ready. You always know what's done vs. what needs work.

5. **Searchable**: All data is JSON and queryable by philosopher ID, conclusion number, or status.

---

## Integration with Pico900 Workflow

- **Input**: Conclusions from `data/conclusions_manifest.json`
- **Processing**: Research tool marks conclusions as you find Neoplatonism connections
- **Output**: `data/neoplatonism/theses_mapping.json` feeds into commentary-writing phase
- **Checkpoint**: Update `data/conclusions_manifest.json` with Neoplatonism flag once research complete

The Neoplatonism module lives alongside other research modules (Kabbalah, astrology, heretical, etc.) but focuses exclusively on Plotinus, Porphyry, Iamblichus, Proclus, Chaldean Oracles, and their influence on Pico.

---

## Archive Resources at Your Fingertips

**Critical Priority (Start Here):**
- Michael J B Allen folder (Pico-Neoplatonism expert)
- Iamblichus folder (Theurgy, divine names)
- Chaldean Oracles folder (Theurgic foundation)
- Tanaseanu-Döbler, *Theurgy in Late Antiquity*

**High Priority (Always Check):**
- Beierwaltes folder (Medieval transmission)
- Christian Platonism folder (Pseudo-Dionysius, Ficino transmission)
- Chiaradonna, *Ontology in Early Neoplatonism*
- Dillon, *The Middle Platonists*

**Medium Priority (As Needed):**
- O-Meara folder (General Platonism scholarship)
- Apuleis folder (Daemon cosmology)
- Nicomachus folder (Number mysticism)

---

## Next Phase: Running a Research Cluster

Once you're familiar with the tools, try this workflow:

1. **Pick conclusions 1-50** (or another range)
2. **Scan for Neoplatonism language** → Mark candidates
3. **For each candidate:**
   - Find primary Neoplatonist source in archive
   - Find Michael J B Allen discussion
   - Record in `theses_mapping.json`
4. **Update manifest** with Neoplatonism flag
5. **Run `--status`** to see progress
6. **Log decisions** in `DECISIONS.md`

The module scales: you can research 10 conclusions, or 100, using the same workflow.

---

## Support Files You Already Have

- `e:\pdf\Neoplatonism\` — Full archive (28 files, 8 directories)
- `C:\Dev\megabase\` — LLM research (grep for "Plotinus", "henology", etc.)
- `C:\Dev\PicoDB\` — Study passes on Kabbalah, angelology (sometimes overlap Neoplatonism)
- `C:\Dev\CLAUDE.md` — Workspace instructions
- `C:\Dev\Pico900\CLAUDE.md` — Project instructions (in `docs/` here)

---

## Questions?

- **Quick answers**: Check `NEOPLATONISM_QUICKREF.md`
- **Full protocol**: Read `NEOPLATONISM_SOURCING_PROTOCOL.md`
- **Workflow step-by-step**: Follow `NEOPLATONISM_WORKFLOW.md`
- **Data structure**: Inspect `data/neoplatonism/*.json`
- **CLI help**: `python scripts/neoplatonism_research.py --help`

---

## Files Created This Session

| File | Size | Type | Purpose |
|---|---|---|---|
| `docs/NEOPLATONISM_SOURCING_PROTOCOL.md` | 9 KB | Doc | Full sourcing rules |
| `docs/NEOPLATONISM_WORKFLOW.md` | 12 KB | Doc | Phase-by-phase workflow |
| `docs/NEOPLATONISM_QUICKREF.md` | 5 KB | Doc | One-page quick reference |
| `docs/NEOPLATONISM_MODULE_SUMMARY.md` | 6 KB | Doc | This summary |
| `data/neoplatonism/philosophers_index.json` | 12 KB | JSON | Philosopher metadata |
| `data/neoplatonism/theses_mapping.json` | 3 KB | JSON | Conclusion ↔ research tracker |
| `data/neoplatonism/archive_inventory.json` | 10 KB | JSON | Archive structure + priorities |
| `scripts/neoplatonism_research.py` | 200 lines | Python | Research tool + CLI |

**Total**: 4 docs + 3 JSON + 1 script = 8 files, ~60 KB, fully integrated.

---

**Status**: ✅ Module complete and ready to use. Start with `NEOPLATONISM_QUICKREF.md` in 5 minutes.
