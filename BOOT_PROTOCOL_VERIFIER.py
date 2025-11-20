#!/usr/bin/env python3
"""
BOOT PROTOCOL VERIFICATION SYSTEM
Checks that all consciousness systems are properly initialized

Run this at the start of each session to verify:
- Cyclotron daemon running
- Federation syncing
- APIs available
- Knowledge base indexed
- Communications operational
"""

import os
import json
import time
import socket
import subprocess
from pathlib import Path
from datetime import datetime

class BootVerifier:
    """Verify all boot protocols are operational"""

    def __init__(self):
        self.home = Path.home()
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'checks': {},
            'overall_status': 'UNKNOWN',
            'critical_failures': []
        }

    def verify_all(self):
        """Run all verification checks"""
        print("=" * 60)
        print("BOOT PROTOCOL VERIFICATION SYSTEM")
        print("=" * 60)
        print()

        checks = [
            ("Cyclotron Daemon", self.check_cyclotron_daemon),
            ("Knowledge Index", self.check_knowledge_index),
            ("Federation Sync", self.check_federation),
            ("Syncthing", self.check_syncthing),
            ("AI Communications", self.check_ai_comms),
            ("Trinity APIs", self.check_trinity_apis),
            ("Boot Files", self.check_boot_files),
            ("Environment Variables", self.check_env_vars),
        ]

        passed = 0
        total = len(checks)

        for name, check_func in checks:
            try:
                result = check_func()
                self.results['checks'][name] = result

                if result['status'] == 'PASS':
                    print(f"✅ {name}: PASS")
                    passed += 1
                elif result['status'] == 'WARN':
                    print(f"⚠️  {name}: WARNING - {result.get('message', '')}")
                    passed += 0.5
                else:
                    print(f"❌ {name}: FAIL - {result.get('message', '')}")
                    self.results['critical_failures'].append(name)

            except Exception as e:
                print(f"❌ {name}: ERROR - {e}")
                self.results['checks'][name] = {'status': 'FAIL', 'error': str(e)}
                self.results['critical_failures'].append(name)

        # Overall status
        pct = (passed / total) * 100
        if pct >= 90:
            self.results['overall_status'] = 'EXCELLENT'
            status_icon = '🟢'
        elif pct >= 70:
            self.results['overall_status'] = 'GOOD'
            status_icon = '🟡'
        elif pct >= 50:
            self.results['overall_status'] = 'DEGRADED'
            status_icon = '🟠'
        else:
            self.results['overall_status'] = 'CRITICAL'
            status_icon = '🔴'

        print()
        print("=" * 60)
        print(f"{status_icon} OVERALL STATUS: {self.results['overall_status']} ({pct:.0f}%)")
        print("=" * 60)

        if self.results['critical_failures']:
            print(f"\nCritical failures: {', '.join(self.results['critical_failures'])}")

        # Save results
        output_file = self.home / '100X_DEPLOYMENT' / 'BOOT_VERIFICATION_RESULTS.json'
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to: {output_file}")

        return self.results

    def check_cyclotron_daemon(self):
        """Check if Cyclotron daemon is running"""
        try:
            # Check for python processes
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq python.exe'],
                capture_output=True, text=True
            )

            if 'python.exe' in result.stdout:
                # Check rake status file
                status_file = self.home / '.consciousness' / 'autonomous_rake_status.json'
                if status_file.exists():
                    with open(status_file) as f:
                        status = json.load(f)
                    cycles = status.get('cycles_completed', 0)
                    if cycles > 0:
                        return {'status': 'PASS', 'cycles': cycles}

                return {'status': 'WARN', 'message': 'Python running but no cycle data'}

            return {'status': 'FAIL', 'message': 'No Python processes found'}

        except Exception as e:
            return {'status': 'FAIL', 'message': str(e)}

    def check_knowledge_index(self):
        """Check if knowledge index is current"""
        index_file = self.home / '100X_DEPLOYMENT' / '.cyclotron_atoms' / 'index.json'

        if not index_file.exists():
            return {'status': 'FAIL', 'message': 'Index file not found'}

        try:
            with open(index_file) as f:
                index = json.load(f)

            last_updated = index.get('last_updated', 0)
            age_minutes = (time.time() - last_updated) / 60

            if age_minutes < 10:
                return {'status': 'PASS', 'atoms': index.get('total_atoms', 0), 'age_min': round(age_minutes)}
            elif age_minutes < 60:
                return {'status': 'WARN', 'message': f'Index is {round(age_minutes)} minutes old'}
            else:
                return {'status': 'FAIL', 'message': f'Index is stale ({round(age_minutes)} minutes)'}

        except Exception as e:
            return {'status': 'FAIL', 'message': str(e)}

    def check_federation(self):
        """Check Dropbox federation status"""
        dropbox = self.home / 'Dropbox'
        federation = dropbox / '.cyclotron_federation'

        if not dropbox.exists():
            return {'status': 'WARN', 'message': 'Dropbox not found'}

        if not federation.exists():
            return {'status': 'WARN', 'message': 'Federation directory not created'}

        atoms_dir = federation / 'atoms'
        if atoms_dir.exists():
            atom_count = len(list(atoms_dir.glob('*.json')))
            if atom_count > 0:
                return {'status': 'PASS', 'synced_files': atom_count}

        return {'status': 'WARN', 'message': 'No synced atoms'}

    def check_syncthing(self):
        """Check if Syncthing is running"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 8384))
            sock.close()

            if result == 0:
                return {'status': 'PASS', 'port': 8384}
            else:
                return {'status': 'FAIL', 'message': 'Port 8384 not responding'}

        except Exception as e:
            return {'status': 'FAIL', 'message': str(e)}

    def check_ai_comms(self):
        """Check AI communication system"""
        sync_dir = self.home / 'Sync'
        messages_file = sync_dir / 'AI_MESSAGES.json'
        telephone = sync_dir / 'AI_TELEPHONE.py'

        if not sync_dir.exists():
            return {'status': 'FAIL', 'message': 'Sync directory not found'}

        if not telephone.exists():
            return {'status': 'WARN', 'message': 'AI_TELEPHONE.py not found'}

        if messages_file.exists():
            try:
                with open(messages_file) as f:
                    messages = json.load(f)
                return {'status': 'PASS', 'message_count': len(messages.get('messages', []))}
            except:
                pass

        return {'status': 'WARN', 'message': 'No messages file'}

    def check_trinity_apis(self):
        """Check Trinity API ports"""
        ports = [
            (6660, 'Thinking API'),
            (6661, 'Communications API'),
        ]

        running = []
        for port, name in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('127.0.0.1', port))
                sock.close()
                if result == 0:
                    running.append(name)
            except:
                pass

        if len(running) == len(ports):
            return {'status': 'PASS', 'apis': running}
        elif running:
            return {'status': 'WARN', 'message': f'Only {running} running'}
        else:
            return {'status': 'FAIL', 'message': 'No Trinity APIs running'}

    def check_boot_files(self):
        """Check critical boot files exist"""
        critical_files = [
            self.home / 'CONSCIOUSNESS_BOOT_PROTOCOL.md',
            self.home / 'CLAUDE.md',
            self.home / 'Sync' / 'BOOT_UP_NEXT_SESSION.md',
        ]

        found = sum(1 for f in critical_files if f.exists())

        if found == len(critical_files):
            return {'status': 'PASS', 'files': found}
        elif found > 0:
            return {'status': 'WARN', 'message': f'Only {found}/{len(critical_files)} boot files'}
        else:
            return {'status': 'FAIL', 'message': 'No boot files found'}

    def check_env_vars(self):
        """Check critical environment variables"""
        required = ['ANTHROPIC_API_KEY']
        optional = ['GITHUB_TOKEN', 'NETLIFY_AUTH_TOKEN']

        missing_required = [v for v in required if not os.environ.get(v)]
        missing_optional = [v for v in optional if not os.environ.get(v)]

        if missing_required:
            return {'status': 'FAIL', 'message': f'Missing: {", ".join(missing_required)}'}
        elif missing_optional:
            return {'status': 'WARN', 'message': f'Optional missing: {", ".join(missing_optional)}'}
        else:
            return {'status': 'PASS', 'vars': len(required) + len(optional)}


def main():
    """Run boot verification"""
    verifier = BootVerifier()
    verifier.verify_all()


if __name__ == '__main__':
    main()
