
# Agenda

*Time management through three simple files.*

---

## The Three Files

outheis manages your schedule through three Markdown files in your vault:

```
vault/Agenda/
├── Agenda.md     # Today: schedule, tasks, notes
├── Exchange.md   # Async dialogue: system ↔ user
├── Shadow.md     # Chronological vault index (auto-generated)
└── Backlog.md    # Priority-sorted view of Shadow.md (on-demand)
```

### Agenda.md

Your day at a glance. The default template:

```markdown
⛅ [Weekday, DD.MM.YYYY]
*Refresh: HH:MM*

---
## 🧘 Personal

- [ ]

---
## 📅 Today

---
## 🗓️ This Week

---
## 💶 Cashflow
```

The structure is user-configurable via `DailyTemplate.md` in your vault. Once established, outheis preserves it exactly on each refresh — only the content changes, never the structure.

outheis reads this file, understands your commitments, and can answer questions like "am I free this afternoon?" or "what's on tomorrow?"

### Exchange.md

Asynchronous dialogue between you and outheis:

```markdown
# Exchange

---

## 2026-04-08T10:15:00 – Question

Which day works for the meeting with X?

- [ ] Accept
- [ ] Reject

---
```

Write a `>` reply directly below an open item, or check a box — cato processes it on the next run.

## Hourly Review

At 55 minutes past each hour (configurable), the Agenda agent runs:

### Conditional Execution

Before processing, outheis checks file hashes:

```
~/.outheis/human/cache/agenda/hashes.json
```

If nothing changed since the last run, no LLM call is made. This saves API costs while maintaining responsiveness.

**Exceptions:** Morning (04:55) and evening (23:55) runs are unconditional to handle day transitions properly.

### Processing Steps

1. **Hash check** — Compare current files with stored hashes
2. **Process Inbox** — Parse items, move tasks to Daily, unclear → Exchange
3. **Check Exchange** — Look for your responses, extract learnings
4. **Review Daily** — Notice annotations, comments, completions
5. **Update hashes** — Store new file hashes for next comparison
6. **Cache diffs** — Save `.prev` versions for debugging

### Annotations

A `>` line written immediately below an item is a direct instruction to cato:

```markdown
#action-required #topic-admin
Call supplier about delivery date
> done, confirmation expected by Friday
```

cato classifies each annotation into one of three types:

| Type | Identified by | Action |
|---|---|---|
| **Completion** | done, finished, confirmed, resolved | Remove item from Agenda.md |
| **Postpone** | later, next week, [future date] | Remove from Agenda.md, update date in Shadow.md |
| **Correction** | explanation, rephrasing, new context | Rewrite item in place, keep it |

The `>` line is always removed after processing. See [Annotation Feedback Loop](annotation-feedback.html) for how annotations feed into long-term memory.

### Time Window

By default, hourly reviews only run between 04:55 and 23:55. No reviews during night hours. Configurable in `config.json`:

```json
{
  "schedule": {
    "agenda_review": {
      "enabled": true,
      "time": ["04:55", "05:55", "06:55", "...", "23:55"]
    }
  }
}
```

## Manual Refresh

You can trigger an immediate agenda update:

- "update daily"
- "refresh agenda"

This bypasses the hash check and runs a full review immediately. Useful after making many changes or before asking schedule questions.

## Creating the Structure

When outheis starts and the Agenda agent is enabled, it creates the directory automatically. You can also create manually:

```bash
mkdir -p ~/Documents/Vault/Agenda
touch ~/Documents/Vault/Agenda/{Agenda,Exchange}.md
```

## Asking About Your Schedule

Once set up, you can ask:

- "What's on today?"
- "Am I free tomorrow afternoon?"
- "When is my next appointment with X?"
- "Add: meeting with Y on Friday at 10"

outheis reads your Agenda files and responds naturally.

### Read Queries

When asked to show the agenda ("Agenda", "what's on today", "show my agenda"), cato returns the content of Daily.md verbatim — no reformatting, no summarizing. The file content is the answer. Relay passes it through directly without a second LLM call.

## Integration with Other Agents

**Relay (ou)** routes schedule questions to Agenda. Read queries ("Agenda", "what's on today") are routed directly to cato, which returns Agenda.md verbatim. Write/update queries go through the full tool loop.

**Data Agent (zeno)** can search your vault but doesn't write to Agenda files.

**Action Agent (hiro)** can execute tasks (send emails, create calendar events) but Agenda manages what's scheduled.

**Pattern Agent (rumi)** observes your scheduling patterns and may:

- Create rules like "User prefers no meetings before 10:00"

