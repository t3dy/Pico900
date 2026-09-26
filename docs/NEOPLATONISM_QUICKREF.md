<!-- QUARANTINE-BANNER -->
> **QUARANTINED 2026-09-25: do not cite, quote or build on this file.**  
> audit/A3: certified by shape-only validators. See audit/A3_angelology_neoplatonism.md.  
> Rewrite from the sources under `docs/ORCHESTRATION.md` (RESEARCHER -> WRITER -> VERIFIER). Evidence in `audit/`.

# Neoplatonism Research — Quick Reference Card

**Keep this open while researching Pico's Neoplatonic theses.**

---

## 1. Archive Folders (Search Priority)

**🔴 CRITICAL — Start Here**
- **Michael J B Allen/** — Pico-Neoplatonism expert; go here first for every philosopher
- **Iamblichus/** — For theurgy, divine names, daemons
- **Chaldean Oracles/** — For divine names, mystical fire, theurgic claims
- **Tanaseanu-Döbler** — *Theurgy in Late Antiquity* (critical for Iamblichus)

**🟠 HIGH PRIORITY — Always Check**
- **Beierwaltes/** — Medieval transmission, ontology, Plotinus reception
- **Christian Platonism/** — Pseudo-Dionysius, Ficino (transmission layer)
- **Chiaradonna** — *Ontology in Early Neoplatonism* (foundational)
- **Dillon** — *The Middle Platonists* (Apuleius, general context)

**🟡 MEDIUM — As Needed**
- **O-Meara/** — Scholarly interpretation
- **Apuleis/** — Daemon cosmology
- **Nicomachus/** — Number mysticism, Pythagorean parallels

---

## 2. Philosophers → Key Concepts

| Philosopher | Key Concepts | Pico Connection |
|---|---|---|
| **Plotinus** | The One, emanation, Intellect, Soul, henosis | Metaphysics, ontology, mystical union |
| **Porphyry** | Substance, daemons, theurgy, virtue ethics | Daemon hierarchy, ethics, intermediaries |
| **Iamblichus** | Theurgy, henads, divine names, ritual | Theurgic theses (controversial) |
| **Proclus** | Henology, triadic structure, procession-reversion | Medieval reception, systematic Neoplatonism |
| **Chaldean Oracles** | Divine fire, divine names, henads | Theurgic foundation, divine names |
| **Nicomachus** | Number mysticism, arithmetic, harmonics | Kabbalah parallels, numeric theses |

---

## 3. Search Terms in PDFs

When browsing archive files, **Ctrl+F** for:

- **On Plotinus**: "Plotinus", "Enneads", "emanation", "noesis", "henosis", "One"
- **On Porphyry**: "Porphyry", "daemon", "theurgy", "Sententiae", "substantia"
- **On Iamblichus**: "Iamblichus", "Mysteries", "theurgic", "henad", "divine working"
- **On Proclus**: "Proclus", "Elements", "henads", "procession", "reversion"
- **On Chaldean Oracles**: "Chaldean", "oracle", "fragment", "nomina", "divine names"

---

## 4. Citation Templates

**Primary Neoplatonist Source:**
```
[Philosopher]. *[Work]*. [Section]. Trans. [Translator], p. [page].
Plotinus. *Enneads* 5.1.1. Trans. Armstrong, p. 234.
```

**Secondary Scholarship:**
```
[Author], *[Work]* (Publisher, [Year]), p. [page].
Michael J B Allen, *Neoplatonism and the Platonic Tradition* (Harvard UP, 1994), p. 78.
```

**Pico Citation:**
```
Pico, *Conclusions*, [Part].[Section].[Number].
Pico, *Conclusions*, II.i.1.
```

---

## 5. Data Workflow

**Mark a conclusion as Neoplatonic candidate:**
```python
python scripts/neoplatonism_research.py --philosopher plotinus
```

**See research status:**
```bash
python scripts/neoplatonism_research.py --status
```

**Check high-priority archives:**
```bash
python scripts/neoplatonism_research.py --list-archives
```

**Or, in Python:**
```python
from scripts.neoplatonism_research import NeoplatonismResearch
research = NeoplatonismResearch()
research.add_thesis_mapping(123, ["plotinus"], "candidate", "emanation language")
research.add_primary_source(123, "plotinus", "Enneads 5.1.1", "Armstrong", "234-245")
research.add_scholarship(123, "Michael J B Allen", "Neoplatonism...", "Ch. 3", "45-78")
```

---

## 6. Red Flags & Special Cases

🚩 **Heretical conclusions**: Theurgy, divine names, and daemon-magic theses were condemned (1486). Check `HERETICAL_RESEARCH_PLAN.md`.

🚩 **Emanation vs. Creation**: Pico merges Neoplatonic emanation with Christian creation. Check whether Pico reconciles them or treats them as compatible.

🚩 **Henads as Kabbalah**: Proclean henads map to Sephiroth AND divine names in Chaldean Oracles. When you see "divine names," both traditions may be invoked.

🚩 **Ficino's Mediation**: Ficino's Plotinus translation predates Pico. Check whether Pico cites Plotinus directly or through Ficino.

🚩 **Proclus Dominance**: Medieval scholastics got Neoplatonism mainly through Proclus (*Elements of Theology*). If a thesis echoes Neoplatonic structure via Aquinas, Proclus is likely behind it.

---

## 7. Status Labels

- **unmapped** — Not yet examined for Neoplatonism
- **candidate** — Possibly relevant; awaiting verification
- **primary_sourced** — Primary Neoplatonist source identified
- **scholarship_added** — Secondary scholarship found (especially Pico connections)
- **commentary_ready** — Full citation chain complete; ready to write commentary

---

## 8. Key Scholars (Consult Immediately)

| Scholar | Specialty | Must-Read |
|---|---|---|
| **Michael J B Allen** | Pico + Neoplatonism | *Neoplatonism and the Platonic Tradition* |
| **Copenhaver** | Pico condemned propositions, theurgy | *Pico on Trial* |
| **Beierwaltes** | Medieval Neoplatonism, ontology | *Denken des Einen* + essays |
| **Dillon** | Middle Platonism, daemon cosmology | *The Middle Platonists* |
| **Tanaseanu-Döbler** | Iamblichus, theurgy | *Theurgy in Late Antiquity* |
| **Chiaradonna** | Early Neoplatonism ontology | *Ontology in Early Neoplatonism* |

---

## 9. Next Steps

1. **Pick a philosopher** (start with Plotinus or Iamblichus)
2. **Find their archive folder** (consult Section 1)
3. **Search for Pico references** (Ctrl+F key terms from Section 3)
4. **Extract citations** (use templates from Section 4)
5. **Log in data** (use Python workflow from Section 5)
6. **Check status** (run `--status` to see progress)
7. **Write commentary** (cite primary + secondary + Pico together)

---

**Questions?** Check `NEOPLATONISM_SOURCING_PROTOCOL.md` (full rules) or `NEOPLATONISM_WORKFLOW.md` (phase-by-phase guide).
