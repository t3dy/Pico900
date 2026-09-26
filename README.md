# Pico900 — Digital Edition of Pico's 900 Conclusions

A snazzy website presenting Giovanni Pico della Mirandola's *900 Conclusiones* (900 Theses) with facing-page Latin and English translation, scholarly commentary, and a deep-dive essay on the heretical conclusions.

## Features

- **Facing-page edition**: Latin (from the free critical edition) alongside English translations
- **Scholarly commentary**: Verbatim quotations from modern Pico scholarship (Wirszubski, Copenhaver, Howlett, Edelheit, Dougherty, Busi, Allen, Akopyan, and others)
- **"Heretical" essay**: Synthesis of historical research on the 1486 condemned propositions, drawing on Copenhaver's *Pico on Trial*, the Dougherty anthology, and related scholarship
- **Searchable and filterable**: Browse by theme, by scholar, or by conclusion number
- **Hyperlinked**: Cross-references between related conclusions, philosophers, and magical/Kabbalistic concepts

## Live Site

https://t3dy.github.io/Pico900

## Repository

https://github.com/t3dy/Pico900

## Documentation

- **[CLAUDE.md](CLAUDE.md)** — Project overview, file structure, workflow phases, and context engineering strategy
- **[DECISIONS.md](DECISIONS.md)** — Decisions log
- **[DEPLOY_STATE.md](DEPLOY_STATE.md)** — Deployment configuration
- **[docs/SOURCING_PROTOCOL.md](docs/SOURCING_PROTOCOL.md)** — How to find translations in megabase
- **[docs/COMMENTARY_PROTOCOL.md](docs/COMMENTARY_PROTOCOL.md)** — When to quote scholarship vs. synthesize
- **[docs/HERETICAL_ESSAY_PLAN.md](docs/HERETICAL_ESSAY_PLAN.md)** — Structure for the condemned-propositions essay

## Related Projects

- **[PicoDB](../PicoDB)** — Full Pico research portal with 15+ study passes, SQLite database, and 73 processed research sources
- **[megabase](../megabase)** — LLM conversation archive containing translation passes and conceptual work on Pico's philosophy
- **[Claudiens](../Claudiens)** — Similar static-site digital edition for Maier's *Atalanta Fugiens*

## Sources

- **Critical edition (free)**: https://cds.lib.brown.edu/cds-project/picos-900-theses
- **Scholarship**: Wirszubski & Kristeller, Copenhaver, Howlett, Edelheit, Dougherty, Busi, Allen, Akopyan, Black, and others (see PicoDB)
- **Research materials**: 73 Markdown conversions in `E:\pdf\renaissance magic\Pico\Markdown`

## Building

```bash
python scripts/fetch_critical_edition.py      # Fetch Latin text
python scripts/merge_translations.py           # Consolidate translations from megabase
python scripts/build_site.py                   # Generate static HTML
```

## License

This digital edition is a research and teaching tool. Pico's *900 Conclusions* are in the public domain. Modern scholarly apparatus (commentary, citations, essays) is original work by Ted Hand and contributors, released under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
