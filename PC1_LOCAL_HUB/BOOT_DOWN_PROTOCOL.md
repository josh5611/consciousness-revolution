# BOOT DOWN PROTOCOL

**Same funnel. Same shape. Every time.**

---

## WHEN SESSION ENDS

Each instance (C1, C2, C3, Cloud, Desktop) writes boot down to:

```
~/PC1_LOCAL_HUB/boot_down_inputs/
```

---

## BOOT DOWN FORMAT

```bash
echo '{
  "instance": "C1",
  "timestamp": "'$(date -Iseconds)'",
  "work_completed": "what you finished",
  "work_in_progress": "what was interrupted",
  "state": "important state to preserve",
  "next_priorities": "what should happen next",
  "blockers": "any issues"
}' > ~/PC1_LOCAL_HUB/boot_down_inputs/C1_BOOT_DOWN.json
```

**Replace C1 with your instance (C1, C2, C3, Cloud, Desktop)**

---

## CONSOLIDATION

After all instances submit boot downs:

```bash
python ~/PC1_LOCAL_HUB/boot_down_consolidator.py
```

This creates:
- `boot_down_archive/BOOT_DOWN_[DATE].json`
- `boot_down_archive/BOOT_DOWN_[DATE].md`

---

## THE FLOW

```
C1 boot down ──┐
C2 boot down ──┼──► boot_down_inputs/ ──► consolidator ──► ONE FILE
C3 boot down ──┘
Cloud ─────────┘
Desktop ───────┘
```

**Same funnel as reporting. Same shape.**

---

## CROSS-COMPUTER

Eventually:
- PC1 outputs ONE boot down
- PC2 outputs ONE boot down
- PC3 outputs ONE boot down
- All 3 merge into MASTER boot down

---

## WHERE THINGS LIVE

### Boot Down Inputs
`~/PC1_LOCAL_HUB/boot_down_inputs/`

### Boot Down Archives
`~/PC1_LOCAL_HUB/boot_down_archive/`

### Latest Boot Down
```bash
ls -t ~/PC1_LOCAL_HUB/boot_down_archive/*.md | head -1
```

---

## BOOT UP REFERENCES THIS

When you boot up, check:
```bash
# Last boot down
cat $(ls -t ~/PC1_LOCAL_HUB/boot_down_archive/*.md | head -1)
```

This tells you:
- What was being worked on
- What state to restore
- What priorities exist
- What blockers remain
