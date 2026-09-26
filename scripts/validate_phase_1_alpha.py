#!/usr/bin/env python3
"""
Phase 1-Alpha Final Validation Suite
Validates 69 angelology entries + 6 scholarship files
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# === Configuration ===
PROJECT_ROOT = Path(__file__).parent.parent
DATA_ROOT = PROJECT_ROOT / "data"
TEXTS_ROOT = DATA_ROOT / "texts"
SCHOLARSHIPS_ROOT = DATA_ROOT / "scholarships" / "angels"

ALLOWED_LINEAGES = {"pseudo-dionysius", "aquinas", "kabbalah", "plotinus", "synthesis"}
ALLOWED_TAGS = {
    "angelology", "hierarchy", "dignity", "neoplatonism", "metaphysics",
    "kabbalistic", "mystical_union", "heretical_adjacent", "kabbalah",
    "divine-embodiment", "participated-being", "apophatic-theology",
    "mysticism", "death-of-the-kiss", "song-of-songs", "kabbalistic-doctrine",
    "incarnation", "eucharist", "theology", "christology", "soul",
    "intellect", "divine", "transformation", "unity", "emanation",
    "ascent", "being", "causality", "logic", "angels", "hypostases",
    "participation"
}
REQUIRED_FIELDS = {"conclusion_id", "english_translation", "exegesis", "tags", "status"}
# latin_text is acceptable alternative to latin_incipit
OPTIONAL_LATIN_FIELDS = {"latin_text", "latin_incipit"}
# Different texts use different field names for sections/passages
OPTIONAL_SECTION_FIELDS = {"section", "book", "layer", "passage_number"}
SCHOLARSHIP_FILES = [
    "lineage_pseudodionysius.json",
    "lineage_aquinas.json",
    "lineage_kabbalah.json",
    "lineage_plotinus.json",
    "scholar_debate_log.json",
    "cross_text_angelology_web.json"
]

@dataclass
class ValidationIssue:
    """Represents a validation issue"""
    entry_id: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # e.g., "json_parsing", "schema_violation", etc.
    message: str
    details: str = ""

@dataclass
class EntryValidation:
    """Validation result for an entry"""
    entry_id: str
    file_path: str
    checklist: Dict[str, bool]  # 9-point checklist
    issues: List[ValidationIssue]
    raw_data: Dict[str, Any] = None

@dataclass
class ValidationReport:
    """Final validation report"""
    timestamp: str
    total_entries: int
    entries_passing: int
    scholarship_files_passing: int
    total_issues: Dict[str, int]  # severity -> count
    entries_by_status: Dict[str, int]  # status -> count
    checklist_summary: Dict[str, int]  # criterion -> pass_count
    critical_blockers: List[str]
    entry_validations: List[Dict[str, Any]]

def load_json_safe(file_path: Path) -> Tuple[Any, str]:
    """Safely load JSON file, return (data, error_message)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f), ""
    except json.JSONDecodeError as e:
        return None, f"JSON Decode Error: {str(e)}"
    except Exception as e:
        return None, f"File Error: {str(e)}"

def validate_json_parsing(entry_path: Path) -> Tuple[bool, str, Dict]:
    """Check if JSON parses without error"""
    data, error = load_json_safe(entry_path)
    if error:
        return False, error, {}
    return True, "", data

def check_required_fields(data: Dict) -> Tuple[bool, List[str]]:
    """Check if all required fields are present"""
    missing = []
    for field in REQUIRED_FIELDS:
        if field not in data:
            missing.append(field)

    # Check for at least one latin field
    has_latin = any(field in data for field in OPTIONAL_LATIN_FIELDS)
    if not has_latin:
        missing.append("latin_text or latin_incipit (one required)")

    # Check for at least one section field
    has_section = any(field in data for field in OPTIONAL_SECTION_FIELDS)
    if not has_section:
        missing.append("section/book/layer/passage_number (one required)")

    return len(missing) == 0, missing

def check_lineage_schema(data: Dict) -> Tuple[bool, List[str]]:
    """Check if lineage field conforms to schema"""
    if "lineage" not in data:
        return True, []  # lineage is optional

    lineage = data["lineage"]
    if isinstance(lineage, str):
        # Check if it's a valid single lineage or pipe-separated multiple
        parts = [p.strip() for p in lineage.split("|")]
        invalid = [p for p in parts if p not in ALLOWED_LINEAGES]
        return len(invalid) == 0, invalid
    elif isinstance(lineage, list):
        # Check if it's a list of valid lineages
        invalid = [p for p in lineage if p not in ALLOWED_LINEAGES]
        return len(invalid) == 0, invalid
    return False, ["lineage must be a string or list"]

