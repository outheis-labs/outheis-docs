---
title: Memory
---

# Memory

*What outheis remembers about you — and how.*

## Memory vs. Vault

outheis maintains two separate knowledge stores:

| | Memory | Vault |
|---|--------|-------|
| **Purpose** | Meta-knowledge about you | Your work content |
| **Contains** | Facts, preferences, context | Documents, notes, projects |
| **Updated by** | Agents during interaction, Pattern agent, explicit markers | You directly |
| **Format** | Structured JSON | Markdown files |

**Memory** answers: *Who is this person? How do they want me to work?*

**Vault** answers: *What information do they have?*

## Memory Types

### user

Personal facts that don't change often.

Examples:

- "User is 35 years old"
- "Children: Leo (8) and Emma (5)"

- "Lives in Munich"
- "Works as a software engineer"

**Decay:** Permanent (until corrected)

### feedback

How you want outheis to behave.

Examples:

- "Prefers short, direct answers"
- "Respond in German unless asked otherwise"
- "Don't explain technical concepts — user is an expert"

**Decay:** Permanent (until corrected)

### context

What you're currently focused on.

Examples:

- "Working on Project Alpha mobile app"
- "Preparing for conference talk next week"
- "Learning Japanese"

**Decay:** 14 days by default (fades when no longer relevant)

## How Memory is Created

Memory is written through three channels:

### 1. Explicit Marker (`!`)

Prefix any message with `!` to store it immediately:

```
! I am 35 years old
→ Stored in user memory, agent responds with this knowledge

! please always give short answers
→ Stored in feedback memory, agent adapts immediately

! I'm currently working on Project Alpha
→ Stored in context memory (14 day decay)
```

Classification happens automatically based on content. The `!` marker is a shorthand — it's equivalent to saying "remember this" but shorter. The agent both stores the information AND uses it immediately in the current conversation.

### 2. Agents During Interaction

Agents can recognize when you share something worth remembering:

- You mention your birthday → agent may store it
- You express a preference → agent may store it
- You describe a current project → agent may store it as context

This happens through judgment, not rigid rules. Agents are instructed to notice relevant information but not to over-extract. Not every statement becomes a memory — only what seems genuinely useful for future interactions.

### 3. Pattern Agent Extraction

The Pattern agent (rumi) runs nightly at 04:00 and:

1. Reviews recent conversations
2. Extracts memorable information agents may have missed
3. Consolidates duplicates and resolves contradictions
4. Assigns confidence scores
5. Cleans up expired entries
6. Considers promoting stable patterns to User Rules

You can trigger this manually: `outheis pattern`

## Memory Consolidation

Over time, memory can accumulate duplicates or contradictory entries. The Pattern agent handles this during its scheduled run:

- **Duplicates**: "Has pending tasks: X, Y" and "Current pending tasks: X, Y" → keeps the newer one

- **Contradictions**: "User is 35" and "User is 36" → keeps the more recent or explicitly-marked one

- **Superseded entries**: Context that's been updated → removes the older version

This is not a mechanical process — the Pattern agent uses judgment to decide what to consolidate, erring on the side of keeping information when uncertain.

## Temporal Awareness

Not everything should be remembered forever.

**Stored as permanent fact:**

- "User has two children"
- "Prefers formal communication"

**NOT stored (temporary state):**

- "User seems frustrated today"
- "User is tired"
- "User is stressed about deadline"

All agents are instructed to distinguish stable traits from temporary moods. A frustrated message isn't a personality trait — it's a moment.

## Viewing and Editing Memory

### CLI

```bash
# View all memory
outheis memory

# Add entry manually
outheis memory --add "user:My birthday is March 15"

# Clear a type
outheis memory --clear context
```

### Display Format

```
Memory
----------------------------------------

[user] (3 entries)
  1. User is 35 years old
  2. Children: Leo (8), Emma (5) [!]
  3. Lives in Munich [90%]

[feedback] (1 entries)
  1. Prefers short answers [!]

[context] (2 entries)
  1. Working on Project Alpha [↓12d]
  2. Preparing conference talk [↓5d]
```

Markers:

- `[!]` — Explicitly stored via `!` marker
- `[90%]` — Confidence below 100%
- `[↓12d]` — Expires in 12 days

## Storage

