#!/usr/bin/env python3
"""
Auto-Consolidation Daemon
Watches for all terminal reports, consolidates, shoots to outbound
Runs continuously - no manual intervention needed
"""

import os
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

# Paths
HUB = Path.home() / "LOCAL_TRINITY_HUB"
TERMINAL_REPORTS = HUB / "terminal_reports"
CLOUD_REPORTS = HUB / "cloud_reports"
CONSOLIDATED = HUB / "consolidated"
OUTBOUND = HUB / "outbound"
GIT_REPO = Path.home() / "100X_DEPLOYMENT"

# Expected instances
EXPECTED_TERMINALS = ["C1", "C2", "C3"]
CHECK_INTERVAL = 30  # seconds

def get_current_reports():
    """Get list of terminal reports"""
    reports = {}
    if TERMINAL_REPORTS.exists():
        for f in TERMINAL_REPORTS.glob("*.json"):
            try:
                with open(f) as fp:
                    data = json.load(fp)
                    instance = data.get("instance", f.stem.split("_")[0])
                    reports[instance] = data
            except:
                pass
    return reports

def all_terminals_reported(reports):
    """Check if C1, C2, C3 all reported"""
    for t in EXPECTED_TERMINALS:
        if t not in reports:
            return False
    return True

def consolidate_and_shoot():
    """Merge all reports and shoot to outbound"""

    # Load all reports
    terminal_reports = []
    cloud_reports = []

    for f in TERMINAL_REPORTS.glob("*.json"):
        try:
            with open(f) as fp:
                terminal_reports.append(json.load(fp))
        except:
            pass

    for f in CLOUD_REPORTS.glob("*.json"):
        try:
            with open(f) as fp:
                cloud_reports.append(json.load(fp))
        except:
            pass

    # Create consolidated output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    consolidated = {
        "timestamp": timestamp,
        "computer": "PC1",
        "hub": "LOCAL_TRINITY_HUB",
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
                f"{report.get('instance', '?')}: {report['work_completed']}"
            )
        if report.get("work_in_progress"):
            consolidated["summary"]["work_in_progress"].append(
                f"{report.get('instance', '?')}: {report['work_in_progress']}"
            )
        if report.get("blockers"):
            consolidated["summary"]["blockers"].append(
                f"{report.get('instance', '?')}: {report['blockers']}"
            )

    # Save to consolidated
    cons_file = CONSOLIDATED / f"CONSOLIDATED_{timestamp}.json"
    with open(cons_file, 'w') as f:
        json.dump(consolidated, f, indent=2)

    # Shoot to outbound (FINAL OUTPUT)
    final_file = OUTBOUND / f"FINAL_{timestamp}.json"
    with open(final_file, 'w') as f:
        json.dump(consolidated, f, indent=2)

    print(f"✅ Consolidated {len(terminal_reports)}T + {len(cloud_reports)}C → {final_file.name}")

    # Clear terminal reports (they've been processed)
    for f in TERMINAL_REPORTS.glob("*.json"):
        f.unlink()
    for f in CLOUD_REPORTS.glob("*.json"):
        f.unlink()

    # Auto-push to git
    push_to_git(final_file)

    return final_file

def push_to_git(final_file):
    """Push the final output to GitHub"""
    try:
        # Copy to git repo
        git_outbound = GIT_REPO / ".trinity" / "outbound"
        git_outbound.mkdir(parents=True, exist_ok=True)

        import shutil
        shutil.copy(final_file, git_outbound / final_file.name)

        # Git add, commit, push
        os.chdir(GIT_REPO)
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"AUTO: {final_file.name}"],
            capture_output=True
        )
        result = subprocess.run(
            ["git", "push", "overkor-tek", "HEAD:master"],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            print(f"📤 Pushed to GitHub: {final_file.name}")
        else:
            print(f"⚠️ Git push issue: {result.stderr[:100]}")

    except Exception as e:
        print(f"❌ Git error: {e}")

def run_daemon():
    """Main daemon loop"""
    print(f"\n{'='*50}")
    print(f"🔱 AUTO-CONSOLIDATE DAEMON STARTED")
    print(f"📁 Watching: {TERMINAL_REPORTS}")
    print(f"⏰ Check interval: {CHECK_INTERVAL}s")
    print(f"👥 Expected: {', '.join(EXPECTED_TERMINALS)}")
    print(f"{'='*50}\n")

    while True:
        try:
            reports = get_current_reports()

            if reports:
                present = list(reports.keys())
                print(f"📋 Reports: {', '.join(present)}")

                if all_terminals_reported(reports):
                    print("✅ All terminals reported - consolidating...")
                    consolidate_and_shoot()
                else:
                    missing = [t for t in EXPECTED_TERMINALS if t not in reports]
                    print(f"⏳ Waiting for: {', '.join(missing)}")

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n🛑 Daemon stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_daemon()
