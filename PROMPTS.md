

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
| R1 | Work autonomously; never ask engineering questions; keep going across phases; hand over for `/goal` | P20260926002233, P20260926011051, P20260926041326 | built | `CLAUDE.md` working mode, `HANDOVER.md` |
| R2 | A sophisticated agentic coding environment and agile ticketing system, reflected in the system files; the orchestrator knows every new feature | P20260926002233, P20260926035544, P20260926030948 | built | `docs/ORCHESTRATION.md`, `data/tickets/`, `scripts/tickets.py` |
| R3 | Writing at PhD / academic-encyclopedia standard, in the style of our scholars, no AI tropes ("not this but that"); every thesis gets historical and philosophical context and its historiographical importance from the scholars' point of view | P20260926005916, P20260926030948, P20260926035544 | built | `docs/EDITORIAL_STANDARD.md`, `scripts/entry_gate.py`, `audit/` |
| R4 | A method of reading the scholars (Markdown and audiobookmaker text versions) that yields mention statistics per thesis, dossiers of historiographical importance, connections to people in Pico's life, dynamic hyperlinks, rich metadata, a data ontology; artifacts such as RESEARCHNOTES and DATAONTOLOGY; system files and orchestrator kept current | P20260926035544, P20260926035711 | built | `docs/DATA_ONTOLOGY.md`, `docs/RESEARCH_PROTOCOL.md`, `data/inventory/`, `data/ontology/`, `research-packets/` |
| R5 | Deconstruct the scholarly resources into claims, warrants, open questions and historiographical importance scores on various metrics; a system that corrects itself as it goes | P20260926041129 | built | `docs/CLAIMS_MODEL.md`, `scripts/claims_*.py` (1,665 claims verified) |
| R6 | All 900 theses with stubs, translations and commentary; Neoplatonic and Arabic philosophers first; a Neoplatonism research module | P20260926020557, P20260926002336, P20260926000155 | partial | `data/inventory/theses.json` (900 inventory done), `entries/` (20 pass gate, 98 in remediation; T-ENT-01/02) |
| R7 | Digital editions with commentary of the *Oration*, *Commento*, *Heptaplus* and *De ente et uno*, as context for the scholastic theses; an ANGELICRESEARCH finding aid (Aquinas, Pseudo-Dionysius, Kabbalah, Proclus); a commentary on the angelic material using Allen and Black | P20260926003059, P20260926040957 | partial | `docs/angelology/`, `data/claims/angelology/` (14 packets verified; commentary/finding aid in backlog T-ANG-01/02) |
| R8 | A Sources tab of index-card blurbs (30-100 words) sortable by tradition; a People tab; merge PicoDB's scholars, figures, sources and documents; a comprehensive research companion | P20260926004626, P20260926005522, P20260926005558, P20260926005916 | specified | `docs/SITE_DESIGN.md`, `pico900_picodb_integration_plan.md`, `data/sources.json` (ticket T-SITE-05 ready) |
| R9 | Card frames that show a great deal of information while browsing theses and other pages: buttons, colour coding, click boxes, sorting, search; relationally browsable | P20260926041446, P20260926041502, P20260926041418 | specified | `docs/SITE_DESIGN.md`, `scripts/build_cards.py` (ticket T-SITE-01/02) |
| R10 | Full-stack version: login, personal collections of cards for research and writing projects; best-practice relational browsing over rich metadata (historical and cultural contexts, philosophical turns, relationships); a relevance score on Pico's relationships for every thesis | P20260926041711 | specified | `docs/SITE_DESIGN.md` (Workbench), `docs/INTELLECTUAL_NETWORK_DESIGN.md` (tickets T-SITE-07/08, T-REL-02) |
| R11 | An essay on the Ficino-Pico dispute over the Neoplatonic metaphysics of the One, leading the reader through pages: a tour through *De ente et uno* and Aquinas's encounter with Dionysius as the background to Pico's moves against Ficino | P20260926041806 | partial | Claims verified in `wallis1965-deente`, `howlett2021`, `edelheit2022`; essay queued (ticket T-FIC-01) |
| R12 | This file is the source of truth for intent, and the system files know it | P20260926041326 | built | `scripts/harvest_prompts.py`, `CLAUDE.md`, `docs/ORCHESTRATION.md`, `HANDOVER.md` |


## Hand-entered

None yet.

## Every prompt, verbatim

<!-- BEGIN GENERATED PROMPTS (scripts/harvest_prompts.py rewrites everything to END) -->

Generated 2026-09-26 05:12 UTC from 32 prompts. Timestamps are UTC. IDs are stable (timestamp of typing).

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

### P20260926041901  (2026-09-26 04:19, session 3bc261ff)

> so various theses and other cards with information about Pico's writings will have a score for relevance to his relations based on a study of what we know about the relevance of all his writing to all his relationships, in this case relevance to the beef with ficino but it could be with anyone he corresponded or quarrelled with

### P20260926042256  (2026-09-26 04:22, session a08fd9b0)

