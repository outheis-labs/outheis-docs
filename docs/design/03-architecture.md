# Architecture

This document describes the outheis architecture derived from the operating system principles surveyed in the previous documents.

---

## Overview

outheis is a multi-agent system where specialized agents communicate via message passing. A transport daemon handles external interfaces, a dispatcher routes messages and manages agent lifecycle, and agents process requests.

```
┌─────────────────────────────────────────────────────────────┐
│                      External World                          │
│                  (Signal, CLI, API)                          │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Transport (daemon)                        │
│                     (static, no LLM)                         │
│          receives, converts, sends — no understanding        │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
                       messages.jsonl
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        Dispatcher                            │
│                     (static, no LLM)                         │
│                                                              │
│  1. Explicit: "@ou", "@zeno", "@cato", "@hiro", "@rumi"       │
│  2. Keywords + Scoring → Agent (if above threshold)          │
│  3. Fallback → Relay (LLM decides)                           │
└─────────────────────────────┬───────────────────────────────┘
                              │
    ┌──────────┬──────────┬───┴───┬──────────┬──────────┐
    ▼          ▼          ▼       ▼          ▼          ▼
 Relay      Data      Agenda   Action    Pattern
 (route,   (vault,   (user    (execute, (reflect,
 compose)  aggregate) filter)  import)   insight)
```

---

## Directory Structure

```
~/.outheis/                      # System directory
├── agents/                      # Agent implementations
├── transport/                   # Transport daemon
├── dispatcher/                  # Dispatcher
├── web/                         # Web UI (localhost-only)
└── human/                       # ALL user-specific data
    ├── config.json              # User configuration
    ├── insights.jsonl           # Pattern agent output
    ├── rules/                   # Agenda agent rules
    ├── messages.jsonl           # Message queue (append-only)
    ├── archive/                 # Cold storage
    │   ├── messages-2025-01.jsonl
    │   └── ...
    ├── index.jsonl              # Search index (across all vaults)
    ├── tag-weights.jsonl        # Learned tag importance
    ├── cache/                   # Cached data
    │   └── agenda/              # Previous versions for diff
    ├── imports/                 # Imported external data
    │   ├── calendar/
    │   ├── email/
    │   └── ...
    └── vault/                   # Minimal starter vault

~/Documents/MyVault/             # External vault (user-managed, anywhere)
├── Agenda/
│   ├── Daily.md
│   ├── Inbox.md
│   └── Exchange.md
├── notes/
├── projects/
└── ...
```

### Privacy Guarantee

Removing `human/` erases ALL user-specific data: configuration, messages, insights, imports, cache. The system retains no knowledge of the user.

---

## Components

### Transport (daemon, no LLM)

Handles external interfaces. Converts between protocols and internal message format.

| Interface | Function |
|-----------|----------|
| Signal | Receive/send messages |
| CLI | Local interaction |
| API | Programmatic access (future) |

Transport does not understand content. It only converts and forwards.

```
Signal message → JSON → messages.jsonl
messages.jsonl → JSON → Signal message
```

### Dispatcher (daemon, no LLM)

Observes message queue (via filewatch: `inotify`/`kqueue`), routes messages, spawns/notifies agents.

#### Routing Logic

```python
msg = read_next()

if msg.to == "transport":
    notify(transport)
elif msg.to != "dispatcher":
    # Explicit target
    agent = get_or_spawn(msg.to)
    notify(agent)
else:
    # Dispatcher decides
    target = route(msg)
    if target:
        agent = get_or_spawn(target)
        notify(agent)
    else:
        # Fallback: Relay decides
        notify(relay)
```

#### Scoring

```python
def route(msg) -> AgentId | None:
    text = msg.payload.text.lower()
    
    # Explicit mention → immediate
    if "@ou" in text: return "relay"
    if "@zeno" in text: return "data"
    if "@cato" in text: return "agenda"
    if "@hiro" in text: return "action"
    if "@rumi" in text: return "pattern"
    
    # Scoring
    scores = {
        "data":   score(text, config.routing.data),
        "agenda": score(text, config.routing.agenda),
        "action": score(text, config.routing.action),
    }
    
    best = max(scores, key=scores.get)
    
    if scores[best] >= config.routing.threshold:
        return best
    
    return None  # → Relay
```

Keywords and threshold are configurable. Can be empty (all goes to Relay).

#### Lock Manager