```
~/.outheis/human/memory/
├── user.json           # Personal facts
├── feedback.json       # Working preferences
├── context.json        # Current focus
└── pattern/            # Pattern agent's learning
    └── strategies.md
```

Each memory file contains timestamped entries with metadata:

```json
{
  "type": "user",
  "updated_at": "2025-03-28T14:30:00",
  "entries": [
    {
      "content": "User is 35 years old",
      "created_at": "2025-03-28T14:30:00",
      "updated_at": "2025-03-28T14:30:00",
      "confidence": 1.0,
      "source_count": 1,
      "decay_days": null,
      "is_explicit": true
    }
  ]
}
```

## Migration

To import existing knowledge from Claude.ai or other sources, use the Migration workflow. See [Migration](migration.md) for details.

Quick summary:
1. Create `vault/Migration/` with your `.json` or `.md` files
2. Say "memory migrate" in chat
3. Review and mark entries in `Migration.md`
4. Say "memory migrate" again to apply
5. Delete `vault/Migration/` when done

## Pattern Agent Meta-Memory

The Pattern agent has its own memory in `~/.outheis/human/memory/pattern/`. This is where it stores:

- What extraction strategies work for this user
- Patterns in communication style
- Meta-insights about its own process

This memory doesn't decay — it's how the Pattern agent gets better over time at understanding what matters to you.

## Integration with Agents

Memory is injected into agent system prompts automatically:

```
# Memory

## About the user
- User is 35 years old
- Children: Leo (8), Emma (5)

## Working preferences
- Prefers short answers

## Current context
- Working on Project Alpha
```

Agents use this naturally — they don't announce "I remember that..." but simply know.

## Correction

If outheis has wrong information:

1. **Explicit correction:** `! I'm 36, not 35`
2. **CLI edit:** `outheis memory --clear user` then re-add
3. **Direct file edit:** Modify JSON in `~/.outheis/human/memory/`

Explicit (`!`) entries take precedence — agents won't override them with lower-confidence extractions.

---

## Rules

Rules are the stable distillation of memory — behavioral principles that shape how outheis works with you.

### Two Layers

| | System Rules | User Rules |
|---|--------------|------------|
| **Source** | Developers | Emergent from interaction |
| **Purpose** | Boundaries, capabilities | Style, preferences |
| **Location** | `src/outheis/agents/rules/` | `~/.outheis/human/rules/` |
| **Mutability** | Changes with code updates | Grows over time |

**System rules** define what an agent *can* do — architectural constraints.

**User rules** define how an agent *should* do it — your working style.

### How User Rules Emerge

User rules aren't written by you directly. They emerge from memory through the Pattern agent.

The Pattern agent reviews memory during its nightly run and looks for patterns that have become stable enough to codify as rules. This isn't a mechanical process with fixed thresholds — the agent uses judgment:

- A strong preference stated clearly once might become a rule
- Something mentioned many times casually might not
- Explicit corrections always matter more than inferences

When the Pattern agent identifies a stable pattern, it writes it to `~/.outheis/human/rules/{agent}.md`:

```markdown
# User Rules for Relay Agent

- User prefers concise responses  <!-- 2026-03-30 -->
- Respond in German unless the user writes in English  <!-- 2026-03-28 -->
```

### Memory vs. Rules

| | Memory | Rules |
|---|--------|-------|
| **Timescale** | Days to weeks | Months to years |
| **Volatility** | Can expire, frequently updated | Stable once established |
| **Content** | Facts, observations | Principles, patterns |
| **Example** | "User is 35 years old" | "User prefers brevity" |

Memory is *what we know*. Rules are *how we work*.

### Storage

```
~/.outheis/human/rules/
├── common.md      # Applies to all agents
├── relay.md       # Conversation style
├── data.md        # Search behavior
├── agenda.md      # Scheduling preferences
└── pattern.md     # Extraction behavior
```

### CLI

```bash
# View all rules
outheis rules

# View rules for specific agent
outheis rules relay

# View only user rules (emergent)
outheis rules --user

# View only system rules (architectural)
outheis rules --system
```

### Coherent Personality

Although outheis consists of five agents, you experience one assistant. Rules maintain this coherence:

- **Common rules** ensure consistent behavior across all agents
- **Agent-specific rules** allow appropriate specialization
- **User rules** adapt the entire system to your working style

Over time, outheis develops a stable personality — not programmed, but grown from working together.