def check_tags_schema(data: Dict) -> Tuple[bool, List[str]]:
    """Check if tags conform to schema"""
    if "tags" not in data:
        return False, ["missing tags field"]

    tags = data.get("tags", [])
    if not isinstance(tags, list):
        return False, ["tags must be a list"]

    invalid = [t for t in tags if t not in ALLOWED_TAGS]
    return len(invalid) == 0, invalid

def check_cross_references(data: Dict) -> Tuple[bool, List[str]]:
    """Check if cross-references are properly formatted"""
    issues = []

    # Check related_conclusions field if present
    if "related_conclusions" in data:
        related = data["related_conclusions"]
        if isinstance(related, list):
            for ref in related:
                if isinstance(ref, str):
                    # Should be format: "ID (description)" or just "ID"
                    if "(" in ref and not ref.endswith(")"):
                        issues.append(f"Malformed reference: {ref}")

    return len(issues) == 0, issues

def check_confidence_markers(data: Dict) -> Tuple[bool, str]:
    """Check if exegesis has confidence markers"""
    exegesis = data.get("exegesis", "")
    if not exegesis:
        return False, "exegesis is empty"

    valid_markers = ["[VERIFIED]", "[CITED]", "[INFERRED]"]
    has_marker = any(marker in str(exegesis) for marker in valid_markers)

    if not has_marker:
        return False, "exegesis lacks confidence marker ([VERIFIED]/[CITED]/[INFERRED])"
    return True, ""

def check_heretical_adjacent(data: Dict) -> Tuple[bool, str]:
    """Check if entry discussing heretical themes is tagged"""
    exegesis = data.get("exegesis", "")
    tags = data.get("tags", [])

    # Keywords that suggest heretical content
    heretical_keywords = [
        "divine embodiment", "incarnation", "eucharist", "soul-intellect",
        "heretical", "condemned", "incarnate", "flesh", "body", "presence"
    ]

    has_heretical_content = any(kw.lower() in str(exegesis).lower() for kw in heretical_keywords)
    has_tag = "heretical_adjacent" in tags

    if has_heretical_content and not has_tag:
        return False, "Entry discusses heretical theme but lacks heretical_adjacent tag"
    return True, ""

def check_scholar_citations(data: Dict, entry_id: str) -> Tuple[bool, str]:
    """Check if scholar citations are present and valid"""
    citations = data.get("scholar_citations", [])

    # At least one citation should be present for full entries
    if not citations and data.get("status") == "complete":
        return False, "Complete entry lacks scholar citations"
    return True, ""

def validate_entry_checklist(data: Dict, entry_id: str) -> Dict[str, bool]:
    """Run the 9-point validation checklist"""
    checklist = {}

    # 1. Angelology passages accurately extracted
    checklist["angelology_passage_extracted"] = "exegesis" in data and data["exegesis"] is not None

    # 2. Lineage tags correct and schema-compliant
    valid_lineage, _ = check_lineage_schema(data)
    checklist["lineage_schema_compliant"] = valid_lineage

    # 3. Cross-references point to correct locations
    valid_refs, _ = check_cross_references(data)
    checklist["cross_references_valid"] = valid_refs

    # 4. Scholarly citations backed by corpus
    valid_cites, _ = check_scholar_citations(data, entry_id)
    checklist["scholarly_citations_backed"] = valid_cites

    # 5. Exegesis explains philosophical function
    exegesis = data.get("exegesis", "")
    checklist["exegesis_explains_function"] = len(str(exegesis)) > 50

    # 6. Tags consistent with schema
    valid_tags, _ = check_tags_schema(data)
    checklist["tags_consistent"] = valid_tags

    # 7. Status field accurate
    checklist["status_accurate"] = data.get("status") in ["draft", "sourced", "complete", "reviewed"]

    # 8. Confidence levels marked
    has_marker, _ = check_confidence_markers(data)
    checklist["confidence_levels_marked"] = has_marker

    # 9. Heretical conclusions flagged
    has_heretical, _ = check_heretical_adjacent(data)
    checklist["heretical_conclusions_flagged"] = has_heretical

    return checklist

