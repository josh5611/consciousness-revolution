# GIT BRANCH CLEANUP PROTOCOL

## THE PROBLEM

Branches accumulate:
- feature-x
- test-something
- fix-bug
- old-experiment

Eventually: 500 branches, chaos.

---

## BRANCH NAMING (7 DIMENSIONS)

```
[date]-[computer]-[type]-[domain]-[description]
```

### Examples:
```
20251123-pc1-feature-infrastructure-local-hub
20251123-pc2-fix-pattern-boot-protocol
20251123-pc1-test-business-stripe-api
```

---

## BRANCH TYPES

- `feature` - New functionality
- `fix` - Bug fix
- `test` - Experimental
- `hotfix` - Urgent production fix
- `release` - Version release

---

## CLEANUP SCHEDULE

### Daily
```bash
# List merged branches
git branch --merged master

# Delete merged branches (except master/main)
git branch --merged master | grep -v "master\|main" | xargs git branch -d
```

### Weekly
```bash
# List branches older than 7 days
git for-each-ref --sort=committerdate refs/heads/ --format='%(committerdate:short) %(refname:short)'

# Delete stale branches (manually review first)
git branch -d old-branch-name
```

### Monthly
```bash
# Prune remote tracking branches
git fetch --prune

# List ALL branches
git branch -a

# Delete old remote branches
git push origin --delete old-branch-name
```

---

## AUTOMATED CLEANUP SCRIPT

```python
#!/usr/bin/env python3
"""Git branch cleanup"""

import subprocess
from datetime import datetime, timedelta

def get_branches():
    """Get all local branches with dates"""
    result = subprocess.run(
        ['git', 'for-each-ref', '--sort=committerdate',
         'refs/heads/', '--format=%(committerdate:short) %(refname:short)'],
        capture_output=True, text=True
    )
    branches = []
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split(' ', 1)
            date_str = parts[0]
            branch = parts[1] if len(parts) > 1 else ''
            branches.append((date_str, branch))
    return branches

def cleanup_merged():
    """Delete merged branches"""
    result = subprocess.run(
        ['git', 'branch', '--merged', 'master'],
        capture_output=True, text=True
    )
    for branch in result.stdout.strip().split('\n'):
        branch = branch.strip()
        if branch and branch not in ['master', 'main', '* master', '* main']:
            print(f"Deleting merged: {branch}")
            subprocess.run(['git', 'branch', '-d', branch])

def cleanup_old(days=30):
    """List branches older than X days"""
    cutoff = datetime.now() - timedelta(days=days)
    branches = get_branches()

    print(f"\nBranches older than {days} days:")
    for date_str, branch in branches:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            if date < cutoff:
                print(f"  {date_str} - {branch}")
        except:
            pass

if __name__ == "__main__":
    print("=== Git Branch Cleanup ===\n")
    cleanup_merged()
    cleanup_old(30)
    print("\n✅ Cleanup complete")
```

---

## PROTECTION

### Never Delete:
- master
- main
- production
- release-*

### Always Delete:
- Merged branches
- Branches > 90 days with no activity
- Test branches after testing complete

---

## RUN WEEKLY

Add to maintenance daemon:
```bash
cd ~/100X_DEPLOYMENT
python ~/PC1_LOCAL_HUB/git_branch_cleanup.py
```
