---
title: Web UI
---

# Web UI

*Local administration interface for outheis.*

## Overview

The Web UI provides a browser-based interface for configuring and monitoring outheis. It runs on `localhost:8080` and is explicitly **not** designed for remote access — all user data stays local.

```
┌─────────────────────────────────────────────────────────────┐
│ outheis                              [Overview] [Save]       │
├─────────────┬───────────────────────────────────────────────┤
│ System      │                                               │
│  Overview   │  ┌─────────┐ ┌─────────┐ ┌─────────┐         │
│  Config     │  │Dispatcher│ │ Agents │ │Messages │         │
│  Messages   │  │ Running  │ │  5/6   │ │   42    │         │
│  Scheduler  │  └─────────┘ └─────────┘ └─────────┘         │
│             │                                               │
│ Knowledge   │  Recent messages                              │
│  Memory     │  ┌─────────────────────────────────────────┐ │
│  Skills     │  │ 14:32  cato → relay  Daily updated      │ │
│  Rules      │  │ 14:30  scheduler     agenda_review      │ │
│  Patterns   │  │ 14:15  zeno → relay  Found 3 matches    │ │
│             │  └─────────────────────────────────────────┘ │
│ Vault       │                                               │
│  Agenda     │                                               │
│  Codebase   │                                               │
│  Migration  │                                               │
│  Tags       │                                               │
└─────────────┴───────────────────────────────────────────────┘
```

## Starting the Server

```bash
cd outheis-minimal/webui
pip install fastapi uvicorn
python server.py
```

Opens at `http://localhost:8080`. The server watches `~/.outheis/human/` for changes.

## Navigation

### System

| View | Purpose |
|------|---------|
| **Overview** | Dashboard with dispatcher status, active agents, message count, recent messages |
| **Configuration** | Full config editor with tabs: General, Providers, Models, Agents, Signal |
| **Messages** | Live view of `messages.jsonl` with WebSocket updates |
| **Scheduler** | Manage scheduled tasks (agenda_review, shadow_scan, pattern_nightly) |

### Knowledge

| View | Purpose |
|------|---------|
| **Memory** | View/edit files in `~/.outheis/human/memory/` |
| **Skills** | View/edit files in `~/.outheis/human/skills/` |
| **Rules** | View/edit files in `~/.outheis/human/rules/` |
| **Patterns** | View files in `~/.outheis/human/cache/patterns/` (read-only) |

### Vault

