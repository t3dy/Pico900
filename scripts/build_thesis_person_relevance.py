#!/usr/bin/env python3
"""
T-REL-02: Compute thesis x person relevance for all 900 theses.

Input:
  - data/network/persons.json (16 key persons)
  - data/ontology/mentions/by_thesis/*.json (mention harvest, 900 theses)
  - data/claims/angelology/*.claims.json (verified claims with bears_on party tags)

Output:
  - data/network/thesis_person_relevance.json
    One entry per thesis: {thesis_id, persons: [{person_id, relevance_score, mention_count, claim_count}]}

Scoring:
  - mention_count: # of times scholars mention this person when discussing this thesis
  - claim_count: # of verified claims bearing on this thesis that mention this person in bears_on
  - relevance_score: weighted combination (mention_count * 0.3 + claim_count * 0.7, normalized)
"""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict

def load_persons():
    """Load the 16 key persons from the network."""
    with open('data/network/persons.json') as f:
        persons = json.load(f)
    return {p['person_id']: p for p in persons}

def load_mentions_by_thesis():
    """Load all 900 thesis mention files and extract person references."""
    mentions_path = Path('data/ontology/mentions/by_thesis')
    thesis_persons = defaultdict(lambda: defaultdict(int))  # {thesis_id: {person_id: mention_count}}

    loaded = 0
    errors = 0

    for mention_file in sorted(mentions_path.glob('*.json')):
        try:
            # Try UTF-8 first, then fallback to latin-1
            try:
                with open(mention_file, encoding='utf-8') as f:
                    data = json.load(f)
            except UnicodeDecodeError:
                with open(mention_file, encoding='latin-1') as f:
                    data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"  Skipping {mention_file.name}: {e}", file=sys.stderr)
            errors += 1
            continue

        loaded += 1
        thesis_id = data.get('thesis_id', 'unknown')
        mentions = data.get('mentions', [])

        # For each mention, count references to known persons
        # Map scholar works to key persons based on who they primarily discuss
        scholar_person_map = {
            'copenhaver2019': ['ficino', 'delmedigo', 'mithridates', 'barbaro'],
            'copenhaver2022': ['ficino', 'delmedigo', 'mithridates', 'barbaro'],
            'howlett2021': ['ficino', 'delmedigo', 'mithridates', 'barbaro', 'poliziano'],
            'edelheit2022': ['ficino', 'savonarola', 'benivieni'],
            'edelheit2008': ['ficino', 'savonarola'],
            'wirszubski1989': ['alemanno', 'mithridates', 'delmedigo'],
            'allen2017-venus': ['ficino', 'poliziano'],
            'allen2017-other': ['ficino'],
            'black2006-a': ['ficino', 'delmedigo'],
            'black2006-b': ['ficino'],
            'black2006-c': ['ficino'],
            'wallis1965-deente': ['ficino', 'delmedigo'],
            'wallis1965-heptaplus': ['ficino'],
            'borghesi2012': ['ficino'],
            'dougherty2008': ['ficino', 'barbaro'],
        }

        for mention in mentions:
            work = mention.get('work')
            context = mention.get('context', '').lower() if mention.get('context') else ''

            # Count mentions for this scholar
            if work in scholar_person_map:
                for person_id in scholar_person_map[work]:
                    # Check if the person name appears in the context
                    person_names = {
                        'ficino': ['ficino'],
                        'delmedigo': ['del medigo', 'medigo', 'elijah'],
                        'mithridates': ['mithridates', 'flavius'],
                        'barbaro': ['barbaro'],
                        'alemanno': ['alemanno', 'yohanan'],
                        'poliziano': ['poliziano', 'politianus'],
                        'benivieni': ['benivieni'],
                        'savonarola': ['savonarola'],
                        'gianfrancesco-pico': ['gianfrancesco', 'g.f. pico'],
                        'lorenzo-de-medici': ['lorenzo', 'medici'],
                    }

                    if person_id in person_names:
                        if any(name in context for name in person_names[person_id]):
                            # Explicit mention of the person
                            thesis_persons[thesis_id][person_id] += 1
                        else:
                            # Scholar discusses this person even if not named
                            thesis_persons[thesis_id][person_id] += 0.3
                    else:
                        # Other persons: weaker association
                        thesis_persons[thesis_id][person_id] += 0.1

    print(f"  Loaded {loaded} mention files, {errors} errors", file=sys.stderr)
    return thesis_persons

