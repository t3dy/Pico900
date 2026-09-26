

# PROMPTS: what Ted has asked for (source of truth for intent)

This file collects every prompt Ted has typed for this project, verbatim, so that no agent has to reconstruct
his intent from a handover, a status file or a summary. **Read it before planning any work.** Status files
drift and have been wrong (see `audit/`); the prompts do not.

## How this file is used

1. **Precedence.** If a status file, handover or plan conflicts with a prompt, the prompt wins. If two prompts
   conflict, the later one wins unless it says otherwise. The one thing a prompt cannot override is the truth
   rules in `CLAUDE.md` (never invent text, quote gate, no self-approval): they are Ted's own values ("our high
   scholarly values", P20260926030948), and every prompt below assumes them.
2. **Stay current.** Run `python scripts/harvest_prompts.py` at the start of a session and before writing a
   handover. It rewrites only the generated block at the bottom, from the session transcripts, including messages
   typed mid-turn. `--check` exits 1 if the file is stale. Nothing outside the generated block is touched.
3. **Add, never edit.** The generated block is verbatim. Prompts from before 2026-09-26 00:01 UTC are not in the
   harvestable transcripts; add any of those by hand under "Hand-entered", with the date.
4. **Cite by ID.** Decisions, tickets and handovers cite `P<timestamp>` ids. A requirement with no prompt behind it
   is the agent's own idea and is labelled so.

## Working mode (from P20260926002233, P20260926000155, P20260926003059, P20260926011051, P20260926041326)

Ted is not an engineer and does not want to make engineering calls. **Do not ask him questions; use judgement, record
the decision in `DECISIONS.md` with the reason, and keep going.** Do as much work per prompt as is appropriate,
proceed through phases without waiting for "go", and end a session with a handover that the next window can run as a
`/goal`. Several Claude Code windows work on this project at once: name the files you own, do not edit files another
window is changing (check `git status`), and prefer new files to edits of shared ones. When something promised has not
been built yet, build it rather than reporting the gap.

## Standing requirements (editor's distillation; the prompts below are the authority)

Status vocabulary: `not started`, `specified` (a design exists), `partial`, `built` (exists and was run; say what
was verified). Updated: see the last line of this section.

| id | requirement | prompts | status | where |
|---|---|---|---|---|
| R1 | Work autonomously; never ask engineering questions; keep going across phases; hand over for `/goal` | P20260926002233, P20260926011051, P20260926041326 | see below | `CLAUDE.md` working mode |
| R2 | A sophisticated agentic coding environment and agile ticketing system, reflected in the system files; the orchestrator knows every new feature | P20260926002233, P20260926035544, P20260926030948 | see below | `docs/ORCHESTRATION.md`, `data/tickets/` |
| R3 | Writing at PhD / academic-encyclopedia standard, in the style of our scholars, no AI tropes ("not this but that"); every thesis gets historical and philosophical context and its historiographical importance from the scholars' point of view | P20260926005916, P20260926030948, P20260926035544 | see below | `docs/EDITORIAL_STANDARD.md`, `scripts/style_lint.py` |
| R4 | A method of reading the scholars (Markdown and audiobookmaker text versions) that yields mention statistics per thesis, dossiers of historiographical importance, connections to people in Pico's life, dynamic hyperlinks, rich metadata, a data ontology; artifacts such as RESEARCHNOTES and DATAONTOLOGY; system files and orchestrator kept current | P20260926035544, P20260926035711 | see below | `docs/DATA_ONTOLOGY.md`, `docs/RESEARCH_PROTOCOL.md`, `data/ontology/` (another window) |
| R5 | Deconstruct the scholarly resources into claims, warrants, open questions and historiographical importance scores on various metrics; a system that corrects itself as it goes | P20260926041129 | see below | `docs/CLAIMS_MODEL.md`, `scripts/claims_*.py` |
| R6 | All 900 theses with stubs, translations and commentary; Neoplatonic and Arabic philosophers first; a Neoplatonism research module | P20260926020557, P20260926002336, P20260926000155 | see below | `COVERAGE.md`, `data/neoplatonism/` (quarantined) |
| R7 | Digital editions with commentary of the *Oration*, *Commento*, *Heptaplus* and *De ente et uno*, as context for the scholastic theses; an ANGELICRESEARCH finding aid (Aquinas, Pseudo-Dionysius, Kabbalah, Proclus); a commentary on the angelic material using Allen and Black | P20260926003059, P20260926040957 | see below | `docs/angelology/` |
| R8 | A Sources tab of index-card blurbs (30-100 words) sortable by tradition; a People tab; merge PicoDB's scholars, figures, sources and documents; a comprehensive research companion | P20260926004626, P20260926005522, P20260926005558, P20260926005916 | see below | `docs/SITE_DESIGN.md` |
| R9 | Card frames that show a great deal of information while browsing theses and other pages: buttons, colour coding, click boxes, sorting, search; relationally browsable | P20260926041446, P20260926041502, P20260926041418 | see below | `docs/SITE_DESIGN.md` |
| R10 | Full-stack version: login, personal collections of cards for research and writing projects; best-practice relational browsing over rich metadata (historical and cultural contexts, philosophical turns, relationships); a relevance score on Pico's relationships for every thesis | P20260926041711 | see below | `docs/SITE_DESIGN.md`, `docs/CLAIMS_MODEL.md` |
| R11 | An essay on the Ficino-Pico dispute over the Neoplatonic metaphysics of the One, leading the reader through pages: a tour through *De ente et uno* and Aquinas's encounter with Dionysius as the background to Pico's moves against Ficino | P20260926041806 | see below | `docs/essays/` |
| R12 | This file is the source of truth for intent, and the system files know it | P20260926041326 | see below | `CLAUDE.md`, `docs/ORCHESTRATION.md`, `HANDOVER.md` |

