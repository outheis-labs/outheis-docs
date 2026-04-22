
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

1. **Scan vault** — Read all files for date-relevant content via LLM extraction
2. **Detect changes** — Hash-based cache; only new or modified files are reprocessed
3. **Update by section** — Each source file has its own `<!-- BEGIN/END -->` block; sections are replaced independently
4. **Source tracking** — Each section is keyed to its origin file path

### Format

Shadow.md is organised by source file. Each section is delimited by HTML comment markers so individual sections can be replaced without touching the rest:

```markdown
# Shadow — Vault Chronological Index
*Last updated: 2026-04-14 21:55*

<!-- BEGIN: projects/alpha.md -->
## projects/alpha.md
#date-2026-04-15 #action-required
Project Alpha deadline

#date-2026-05-12
Emma's birthday
<!-- END: projects/alpha.md -->

<!-- BEGIN: work/routines.md -->
## work/routines.md
#recurring-weekly
Team standup
<!-- END: work/routines.md -->
```

Each entry is two lines: a tag line followed by a plain-text description. The tag line carries the scheduling anchor; the description is self-contained and readable without context.

### Item Completeness

For the Agenda agent to reliably schedule an item, every Shadow entry needs one of two anchors:

| Anchor | Meaning |
|--------|---------|
| `#date-YYYY-MM-DD` | Temporal anchor — show this item in the agenda from this date onwards |
| attention marker (e.g. `#action-required`) | No date — permanently visible until explicitly decided |

Items without either anchor are semantically incomplete: the agent cannot know when, or whether, to surface them.

**Reminder date vs. event date** — `#date` controls *when the item appears*, not necessarily when the event occurs. For a birthday, both dates are the same. For "remind me on May 3rd about the event on June 30th", `#date-2026-05-03` is the trigger; June 30th belongs in the item text. When the two dates differ, the event date is plain text; `#date` is the agenda trigger.

**Overdue items** — if a `#date` is in the past and no decision has been recorded, the item stays visible. Overdue = must decide (complete, defer, or drop).

#### Completion — `#done-YYYY-MM-DD`

When you mark an item done (via a `> done` annotation in Agenda.md), outheis records the completion date rather than deleting the entry:

```
#done-2026-04-14 #date-2026-04-10 #action-required
Email Alex Smith — recommendation on training track
```

The `#done-*` tag is written to Shadow.md and to the source vault file. Done items are filtered out of the agenda immediately and never resurface — the loop of completed items reappearing is explicitly prevented.

After a configurable retention period, done entries are pruned from Shadow.md automatically:

```json
{
  "agents": {
    "agenda": {
      "retention": 90
    }
  }
}
```

The default is no retention limit (`null`). Set `retention` to the number of days after which completed entries are removed from Shadow.md.

**Tag names are yours to choose.** `#action-required` is outheis's default; you can use `#attention`, `#priority`, `#open`, or any marker your rules file defines — as long as the agent knows which tag means "always show".

### Time Tags

Items without a fixed time are *volatile* — they surface on the right day but have no position on the timeline. To place an item at a specific time, add `#time-HH:MM-HH:MM` on the same tag line:

| Shadow tag line | Meaning |
|---|---|
| `#date-2026-04-28` | Volatile — surfaces on April 28, no fixed time |
| `#date-2026-04-28 #time-09:00-10:30` | Fixed — April 28, 09:00–10:30 |
| `#date-2026-04-28 #date-2026-04-30 #time-12:00-18:00` | Multi-day — starts April 28 at 12:00, ends April 30 at 18:00 |
| `#action-required` | Permanently volatile — no date, always visible |

Rules:
- `#time-` is always accompanied by at least one `#date-` — never standalone
- Two `#date-` tags define a multi-day span; `#time-` anchors the start time on the first date and the end time on the last
- `#date-` without `#time-` produces a volatile item that floats freely within its day in the calendar view

### Item Identity

Every Shadow item carries a stable snowflake UUID on its tag line:

```
#date-2026-04-28 #time-09:00-10:30 #facet-work #id-744f3a2b8c1e0d9f
Workshop
```

The `#id-` tag links the item across Shadow.md, Agenda.md, and agenda.json. It enables precise change tracking and conflict detection when multiple input channels modify the same item.

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

## Calendar View

The WebUI includes an interactive calendar tab that renders your schedule visually. It is driven by `agenda.json`, a structured projection of Shadow.md generated by cato alongside Agenda.md on each hourly run.

### agenda.json Reference v0.1

#### Top-level structure

```json
{
  "meta":   { ... },
  "facets": [ ... ],
  "view":   { ... },
  "items":  [ ... ]
}
```

#### meta

```json
"meta": {
  "version":   "0.1",
  "generated": "2026-04-23T10:00:00Z",
  "base_date": "2026-04-23"
}
```

`base_date` is the reference day for all relative `day` offsets. Regenerated daily — always today.

#### facets

