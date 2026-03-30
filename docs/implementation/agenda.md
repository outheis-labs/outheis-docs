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

Your day at a glance. Contains:

- **Schedule** — Appointments with times
- **Tasks** — What needs doing today
- **Notes** — Quick thoughts throughout the day
- **Evening** — End-of-day reflection (optional)

Example:

```markdown
# Monday, March 30, 2026

## Schedule
- 09:00 Standup
- 14:00 Client call
- 16:30 Pick up kids

## Tasks
- [ ] Finish quarterly report
- [x] Email X about meeting
- [ ] Review PR #42

## Notes
<!-- 10:15 -->
Call with client went well. Follow up next week.

## Evening
Good day. Report still pending — carry to tomorrow.
```

outheis reads this file, understands your commitments, and can answer questions like "bin ich heute nachmittag frei?" or "was steht morgen an?"

### Inbox.md

Quick capture without structure. When you have a thought but don't want to think about where it goes:

```markdown
# Inbox

meeting with X next week, wichtig
call dentist
projekt alpha deadline moved to april
```

outheis processes this hourly:
- Recognizes tasks → moves to Daily.md
- Unclear items → asks via Exchange.md
- Notes → keeps or archives

### Exchange.md

Asynchronous dialogue. When outheis needs clarification, it writes here:

```markdown
# Exchange

*Asynchronous communication between you and outheis*

---

## 2026-03-30T10:15:00 – Conflict

> On Friday you have:
> - 10:00 Team meeting
> - 10:00 Dentist appointment
> - 10:30 Client call
>
> How should I prioritize?

**Your response:**
Dentist is more important, reschedule team meeting.

---

## 2026-03-30T14:00:00 – Clarification

> You mentioned "meeting with X next week" — which day works best?

**Your response:**


---
```

No pressure to respond immediately. outheis checks hourly and learns from your answers.

## Hourly Review

At 55 minutes past each hour, the Agenda agent:

1. **Detects changes** — Compares files with cached previous versions
2. **Processes Inbox** — Moves tasks to Daily, asks questions if unclear
3. **Checks Exchange** — Looks for your responses, extracts learnings
4. **Reviews Daily** — Notices your annotations and comments
5. **Caches current** — Saves for next comparison

### Comments Matter

HTML comments in Daily.md are noticed:

```markdown
- [ ] Report schreiben #deadline-2025-03-28  <!-- verschoben auf nächste Woche -->
```

outheis sees this annotation and can act on it.

## Creating the Structure

When you first enable outheis, it creates the Agenda directory with default templates:

```bash
outheis start
# Creates vault/Agenda/ with Daily.md, Inbox.md, Exchange.md
```

Or create manually:

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

## Integration with Other Agents

**Data Agent** can search your vault but doesn't write to Agenda files.

**Action Agent** can execute tasks (send emails, create calendar events) but Agenda manages what's scheduled.

**Pattern Agent** observes your scheduling patterns and may create rules like "User prefers no meetings before 10:00".

## Storage

```
vault/Agenda/
├── Daily.md
├── Inbox.md
└── Exchange.md

~/.outheis/human/cache/agenda/
├── Daily.md.prev      # Previous version for diff
├── Inbox.md.prev
└── Exchange.md.prev
```

The cache is regenerable — delete it anytime and outheis will rebuild.

## Best Practices

1. **Keep Daily.md simple** — Schedule + Tasks + Notes is enough
2. **Use Inbox for quick capture** — Don't think, just dump
3. **Answer Exchange when you can** — No rush, but it helps outheis learn
4. **Add comments freely** — `<!-- notes -->` won't break anything
5. **Let outheis manage structure** — Focus on content, not formatting
