# PACKAGE 2: OPERATIONS
## How To Work Daily

---

## WHAT THIS IS

Daily operations - boot up, work, boot down, maintain.
This is the rhythm of the system.

---

## CONTENTS

### 1. BOOT UP (3 Phases)
**File:** RECURSIVE_LEARNING_SYSTEM.md (Section: 3-Phase Boot Up)

**Phase 1: WAKE**
- Run MORNING_BOOT_LOADER.py
- Load last session state
- Load task queue

**Phase 2: ORIENT**
- Read hub reports
- Check urgent messages
- Identify your role

**Phase 3: ENGAGE**
- Claim task
- Report BOOT status
- Start working

### 2. WORKING
**File:** MASTER_PROTOCOL_REGISTRY.md (Phase 2)

- Task claim protocol
- Progress reports every 30 min
- Discovery logging
- Blocker alerts
- Commit protocol

### 3. BOOT DOWN (3 Phases)
**File:** RECURSIVE_LEARNING_SYSTEM.md (Section: 3-Phase Boot Down)

**Phase 1: CAPTURE**
- Document completed work
- Document in-progress
- Save context

**Phase 2: TEACH**
- What would I tell myself tomorrow?
- Update _BOOTSTRAP.json files

**Phase 3: IMPROVE**
- Did any protocol fail? Fix it
- Push all updates

### 4. MAINTENANCE SCHEDULE
**File:** MASTER_PROTOCOL_REGISTRY.md (Phase 6)

| Frequency | Tasks |
|-----------|-------|
| Every minute | Wake check, heartbeat |
| Every 5 min | Git pull, message check |
| Every 30 min | Progress report |
| Every hour | Consolidation check |
| Daily 3AM | Desktop/Downloads cleanup |
| Weekly | Capability manifest, health check |
| Monthly | Full cleanup, API rotation |

### 5. LEARNING LOOPS
**File:** RECURSIVE_LEARNING_SYSTEM.md

Four loops:
1. Task learning
2. Session learning
3. Cross-computer learning
4. Protocol learning

---

## QUICK REFERENCE

### Morning Start
```bash
python ~/LOCAL_TRINITY_HUB/protocols/MORNING_BOOT_LOADER.py
# Then report BOOT to hub
```

### During Work
```bash
# Every 30 min or on completion:
# Update ~/LOCAL_TRINITY_HUB/terminal_reports/C1_REPORT.json
```

### Evening End
```bash
# 1. Report HANDOFF to hub
# 2. Save state to session_state/
# 3. Update any _BOOTSTRAP.json that changed
# 4. git push
```

---

## GAPS IN THIS PACKAGE

- [ ] Automated boot sequence script
- [ ] 30-min reminder daemon
- [ ] Handoff automation
- [ ] Learning database structure

---

## RECURSIVE LEARNING HOOK

After each session, ask:
1. Did boot up work smoothly?
2. Did reporting flow naturally?
3. Did boot down capture everything?
4. What friction did I hit?

**Update protocols with answers.**
