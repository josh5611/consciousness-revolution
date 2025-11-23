#!/usr/bin/env python3
"""
Boot Down Consolidator
Merges all boot down reports into ONE output
Same funnel pattern as reporting
"""

import os
import json
from datetime import datetime
from pathlib import Path

HUB_PATH = Path.home() / "PC1_LOCAL_HUB"
BOOT_DOWN_INPUTS = HUB_PATH / "boot_down_inputs"
BOOT_DOWN_ARCHIVE = HUB_PATH / "boot_down_archive"

# Ensure folders exist
BOOT_DOWN_INPUTS.mkdir(exist_ok=True)
BOOT_DOWN_ARCHIVE.mkdir(exist_ok=True)

def consolidate_boot_downs():
    """Merge all boot down reports into one"""

    # Collect all boot down files
    boot_downs = []

    for f in BOOT_DOWN_INPUTS.glob("*.json"):
        try:
            with open(f) as fp:
                data = json.load(fp)
                boot_downs.append(data)
        except:
            pass

    for f in BOOT_DOWN_INPUTS.glob("*.md"):
        try:
            with open(f) as fp:
                content = fp.read()
                boot_downs.append({
                    "source": f.name,
                    "content": content
                })
        except:
            pass

    if not boot_downs:
        print("No boot down reports found")
        return None

    # Create consolidated boot down
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    consolidated = {
        "timestamp": timestamp,
        "computer": "PC1",
        "instance_count": len(boot_downs),
        "instances": boot_downs,
        "summary": {
            "work_completed": [],
            "state_to_preserve": [],
            "next_session_priorities": [],
            "blockers": []
        }
    }

    # Extract summaries from each boot down
    for bd in boot_downs:
        if isinstance(bd, dict):
            if bd.get("work_completed"):
                consolidated["summary"]["work_completed"].append(bd["work_completed"])
            if bd.get("state"):
                consolidated["summary"]["state_to_preserve"].append(bd["state"])
            if bd.get("next_priorities"):
                consolidated["summary"]["next_session_priorities"].append(bd["next_priorities"])
            if bd.get("blockers"):
                consolidated["summary"]["blockers"].append(bd["blockers"])

    # Save consolidated boot down
    output_file = BOOT_DOWN_ARCHIVE / f"BOOT_DOWN_{timestamp}.json"
    with open(output_file, 'w') as f:
        json.dump(consolidated, f, indent=2)

    # Also save as markdown for readability
    md_file = BOOT_DOWN_ARCHIVE / f"BOOT_DOWN_{timestamp}.md"
    with open(md_file, 'w') as f:
        f.write(f"# BOOT DOWN - {timestamp}\n\n")
        f.write(f"**Computer**: PC1\n")
        f.write(f"**Instances**: {len(boot_downs)}\n\n")

        f.write("## Work Completed\n")
        for item in consolidated["summary"]["work_completed"]:
            f.write(f"- {item}\n")

        f.write("\n## State to Preserve\n")
        for item in consolidated["summary"]["state_to_preserve"]:
            f.write(f"- {item}\n")

        f.write("\n## Next Session Priorities\n")
        for item in consolidated["summary"]["next_session_priorities"]:
            f.write(f"- {item}\n")

        f.write("\n## Blockers\n")
        for item in consolidated["summary"]["blockers"]:
            f.write(f"- {item}\n")

    # Clear inputs (they've been archived)
    for f in BOOT_DOWN_INPUTS.glob("*"):
        f.unlink()

    print(f"✅ Consolidated {len(boot_downs)} boot downs")
    print(f"📄 Output: {output_file}")
    print(f"📄 Markdown: {md_file}")

    return output_file

def get_latest_boot_down():
    """Get the most recent boot down file"""
    files = sorted(BOOT_DOWN_ARCHIVE.glob("BOOT_DOWN_*.md"))
    if files:
        return files[-1]
    return None

if __name__ == "__main__":
    consolidate_boot_downs()
