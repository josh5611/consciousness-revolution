@echo off
REM TRIPLE TRINITY ORCHESTRATOR
REM Runs on each PC to participate in coordinated execution

echo.
echo  ========================================
echo   TRIPLE TRINITY ORCHESTRATOR
echo  ========================================
echo.

REM Set computer ID
if "%COMPUTER_ID%"=="" (
    set /p COMPUTER_ID="Enter this computer's ID (PC1/PC2/PC3): "
)

cd %USERPROFILE%\100X_DEPLOYMENT

REM 1. Pull latest
echo [1/5] Syncing with git...
git pull

REM 2. Check for wake signals
echo [2/5] Checking wake signals...
python -c "
from pathlib import Path
import json
import os
pc = os.environ.get('COMPUTER_ID', 'PC1')
wake_file = Path.home() / '100X_DEPLOYMENT' / '.trinity' / 'wake_signals' / f'{pc}_wake.json'
if wake_file.exists():
    data = json.loads(wake_file.read_text())
    print(f'WAKE SIGNAL: {data.get(\"task\", \"No task specified\")}')
    wake_file.unlink()  # Clear signal
else:
    print('No wake signal - starting normally')
"

REM 3. Start daemon in background
echo [3/5] Starting coordination daemon...
start "Trinity Daemon %COMPUTER_ID%" cmd /k "set COMPUTER_ID=%COMPUTER_ID% && python .trinity\automation\CROSS_COMPUTER_DAEMON.py"

REM 4. Start credit monitor
echo [4/5] Starting credit monitor...
start "Credit Monitor %COMPUTER_ID%" cmd /k "set COMPUTER_ID=%COMPUTER_ID% && python .trinity\automation\CREDIT_EXHAUSTION_MONITOR.py"

REM 5. Show spawn queue
echo [5/5] Checking spawn queue...
echo.
python -c "
from pathlib import Path
import json
spawn = Path.home() / '100X_DEPLOYMENT' / '.trinity' / 'spawn_queue'
print('=== SPAWN QUEUE ===')
tasks = list(spawn.glob('*.json'))
for f in sorted(tasks, key=lambda x: json.loads(x.read_text()).get('priority', 'normal') == 'high', reverse=True):
    t = json.loads(f.read_text())
    priority = t.get('priority', 'normal')
    marker = '🔥' if priority == 'high' else '  '
    print(f'{marker} {t[\"id\"]} [{priority}]')
print(f'\nTotal: {len(tasks)} tasks')
"

echo.
echo ========================================
echo  %COMPUTER_ID% READY FOR TRIPLE TRINITY
echo ========================================
echo.
echo Systems running:
echo   - Coordination daemon (git sync, wake signals)
echo   - Credit monitor (auto-handoff when exhausted)
echo.
echo To start working:
echo   1. Open Claude Code
echo   2. Say: "Claim high priority task from spawn queue and execute"
echo.
echo When credits run low:
echo   - Monitor detects exhaustion
echo   - Automatic handoff to next PC
echo   - You'll see: "Handoff: PC1 → PC2"
echo.
pause