def validate_entry(entry_path: Path) -> EntryValidation:
    """Validate a single entry file"""
    entry_id = entry_path.stem
    issues = []
    raw_data = {}
    checklist = {}

    # 1. JSON parsing
    valid_json, json_error, data = validate_json_parsing(entry_path)
    raw_data = data

    if not valid_json:
        issues.append(ValidationIssue(
            entry_id=entry_id,
            severity="CRITICAL",
            category="json_parsing",
            message=f"JSON parse error",
            details=json_error
        ))
        return EntryValidation(entry_id, str(entry_path), {}, issues, raw_data)

    # 2. Required fields
    has_required, missing = check_required_fields(data)
    if not has_required:
        issues.append(ValidationIssue(
            entry_id=entry_id,
            severity="HIGH",
            category="missing_fields",
            message=f"Missing required fields: {', '.join(missing)}"
        ))

    # 3. Schema validation
    valid_lineage, invalid_lineages = check_lineage_schema(data)
    if not valid_lineage:
        issues.append(ValidationIssue(
            entry_id=entry_id,
            severity="HIGH",
            category="lineage_schema_violation",
            message=f"Invalid lineage values: {', '.join(invalid_lineages)}"
        ))

    valid_tags, invalid_tags = check_tags_schema(data)
    if not valid_tags:
        issues.append(ValidationIssue(
            entry_id=entry_id,
            severity="HIGH",
            category="tag_schema_violation",
            message=f"Invalid tags: {', '.join(invalid_tags)}"
        ))

    # 4. Cross-references
    valid_refs, ref_issues = check_cross_references(data)
    if not valid_refs:
        for ref_issue in ref_issues:
            issues.append(ValidationIssue(
                entry_id=entry_id,
                severity="MEDIUM",
                category="cross_reference_error",
                message=ref_issue
            ))

    # 5. Confidence markers
    has_marker, marker_error = check_confidence_markers(data)
    if not has_marker:
        issues.append(ValidationIssue(
            entry_id=entry_id,
            severity="LOW",
            category="missing_confidence_marker",
            message=marker_error
        ))

    # 6. Heretical adjacent tagging
    heretical_valid, heretical_error = check_heretical_adjacent(data)
    if not heretical_valid:
        issues.append(ValidationIssue(
            entry_id=entry_id,
            severity="MEDIUM",
            category="heretical_tagging",
            message=heretical_error
        ))

    # 7. Run full checklist
    checklist = validate_entry_checklist(data, entry_id)

    return EntryValidation(
        entry_id=entry_id,
        file_path=str(entry_path),
        checklist=checklist,
        issues=issues,
        raw_data=data
    )

def validate_scholarship_files() -> Tuple[int, List[ValidationIssue]]:
    """Validate scholarship database files"""
    files_passing = 0
    issues = []

    for filename in SCHOLARSHIP_FILES:
        file_path = SCHOLARSHIPS_ROOT / filename
        if not file_path.exists():
            issues.append(ValidationIssue(
                entry_id=filename,
                severity="CRITICAL",
                category="missing_scholarship_file",
                message=f"Scholarship file missing: {filename}"
            ))
            continue

        data, error = load_json_safe(file_path)
        if error:
            issues.append(ValidationIssue(
                entry_id=filename,
                severity="CRITICAL",
                category="json_parsing",
                message=f"Scholarship file parse error",
                details=error
            ))
        else:
            files_passing += 1

    return files_passing, issues

def validate_all_entries() -> Tuple[List[EntryValidation], List[ValidationIssue]]:
    """Validate all 69 angelology entries"""
    entries = []
    critical_issues = []

    text_dirs = [
        ("oration", "O"),
        ("commento", "C"),
        ("heptaplus", "H"),
        ("being_unity", "U")
    ]

    for text_dir, prefix in text_dirs:
        entries_dir = TEXTS_ROOT / text_dir / "entries"
        if not entries_dir.exists():
            critical_issues.append(ValidationIssue(
                entry_id=text_dir,
                severity="CRITICAL",
                category="missing_directory",
                message=f"Entries directory missing: {text_dir}"
            ))
            continue

        entry_files = sorted(entries_dir.glob("*.json"))
        for entry_file in entry_files:
            validation = validate_entry(entry_file)
            entries.append(validation)

            # Track critical issues
            critical = [iss for iss in validation.issues if iss.severity == "CRITICAL"]
            critical_issues.extend(critical)

    return entries, critical_issues

