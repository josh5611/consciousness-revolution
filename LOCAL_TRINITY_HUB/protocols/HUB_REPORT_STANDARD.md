# HUB REPORT STANDARD

## THE RULE
Every terminal reports to hub in the **exact same format**.
Two report types: BOOT and WORKING.

---

## REPORT TYPE 1: BOOT REPORT
**When:** First message of session, just woke up

```json
{
  "type": "BOOT",
  "instance": "C1",
  "computer": "DWREKSCPU",
  "timestamp": "2025-11-23T08:00:00Z",

  "context_loaded": {
    "morning_boot": true,
    "last_session": "2025-11-22",
    "hub_connected": true,
    "git_synced": true
  },

  "work_area": {
    "understanding": "Building cross-computer communication system",
    "my_role": "C1 Mechanic - infrastructure and execution",
    "active_project": "LOCAL_TRINITY_HUB standardization"
  },

  "ready_status": {
    "tools_available": ["git", "python", "mcp", "bash"],
    "blockers": [],
    "ready": true
  },

  "grabbing_next": "Check task queue for assigned work"
}
```

**Required fields:**
- type: "BOOT"
- instance: Your ID
- computer: Machine name
- context_loaded: Did morning boot work?
- work_area: What do you understand is happening?
- ready_status: Are you ready to work?
- grabbing_next: What will you do first?

---

## REPORT TYPE 2: WORKING REPORT
**When:** During session, reporting progress

```json
{
  "type": "WORKING",
  "instance": "C1",
  "computer": "DWREKSCPU",
  "timestamp": "2025-11-23T09:30:00Z",

  "completed": [
    "Created LOCAL_TRINITY_HUB structure",
    "Tested morning boot loader",
    "Pushed to GitHub"
  ],

  "in_progress": {
    "task": "Integrating C2 round-robin system",
    "started": "2025-11-23T09:00:00Z",
    "percent": 75,
    "notes": "Token passing works, need to test epoch rotation"
  },

  "blockers": [],

  "discoveries": [
    "C2's morning boot loader solves amnesia problem",
    "Need same folder structure on all computers"
  ],

  "questions": [],

  "grabbing_next": "Configure Syncthing sync after current task"
}
```

**Required fields:**
- type: "WORKING"
- instance, computer, timestamp
- completed: List of done items
- in_progress: Current task with details
- blockers: What's stopping you?
- discoveries: What did you learn?
- grabbing_next: What's after current task?

---

## REPORT TYPE 3: HANDOFF REPORT
**When:** End of session, booting down

```json
{
  "type": "HANDOFF",
  "instance": "C1",
  "computer": "DWREKSCPU",
  "timestamp": "2025-11-23T17:00:00Z",

  "session_summary": {
    "duration": "8 hours",
    "tasks_completed": 5,
    "tasks_started": 1
  },

  "completed": [
    "LOCAL_TRINITY_HUB finalized",
    "Universal file structure",
    "Morning boot integration"
  ],

  "incomplete": {
    "task": "Syncthing configuration",
    "status": "Waiting for C2/C3 to create folders",
    "next_steps": ["Verify folders exist", "Configure sync targets", "Test sync"]
  },

  "state_saved": {
    "location": "~/LOCAL_TRINITY_HUB/session_state/",
    "files": ["current_task.json", "context.json"]
  },

  "for_next_session": [
    "Check if C2/C3 created folders",
    "Complete Syncthing config",
    "Test cross-computer sync"
  ]
}
```

---

## WHERE TO SAVE REPORTS

```
~/LOCAL_TRINITY_HUB/terminal_reports/C1_REPORT.json
~/LOCAL_TRINITY_HUB/terminal_reports/C2_REPORT.json
~/LOCAL_TRINITY_HUB/terminal_reports/C3_REPORT.json
```

**Overwrite each time** - we only need current status.
For history, the consolidator archives old reports.

---

## REPORT FREQUENCY

| Event | Report Type |
|-------|-------------|
| Session start | BOOT |
| Every 30 min of work | WORKING |
| Task completed | WORKING |
| Hit a blocker | WORKING |
| Session end | HANDOFF |

---

## CONSOLIDATION

When all 3 terminals report:
1. AUTO_CONSOLIDATE_DAEMON detects
2. Merges into single consolidated report
3. Shoots to outbound/
4. Pushes to GitHub

---

## SLASH COMMAND (Future)

```
/report-hub
```

Should auto-generate the report based on:
- Current context
- Recent git activity
- Task queue status
- Time since last report

---

## EXAMPLES

### First Boot of Day
```json
{
  "type": "BOOT",
  "instance": "C2",
  "computer": "DESKTOP-MSMCFH2",
  "timestamp": "2025-11-23T08:00:00Z",
  "context_loaded": {
    "morning_boot": true,
    "last_session": "2025-11-22",
    "hub_connected": true,
    "git_synced": true
  },
  "work_area": {
    "understanding": "Building cyclotron round-robin system",
    "my_role": "C2 Architect - design and architecture",
    "active_project": "Persistent memory and token passing"
  },
  "ready_status": {
    "tools_available": ["git", "python", "mcp"],
    "blockers": [],
    "ready": true
  },
  "grabbing_next": "Continue round-robin token system"
}
```

### Mid-Session Progress
```json
{
  "type": "WORKING",
  "instance": "C3",
  "computer": "DESKTOP-S72LRRO",
  "timestamp": "2025-11-23T10:30:00Z",
  "completed": [
    "Created PC3_LOCAL_HUB",
    "Copied protocols from PC1"
  ],
  "in_progress": {
    "task": "Generating capability manifest",
    "started": "2025-11-23T10:15:00Z",
    "percent": 50,
    "notes": "Scanning installed software"
  },
  "blockers": [],
  "discoveries": [
    "PC3 has different Python version than PC1"
  ],
  "questions": [],
  "grabbing_next": "Test 5 communication routes"
}
```

---

## THE POINT

With standard reports:
1. **Commander sees everything** - one glance at consolidated report
2. **Terminals know what others are doing** - no duplicate work
3. **Handoffs work** - next session knows exactly where to start
4. **Automation possible** - consistent format = parseable

**Same shape. Every time. Every computer.**
