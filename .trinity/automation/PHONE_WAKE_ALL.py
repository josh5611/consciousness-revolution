#!/usr/bin/env python3
"""
PHONE WAKE ALL - Trigger all 3 computers from phone
Creates wake signals that each PC's daemon picks up.
"""

import json
from datetime import datetime
from pathlib import Path
import subprocess

TRINITY_DIR = Path.home() / "100X_DEPLOYMENT" / ".trinity"
WAKE_DIR = TRINITY_DIR / "wake_signals"

def wake_all_computers(task_description="Start Triple Trinity"):
    """Create wake signals for all 3 PCs"""
    WAKE_DIR.mkdir(parents=True, exist_ok=True)

    computers = ["PC1", "PC2", "PC3"]

    for pc in computers:
        wake_signal = {
            "target": pc,
            "command": "START_TRINITY",
            "task": task_description,
            "triggered_at": datetime.utcnow().isoformat() + "Z",
            "triggered_by": "phone",
            "status": "pending"
        }

        signal_file = WAKE_DIR / f"{pc}_wake.json"
        signal_file.write_text(json.dumps(wake_signal, indent=2))
        print(f"📱 Wake signal created for {pc}")

    # Git sync
    git_sync()

    print(f"\n✅ All 3 computers will wake on next daemon poll (<60 sec)")
    print(f"   Task: {task_description}")

def wake_single(computer_id, task_description):
    """Wake just one computer"""
    WAKE_DIR.mkdir(parents=True, exist_ok=True)

    wake_signal = {
        "target": computer_id,
        "command": "START_TRINITY",
        "task": task_description,
        "triggered_at": datetime.utcnow().isoformat() + "Z",
        "triggered_by": "phone",
        "status": "pending"
    }

    signal_file = WAKE_DIR / f"{computer_id}_wake.json"
    signal_file.write_text(json.dumps(wake_signal, indent=2))

    git_sync()
    print(f"📱 {computer_id} wake signal sent: {task_description}")

def handoff_to_next(current_pc, reason="credits_exhausted"):
    """Handoff work to next PC in chain"""
    chain = {"PC1": "PC2", "PC2": "PC3", "PC3": "PC1"}
    next_pc = chain.get(current_pc, "PC1")

    WAKE_DIR.mkdir(parents=True, exist_ok=True)

    handoff = {
        "target": next_pc,
        "command": "HANDOFF_CONTINUE",
        "from": current_pc,
        "reason": reason,
        "triggered_at": datetime.utcnow().isoformat() + "Z",
        "status": "pending"
    }

    signal_file = WAKE_DIR / f"{next_pc}_wake.json"
    signal_file.write_text(json.dumps(handoff, indent=2))

    # Save handoff state
    state_file = TRINITY_DIR / "handoff_state.json"
    state_file.write_text(json.dumps({
        "from": current_pc,
        "to": next_pc,
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }, indent=2))

    git_sync()
    print(f"🔄 Handoff: {current_pc} → {next_pc} ({reason})")

def git_sync():
    """Push wake signals to git"""
    repo = Path.home() / "100X_DEPLOYMENT"
    try:
        subprocess.run(["git", "add", "-A"], cwd=repo, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"phone trigger: wake signal {datetime.now().strftime('%H:%M')}"],
            cwd=repo, capture_output=True
        )
        subprocess.run(
            ["git", "push", "overkor-tek", "HEAD:master"],
            cwd=repo, capture_output=True
        )
    except:
        pass

def main():
    """Demo: Wake all computers"""
    import sys

    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        task = "Execute spawn queue tasks - Triple Trinity mode"

    print("=" * 50)
    print("  PHONE WAKE ALL - Triple Trinity Activation")
    print("=" * 50)
    print()

    wake_all_computers(task)

    print()
    print("Each PC will:")
    print("  1. Detect wake signal via daemon")
    print("  2. Start Trinity (3 instances)")
    print("  3. Claim tasks from spawn queue")
    print("  4. Execute until credits exhausted")
    print("  5. Handoff to next PC")

if __name__ == "__main__":
    main()