- Notice recurring tasks and suggest automation
- Write to Exchange.md when seed files need approval

## Storage

```
vault/Agenda/
├── Agenda.md             # Your working file
├── Exchange.md           # Async dialogue
├── Shadow.md             # Chronological vault index (auto-generated)
└── Backlog.md            # Priority-sorted Shadow view (on-demand)

~/.outheis/human/cache/agenda/
└── hashes.json           # SHA256 hashes for change detection
```

The cache is regenerable — delete it anytime and outheis will rebuild.

## Shadow.md

A staging area for chronological entries detected across your vault.

### Purpose

Your vault contains dates scattered across many files: project deadlines, birthdays in contact notes, recurring events in project docs. Shadow.md collects these automatically so Agenda can surface them at the right time.

### How It Works

The Data Agent (zeno) runs a nightly scan at 03:30 (configurable):

1. **Scan vault** — Parse all files for date-relevant content
2. **Detect patterns** — Deadlines, birthdays, appointments, recurring events
3. **Append new entries** — Add to Shadow.md without overwriting existing content
4. **Source tracking** — Each entry links back to its origin file

### Format

```markdown
# Shadow

*Chronological entries detected from vault. Auto-updated nightly.*

---

## Scan 2026-03-30 03:30

- ⏰ **2026-04-15** Project Alpha deadline `← projects/alpha.md`
- 🎂 **2026-05-12** Emma's birthday `← contacts/family.md`
- 🔄 **every Monday** Team standup `← work/routines.md`
- 📅 **2026-04-01** Tax filing deadline `← admin/taxes.md`

## Scan 2026-03-29 03:30

- ☐ **2026-03-31** Send quarterly report `← work/q1.md`
```

### Icons

| Icon | Type | Example |
|------|------|---------|
| ⏰ | Deadline | Project due dates |
| 🎂 | Birthday | Contact birthdays |
| 📅 | Appointment | Fixed calendar events |
| 🔄 | Recurring | Weekly/monthly events |
| ☐ | Task | Time-bound tasks |

### Item Completeness

For the Agenda agent to reliably schedule an item, every Shadow entry needs one of two anchors:

| Anchor | Meaning |
|--------|---------|
| `#date-YYYY-MM-DD` | Temporal anchor — show this item in the agenda from this date onwards |
| attention marker (e.g. `#action-required`) | No date — permanently visible until explicitly decided |

Items without either anchor are semantically incomplete: the agent cannot know when, or whether, to surface them.

**Reminder date vs. event date** — `#date` controls *when the item appears*, not necessarily when the event occurs. For a birthday, both dates are the same. For "remind me on May 3rd about the event on June 30th", `#date-2026-05-03` is the trigger; June 30th belongs in the item text. When the two dates differ, the event date is plain text; `#date` is the agenda trigger.

**Overdue items** — if a `#date` is in the past and no decision has been recorded, the item stays visible. Overdue = must decide (complete, defer, or drop).

**Tag names are yours to choose.** `#action-required` is outheis's default; you can use `#attention`, `#priority`, `#open`, or any marker your rules file defines — as long as the agent knows which tag means "always show".

### Integration with Daily

Agenda agent reads Shadow.md and can surface relevant entries in Daily.md. When you ask "what's on this week?", outheis checks both your explicit schedule and Shadow's detected dates.

### Configuration

```json
{
  "schedule": {
    "shadow_scan": {
      "enabled": true,
      "hour": 3,
      "minute": 30
    }
  }
}
```

### Manual Trigger

You can ask: "scan vault for dates" or "update shadow" to run the scan immediately.

## Configuration

In `config.json`:

```json
{
  "agents": {
    "agenda": {
      "name": "cato",
      "model": "capable",
      "enabled": true
    }
  },
  "schedule": {
    "agenda_review": {
      "enabled": true,
      "time": ["04:55", "05:55", "06:55", "07:55", "08:55", "09:55", "10:55",
               "11:55", "12:55", "13:55", "14:55", "15:55", "16:55", "17:55",
               "18:55", "19:55", "20:55", "21:55", "22:55", "23:55"]
    }
  }
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | true | Enable/disable Agenda agent |
| `time` | 04:55–23:55 hourly | List of times to run review |

## Best Practices

1. **Keep Agenda.md simple** — 🧘 Personal + 📅 Today + 🗓️ This Week is enough
2. **Annotate with `>`** — Use `> defer to ...` or `> done` to instruct cato without editing the task itself
3. **Answer Exchange when you can** — No rush, but it helps outheis learn
4. **Let outheis manage structure** — Focus on content, not formatting
5. **Use manual refresh sparingly** — Hourly is usually sufficient
