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
      "content": "Your fact or preference here",
      "type": "user"
    },
    {
      "content": "Another entry",
      "type": "feedback"
    }
  ]
}
```

**Types:**
- `user` — Facts about you (schedule, roles, preferences)
- `feedback` — How you want outheis to behave
- `context` — Temporary focus (will decay)

### How It Works

1. **Place files** in `~/.outheis/human/memory/seed/`
2. **Pattern Agent runs** (nightly at 04:00, or manually)
3. **Agent processes** each `*.json` file (ignores `x-*.json`)
4. **New entries** are staged in `seed.json`
5. **Processed files** are renamed with `x-` prefix
6. **You approve** entries in `seed.json`
7. **Next run** applies approved entries to memory

### Approving Entries

Edit `~/.outheis/human/memory/seed.json`:

```json
{
  "pending": [
    {
      "content": "Works remotely on Fridays",
      "source": "seed/my-facts.json",
      "status": null,
      "conflicts_with": null,
      "target": "user"
    }
  ]
}
```

Set `status` to:
- `"approved"` — Add to memory, remove from staging
- `"rejected"` — Discard, remove from staging
- `null` — Keep waiting (no action yet)

### Notifications

If Agenda agent is enabled, pending entries are noted in `Exchange.md`.

## User Rules (Direct)

User Rules are markdown files that agents read directly. No approval needed — they're active immediately.

### Directory

```
~/.outheis/human/rules/
├── relay.md      # Rules for Relay agent
├── agenda.md     # Rules for Agenda agent
└── data.md       # Rules for Data agent
```

### Format

```markdown
# User Rules: Agenda

## Daily.md Format

- MAX 10-12 items total
- Dated items have priority

## Processing

- Items from Inbox → Daily.md
- Unclear items → Exchange.md (ask)
```

Rules are merged with system rules. Your rules take precedence.

## Memory vs Rules

| Type | What | Format | Approval |
|------|------|--------|----------|
| Memory (seed) | Facts, preferences | JSON | Required (seed.json) |
| Rules | Behavioral guidelines | Markdown | None (direct) |

Memory = "what I know about you"
Rules = "how I should behave for you"

## Verifying Migration

After placing seed files:

```bash
# Trigger Pattern agent manually (or wait for 04:00)
outheis pattern run

# Check staging
cat ~/.outheis/human/memory/seed.json

# Approve entries, then run again
outheis pattern run

# Verify memory
outheis memory show
```

## Privacy Note

All data in `~/.outheis/human/` stays local. Nothing is transmitted externally. You control what goes in these files.
