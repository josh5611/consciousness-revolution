# THE 5 COMMUNICATION ROUTES
## How Computers Talk To Each Other

---

## ROUTE 1: LOCAL HUB FILES
**Type:** File-based, same computer
**Speed:** Instant
**Use:** C1/C2/C3 on same PC

```
C1 writes → ~/LOCAL_TRINITY_HUB/terminal_reports/C1_REPORT.json
C2 reads → ~/LOCAL_TRINITY_HUB/terminal_reports/C1_REPORT.json
```

**When:** Always. Primary route for same-computer coordination.

---

## ROUTE 2: GIT (GitHub)
**Type:** Version control sync
**Speed:** Minutes (push/pull cycle)
**Use:** Cross-computer, persistent

```
PC1 pushes → github.com/overkillkulture/consciousness-revolution
PC2 pulls ← github.com/overkillkulture/consciousness-revolution
```

**When:**
- Sharing code/protocols
- Permanent record needed
- C1 gatekeeper pushes consolidated output

---

## ROUTE 3: SYNCTHING
**Type:** Real-time file sync
**Speed:** Seconds
**Use:** Cross-computer, auto-sync

```
PC1 ~/LOCAL_TRINITY_HUB/outbound/ → syncs to → PC2 ~/LOCAL_TRINITY_HUB/inbound/
```

**Folders to sync:**
- protocols/ (same everywhere)
- session_state/ (shared state)
- outbound/ → inbound/ (cross-computer)

**When:** Continuous. Background sync for hot data.

---

## ROUTE 4: TRINITY MCP TOOLS
**Type:** Message passing
**Speed:** Instant
**Use:** Direct communication

```python
# Broadcast to all
mcp__trinity__trinity_broadcast(message="Status update", from="C1")

# Direct message
mcp__trinity__trinity_send_message(to="C2", message="Your turn", from="C1")

# Receive messages
mcp__trinity__trinity_receive_messages(instanceId="C1")
```

**When:**
- Urgent coordination
- Task assignment
- Status updates

---

## ROUTE 5: TAILSCALE (Network Mesh)
**Type:** Direct IP connection
**Speed:** Instant
**Use:** When other routes fail

**IPs:**
- PC1: 100.70.208.75
- PC2: 100.85.71.74
- PC3: 100.101.209.1

```bash
# Test connection
ping 100.85.71.74

# SSH if needed
ssh user@100.85.71.74

# File transfer
scp file.txt user@100.85.71.74:~/
```

**When:** Emergency. Direct access when Git/Syncthing down.

---

## ROUTE SELECTION GUIDE

| Situation | Use Route |
|-----------|-----------|
| Same computer, C1→C2 | 1. Local Hub Files |
| Share code permanently | 2. Git |
| Real-time file sync | 3. Syncthing |
| Urgent message | 4. Trinity MCP |
| Everything else broken | 5. Tailscale |

---

## TESTING ALL 5 ROUTES

### Test 1: Local Hub
```bash
# On PC1
echo '{"test": true}' > ~/LOCAL_TRINITY_HUB/terminal_reports/test.json
# Check C2 terminal can read it
```

### Test 2: Git
```bash
git add . && git commit -m "test" && git push
# On PC2: git pull
```

### Test 3: Syncthing
```bash
# Drop file in outbound/
# Check it appears in PC2 inbound/
```

### Test 4: Trinity MCP
```python
mcp__trinity__trinity_broadcast(message="Test", from="C1")
# Check other instances receive
```

### Test 5: Tailscale
```bash
ping 100.85.71.74
# Should respond
```

---

## REDUNDANCY

If one route fails:
- Local Hub → Use Git
- Git → Use Syncthing
- Syncthing → Use Trinity MCP
- Trinity MCP → Use Tailscale
- Tailscale → Walk to the other computer

**Always have backup route.**
