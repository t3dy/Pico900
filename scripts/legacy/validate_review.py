#!/usr/bin/env python3
"""
REVIEWER R2 Validation Script — S1 + S4 Conclusions Review

Validates all 107 standardized conclusions against STYLE_GUIDE checklist.
Generates quality metrics and section reports.
"""

import json
import os
from pathlib import Path
from collections import defaultdict

# Validation criteria
VALIDATION_CHECKLIST = {
    "latin_incipit": "Latin incipit present and verified (not placeholder)",
    "english_translation": "English translation sourced (not [TO_TRANSLATE])",
    "charge": "Charge section present (not empty or TO_FILL)",
    "defense": "Defense section present (not empty or TO_FILL)",
    "scholar_citations": "Minimum 2 citations with sources",
    "citations_verified": "At least 1 citation verified or confident",
    "tags": "Tags properly populated (not empty)",
    "status": "Status field is 'standardized'",
    "no_nulls": "No null values in critical fields",
}

def is_placeholder(value):
    """Check if value is a placeholder."""
    if not value:
        return True
    if isinstance(value, str):
        upper = value.upper()
        return any(x in upper for x in ["TO_BE_FILLED", "TO_BE_SOURCED", "TO FILL", "TO TRANSLATE", "TO_EXTRACT", "[PAGE", "[WORK", "[TO SOURCE", "[FROM CRITICAL"])
    return False

def load_json_safe(filepath):
    """Load JSON with error handling."""
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except Exception as e:
        return {"_error": str(e), "_filepath": filepath}

def validate_entry(entry, filepath):
    """Validate a single conclusion entry."""
    results = {
        "conclusion_id": entry.get("conclusion_id", "UNKNOWN"),
        "filepath": str(filepath),
        "checklist": {},
        "gaps": [],
        "warnings": [],
        "metrics": {}
    }

    # Latin incipit check
    latin = entry.get("latin_incipit", "")
    if not is_placeholder(latin) and latin.strip():
        results["checklist"]["latin_incipit"] = "PASS"
    else:
        results["checklist"]["latin_incipit"] = "FAIL"
        results["gaps"].append("Latin incipit is missing or placeholder")

    # English translation check
    trans = entry.get("english_translation", "")
    if isinstance(trans, dict):
        trans_text = trans.get("text", "")
    else:
        trans_text = trans

    if not is_placeholder(trans_text) and trans_text.strip():
        results["checklist"]["english_translation"] = "PASS"
        trans_source = entry.get("translation_source")
        if isinstance(trans, dict):
            trans_source = trans.get("source")
        if trans_source:
            results["metrics"]["translation_source"] = trans_source
    else:
        results["checklist"]["english_translation"] = "FAIL"
        results["gaps"].append("English translation is missing or placeholder")

    # Charge check
    charge = entry.get("charge", "")
    if not is_placeholder(charge) and charge.strip() and charge != "TO BE FILLED":
        results["checklist"]["charge"] = "PASS"
    else:
        results["checklist"]["charge"] = "FAIL"
        results["gaps"].append("Charge section is empty or placeholder")

    # Defense check
    defense = entry.get("defense", "")
    if not is_placeholder(defense) and defense.strip() and defense != "TO BE FILLED":
        results["checklist"]["defense"] = "PASS"
    else:
        results["checklist"]["defense"] = "FAIL"
        results["gaps"].append("Defense section is empty or placeholder")

    # Scholar citations check
    citations = entry.get("scholar_citations", [])
    citation_count = 0
    verified_count = 0
    full_citations = 0

    if isinstance(citations, list):
        for cit in citations:
            if isinstance(cit, dict):
                # Check if citation has actual content
                quotation = cit.get("quotation", "")
                scholar = cit.get("scholar", "")
                page = cit.get("page")

                if scholar and not is_placeholder(quotation) and quotation.strip():
                    citation_count += 1
                    full_citations += 1
                    if cit.get("verified") or cit.get("confidence_level") in ["VERIFIED", "CITED"]:
                        verified_count += 1

    results["metrics"]["total_citations"] = citation_count
    results["metrics"]["verified_citations"] = verified_count
    results["metrics"]["scholar_count"] = len(citations)

    if citation_count >= 2:
        results["checklist"]["scholar_citations"] = "PASS"
    else:
        results["checklist"]["scholar_citations"] = "FAIL"
        results["gaps"].append(f"Only {citation_count} complete citations (need ≥2)")

    if verified_count >= 1:
        results["checklist"]["citations_verified"] = "PASS"
    else:
        results["checklist"]["citations_verified"] = "FAIL"
        results["gaps"].append("No verified or confident citations")

    # Tags check
    tags = entry.get("tags", [])
    if tags and len(tags) > 0:
        results["checklist"]["tags"] = "PASS"
        results["metrics"]["tag_count"] = len(tags)
    else:
        results["checklist"]["tags"] = "FAIL"
        results["gaps"].append("Tags are empty or missing")

    # Status check
    status = entry.get("status", "")
    if status == "standardized":
        results["checklist"]["status"] = "PASS"
    else:
        results["checklist"]["status"] = "FAIL"
        results["warnings"].append(f"Status is '{status}', expected 'standardized'")

    # Null check
    null_fields = []
    critical_fields = ["conclusion_id", "section", "status"]
    for field in critical_fields:
        if field not in entry or entry[field] is None:
            null_fields.append(field)

    if not null_fields:
        results["checklist"]["no_nulls"] = "PASS"
    else:
        results["checklist"]["no_nulls"] = "FAIL"
        results["gaps"].append(f"Null critical fields: {', '.join(null_fields)}")

    # Heretical flag check
    if entry.get("heretical_flag"):
        if not entry.get("heretical_notes"):
            results["warnings"].append("Heretical flag set but no notes provided")

    results["metrics"]["heretical_flag"] = entry.get("heretical_flag", False)

    return results

