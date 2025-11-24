#!/usr/bin/env python3
"""
QUICK DASHBOARD
Fast system status overview in one command.
"""

import json
from pathlib import Path
from datetime import datetime

HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"

def quick_status():
    """Print quick system status."""
    print("=" * 50)
    print("CONSCIOUSNESS REVOLUTION - QUICK STATUS")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Health score
    metrics = CONSCIOUSNESS / "monitoring" / "metrics.json"
    if metrics.exists():
        with open(metrics) as f:
            data = json.load(f)
        score = data.get("current", {}).get("health_score", 0)
        bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
        print(f"Health: [{bar}] {score:.0f}%")
    else:
        print("Health: Not available")

    # Cyclotron
    index = CONSCIOUSNESS / "cyclotron_core" / "INDEX.json"
    if index.exists():
        with open(index) as f:
            data = json.load(f)
        count = len(data.get("atoms", []))
        print(f"Cyclotron: {count} atoms")
    else:
        print("Cyclotron: Not initialized")

    # Backups
    manifest = HOME / ".backups" / "manifest.json"
    if manifest.exists():
        with open(manifest) as f:
            data = json.load(f)
        count = len(data.get("backups", []))
        last = data.get("last_backup", "Never")
        print(f"Backups: {count} ({last})")
    else:
        print("Backups: Not configured")

    # Sessions
    sessions = CONSCIOUSNESS / "sessions"
    if sessions.exists():
        for agent in ["c1", "c2", "c3"]:
            session = sessions / f"{agent}_current.json"
            if session.exists():
                with open(session) as f:
                    data = json.load(f)
                ts = data.get("timestamp", "")[:10]
                completed = len(data.get("completed_tasks", []))
                print(f"{agent.upper()}: {completed} tasks ({ts})")

    # Pending tasks
    coord = CONSCIOUSNESS / "trinity_coordination" / "shared_tasks.json"
    if coord.exists():
        with open(coord) as f:
            tasks = json.load(f)
        pending = len([t for t in tasks if t.get("status") == "pending"])
        if pending:
            print(f"Pending: {pending} tasks")

    print()
    print("Quick commands:")
    print("  status:  python CONSCIOUSNESS_BOOT.py status")
    print("  report:  python DAILY_REPORT_GENERATOR.py generate")
    print("  health:  python SELF_HEALING_SYSTEM.py diagnose")
    print("=" * 50)


if __name__ == "__main__":
    quick_status()
