
# agenda.json — Syntax Reference v0.1

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
  "params": {
    "peak_amp":      0.9,
    "decay":         10.0,
    "ghost_pull":    0.04,
    "overlay_alpha": 0.09
  }
}
```

`range` = visible days (7 / 14 / 30).
`params` control the gravitational field rendering and are applied to the UI
sliders on load.

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
