<!-- QUARANTINE-BANNER -->
> **QUARANTINED 2026-09-25: do not cite, quote or build on this file.**  
> audit/A3: certified by shape-only validators. See audit/A3_angelology_neoplatonism.md.  
> Rewrite from the sources under `docs/ORCHESTRATION.md` (RESEARCHER -> WRITER -> VERIFIER). Evidence in `audit/`.

# Neoplatonism Sourcing Protocol for Pico900

Pico's *900 Conclusions* engage deeply with Neoplatonic philosophy, especially Plotinus, Porphyry, Iamblichus, and their medieval Platonist heirs. This protocol governs how we find, verify, and cite Neoplatonism material for commentary.

## Archive Structure

### Primary Archive: `e:\pdf\Neoplatonism\`

- **`Chaldean Oracles/`** — Primary texts and commentary on the Oracles (Pico relies on these for theurgic theses)
- **`Iamblichus/`** — Works by/on Iamblichus (*De Mysteriis*, *On the Mysteries*, theurgy)
- **`Michael J B Allen/`** — Critical studies on Neoplatonism and Renaissance reception (essential for Pico connections)
- **`Beierwaltes/`** — Werner Beierwaltes's work on Neoplatonism, ontology, and medieval reception
- **`O-Meara/`** — Dominic O'Meara's scholarship on Platonism
- **`Nicomachus/`** — Arithmetic and cosmological sources (Pico cites Nicomachus on number mysticism)
- **`Apuleis/`** — Apuleius's *Golden Ass* and Platonic philosophy (relevant for Pico's demonology)
- **`Christian Platonism/`** — Medieval and Renaissance Platonism (Ficino, Aquinas on Platonism)
- **Loose PDFs**: Dillon's *Middle Platonists*, Chiaradonna on *Ontology in Early Neoplatonism*, Roskam on Stoic/Platonic continuities, Tanaseanu-Döbler on theurgy

### Secondary Archives