| View | Purpose |
|------|---------|
| **Files** | Full vault browser — all configured vaults, directory tree, edit and delete |
| **Agenda** | View/edit files in `vault/Agenda/` (Daily.md, Inbox.md, Exchange.md) |
| **Codebase** | View files in `vault/Codebase/` (alan's proposals) |
| **Migration** | Upload migration files (drop zone), view and edit files, manage Migration/ directory |
| **Tags** | Scan vault for #tags, list by namespace group, rename or delete tags across all files |

## Files View

Full browser for all configured vault directories:

- **Directory tree** on the left — all vaults as roots, directories collapsed by default, click to expand
- **File viewer/editor** on the right — same rendered/source toggle as other file views
- **All file types** visible in the tree:
  - Text files (`.md`, `.txt`, `.json`, `.py`, …) — editable, Save button
  - Image files (`.png`, `.jpg`, `.svg`, …) — rendered inline, Download button
  - Binary files (`.pdf`, `.docx`, …) — Download button
- **Obsidian wikilinks** — `![[image.jpg]]` and `![[image.jpg|WxH]]` are resolved and rendered as inline images
- **Delete** — confirmation dialog, removes file from vault

## Tags View

The Tags view scans the vault for all `#tags` and presents them grouped by namespace prefix:

- **Scan button** — queues a `tag_scan` dispatcher task (same async UX as the Scheduler)
- Results are cached; the scan button re-runs on demand
- Tags are grouped by namespace prefix (`#action-*`, `#date-*`, `#rank-*`, etc.), all collapsed by default
- Each group shows tag count and total occurrences across the vault
- Per-tag: occurrence count, file count, rename input field, Delete button
- `#outheis-*` tags are hidden (internal system use only)

## Configuration Editor

The Configuration view provides a complete editor for `~/.outheis/human/config.json`:

### General Tab

- **User profile**: Name, email, phone, language, timezone
- **Vaults**: List of vault directories (primary + secondary)

### Providers Tab

Three provider cards (Anthropic, OpenAI, Ollama):
- API key (password field, not stored in plain text in UI)
- Base URL (for custom endpoints or proxies)
- Status indicator (green dot when configured)

### Models Tab

Model alias mapping:
```
fast      → claude-haiku-4-5
capable   → claude-sonnet-4-20250514
reasoning → claude-opus-4-5
```

Add/remove aliases with provider selection.

### Agents Tab

Per-agent configuration:

| Agent | Name | Model | Enabled |
|-------|------|-------|---------|
| relay | ou | capable | ✓ |
| data | zeno | capable | ✓ |
| agenda | cato | capable | ✓ |
| action | hiro | capable | ☐ |
| pattern | rumi | capable | ✓ |
| code | alan | capable | ☐ |

Each agent can use a different model alias (fast/capable/reasoning).

### Signal Tab

Signal transport configuration:
- Enabled toggle
- Phone number (registered with signal-cli)
- CLI path (default: `/usr/local/bin/signal-cli`)
- Whitelist (phone numbers allowed to interact)

## Scheduler

Manage scheduled tasks:

```
┌─ Task Type ─────────┬─ Times ──────────────┬─ Enabled ─┐
│ agenda_review       │ 06:00 12:00 18:00 +  │    ✓      │
│ shadow_scan         │ 03:30              +  │    ✓      │
│ pattern_nightly     │ 04:00              +  │    ✓      │
└─────────────────────┴──────────────────────┴───────────┘
```

- **+ button**: Add another time (auto-increments by 1 hour)
- **× button**: Remove a time (minimum one remains)
- **Checkbox**: Enable/disable task
- **History tab**: View past scheduler events from messages.jsonl

## File Browser

Memory, Skills, Rules, Patterns, Agenda, and Codebase views share a file browser:

```
┌─ Files ───────┬─ Content ──────────────────────────────┐
│ common.md  ✓  │  [Rendered] [Source]                   │
│ relay.md      │                                        │
│ data.md       │  # Common Skills                       │
│               │                                        │
│               │  ## Dates                              │
│               │  Always use ISO format (YYYY-MM-DD)    │
│               │                                        │
└───────────────┴────────────────────────────────────────┘
```

- **Rendered**: Markdown rendered as HTML (via marked.js)
- **Source**: Raw text, editable (contenteditable)
- **Save**: Writes changes back to disk

## Live Updates

The Messages view uses WebSocket for real-time updates:

1. Server watches `messages.jsonl` for changes
2. New lines are parsed and pushed to connected clients
3. Messages appear instantly in the UI

Connection status shown in the status bar:
- `Connected` — WebSocket active
- `Disconnected` — Reconnecting in 3 seconds
- `Error` — Connection failed

## API Endpoints

The server exposes REST endpoints:

### Config
- `GET /api/config` — Read config.json
- `POST /api/config` — Write config.json

### Status
- `GET /api/status` — Dispatcher running, PID, agent count, messages today

### Messages
- `GET /api/messages?limit=50` — Recent messages from messages.jsonl

### Files
- `GET /api/{type}` — List files (type: memory, skills, rules, patterns, agenda, codebase)
- `GET /api/{type}/{filename}` — Read file content
- `PUT /api/{type}/{filename}` — Write file content

### Tags
- `GET /api/tags` — Tag scan results (cached, filtered, sorted lexically)
- `POST /api/tags/scan` — Queue tag_scan dispatcher task, returns conversation_id
- `POST /api/tags/rename` — Rename tag across all vault files
- `POST /api/tags/delete` — Remove tag from all vault files

### Vault Files
- `GET /api/vault/tree` — Recursive tree of all configured vaults
- `GET /api/vault/file?path=` — Read file (text/image/binary detection, wikilinks resolved for .md)
- `PUT /api/vault/file` — Write file content
- `DELETE /api/vault/file?path=` — Delete file
- `GET /api/vault/raw?path=` — Serve raw file (used for inline images and downloads)

### Migration
- `GET /api/migration` — List files in vault/Migration/
- `GET /api/migration/{filename}` — Read file content
- `PUT /api/migration/{filename}` — Write file content
- `POST /api/migration/create` — Create vault/Migration directory
- `POST /api/migration/upload` — Upload file via multipart form

### WebSocket
- `WS /ws` — Live message stream

## File Locations

```
outheis-minimal/
└── webui/
    ├── server.py      # FastAPI backend
    ├── index.html     # HTML structure
    ├── style.css      # Lexend Deca, light/dark mode
    ├── app.js         # View routing, WebSocket, forms
    └── assets/
        ├── logo.svg   # outheis labs logo
        └── logo.png   # Fallback
```

## Design Decisions

### Typography
Single font family (Lexend Deca) in two weights:
- **400** — Body text, labels, inputs
- **500** — Titles, emphasis, agent names

### Color Modes
CSS variables support automatic light/dark mode via `prefers-color-scheme`. The logo inverts in dark mode.

### No Authentication
The UI is localhost-only by design. No login, no sessions. If you can reach port 8080, you have full access.

### No Chat
This is an administration interface, not a chat UI. For chat, use the CLI (`nous chat`) or Signal transport.

## Dependencies

Server-side:
- `fastapi` — Web framework
- `uvicorn` — ASGI server

Client-side:
- `marked.js` — Markdown rendering (CDN)
- Lexend Deca — Typography (Google Fonts)

No build step. No bundler. Plain files served directly.
