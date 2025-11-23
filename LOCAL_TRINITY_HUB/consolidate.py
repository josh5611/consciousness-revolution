#!/usr/bin/env python3
"""
PC1 Local Hub Consolidation Script
Merges all terminal and cloud reports into ONE output
"""

import os
import json
from datetime import datetime
from pathlib import Path

HUB_PATH = Path.home() / "PC1_LOCAL_HUB"
TERMINAL_REPORTS = HUB_PATH / "terminal_reports"
CLOUD_REPORTS = HUB_PATH / "cloud_reports"
CONSOLIDATED = HUB_PATH / "consolidated"
OUTBOUND = HUB_PATH / "outbound"

def load_reports(folder):
    """Load all JSON reports from a folder"""
    reports = []
    if folder.exists():
        for f in folder.glob("*.json"):
            try:
                with open(f) as fp:
                    reports.append(json.load(fp))
            except:
                pass
    return reports

def consolidate():
    """Merge all reports into one output"""

    # Load all reports
    terminal_reports = load_reports(TERMINAL_REPORTS)
    cloud_reports = load_reports(CLOUD_REPORTS)

    # Create consolidated output
    consolidated = {
        "computer": "PC1",
        "timestamp": datetime.now().isoformat(),
        "terminal_count": len(terminal_reports),
        "cloud_count": len(cloud_reports),
        "terminals": terminal_reports,
        "clouds": cloud_reports,
        "summary": {
            "work_completed": [],
            "work_in_progress": [],
            "blockers": []
        }
    }

    # Extract summaries
    for report in terminal_reports + cloud_reports:
        if report.get("work_completed"):
            consolidated["summary"]["work_completed"].append(
                f"{report.get('instance', 'unknown')}: {report['work_completed']}"
            )
        if report.get("work_in_progress"):
            consolidated["summary"]["work_in_progress"].append(
                f"{report.get('instance', 'unknown')}: {report['work_in_progress']}"
            )
        if report.get("blockers"):
            consolidated["summary"]["blockers"].append(
                f"{report.get('instance', 'unknown')}: {report['blockers']}"
            )

    # Save consolidated report
    consolidated_file = CONSOLIDATED / f"PC1_CONSOLIDATED_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(consolidated_file, 'w') as f:
        json.dump(consolidated, f, indent=2)

    # Create outbound file (this goes to GitHub)
    outbound_file = OUTBOUND / f"PC1_OUTPUT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(outbound_file, 'w') as f:
        json.dump(consolidated, f, indent=2)

    # Print summary
    print(f"✅ Consolidated {len(terminal_reports)} terminal + {len(cloud_reports)} cloud reports")
    print(f"📄 Output: {outbound_file}")
    print(f"\n📋 Summary:")
    print(f"   Work completed: {len(consolidated['summary']['work_completed'])} items")
    print(f"   In progress: {len(consolidated['summary']['work_in_progress'])} items")
    print(f"   Blockers: {len(consolidated['summary']['blockers'])} items")

    return outbound_file

if __name__ == "__main__":
    consolidate()
