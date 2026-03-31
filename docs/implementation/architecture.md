---
title: Architecture
---

# Architecture

*How the pieces fit together.*

## Overview

```
┌─────────────────────────────────────────┐
│              Dispatcher                  │
│            (Microkernel)                 │
│  ┌─────────┐ ┌─────────┐ ┌───────────┐  │
│  │ Watcher │ │  Lock   │ │ Scheduler │  │
│  │         │ │ Manager │ │           │  │
│  └─────────┘ └─────────┘ └───────────┘  │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────┬─────────────┐
    ▼             ▼             ▼             ▼
┌───────┐    ┌───────┐    ┌───────┐    ┌───────┐
│  ou   │    │ zeno  │    │ cato  │    │ rumi  │
│ relay │    │ data  │    │agenda │    │pattern│
└───┬───┘    └───┬───┘    └───┬───┘    └───┬───┘
    │            │             │             │
    ▼            ▼             ▼             ▼
┌─────────┐  ┌───────┐   ┌────────┐   ┌────────┐
│   LLM   │  │ Vault │   │ Agenda │   │ Memory │
│ (Haiku) │  │       │   │  dir   │   │        │
└─────────┘  └───────┘   └────────┘   └────────┘
```

## Dispatcher

The dispatcher is the microkernel. It:
- **Watches** the message queue for changes
- **Manages locks** for shared resources
- **Schedules** periodic tasks (pattern analysis, index rebuild)
- **Recovers** pending operations on startup

The dispatcher contains no LLM calls. It's deterministic, testable, fast.

## Agents

Five agents, each with a name and role:

| Role | Name | When used | Reads | Writes |
|------|------|-----------|-------|--------|
| relay | ou | All messages — decides routing | Memory, Context | Messages |
| data | zeno | Vault search (via tool) | Vault, Memory | — |
| agenda | cato | Schedule queries (via tool) | Agenda/ | Agenda/ |
| action | hiro | External actions (future) | — | External |
| pattern | rumi | Scheduled (04:00) | Messages, Seed | Memory, Rules |

### Routing

Relay (ou) handles all user messages. It uses Haiku with tools:
- **search_vault** → delegates to Data agent (zeno)
- **check_agenda** → delegates to Agenda agent (cato)
- **refresh_agenda** → triggers manual agenda update

No separate classification step. Relay decides intelligently based on the question and Memory.

Explicit mentions (@zeno, @cato) still work for direct delegation.

### Data Agent (zeno)

The Data agent handles vault queries. For simple questions, it answers directly without LLM calls:

| Query Type | Example | Response |
|------------|---------|----------|
| File existence | "Habe ich X?" | `Ja, die Datei existiert: /path/to/X` |
| Stats | "Wie viele PDFs?" | `Du hast 12 PDF-Dateien im Vault.` |
| List | "Welche PDFs?" | List of matching files |
| Path lookup | "Wo ist X?" | Direct path or fuzzy matches |

Complex queries still use LLM for intelligent search and synthesis.

### Agenda Agent (cato)

The Agenda agent manages three files in `vault/Agenda/`:

| File | Direction | Purpose |
|------|-----------|---------|
| Daily.md | Bidirectional | Today's schedule, tasks, notes |
| Inbox.md | User → System | Quick capture, unprocessed items |
| Exchange.md | System ↔ User | Async questions, no pressure to respond |

**Commands:**
- "aktualisiere daily" / "update agenda" → triggers manual refresh
- Processes Inbox items, checks Exchange responses, updates Daily

**Hourly Review (conditional):**
- Runs at xx:55 (configurable)
- Checks file hashes before processing — no changes = no LLM call
- Unconditional at start (04:55) and end (23:55) of day
- Only runs within configured hours (default 04:55-23:55)

### Pattern Agent (rumi)

The Pattern agent runs nightly and:
1. Extracts memories from recent conversations
2. Consolidates duplicates, resolves contradictions
3. Promotes stable patterns to User Rules
4. Validates own extraction strategies (learns how to learn)

**Memory Migration** is handled via chat commands ("memory migrate") through Relay, not Pattern agent. See [Migration](migration.md).

## Knowledge Stores

### Memory

Meta-knowledge about the user:

| Type | Purpose | Decay |
|------|---------|-------|
| `user` | Personal facts | Permanent |
| `feedback` | Working preferences | Permanent |
| `context` | Current focus | 14 days |

Stored in `~/.outheis/human/memory/`. See [Memory](memory.md) for details.

### Rules

External instructions to agents — what to observe:

- User-defined: "Respond in German"
- Pattern-promoted: "User prefers short answers"

Stored in `~/.outheis/human/rules/`. See [Memory](memory.md) for details.

### Skills

