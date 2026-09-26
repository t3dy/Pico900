#!/usr/bin/env python3
"""
Neoplatonism Research Module for Pico900

Manages indexing, querying, and tracking of Neoplatonism research across the archive.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Project paths
PICO900_ROOT = Path(__file__).parent.parent
DATA_NEO = PICO900_ROOT / "data" / "neoplatonism"
ARCHIVE_ROOT = Path("e:\\pdf\\Neoplatonism")
MANIFEST_PATH = PICO900_ROOT / "data" / "conclusions_manifest.json"


class NeoplatonismResearch:
    """Manage Neoplatonism research for Pico900."""

    def __init__(self):
        self.philosophers = self._load_json(DATA_NEO / "philosophers_index.json")
        self.theses = self._load_json(DATA_NEO / "theses_mapping.json")
        self.archive = self._load_json(DATA_NEO / "archive_inventory.json")

    def _load_json(self, path: Path) -> Dict:
        """Load JSON safely."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {path} not found")
            return {}

    def _save_json(self, data: Dict, path: Path):
        """Save JSON safely."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # --- Query Operations ---

    def get_philosopher(self, phil_id: str) -> Optional[Dict]:
        """Get philosopher metadata by ID."""
        for phil in self.philosophers.get("philosophers", []):
            if phil["id"] == phil_id:
                return phil
        return None

    def list_philosophers(self) -> List[str]:
        """List all philosopher IDs."""
        return [p["id"] for p in self.philosophers.get("philosophers", [])]

    def get_archive_location(self, phil_id: str) -> List[str]:
        """Get archive folders for a philosopher."""
        phil = self.get_philosopher(phil_id)
        if phil:
            return phil.get("archive_locations", [])
        return []

    def get_philosopher_works(self, phil_id: str) -> List[Dict]:
        """Get key works of a philosopher."""
        phil = self.get_philosopher(phil_id)
        if phil:
            return phil.get("key_works", [])
        return []

    def get_archive_priority(self, folder_name: str) -> str:
        """Get priority level of an archive folder."""
        for d in self.archive.get("directories", []):
            if d["name"] == folder_name:
                return d["priority"]
        return "unknown"

    def list_high_priority_archives(self) -> List[str]:
        """List high-priority and critical archive folders."""
        critical = self.archive["research_priorities"].get("1_critical", [])
        high = self.archive["research_priorities"].get("2_high", [])

        # Extract folder names from descriptions
        folders = []
        for item in critical + high:
            # Try to extract folder name (first word usually)
            parts = item.split()
            if parts:
                folder = parts[0].rstrip("(")
                if folder in [d["name"] for d in self.archive["directories"]]:
                    folders.append(folder)

        return folders

    # --- Thesis Mapping ---

    def add_thesis_mapping(self,
                          conclusion_id: int,
                          philosophers: List[str],
                          status: str = "candidate",
                          notes: str = ""):
        """Add or update a thesis mapping."""
        thesis = {
            "conclusion_id": conclusion_id,
            "status": status,
            "neoplatonist_philosophers": philosophers,
            "primary_sources": [],
            "scholarship": [],
            "notes": notes,
            "last_checked": datetime.now().isoformat(),
            "researcher": "automated"
        }

        # Find and update or append
        theses_list = self.theses.get("theses", [])
        existing = None
        for t in theses_list:
            if t["conclusion_id"] == conclusion_id:
                existing = t
                break

        if existing:
            existing.update(thesis)
        else:
            theses_list.append(thesis)

        self._save_json(self.theses, DATA_NEO / "theses_mapping.json")
        self._update_summary()

    def add_primary_source(self,
                          conclusion_id: int,
                          philosopher: str,
                          work: str,
                          edition: str,
                          pages: str):
        """Add a primary source to a thesis mapping."""
        theses_list = self.theses.get("theses", [])
        for t in theses_list:
            if t["conclusion_id"] == conclusion_id:
                t["primary_sources"].append({
                    "philosopher": philosopher,
                    "work": work,
                    "edition": edition,
                    "pages": pages,
                    "quote_extracted": False
                })
                t["last_checked"] = datetime.now().isoformat()
                break

        self._save_json(self.theses, DATA_NEO / "theses_mapping.json")
        self._update_summary()

    def add_scholarship(self,
                       conclusion_id: int,
                       author: str,
                       work: str,
                       chapter: str,
                       pages: str):
        """Add secondary scholarship reference."""
        theses_list = self.theses.get("theses", [])
        for t in theses_list:
            if t["conclusion_id"] == conclusion_id:
                t["scholarship"].append({
                    "author": author,
                    "work": work,
                    "chapter": chapter,
                    "pages": pages,
                    "quote_extracted": False,
                    "pico_connection_stated": True
                })
                t["last_checked"] = datetime.now().isoformat()
                break

        self._save_json(self.theses, DATA_NEO / "theses_mapping.json")
        self._update_summary()

    def _update_summary(self):
        """Update research summary statistics."""
        theses_list = self.theses.get("theses", [])
        stats = {
            "total_conclusions": len(theses_list),
            "unmapped": len([t for t in theses_list if t["status"] == "unmapped"]),
            "candidate": len([t for t in theses_list if t["status"] == "candidate"]),
            "primary_sourced": len([t for t in theses_list if t["status"] == "primary_sourced"]),
            "scholarship_added": len([t for t in theses_list if t["status"] == "scholarship_added"]),
            "commentary_ready": len([t for t in theses_list if t["status"] == "commentary_ready"]),
            "last_updated": datetime.now().isoformat()
        }

        self.theses["summary_statistics"] = stats
        self._save_json(self.theses, DATA_NEO / "theses_mapping.json")

    def get_thesis_status(self, conclusion_id: int) -> Optional[Dict]:
        """Get status of a thesis mapping."""
        for t in self.theses.get("theses", []):
            if t["conclusion_id"] == conclusion_id:
                return t
        return None

    def get_theses_by_philosopher(self, phil_id: str) -> List[Dict]:
        """Get all theses mapped to a philosopher."""
        result = []
        for t in self.theses.get("theses", []):
            if phil_id in t.get("neoplatonist_philosophers", []):
                result.append(t)
        return result

    def get_theses_by_status(self, status: str) -> List[Dict]:
        """Get all theses with a given status."""
        return [t for t in self.theses.get("theses", []) if t["status"] == status]

    # --- Reporting ---

    def report_research_status(self) -> str:
        """Generate a status report."""
        stats = self.theses.get("summary_statistics", {})

        report = f"""
