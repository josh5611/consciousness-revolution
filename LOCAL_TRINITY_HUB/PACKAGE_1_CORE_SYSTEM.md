# PACKAGE 1: CORE SYSTEM
## Foundation Every Computer Needs

---

## WHAT THIS IS

This is the foundation layer. Without this, nothing else works.
Install this FIRST on any computer joining the network.

---

## CONTENTS

### 1. FOUNDATION (Mission/Vision/Values)
**File:** FOUNDATION.md

- Mission: Make 1M humans manipulation-immune
- Vision: 2035 target
- 5 Core Values
- 90-day Rocks
- Scorecard

### 2. UNIVERSAL FILE STRUCTURE
**File:** UNIVERSAL_FILE_STRUCTURE.md

```
~/LOCAL_TRINITY_HUB/
├── terminal_reports/
├── consolidated/
├── outbound/
├── inbound/
├── capabilities/
├── archives/
├── logs/
├── boot_state/
├── session_state/
├── protocols/
├── commands/
├── api_keys/
└── emergency/
```

**SAME ON EVERY COMPUTER. No exceptions.**

### 3. HUB PROTOCOL
**File:** HUB_PROTOCOL.md

- Where to save reports
- How consolidation works
- Git gatekeeper rules

### 4. REPORT STANDARD
**File:** HUB_REPORT_STANDARD.md

Three report types:
- BOOT (session start)
- WORKING (during session)
- HANDOFF (session end)

Same JSON format everywhere.

### 5. FRACTAL STRUCTURE
**File:** FRACTAL_STRUCTURE.md

- Every folder has _BOOTSTRAP.json
- Same 7 fields at every level
- Infinite zoom depth

### 6. FILE NAMING
**File:** FILE_NAMING_SYSTEM.md

Format: `DATE_COMPUTER_INSTANCE_DOMAIN_TYPE_PROJECT_VERSION.ext`

---

## INSTALLATION

### Step 1: Create folder structure
```bash
mkdir -p ~/LOCAL_TRINITY_HUB/{terminal_reports,consolidated,outbound,inbound,capabilities,archives,logs,boot_state,session_state,protocols,commands,api_keys,emergency}
```

### Step 2: Copy core docs
```bash
git clone https://github.com/overkillkulture/consciousness-revolution.git
cp -r consciousness-revolution/LOCAL_TRINITY_HUB/protocols ~/LOCAL_TRINITY_HUB/
cp consciousness-revolution/LOCAL_TRINITY_HUB/FOUNDATION.md ~/LOCAL_TRINITY_HUB/
cp consciousness-revolution/LOCAL_TRINITY_HUB/_BOOTSTRAP.json ~/LOCAL_TRINITY_HUB/
```

### Step 3: Create root bootstrap
```bash
# Edit _BOOTSTRAP.json with this computer's info
```

### Step 4: Verify
```bash
ls ~/LOCAL_TRINITY_HUB/
# Should see 13 folders + core docs
```

---

## GAPS IN THIS PACKAGE

- [ ] Computer-specific _BOOTSTRAP.json template
- [ ] Automated installation script
- [ ] Verification checklist

---

## RECURSIVE LEARNING HOOK

After installing, update:
1. FOUNDATION.md if mission clarity needed
2. UNIVERSAL_FILE_STRUCTURE.md if folders wrong
3. HUB_REPORT_STANDARD.md if format insufficient

**Every use improves the package.**