> <pasted_content id="e894">
> You are working on my existing Pico della Mirandola research/database project. Inspect the existing codebase, SQLite schema, ingestion scripts, metadata structures, scoring system, and documentation before making changes. Do not invent a parallel architecture if the project already has a suitable abstraction that can be extended.
> The goal is to upgrade the database so that Pico's intellectual relationships become first-class scholarly metadata and materially inform the interpretation/scoring of individual Pico texts, especially each of the 900 Conclusions, but also the Oration/De hominis dignitate, Heptaplus, Commento, Apologia, letters, and other Pico texts.
> This is a scholarly knowledge graph / research database, not merely a bibliography. The system must distinguish evidence about a relationship from an inference about how that relationship affected a particular proposition.
> CORE REQUIREMENT
> Every significant person in Pico's intellectual network should be representable as a structured entity, with relationships to Pico and relationships to particular texts, passages, propositions, sources, concepts, schools, and historical episodes.
> Do not reduce relationships to a single field such as "influence" or "associated_with."
> The system needs to represent distinctions such as:
>
> * correspondence
> * friendship
> * patronage
> * teacher/student relationship
> * collaborator
> * translator
> * source/intermediary
> * intellectual influence
> * philosophical interlocutor
> * philosophical disagreement
> * explicit polemical opponent
> * theological opponent
> * trial/commission participant
> * institutional relationship
> * acquaintance
> * member of same intellectual circle
> * contemporary whose work Pico studied
> * person whose work Pico cited
> * person whose work Pico appears to have known indirectly
> * posthumous interpreter/editor
> * later respondent/reception figure
>
> These relationship types must have evidence, dates where possible, confidence, and provenance.
> IMPORTANT SCHOLARLY PRINCIPLE
> Do NOT assume that every relationship constitutes "influence."
> For example:
> Pico ↔ Ficino:
> friendship, correspondence, intellectual exchange, Platonist relationship, philosophical disagreement, possible influence.
> Pico ↔ Elia del Medigo:
> teacher/interlocutor, Aristotelian/Averroist transmission, Hebrew/Jewish intellectual intermediary, collaboration/consultation.
> Pico ↔ Flavius Mithridates:
> translator, Hebrew/Kabbalistic collaborator, teacher, textual intermediary.
> Pico ↔ Yohanan Alemanno:
> Jewish intellectual collaborator/interlocutor, Kabbalistic source/intermediary, later testimony concerning their collaboration.
> Pico ↔ Ermolao Barbaro:
> correspondent and philosophical interlocutor; explicit dispute concerning scholastic versus humanist philosophical language.
> Pico ↔ Pedro Garcia:
> institutional/theological opponent in the 1487 investigation; author of a direct response to Pico's Apologia.
> Pico ↔ Jean Cordier:
> Parisian intellectual connection and later member of the papal commission; importantly, Cordier defended Pico's Conclusions rather than simply opposing him.
> Pico ↔ Savonarola:
> religious/intellectual interlocutor, later spiritual influence, but do not retroactively treat Savonarola as the cause of every change in Pico's thought.
> Pico ↔ Gianfrancesco:
> nephew, posthumous editor/interpreter, biographer, transmitter and reshaper of Pico's reputation. This is especially important because Gianfrancesco's editorial decisions constitute evidence about reception rather than direct evidence of Giovanni's intentions.
> DATABASE DESIGN
> First inspect the existing schema and determine whether entities, people, works, passages, propositions, citations, concepts, and relationships already exist.
> Extend existing structures wherever possible.
> At minimum, the system needs concepts equivalent to:
> PERSON
> WORK
> TEXT_SECTION
> PROPOSITION
> RELATIONSHIP
> RELATIONSHIP_EVIDENCE
> SOURCE
> INTELLECTUAL_TRADITION
> CONCEPT
> EVENT
> INSTITUTION
> If equivalent entities already exist, reuse them rather than creating duplicates.
> PERSON METADATA
> Expand person records to support:
>
> * canonical_name
> * alternate_names
> * Latin_name
> * Italian_name
> * Hebrew/Arabic name where relevant
> * birth_year
> * death_year
> * locations
> * institutions
> * occupations/roles
> * intellectual traditions
> * languages
> * relevant bibliography
> * authority identifiers where available
> * notes
> * evidence status
>
> Examples should include, at minimum:
> Marsilio Ficino
> Angelo Poliziano
> Ermolao Barbaro
> Elia del Medigo / Elijah of Candia
> Nicoletto Vernia
> Agostino Nifo
> Girolamo Benivieni
> Battista Guarini
> Flavius Mithridates
> Yohanan Alemanno
> Lorenzo de' Medici
> Giovanni Nesi
> Roberto Salviati
> Savonarola
> Gianfrancesco Pico
> Jean Cordier
> Jean Monissart
> Pedro Garcia
> Marco de Miroldo
> Gioacchino da Vinci
> Antonio Flores
> Luca Borsiani da Foligno
> Francesco da Murcia
> Battista Signori da Genova
> Cristoforo da Castronuovo
> Bonfrancesco Arlotti
> Giorgio da Costa
> Giovanni de Myrle
> Girolamo Donato
> Girolamo Ramusio
> Antonio Cittadini
> Paolo Cortesi
> Do not assume this is exhaustive. Search the existing corpus and metadata for additional Pico associates and opponents and add them when supported by evidence.
> RELATIONSHIP MODEL
> Create a normalized relationship table or equivalent graph structure.
> Each relationship should support fields equivalent to:
> person_a_id
> person_b_id
> relationship_type
> relationship_subtype
> start_date
> end_date
> location
> directionality
> description
> confidence
> evidence_status
> source_id
> source_passage_id
> created_by
> notes
> Critically, distinguish:
> DIRECT_DOCUMENTARY
> STRONG_INFERENCE
> PROBABLE
> POSSIBLE
> UNCERTAIN
> Do not collapse these into one generic confidence score.
> A relationship should be able to have multiple pieces of evidence.
> For example:
> Pico → Ficino
> relationship_type = correspondence
> evidence = Ficino letter X
> Pico → Ficino
> relationship_type = philosophical_disagreement
> evidence = De ente et uno / Ficino response
> These are separate relationships even though they concern the same two people.
> TEXT/PASSAGE MODEL
> The database must permit a relationship to be connected to a precise passage rather than only to an entire work.
> For every Pico text, support:
> WORK
> ↓
> SECTION
> ↓
> PASSAGE
> ↓
> PROPOSITION / CLAIM
> This should work for:
>
> * 900 Conclusions
> * Oratio / De hominis dignitate
> * Apologia
> * Heptaplus
> * Commento
> * De ente et uno
> * Disputationes adversus astrologiam divinatricem
> * letters
> * poems
> * other works present in the corpus
>
> For the 900 Conclusions, each thesis must remain individually addressable.
> Do NOT treat the 900 Conclusions merely as one document.
> THESIS-RELATIONSHIP METADATA
> Every individual thesis should be able to have explicit links to:
>
> * people
> * works
> * philosophical traditions
> * schools
> * concepts
> * cited authorities
> * sources
> * opponents
> * possible intellectual antecedents
> * later commentators
>
> Create something equivalent to:
> THESIS_PERSON_RELATIONSHIP
> with:
> thesis_id
> person_id
> relation_type
> relation_direction
> relevance
> evidence_level
> confidence
> source_id
> source_passage_id
> notes
> relation_type should distinguish things such as:
> DIRECTLY_CITES
> QUOTES
> PARAPHRASES
> ARGUES_AGAINST
> DEFENDS
> USES_ARGUMENT_FROM
> USES_TERMINOLOGY_FROM
> RESPONDS_TO
> CONTRASTS_WITH
> AGREES_WITH
> POSSIBLE_INFLUENCE
> DOCUMENTED_INFLUENCE
> HISTORICAL_CONTEXT
> LATER_INTERPRETER
> Do NOT infer "influence" merely because two people discussed the same subject.
> THE 900 CONCLUSIONS SCORING SYSTEM
> Audit the existing scoring algorithm before changing it.
> The existing score should be extended so that a thesis can be evaluated in the context of Pico's intellectual network.
> Do NOT simply add points for every associated person.
> That would systematically reward heavily documented theses and distort the scholarship.
> Instead, create separate dimensions.
> For example:
>
> 1. TEXTUAL CENTRALITY
> How central is the proposition to Pico's argument?
> 2. SOURCE RELATION
> How strongly is the proposition textually connected to another author's work?
> 3. INTELLECTUAL NETWORK RELEVANCE
> How strongly does the proposition intersect with a documented intellectual relationship?
> 4. CONTROVERSY
> Was this proposition involved in an identifiable philosophical/theological disagreement?
> 5. HISTORICAL SIGNIFICANCE
> Did this proposition play a role in the 1487 investigation or later reception?
> 6. EVIDENCE QUALITY
> How strong is the documentary evidence connecting the proposition to the person/work?
> 7. TRADITIONAL SIGNIFICANCE
> Does it connect Aristotelianism, Platonism, Kabbalah, Hermeticism, scholastic theology, astrology, etc.?
> 8. RECEPTION
> How important was the proposition to later interpreters?
>
> The final score should retain these dimensions separately.
> For example:
> score_textual_centrality
> score_source_relation
> score_network_relevance
> score_controversy
> score_historical_significance
> score_evidence_quality
> score_reception
> score_total
> Do not hide the scholarly reasoning inside one opaque number.
> The UI should be able to say something like:
> "High network relevance because this proposition directly engages a question associated with Ficino, but documentary evidence for direct influence is moderate."
> rather than:
> "Ficino influence: +8."
> EVIDENCE WEIGHTING
> Build explicit evidence levels.
> Suggested hierarchy:
> 5 = direct primary-source evidence
> 4 = strong documentary evidence from contemporary/near-contemporary material
> 3 = strong scholarly inference
> 2 = plausible scholarly inference
> 1 = speculative association
> 0 = unsupported
> But store the underlying evidence rather than relying solely on this number.
> For every scored relationship, preserve:
> WHO made the claim
> WHAT source supports it
> WHICH passage supports it
> WHETHER the relationship is explicit or inferred
> WHAT the scholar actually argues
> This is essential because different historians may disagree about Pico's intellectual influences.
> SOURCE PROVENANCE
> Every scholarly claim imported into the database needs provenance.
> Support:
> source_author
> source_title
> publication_year
> edition
> page
> chapter
> passage
> URL/DOI where available
> citation
> claim_type
> claim_text
> interpretation
> evidence_level
> The system should distinguish:
> PRIMARY_SOURCE
> SCHOLARLY_ARGUMENT
> EDITORIAL_METADATA
> DATABASE_INFERENCE
> Do not turn a modern scholar's interpretation into an unqualified historical fact.
> Example:
> A scholar may argue that Pico's work with Alemanno influenced a particular Kabbalistic thesis.
> Store:
> claim = "Scholar X argues that Alemanno influenced..."
> rather than:
> claim = "Alemanno influenced Pico."
> The latter should only exist where the documentary evidence warrants it.
> RELATIONSHIP → THESIS SCORING
> Create a transparent derivation layer.
> Something equivalent to:
> thesis_relationship_evidence
> should record exactly why a person/relationship affects a thesis's metadata.
> Example:
> Thesis 229
> Person: Ficino
> Relationship: philosophical_disagreement
> Evidence: Pico, De ente et uno
> Evidence level: 5
> Network relevance: high
> Scoring contribution: controversy/context, not "influence"
> Another:
> Thesis X
> Person: Elia del Medigo
> Relationship: intellectual_source
> Evidence: Pico's use of Averroist terminology plus documentary evidence of their collaboration
> Evidence level: 4
> Network relevance: high
> Scoring contribution: source relation + network context
> Another:
> Thesis X
> Person: Yohanan Alemanno
> Relationship: possible intellectual influence
> Evidence level: 2
> Scoring contribution: low and explicitly marked speculative
> The system must prevent the same evidence from being counted multiple times through overlapping relationship types.
> Avoid double-counting.
> TEXT-SPECIFIC RELATIONSHIPS
> Do not assume that a relationship has the same relevance to every work.
> For example:
> Ficino should have high relevance to:
>
> * Commento
> * De ente et uno
> * some Oration material
> * some astrological material
>
> Del Medigo should have high relevance to:
>
> * Aristotelian Conclusions
> * Kabbalistic material
> * Hebrew-related material
>
> Mithridates should have especially high relevance to:
>
> * Kabbalistic Conclusions
> * Hebrew/Chaldean textual material
>
> Savonarola should have high relevance to:
>
> * later theologica
> </pasted_content id="e894">