Internal capabilities — how agents act:

- System skills: Base capabilities (in package)
- Learned skills: Refined through use and correction

Stored in `src/outheis/agents/skills/` (system) and `~/.outheis/human/skills/` (learned). See [Skills](skills.md) for details.

### Vault

The vault is a directory of Markdown files with YAML frontmatter:

```
vault/
├── Agenda/
│   ├── Daily.md      # Today's schedule
│   ├── Inbox.md      # Unprocessed items
│   └── Exchange.md   # Async communication
├── projects/
│   └── *.md
└── notes/
    └── *.md
```

The Data agent maintains a search index in `~/.outheis/human/cache/index/`.

## Message Queue

All communication flows through `messages.jsonl`:

```json
{"v":1,"id":"msg_abc","conversation_id":"conv_xyz","to":"dispatcher",...}
{"v":1,"id":"msg_def","conversation_id":"conv_xyz","to":"transport",...}
```

Append-only. Versioned. Recoverable.

## File Layout

```
~/.outheis/
├── .dispatcher.pid       # PID file
├── .dispatcher.sock      # Lock manager socket
└── human/
    ├── config.json       # Configuration (includes schedule)
    ├── messages.jsonl    # Message queue
    ├── memory/           # Persistent memory
    │   ├── user.json
    │   ├── feedback.json
    │   ├── context.json
    │   └── pattern/      # Pattern agent's learning
    │       └── strategies.md
    ├── cache/            # Regenerable working data
    │   ├── index/        # Search indices
    │   │   └── Vault.jsonl
    │   ├── agenda/       # Agenda file state
    │   │   ├── hashes.json       # Quick change detection
    │   │   ├── Daily.md.prev     # For diff
    │   │   ├── Inbox.md.prev
    │   │   └── Exchange.md.prev
    │   └── sessions/     # Session replay logs
    ├── rules/            # User-defined rules (external)
    │   ├── common.md
    │   ├── relay.md
    │   ├── agenda.md
    │   └── data.md
    ├── skills/           # Learned skills (internal)
    │   ├── common.md
    │   ├── relay.md
    │   ├── agenda.md
    │   └── data.md
    ├── vault/            # Primary vault (default)
    │   └── Migration/    # Temporary migration dir (user creates)
    │       ├── data.md           # Files to import
    │       └── Migration.md      # outheis creates
    └── archive/          # Archived messages
```

### Cache vs. Memory vs. Vault vs. Rules vs. Skills

| Directory | What | Who writes | Deletable? |
|-----------|------|------------|------------|
| `memory/` | Facts about user | Pattern Agent | Lose learnings |
| `rules/` | Instructions to agents | User, Pattern | Lose preferences |
| `skills/` | Agent capabilities | Agent, Pattern | Lose refinements |
| `cache/` | Working state | System | Safe — rebuilds |
| `vault/` | User's content | User | User's responsibility |

The cache directory is explicitly regenerable. Delete it anytime — outheis rebuilds what it needs.

## Scheduled Tasks

The dispatcher runs periodic tasks via built-in scheduler. All times configurable in `config.json`:

| Task | Default Time | Purpose |
|------|--------------|---------|
| `pattern_nightly` | 04:00 | Extract memories, consolidate, promote rules |
| `index_rebuild` | 04:30 | Rebuild vault search indices |
| `archive_rotation` | 05:00 | Archive old messages |
| `agenda_review` | xx:55 (04-23) | Parse Agenda files (conditional on changes) |
| `action_tasks` | every 15 min | Run due scheduled tasks |
| `session_summary` | every 6 hours | Extract session insights |

**Resource efficiency:** Agenda review checks file hashes before processing. If nothing changed, no LLM call is made. Morning (04:55) and evening (23:55) runs are unconditional to ensure day boundaries are handled.

### Schedule Configuration

In `config.json`:

```json
{
  "schedule": {
    "pattern_nightly": {"enabled": true, "hour": 4, "minute": 0},
    "index_rebuild": {"enabled": true, "hour": 4, "minute": 30},
    "archive_rotation": {"enabled": true, "hour": 5, "minute": 0},
    "agenda_review": {
      "enabled": true,
      "hourly_at_minute": 55,
      "start_hour": 4,
      "end_hour": 23
    },
    "action_tasks": {"enabled": true},
    "session_summary": {"enabled": true}
  }
}
```

Each task can be disabled independently. Agents run sequentially in the early morning to avoid conflicts.

## Further Reading

- [Memory](memory.md) — How persistent memory works
- [Agenda](agenda.md) — Time management with Daily, Inbox, Exchange
- [Migration](migration.md) — Seeding memory from external sources
- [Philosophy](../philosophy/) — Why this architecture
