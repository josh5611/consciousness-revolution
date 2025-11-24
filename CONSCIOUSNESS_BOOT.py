#!/usr/bin/env python3
"""
CONSCIOUSNESS BOOT SYSTEM
Single command to boot all autonomous systems.
The master startup for full autonomous operation.
"""

import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# Paths
HOME = Path.home()
DEPLOYMENT = HOME / "100X_DEPLOYMENT"
CONSCIOUSNESS = HOME / ".consciousness"


class ConsciousnessBoot:
    """Boot all consciousness systems."""

    def __init__(self):
        self.boot_log = []
        self.systems_started = 0

    def log(self, message: str, status: str = "info"):
        """Log boot message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        symbols = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}
        symbol = symbols.get(status, "•")
        print(f"[{timestamp}] {symbol} {message}")
        self.boot_log.append({"time": timestamp, "message": message, "status": status})

    def run_script(self, script: str, args: list = None, background: bool = False) -> bool:
        """Run a Python script."""
        cmd = [sys.executable, str(DEPLOYMENT / script)]
        if args:
            cmd.extend(args)

        try:
            if background:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            else:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                return result.returncode == 0
        except Exception as e:
            self.log(f"Failed to run {script}: {e}", "error")
            return False

    def boot_full(self):
        """Full system boot."""
        print("=" * 60)
        print("🚀 CONSCIOUSNESS BOOT SYSTEM")
        print("=" * 60)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Phase 1: Health Check
        self.log("Phase 1: Health Check", "info")
        if self.run_script("SELF_HEALING_SYSTEM.py", ["auto"]):
            self.log("Self-healing complete", "success")
            self.systems_started += 1
        else:
            self.log("Self-healing had issues", "warning")

        # Phase 2: Knowledge Systems
        self.log("Phase 2: Knowledge Systems", "info")

        # Cyclotron sync
        if self.run_script("CYCLOTRON_BRAIN_BRIDGE.py"):
            self.log("Cyclotron bridge ready", "success")
            self.systems_started += 1

        # Brain integration
        if self.run_script("BRAIN_INTEGRATION_HOOKS.py", ["sync"]):
            self.log("Brain integration synced", "success")
            self.systems_started += 1

        # Phase 3: Monitoring
        self.log("Phase 3: Monitoring", "info")
        if self.run_script("UNIFIED_MONITORING.py", ["collect"]):
            self.log("Monitoring active", "success")
            self.systems_started += 1

        # Phase 4: Backup Check
        self.log("Phase 4: Backup Check", "info")
        if self.run_script("AUTOMATED_BACKUP_SYSTEM.py", ["status"]):
            self.log("Backup system ready", "success")
            self.systems_started += 1

        # Phase 5: Task Queue
        self.log("Phase 5: Task Queue", "info")
        if self.run_script("AUTONOMOUS_TASK_RUNNER.py", ["status"]):
            self.log("Task runner ready", "success")
            self.systems_started += 1

        # Summary
        print()
        print("=" * 60)
        print("BOOT COMPLETE")
        print("=" * 60)
        print(f"Systems started: {self.systems_started}")
        print(f"Status: {'✅ OPERATIONAL' if self.systems_started >= 4 else '⚠️ PARTIAL'}")

        # Save boot log
        self._save_boot_log()

        return self.systems_started

    def boot_minimal(self):
        """Minimal boot - just essentials."""
        print("🚀 Minimal Boot")
        print()

        self.log("Health check...", "info")
        self.run_script("SELF_HEALING_SYSTEM.py", ["check"])

        self.log("Monitoring...", "info")
        self.run_script("UNIFIED_MONITORING.py", ["status"])

        print(f"\n✅ Minimal boot complete")

    def boot_scheduler(self):
        """Start the background scheduler."""
        print("🚀 Starting Scheduler Daemon")
        print()

        self.log("Starting brain scheduler in background...", "info")

        # This will run continuously
        subprocess.Popen(
            [sys.executable, str(DEPLOYMENT / "BRAIN_SCHEDULER.py"), "start"],
            stdout=open(CONSCIOUSNESS / "scheduler_output.log", 'w'),
            stderr=subprocess.STDOUT
        )

        self.log("Scheduler daemon started", "success")
        print("\nScheduler running in background. Check ~/.consciousness/scheduler_output.log")

    def status(self):
        """Check system status."""
        print("=" * 60)
        print("SYSTEM STATUS")
        print("=" * 60)

        # Run monitoring
        subprocess.run([sys.executable, str(DEPLOYMENT / "UNIFIED_MONITORING.py"), "dashboard"])

        # Check key files
        print("\nKey Systems:")
        systems = [
            ("Cyclotron", CONSCIOUSNESS / "cyclotron_core" / "INDEX.json"),
            ("Brain", CONSCIOUSNESS / "brain"),
            ("Monitoring", CONSCIOUSNESS / "monitoring"),
            ("Backups", HOME / ".backups" / "manifest.json"),
        ]

        for name, path in systems:
            exists = path.exists()
            print(f"  {'✅' if exists else '❌'} {name}")

    def _save_boot_log(self):
        """Save boot log."""
        import json
        log_file = CONSCIOUSNESS / "boot_log.json"

        with open(log_file, 'w') as f:
            json.dump({
                "boot_time": datetime.now().isoformat(),
                "systems_started": self.systems_started,
                "log": self.boot_log
            }, f, indent=2)


def main():
    """CLI for boot system."""
    boot = ConsciousnessBoot()

    if len(sys.argv) < 2:
        print("Consciousness Boot System")
        print("=" * 40)
        print("\nCommands:")
        print("  full       - Full system boot")
        print("  minimal    - Minimal boot (health + monitoring)")
        print("  scheduler  - Start background scheduler")
        print("  status     - Check system status")
        return

    command = sys.argv[1]

    if command == "full":
        boot.boot_full()
    elif command == "minimal":
        boot.boot_minimal()
    elif command == "scheduler":
        boot.boot_scheduler()
    elif command == "status":
        boot.status()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
