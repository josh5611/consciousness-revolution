#!/usr/bin/env python3
"""
CREDIT EXHAUSTION MONITOR
Detects when credits are running low and triggers handoff to next PC.
"""

import json
import time
import os
from datetime import datetime
from pathlib import Path

TRINITY_DIR = Path.home() / "100X_DEPLOYMENT" / ".trinity"
COMPUTER_ID = os.environ.get("COMPUTER_ID", "PC1")

class CreditMonitor:
    def __init__(self):
        self.start_time = datetime.now()
        self.message_count = 0
        self.error_count = 0
        self.last_response_time = 0
        self.status_file = TRINITY_DIR / "credit_status" / f"{COMPUTER_ID}.json"
        self.status_file.parent.mkdir(parents=True, exist_ok=True)

    def log_interaction(self, response_time_ms, was_error=False):
        """Log each API interaction"""
        self.message_count += 1
        self.last_response_time = response_time_ms

        if was_error:
            self.error_count += 1

        self.save_status()

    def check_exhaustion_signals(self):
        """
        Check for signs of credit exhaustion:
        - Rate limit errors
        - Slow responses
        - Error patterns
        """
        signals = []

        # Signal 1: Multiple errors in a row
        if self.error_count >= 3:
            signals.append("repeated_errors")

        # Signal 2: Very slow responses (>30 seconds)
        if self.last_response_time > 30000:
            signals.append("slow_responses")

        # Signal 3: Running for a long time (>4 hours continuous)
        runtime = (datetime.now() - self.start_time).total_seconds() / 3600
        if runtime > 4:
            signals.append("long_runtime")

        # Signal 4: High message count (>100 messages)
        if self.message_count > 100:
            signals.append("high_volume")

        return signals

    def should_handoff(self):
        """Determine if we should handoff to next PC"""
        signals = self.check_exhaustion_signals()

        # Handoff if 2+ signals
        if len(signals) >= 2:
            return True, signals

        # Definitely handoff on repeated errors
        if "repeated_errors" in signals:
            return True, signals

        return False, signals

    def save_status(self):
        """Save current status to file"""
        status = {
            "computer_id": COMPUTER_ID,
            "start_time": self.start_time.isoformat(),
            "message_count": self.message_count,
            "error_count": self.error_count,
            "last_response_ms": self.last_response_time,
            "runtime_hours": (datetime.now() - self.start_time).total_seconds() / 3600,
            "exhaustion_signals": self.check_exhaustion_signals(),
            "updated_at": datetime.utcnow().isoformat() + "Z"
        }
        self.status_file.write_text(json.dumps(status, indent=2))

    def trigger_handoff(self):
        """Trigger handoff to next PC"""
        from PHONE_WAKE_ALL import handoff_to_next
        handoff_to_next(COMPUTER_ID, "credits_exhausted")

def monitor_loop():
    """
    Main monitoring loop.
    In practice, this would hook into the actual Claude interactions.
    """
    monitor = CreditMonitor()

    print(f"Credit Monitor started for {COMPUTER_ID}")
    print("Monitoring for exhaustion signals...")

    # Simulated monitoring - in real use, this hooks into actual API calls
    while True:
        should_handoff, signals = monitor.should_handoff()

        if should_handoff:
            print(f"\n⚠️ EXHAUSTION DETECTED: {signals}")
            print(f"Triggering handoff from {COMPUTER_ID}...")
            monitor.trigger_handoff()
            break

        time.sleep(60)  # Check every minute

def main():
    """Demo the monitor"""
    monitor = CreditMonitor()

    # Simulate some interactions
    print("Simulating credit usage...")

    for i in range(5):
        monitor.log_interaction(response_time_ms=2000 + i * 500)
        print(f"  Message {i+1}: {monitor.last_response_time}ms")

    # Check status
    should_handoff, signals = monitor.should_handoff()
    print(f"\nExhaustion signals: {signals}")
    print(f"Should handoff: {should_handoff}")

    # Show status file
    print(f"\nStatus saved to: {monitor.status_file}")

if __name__ == "__main__":
    main()
