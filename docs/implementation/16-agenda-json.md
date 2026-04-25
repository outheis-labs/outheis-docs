
# agenda.json — Syntax Reference v0.2

The calendar view in the WebUI is driven by `agenda.json`, a structured
projection of all scheduled items. It lives at:

```
~/.outheis/human/webui/pages/agenda.json
```

---

## Top-level structure

```json
{
  "meta":   { ... },
  "facets": [ ... ],
  "view":   { ... },
  "items":  [ ... ]
}
```

---

## meta

```json
"meta": {
  "version":    "0.1",
  "generated":  "2026-04-23T10:00:00Z",
  "base_date":  "2026-04-23"
}
```

`base_date` is the reference day for all relative `day` offsets.
Regenerated daily — always today.

---

## facets

```json
"facets": [
  { "id": "cato", "label": "Arbeit",   "hex": "#FF2E00" },
  { "id": "hiro", "label": "senswork", "hex": "#FFB400" },
  { "id": "rumi", "label": "Self",     "hex": "#460A46" },
  { "id": "zeno", "label": "OFC",      "hex": "#97EAD2" },
  { "id": "ou",   "label": "Privat",   "hex": "#218380" },
  { "id": "misc", "label": "Misc",     "hex": "#7A7676" }
]
```

`hex` = CI color as a hex code. Hue and saturation are derived automatically
by the renderer via HSL conversion — no manual entry required.
The legend is built solely from this array.

---

## view

```json
"view": {
  "range": 7,
  "day_start": 5,
  "time_axis": [
    { "from": "05:00", "to": "09:00", "weight": 0.5 },
    { "from": "09:00", "to": "13:00", "weight": 2.2 },
    { "from": "13:00", "to": "17:00", "weight": 1.8 },
    { "from": "17:00", "to": "21:00", "weight": 1.0 },
    { "from": "21:00", "to": "01:00", "weight": 0.5 },
    { "from": "01:00", "to": "05:00", "weight": 0.3 }
  ],
  "params": {
    "peak_amp":      0.9,
    "decay":         10.0,
    "ghost_pull":    0.04,
    "overlay_alpha": 0.09
  }
}
```

`range` = visible days (7 / 14 / 30).
`day_start` = first hour of the timeline (integer, 0–23). Default: 5.
`time_axis` = non-linear time axis: 6 segments of 4 hours each, covering exactly 24 hours starting at `day_start`. `weight` controls relative screen width — higher weight means more visual resolution for that time range. Segments without `time_axis` fall back to linear 24-hour distribution.
`params` control the gravitational field rendering and are applied to the UI sliders on load.

### Spread panel (UI)

The **Spread** button in the top bar opens a configuration panel for `day_start` and `time_axis`. Changes take effect immediately and are persisted on the next Save.

- **Tag ab** — time input (whole hours only) that sets `day_start`; updates all segment boundaries automatically
- **Six segment rows** — each shows its `from–to` range (computed from `day_start` in 4-hour steps) and a weight slider (0.1–5.0)

---

## items

Every item carries a Snowflake ID and a `type`.

### fixed — time-boxed event

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
  "source":  "projects/alpha.md",
  "note":    "optional"
}
```

### fixed — multi-day (ISO datetime)

```json
{
  "id":     "7430000000000041",
  "type":   "fixed",
  "facet":  "zeno",
  "title":  "Family gathering",
  "start":  "2026-04-28T12:00",
  "end":    "2026-04-30T18:00",
  "source": "projects/travel.md"
}
```

No `day` field — computed automatically from the date.
Rendered as a connected bar spanning all affected rows.

### volatile — undated floating item

```json
{
  "id":     "7430000000000006",
  "type":   "volatile",
  "facet":  "cato",
  "title":  "Substack draft",
  "day":    0,
  "size":   "m",
  "source": "cato"
}
```

### recurring — repeating event

Recurring events are stored as **a single anchor item** with a `#recurring-*` tag. The frontend generates display instances for all matching days in the visible range, but never writes them back as individual items into `agenda.json`.

