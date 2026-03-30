---
title: Migrating Personal Rules
---

# Migrating Personal Rules

*How to bring your existing knowledge into outheis.*

## Overview

outheis learns through:
1. **Direct interaction** — conversations with you
2. **Pattern extraction** — Pattern agent observes and promotes rules
3. **Manual seeding** — you can pre-populate memory and rules

This guide covers option 3: manually adding your existing knowledge so outheis starts smarter.

## Seed Files (Recommended)

The seed workflow lets you stage entries for manual approval before they're added to memory.

### Directory Structure

```
~/.outheis/human/memory/
├── user.json           # Canonical memory (Pattern writes here)
├── feedback.json       # Canonical memory
├── context.json        # Canonical memory
├── seed/               # Your migration files
│   ├── my-facts.json       # Unprocessed (will be read)
│   └── x-my-facts.json     # Processed (ignored)
└── seed.json           # Staging file (Pattern creates this)
```

### Seed File Format

Place `.json` files in `~/.outheis/human/memory/seed/`:

```json
{
  "entries": [
    {
      "content": "User works remotely on Fridays",
      "type": "user"
    },
    {
      "content": "Prefers concise responses without excessive formality",
      "type": "feedback"
    },
    {
      "content": "Currently focused on quarterly planning",
      "type": "context"
    },
    {
      "content": "User speaks German and English fluently"
    }
  ]
}
```

**Types:**
- `user` — Facts about you (roles, relationships, preferences)
- `feedback` — How you want outheis to behave
- `context` — Temporary focus (will decay after 14 days)

If `type` is omitted, Pattern agent infers it from content using heuristics:
- Starts with "User prefers/wants/likes" → `feedback`
- Contains "working on/focused on/currently" → `context`
- Otherwise → `user`

### Processing Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  seed/*.json    │ ──▶ │   seed.json     │ ──▶ │  user.json      │
│  (your files)   │     │   (staging)     │     │  feedback.json  │
└─────────────────┘     └─────────────────┘     │  context.json   │
        │                      │                └─────────────────┘
        │                      │
        ▼                      ▼
┌─────────────────┐     ┌─────────────────┐
│  x-*.json       │     │  Exchange.md    │
│  (processed)    │     │  (notification) │
└─────────────────┘     └─────────────────┘
```

1. **Place files** in `~/.outheis/human/memory/seed/`
2. **Pattern Agent runs** (nightly at 04:00, or manually via `outheis pattern run`)
3. **Agent reads** each `*.json` file (ignores `x-*.json`)
4. **Compares** with existing memory for duplicates and conflicts
5. **New entries** are staged in `seed.json` with `status: null`
6. **Processed files** are renamed with `x-` prefix
7. **Notification** written to Exchange.md (if Agenda enabled)
8. **You review** entries in `seed.json`, set status
9. **Next run** applies approved, discards rejected, keeps null

### Staging File Format

After processing, `seed.json` looks like:

```json
{
  "entries": [
    {
      "content": "User works remotely on Fridays",
      "type": "user",
      "source_file": "my-facts.json",
      "status": null,
      "conflict_with": null
    },
    {
      "content": "User is 36 years old",
      "type": "user",
      "source_file": "my-facts.json",
      "status": null,
      "conflict_with": "User is 35 years old"
    }
  ]
}
```

### Approving Entries

Edit `seed.json` and set `status`:

| Status | Effect |
|--------|--------|
| `null` | Keep waiting (no action) |
| `"approved"` | Add to memory, remove from staging |
| `"rejected"` | Discard, remove from staging |

For conflicts:
- **Approve** → new entry replaces existing
- **Reject** → keep existing entry
- **Null** → defer decision

Example approval:

```json
{
  "content": "User works remotely on Fridays",
  "type": "user",
  "source_file": "my-facts.json",
  "status": "approved",
  "conflict_with": null
}
```

### Notifications

If Agenda agent is enabled, Pattern agent writes to Exchange.md:

```markdown
## 2026-03-30T04:15:00 – Seed Review

> 5 new memory entries from my-facts.json need your review.
> 
> Please check ~/.outheis/human/memory/seed.json and set status to "approved" or "rejected".

**Your response:**

```

No pressure to respond immediately — entries stay in staging until you decide.

## User Rules (Direct)

User Rules are markdown files that agents read directly. No approval needed — they're active immediately.

### Directory

```
~/.outheis/human/rules/
├── relay.md      # Rules for Relay agent (conversation style)
├── agenda.md     # Rules for Agenda agent (scheduling)
├── data.md       # Rules for Data agent (search behavior)
└── pattern.md    # Rules for Pattern agent (extraction)
```

### Format

```markdown
# User Rules: Agenda

## Daily.md Format

- MAX 10-12 items total
- Dated items have priority
- Use 🔴 for time-bound, 🟠 for flexible

## Processing

- Items from Inbox → Daily.md
- Unclear items → Exchange.md (ask, don't guess)
- Honor user's emoji conventions

## Language

- Respond in user's language
- Keep task descriptions concise
```

Rules are merged with system rules. User rules take precedence for behavioral preferences; system rules define capabilities and boundaries.

### Rule Promotion

Stable patterns in feedback memory can be promoted to rules by the Pattern agent:

1. Pattern agent notices consistent feedback ("User always prefers X")
2. Checks if pattern has been stable over multiple weeks
3. Writes rule to appropriate `rules/{agent}.md` with timestamp comment
4. Optionally notifies via Exchange.md

Example promoted rule:

```markdown
- Respond in German unless user writes in English  <!-- 2026-03-28 promoted from feedback -->
```

## Memory vs Rules

| Aspect | Memory (seed) | Rules |
|--------|---------------|-------|
| What | Facts, observations | Behavioral guidelines |
| Format | JSON | Markdown |
| Approval | Required (seed.json) | None (direct) |
| Volatility | Can change, can decay | Stable once set |
| Example | "User is 35 years old" | "Always respond in German" |

Memory = "what I know about you"
Rules = "how I should behave for you"

## Verifying Migration

After placing seed files:

```bash
# Check seed directory
ls ~/.outheis/human/memory/seed/

# Trigger Pattern agent manually (or wait for 04:00)
outheis pattern run

# Check what was staged
cat ~/.outheis/human/memory/seed.json | jq .

# Edit seed.json, set status to "approved" or "rejected"

# Run again to apply
outheis pattern run

# Verify memory
outheis memory show
```

### Checking Status

```bash
# See processed seed files
ls ~/.outheis/human/memory/seed/x-*

# Check canonical memory
cat ~/.outheis/human/memory/user.json | jq .entries

# Check rules
cat ~/.outheis/human/rules/relay.md
```

## Example: Claude.ai Migration

If you have knowledge in Claude.ai you want to transfer:

1. **Create seed file** from your Claude.ai memories:

```json
{
  "entries": [
    {"content": "User is a software engineer", "type": "user"},
    {"content": "User has two children", "type": "user"},
    {"content": "Prefers technical depth over simplification", "type": "feedback"},
    {"content": "Working on quarterly planning", "type": "context"}
  ]
}
```

2. **Save as** `~/.outheis/human/memory/seed/claude-export.json`

3. **Run Pattern agent:** `outheis pattern run`

4. **Review** `seed.json`, approve entries

5. **Run again** to apply

6. **Verify:** `outheis memory show`

## Privacy Note

All data in `~/.outheis/human/` stays local:
- Nothing is transmitted to external services
- Memory files are plain JSON you can read and edit
- Seed files remain on your machine (never uploaded)
- You control what outheis knows

Delete any file at any time — outheis adapts to what remains.
