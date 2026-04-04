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

Six agents, each with a name and role:

| Role | Name | When used | Reads | Writes |
|------|------|-----------|-------|--------|
| relay | ou | All messages — decides routing | Memory, Context | Messages |
| data | zeno | Vault search (via tool) | Vault, Memory | — |
| agenda | cato | Schedule queries (via tool) | Agenda/ | Agenda/ |
| action | hiro | External actions, background jobs | Task registry | External |
| pattern | rumi | Scheduled (04:00), 7-tool autonomous loop | Messages, Memory | Memory, Rules, Skills |
| code | alan | Code questions (development only) | Source code | vault/Codebase/ |

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

### Action Agent (hiro)

The Action agent executes tasks and background jobs. Currently in development with these planned capabilities:

| Capability | Status | Description |
|------------|--------|-------------|
| Task scheduling | Planned | Schedule one-time or recurring actions |
| Email sending | Planned | Send emails via configured SMTP |
| Calendar events | Planned | Create/modify calendar entries |
| File operations | Planned | Move, copy, archive files |
| External commands | Planned | Run whitelisted shell commands |

Action is disabled by default (`enabled: false`). When enabled, it:

- Receives tasks from other agents or scheduled jobs
- Executes actions with explicit confirmation for destructive operations
- Reports results back via message queue

**Security model:** Action has a whitelist of permitted operations. Unknown commands require explicit user approval in Exchange.md.

### Code Agent (alan)

The Code agent provides development-time intelligence. See [Code Agent (alan)](alan.md) for full documentation.

Summary:

- **Introspection**: Answer questions about outheis implementation

- **Proposals**: Suggest improvements via `vault/Codebase/Exchange.md`

- **Search**: Find patterns and implementations in source code

- **Isolation**: Write access restricted to `vault/Codebase/` only

**alan is development-only.** Disabled by default, never loaded in production.

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
| `shadow_scan` | 03:30 | Scan vault for chronological entries → Shadow.md |
| `agenda_review` | xx:55 (04-23) | Parse Agenda files (conditional on changes) |
| `action_tasks` | every 15 min | Run due scheduled tasks |
| `session_summary` | every 6 hours | Extract session insights |
| `tag_scan` | on demand | Scan vault for #tags, update cache — triggered from WebUI |

**Resource efficiency:** Agenda review checks file hashes before processing. If nothing changed, no LLM call is made. Morning (04:55) and evening (23:55) runs are unconditional to ensure day boundaries are handled.

### Schedule Configuration

In `config.json`:

```json
{
  "schedule": {
    "pattern_nightly": {"enabled": true, "times": ["04:00"]},
    "index_rebuild":   {"enabled": true, "times": ["04:30"]},
    "archive_rotation":{"enabled": true, "times": ["05:00"]},
    "shadow_scan":     {"enabled": true, "times": ["03:30"]},
    "agenda_review": {
      "enabled": true,
      "times": ["04:55","05:55","06:55","07:55","08:55","09:55",
                "10:55","11:55","12:55","13:55","14:55","15:55",
                "16:55","17:55","18:55","19:55","20:55","21:55",
                "22:55","23:55"]
    }
  }
}
```

Each task can be disabled independently. Tasks run in daemon threads — a running task blocks a second start of the same task but not others.

## The Scaling Problem

As a vault grows, agents can't hold everything in context. This is addressed through abstraction, not by adding more read-tools.

**Wrong:** more tools
```
read_file_1(), read_file_2(), ... read_file_n()
```

**Right:** better abstractions — an index the agent can query, with on-demand detail.

Four strategies in use or planned:

**1. Index with recency weighting** — The Data agent maintains a search index. Agents see a compact index, not raw files. The index includes access frequency and recency signals.

**2. Shadow.md as chronological pre-filter** — The Data agent runs a nightly vault scan and writes all time-relevant entries into a single structured file (`Agenda/Shadow.md`). The Agenda agent loads this instead of scanning the full vault on every hourly review.

**3. Progressive loading** — Overview first, detail on demand. The `load_skill(topic)` mechanism works like controlled demand paging: the agent has a summary in context and requests detail only when needed.

**4. Skill-based compression** — Skills replace lengthy instructions. "Use ISO dates" instead of ten examples. Better skills mean smaller prompts and more room for user content.

---

## Further Reading

- [Memory](memory.md) — How persistent memory works
- [Agenda](agenda.md) — Time management with Daily, Inbox, Exchange
- [Migration](migration.md) — Seeding memory from external sources
- [Code Agent (alan)](alan.md) — Development-time code intelligence
- [Web UI](webui.md) — Browser-based administration interface
- [Foundations](../foundations/) — Why this architecture