The Dispatcher owns queue access via a Unix socket lock manager. All writers must acquire a lock before writing to `messages.jsonl`.

**Socket:** `~/.outheis/.dispatcher.sock`

**Priority Scheduling:**

| Priority | Requester | Rationale |
|----------|-----------|-----------|
| HIGH (0) | transport | User is waiting |
| NORMAL (1) | relay, data, agenda, action | Agent work |
| LOW (2) | pattern | Background processing |

Within each priority class: FIFO.

**Protocol:**

```json
// Request lock
→ {"cmd": "request", "requester": "relay"}
← {"status": "granted"}
← {"status": "queued", "position": 2}

// Release lock
→ {"cmd": "release"}
← {"status": "released"}

// Query status
→ {"cmd": "status"}
← {"holder": "client_123", "queue_length": 2, "queue": [...]}
```

**Behavior:**

- Lock granted immediately if queue empty
- On release, next-in-queue is notified
- Client disconnect → automatic release, cleanup
- Priorities are architectural, not configurable

#### File Locking

For files other than `messages.jsonl`, simple `flock` is used:

| File | Writers | Lock |
|------|---------|------|
| `messages.jsonl` | Transport, all Agents | Socket (prioritized) |
| `session_notes.jsonl` | All Agents | `flock` |
| `config.json` | CLI, Web UI | `flock` |
| Vault files | Data Agent | `flock` |

#### Write-Ahead Logging

All queue writes use write-ahead for crash safety:

```
~/.outheis/human/.pending/
├── msg_abc123.json
└── msg_def456.json
```

**Write sequence:**
1. Write message to `.pending/{msg_id}.json`
2. `flock` + append to `messages.jsonl`
3. Delete from `.pending/`

**Recovery (Dispatcher startup):**
1. Scan `.pending/`
2. Check for duplicates (last 100 IDs in queue)
3. Append missing messages, skip duplicates
4. Delete recovered pending files

If a process dies while waiting for the lock, the message survives in `.pending/` and is recovered when Dispatcher (re)starts.

### Web UI (localhost-only)

Simple web interface for configuration. No chat functionality.

| Function | Description |
|----------|-------------|
| Agents | Model, run mode, enabled |
| Models | Provider, name, local/remote |
| Dispatcher | Keywords, threshold |
| Human | Name, language, vault paths |
| System | Log level |
| Status | Agent status, logs |

Access: `http://localhost:<port>` only. No external exposure.

---

## Agents

### Roles and Responsibilities

| Role | Responsibility | Run Mode |
|------|----------------|----------|
| **Relay** | Classify, route, compose, ask user | daemon |
| **Data** | Knowledge management, aggregation, synthesis | on-demand |
| **Agenda** | Personal secretary: filter, prioritize, learn user | on-demand |
| **Action** | Task execution, external imports | on-demand |
| **Pattern** | Reflection, insight extraction | scheduled |

### Relay Agent

Routes unclear requests, composes responses, asks for clarification when needed.

- Receives messages Dispatcher cannot route
- Classifies intent
- Routes to appropriate agent
- Composes final response from agent outputs
- Formats output for each channel (Signal, CLI, API)

### Agenda Agent (Personal Mode)

Acts as a personal secretary. The name reflects both meanings: managing your agenda (schedule, priorities) and enabling your agency (capacity to act).

**Problem it solves**: 47 calendar entries, 23 emails, 14 tasks—presented raw, this creates cognitive overhead. The agenda agent reduces mental friction by filtering and prioritizing based on learned preferences.

```
Raw data (overwhelming)
  │
  ▼
Data Agent (complete, neutral)
  │
  ▼
Agenda Agent (filtered, prioritized, personal)
  │
  ▼
User (only what matters, when it matters)
```

**What Agenda does**:

- Learns user rules ("Monday mornings: no meetings")

- Understands priorities ("family over work, except deadlines")
- Filters noise ("this email can wait, that one cannot")
- Presents relevance, not completeness

**Where rules live**: `human/rules/` directory—only Agenda reads them.

In Domain Expert Mode, Agenda is disabled. Data delivers directly to Relay.

### Data Agent

Central knowledge manager:

1. **Vault Access**: Reads and writes to vault
2. **Aggregation**: Combines information from multiple sources
3. **Synthesis**: Answers complex queries requiring reasoning
4. **Coordination**: Requests external data from Action when needed