- **`e:\pdf\renaissance magic\Pico\`** — 73 Pico-focused sources (some overlap with Neoplatonism)
- **`e:\pdf\renaissance magic\`** — Broader Renaissance magic/philosophy materials (check for Ficino, Pico's Neoplatonic transmission)
- **`C:\Dev\megabase\`** — LLM research conversations; grep for "Neoplatonism", "Plotinus", "Porphyry", "Iamblichus"
- **`C:\Dev\PicoDB\`** — Study passes on Kabbalah and angelology (often intersect Neoplatonism in Pico)

## Workflow: From Archive to Commentary

### Step 1: Identify Neoplatonist Theses in the 900

Scan the conclusions for:
- **Plotinus references** (ontology, emanation, soul, intellect, the One)
- **Porphyry references** (substance, categories, intellect, soul-body union)
- **Iamblichus references** (theurgy, divine names, daemons, rituals)
- **Proclus references** (henology, triad logic, procession/reversion)
- **Chaldean Oracles** (divine names, number mysticism, fire-theology)
- **Nicomachus** (arithmetic, cosmology)
- **Procline daemons, henads, triads** (medieval Platonism)

**Source**: Check `data/neoplatonism/theses_mapping.json` for pre-mapped conclusions.

### Step 2: Find Primary Texts

For each Neoplatonist philosopher invoked by a conclusion:

1. **Plotinus** (*Enneads*, trans. Armstrong)
   - Archive: Look in `Michael J B Allen/` and `Beierwaltes/`
   - Standard ref: Ennead.Tractate.Section (e.g., Enn. 5.1.1)

2. **Porphyry** (*Sententiae ad Intelligibilia*, *Isagoge*, *On Abstinence*)
   - Archive: Scattered in `Beierwaltes/`, `Michael J B Allen/`, `Christian Platonism/`
   - Standard ref: Section numbers in modern translations

3. **Iamblichus** (*De Mysteriis* / *On the Mysteries*, fragments)
   - Archive: `Iamblichus/` directory
   - Critical edition: des Places or Clarke/Dillon/Hershbell translations

4. **Proclus** (*Elements of Theology*, *Theologia Platonica*)
   - Archive: `Michael J B Allen/` (Allen is the expert on Proclus in Pico)
   - Standard ref: Chapter/proposition numbers

5. **Chaldean Oracles** (fragmentary)
   - Archive: `Chaldean Oracles/` + scattered in `Iamblichus/`
   - Standard ref: Fragment number (Majercik, des Places, or Majercik-Tardieu editions)

### Step 3: Search the Archive for Relevant Passages

**Protocol for searching**:
- Use the Markdown conversions if available (check file tree for `.md` versions)
- Extract key passage with citation (page number, section, line)
- Note the translation/edition used
- If PDF-only, extract text + page number for later verification

**Critical rule**: Always cite the *original* Neoplatonist source (Plotinus's *Enneads*, etc.) via modern standard translations. Secondary scholarship (Dillon, Beierwaltes) provides *interpretation* but goes in footnotes, not as primary evidence.

### Step 4: Cross-Reference Pico Commentary Scholarship

Once you have a Neoplatonist primary source, find secondary scholarship on Pico's use of it:

- **Michael J B Allen** — *Neoplatonism and the Platonic Tradition*, *Plato's Third Eye*, essays on Pico's Neoplatonism
  - Allen is *the* expert; every Neoplatonic thesis in Pico likely has an Allen chapter/article
- **Copenhaver** — *Pico on Trial* has a section on Neoplatonism and condemned propositions
- **Howlett** — Chapters on Pico's concordism sometimes invoke Proclus
- **Edelheit** — Scholastic reception of Neoplatonism in Pico
- **Dougherty** (ed.) — Anthology; check table of contents for Neoplatonism essays
- **Farmer** — The 900 as a debate-synthesis project (cites Plotinus, Porphyry)

**Strategy**: Search these secondary sources FIRST for direct quotations discussing Pico's use of X Neoplatonist. If found, use that quotation + cite the secondary source in commentary.

### Step 5: Populate the Manifest

After sourcing a conclusion's Neoplatonism connections:

1. Update `data/neoplatonism/theses_mapping.json`:
   ```json
   {
     "conclusion_id": 123,
     "neoplatonist_philosophers": ["Plotinus", "Porphyry"],
     "primary_sources": [
       {
         "philosopher": "Plotinus",
         "work": "Enneads 5.1.1 (The Three Hypostases)",
         "edition": "Armstrong",
         "pages": "234-245"
       }
     ],
     "scholarship": [
       {
         "author": "Michael J B Allen",
         "work": "Neoplatonism and the Platonic Tradition",
         "chapter": "Pico's Plotinus",
         "pages": "45-78",
         "quote_extracted": true
       }
     ],
     "status": "primary_sourced",
     "last_updated": "2026-09-25"
   }
   ```

2. Update `data/conclusions_manifest.json` to mark the conclusion as "neoplatonism_commentary_ready"

## Citation Format

**Primary Neoplatonist sources** in commentary:
```
[Author]. *Work*. [Translation/Edition]. [Section/Page].
Example: Plotinus. *Enneads* 5.1.1 (Armstrong trans., p. 234).
```

**Secondary scholarship** (footnote-level):
```
[Scholar], [work], [page].
Example: Michael J B Allen, *Neoplatonism and the Platonic Tradition*, p. 67.
```

**Pico connection** (if quoting a scholar discussing Pico's use):
```
[Scholar] argues that Pico's Thesis X relies on [Neoplatonist source].
[Scholar], [work], p. Y.
```

## Constraints

1. **Never quote full passages from copyrighted works** without noting edition/translator. Only short phrases + page number.
2. **Primary sources take precedence.** If a passage can be cited from Plotinus directly, do not cite it only from Dillon's secondary account.
3. **Track translation editions carefully.** Plotinus in Armstrong differs from Plotinus in other translations; specify which you're using.
4. **Verify multi-source claims.** If Allen says Pico took X from Plotinus, spot-check the Plotinus reference yourself in the archive before stating it as fact.
5. **Neoplatonism ≠ Kabbalah.** Pico synthesizes both, but keep them separate in commentary; a Neoplatonic source for a thesis does not mean Kabbalah isn't also invoked.

## Quick Reference: Philosophers → Archive Locations

| Philosopher | Key Archive Folder | Key Works |
|---|---|---|
| **Plotinus** | `Michael J B Allen/`, `Beierwaltes/` | *Enneads* (Armstrong trans.) |
| **Porphyry** | `Christian Platonism/`, `Michael J B Allen/` | *Sententiae*, *Isagoge*, *On Abstinence* |
| **Iamblichus** | `Iamblichus/`, `Chaldean Oracles/` | *De Mysteriis*, Fragments |
| **Proclus** | `Michael J B Allen/` | *Elements of Theology*, *Theologia Platonica* |
| **Chaldean Oracles** | `Chaldean Oracles/`, `Iamblichus/` | Fragments (Majercik ed.) |
| **Nicomachus** | `Nicomachus/` | *Arithmetic*, *Harmonics* |
| **Apuleius** | `Apuleis/` | *Golden Ass*, *Florida* |
| **Ficino** | `Christian Platonism/`, `e:\pdf\renaissance magic\` | *Theologia Platonica* (medieval Platonism reception) |

## Running the Research Pipeline

```bash
# 1. Index the archive
python scripts/index_neoplatonism.py

# 2. Query theses by philosopher
python scripts/query_neoplatonism.py --philosopher Plotinus

# 3. Export Neoplatonism findings for a conclusion range
python scripts/export_neoplatonism.py --start 1 --end 100 --format json
```

See `scripts/` for usage examples.

## Related Docs

- `SOURCING_PROTOCOL.md` — General sourcing for all conclusions
- `COMMENTARY_PROTOCOL.md` — When to quote vs. synthesize
- `HERETICAL_RESEARCH_PLAN.md` — Condemned propositions (some are Neoplatonic)
- `data/neoplatonism/philosophers_index.json` — Metadata on each Neoplatonist
- `data/neoplatonism/theses_mapping.json` — Conclusions → Neoplatonism connections
