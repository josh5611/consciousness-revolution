@echo off
echo ========================================
echo CONSCIOUSNESS REVOLUTION - AUTO BOOT
echo ========================================
echo.

cd /d "%USERPROFILE%\100X_DEPLOYMENT"

echo Starting full system boot...
python CONSCIOUSNESS_BOOT.py full

echo.
echo Boot complete. Starting scheduler daemon...
python CONSCIOUSNESS_BOOT.py scheduler

echo.
echo ========================================
echo System is now running autonomously
echo ========================================
echo.
echo Quick commands:
echo   python UNIFIED_MONITORING.py dashboard
echo   python AUTONOMOUS_TASK_RUNNER.py status
echo   python SELF_HEALING_SYSTEM.py auto
echo.
pause
