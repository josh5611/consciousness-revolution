# UNIVERSAL CLEANUP PROTOCOL

**Same protocol. Every computer. Every folder.**

---

## CLEANUP SCHEDULE

| Frequency | What | Action |
|-----------|------|--------|
| Daily | Desktop | Archive files > 3 days |
| Daily | Downloads | Archive files > 7 days |
| Daily | Temp | Delete files > 1 day |
| Weekly | Git branches | Delete merged |
| Weekly | Logs | Archive > 7 days |
| Weekly | Boot down archive | Keep last 10 |
| Monthly | Old archives | Delete > 30 days |
| Monthly | Remote git branches | Prune |

---

## FOLDER-SPECIFIC RULES

### Desktop
- Max items: 20
- Archive after: 3 days
- Never delete: Shortcuts, .lnk files

### Downloads
- Max items: 50
- Archive after: 7 days
- Auto-sort by type into subfolders

### Logs
- Keep: Last 7 days
- Archive: Days 8-30
- Delete: > 30 days

### Boot Down Archive
- Keep: Last 10 files
- Archive: 11-30
- Delete: > 30

### Terminal Reports
- Keep: Last 24 hours
- Archive: Older (into consolidated)
- Delete: After consolidation

### Git Branches
- Delete: Merged branches immediately
- Review: Branches > 14 days
- Delete: Branches > 30 days (unless protected)

---

## THE CLEANUP DAEMON

Runs daily at 3 AM:

```python
#!/usr/bin/env python3
"""Universal cleanup daemon"""

import schedule
import time

def daily_cleanup():
    # Desktop
    clean_folder("Desktop", max_age_days=3)

    # Downloads
    clean_folder("Downloads", max_age_days=7)

    # Temp
    clean_folder("Temp", max_age_days=1, delete=True)

    # Terminal reports
    consolidate_and_clean("terminal_reports")

def weekly_cleanup():
    # Git branches
    cleanup_git_branches()

    # Logs
    archive_logs()

    # Boot downs
    trim_boot_down_archive(keep=10)

def monthly_cleanup():
    # Old archives
    delete_old_archives(max_age_days=30)

    # Remote git
    prune_remote_branches()

# Schedule
schedule.every().day.at("03:00").do(daily_cleanup)
schedule.every().monday.at("03:30").do(weekly_cleanup)
schedule.every(1).months.do(monthly_cleanup)

while True:
    schedule.run_pending()
    time.sleep(3600)
```

---

## MANUAL CLEANUP COMMANDS

### Quick Desktop Cleanup
```bash
python ~/PC1_LOCAL_HUB/MAINTENANCE_DAEMON.py
```

### Git Branch Cleanup
```bash
cd ~/100X_DEPLOYMENT
git branch --merged master | grep -v master | xargs git branch -d
git fetch --prune
```

### Archive Everything Old
```bash
find ~ -maxdepth 2 -type f -mtime +30 -exec mv {} ~/AUTO_ARCHIVE/ \;
```

---

## FILE RETENTION POLICY

| Type | Keep Active | Archive | Delete |
|------|-------------|---------|--------|
| Code | Forever | N/A | Never |
| Reports | 7 days | 30 days | 90 days |
| Logs | 7 days | 30 days | 90 days |
| Boot downs | 10 files | 30 files | Older |
| Temp | 1 day | N/A | Immediate |
| Downloads | 7 days | 30 days | 90 days |

---

## SAME ON ALL COMPUTERS

PC1, PC2, PC3 all use:
- Same cleanup daemon
- Same schedule
- Same retention policy
- Same folder structure
- Same file naming

**Copy MAINTENANCE_DAEMON.py to each computer.**

---

## VERIFY CLEANUP WORKING

```bash
# Check auto-archive size
du -sh ~/AUTO_ARCHIVE/

# Check desktop count
ls ~/Desktop | wc -l

# Check downloads count
ls ~/Downloads | wc -l

# Check git branches
git branch | wc -l
```

---

## ALERTS

If any folder exceeds limits:
- Desktop > 50 items → Alert
- Downloads > 100 items → Alert
- Git branches > 20 → Alert
- Archive > 5GB → Alert

---

## THIS PREVENTS CHAOS

- No more cluttered desktops
- No more 500 branches
- No more endless downloads
- Same shape everywhere
- Automated, not manual
