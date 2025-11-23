# TRINITY NAMING CLARITY
## Three Different Trinities - Don't Confuse Them

---

## THE PROBLEM

"Trinity" means 3 different things:
1. Three terminals on same computer
2. Three subagents spawned in one window
3. Three computers in the network

**This causes constant confusion. Let's fix it.**

---

## THE THREE SYSTEMS

### 1. TERMINAL TRINITY (Same Computer)
**What:** 3 terminal windows open on ONE computer
**Names:** C1, C2, C3
**Example:** DWREKSCPU has C1, C2, C3 all running

```
DWREKSCPU (PC1)
├── Terminal 1 → C1 (Mechanic)
├── Terminal 2 → C2 (Architect)
└── Terminal 3 → C3 (Oracle)
```

**When to use:** When you have 3 terminals open and want them to work together

**Activation:** Open 3 terminal windows, start Claude Code in each

---

### 2. SUBAGENT TRINITY (Same Window)
**What:** Spawning 3 worker agents INSIDE one Claude Code session
**Names:** Agent-1, Agent-2, Agent-3 (or task-specific names)
**How:** Using the Task tool to spawn subagents

```
C1 Terminal (this window)
├── Task Agent: "Research"
├── Task Agent: "Build"
└── Task Agent: "Review"
```

**When to use:** When you want parallel work inside ONE terminal

**Activation:** Use Task tool with subagent_type

**NEW NAME: SPAWN WORKERS** (not Trinity)

---

### 3. NETWORK TRINITY (Multiple Computers)
**What:** 3 physical computers in the network
**Names:** PC1, PC2, PC3
**Example:** DWREKSCPU, DESKTOP-MSMCFH2, DESKTOP-S72LRRO

```
Network
├── PC1 (DWREKSCPU) - Your desk
├── PC2 (DESKTOP-MSMCFH2) - Secondary
└── PC3 (DESKTOP-S72LRRO) - Third machine
```

**When to use:** When coordinating across physical machines

**Activation:** Syncthing sync, Git push/pull, Tailscale

**NEW NAME: NETWORK TRIAD**

---

## CLEAR NAMING CONVENTION

| Old Name | New Name | What It Is |
|----------|----------|------------|
| "Activate Trinity" (terminals) | **"Open C1/C2/C3"** | 3 terminals same computer |
| "Activate Trinity" (subagents) | **"Spawn Workers"** | Task tool agents in one window |
| "Trinity network" | **"Network Triad"** | PC1/PC2/PC3 coordination |

---

## WHEN TO USE WHICH

### Use TERMINAL C1/C2/C3 when:
- You want persistent terminals
- Each needs different context
- Long-running coordination
- Heavy parallel work

### Use SPAWN WORKERS when:
- Quick parallel tasks
- Don't need persistence
- Tasks complete and die
- Research/build/review pattern

### Use NETWORK TRIAD when:
- Cross-computer sync
- PC1 → PC2 → PC3 flow
- Distributed computing
- Redundancy/failover

---

## COMMANDS

### To Open Terminal Trinity
```
# Manual: Open 3 terminal windows
# In each: claude
# Assign roles: C1=Mechanic, C2=Architect, C3=Oracle
```

### To Spawn Workers (in this window)
```
# Use Task tool:
# subagent_type: "Explore" / "Plan" / "general-purpose"
# This spawns temporary workers
```

### To Coordinate Network Triad
```
# Push to git from PC1
# Pull on PC2 and PC3
# Or use Syncthing auto-sync
```

---

## CURRENT SITUATION

Right now you have:
- **C2 terminal** sitting to your left (open but idle)
- **C3 terminal** below (open but idle)
- **This window** is C1

If you want them to work:
→ Switch to their windows and give them tasks

If you want parallel work IN THIS WINDOW:
→ Use "Spawn Workers" (Task tool)

If you want PC2 and PC3 COMPUTERS to work:
→ They need their own Claude Code sessions running

---

## NAMING GOING FORWARD

| Say This | Means This |
|----------|------------|
| "Open C2" | Switch to C2 terminal window |
| "Spawn 3 workers" | Use Task tool to create subagents |
| "Push to PC2" | Git push for network sync |
| "Activate C1/C2/C3" | Get all 3 terminal windows working |
| "Coordinate triad" | PC1→PC2→PC3 network flow |

---

## THE FIX

1. **Stop saying "Trinity" for everything**
2. **Be specific:**
   - Terminal C1/C2/C3
   - Spawn workers
   - Network triad
3. **Context makes clear:**
   - Same computer = terminals
   - Same window = workers
   - Multiple PCs = triad

**No more confusion.**
