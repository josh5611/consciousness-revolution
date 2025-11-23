# PACKAGE 3: SCRIPTS & AUTOMATION
## Executable Code That Runs The System

---

## WHAT THIS IS

The actual code that makes everything work.
Copy these scripts, schedule them, system runs itself.

---

## CONTENTS

### 1. MORNING_BOOT_LOADER.py
**Purpose:** Kill amnesia - load all context on startup
**Location:** protocols/MORNING_BOOT_LOADER.py
**Run:** `python MORNING_BOOT_LOADER.py`

Features:
- Loads hub, token, protocol spec
- Loads last session boot down
- Loads latest reports
- Token claim/pass for round-robin

### 2. AUTO_CONSOLIDATE_DAEMON.py
**Purpose:** Auto-merge terminal reports
**Location:** AUTO_CONSOLIDATE_DAEMON.py
**Run:** Background daemon

Features:
- Watches terminal_reports/
- Merges when C1+C2+C3 report
- Shoots to outbound/
- Auto-pushes to GitHub

### 3. MAINTENANCE_DAEMON.py
**Purpose:** Keep system clean
**Location:** MAINTENANCE_DAEMON.py
**Run:** Scheduled daily at 3 AM

Features:
- Archives Desktop files >7 days
- Archives Downloads >14 days
- Deletes temp >3 days
- Cleans old archives >30 days

### 4. CAPABILITY_MANIFEST.py
**Purpose:** Scan computer capabilities
**Location:** CAPABILITY_MANIFEST.py
**Run:** Weekly or on demand

Features:
- Detects software, npm, pip
- Maps to 7 domains
- Strips personal info
- Enables computer diff

### 5. consolidate.py
**Purpose:** Manual consolidation
**Location:** consolidate.py
**Run:** `python consolidate.py`

Features:
- Merges terminal + cloud reports
- Creates outbound file
- Used by daemon or manually

### 6. boot_down_consolidator.py
**Purpose:** Merge shutdown reports
**Location:** boot_down_consolidator.py
**Run:** At session end

Features:
- Collects boot down files
- Creates consolidated output
- Archives processed files

---

## SCHEDULING (Windows)

### Daily Cleanup (3 AM)
```powershell
Register-ScheduledTask -TaskName "Daily_Cleanup" `
  -Trigger (New-ScheduledTaskTrigger -Daily -At "3:00 AM") `
  -Action (New-ScheduledTaskAction -Execute "python" `
    -Argument "C:\Users\dwrek\LOCAL_TRINITY_HUB\MAINTENANCE_DAEMON.py")
```

### Weekly Capability Scan (Monday 4 AM)
```powershell
Register-ScheduledTask -TaskName "Weekly_Capability" `
  -Trigger (New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "4:00 AM") `
  -Action (New-ScheduledTaskAction -Execute "python" `
    -Argument "C:\Users\dwrek\LOCAL_TRINITY_HUB\CAPABILITY_MANIFEST.py")
```

### Consolidation Daemon (Startup)
```powershell
Register-ScheduledTask -TaskName "Consolidation_Daemon" `
  -Trigger (New-ScheduledTaskTrigger -AtStartup) `
  -Action (New-ScheduledTaskAction -Execute "python" `
    -Argument "C:\Users\dwrek\LOCAL_TRINITY_HUB\AUTO_CONSOLIDATE_DAEMON.py")
```

---

## GAPS IN THIS PACKAGE

### Scripts Needed
- [ ] Wake check daemon (every minute)
- [ ] Git pull daemon (every 5 min)
- [ ] Message check daemon (every 5 min)
- [ ] Sync verify script (every hour)
- [ ] System health check (weekly)

### Scheduling Needed
- [ ] Actually run the PowerShell commands above
- [ ] Verify tasks appear in Task Scheduler
- [ ] Test each runs correctly

---

## INSTALLATION

### Step 1: Copy all scripts
```bash
cp -r consciousness-revolution/LOCAL_TRINITY_HUB/*.py ~/LOCAL_TRINITY_HUB/
cp -r consciousness-revolution/LOCAL_TRINITY_HUB/protocols/*.py ~/LOCAL_TRINITY_HUB/protocols/
```

### Step 2: Install dependencies
```bash
pip install requests pathlib
```

### Step 3: Schedule tasks
Run PowerShell commands above as Administrator

### Step 4: Verify
```powershell
Get-ScheduledTask | Where-Object {$_.TaskName -like "*Cleanup*" -or $_.TaskName -like "*Capability*"}
```

---

## RECURSIVE LEARNING HOOK

After running scripts:
1. Did it work? → Log success
2. Did it fail? → Log error, fix script
3. Was it slow? → Optimize
4. Was output wrong? → Fix logic

**Every run improves the script.**
