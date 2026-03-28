---
title: Alan
---

# Alan

*Code intelligence for development environments.*

## What alan does

alan is outheis's code agent. It reads locally available source code, answers questions about implementation, and proposes improvements through a structured review workflow.

**alan is a development-only agent. It is never active in production environments.**

## The Codebase Workflow

alan stages all proposals in `vault/Codebase/`, mirroring the pattern established by cato's `vault/Agenda/`:

```
vault/Codebase/
├── Exchange.md          # proposals for review
└── <staged files>       # modified files or diffs for context
```

### Exchange.md

Each proposal from alan is an entry in `vault/Codebase/Exchange.md`:

```markdown
## 2026-04-01 — Beschreibung des Vorschlags

**Type:** refactor | bugfix | improvement | answer
**Files:** src/outheis/agents/data.py
**Status:** proposed | approved | rejected | discussing

### Summary
Was wird vorgeschlagen und warum.

### Proposed Change
Verweis auf staged file oder inline diff.

### Discussion
(Deine Antworten und Rückfragen kommen hier hin)
```

You respond under "Discussion", approve or reject with a keyword (`approved`, `rejected`), and alan picks up the decision at the next run.

### Staged Files

For non-trivial changes, alan writes the modified file to `vault/Codebase/<filename>` alongside the Exchange.md entry. Review the diff, then respond in Exchange.md.

## Responsibilities

### Code Introspection

Answer questions about how outheis is implemented. Examples:

- "Wie funktioniert der Dispatcher?"
- "Wo wird memory.json geschrieben?"
- "Was passiert wenn ich `@zeno` verwende?"

alan reads source files, traces call paths, and explains logic — without making any changes.

### Improvement Proposals

Respond to requests or proactively identify:

- Refactoring opportunities
- Bug fixes
- Inconsistencies between documentation and implementation

All proposals go through Exchange.md. alan never modifies `src/` directly.

### Code Search

Find implementations, patterns, and references across the local codebase:

- "Zeig mir alle Stellen wo Vault-Dateien gelesen werden"
- "Welcher Agent ist für Scheduling zuständig?"
- "Wie ist das Tool `append_file` implementiert?"

## Tools

| Tool | Purpose |
|------|---------|
| `read_file(path)` | Read any local source file |
| `search_code(query, path)` | Search for patterns, function names, identifiers |
| `list_files(path)` | Explore directory structure |
| `write_vault(path, content)` | Write to `vault/Codebase/` only |
| `append_vault(path, content)` | Append to Exchange.md |
| `load_skill(topic)` | Load alan-specific skills on demand |

alan has **read access** to any local path. **Write access is restricted to `vault/Codebase/`.**

## Context at Startup

alan receives at invocation:

- A code index of the target repository (file tree + brief descriptions)
- Current contents of `vault/Codebase/Exchange.md`
- Skills from `agents/skills/code.md`

For large repositories, full file contents are fetched on demand via `read_file` — the index provides orientation.

## Asking alan

Invoke directly:

```
@alan wie ist der Dispatcher implementiert?
@alan schlage eine Verbesserung für die Vault-Suche vor
```

Or naturally in chat — ou detects code-related questions and delegates to alan automatically.

## Availability

alan is registered in the dispatcher only when `config.json` contains:

```json
{
  "agents": {
    "code": {
      "name": "alan",
      "model": "capable",
      "enabled": true
    }
  }
}
```

Note: The config key is `code` (function name), the display name is `alan` (persona).

Production deployments omit this entry. alan is never loaded by default.

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | false | Must be explicitly enabled |
| `model` | capable | Use a capable model — code understanding benefits from it |

## Storage

```
vault/Codebase/
├── Exchange.md           # Open proposals and decisions
└── <staged files>        # Proposed changes awaiting review
```

## Integration with Other Agents

**Relay (ou)** detects code questions and delegates to alan. Routes `@alan` prefix directly.

**Data Agent (zeno)** handles vault and personal data. alan handles source code. The domains do not overlap.

**Pattern Agent (rumi)** can observe alan's proposal history and extract patterns — e.g., recurring refactoring suggestions may indicate a deeper structural issue worth noting.

## Design Notes

- The `vault/Codebase/Exchange.md` pattern is intentionally parallel to `vault/Agenda/Exchange.md`. The interaction model is the same: outheis proposes, you decide.

- Write access restricted to `vault/Codebase/` is enforced at the tool level, not by prompt instruction alone.
- alan is deliberately absent from production. Code introspection and proposal workflows are development concerns only.
