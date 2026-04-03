---
title: Vault
---

# Vault

*How to structure your knowledge so outheis can work with it.*

## What the vault is

The vault is a directory of Markdown files — your notes, projects, documents, schedules. outheis reads it but does not own it. You bring the structure; outheis learns to navigate it.

The only required subdirectory is `Agenda/`, which outheis manages:

```
vault/
├── Agenda/
│   ├── Daily.md      # Today — schedule, tasks, notes
│   ├── Inbox.md      # Quick capture, unprocessed
│   └── Exchange.md   # Async communication with outheis
└── ... your files
```

Everything else is yours.

## Tags

outheis does not impose a tag schema. When you start outheis for the first time (or run `analyze tags`), the data agent scans your vault and extracts whatever tag system you already use — without modification.

### Tag systems vary

Users come with different conventions:

```
#todo #project #someday          ← flat, singular
#work/client/project             ← hierarchical with /
#action-required #status-active  ← namespaced with -
```

All of these work. outheis maps what it finds and works within that structure.

### The faceted namespace pattern

One particularly effective convention for personal knowledge management uses a `category-value` namespace with hyphens:

```
#action-required   #action-waiting   #action-now
#status-active     #status-completed #status-linger
#rank-urgent       #rank-high        #rank-low
#unit-work         #unit-self        #unit-family
#topic-design      #topic-admin
#size-S            #size-M           #size-L
#recurring
```

Each tag carries two pieces of information: what dimension it describes (`action`, `status`, `rank`) and what value it holds (`required`, `active`, `urgent`). This makes files queryable along multiple axes without nested folders or complex metadata.

The temporal dimension of this pattern — how time-anchored tags interact with recurring structure — is explored in the [research-base](https://github.com/outheis-labs/research-base/tree/main/temporalization-of-order).

### Date tags

Date tags (`#date-2026-03-24`) are one category outheis may generate itself. When creating notes or capturing information, the data agent adds a date tag to anchor the entry in time. All other tags are user-owned.

### Internal tags

outheis uses the `#outheis-` namespace for its own internal state tracking. These tags are never shown to the user in the WebUI and serve agent operations only — flagging processed items, archiving candidates, state markers.

Examples: `#outheis-state-done`, `#outheis-state-pending`, `#outheis-archive`

`#outheis-*` tags are always in English. They are created sparingly and only when they add genuine value to a future agent operation.

### Tag analysis

outheis learns your tag system on demand, not automatically. To start:

```
analyze tags
```

The data agent scans the vault, extracts the tag taxonomy, and reflects it back. You confirm or correct the interpretation. From that point, search and daily planning work within your established system.

If the data agent later observes inconsistencies or potential simplifications — a category with only one value, two tags that always appear together, a naming pattern that could be unified — it raises this directly in conversation. No changes are made without your agreement.

## Daily.md

Daily.md is generated fresh each day by the agenda agent. The default structure:

```markdown
# [Weekday], [Date]

## Morning

## Schedule

## Tasks

## Notes

## Evening
```

The agenda agent populates this from your vault: scheduled events, recurring items, tasks due today, items from Inbox.md. If your vault contains a timetable, a recurring schedule, or date-tagged entries, they appear here automatically.

You can modify the template. Put your preferred structure in `rules/agenda.md`:

```markdown
Daily.md should use these sections: [your sections here]
```

## Inbox.md

Quick capture without friction. Write anything — voice, typed, dictated. The agenda agent processes Inbox items during the hourly review: moves them to Daily.md, creates vault notes, or asks in Exchange.md if something needs clarification.

Format is free. One line per item is enough.

## Exchange.md

Async communication between you and outheis. Questions that don't need immediate answers, proposals that need review, information waiting for your input.

outheis writes here when it needs something from you. You answer when you have time. No notifications, no pressure.
