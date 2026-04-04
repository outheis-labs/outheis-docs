---
title: Communicating with outheis
---

# Communicating with outheis

outheis can be reached through three channels. All channels connect to the same dispatcher and agents — the difference is where you type and how you receive responses.

---

## Web UI

A browser-based interface served locally by the dispatcher. No separate server needed — the Web UI is built into the daemon and starts automatically with it.

**Access:** `http://127.0.0.1:8080` (while dispatcher is running)

**What it provides:**
- Live message feed showing all agent conversations in real time
- Prompt input — send messages to the relay agent directly from the browser
- Configuration editor (models, agents, providers, scheduler)
- Memory, Rules, Skills viewer and editor
- Vault file browser — browse, edit, and delete files across all configured vaults
- Tags view — scan for `#tags`, rename or remove them across the vault
- Scheduler — manage recurring tasks, view history

**Configuration:** Enabled by default. Port and host can be changed in `config.json`:

```json
"webui": { "host": "127.0.0.1", "port": 8080 }
```

**Remote access:** The UI binds to localhost only. To reach it from another machine, use SSH port forwarding:

```bash
ssh -L 8080:localhost:8080 user@your-server
```

Then open `http://localhost:8080` in your local browser. The tunnel stays active as long as the SSH connection is open.

For a full description of all views and API endpoints, see [Web UI](../implementation/webui.md).

---

## CLI

Command-line interface for sending messages and managing the daemon. Available as `outheis` after installation.

**Setup:** Available after `pip install -e .` with the venv active.

**Sending messages:**

```bash
outheis send "What's on my agenda today?"
outheis send "@zeno find notes about project alpha"
outheis chat                                        # interactive mode with history
```

The relay agent handles all messages and routes to the right agent automatically. Use `@name` to address an agent directly (`@zeno`, `@cato`, `@alan`, …).

**Daemon control:**

```bash
outheis start         # start in background
outheis start -f      # start in foreground
outheis start -fv     # foreground + verbose (shows tool calls)
outheis stop          # stop daemon
outheis status        # show PID, uptime, agent status
```

**Inspecting memory and rules:**

```bash
outheis memory              # show all stored memories
outheis memory --type user  # show only user facts
outheis rules               # show all rules (system + user)
outheis rules relay         # show rules for a specific agent
```

---

## Signal

Receive and send messages via the Signal messenger app. Requires a dedicated phone number for the bot and `signal-cli` installed and registered.

**How it works:** The Signal transport runs as a separate process alongside the daemon. It listens for incoming Signal messages from authorized numbers, routes them to the relay agent, and sends the responses back as Signal messages. Voice messages are transcribed automatically if `faster-whisper` is installed.

**Requirements:**
- A phone number registered with `signal-cli` for the bot
- `signal-cli` installed and configured
- `pip install -e ".[signal]"` for voice transcription (optional)

**Configuration:**

```json
"signal": {
  "enabled": true,
  "bot_name": "Ou",
  "bot_phone": "+49...",
  "allowed": []
}
```

`allowed` is a whitelist of phone numbers permitted to interact with the bot. An empty list means only `human.phone` can send messages.

**Running:**

```bash
outheis signal        # foreground
outheis signal -v     # verbose
```

Signal transport and the main daemon run independently and can be active simultaneously.

**When to use:** The primary channel for interacting with outheis from a phone without opening a browser or terminal.

For full setup instructions, see [Signal](../implementation/signal.md).
