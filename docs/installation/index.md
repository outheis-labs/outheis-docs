---
title: Installation
---

# Installation

*Private beta — April 2026.*

---

outheis is in private beta. The core loop works: you send a message, relay routes it, agents respond, patterns accumulate overnight. What's here is usable, not polished.

Known gaps are documented at the end of this page.

---

## Requirements

- Python 3.11 or higher
- An Anthropic API key (Claude Haiku / Sonnet — no other provider required)
- A vault directory — a folder of Markdown files (Obsidian vaults work directly)

Optional:
- Signal account + `signal-cli` for messaging via Signal

---

## Installation

```bash
git clone https://github.com/outheis-labs/outheis-minimal.git
cd outheis-minimal
pip install -e ".[dev]"
```

---

## Setup

```bash
outheis init
```

This creates `~/.outheis/human/` with default configuration, skills, and rules. Edit the config:

```bash
$EDITOR ~/.outheis/human/config.json
```

Minimum required:

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

The `vault` array accepts multiple paths.

---

## Vault

Create the Agenda directory in your vault:

```bash
mkdir -p ~/Documents/Vault/Agenda
touch ~/Documents/Vault/Agenda/Daily.md
touch ~/Documents/Vault/Agenda/Inbox.md
touch ~/Documents/Vault/Agenda/Exchange.md
```

cato generates `Daily.md` on first run. The other two files can stay empty.

---

## Start

```bash
outheis start        # Background daemon
outheis start -f     # Foreground (recommended for first run)
outheis status       # PID, uptime, agent status
outheis stop
```

On first start, outheis seeds `~/.outheis/human/skills/` and `~/.outheis/human/rules/` with defaults. These are yours to edit — they are never overwritten on restart.

---

## First Conversation

```bash
outheis chat
```

Or send a single message:

```bash
outheis send "What do you know about me?"
outheis send "What's on today?"
outheis send "! I work at Acme Corp"     # explicit memory marker
```

The `!` prefix writes directly to memory without waiting for the pattern agent.

---

## Web UI

```
http://localhost:8080
```

Starts automatically with the dispatcher. Provides:

- Live message feed (WebSocket)
- Memory, Skills, Rules editors
- Scheduler — manage and trigger background tasks
- Vault: Files (full browser), Agenda, Tags, Migration

---

## CLI Reference

### Daemon

```bash
outheis start        # Background
outheis start -f     # Foreground
outheis start -fv    # Foreground + verbose (shows tool calls)
outheis stop
outheis status
```

### Messaging

```bash
outheis send "message"
outheis send "@zeno find notes about X"   # direct to Data agent
outheis send "@cato what's on Thursday?"  # direct to Agenda agent
outheis chat                               # interactive session with history
```

### Memory

```bash
outheis memory              # show all
outheis memory --type user  # user facts only
```

### Rules

```bash
outheis rules               # all rules
outheis rules relay         # relay agent rules
```

---

## Signal Setup (optional)

Register a dedicated phone number with Signal, install `signal-cli`, then add to `config.json`:

```json
{
  "signal": {
    "enabled": true,
    "bot_name": "ou",
    "bot_phone": "+49...",
    "allowed": ["+49..."]
  }
}
```

`allowed` is a whitelist. Empty array permits all contacts.

**First contact — trust your identity key:**

On first use, signal-cli may not trust the sender's identity key. If messages are received but no response arrives, run:

```bash
signal-cli -a <bot_phone> listIdentities
signal-cli -a <bot_phone> trust -a <uuid>
```

outheis learns and saves UUIDs automatically after the first trusted message. The bot's display name (`bot_name`) is set as the Signal profile name on each start.

---

## What's in This Release

| Component | Status |
|-----------|--------|
| Dispatcher — microkernel, scheduler, lock manager | ✓ |
| Relay (ou) — routing, memory integration | ✓ |
| Data (zeno) — vault search, tag analysis | ✓ |
| Agenda (cato) — Daily, Inbox, Exchange | ✓ |
| Pattern (rumi) — nightly memory extraction | ✓ |
| Web UI — config, memory, scheduler, vault files, tags, migration | ✓ |
| Tags — scan, namespace grouping, rename, delete | ✓ |
| Migration — Exchange.md approval workflow | ✓ |
| Signal transport — receive, respond, voice transcription | ✓ |
| Vault file browser — all file types, images, Obsidian wikilinks | ✓ |
| Action (hiro) — external tasks, email, calendar | planned |
| Code (alan) — development-time introspection | dev only |

---

## Known Gaps

**hiro is disabled by default.** The Action agent framework is present but external integrations (email, calendar, shell commands) are not implemented. Enable at your own risk — it has no configured capabilities yet.

**alan is development-only.** The Code agent provides introspection into the outheis codebase itself. It is disabled in production and not relevant for users.

**Pattern agent requires conversation history.** On a fresh install, rumi has nothing to extract on the first nightly run. Memory builds over days, not immediately.

**Tag scan is on demand.** Tags are not indexed at startup. Run a scan from the Web UI (Vault → Tags → Scan) or say `analyze tags` in chat.

**No mobile UI.** Web UI is localhost-only by design. Use Signal transport for mobile access.

---

## Troubleshooting

**Dispatcher won't start**
```bash
rm ~/.outheis/.dispatcher.pid
outheis start -f
```

**No response from agents**
```bash
outheis status           # check dispatcher is running
outheis send "ping"      # check relay responds
```

**Web UI not loading**
The Web UI starts with the dispatcher. If port 8080 is busy, change it in `config.json`:
```json
{"webui": {"port": 8081}}
```

**API key errors**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```
Or set it permanently in `config.json` under `llm.providers.anthropic.api_key`.
