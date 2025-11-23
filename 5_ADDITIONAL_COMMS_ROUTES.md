# 5 ADDITIONAL COMMUNICATION ROUTES

**Beyond git. These work even if git breaks.**

---

## ROUTE 6: SYNCTHING (Already Working!)

**Folder**: `C:\Users\dwrek\Sync\`

**How it works**: Files auto-sync between computers. No git needed.

### To Send Message:
```bash
echo "Message to all computers" > ~/Sync/PC1_MESSAGE_$(date +%s).txt
```

### To Receive:
```bash
ls ~/Sync/
cat ~/Sync/PC2_MESSAGE_*.txt
```

**AI_MESSAGES.json** already has 845KB of messages syncing!

### Setup on PC2/PC3:
1. Install Syncthing
2. Add PC1's device ID
3. Share the Sync folder
4. Done - files appear automatically

---

## ROUTE 7: ANYDESK (Remote Desktop + File Transfer)

**PC1 AnyDesk ID**: 157-645-9360
**PC2 AnyDesk ID**: 142-133-9914

### To Connect:
1. Open AnyDesk
2. Enter other computer's ID
3. Connect

### To Transfer Files:
1. Connect via AnyDesk
2. Open file transfer panel
3. Drag files between computers

### To Send Commands:
1. Connect via AnyDesk
2. Open remote terminal
3. Run commands directly

**This is VISUAL + DIRECT. No networking issues.**

---

## ROUTE 8: WINDOWS NETWORK SHARE

**Already shared**: `\\dwrekscpu\Users\dwrek\`

### From PC2 to access PC1:
```bash
# In File Explorer or terminal
\\100.70.208.75\Users\dwrek\100X_DEPLOYMENT\
```

### From PC1 to access PC2:
```bash
\\100.85.71.74\Users\
```

### To Send File:
```bash
copy myfile.txt \\100.85.71.74\Users\dwrek\
```

### To Receive:
Check the folder - files appear.

**Uses Tailscale IPs so it works over the mesh.**

---

## ROUTE 9: GOOGLE DRIVE SHARED FOLDER

**Setup Required**:
1. Create folder in Google Drive: `TRINITY_COMMS`
2. Share with all computers
3. Install Google Drive for Desktop on each PC
4. Mount to same location

### To Send:
```bash
echo "Message" > "G:\My Drive\TRINITY_COMMS\PC1_MSG.txt"
```

### To Receive:
```bash
cat "G:\My Drive\TRINITY_COMMS\PC2_MSG.txt"
```

**Syncs via cloud. Works even if local network dies.**

---

## ROUTE 10: DIRECT TCP SOCKET

**The nuclear option. Raw TCP over Tailscale.**

### Listener on PC2 (port 9999):
```python
# listen.py
import socket
s = socket.socket()
s.bind(('0.0.0.0', 9999))
s.listen(1)
print("Listening on 9999...")
conn, addr = s.accept()
data = conn.recv(1024)
print(f"Received: {data.decode()}")
conn.close()
```

### Sender from PC1:
```python
# send.py
import socket
s = socket.socket()
s.connect(('100.85.71.74', 9999))  # PC2's Tailscale IP
s.send(b"WAKE UP AND DO TASK X")
s.close()
```

### Or use netcat:
```bash
# PC2 listen
nc -l 9999

# PC1 send
echo "WAKE UP" | nc 100.85.71.74 9999
```

**Zero dependencies. Just IP and port.**

---

## SUMMARY: ALL 10 ROUTES

| # | Route | Type | Needs Git? | Needs Internet? |
|---|-------|------|------------|-----------------|
| 1 | Git Messages | File | Yes | Yes |
| 2 | Git Wake | File | Yes | Yes |
| 3 | Git Spawn Queue | File | Yes | Yes |
| 4 | Git Heartbeat | File | Yes | Yes |
| 5 | Tailscale Ping | Network | No | No (local) |
| 6 | Syncthing | File Sync | No | No (local) |
| 7 | AnyDesk | Remote | No | Yes |
| 8 | Windows Share | File | No | No (local) |
| 9 | Google Drive | Cloud | No | Yes |
| 10 | TCP Socket | Network | No | No (local) |

---

## FAILOVER PROTOCOL

**If Git fails**: Use Syncthing or Windows Share
**If Local network fails**: Use Google Drive or AnyDesk
**If Everything fails**: Use TCP Socket over Tailscale

---

## TEST EACH ROUTE NOW

### Route 6 Test (Syncthing):
```bash
# PC1
echo "SYNCTHING TEST $(date)" > ~/Sync/PC1_TEST.txt

# PC2 - check if file appears
ls ~/Sync/
```

### Route 7 Test (AnyDesk):
```
1. PC2: Open AnyDesk
2. PC2: Connect to 157-645-9360 (PC1)
3. Send test file via file transfer
```

### Route 8 Test (Windows Share):
```bash
# From PC2
dir \\100.70.208.75\Users\dwrek\100X_DEPLOYMENT\
```

### Route 9 Test (Google Drive):
```
1. Both PCs logged into same Google account
2. Create TRINITY_COMMS folder
3. Drop test file
4. Verify on other PC
```

### Route 10 Test (TCP):
```bash
# PC2 terminal
nc -l 9999

# PC1 terminal
echo "TCP TEST" | nc 100.85.71.74 9999
```

---

## EVERY PC MUST KNOW ALL 10 ROUTES

Copy this file to:
- PC1: Done
- PC2: Send via Syncthing + Git + AnyDesk
- PC3: Same

**NO EXCUSES. 10 ROUTES. SOMETHING WILL WORK.**
