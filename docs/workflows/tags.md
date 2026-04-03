# Working with Tags

*How outheis learns your tag system and works within it.*

## The principle

outheis does not come with a tag schema. It learns yours.

When you start outheis for the first time, your vault tags are unknown to it. The data agent can scan and extract your tag taxonomy — but only when you ask. No automatic restructuring, no invented tags.

The one exception: date tags. When outheis creates or annotates a note, it may add a `#date-YYYY-MM-DD` tag to anchor it in time. Everything else stays untouched.

## Starting the analysis

Once your vault is connected, run:

```
analyze tags
```

The data agent scans all Markdown files, extracts every tag it finds, and reflects the structure back to you. For example:

```
Found 847 tags across 134 files.

Tag categories detected:
  action-*   (required, waiting, idle, now, call, send)
  status-*   (active, linger, completed, init)
  rank-*     (urgent, high, medium, low)
  unit-*     (work, self, family, ...)
  topic-*    (12 values)
  size-*     (S, M, L)
  recurring

No fixed schema assumed. Does this match how you use these tags?
```

You confirm or correct. From that point, outheis searches, plans, and reasons within your system.

## What outheis does with tags

**Daily planning** — the agenda agent uses `#action-required`, `#action-now`, `#focus-today`, and date tags when building your daily view. Items tagged for today surface automatically.

**Search** — you can query by tag directly:

```
show everything tagged #unit-work and #action-waiting
what's tagged #recurring this week?
```

**Shadow.md** — the nightly vault scan uses your tags to identify time-relevant entries. Items with `#recurring`, `#date-*`, or action tags appear in the chronological index the agenda agent reads each morning.

## Tag systems vary

outheis works with whatever convention you use:

```
#todo #project #someday           ← flat
#work/client/project              ← hierarchical with /
#action-required #status-active   ← namespaced with -
```

The data agent maps the structure it finds. It does not rewrite your tags to fit a preferred format.

## The faceted namespace pattern

One particularly effective convention uses a `category-value` namespace separated by hyphens. Each tag carries two pieces of information: what dimension it describes and what value it holds.

```
#action-required    what needs to happen
#status-active      current state
#rank-high          priority
#unit-work          context
#topic-design       subject matter
#size-M             estimated effort
#recurring          repeats
```

This makes any file queryable along multiple axes — without nested folders or formal metadata. A file tagged `#action-required #rank-urgent #unit-work` tells you immediately what it is, how urgent it is, and where it belongs.

The temporal dimension of this pattern — how time-anchored tags interact with recurring structure — is explored in the [research-base](https://github.com/outheis-labs/research-base/tree/main/temporalization-of-order).

## Improvements and proposals

Over time, the data agent may notice things: a category with only one value, two tags that always appear together, an inconsistency that a small convention change would resolve. When it does, it raises this directly in conversation — not silently, not automatically.

You decide whether to adopt the suggestion. If yes, outheis helps you apply it. The tag system stays yours.