Neoplatonism Research Status Report
===================================
Generated: {datetime.now().isoformat()}

Total Conclusions in 900: {stats.get('total_conclusions', '?')}

Status Breakdown:
  - Unmapped:            {stats.get('unmapped', '?')}
  - Candidate:           {stats.get('candidate', '?')}
  - Primary Sourced:     {stats.get('primary_sourced', '?')}
  - Scholarship Added:   {stats.get('scholarship_added', '?')}
  - Commentary Ready:    {stats.get('commentary_ready', '?')}

Archive Resources:
  - Critical Priority:   {len(self.archive['research_priorities']['1_critical'])} items
  - High Priority:       {len(self.archive['research_priorities']['2_high'])} items
  - Medium Priority:     {len(self.archive['research_priorities']['3_medium'])} items

Key Philosophers:
  {', '.join(self.list_philosophers())}
"""
        return report

    def report_philosopher(self, phil_id: str) -> str:
        """Generate a report on a philosopher."""
        phil = self.get_philosopher(phil_id)
        if not phil:
            return f"Philosopher '{phil_id}' not found."

        theses = self.get_theses_by_philosopher(phil_id)

        report = f"""
{phil['name']} ({phil['dates']})
{'-' * 60}

Core Concepts:
  {', '.join(phil['core_concepts'])}

Key Works:
  {chr(10).join([f"  - {w['title']}" for w in phil['key_works']])}

Archive Locations:
  {', '.join(phil['archive_locations'])}

Pico Relevance:
  {phil['pico_relevance']}

Theses Mapped: {len(theses)}
  {theses[:5] if theses else 'None yet'}
"""
        return report

    def report_archive(self) -> str:
        """Generate a report on the archive."""
        report = f"""
Neoplatonism Archive Report
============================
Root: {self.archive['archive_root']}
Last Scanned: {self.archive['last_scanned']}

Directories: {len(self.archive['directories'])}
  Critical: {len([d for d in self.archive['directories'] if d['priority'] == 'critical'])}
  High:     {len([d for d in self.archive['directories'] if d['priority'] == 'high'])}
  Medium:   {len([d for d in self.archive['directories'] if d['priority'] == 'medium'])}

Loose Files: {len(self.archive['loose_files'])}

Critical Resources:
"""
        for item in self.archive['research_priorities']['1_critical']:
            report += f"  - {item}\n"

        return report


def main():
    """CLI for Neoplatonism research."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Neoplatonism Research Module for Pico900"
    )
    parser.add_argument("--status", action="store_true",
                       help="Show research status report")
    parser.add_argument("--philosopher", type=str,
                       help="Show report on a philosopher")
    parser.add_argument("--archive", action="store_true",
                       help="Show archive report")
    parser.add_argument("--list-philosophers", action="store_true",
                       help="List all philosophers")
    parser.add_argument("--list-archives", action="store_true",
                       help="List high-priority archives")

    args = parser.parse_args()

    research = NeoplatonismResearch()

    if args.status:
        print(research.report_research_status())
    elif args.philosopher:
        print(research.report_philosopher(args.philosopher))
    elif args.archive:
        print(research.report_archive())
    elif args.list_philosophers:
        print("\nAvailable Philosophers:")
        for phil_id in research.list_philosophers():
            phil = research.get_philosopher(phil_id)
            print(f"  {phil_id:20} {phil['name']:25} ({phil['dates']})")
    elif args.list_archives:
        print("\nHigh-Priority Archive Folders:")
        for folder in research.list_high_priority_archives():
            priority = research.get_archive_priority(folder)
            print(f"  [{priority:10}] {folder}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
