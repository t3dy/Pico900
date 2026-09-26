# Brief: LINKER for claim packets

You are a LINKER (`docs/ORCHESTRATION.md`). The packets hold verified claims from different scholars, each written in
isolation. You connect them: where two scholars say the same thing, where one gives evidence for another, where they
disagree, qualify or lean on each other. You own exactly one file: `data/claims/<domain>/links.json`. You write no claim,
no prose, and you edit no packet.

Read `docs/CLAIMS_MODEL.md` (sections 1, 4, 5, 6) first. Your links decide the centrality, corroboration and contestation
scores, so a careless link corrupts the ranking that decides what the edition foregrounds.

## Tools

```
python scripts/claims_query.py --topics                      topics with claim counts
python scripts/claims_query.py --topic TOPIC                 every verified claim on a topic: id | claimant | hedge | text
python scripts/claims_query.py --topic TOPIC --full          plus the quotations, warrants, open questions
python scripts/claims_query.py --id ID --full                one claim
python scripts/claims_query.py --text "Anaxagoras" --full    find claims by a word in the restatement or quotation
python scripts/claims_score.py                               (last) verifies your links and prints how many were rejected
```

## Method

Work topic by topic (all 19 in `data/claims/topics.json`; the sweep's proposed topics are in each packet's `proposed_topics`).
For each topic read the whole list, then group claims that concern the same point. Within a group compare **quotations,
not restatements**: restatements are paraphrases by a model and may hide a difference; the quotation is the evidence.

Relations (`relation`, direction from -> to):

- `same_claim`: two claimants (or two places) assert the same proposition. The quotations must say it in substance.
- `supports`: `from` offers evidence, a source or an argument that bears out `to`.
- `contradicts`: the quotations cannot both be right (a real disagreement, not a difference of topic or emphasis).
- `qualifies`: `from` narrows, hedges or adds a condition to `to`.
- `depends_on`: `from` presupposes `to` (a premise in the same scholar's argument, or one scholar building on another's finding).
- `cites`: `from` is a scholar reporting `to`, which is the claim (usually in another packet) about the same view.

Each link: `{"id": "L001", "from": "<claim id>", "to": "<claim id>", "relation": "...", "basis": "one sentence"}`. The
**basis states, from the quotations of the two claims, why the relation holds**, in your own words, using nothing you did
not read in the two claims. It must let a reader who has only these two cards see the relation. If the basis needs
outside knowledge, do not make the link.

Rules:
1. **Do not link what merely shares a topic.** Two claims on the Heptaplus are not related until you can say how.
2. **`contradicts` is expensive.** Use it only when the quotations conflict on the same question; when they differ in
   scope (Black on the second proem, Allen on the Commento), use `qualifies` or no link. A wrong `contradicts` invents a
   scholarly quarrel, which is the failure this project exists to prevent.
3. **Cross-scholar is the point.** Links inside one scholar's own argument are already in `relations_local`; add them only if
   the packet's owner missed a dependency that matters.
4. **A scholar reporting another scholar** is `cites`, to the claim (in another packet) that holds the reported view if you can find it.
5. **Directional care:** `supports` and `depends_on` are not symmetric; `same_claim` and `contradicts` are (list once).
6. Only verified claims exist for you; do not invent ids. `claims_score.py` rejects a link whose ends are missing,
   unverified, unknown-relation or basis-less.
7. Record each **open dispute** you find (two claimants, contradicting) in the `disputes` list of the file: topic, the two
   claim ids, one sentence on what the disagreement is about. This becomes the tour's "where scholars differ" material.

## Output

```json
{ "linker": "LINK-1", "date": "2026-09-26",
  "links": [ {"id": "L001", "from": "...", "to": "...", "relation": "same_claim", "basis": "..."} ],
  "disputes": [ {"topic": "three-worlds", "claims": ["a:1", "b:2"], "about": "one sentence"} ],
  "notes": "topics not yet linked and why" }
```

Write the file incrementally (a whole topic at a time) so an interruption loses nothing, and run `python scripts/claims_score.py`
at the end: it prints `links ok N rejected M`; fix every rejection. Report in under 150 words: links by relation, disputes
found, topics not covered, and any place where you suspect a claim overreaches (name the id; a verifier will look).