```json
"facets": [
  { "id": "cato", "label": "Arbeit",  "hex": "#FF2E00" },
  { "id": "hiro", "label": "...",     "hex": "#FFB400" },
  { "id": "rumi", "label": "Self",    "hex": "#460A46" },
  { "id": "zeno", "label": "OFC",     "hex": "#97EAD2" },
  { "id": "ou",   "label": "Privat",  "hex": "#218380" },
  { "id": "misc", "label": "Misc",    "hex": "#7A7676" }
]
```

`hex` = CI color as a hex code. Hue and saturation are derived automatically by the renderer via HSL conversion — no manual entry required. Facets are derived exclusively from `#facet-*` tags in Shadow.md. The legend is built solely from this array.

#### view

```json
"view": {
  "range": 7,
  "params": {
    "peak_amp":      0.9,
    "decay":         10.0,
    "ghost_pull":    0.04,
    "overlay_alpha": 0.09
  }
}
```

`range` = visible days (7 / 14 / 30). `params` control the gravitational field rendering and are applied to the UI sliders on load.

#### items

Every item carries a Snowflake ID and a `type`.

**fixed — time-boxed event**

```json
{
  "id":      "7430000000000001",
  "type":    "fixed",
  "facet":   "cato",
  "title":   "outheis Architecture",
  "day":     0,
  "start":   "09:00",
  "end":     "11:00",
  "density": "high",
  "layer":   0,
  "note":    "optional"
}
```

**fixed — multi-day (ISO datetime)**

```json
{
  "id":    "7430000000000041",
  "type":  "fixed",
  "facet": "zeno",
  "title": "Family gathering",
  "start": "2026-04-28T12:00",
  "end":   "2026-04-30T18:00"
}
```

No `day` field — computed automatically from the date. Rendered as a connected bar spanning all affected rows.

**volatile — undated floating item**

```json
{
  "id":    "7430000000000006",
  "type":  "volatile",
  "facet": "cato",
  "title": "Substack draft",
  "day":   0,
  "size":  "m"
}
```

#### Field reference

| Field     | Type                                | fixed | volatile | Description                              |
|-----------|-------------------------------------|-------|----------|------------------------------------------|
| `id`      | string (Snowflake)                  | ✓     | ✓        | Unique, chronologically sortable         |
| `type`    | `"fixed"` \| `"volatile"`          | ✓     | ✓        |                                          |
| `facet`   | string → `facets[].id`             | ✓     | ✓        | Determines color and field behavior      |
| `title`   | string                              | ✓     | ✓        |                                          |
| `day`     | int (offset from `base_date`)       | ✓*    | ✓        | *omitted for multi-day ISO events        |
| `start`   | `"HH:MM"` or `"YYYY-MM-DDTHH:MM"` | ✓     | –        | ISO format = multi-day                   |
| `end`     | `"HH:MM"` or `"YYYY-MM-DDTHH:MM"` | ✓     | –        |                                          |
| `density` | `"high"` \| `"low"`                | –     | –        | Field weight; absent = default           |
| `layer`   | `0` \| `1`                         | –     | –        | `1` = overlay on top of another event    |
| `size`    | `"s"` \| `"m"` \| `"l"`           | –     | ✓        | Effort estimate; determines visual width |
| `note`    | string                              | –     | –        | Shown in tooltip only                    |
| `pos`     | `{"x": 0.42, "y": 0.38}`          | –     | –        | Last drag position, written by the view  |

**Items** map directly from Shadow entries:

| Shadow tags | agenda.json | Calendar |
|---|---|---|
| `#date-D #time-S-E #facet-X` | `type: fixed, day: N, start: S, end: E` | Time-boxed block |
| `#date-D #facet-X` | `type: volatile, day: N` | Floating label |
| `#action-required #facet-X` | `type: volatile, day: null` | Floating, undated |
| `#date-D1 #date-D2 #time-S-E #facet-X` | `type: fixed, start: D1TS, end: D2TE` | Multi-day block |

### Sync Model

Shadow.md is the single source of truth. Three input channels feed into it with different latencies:

| Channel | Latency | Mechanism |
|---|---|---|
| Calendar UI (agenda.json PUT) | Immediate | WebUI writes directly to Shadow.md via `#id-` |
| Exchange.md bare entry | Next hourly run | cato processes and updates Shadow.md |
| Agenda.md `>` annotation | Next hourly run | cato processes and updates Shadow.md |

When a user modifies an event in the calendar (drag to reschedule, resize, promote volatile→fixed), the WebUI sends a PUT to the server, which updates the matching Shadow.md item by UUID — before cato's next run.

### Conflict Detection

If cato detects, since the last Agenda.md generation, that:
- Shadow.md was updated (via calendar PUT) for an item, **and**
- Agenda.md contains a `>` annotation for the same item (matched by `#id-`)

cato adds a conflict note below the item, preserving all existing annotations:

```markdown
Workshop #id-744f3a...
> postpone to Friday
⚠ Calendar: already rescheduled to Mon 09:00. Please confirm or correct.
```

The user resolves by adding another annotation. No existing input is ever deleted automatically.

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
