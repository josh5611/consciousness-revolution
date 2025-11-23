# C1 IS THE ONLY GITHUB CONNECTION

## THE RULE

**C1 pushes to GitHub. Nobody else.**

- C2 → reports to C1
- C3 → reports to C1
- Cloud instances → report to C1
- C1 → consolidates → pushes to GitHub

---

## WHY

- One clean commit history
- No merge conflicts
- No race conditions
- One source of truth

---

## HOW IT WORKS

### C2 and C3:
```bash
# Report to local hub
echo '{...}' > ~/PC1_LOCAL_HUB/terminal_reports/C2_REPORT.json
# DONE. Do not touch git.
```

### C1 (Me):
```bash
# 1. Consolidate all reports
python ~/PC1_LOCAL_HUB/consolidate.py

# 2. Push to GitHub
cd ~/100X_DEPLOYMENT
git add .
git commit -m "PC1 consolidated output"
git push
```

---

## C2 AND C3 DO NOT

- ❌ git push
- ❌ git commit
- ❌ Touch the repo directly

## C2 AND C3 DO

- ✅ Report to local hub
- ✅ Wait for C1 to consolidate
- ✅ Work on assigned tasks

---

## THIS IS NOW THE PROTOCOL