### P20260926042421  (2026-09-26 04:24, session a08fd9b0)

> <pasted_content id="e894">
> The Pico material in your library is unusually good for reconstructing an intellectual network because it includes Copenhaver’s *Pico della Mirandola on Trial* and *Magic and the Dignity of Man*, Sophia Howlett’s *Re-evaluating Pico*, and Amos Edelheit’s *Ficino, Pico and Savonarola*. Those let us distinguish actual correspondence and personal contact from people Pico merely read.
>
> I would divide the network into four overlapping groups: people who taught or directly influenced Pico; correspondents and collaborators; people with whom he conducted identifiable philosophical arguments; and the opponents who confronted him over the *900 Conclusions*. The last group is especially important because “philosophical quarrel” in Pico's case often means a written or institutional dispute rather than a personal feud.
>
> ### 1. Marsilio Ficino (1433–1499)
>
> Ficino is probably the single most important relationship for understanding Pico's intellectual development, but it was considerably more contentious than the old picture of “Pico as Ficino's disciple” suggests.
>
> Pico encountered Ficino's Platonism in Florence and subsequently corresponded with him extensively. Ficino's letters show a genuine friendship: he helped Pico during the crisis surrounding the *900 Conclusions*, communicated Lorenzo de' Medici's support, discussed astrology and philosophy with him, and received drafts of Pico's writings. Copenhaver's discussion of Ficino's correspondence is particularly useful because it allows you to compare Ficino's contemporary letters with the much more pious portrait constructed by Pico's nephew Gianfrancesco after Pico's death.
>
> But there was a substantial philosophical contest underneath the friendship. Pico's *Commentary on a Song of Benivieni* was partly constructed as a critique of Ficino's *Commentary on Plato's Symposium* (*De amore*). Howlett describes this quite explicitly as a “strike against Ficino”: Pico was positioning himself as an alternative authority on Platonism and, particularly, on Plotinus.
>
> The disagreement continued in *De ente et uno*, where Pico challenged Ficino's Neoplatonic distinction between Being and the One. The disagreement was serious enough to be philosophically consequential but not a personal rupture; Ficino responded politely, and their correspondence remained warm. ([Stanford Encyclopedia of Philosophy][1])
>
> There is an especially interesting historiographical problem here: Gianfrancesco omitted Pico's early *Commentary* from his 1496 collected works and later presented his uncle as having rejected it. Howlett and Copenhaver both treat that as evidence that the posthumous construction of “Pico the Christian saint” obscures some of the intellectual tensions of the earlier Pico.
>
> For your purposes, I would put **Ficino at the center of the network**, but not simply as “teacher.” He is simultaneously mentor, friend, intellectual competitor, correspondent, and foil.
>
> Best library resources: Copenhaver, *Magic and the Dignity of Man*; Howlett, *Re-evaluating Pico*; Edelheit, *Ficino, Pico and Savonarola*.
>
> ### 2. Angelo Poliziano (1454–1494)
>
> Poliziano was one of Pico's closest Florentine intellectual friends and an important bridge between his early literary ambitions and mature philosophical interests.
>
> Pico knew him from the Florentine humanist environment and corresponded with him about poetry. Howlett reports that Pico asked Poliziano to critique his poetry and received an unfavorable assessment; Pico subsequently destroyed some of his poetic work and increasingly turned toward philosophy, although he continued writing poetry.
>
> The relationship is important because Poliziano represents a very different intellectual method from Pico's: philology, textual criticism, Greek scholarship, and humanist literary culture. Pico's later philosophical project nevertheless depended heavily on precisely the philological skills Poliziano represented.
>
> Their connection also appears indirectly through Ficino's correspondence. Messages routinely passed among Pico, Poliziano and Ficino, while Ficino's correspondents asked him to commend them to Pico and Poliziano.
>
> Poliziano therefore belongs in the category of **friend, correspondent, early critic and intellectual interlocutor**, rather than philosophical adversary.
>
> ### 3. Ermolao Barbaro (1454–1493)
>
> Barbaro is indispensable because he participated in one of Pico's earliest explicit philosophical controversies.
>
> Pico's famous 1485 letter to Barbaro responds to Barbaro's criticism of the barbarous Latin of scholastic philosophers. Pico's response is a defense of philosophical substance against purely humanist stylistic standards. Copenhaver emphasizes that Barbaro was himself a major Aristotelian scholar, Hellenist and philologist who had studied and taught at Padua.
>
> This is therefore more than an exchange about literary taste. It concerns the fundamental question: **what kind of language is appropriate to philosophy?** Pico argues that technical philosophical language should not be rejected merely because it is not elegant Ciceronian Latin.
>
> There is a delicious irony here. Barbaro's criticism pushed Pico to defend the very scholastic philosophers whose terminology Pico would later employ extensively in the *Conclusions* and *Apology*.
>
> The letter is one of the best primary documents for seeing Pico negotiating between **humanism and scholasticism**, rather than simply choosing one against the other.
>
> Library resources: Copenhaver, *Pico on Trial*, especially the discussion surrounding the Barbaro correspondence; Howlett's discussion of Pico's Padua education.
>
> ### 4. Elia del Medigo / Elijah of Candia (c. 1458–1493)
>
> Del Medigo is one of the most consequential figures in Pico's education and especially important if you're interested in Pico's Jewish, Arabic and Averroist intellectual sources.
>
> Pico encountered him in Padua, where Del Medigo taught privately. He introduced Pico to Averroes and the Jewish transmission of Averroist Aristotelianism and was also involved in Pico's study of Hebrew and Kabbalah. Howlett characterizes Del Medigo as one of the three major scholars involved in Pico's Kabbalistic project, alongside Flavius Mithridates and Yohanan Alemanno.
>
> There is an important qualification: **Del Medigo himself was not a Kabbalist in the way Pico became one.** His importance is partly that he provided Pico with access to Jewish intellectual traditions while maintaining a substantially Aristotelian/Averroist orientation.
>
> This makes him particularly useful for understanding the transformation of Pico's intellectual project: Pico did not simply encounter “Kabbalah” as an isolated occult tradition. He encountered it within a network of Jewish, Aristotelian, Arabic and Hebrew scholarship.
>
> There is also a major scholarly resource in your library: Edward Mahoney's essay, *Giovanni Pico della Mirandola and Elia del Medigo, Nicoletto Vernia and Agostino Nifo*. Copenhaver's bibliography specifically identifies it.
>
> ### 5. Nicoletto Vernia (c. 1420–1499)
>
> Vernia was one of Pico's principal Paduan Aristotelian connections.
>
> Pico studied at Padua during 1480–82, when the university was an important center of Aristotelianism and Averroism. Howlett identifies Vernia as one of the leading Paduan Aristotelians whom Pico encountered and worked with.
>
> Vernia represents the **scholastic Aristotelian side of Pico's education**, and his importance becomes clearer when juxtaposed with Ficino. Pico did not move straightforwardly from “medieval Aristotelianism” to “Renaissance Platonism.” He carried the technical apparatus of scholastic Aristotelianism into his later attempts at concordance.
>
> Mahoney's article mentioned above is probably the best resource in your library for pursuing the Pico–Vernia relationship.
>
> ### 6. Agostino Nifo (c. 1473–1538)
>
> Nifo was another important Paduan Aristotelian whom Pico encountered in the same intellectual environment as Vernia and Del Medigo.
>
> His significance is somewhat different from that of Del Medigo: he represents the developing Renaissance Aristotelianism that Pico was encountering at precisely the moment when he was beginning to experiment with the relationship between Aristotle and Plato.
>
> Again, Mahoney's essay is the obvious place to pursue the connection.
>
> ### 7. Girolamo Donato
>
> Donato belonged to Pico's Paduan circle and was involved in philosophical and literary studies with him. Howlett identifies him among the students and intellectual companions associated with Vernia's circle.
>
> He is not as important as Vernia, Nifo or Del Medigo, but he matters for reconstructing Pico's **actual social environment at Padua**, rather than reducing his education to a list of famous masters.
>
> ### 8. Girolamo Ramusio
>
> Ramusio was another Paduan companion and later became an important Orientalist. Howlett specifically notes that Ramusio studied Arabic and translated Arabic texts, making him a particularly interesting parallel to Pico's later interest in Arabic and Hebrew materials.
>
> This is one of those relationships where the importance lies less in a famous philosophical controversy than in reconstructing the **knowledge network** through which Pico encountered languages, texts and traditions.
>
> ### 9. Battista Guarini (1435–1503)
>
> Guarini belonged to Pico's Ferrara education. Howlett describes him as Pico's teacher in rhetoric and humanities and subsequently a close friend.
>
> Guarini is important for the literary and rhetorical side of Pico's formation, before the more conspicuous Aristotelian/Platonic conflicts of his mature career.
>
> ### 10. Girolamo Benivieni (1453–1542)
>
> Benivieni was both friend and collaborator.
>
> He was an early Ficinian Platonist and worked with Pico on the poetic-philosophical project that became the *Commentary on the Song of Benivieni*. He also attempted Hebrew study with Flavius Mithridates while staying with Pico. Later both men became closely associated with Savonarola.
>
> Benivieni is especially important because his poetry became the **test case through which Pico challenged Ficino's interpretation of Platonic love**. Pico wanted Benivieni to modify the poem so that Pico could construct a different, more Plotinian interpretation.
>
> So Benivieni is simultaneously friend, literary collaborator, student of Kabbalah/Hebrew, and an unwitting participant in Pico's intellectual contest with Ficino.
>
> ### 11. Girolamo Savonarola (1452–1498)
>
> Savonarola is probably Pico's most consequential late-life relationship after Ficino.
>
> Their relationship was intellectual as well as religious. Edelheit's research in your library preserves evidence for an actual philosophical discussion between Pico and Savonarola concerning the relationship between **ancient pagan theology and Christianity**, reportedly held in the Marciana academy at San Marco.
>
> That is significant because it complicates the common narrative in which Savonarola simply “converted” Pico from Renaissance magic to Christian piety.
>
> The relationship appears to have developed over time. Pico increasingly moved toward Savonarola's religious circle, while Ficino remained more distant. Copenhaver emphasizes that Benivieni attended Savonarola's sermons with Pico by around 1490, while other members of the Ficinian circle were also moving toward Savonarola in different ways.
>
> Savonarola's posthumous account of Pico is another source that has to be treated critically: it became one of the building blocks for Gianfrancesco's presentation of Pico as a penitential Christian. That later hagiographical construction should not simply be projected backward onto Pico's entire intellectual career.
>
> ### 12. Flavius Mithridates
>
> Mithridates was perhaps the most important technical intermediary between Pico and Hebrew/Kabbalistic materials.
>
> He was a Jewish convert to Christianity, linguist and translator. Pico employed him to teach Hebrew and Aramaic/Chaldean and to translate Kabbalistic texts. Howlett stresses that Mithridates was not simply a dubious translator or colorful eccentric, as older scholarship sometimes portrayed him; recent study has substantially rehabilitated his scholarly importance.
>
> The relationship was not always amicable. Mithridates left sarcastic marginal comments about Pico's scholarship and abilities, and by 1489 he had been arrested in Viterbo with books belonging to Pico.
>
> This makes him particularly interesting for your project because he shows Pico's intellectual network functioning almost like a **research laboratory**: Pico supplied patronage and direction while specialists supplied languages, manuscripts, translations and interpretation.
>
> ### 13. Yohanan Alemanno
>
> Alemanno was a Jewish scholar who worked with Pico in Florence and continued his Hebrew studies. The evidence for the relationship is unusually interesting because it is partly **Alemanno's own testimony**, rather than Pico's.
>
> Howlett notes that Alemanno claimed that his *Commentary on the Song of Songs* was written at Pico's suggestion. He was also a Kabbalist whose work combined Kabbalah, magic, astrology, Aristotelianism and the *prisca theologia*.
>
> Fanger's *Invoking Angels* is also in your library and discusses Alemanno's relationship with Pico and the Jewish intellectual milieu of Renaissance Italy.
>
> For your interests, this is one of the relationships I would investigate particularly deeply. Alemanno helps demonstrate that Pico's Kabbalah was embedded in **living Jewish intellectual networks**, rather than being merely a Christian appropriation of mysterious ancient texts.
>
> ### 14. Lorenzo de' Medici (1449–1492)
>
> Lorenzo was patron, political protector, literary correspondent and member of Pico's intellectual network rather than a philosophical teacher in the strict sense.
>
> Pico wrote him a famous 1484 letter about poetry. Later Lorenzo played a crucial political role during the aftermath of the Roman affair, interceding with the pope and helping Pico return to Florence. ([Stanford Encyclopedia of Philosophy][2])
>
> Copenhaver's work also shows how Pico's relationship with Lorenzo intersected with Ficino, Poliziano and the broader Florentine intellectual network. Ficino could use Lorenzo's patronage to facilitate Pico's return to Florence, while Lorenzo's political position was essential to protecting him after the condemnation of the *Conclusions*.
>
> So Lorenzo belongs in the category of **patron-protector and intellectual network hub**.
>
> ### 15. Gianfrancesco Pico della Mirandola (1469–1533)
>
> This is an unusual case because Gianfrancesco was Pico's nephew but also became his **posthumous editor and intellectual interpreter**.
>
> Gianfrancesco published the 1496 edition of Giovanni's works and wrote the *Vita*. The library's recent Stanford Encyclopedia material on Gianfrancesco is useful here because it stresses both the personal closeness and theoretical differences between the two men. ([Stanford Encyclopedia of Philosophy][3])
>
> Gianfrancesco emphasized the Christian and anti-philosophical dimensions of Giovanni's thought and suppressed or reframed material that complicated that image. Copenhaver argues that his editorial decisions helped transform Giovanni from an ambitious philosopher experimenting with Kabbalah, magic and philosophical concord into a penitential Christian saint.
>
> So he belongs in your list, but with a special label: **he is both a primary witness and an active constructor of the posthumous Pico tradition.**
>
> ### 16. Giovanni Nesi (1456–1502)
>
> Nesi belonged to the Ficinian circle and later became involved with Savonarolan prophecy.
>
> Copenhaver's account is particularly interesting: Nesi's *Oraculum de novo saeculo* incorporated the Platonic “ancient theology” into a Savonarolan prophetic framework, with the dead Pico himself appearing within the visionary narrative.
>
> He is therefore more useful for studying **Pico's reception among his immediate intellectual descendants** than for reconstructing a direct philosophical debate with Pico.
>
> ### 17. Roberto Salviati
>
> Salviati was another member of the Ficinian/Pico network who moved toward Savonarola, eventually taking Dominican vows in 1492. Copenhaver identifies him explicitly as a friend of both Pico and Ficino.
>
> Again, the value here is network reconstruction: Salviati demonstrates that Pico's circle was not divided cleanly into “Ficinian Platonists” versus “Savonarolans.” People moved between those intellectual and religious communities.
>
> ### 18. Jacopo Antiquari and Bernardo Michelozzi
>
> These are minor but genuine network figures.
>
> Howlett reports that Antiquari and Michelozzi sent greetings through Ficino and asked to be commended to Pico and Poliziano.
>
> They therefore belong on a comprehensive correspondence/network list, although not among the central philosophical relationships.
>
> ### 19. Jean Cordier
>
> Cordier is particularly important because he creates a fascinating link between Pico's Parisian intellectual formation and his later Roman trial.
>
> He was a Parisian theologian and member of the papal commission examining Pico's *Conclusions*. Unlike several of his colleagues, Cordier defended the theses under consideration and refused to sign the final condemnation. Edelheit records him as one of the commissioners who did not sign the final document.
>
> Thus Cordier was simultaneously part of **Pico's Parisian intellectual network and the institutional confrontation over the *Conclusions*.**
>
> ### 20. Jean Monissart, Bishop of Tournai
>
> Monissart chaired the formal theological commission examining the thirteen propositions that had been selected from the *900 Conclusions*. Howlett identifies him as the commission's presiding figure.
>
> He is less interesting as an intellectual influence on Pico than as a participant in the institutional dispute that turned Pico's proposed philosophical conference into a heresy investigation.
>
> ### 21. Pedro Garcia, Bishop of Ussel
>
> Garcia is the most important identifiable intellectual opponent in the Roman affair.
>
> He was a Thomist theologian and member of the commission that examined Pico's theses. Copenhaver emphasizes that Garcia subsequently published *Determinationes magistrales contra conclusiones apologeticas Joannis Pici* in 1489, a substantial response to Pico's *Apology*.
>
> This gives you an unusually valuable pair of primary texts: **Pico's *Apology* and Garcia's *Determinationes***.
>
> The dispute is especially important for the history of magic. Yates discusses Garcia's rejection of Pico's claim concerning the relationship between magic, Kabbalah and knowledge of Christ's divinity. Garcia's response became an important statement of late-fifteenth-century theological opposition to magical and astrological practices.
>
> If you want to understand “Pico versus the theologians,” Garcia is the person to start with.
>
> ### 22. Marco de Miroldo
>
> Miroldo, a Dominican and Master of the Sacred Palace, was another member of the commission. His position was considerably more hostile to Pico than Cordier's.
>
> Interestingly, he did not participate fully in the final proceedings because he reported illness. Edelheit's reconstruction emphasizes that the commission itself was internally divided rather than being a monolithic body of “the Church” opposing Pico.
>
> That is an important historiographical corrective.
>
> ### 23. Gioacchino da Vinci
>
> Da Vinci was the head of the Dominican order and another member of the commission examining Pico. Edelheit lists him among the experts involved in the investigation.
>
> He is much less important as a personal interlocutor than Garcia or Cordier, but belongs on a comprehensive list of Pico's institutional opponents.
>
> ### 24. Antonio Flores
>
> Flores was a legal expert on the commission. He represents the juridical side of the investigation rather than a sustained philosophical relationship with Pico.
>
> ### 25. Luca Borsiani da Foligno
>
> Borsiani was papal confessor and another member of the commission. Again, this is institutional rather than personal intellectual contact.
>
> ### 26. Francesco da Murcia
>
> Another papal-court theologian involved in the commission. His importance lies in reconstructing the institutional mechanism through which the *Conclusions* were examined.
>
> ### 27. Battista Signori da Genova
>
> Signori represented the Augustinian side of the commission. His presence is useful because it demonstrates that the investigation was not simply a Dominican/Thomist attack on Pico. The commission included representatives of several religious orders and institutional constituencies.
>
> ### 28. Cristoforo da Castronuovo
>
> A professor of theology and another member of the commission. Like several of the preceding figures, he is important primarily for reconstructing the collective theological response to Pico.
>
> ### 29. Bonfrancesco Arlotti and Giorgio da Costa
>
> These are especially interesting because they represent the **pro-Pico side of the Roman theological environment**.
>
> Edelheit notes that Arlotti, bishop of Reggio Emilia, and Cardinal Giorgio da Costa, bishop of Lisbon, were favorable toward Pico even though they were outside or peripheral to the commission.
>
> This reinforces the point that “the Church condemned Pico” is too crude a description of what happened. There was considerable disagreement among theologians and churchmen about the intellectual and theological status of his propositions.
>
> ### 30. Giovanni de Myrle
>
> Edelheit identifies Giovanni de Myrle among Roman theologians sympathetic to Pico, alongside Cordier.
>
> He is a comparatively obscure figure, but worth tracking if your goal is to reconstruct **Pico's actual support network during the trial**, rather than merely his famous friendships.
>
> ### 31. Antonio Cittadini
>
> Cittadini becomes particularly interesting after Pico's death. He was a professor at Pisa and later engaged Gianfrancesco over the interpretation of *De ente et uno* and the question of Platonic/Aristotelian concord. The SEP specifically notes that he was still arguing with Gianfrancesco about it two years after Giovanni's death. ([Stanford Encyclopedia of Philosophy][2])
>
> Thus Cittadini belongs more properly to **the posthumous continuation of a Pico controversy** than to Pico's direct circle.
>
> ### 32. Paolo Cortesi
>
> Cortesi was not a major direct interlocutor of Pico during his lifetime, but he became an important later defender of Pico against conservative theologians.
>
> Edelheit cites Cortesi's *Liber sententiarum* and *De cardinalatu* as part of the later rehabilitation of Pico's reputation.
>
> He belongs on the list if the purpose is intellectual reception, but I would keep him visually separate from Pico's actual contemporaneous relationships.
>
> ---
>
> ## The people Pico actually studied
>
> If we strip away the wider network and ask specifically “Who taught Pico?”, the evidence gives a fairly coherent progression:
>
> **Bologna:** canon law rather than philosophy; this period is less important for his mature intellectual identity.
>
> **Ferrara:** Battista Guarini and the humanist milieu including Ludovico Carbone, Niccolò Leoniceno, Rodolfo Agricola and others. Treccani's account identifies Pico's engagement with rhetoric, poetry, philosophy and theology there. ([Treccani][4])
>
> **Padua:** Nicoletto Vernia, Agostino Nifo, Elia del Medigo, Ermolao Barbaro, Manuel Adramitteno, and the wider circle of Paduan Aristotelianism. This is where the foundations of Pico's Aristotelianism, Averroism and linguistic studies were laid.
>
> **Pavia:** philosophy, rhetoric, Greek and possibly mathematics; the evidence is less specific about individual teachers.
>
> **Florence:** Marsilio Ficino and the Ficinian circle, especially Poliziano and Benivieni.
>
> **Hebrew/Kabbalah:** Del Medigo, Flavius Mithridates and Yohanan Alemanno.
>
> **Paris:** the scholastic environment of the Sorbonne and figures such as Jean Cordier; the documentary evidence for exactly which courses Pico attended is considerably weaker than for Padua. Howlett explicitly warns that the chronology and even the precise nature of Pico's Paris stay are difficult to establish.
>
> That last qualification matters. There is a tendency in older biographies to turn Pico's intellectual itinerary into a neat sequence of schools and masters. The newer scholarship in your library is much more cautious.
>
> ## The core philosophical quarrels
>
> If the purpose of this list is ultimately to understand **Pico's philosophical development through argument**, rather than simply assemble biographical names, I would organize the disputes into five major clusters.
>
> First is **Pico versus Barbaro: rhetoric versus scholastic philosophy**. This establishes the problem of philosophical language.
>
> Second is **Pico versus Ficino: what does Platonism actually mean?** The *Commentary on Benivieni*, *De ente et uno*, Plotinus, the nature of beauty, and eventually astrology all become points of disagreement. This is arguably the richest intellectual relationship in the whole network.
>
> Third is **Pico and the Paduan Aristotelians: Aristotle, Averroes and the possibility of concord**. Del Medigo, Vernia and Nifo supplied Pico with an Aristotelian intellectual infrastructure that he never simply abandoned.
>
> Fourth is **Pico and the Jewish intellectual network: Del Medigo, Mithridates and Alemanno**. Here the question becomes how Jewish philosophical and Kabbalistic materials could be incorporated into a Christian universal philosophy.
>
> Fifth is **Pico versus the Roman theologians: the *900 Conclusions*, 1486–87**. This is the confrontation involving Garcia, Monissart, Cordier, Miroldo, Da Vinci and the other commissioners. Copenhaver's *Pico on Trial* is by far the most useful item in your library for this episode. It also complicates the traditional story by showing that the commission itself was divided and that Pico's Parisian connections mattered.
>
> There is then a sixth, later transformation: **Pico versus astrology**, although this is somewhat anachronistic as a “quarrel” because the principal opponent is often a position rather than a single individual. It becomes particularly important when comparing Pico's earlier relationship with Ficino, whose writings on astrology and astral influence were considerably more accommodating, with Pico's unfinished *Disputationes adversus astrologiam divinatricem*.
>
> ## The most useful resources in your library
>
> For building a serious research dossier, I would prioritize the library roughly as follows.
>
> **Brian P. Copenhaver, *Pico della Mirandola on Trial: Heresy, Freedom, and Philosophy*.** This is the strongest source for the *900 Conclusions*, the *Apology*, Pico's scholastic sources, Garcia, the Roman commission and the relationship between Pico's philosophical method and the trial. The book's bibliography also points you toward Mahoney, Biondi, Farmer and the documentary literature.
>
> **Brian P. Copenhaver, *Magic and the Dignity of Man: Pico della Mirandola and His Oration in Modern Memory*.** This is particularly valuable for the correspondence, Ficino, Gianfrancesco's editorial construction of Pico, Savonarola, Kabbalah, and Pico's later reception. Its bibliography also gives you leads on Alemanno, Del Medigo and the scholarly literature surrounding them.
>
> **Sophia Howlett, *Re-evaluating Pico: Aristotelianism, Kabbalism, and Platonism in the Philosophy of Giovanni Pico della Mirandola*.** This is probably the best single resource in your library for reconstructing the **network** rather than simply the famous biography. It explicitly treats Pico's “academic-court” structure, his Paduan teachers, Florentine colleagues, Kabbalistic collaborators and philosophical disputes.
>
> **Amos Edelheit, *Ficino, Pico and Savonarola: The Evolution of Humanist Theology, 1461–1498*.** Essential for the triangular relationship among Ficino, Pico and Savonarola and for understanding the Roman controversy in its broader theological context. It also contains an unusually useful bibliography of primary and secondary literature.
>
> **Claire Fanger, *Invoking Angels*.** This becomes important when the inquiry shifts from Pico's philosophical network toward the Jewish, magical and theurgical networks surrounding Alemanno, Del Medigo and Renaissance occult practice.
>
> **Frances Yates, *Giordano Bruno and the Hermetic Tradition*.** This is historiographically older and should not be taken as the last word on Pico, but it is still useful for understanding the older “Pico → Hermetic magic → Bruno” narrative and particularly the history of scholarly interpretation of Pico's magical and Kabbalistic propositions.
>
> And outside the library, the Stanford Encyclopedia entry on Pico is useful as a compact orientation point, while Treccani is particularly useful for Italian biographical scholarship. ([Stanford Encyclopedia of Philosophy][2])
>
> The resulting picture is considerably richer than the conventional cast of **Pico–Ficino–Poliziano–Savonarola**. Pico's intellectual world was a dense network connecting Florentine humanism, Paduan Aristotelianism/Averroism, Parisian scholasticism, Jewish philosophy and Kabbalah, papal theology, and Savonarolan spirituality. The really interesting historical question is not which “school” Pico belonged to, but how he used people from **mutually incompatible intellectual communities** to construct his concordist project—and how those same people subsequently became evidence for competing versions of what Pico had actually been trying to do.
>
> [1]: https://plato.stanford.edu/archives/spr2012/entries/pico-della-mirandola/?utm_source=chatgpt.com "Giovanni Pico della Mirandola (Stanford Encyclopedia of Philosophy/Spring 2012 Edition)"
> [2]: https://plato.stanford.edu/entries/pico-della-mirandola/?utm_source=chatgpt.com "Giovanni Pico della Mirandola (Stanford Encyclopedia of Philosophy)"
> [3]: https://plato.stanford.edu/entries/gianfrancesco-pico/?utm_source=chatgpt.com "Giovanni Francesco [Gianfrancesco] Pico della Mirandola (Stanford Encyclopedia of Philosophy)"
> [4]: https://www.treccani.it/enciclopedia/pico-della-mirandola-filosofia-cabala-e-il-progetto-della-concordia-universalis_%28Storia-della-civilt%C3%A0-europea-a-cura-di-Umberto-Eco%29/?utm_source=chatgpt.com "Pico della Mirandola: filosofia, cabala e il progetto della concordia universalis - Enciclopedia - Treccani"
> </pasted_content id="e894">

<!-- END GENERATED PROMPTS -->
