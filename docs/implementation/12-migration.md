
# Migration

*How to bring your existing knowledge into outheis.*

---

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
| "memory migrate" | Parse Migration/ files, write candidates to Migration/Exchange.md |
| "memory traits" | Show current memory and rules |
| "what do you know about me" | Same, conversational |
| "write rule: ..." | Add rule directly, bypassing Pattern agent |

No CLI commands needed. Just talk to outheis.

## File Formats

### JSON Files

```json
{
  "entries": [
    {
      "content": "User works as project lead",
      "type": "user"
    },
    {
      "content": "Keep answers short and direct",
      "type": "feedback"
    },
    {
      "content": "Currently working on outheis",
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
- Lives in Vienna
- Works as software developer

## feedback
- Keep answers short
- Prefer plain text output

## rule:agenda

- MAX 10 Items in Daily.md
- No meetings before 10:00

## rule:data

- Also search PDF files
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

### 3. Trigger migration

**Via chat:** say `memory migrate`

**Via WebUI:** open the Migration view and click **Run now** in the top-right corner. The button is available whether or not the drop zone is visible.

outheis parses all files in `vault/Migration/`, deduplicates candidates against existing memory via LLM, and writes consolidated items as a block into `vault/Migration/Exchange.md`. Proposals are grouped by source file and annotated with the tags found in that file:

```
<!-- outheis:migration:start -->
## Migration Proposals — 2026-04-05 14:30

*`[x]` accept · `[-]` reject · `[ ]` leave open · then run `memory migrate` again*

### prototype-user_markus.md  #unit-self #source-human

- [ ] Works as Director Innovation Lab [user]
- [ ] Prefers short, direct answers [feedback]

### prototype-vault_workflow.md  #unit-work #topic-vault

- [ ] Respond in German [rule:relay]

<!-- outheis:migration:end -->
```

Duplicates are always expected — the LLM deduplication step handles them. Only new or distinct items appear in the block.

### 4. Review Migration/Exchange.md

Open `vault/Migration/Exchange.md` — the dedicated file for migration approvals. Each Exchange.md is scoped to its directory: Migration/ for memory migration, Agenda/ for async communication with cato, Codebase/ for code proposals.

Mark each item:

```
- [x] Works as Director Innovation Lab [user]
- [x] Prefers short, direct answers [feedback]
- [-] Respond in German [rule:relay]

- [ ] Lives in Vienna [user]
```

- `[x]` — apply to memory/rules
- `[-]` — discard
- `[ ]` — leave open for next round

### 5. Say "memory migrate" Again

```
You: memory migrate
Ou: Migration processed:
    - 2 accepted
    - 1 rejected
    - 1 still open
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
You: write rule: no meetings before 10:00
Ou: ✓ Rule added to agenda: no meetings before 10:00
```

Or specify the agent:

```
You: write rule for relay: always respond in plain text
Ou: ✓ Rule added to relay: always respond in plain text
```

This bypasses Pattern agent and writes directly to `~/.outheis/human/rules/{agent}.md`.

## Viewing Current State

To see what outheis knows:

```
You: memory traits

Ou: Recognized traits:

    ## Identity
      • User works as project lead
      • User lives in Vienna

    ## Preferences
      • Keep answers short and direct
      • Prefer plain text output

    ## Established rules
      • agenda: 2 rules
      • relay: 1 rule
```

Or more conversationally:

```
You: what do you know about me?
```

## Memory vs Rules

| Aspect | Memory | Rules |
|--------|--------|-------|
| Location | `~/.outheis/human/memory/` | `~/.outheis/human/rules/` |
| Format | JSON | Markdown |
| Volatility | Can change, context decays | Stable once set |
| Example | "User is 35" | "Respond in plain text" |

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