```json
{
  "id":    "7430000000000010",
  "type":  "fixed",
  "facet": "cato",
  "title": "Daily Standup",
  "day":   0,
  "start": "09:00",
  "end":   "09:30",
  "tags":  ["#date-2026-04-24", "#time-09:00-09:30", "#facet-cato", "#recurring-daily"]
}
```

Supported `#recurring-*` tags:

| Tag | Meaning |
|-----|---------|
| `#recurring-daily` | Every day |
| `#recurring-weekly` | Same weekday as anchor |
| `#recurring-monthly` | Same day of month as anchor |
| `#recurring-yearly` | Same month + day as anchor |
| `#recurring-mon`, `#recurring-mon-wed-fri` | Specific weekdays |
| `#recurring-monthly-1-15` | Specific days of month |

> **Important:** cato must not write individual instances of recurring events into `agenda.json`. Only the anchor item (with `#recurring-*` tag) belongs in `items`.

---

## Field reference

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
| `source`  | string                              | ✓     | ✓        | Origin: vault file path, `"cato"`, `"webui"`, `"signal"`, `"cli"` |
| `done`    | `"YYYY-MM-DD"`                     | –     | –        | Set when item is completed; triggers retention countdown |
| `follows`  | string[]                           | ✓     | ✓        | IDs of items this item waits for (predecessor IDs)      |
| `precedes` | string[]                           | ✓     | ✓        | IDs of items this item blocks (successor IDs)           |
| `relates`  | string[]                           | ✓     | ✓        | IDs of associated items — no ordering implied           |

---

## source values

| Value              | Set by    | Meaning                                       |
|--------------------|-----------|-----------------------------------------------|
| `"path/to/file.md"` | zeno     | Extracted from this vault file                |
| `"cato"`           | cato      | Created or managed by the agenda agent        |
| `"webui"`          | WebUI     | Added or modified via the calendar view       |
| `"signal"`         | signal.py | Received via Signal message                   |
| `"cli"`            | relay/ou  | Added via CLI / TUI                           |

---

## Mapping from Shadow tag format

Items map directly from the two-line tag format used in Shadow.md:

| Shadow tag line                                  | agenda.json                                       | Calendar               |
|--------------------------------------------------|---------------------------------------------------|------------------------|
| `#date-D #time-S-E #facet-X`                    | `type: fixed, day: N, start: S, end: E`          | Time-boxed block       |
| `#date-D #facet-X`                              | `type: volatile, day: N`                         | Floating label         |
| `#action-required #facet-X`                     | `type: volatile, day: null`                      | Floating, undated      |
| `#date-D1 #date-D2 #time-S-E #facet-X`         | `type: fixed, start: D1TS, end: D2TE`            | Multi-day block        |
| `#date-D #time-HH:MM #facet-X`                 | `type: volatile, day: N, duration: "HH:MM"`      | Bounded floating box   |
| `#action-required #time-HH:MM #facet-X`        | `type: volatile, day: 0, duration: "HH:MM"`      | Bounded floating box   |

> **`#time-` forms:** `#time-HH:MM-HH:MM` = start/end → `fixed`; `#time-HH:MM` (single time) = duration → `volatile` with `duration` field.

---

## Dependencies

Items can declare ordering relationships with other items. All three fields hold arrays of Snowflake IDs.

```json
{
  "id":       "7430000000000020",
  "type":     "volatile",
  "title":    "Project Start",
  "day":      5,
  "follows":  ["7430000000000018", "7430000000000019"],
  "precedes": [],
  "relates":  ["7430000000000010"]
}
```

| Field | Direction | Meaning |
|-------|-----------|---------|
| `follows`  | this item ← predecessors | This item waits for the listed items to be done |
| `precedes` | this item → successors   | This item blocks the listed items |
| `relates`  | associative              | Associated items — no ordering implied |

`follows` and `precedes` are independent primitives that express the same relationship from opposite perspectives. Either can be set without the other. The calendar resolves both when computing `effectiveDay`.

**effectiveDay** — the calendar pushes items forward when their predecessors are incomplete:

```
effectiveDay(item) = max(effectiveDay(predecessor) + 1, item.day)
```

Computed recursively with cycle detection. A predecessor with `done` set does not block. The computed day is never written back to `agenda.json`; `day` always holds the intended/planned day.

For calendar rendering details see [Calendar](17-calendar.html).