```
User question: "How does X compare to current developments?"
                              │
                              ▼
                         Data Agent
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
         vault                          Action Agent
      (internal)                     (fetches external)
              │                               │
              └───────────────┬───────────────┘
                              │
                         Data aggregates
                              │
                              ▼
                          Response
```

### Ownership Model

Each agent owns its domain exclusively. Others request access via messages.

| Agent | Owns |
|-------|------|
| Relay | Routing decisions, response composition, channel formatting |
| Agenda | User preferences, rules, Daily/Inbox/Exchange |
| Data | Vault, knowledge synthesis, index |
| Action | Task execution, external imports |
| Pattern | Insights generation, tag learning |

---

## Message Protocol

### Message Schema

```
{
  id:              string       // Snowflake ID (contains timestamp)
  conversation_id: string       // Groups multi-turn exchanges
  
  from: {
    agent?:        AgentId      // If from agent
    user?: {
      channel:     string       // "signal", "cli", "api"
      identity:    string       // Phone, username, key
      name?:       string       // Display name
    }
  }
  
  to:              AgentId | "dispatcher" | "transport"
  
  type:            "request" | "response" | "event"
  intent?:         string       // e.g., "data.query", "action.execute"
  payload:         any
  
  reply_to?:       string       // Message ID for responses
}
```

### Message Flow Example

```
User sends "What's on my agenda tomorrow?" via Signal

1. Transport receives from Signal
   → writes {to: "dispatcher", ...} to queue

2. Dispatcher reads, matches keyword "agenda"
   → notifies Agenda Agent

3. Agenda queries Data, filters, prioritizes
   → writes {to: "relay", ...} to queue

4. Dispatcher notifies Relay
   → Relay composes human-readable response
   → writes {to: "transport", ...} to queue

5. Transport sends via Signal
```

---

## Queue

### Implementation

The message queue is an append-only JSONL file:

```
~/.outheis/human/messages.jsonl
```

- **Append-only**: Messages are never modified or deleted

- **Single file**: Simplicity over performance

- **File locking**: Simple `fcntl` locking for concurrent access

```python
import fcntl
import json

def append_message(path: str, msg: dict) -> None:
    with open(path, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(msg) + '\n')
        fcntl.flock(f, fcntl.LOCK_UN)
```

### Benefits (Event Sourcing)

- **Audit trail**: Complete history of all interactions

- **Replay**: Reconstruct any past state

- **Debugging**: See exactly what happened

- **Recovery**: Resume from last processed message

---

## Deployment Spectrum

The system scales from minimal (cloud, cost-conscious) to maximal (local, all daemon):

### Minimal (Cloud, Sparse)

```json
{
  "dispatcher": {
    "routing": {
      "threshold": 0.3,
      "data":   ["vault", "search", "find"],
      "agenda": ["appointment", "calendar", "tomorrow"],
      "action": ["send", "email", "open"]
    }
  },
  "agents": {
    "instances": {
      "relay":   { "model": "fast",      "run_mode": "daemon" },
      "data":    { "model": "capable",   "run_mode": "on-demand" },
      "agenda":  { "model": "capable",   "run_mode": "on-demand" },
      "action":  { "model": "capable",   "run_mode": "on-demand" },
      "pattern": { "model": "strategic", "run_mode": "scheduled" }
    },
    "models": {
      "fast":      { "provider": "anthropic", "name": "..." },
      "capable":   { "provider": "anthropic", "name": "..." },
      "strategic": { "provider": "anthropic", "name": "..." }
    }
  }
}
```

Strategy: Strict keywords, high threshold → minimize LLM calls.

### Maximal (Local, All Daemon)

```json
{
  "dispatcher": {
    "routing": {
      "threshold": 0.0,
      "data":   [],
      "agenda": [],
      "action": []
    }
  },
  "agents": {
    "instances": {
      "relay":   { "model": "local", "run_mode": "daemon" },
      "data":    { "model": "local", "run_mode": "daemon" },
      "agenda":  { "model": "local", "run_mode": "daemon" },
      "action":  { "model": "local", "run_mode": "daemon" },
      "pattern": { "model": "local", "run_mode": "daemon" }
    },
    "models": {
      "local": { "provider": "ollama", "name": "..." }
    }
  }
}
```

Strategy: Empty keywords, zero threshold → Relay routes everything (free locally).

### Hybrid

Mix of local and remote models. Fast/cheap models locally, capable models remote.

