---
title: Agenda
---

# Agenda

*Time management through three simple files.*

## The Three Files

outheis manages your schedule through three Markdown files in your vault:

```
vault/Agenda/
├── Daily.md      # Today: schedule, tasks, notes
├── Inbox.md      # Quick capture: user → system
└── Exchange.md   # Async dialogue: system ↔ user
```

### Daily.md

Your day at a glance. The default template:

```markdown
⛅ [Weekday, DD.MM.YYYY]
*Refresh: HH:MM*

---
## 🧘 Persönlich

- [ ]

---
## 📅 Heute

---
## 🗓️ Diese Woche

---
## 💶 Cashflow
```

The structure is user-configurable. Once you establish your preferred layout, outheis preserves it exactly on each refresh — only the content changes, never the structure.

outheis reads this file, understands your commitments, and can answer questions like "bin ich heute nachmittag frei?" or "was steht morgen an?"

### Inbox.md

Quick capture without structure. When you have a thought but don't want to think about where it goes:

```markdown
# Inbox

*Drop anything here. outheis processes it hourly.*

---

meeting mit X nächste woche, wichtig
zahnarzt anrufen
projekt alpha deadline verschoben auf april
```

outheis processes this hourly:
- Recognizes tasks → moves to Daily.md
- Unclear items → asks via Exchange.md
- Notes → keeps or archives

### Exchange.md

Asynchronous dialogue between you and outheis. Created automatically on startup:

```markdown
# Exchange

*Asynchronous communication between you and outheis. No pressure to respond immediately — outheis checks hourly and learns from your answers.*

---

## 2026-03-30T10:15:00 – Konflikt

> Am Freitag hast du:
> - 10:00 Team-Meeting
> - 10:00 Zahnarzt
> - 10:30 Client-Call
>
> Wie soll ich priorisieren?

**Your response:**
Zahnarzt ist wichtiger, Team-Meeting verschieben.

---

## 2026-03-30T14:00:00 – Rückfrage

> Du hast "Meeting mit X nächste Woche" erwähnt — welcher Tag passt?

**Your response:**


---
```

**Important:** Exchange.md is for questions from outheis to you. Write your answers under "Your response:" and outheis picks them up at the next hourly review.

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

Lines starting with `>` immediately after a task are processed as instructions:

```markdown
- [ ] Report schreiben
> verschieben auf nächste Woche
```

Supported actions:

| Annotation | Effect |
|------------|--------|
| `> erledigt` or `> ✓` | Remove the item (mark done) |
| `> verschieben auf [Datum]` | Reschedule to the given date |
| `> wiedervorlage am [Datum]` | Schedule the item for that date |
| `> nicht mehr wichtig` | Delete the item |

The `>` line itself is always removed after processing.

### Time Window

By default, hourly reviews only run between 04:55 and 23:55. No reviews during night hours (00:55–03:55). Configurable in `config.json`:

```json
{
  "schedule": {
    "agenda_review": {
      "hourly_at_minute": 55,
      "start_hour": 4,
      "end_hour": 23
    }
  }
}
```

## Manual Refresh

You can trigger an immediate agenda update:

- "aktualisiere daily"
- "aktualisiere meine agenda"
- "update daily"
- "refresh agenda"

This bypasses the hash check and runs a full review immediately. Useful after making many changes or before asking schedule questions.

## Creating the Structure

When outheis starts and the Agenda agent is enabled, it creates the directory with templates:

```bash
outheis start
# Creates vault/Agenda/ with Daily.md, Inbox.md, Exchange.md
```

Templates include helpful structure and emoji sections. You can also create manually:

```bash
mkdir -p ~/Documents/Vault/Agenda
touch ~/Documents/Vault/Agenda/{Daily,Inbox,Exchange}.md
```

## Asking About Your Schedule

Once set up, you can ask:

- "Was steht heute an?"
- "Bin ich morgen nachmittag frei?"
- "Wann ist mein nächster Termin mit X?"
- "Schreib auf: Meeting mit Y am Freitag 10 Uhr"

outheis reads your Agenda files and responds naturally.

### Read Queries

When asked to show the agenda ("Agenda", "was steht heute an", "gib mir die Agenda"), cato returns the content of Daily.md verbatim — no reformatting, no summarizing. The file content is the answer. Relay passes it through directly without a second LLM call.

## Integration with Other Agents

**Relay (ou)** routes schedule questions to Agenda. Read queries ("Agenda", "was steht heute") are routed directly to cato, which returns Daily.md verbatim. Write/update queries go through the full tool loop.

**Data Agent (zeno)** can search your vault but doesn't write to Agenda files.

**Action Agent (hiro)** can execute tasks (send emails, create calendar events) but Agenda manages what's scheduled.

**Pattern Agent (rumi)** observes your scheduling patterns and may:
- Create rules like "User prefers no meetings before 10:00"
- Notice recurring tasks and suggest automation
- Write to Exchange.md when seed files need approval

## Storage

```
vault/Agenda/
├── Daily.md              # Your working file
├── Inbox.md              # Quick capture
├── Exchange.md           # Async dialogue
└── Shadow.md             # Chronological entries from vault (auto-generated)

~/.outheis/human/cache/agenda/
├── hashes.json           # SHA256 hashes for change detection
├── Daily.md.prev         # Previous version for diff
├── Inbox.md.prev
└── Exchange.md.prev
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

### Integration with Daily

Agenda agent reads Shadow.md and can surface relevant entries in Daily.md. When you ask "was steht diese Woche an?", outheis checks both your explicit schedule and Shadow's detected dates.

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

You can ask: "scanne den vault nach terminen" or "aktualisiere shadow" to run the scan immediately.

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
      "hourly_at_minute": 55,
      "start_hour": 4,
      "end_hour": 23
    }
  }
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | true | Enable/disable Agenda agent |
| `hourly_at_minute` | 55 | Minute of each hour to run review |
| `start_hour` | 4 | First hour of day to run (inclusive) |
| `end_hour` | 23 | Last hour of day to run (inclusive) |

## Best Practices

1. **Keep Daily.md simple** — 🧘 Morning + 🔴 Schedule + 🟠 Tasks is enough
2. **Use Inbox for quick capture** — Don't think, just dump
3. **Answer Exchange when you can** — No rush, but it helps outheis learn
4. **Annotate with `>`** — Use `> verschieben auf ...` or `> erledigt` to instruct outheis without editing the task itself
5. **Let outheis manage structure** — Focus on content, not formatting
6. **Use manual refresh sparingly** — Hourly is usually sufficient
