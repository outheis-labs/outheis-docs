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

Receive and send messages via the Signal messenger app. The bot runs as a separate process alongside the daemon — it listens for incoming Signal messages, routes them to the relay agent, and sends responses back. Voice messages are transcribed automatically if `faster-whisper` is installed.

**When to use:** The primary channel for interacting with outheis from a phone without opening a browser or terminal.

### What you need

A dedicated SIM card with a phone number that is not already registered on Signal. This number becomes the bot's identity — it should not be your personal number. A prepaid SIM works fine; the number only needs to be reachable by SMS or voice call once during registration.

### 1. Install signal-cli

signal-cli requires Java 17+. Install it first if needed (`java -version` to check).

**macOS (Homebrew):**

```bash
brew install signal-cli
```

**Linux / manual:**

Download the latest release from [github.com/AsamK/signal-cli/releases](https://github.com/AsamK/signal-cli/releases). Extract and place the `signal-cli` binary somewhere on your `$PATH` (e.g. `/usr/local/bin/signal-cli`).

Verify:

```bash
signal-cli --version
```

### 2. Register the bot number

Replace `+49...` with the bot's phone number in international format throughout.

```bash
signal-cli -a +49... register
```

Signal sends a verification code to the number via SMS. If SMS is not available, request a voice call instead:

```bash
signal-cli -a +49... register --voice
```

Confirm with the received code:

```bash
signal-cli -a +49... verify 123-456
```

The account is now registered. signal-cli stores credentials under `~/.local/share/signal-cli/`.

### 3. Trust your own number

Before the bot can exchange messages with your personal Signal account, you need to trust the safety number once:

```bash
signal-cli -a +49... trust -v <safety-number> +49YOUR_PERSONAL_NUMBER
```

To get the safety number:

```bash
signal-cli -a +49... listIdentities
```

Alternatively, send a test message first — signal-cli will print an untrusted identity warning with the safety number included, which you can then use to run the trust command.

### 4. Configure outheis

Add the Signal section to `~/.outheis/human/config.json`:

```json
"signal": {
  "enabled": true,
  "bot_name": "Ou",
  "bot_phone": "+49...",
  "allowed": []
}
```

Set `bot_phone` to the registered bot number. `bot_name` is the display name Signal contacts will see. `allowed` is a whitelist of phone numbers permitted to interact with the bot — an empty list means only `human.phone` (from the `human` section) can send messages.

Make sure `human.phone` in the config is set to your personal number:

```json
"human": {
  "phone": "+49YOUR_PERSONAL_NUMBER",
  ...
}
```

### 5. Optional: voice transcription

To transcribe incoming voice messages before forwarding them to the relay agent:

```bash
pip install -e ".[signal]"
```

This installs `faster-whisper`. Without it the transport still works; voice messages are silently skipped.

### 6. Run

```bash
outheis signal        # foreground
outheis signal -v     # verbose (shows tool calls)
```

Signal transport and the main daemon run independently. Start the daemon first (`outheis start`), then the Signal transport in a separate terminal or as a background process.

For details on the internal architecture, see [Signal](../implementation/signal.md).