---

## Access Control

### Dynamic Restriction (OpenBSD-inspired)

Agents declare capabilities at startup and progressively restrict themselves:

```python
class DataAgent:
    def __init__(self):
        self.pledge(["vault:read", "vault:write"])
        self.unveil(["vault/"])
        # From here: cannot access human/, cannot make network calls
```

### Capability Matrix

| Agent | vault | human/insights | human/rules | network | execute |
|-------|-------|----------------|-------------|---------|---------|
| Relay | - | - | - | - | - |
| Agenda | read | read | read | - | - |
| Data | read, write | read | - | - | - |
| Action | write (import) | read | - | ✓ | ✓ |
| Pattern | read | read, write | - | - | - |

Note: Agents request services from other agents via messages. Data can ask Action to fetch external data; Agenda asks Data for aggregated information.

---

## Error Handling

When an agent fails:

```
1. Log error (always)
2. Inform user via Relay
3. Retry with clarification if applicable
4. If persistent failure: escalate to user
```

### Error Message Flow

```
Agent fails
    │
    ▼
Dispatcher catches
    │
    ├──► Log error message to messages.jsonl
    │
    └──► Write {to: "relay", type: "error", ...} to queue
            │
            ▼
        Relay informs user:
        "I couldn't complete that. Can you clarify...?"
```

### Retry Logic

| Error Type | Action |
|------------|--------|
| Transient (timeout, rate limit) | Automatic retry (max 3) |
| Ambiguous input | Ask user for clarification |
| Persistent failure | Inform user, log, abort |

---

## Conversation Lifecycle

Conversations do not explicitly end. They age out.

### Rotation

When `messages.jsonl` exceeds a threshold (configurable, default 10MB):

```
messages.jsonl          → messages.jsonl (current)
                        → archive/messages-2025-03.jsonl (cold)
```

### Cold Storage

Old conversations move to `human/archive/`:

```
~/.outheis/human/
├── messages.jsonl           # Hot: current, fast access
└── archive/
    ├── messages-2025-01.jsonl
    ├── messages-2025-02.jsonl
    └── ...                  # Cold: slower access
```

### Access Patterns

| Storage | Access Time | Use Case |
|---------|-------------|----------|
| Hot | Immediate | Recent conversations |
| Cold | Slower (load on demand) | "What did we discuss in January?" |

Cold storage access:
1. User asks about old conversation
2. Data agent loads relevant archive file
3. Searches, returns results
4. Unloads (memory management)

---

## Pattern Agent Scheduling

The pattern agent runs:

1. **Scheduled**: Default 04:00 local time (configurable via Web UI)
2. **On-demand**: When user explicitly requests reflection

### Configuration

```json
{
  "agents": {
    "instances": {
      "pattern": {
        "model": "strategic",
        "run_mode": "scheduled",
        "schedule": {
          "times": ["04:00"],
          "timezone": "local"
        }
      }
    }
  }
}
```

Multiple times possible: `["04:00", "16:00"]`

### On-Demand Trigger

User can request: "@rumi reflect on this week" → Dispatcher routes to Pattern.

---

## Priority Scheduling (GCD-inspired)

Agents have implicit priority levels:

| Priority | Agent | Rationale |
|----------|-------|-----------|
| High | Relay | User-facing, latency-sensitive |
| Default | Action, Data, Agenda | Normal operations |
| Background | Pattern | Reflection can wait |

The dispatcher may defer background work when high-priority messages are pending.

---

## Channel-Specific Formatting

Relay agent formats output for each channel:

### Signal

No Markdown support, but good emoji support:

```
📅 TODAY

• 09:00 Standup
• 14:00 Workshop

⚠️ CONFLICT
   10:00 Team meeting
   10:00 Dentist
   → Which takes priority?

✅ Proposal reviewed
☐ Finish report

💬 1 open question → see Exchange
```

| Element | Formatting |
|---------|------------|
| Headers | CAPS + emoji |
| Lists | • bullets |
| Tasks open | ☐ |
| Tasks done | ✅ |
| Conflicts | ⚠️ prominent |
| Deadlines | 🔴 or ⏰ |
| Questions | 💬 |
| Links/refs | → plain text |

### CLI

ANSI colors and formatting:

```
TODAY
─────
  09:00  Standup
  14:00  Workshop

⚠ CONFLICT
  10:00  Team meeting
  10:00  Dentist

Tasks
  [ ] Finish report
  [x] Proposal reviewed
```

