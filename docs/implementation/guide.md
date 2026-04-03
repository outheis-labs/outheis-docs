---
title: Guide
---

# Guide

*Getting started with outheis.*

## Requirements

- Python 3.11+
- An Anthropic API key
- A vault directory — a folder of Markdown files (Obsidian works directly)

Optional for messaging via Signal:
- A registered Signal account for the bot phone number
- `signal-cli` installed and configured

## Installation

```bash
git clone https://github.com/outheis-labs/outheis-minimal.git
cd outheis-minimal
pip install -e ".[dev]"
```

## Setup

```bash
outheis init
```

This creates `~/.outheis/human/config.json` with defaults. Edit it:

```bash
$EDITOR ~/.outheis/human/config.json
```

Minimal required configuration:

```json
{
  "human": {
    "name": "Your Name",
    "language": "en",
    "timezone": "Europe/Berlin",
    "vault": ["~/Documents/Vault"]
  },
  "llm": {
    "providers": {
      "anthropic": {
        "api_key": "sk-ant-..."
      }
    },
    "models": {
      "fast":    {"provider": "anthropic", "name": "claude-haiku-4-5"},
      "capable": {"provider": "anthropic", "name": "claude-sonnet-4-5"}
    }
  }
}
```

The `vault` array accepts multiple paths. outheis monitors all of them.

## Starting the Dispatcher

```bash
outheis start        # Background daemon
outheis start -f     # Foreground (useful for first run / debugging)
outheis status       # Check PID, uptime, agent status
outheis stop         # Stop daemon
```

## Web UI

Once the dispatcher is running, the Web UI is available at:

```
http://127.0.0.1:8080
```

It provides:
- Live message feed (conversations with agents)
- Memory, Rules, and Skills viewer and editor
- Scheduler status and manual task triggers
- Token usage overview

The Web UI port and host are configurable in `config.json` under `"webui": {"host": "127.0.0.1", "port": 8080}`.

## Vault Setup

outheis treats your vault as a read-only knowledge source. Structure is flexible — any Markdown files work. The recommended Agenda layout:

```
vault/
└── Agenda/
    ├── Daily.md      # Today's schedule — written by cato
    ├── Inbox.md      # Your quick capture — processed hourly
    └── Exchange.md   # Async back-and-forth with cato
```

Create the `Agenda/` directory and empty files. cato generates `Daily.md` on first run.

## Signal Setup (optional)

To receive and send messages via Signal:

1. Register a dedicated phone number with Signal
2. Install and configure `signal-cli` for that number
3. Add to `config.json`:

```json
{
  "signal": {
    "enabled": true,
    "bot_name": "ou",
    "bot_phone": "+49...",
    "allowed": []
  }
}
```

Set `allowed` to an empty array to allow all contacts, or list specific numbers: `["+49..."]`.

Edit `~/.outheis/human/config.json` for the full config:

```json
{
  "user": {
    "name": "your-name",
    "language": "en",
    "timezone": "Europe/Berlin",
    "vault": ["~/Documents/Vault"]
  }
}
```

## CLI Commands

### Daemon Control

```bash
outheis start       # Start dispatcher (background)
outheis start -f    # Start in foreground
outheis start -fv   # Foreground + verbose (shows tool calls)
outheis stop        # Stop dispatcher
outheis status      # Show status, PID, uptime
```

### Messaging

```bash
outheis send "Hello"              # Single message
outheis send "@zeno find notes"   # Direct to Data agent
outheis chat                      # Interactive mode (with history)
```

### Memory

```bash
outheis memory              # Show all memories
outheis memory --type user  # Show only user facts
```

### Rules

```bash
outheis rules         # Show all rules (system + user)
outheis rules relay   # Show relay agent rules
```

## Talking to outheis

Just talk naturally. Relay decides when to use tools:

| You say | What happens |
|---------|--------------|
| "hi" | Direct response |
| "was steht heute an?" | Uses check_agenda tool → Agenda agent |
| "wo wohne ich?" | Uses search_vault tool → Data agent |
| "! ich bin 54" | Saves to Memory (explicit marker) |

### Explicit Agent Mentions

Use `@name` for direct delegation:

| Mention | Agent | Use for |
|---------|-------|---------|
| @zeno | Data | Search vault explicitly |
| @cato | Agenda | Schedule queries |
| @hiro | Action | External actions (future) |

## Vault

Your vault is a directory of Markdown files:

```markdown
---
title: Project Alpha
tags: [active, client-work]
created: 2025-01-15
---
# Project Alpha

Status update...
```

### Recommended Structure

```
vault/
├── Agenda/
│   ├── Daily.md      # Today's schedule
│   ├── Inbox.md      # Unprocessed items
│   └── Exchange.md   # External sync
├── projects/
├── notes/
└── references/
```

## Configuration

`~/.outheis/human/config.json`:

```json
{
  "user": {
    "name": "string",
    "language": "en|de|...",
    "timezone": "Region/City",
    "vault": ["~/path/to/vault"]
  },
  "llm": {
    "provider": "anthropic"
  }
}
```

## Troubleshooting

### "Dispatcher not running"

```bash
outheis status   # Check if running
outheis start    # Start it
```

### Stale PID file

```bash
rm ~/.outheis/.dispatcher.pid
outheis start
```

### No API key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# Or add to ~/.bashrc / ~/.zshrc
```

### macOS: Daemon won't start in background

Use foreground mode:

```bash
outheis start -f &
```
