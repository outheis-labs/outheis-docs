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
├── data.md               # Rules for Data agent
└── Migration.md          # ← Created by outheis
```

This directory is **temporary** — create it when you have something to migrate, delete it when done.

## Chat Commands

All migration happens through natural conversation:

| You say | What happens |
|---------|--------------|
| "memory migrate" | Process Migration/ files, create Migration.md |
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

In chat with outheis:

```
Du: memory migrate
Ou: Migration verarbeitet:
    - 3 Dateien geparst
    - 12 Einträge warten auf Bestätigung
    
    Prüfe vault/Migration/Migration.md
```

### 4. Review Migration.md

outheis creates `Migration.md`:

```markdown
# Migration

*Zuletzt aktualisiert: 2026-03-30 14:30*

Markiere Einträge:
- `[x]` → übernehmen
- `[-]` → ablehnen
- `[ ]` → noch offen

---

## Offen

- [ ] User arbeitet bei senswork [user]
- [ ] Antworte knapp und direkt [feedback]
- [ ] MAX 10 Items in Daily.md [rule:agenda]
- [ ] User ist 35 Jahre alt [user]

---

## Statistik

- Übernommen: 0
- Abgelehnt: 0
```

Edit the file — mark entries:

```markdown
- [x] User arbeitet bei senswork [user]
- [x] Antworte knapp und direkt [feedback]
- [x] MAX 10 Items in Daily.md [rule:agenda]
- [-] User ist 35 Jahre alt [user]
```

### 5. Say "memory migrate" Again

```
Du: memory migrate
Ou: Migration verarbeitet:
    - 3 übernommen
    - 1 abgelehnt
    - 0 noch offen
```

Adopted entries are now in memory/rules. Rejected entries are discarded.

### 6. Delete Migration Directory

When done:

```bash
rm -rf ~/Documents/Vault/Migration
```

outheis doesn't mind — the directory is purely transient.

## Processed Files

After parsing, files get an `x-` prefix:

```
vault/Migration/
├── x-claude-export.json    # Processed
├── x-preferences.md        # Processed
├── Migration.md            # Still active
```

This prevents re-processing. Delete the `x-` files yourself when ready.

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