## Hand-entered

None yet.

## Every prompt, verbatim

<!-- BEGIN GENERATED PROMPTS (scripts/harvest_prompts.py rewrites everything to END) -->

Generated 2026-09-26 04:18 UTC from 29 prompts. Timestamps are UTC. IDs are stable (timestamp of typing).

### P20260926000155  (2026-09-26 00:01, session 65e5ebb0)

> We are working on this project in multiple windows so make sure that you aren't stepping on the other window's toes. I want you to create a module for researching the Neoplatonism material for writing commentary on Pico's theses that deal with Plotinus, Proclus, Iamblichus and other Platonist philosophers. Our primary archive is in e:\pdf\Neoplatonism but there will be lots of relevant research elsewhere on the e:\pdf and its subfolders

### P20260926002049  (2026-09-26 00:20, session 41676ce9)

> <pasted_content id="9347">
> ## Pico900 Continuation — Phase 0 Complete
>
> **Status**: All agents finished. Phase 0 deliverables ready (13 heretical conclusions, essay outline, research notes).
>
> **Your choices**:
> 1. **Review + approve** the heretical essay and 13 entries, OR
> 2. **Deploy to GitHub Pages** now, OR
> 3. **Proceed to Phase 1** (harvest all 900 conclusions)
>
> **Read first**:
> - C:\Dev\Pico900\STATUS.md (quick state)
> - C:\Dev\Pico900\docs\HERETICAL_ESSAY_DRAFT_OUTLINE.md (essay outline)
> - C:\Dev\Pico900\data\conclusions\Heretical\S1_RESEARCH_NOTES.md (research)
>
> **System files** (if scaling to Phase 1):
> - ORCHESTRATION.md (agent dispatch)
> - DECISIONS.md (architecture decisions)
> - PHASE_0_DISPATCH_LOG.md (agent tracking)
>
> **Next agents** (if you want validation + analysis):
> - Dispatch R1-REVIEWER to validate all entries against STYLE_GUIDE
> - Dispatch RETROSPECTIVE to analyze Phase 0 + recommend Phase 1 improvements
>
> Standing by.
> </pasted_content id="9347">

### P20260926002233  (2026-09-26 00:22, session 41676ce9)