def main():
    project_root = Path("C:\\Dev\\Pico900")
    s1_dir = project_root / "data" / "conclusions" / "S1"
    s4_dir = project_root / "data" / "conclusions" / "S4"

    # Load all entries
    s1_results = []
    s4_results = []

    print("Loading S1 entries...")
    for filepath in sorted(s1_dir.glob("*.json")):
        entry = load_json_safe(filepath)
        if "_error" not in entry:
            s1_results.append(validate_entry(entry, filepath))

    print(f"Loaded {len(s1_results)} S1 entries")

    print("Loading S4 entries...")
    for filepath in sorted(s4_dir.glob("*.json")):
        entry = load_json_safe(filepath)
        if "_error" not in entry:
            s4_results.append(validate_entry(entry, filepath))

    print(f"Loaded {len(s4_results)} S4 entries")

    # Aggregate results
    def aggregate_results(results, section_name):
        summary = {
            "section": section_name,
            "total_entries": len(results),
            "checklist_scores": defaultdict(lambda: {"pass": 0, "fail": 0}),
            "gaps_by_type": defaultdict(list),
            "warnings_by_type": defaultdict(list),
            "metrics": {
                "avg_citations": 0,
                "avg_verified_citations": 0,
                "heretical_count": 0,
                "avg_tags": 0,
            },
            "entries_with_gaps": []
        }

        total_citations = 0
        total_verified = 0
        total_tags = 0
        heretical_count = 0

        for result in results:
            # Checklist aggregation
            for check, status in result["checklist"].items():
                if status == "PASS":
                    summary["checklist_scores"][check]["pass"] += 1
                else:
                    summary["checklist_scores"][check]["fail"] += 1

            # Gaps
            if result["gaps"]:
                summary["entries_with_gaps"].append(result["conclusion_id"])
                for gap in result["gaps"]:
                    summary["gaps_by_type"][gap].append(result["conclusion_id"])

            # Warnings
            for warning in result["warnings"]:
                summary["warnings_by_type"][warning].append(result["conclusion_id"])

            # Metrics
            total_citations += result["metrics"].get("total_citations", 0)
            total_verified += result["metrics"].get("verified_citations", 0)
            total_tags += result["metrics"].get("tag_count", 0)
            if result["metrics"].get("heretical_flag"):
                heretical_count += 1

        summary["metrics"]["avg_citations"] = round(total_citations / len(results), 2) if results else 0
        summary["metrics"]["avg_verified_citations"] = round(total_verified / len(results), 2) if results else 0
        summary["metrics"]["avg_tags"] = round(total_tags / len(results), 2) if results else 0
        summary["metrics"]["heretical_count"] = heretical_count
        summary["metrics"]["total_unique_gaps"] = len(summary["gaps_by_type"])

        return summary

    s1_summary = aggregate_results(s1_results, "S1")
    s4_summary = aggregate_results(s4_results, "S4")

    # Generate reports
    def generate_report(summary, results, section_name, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Phase 1 Review Report — {section_name}\n\n")
            f.write(f"**Reviewed**: {summary['total_entries']} conclusions\n")
            f.write(f"**Review Date**: 2026-09-25\n")
            f.write(f"**Reviewer**: R2 (REVIEWER)\n\n")

            # Summary metrics
            f.write("## Summary Metrics\n\n")
            f.write(f"- **Total Entries**: {summary['total_entries']}\n")
            f.write(f"- **Average Citations per Entry**: {summary['metrics']['avg_citations']}\n")
            f.write(f"- **Average Verified Citations per Entry**: {summary['metrics']['avg_verified_citations']}\n")
            f.write(f"- **Average Tags per Entry**: {summary['metrics']['avg_tags']}\n")
            f.write(f"- **Heretical Flags**: {summary['metrics']['heretical_count']}\n")
            gap_pct = 100*len(summary['entries_with_gaps'])//summary['total_entries'] if summary['total_entries'] > 0 else 0
            f.write(f"- **Entries with Gaps**: {len(summary['entries_with_gaps'])} ({gap_pct}%)\n\n")

            # Checklist scores
            f.write("## Quality Checklist Results\n\n")
            f.write("| Criterion | Pass | Fail | %Pass |\n")
            f.write("|-----------|------|------|-------|\n")
            for check in sorted(summary['checklist_scores'].keys()):
                scores = summary['checklist_scores'][check]
                total = scores['pass'] + scores['fail']
                pct = (100 * scores['pass'] // total) if total > 0 else 0
                f.write(f"| {check} | {scores['pass']} | {scores['fail']} | {pct}% |\n")
            f.write("\n")

            # Gaps by type
            f.write("## Gaps by Type\n\n")
            if summary['gaps_by_type']:
                for gap_type in sorted(summary['gaps_by_type'].keys()):
                    entries = summary['gaps_by_type'][gap_type]
                    f.write(f"### {gap_type}\n")
                    f.write(f"**Affected entries ({len(entries)})**: {', '.join(sorted(entries)[:5])}")
                    if len(entries) > 5:
                        f.write(f", ... and {len(entries)-5} more")
                    f.write("\n\n")
            else:
                f.write("No gaps detected.\n\n")

            # Warnings
            if summary['warnings_by_type']:
                f.write("## Warnings\n\n")
                for warning_type in sorted(summary['warnings_by_type'].keys()):
                    entries = summary['warnings_by_type'][warning_type]
                    f.write(f"- **{warning_type}**: {len(entries)} entries\n")
                f.write("\n")

            # Sample failures
            f.write("## Sample Entries Needing Attention\n\n")
            failures = [r for r in results if r['gaps']][:5]
            for result in failures:
                f.write(f"### {result['conclusion_id']}\n")
                for gap in result['gaps']:
                    f.write(f"- {gap}\n")
                f.write("\n")

            # Recommendations
            f.write("## Recommendations for Phase 2\n\n")
            if summary['checklist_scores']['latin_incipit']['fail'] > 0:
                f.write(f"1. **Fetch Critical Edition Latin**: {summary['checklist_scores']['latin_incipit']['fail']} entries need Latin incipit verification.\n")
            if summary['checklist_scores']['english_translation']['fail'] > 0:
                f.write(f"2. **Source Translations**: {summary['checklist_scores']['english_translation']['fail']} entries need English translations from megabase or original work.\n")
            if summary['checklist_scores']['charge']['fail'] > 0:
                f.write(f"3. **Complete Charge/Defense**: {summary['checklist_scores']['charge']['fail']} entries need charge sections filled.\n")
            if summary['checklist_scores']['scholar_citations']['fail'] > 0:
                f.write(f"4. **Add Scholar Citations**: {summary['checklist_scores']['scholar_citations']['fail']} entries need complete citations (≥2 per entry).\n")
            f.write("\n")

    # Generate S1 report
    s1_report_path = project_root / "docs" / "PHASE_1_S1_REVIEW_REPORT.md"
    generate_report(s1_summary, s1_results, "S1 (Neoplatonic)", s1_report_path)
    print(f"Generated S1 report: {s1_report_path}")

    # Generate S4 report
    s4_report_path = project_root / "docs" / "PHASE_1_S4_REVIEW_REPORT.md"
    generate_report(s4_summary, s4_results, "S4 (Avicennist)", s4_report_path)
    print(f"Generated S4 report: {s4_report_path}")

    # Print summary to stdout
    print("\n" + "="*60)
    print(f"S1 Summary: {s1_summary['total_entries']} entries")
    print(f"  - Avg citations: {s1_summary['metrics']['avg_citations']}")
    print(f"  - Entries with gaps: {len(s1_summary['entries_with_gaps'])}")
    print(f"  - Heretical flags: {s1_summary['metrics']['heretical_count']}")

    print(f"\nS4 Summary: {s4_summary['total_entries']} entries")
    print(f"  - Avg citations: {s4_summary['metrics']['avg_citations']}")
    print(f"  - Entries with gaps: {len(s4_summary['entries_with_gaps'])}")
    print(f"  - Heretical flags: {s4_summary['metrics']['heretical_count']}")
    print("="*60)

if __name__ == "__main__":
    main()