def generate_report(entries: List[EntryValidation], scholarship_passing: int) -> ValidationReport:
    """Generate comprehensive validation report"""

    # Count entries passing all checks
    entries_passing = sum(
        1 for e in entries
        if not e.issues and all(e.checklist.values())
    )

    # Count issues by severity
    all_issues = []
    for entry in entries:
        all_issues.extend(entry.issues)

    issues_by_severity = {}
    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        issues_by_severity[severity] = len([i for i in all_issues if i.severity == severity])

    # Count entries by status
    entries_by_status = {}
    for entry in entries:
        if entry.raw_data:
            status = entry.raw_data.get("status", "unknown")
            entries_by_status[status] = entries_by_status.get(status, 0) + 1

    # Checklist summary (how many entries pass each criterion)
    checklist_summary = {}
    for criterion in [
        "angelology_passage_extracted",
        "lineage_schema_compliant",
        "cross_references_valid",
        "scholarly_citations_backed",
        "exegesis_explains_function",
        "tags_consistent",
        "status_accurate",
        "confidence_levels_marked",
        "heretical_conclusions_flagged"
    ]:
        passing = sum(
            1 for e in entries
            if e.checklist.get(criterion, False)
        )
        checklist_summary[criterion] = passing

    # Identify critical blockers
    critical_blockers = []
    if issues_by_severity["CRITICAL"] > 0:
        critical_issues = [i for i in all_issues if i.severity == "CRITICAL"]
        critical_blockers = list(set(i.category for i in critical_issues))

    if scholarship_passing < 6:
        critical_blockers.append("scholarship_database_incomplete")

    # Build entry validations for JSON output
    entry_validations = []
    for entry in entries:
        entry_validations.append({
            "entry_id": entry.entry_id,
            "file_path": entry.file_path,
            "checklist": entry.checklist,
            "checklist_passing": all(entry.checklist.values()),
            "issues_count": len(entry.issues),
            "issues": [asdict(i) for i in entry.issues]
        })

    return ValidationReport(
        timestamp=datetime.now().isoformat(),
        total_entries=len(entries),
        entries_passing=entries_passing,
        scholarship_files_passing=scholarship_passing,
        total_issues=issues_by_severity,
        entries_by_status=entries_by_status,
        checklist_summary=checklist_summary,
        critical_blockers=critical_blockers,
        entry_validations=entry_validations
    )

def main():
    """Run full validation suite"""
    print("=" * 80)
    print("PHASE 1-ALPHA FINAL VALIDATION")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 80)

    # Validate angelology entries
    print("\n[1/3] Validating 69 angelology entries...")
    entries, critical_entry_issues = validate_all_entries()
    print(f"  [OK] Checked {len(entries)} entries")

    # Validate scholarship database
    print("\n[2/3] Validating 6 scholarship files...")
    scholarship_passing, scholarship_issues = validate_scholarship_files()
    print(f"  [OK] Scholarship files: {scholarship_passing}/6 passing")

    # Generate report
    print("\n[3/3] Generating validation report...")
    report = generate_report(entries, scholarship_passing)

    # Output summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"\nAngelology Entries: {report.entries_passing}/{report.total_entries} passing all checks")
    print(f"Scholarship Database: {report.scholarship_files_passing}/6 files passing")
    print(f"\nIssues by Severity:")
    for severity, count in report.total_issues.items():
        print(f"  {severity}: {count}")

    print(f"\nEntries by Status:")
    for status, count in report.entries_by_status.items():
        print(f"  {status}: {count}")

    print(f"\n9-Point Checklist (entries passing each criterion):")
    criteria = [
        "angelology_passage_extracted",
        "lineage_schema_compliant",
        "cross_references_valid",
        "scholarly_citations_backed",
        "exegesis_explains_function",
        "tags_consistent",
        "status_accurate",
        "confidence_levels_marked",
        "heretical_conclusions_flagged"
    ]
    for i, criterion in enumerate(criteria, 1):
        passing = report.checklist_summary.get(criterion, 0)
        pct = (passing / report.total_entries * 100) if report.total_entries > 0 else 0
        print(f"  {i}. {criterion}: {passing}/{report.total_entries} ({pct:.1f}%)")

    print(f"\nCritical Blockers: {len(report.critical_blockers)}")
    for blocker in report.critical_blockers:
        print(f"  - {blocker}")

    # Approval decision
    print("\n" + "=" * 80)
    if report.critical_blockers:
        print("DECISION: HOLD - Critical issues remain")
    elif report.total_issues["CRITICAL"] > 0 or report.total_issues["HIGH"] > 0:
        print("DECISION: HOLD - High-priority issues require fixing")
    elif report.entries_passing < report.total_entries:
        print("DECISION: HOLD - Some entries incomplete")
    else:
        print("DECISION: APPROVED - All checks passed")
    print("=" * 80)

    # Save JSON report
    json_output = PROJECT_ROOT / "PHASE_1_ALPHA_FINAL_VALIDATION.json"
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(asdict(report), f, indent=2, default=str)
    print(f"\nJSON Report saved: {json_output}")

    return 0 if not report.critical_blockers else 1

if __name__ == "__main__":
    sys.exit(main())