> It should be baked into our system files that you don't ask me questions like this. I'm not an engineer and don't know how to make those sorts of calls. Just do as much work as is appropriate per prompt without asking me a bunch of pesky questions. Make sure the system files reflect that you have set up a sophisticated agentic coding environment and agile ticketing development system. Get going

### P20260926002336  (2026-09-26 00:23, session 41676ce9)

> the next priorities should be the Neoplatonic and Arabic philosophers which we have already done some work researching

### P20260926002732  (2026-09-26 00:27, session 41676ce9)

> go

### P20260926003059  (2026-09-26 00:30, session 3bc261ff)

> We are also going to want to have digital editions with commentary of Pico's Oration, Commento, Heptaplus, and On Being and Unity for context. This will help us with the scholastic philosophers when we work on their commentary sections for the 900 theses. You already have access to the relevant research materials. I am particularly interested in Pico's discussion of angels (and it's background in Aquinas and Pseudo-Dionysius, Kabbalah and the metaphysics of Proclus) so make sure you have a solid sense of the angelic materials and give me an output ANGELICRESEARCH.md helping the orchestrator and agentic coding agents to find that material. Update our system files and style guides and handover doc and etc as necessary. Be aware that other windows of claude code are working on other aspects of the project, spawn agent swarms as necessary and don't ask me too much about what to do next just keep going

### P20260926004420  (2026-09-26 00:44, session 3bc261ff)

> go

### P20260926004626  (2026-09-26 00:46, session 2f4b7fcd)

> I want to add a Sources tab that leads to a page with cards (that can be clicked to go to pages with more information) that have index card length (30-100 words) blurbs about Pico's sources, which can be sorted into scholastic, platonic, aristotelian, arabic, kabbalistic etc using information from our scholarship to give the complete library of works Pico is known to have consulted in the production of his writing

### P20260926005522  (2026-09-26 00:55, session 2f4b7fcd)

> It occurs to me that we have work in the PicoDB that we should just merge with this project in terms of scholars of Pico, figures in his life, and sources and documents of primary and secondary sources etc. Ask me any questions about how to resolve any issues bringing over the material from PicoDB into tabs and pages of our project

### P20260926005558  (2026-09-26 00:55, session 2f4b7fcd)

> comprehensive research companion. use your judgement and look at PicoDB in Dev yourself

### P20260926005916  (2026-09-26 00:59, session 2f4b7fcd)

> use your judgement. People should get its own tab. reuse PicoDB writing and update as necessary since we are pushing the research forward. I want this to be academic encyclopedia quality writing at every stage, following the style of our scholars. I don't want it to sound like AI writing so be sure to include notes in the style guide not to speak in Claude-ish or use AI writing tropes like "it's not this but that"

### P20260926011051  (2026-09-26 01:10, session 41676ce9)

> /goal I don't want to have to say go a million times can you just proceed through multiple phases then give me a handover document to do similar in the next window and get a fuck ton of work done

### P20260926020530  (2026-09-26 02:05, session 6c373c49)

> <pasted_content id="81ad">
> ✓ Phase 0: Heretical essay research complete
> ✓ Phase 1: 236 conclusions standardized (100% gate pass)
> ✓ Phase 2: Website built, S7 citations filled, frameworks ready
> → Phase 3: 7 agents ready (essays, supplementation, extraction)
> → Phase 4: Specialist review + final assembly
> → Phase 5: Public deployment + launch
> </pasted_content id="81ad">

### P20260926020557  (2026-09-26 02:05, session 6c373c49)

> keep working until we have all 900 conclusions with stubs, translations, commentary

### P20260926021815  (2026-09-26 02:18, session 6c373c49)

> continue

### P20260926023227  (2026-09-26 02:32, session 6c373c49)

> go

### P20260926030742  (2026-09-26 03:07, session 6c373c49)

> continue then give me a handover document giving an overview of the next steps for the project that I can input as a slash goal

### P20260926030948  (2026-09-26 03:09, session 8857d983)

> Read handover and do an overview of our agentic coding environment and style guides and agent orchestration, making necessary improvements and auditing samples of all category of the writing to see where it needs to be improved to meet our high scholarly values. This should be writing on a PhD level for a digital humanities resource making available all the historical contexts and philosophical depths of the 900 theses.

### P20260926034343  (2026-09-26 03:43, session 8857d983)

> make any necessary tweaks to our system files based on what we have learned and get back to writing needed content of all kinds for the 900 theses

### P20260926035544  (2026-09-26 03:55, session 8857d983)

> /goal  create agent swarms and whatever other techniques to get as much of the researching and writing done for the entries as possible. Update the style guide and templates in our system files thinking about how best we can make sure each entry gets commentary on historical and philosophical contexts and historiographical importance of each of the 900 theses from the pov of our scholars. Perhaps we should keep statistics on how many mentions of each thesis we find in all our scholars, and have other metrics for the discovery and selection of important facts of various categories. This should be based on the knowledge that our scholars produce about the theses, so create a sophisticated method of reading our scholars in the pdf collection (we have markdown and text versions created by audiobookmaker of many btw that we could use as well since searching text is easier than pdf) to create dossiers of historiographical importance and connections with people in pico's life that we can dynamically hyperlink and rich metadata and a data ontology etc. output artifacts along the way like RESEARCHNOTES9252026.md or DATAONTOLOGY.md and make sure the system files and orchestrator are updated with knowledge and functional access to these new features we are building

### P20260926035711  (2026-09-26 03:57, session 8857d983)

> I am going to run the fable model just once. What can you contribute to our data pipeline for researching Pico and writing dynamic database information and translating that into artifacts to pass onto future LLM agents to do the writing of all the sorts of content we need for our digital edition of the 900 theses and pico's other texts

### P20260926040957  (2026-09-26 04:09, session 3bc261ff)

> write a commentary on the angelic material in oration, commento and heptaplus using Allen and Black

### P20260926041129  (2026-09-26 04:11, session 3bc261ff)

> use your judgement and just correct whatever needs updating. We should be building a robust system that can correct itself as it goes, and we should be deconstructing our scholarly resources into claims and warrants and open questions and historiographical importance scores based on various metrics, etc.

### P20260926041326  (2026-09-26 04:13, session 3bc261ff)

> we obviously have a lot of work to do and you should be relying on the system files which should have guidance as to how to build agent swarms to work on the writing that is needed. Don't get tripped up when everything you promised hasn't been built yet, and stop asking me what to do. Just methodically build what I've been asking for in my prompts. Output a PROMPTS.md that the system files know is collecting all my prompts as a source of truth for the project

### P20260926041418  (2026-09-26 04:14, session 3bc261ff)

> we are in the middle of an agentic environment audit in another window so we should be paying attention to any recent improvements in our system files for coding the structures and writing the stuff we need to write and building the website displays and making them relationally browsable

### P20260926041446  (2026-09-26 04:14, session 3bc261ff)

> think about the interface of the website I want the card frames to be designed so as to show off a lot of the information about the Pico topics when the reader is browsing our theses and other website pages and cards

### P20260926041502  (2026-09-26 04:15, session 3bc261ff)

> like there should be buttons and color coding and click boxes and ways for the reader to sort cards and search

### P20260926041711  (2026-09-26 04:17, session 3bc261ff)

> for the full stack version of the website I'll want to give the user the ability to log in and create their own collection of cards that can be used for research and writing projects on pico, we will want to design the cards and their frames and other dynamic web tools we're going to apply I don't know how to name everything. Think about best practices for sophisticated relational browsing of database entries with rich metadata to cover all the historical and cultural contexts, philosophical twists and turns of Pico's work and relationships. We should add relevance to pico's relationships data to every thesis

### P20260926041806  (2026-09-26 04:18, session 3bc261ff)

> like I want to produce an essay about the beef between ficino and pico over neoplatonic metaphysics of the one that will take the reader to pages with a tour through the de ente et uno and Aquinas's encounter with Dionysius as the background for Pico's moves against Ficino

<!-- END GENERATED PROMPTS -->
