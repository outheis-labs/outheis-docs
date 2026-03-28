---
title: Skills
---

# Skills

*What agents know about how to act.*

## Overview

Skills are an agent's internal capabilities — strategies, methods, heuristics for accomplishing tasks. Unlike rules (external instructions), skills represent the agent's own knowledge about *how* to do things.

## The Three Stores

| Store | What it contains | Who writes | Example |
|-------|------------------|------------|---------|
| **memory** | Facts, observations, state | Pattern Agent | "User lives in Munich" |
| **rules** | Instructions, constraints | User, Pattern Agent | "Respond in German" |
| **skills** | Capabilities, strategies | Agent itself, Pattern Agent | "Date formats I recognize: ..." |

## How They Combine

When an agent processes a request:

```
Agent receives message
    ↓
Skills: "How do I approach this?"
    ↓
Rules: "What constraints apply?"
    ↓
Memory: "What do I know about this user/context?"
    ↓
Action
```

## Directory Structure

```
# System skills (in package, read-only)
src/outheis/agents/skills/
├── common.md       # Shared by all agents
├── relay.md        # Relay-specific
├── agenda.md       # Agenda-specific
├── data.md         # Data-specific
└── pattern.md      # Pattern-specific

# User skills (learned, mutable)
~/.outheis/human/skills/
├── common.md       # Learned strategies (all agents)
├── relay.md        # Relay refinements
├── agenda.md       # Agenda refinements
└── data.md         # Data refinements
```

## System Skills

Base capabilities defined by the developer. Examples:

**Agenda Agent:**

- Date format recognition
- Daily.md structure
- Inbox processing strategy
- Exchange.md usage

**Data Agent:**

- File search strategies
- Tag interpretation
- JSON structure parsing
- Result ranking

**Relay Agent:**

- Request routing
- Tool selection
- Migration handling
- Correction processing

**Pattern Agent:**

- Memory extraction
- Rule promotion
- Conflict detection
- Self-evaluation

## User Skills (Learned)

Skills refined through use and correction. Written by:

1. **Agent itself** — when a strategy works consistently
2. **Pattern Agent** — when observing stable patterns

Example evolution:

```markdown
# ~/.outheis/human/skills/agenda.md

## Date Formats

- User writes dates as DD.MM.YYYY, not MM/DD/YYYY
- "nächste Woche" means Monday, not 7 days from now

## Daily Structure

- User prefers 🧘/🔴/🟠 emoji sections
- No "Evening" section needed — user doesn't use it
```

## Skill vs. Rule

| Aspect | Skill | Rule |
|--------|-------|------|
| Perspective | "How I do this" | "What I should observe" |
| Origin | Learned by agent | Given by user/Pattern |
| Scope | Internal capability | External constraint |
| Example | "I recognize dates like..." | "Always respond in German" |

Rules constrain behavior from outside.
Skills enable behavior from inside.

## Loading Order

In the system prompt:

1. **Skills** (common + agent-specific)
2. **Rules** (common + agent-specific)
3. **Memory context** (user + feedback + context)

System versions first, user versions extend/override.

## Writing Skills

Skills should be:

- **Concrete**: Specific patterns, not vague principles

- **Actionable**: Tell the agent what to do

- **Learnable**: Can be refined through feedback

Good skill:
```markdown
## Date Recognition
- "morgen" → tomorrow's date
- "nächsten Montag" → next Monday (not today if today is Monday)
- "24.03.2026" → parse as YYYY-MM-DD internally
```

Weak skill:
```markdown
## Dates
- Understand dates properly
- Be smart about date parsing
```

## Skill Refinement

When a user corrects an agent:

1. Agent stores correction in memory (feedback)
2. Pattern Agent observes repeated corrections
3. If stable: promotes to user skill
4. Skill now influences all future actions

This creates a learning loop where corrections become permanent improvements.

### Distillation Triggers

The Pattern Agent uses judgment, not fixed thresholds. But these conditions indicate a pattern is ready:

- **3+ similar observations** → pattern detectable
- **Repeated corrections** → principle extractable
- **Stable preference** → ready for skill

A strong preference stated clearly once may become a skill. Something mentioned casually many times may not. Explicit corrections always carry more weight than inferred patterns.

### Quality Criteria

A good skill:

- **Directs attention** — tells the agent what to notice, not what to do
- **Generalizes** — applies beyond the specific instance that prompted it
- **Replaces** — makes one or more memory entries unnecessary

If a skill doesn't replace anything, it may be too specific. If it doesn't direct attention, it may be a rule in disguise.