def load_claims_by_thesis():
    """Load verified claims and extract person mentions via bears_on tags."""
    claims_persons = defaultdict(lambda: defaultdict(int))  # {thesis_id: {person_id: claim_count}}

    claims_path = Path('data/claims/angelology')
    if not claims_path.exists():
        print(f"Warning: {claims_path} not found", file=sys.stderr)
        return claims_persons

    loaded = 0
    for claims_file in sorted(claims_path.glob('*.claims.json')):
        try:
            # Try UTF-8 first, then fallback to latin-1
            try:
                with open(claims_file, encoding='utf-8') as f:
                    claims_data = json.load(f)
            except UnicodeDecodeError:
                with open(claims_file, encoding='latin-1') as f:
                    claims_data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Warning: skipping {claims_file.name}: {e}", file=sys.stderr)
            continue

        loaded += 1

        # Handle both array and object formats
        claims_list = claims_data if isinstance(claims_data, list) else claims_data.get('claims', [])

        for claim in claims_list:
            # Only count verified/supported claims
            verdict = claim.get('semantic_verdict', {})
            if verdict.get('verdict') == 'unsupported':
                continue

            # Get the thesis IDs this claim bears on
            applies_to = claim.get('applies_to', [])
            if isinstance(applies_to, str):
                applies_to = [applies_to]

            # Get the parties (persons) this claim bears on
            bears_on = claim.get('bears_on', [])
            if isinstance(bears_on, str):
                bears_on = [bears_on]

            # Map party slugs to person IDs
            party_to_person = {
                'ficino': 'ficino',
                'del-medigo': 'delmedigo',
                'mithridates': 'mithridates',
                'barbaro': 'barbaro',
                'alemanno': 'alemanno',
                'poliziano': 'poliziano',
                'benivieni': 'benivieni',
                'savonarola': 'savonarola',
                'gianfrancesco-pico': 'gianfrancesco-pico',
                'lorenzo-de-medici': 'lorenzo-de-medici',
            }

            for thesis_id in applies_to:
                for party in bears_on:
                    person_id = party_to_person.get(party, party)
                    claims_persons[thesis_id][person_id] += 1

    print(f"  Loaded {loaded} claims files", file=sys.stderr)
    return claims_persons

def compute_relevance_scores(mention_persons, claim_persons, persons):
    """Compute combined relevance scores for each thesis x person pair."""
    thesis_relevance = {}

    # Collect all thesis IDs
    all_theses = set(mention_persons.keys()) | set(claim_persons.keys())

    for thesis_id in sorted(all_theses):
        mention_counts = mention_persons.get(thesis_id, {})
        claim_counts = claim_persons.get(thesis_id, {})

        # Combine person mentions
        all_persons = set(mention_counts.keys()) | set(claim_counts.keys())

        person_scores = []
        for person_id in sorted(all_persons):
            mention_count = mention_counts.get(person_id, 0)
            claim_count = claim_counts.get(person_id, 0)

            # Weight: claims are more direct evidence than mentions
            # mention_count: 0.3 weight (scholar discusses the person)
            # claim_count: 0.7 weight (claim directly bears on the person)
            score = mention_count * 0.3 + claim_count * 0.7

            if score > 0:
                person_scores.append({
                    'person_id': person_id,
                    'relevance_score': round(score, 2),
                    'mention_count': round(mention_count, 1),
                    'claim_count': claim_count,
                })

        # Sort by relevance score descending
        person_scores.sort(key=lambda x: x['relevance_score'], reverse=True)

        if person_scores:
            thesis_relevance[thesis_id] = {
                'thesis_id': thesis_id,
                'persons': person_scores,
            }

    return thesis_relevance

def main():
    print("T-REL-02: Building thesis x person relevance...", file=sys.stderr)

    # Load data
    print("Loading persons...", file=sys.stderr)
    persons = load_persons()
    print(f"  Loaded {len(persons)} persons", file=sys.stderr)

    print("Loading mention harvest...", file=sys.stderr)
    mention_persons = load_mentions_by_thesis()
    print(f"  Found mentions for {len(mention_persons)} theses", file=sys.stderr)

    print("Loading claims layer...", file=sys.stderr)
    claim_persons = load_claims_by_thesis()
    print(f"  Found claims for {len(claim_persons)} theses", file=sys.stderr)

    # Compute scores
    print("Computing relevance scores...", file=sys.stderr)
    thesis_relevance = compute_relevance_scores(mention_persons, claim_persons, persons)
    print(f"  Scored {len(thesis_relevance)} theses", file=sys.stderr)

    # Write output
    output_path = 'data/network/thesis_person_relevance.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(thesis_relevance, f, indent=2, ensure_ascii=False)

    print(f"\nWrote {output_path}")
    print(f"Theses with person relevance: {len(thesis_relevance)} of 900")

    # Summary stats
    all_person_ids = set()
    for entry in thesis_relevance.values():
        for person in entry['persons']:
            all_person_ids.add(person['person_id'])

    print(f"Unique persons referenced: {len(all_person_ids)}")
    print("Top persons by total relevance:")
    person_totals = defaultdict(float)
    for entry in thesis_relevance.values():
        for person in entry['persons']:
            person_totals[person['person_id']] += person['relevance_score']

    for person_id, total in sorted(person_totals.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {person_id}: {total:.1f}")

if __name__ == '__main__':
    main()
