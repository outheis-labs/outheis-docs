---
title: Communicating with outheis
---

# Communicating with outheis

outheis can be reached through three channels. All channels connect to the same dispatcher and agents — the difference is where you type and how you receive responses.

---

## Web UI

A browser-based interface served locally by the dispatcher.

**Access:** `http://127.0.0.1:8080` (while dispatcher is running)

**What it provides:**
- Live message feed — conversations with agents in real time
- Prompt input — send messages directly from the browser
- Configuration editor — models, agents, scheduler
- Memory, Rules, Skills viewer and editor
- Vault file browser
- Scheduler status and manual task triggers

**Setup:** Enabled by default. Port and host are configurable in `config.json`:

```json
"webui": { "host": "127.0.0.1", "port": 8080 }
```

**Remote access via SSH port forwarding:**

```bash
ssh -L 8080:localhost:8080 user@your-server
```

---

## CLI

Command-line interface for sending messages and managing the daemon.

**Setup:** Available after `pip install -e .` with the venv active.

**Sending messages:**

```bash
outheis send "What's on my agenda today?"
outheis send "@zeno find notes about project alpha"
outheis chat                                        # interactive mode
```

**Daemon control:**

```bash
outheis start         # start in background
outheis start -f      # start in foreground
outheis start -fv     # foreground + verbose (shows tool calls)
outheis stop          # stop daemon
outheis status        # show PID, uptime, agent status
```

---

## Signal

Receive and send messages via the Signal messenger app. Requires a dedicated phone number for the bot.

**Setup:** See [Signal](../implementation/signal.md) in the implementation docs.

**How it works:** The bot listens for incoming Signal messages and routes them to the dispatcher. Responses are sent back as Signal messages. Voice messages are transcribed automatically if `faster-whisper` is installed.

**When to use:** Primary channel if you want to interact with outheis from your phone without opening a browser or terminal.
