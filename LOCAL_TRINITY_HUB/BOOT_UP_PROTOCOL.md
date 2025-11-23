# BOOT UP PROTOCOL

**Read this first. Every session.**

---

## STEP 1: WHO ARE YOU

- **Computer**: PC1
- **Instance**: C1 (or C2, C3)
- **Role**: C1 = GitHub Gatekeeper, C2/C3 = Builders

---

## STEP 2: CHECK LAST BOOT DOWN

```bash
# Read last boot down
cat $(ls -t ~/PC1_LOCAL_HUB/boot_down_archive/*.md | head -1)
```

This tells you:
- What was being worked on
- State to restore
- Priorities
- Blockers

---

## STEP 3: CHECK FOR MESSAGES

```bash
# Local hub reports
ls ~/PC1_LOCAL_HUB/terminal_reports/

# Syncthing messages
ls ~/Sync/
```

---

## STEP 4: SEND HEARTBEAT

```bash
echo '{
  "instance": "C1",
  "status": "online",
  "timestamp": "'$(date -Iseconds)'"
}' > ~/PC1_LOCAL_HUB/terminal_reports/C1_HEARTBEAT.json
```

---

## WHERE EVERYTHING LIVES

### Local Hub
`~/PC1_LOCAL_HUB/`

### Reports Go Here
`~/PC1_LOCAL_HUB/terminal_reports/`

### Boot Downs Go Here
`~/PC1_LOCAL_HUB/boot_down_inputs/`

### Boot Down Archives
`~/PC1_LOCAL_HUB/boot_down_archive/`

### Git Repo
`~/100X_DEPLOYMENT/`

### Syncthing
`~/Sync/`

---

## THE SHAPE

```
REPORTING:
C1, C2, C3 ──► LOCAL HUB ──► consolidate.py ──► ONE OUTPUT

BOOT DOWN:
C1, C2, C3 ──► boot_down_inputs/ ──► boot_down_consolidator.py ──► ONE FILE

GITHUB:
Only C1 pushes. C2/C3 report to hub.
```

---

## IF CONFUSED

1. Read `~/PC1_LOCAL_HUB/BOOT_FIRST.md`
2. Read `~/PC1_LOCAL_HUB/HUB_PROTOCOL.md`
3. Check last boot down
4. Report to hub asking for clarification

---

## DO NOT

- ❌ Search for "hub", "trinity", "communications"
- ❌ Push to GitHub (unless you're C1)
- ❌ Create new folders or protocols
- ❌ Report anywhere except the local hub

---

## DO

- ✅ Read this protocol
- ✅ Check last boot down
- ✅ Report to local hub
- ✅ Follow the funnel shape