### API

Structured JSON for programmatic access.

### User Behavior

| File | User attention |
|------|----------------|
| `Daily.md` | Primary — checked regularly |
| `Inbox.md` | Write-only from user perspective |
| `Exchange.md` | Occasional — when Daily references it |

Conflicts and urgent items must surface in `Daily.md`, not hidden in Exchange.

---

## Operating Modes

### Personal Assistant (Default)

- `human/` directory active
- Agenda agent enabled
- Pattern agent reflects on user behavior
- Single user via Transport

### Domain Expert (Future)

- `human/` directory represents admin, not end-user
- Agenda agent disabled
- Pattern agent reflects on domain knowledge
- Multiple end-users via Transport
- Admin configures system via Web UI

---

## Importance of Attention

The transformer architecture's core insight from "Attention Is All You Need" (Vaswani et al., 2017) — that attention mechanisms direct processing to what matters — applies directly to outheis. This isn't metaphor; it's the same principle at a different level.

### The Learning Architecture

```
Skills (highest density)
   │  condensed principles
   │  "Dates: Always ISO format"
   │  direct attention BEFORE processing
   │
Memory (medium density)
   │  facts, observations
   │  "User corrected date format 3x"
   │  raw material for distillation
   │
Rules (lowest density)
      hard constraints
      "Never delete without confirmation"
      override everything, rarely change
```

### The Mapping

| LLM Concept | outheis Equivalent |
|-------------|-------------------|
| Trained weights | Skills (distilled principles) |
| Context window | Memory (current observations) |
| Query | User message |
| Training loop | Pattern Agent (nightly) |

### How Learning Works

```
User interacts with agents
        ↓
Corrections, preferences observed
        ↓
Stored in Memory (feedback type)
        ↓
Pattern Agent runs (nightly)
        ↓
Recognizes patterns (3+ similar observations)
        ↓
Distills into Skill (condensed principle)
        ↓
Deletes redundant Memory entries
        ↓
Next agent invocation: Skill directs attention
        ↓
Agent behaves differently (learned)
```

This is gradient descent at the system level. Each correction adjusts the "weights" (skills). Over time, the system needs less explicit context because skills direct attention efficiently.

### Why Not More Code?

The anti-pattern is solving learning with hardcoded logic:

**Wrong:**
```python
def format_date(date):
    if user_prefers_iso:
        return date.isoformat()
    elif user_prefers_german:
        return date.strftime("%d.%m.%Y")
```

**Right:**
```
Skill: "Dates: Always ISO format (YYYY-MM-DD)"
```

The LLM reads the skill and applies it. No code changes needed when preferences change. The system learns by refining skills, not by adding branches.

### Scaling Through Semantic Compression

As context grows, naive approaches fail:

**Wrong:** Add more tools to fetch more data

**Right:** Semantic compression — the Pattern Agent distills many specific observations into few general principles

```
3x "User corrected date format"  →  "Dates: Always ISO format"
5x "User prefers short answers"  →  "Brevity: be concise"
```

The meaning is preserved, the redundancy disappears. One skill replaces ten memory entries, directing attention to what matters.

### Pattern Agent as Optimizer

The Pattern Agent is the optimizer of this system:

1. **Observes gradients** — user corrections indicate error
2. **Accumulates updates** — memory stores observations
3. **Applies batch update** — nightly distillation
4. **Prunes redundancy** — deletes obsolete memory

The goal: a system that improves not by adding code, but by refining attention. The longer it runs, the less context it needs.

---

## Design Principles Summary

| Principle | Implementation |
|-----------|----------------|
| Message Passing | Append-only queue, no shared state |
| Ownership | Each agent owns its domain |
| Supervision | Dispatcher monitors and restarts |
| Dynamic Restriction | Agents pledge/unveil at startup |
| Priority Scheduling | User-facing work first |
| Append-Only Log | Queue as source of truth |
| Specialization | One agent, one role |
| Secure by Default | No implicit capabilities |

---

## Implementation Stack

| Component | Technology |
|-----------|------------|
| Transport | Python (daemon) |
| Dispatcher | Python (daemon) |
| Agents | Python |
| Queue | JSONL file |
| Configuration | JSON |
| Web UI | localhost-only, config only |
| Vault | Markdown files + arbitrary assets |

---

Next steps: Implementation of core components following this architecture.
