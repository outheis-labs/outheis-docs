
# Remote Access via WireGuard (iPhone → Mac Mini)

This guide documents how to set up secure remote access to the outheis WebUI from an iPhone using WireGuard, including all pitfalls encountered.

---

## Overview

Goal: access `http://10.10.0.1:8080` from an iPhone over WireGuard, where the Mac Mini is the WireGuard server and the iPhone is the peer.

---

## 1. Install WireGuard on macOS

```bash
brew install wireguard-go wireguard-tools
```

---

## 2. Create keys

On the Mac Mini:

```bash
wg genkey | tee /etc/wireguard/server_private.key | wg pubkey > /etc/wireguard/server_public.key
```

On the iPhone: generate keys inside the WireGuard iOS app (Add Tunnel → Create from scratch).

---

## 3. Server config (`/etc/wireguard/wg0.conf`)

```ini
[Interface]
PrivateKey = <server private key>
Address = 10.10.0.1/24
ListenPort = 51820

[Peer]
PublicKey = <iphone public key>
AllowedIPs = 10.10.0.2/32
```

> **Note:** The server's `Address` will appear as `inet 10.10.0.1 --> 10.10.0.1` (a P2P self-loop on the `utun` interface) — this is normal for macOS WireGuard.

---

## 4. iPhone config (in WireGuard app)

```ini
[Interface]
PrivateKey = <iphone private key>
Address = 10.10.0.2/32
DNS = 1.1.1.1

[Peer]
PublicKey = <server public key>
Endpoint = <mac-mini-public-ip>:51820
AllowedIPs = 10.10.0.0/24
PersistentKeepalive = 25
```

`AllowedIPs = 10.10.0.0/24` routes only WireGuard traffic through the tunnel (not all internet traffic).

---

## 5. Start WireGuard

```bash
sudo wg-quick up wg0
```

Verify:

```bash
sudo wg show
```

---

## 6. outheis WebUI: bind to all interfaces

In the outheis WebUI config, set **Host** to `0.0.0.0` (with the warning acknowledged). This makes uvicorn listen on all interfaces, including the WireGuard `utun` interface.

Restart the daemon after changing the host.

---

## Pitfalls & Solutions

### Pitfall 1: Can't ping 10.10.0.1 — no ICMP reply

**Symptom:** `ping 10.10.0.1` from iPhone gets no reply. WireGuard handshake succeeds (`wg show` shows a recent handshake).

**Cause:** macOS Stealth Mode silently drops all uninitiated incoming packets — including ICMP echo requests.

**Fix:**
```bash
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode off
```

Verify:
```bash
/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode
# → Stealth mode is off
```

---

### Pitfall 2: TCP handshake succeeds but HTTP never responds

**Symptom:** `tcpdump` on `utun4` shows SYN → SYN/ACK → ACK → HTTP GET → server ACK, but uvicorn never logs the request and sends no HTTP response. Browser shows `ERR_CONNECTION_CLOSED`.

**Cause:** macOS Application Firewall was blocking incoming connections to the Homebrew Python binary. The firewall allows `/usr/bin/python3` but not `/opt/homebrew/.../Python`. Loopback traffic (SSH tunnel) bypasses the firewall, so local access works while WireGuard traffic is silently blocked at the application layer.

**Diagnosis:**
```bash
lsof -i :8080 -n -P        # find the PID of uvicorn
lsof -p <pid> | grep txt   # find the actual Python binary path
/usr/libexec/ApplicationFirewall/socketfilterfw --listapps  # check allowlist
```

**Fix:**
```bash
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add \
  /opt/homebrew/Cellar/python@3.12/3.12.13/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python

sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp \
  /opt/homebrew/Cellar/python@3.12/3.12.13/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python
```

> **Note:** The path contains the exact Python version. If you upgrade Python via Homebrew, repeat this step for the new version.

---

### Pitfall 3: IP forwarding is irrelevant

**Symptom/Confusion:** `sysctl net.inet.ip.forwarding` shows `0`. Might seem like a routing problem.

**Reality:** IP forwarding is only needed when the Mac acts as a router between two *different* networks. For WireGuard delivering packets destined for the Mac itself (10.10.0.1), forwarding is not involved. Leave it at 0.

---

### Pitfall 4: Brave browser blocks requests to private IPs (Private Network Access)

**Symptom:** Requests from a web page to `http://10.x.x.x/` fail with `ERR_FAILED`. Affects Chromium-based browsers (Brave, Chrome).

**Cause:** Chrome's Private Network Access (PNA) policy requires a preflight OPTIONS request with `Access-Control-Request-Private-Network: true` header, and the server must respond with `Access-Control-Allow-Private-Network: true`.

**Fix:** Add this to the FastAPI/Starlette middleware:

```python
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.method == "OPTIONS" and request.headers.get("Access-Control-Request-Private-Network"):
        return JSONResponse({}, headers={
            "Access-Control-Allow-Origin": request.headers.get("Origin", "*"),
            "Access-Control-Allow-Private-Network": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        })
    ...
```

---

### Pitfall 5: SSH tunnel conflicts with direct WireGuard access

**Symptom:** `ssh -fNL 8080:localhost:8080 <host>` fails with `bind [127.0.0.1]:8080: Address already in use` if outheis is already running locally.

**Cause:** Port 8080 is already bound by the local outheis instance.

**Solution:** Use a different local port for the tunnel, e.g.:
```bash
ssh -fNL 8081:localhost:8080 <host>
# then access http://localhost:8081/
```

Or stop the local outheis instance before tunneling.

---

## Normal Behavior to Expect

- `ifconfig utun4` shows `inet 10.10.0.1 --> 10.10.0.1` — the P2P self-loop is correct for macOS WireGuard (not Linux).
- `wg show` shows the peer with a handshake timestamp — this confirms the tunnel is active.
- `lsof -i :8080` shows `TCP *:8080 (LISTEN)` — uvicorn is bound to all interfaces.
