---
title: Migration
---

# Migration

*How to bring your existing knowledge into outheis.*

## Overview

outheis learns through:
1. **Direct interaction** — conversations with you
2. **Pattern extraction** — Pattern agent observes and promotes rules
3. **Manual migration** — import existing knowledge via vault

This guide covers option 3: migrating data from Claude.ai or other sources.

## The Migration Directory

Place files to migrate in your vault:

```
vault/Migration/
├── claude-export.json    # Your data
├── preferences.md        # Your rules/preferences
└── data.md               # Rules for Data agent
```

This directory is **temporary** — create it when you have something to migrate, delete it when done.

## Chat Commands

All migration happens through natural conversation:

| You say | What happens |
|---------|--------------|
| "memory migrate" | Parse Migration/ files, write candidates to Exchange.md |
| "migriere memory" | Same, in German |
| "memory traits" | Show current memory and rules |
| "zeige traits" | Same, in German |
| "was weißt du über mich" | Same, conversational |
| "schreibe regel: ..." | Add rule directly, bypassing Pattern agent |

No CLI commands needed. Just talk to outheis.

## File Formats

### JSON Files

```json
{
  "entries": [
    {
      "content": "User arbeitet bei senswork",
      "type": "user"
    },
    {
      "content": "Antworte knapp und direkt",
      "type": "feedback"
    },
    {
      "content": "Arbeitet gerade an outheis",
      "type": "context"
    }
  ]
}
```

**Types:**
- `user` — Facts about you (permanent)
- `feedback` — How you want outheis to behave (permanent)
- `context` — Current focus (decays after 14 days)

If `type` is omitted, outheis infers from content.

### Markdown Files

```markdown
# Preferences

## user
- Lebt in München
- Arbeitet als Software-Entwickler

## feedback
- Antworte immer auf Deutsch
- Bevorzuge kurze Antworten

## rule:agenda
- MAX 10 Items in Daily.md
- Keine Meetings vor 10 Uhr

## rule:data
- Durchsuche auch PDF-Dateien
```

Sections map to memory types or rules:
- `## user`, `## feedback`, `## context` → Memory
- `## rule:agenda`, `## rule:data`, `## rule:relay` → Rules files

Any markdown or JSON structure is acceptable — outheis uses LLM parsing and does not require a specific schema.

## Workflow

### 1. Create Migration Directory

```bash
mkdir ~/Documents/Vault/Migration
```

### 2. Add Your Files

Copy your data:
- Export from Claude.ai → `claude-export.json`
- Your preferences → `preferences.md`
- Agent-specific rules → `agenda.md`, `data.md`

### 3. Say "memory migrate"

outheis parses all files in `vault/Migration/`, deduplicates candidates against existing memory via LLM, and writes consolidated items as a block into `vault/Agenda/Exchange.md`:

```
<!-- outheis:migration:start -->
## Migration-Vorschläge

*2026-04-03 14:30 — Bitte prüfen und markieren:*
*`[x]` übernehmen · `[-]` ablehnen · `[ ]` offen lassen*
*Anschließend: `memory migrate` erneut ausführen.*

- [ ] Works as Director Innovation Lab [user]
- [ ] Prefers short, direct answers [feedback]
- [ ] Respond in German [rule:relay]

<!-- outheis:migration:end -->
```

Duplicates are always expected — the LLM deduplication step handles them. Only new or distinct items appear in the block.

### 4. Review Exchange.md

Open `vault/Agenda/Exchange.md` — the same file you already use for async communication with outheis. The migration block appears at the top or inline, clearly delimited.

Mark each item:

```
- [x] Works as Director Innovation Lab [user]
- [x] Prefers short, direct answers [feedback]
- [-] Respond in German [rule:relay]
- [ ] Lebt in München [user]
```

- `[x]` — apply to memory/rules
- `[-]` — discard
- `[ ]` — leave open for next round

Cato (agenda agent) ignores the migration block when processing Exchange.md.

### 5. Say "memory migrate" Again

```
Du: memory migrate
Ou: Migration verarbeitet:
    - 2 übernommen
    - 1 abgelehnt
    - 1 noch offen
```

- `[x]` items are written to memory and rules
- `[-]` items are discarded
- `[ ]` items remain in the block for the next round
- The block is removed from Exchange.md once all items are resolved (or on your request)

### 6. Processed Source Files

After parsing, source files in `vault/Migration/` get an `x-` prefix:

```
vault/Migration/
├── x-claude-export.json    # Processed
├── x-preferences.md        # Processed
```

This prevents re-processing. Delete the `x-` files yourself when ready, or use the WebUI Migration view.

## WebUI Migration View

The Migration view in the Web UI provides:
- Full list of files in `vault/Migration/`
- View and edit each file directly
- Drop zone for uploading new migration files

Use it to add files without leaving the browser, or to inspect what has already been processed.

## Direct Rule Writing

To add a rule immediately without the Migration workflow:

```
Du: schreibe regel: antworte immer auf Deutsch
Ou: ✓ Regel hinzugefügt zu relay: antworte immer auf Deutsch
```

Or specify the agent:

```
Du: schreibe regel für agenda: keine Meetings vor 10 Uhr
Ou: ✓ Regel hinzugefügt zu agenda: keine Meetings vor 10 Uhr
```

This bypasses Pattern agent and writes directly to `~/.outheis/human/rules/{agent}.md`.

## Viewing Current State

To see what outheis knows:

```
Du: memory traits

Ou: Erkannte Eigenschaften:

    ## Identität
      • User arbeitet bei senswork
      • User lebt in München

    ## Präferenzen
      • Antworte knapp und direkt
      • Bevorzuge deutsche Sprache

    ## Etablierte Regeln
      • agenda: 2 Regeln
      • relay: 1 Regel
```

Or more conversationally:

```
Du: was weißt du über mich?
```

## Memory vs Rules

| Aspect | Memory | Rules |
|--------|--------|-------|
| Location | `~/.outheis/human/memory/` | `~/.outheis/human/rules/` |
| Format | JSON | Markdown |
| Volatility | Can change, context decays | Stable once set |
| Example | "User ist 35" | "Antworte auf Deutsch" |

Memory = "what I know about you"
Rules = "how I should behave"

Both are populated through Migration or through ongoing conversation.

## Privacy

All data stays local:
- Migration files are in your vault
- Memory is in `~/.outheis/human/memory/`
- Rules are in `~/.outheis/human/rules/`
- Nothing is transmitted externally

Delete any file at any time — outheis adapts to what remains.
