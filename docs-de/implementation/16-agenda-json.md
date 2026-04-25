
# agenda.json — Syntax-Referenz v0.2

Die Kalenderansicht im WebUI wird durch `agenda.json` gesteuert, die strukturierte
Projektion aller geplanten Einträge. Speicherort:

```
~/.outheis/human/webui/pages/agenda.json
```

---

## Struktur auf oberster Ebene

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
  "version":    "0.2",
  "generated":  "2026-04-24T10:00:00Z",
  "base_date":  "2026-04-24"
}
```

`base_date` ist der Referenztag für alle relativen `day`-Offsets. Wird täglich neu gesetzt.

---

## facets

```json
"facets": [
  { "id": "cato", "label": "Arbeit",   "hex": "#FF2E00" },
  { "id": "hiro", "label": "senswork", "hex": "#FFB400" },
  { "id": "rumi", "label": "Self",     "hex": "#460A46" },
  { "id": "ou",   "label": "Privat",   "hex": "#218380" },
  { "id": "zeno", "label": "OFC",      "hex": "#97EAD2" },
  { "id": "misc", "label": "Misc",     "hex": "#C490D1" }
]
```

`hex` = CI-Farbe als Hex-Code. Farbton und Sättigung werden automatisch berechnet.
Die Legende wird ausschließlich aus diesem Array gebaut.

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

`range` = sichtbare Tage (7 / 14 / 30).
`day_start` = erste Stunde der Zeitleiste (ganzzahlig, 0–23). Standard: 5.
`time_axis` = nicht-lineare Zeitachse: 6 Segmente à 4 Stunden, die genau 24 Stunden ab `day_start` abdecken. `weight` steuert die relative Bildschirmbreite — ein höheres Gewicht bedeutet mehr visuelle Auflösung für diesen Zeitbereich. Fehlt `time_axis`, wird linear über 24 Stunden verteilt.
`params` steuern das Gravitationsfeld-Rendering und werden beim Laden auf die UI-Schieberegler angewendet.

### Spread-Panel (UI)

Der **Spread**-Button in der oberen Leiste öffnet ein Konfigurationspanel für `day_start` und `time_axis`. Änderungen wirken sofort und werden beim nächsten Speichern übernommen.

- **Tag ab** — Zeitfeld (nur ganze Stunden) für `day_start`; aktualisiert alle Segmentgrenzen automatisch
- **Sechs Segment-Zeilen** — jede zeigt ihren `von–bis`-Bereich (berechnet aus `day_start` in 4-Stunden-Schritten) und einen Gewichts-Regler (0,1–5,0)

---

## items

Jeder Eintrag trägt eine Snowflake-ID und einen `type`.

### fixed — zeitgebundenes Event

```json
{
  "id":      "7430000000000001",
  "type":    "fixed",
  "facet":   "cato",
  "title":   "outheis Architektur",
  "day":     0,
  "start":   "09:00",
  "end":     "11:00",
  "density": "high"
}
```

### fixed — mehrtägig (ISO-Datetime)

```json
{
  "id":    "7430000000000041",
  "type":  "fixed",
  "facet": "zeno",
  "title": "ALP Dillingen",
  "start": "2026-07-20T09:00",
  "end":   "2026-07-22T17:00"
}
```

Kein `day`-Feld — wird automatisch aus dem Datum berechnet.
Wird als verbundener Balken über alle betroffenen Zeilen gerendert.

### volatile — freischwebender Eintrag

```json
{
  "id":    "7430000000000006",
  "type":  "volatile",
  "facet": "cato",
  "title": "Substack Entwurf",
  "day":   0,
  "size":  "m"
}
```

### recurring — wiederkehrendes Event

Wiederkehrende Events werden als **ein einziger Eintrag** mit einem `#recurring-*`-Tag gespeichert.
Das Frontend generiert Anzeigeinstanzen für alle betroffenen Tage, schreibt sie aber **nicht** als
einzelne Items zurück in `agenda.json`.

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

Unterstützte `#recurring-*`-Tags:

| Tag | Bedeutung |
|-----|-----------|
| `#recurring-daily` | Täglich |
| `#recurring-weekly` | Wöchentlich (selber Wochentag wie Anker) |
| `#recurring-monthly` | Monatlich (selber Tag des Monats) |
| `#recurring-yearly` | Jährlich |
| `#recurring-mon`, `#recurring-mon-wed-fri` | Bestimmte Wochentage |
| `#recurring-monthly-1-15` | Bestimmte Tage des Monats |

> **Wichtig:** Cato darf wiederkehrende Einträge nicht als Einzelinstanzen in `agenda.json` schreiben.
> Nur der Anker-Eintrag (mit `#recurring-*`-Tag) gehört in `items`.

---

## Feldübersicht

| Feld      | Typ                                  | fixed | volatile | Beschreibung                                  |
|-----------|--------------------------------------|-------|----------|-----------------------------------------------|
| `id`      | string (Snowflake)                   | ✓     | ✓        | Eindeutig, chronologisch sortierbar           |
| `type`    | `"fixed"` \| `"volatile"`           | ✓     | ✓        |                                               |
| `facet`   | string → `facets[].id`              | ✓     | ✓        | Bestimmt Farbe und Feldverhalten              |
| `title`   | string                               | ✓     | ✓        |                                               |
| `day`     | int (Offset von `base_date`)         | ✓*    | ✓        | *entfällt bei mehrtägigen ISO-Events          |
| `start`   | `"HH:MM"` oder `"YYYY-MM-DDTHH:MM"` | ✓     | –        | ISO-Format = mehrtägig                        |
| `end`     | `"HH:MM"` oder `"YYYY-MM-DDTHH:MM"` | ✓     | –        |                                               |
| `density` | `"high"` \| `"low"`                 | –     | –        | Feldgewicht; fehlt = Standard                 |
| `layer`   | `0` \| `1`                          | –     | –        | `1` = Overlay über einem anderen Event        |
| `size`    | `"s"` \| `"m"` \| `"l"`            | –     | ✓        | Aufwandsschätzung; bestimmt visuelle Breite   |
| `note`    | string                               | –     | –        | Nur im Tooltip sichtbar                       |
| `source`  | string                               | ✓     | ✓        | Herkunft: Vault-Pfad, `"cato"`, `"webui"` …  |
| `done`     | `"YYYY-MM-DD"`                     | –     | –        | Gesetzt wenn abgeschlossen                              |
| `follows`  | string[]                           | ✓     | ✓        | IDs der Items, auf die dieses Item wartet               |
| `precedes` | string[]                           | ✓     | ✓        | IDs der Items, die dieses Item blockiert                |
| `relates`  | string[]                           | ✓     | ✓        | IDs assoziierter Items — kein Ordering                  |
| `tags`     | string[]                           | ✓     | ✓        | Strukturelle Tags (`#date-`, `#time-`, etc.)            |

---

## Abhängigkeiten

Items können Reihenfolgebeziehungen zu anderen Items deklarieren. Alle drei Felder enthalten Arrays von Snowflake-IDs.

```json
{
  "id":       "7430000000000020",
  "type":     "volatile",
  "title":    "Projektstart",
  "day":      5,
  "follows":  ["7430000000000018", "7430000000000019"],
  "relates":  ["7430000000000010"]
}
```

| Feld | Richtung | Bedeutung |
|------|----------|-----------|
| `follows`  | dieses Item ← Vorgänger | Dieses Item wartet auf den Abschluss der gelisteten Items |
| `precedes` | dieses Item → Nachfolger | Dieses Item blockiert die gelisteten Items |
| `relates`  | assoziativ               | Verknüpfte Items — kein Ordering                          |

`follows` und `precedes` sind eigenständige Primitive, die dieselbe Beziehung aus entgegengesetzten Perspektiven ausdrücken. Keines setzt das andere voraus.

**effectiveDay** — der Kalender verschiebt Items nach vorne, wenn ihre Vorgänger noch offen sind:

```
effectiveDay(item) = max(effectiveDay(Vorgänger) + 1, item.day)
```

Rekursiv berechnet mit Zyklenerkennung. Erledigte Vorgänger (`done` gesetzt) blockieren nicht mehr. Das berechnete Datum wird nie in `agenda.json` zurückgeschrieben; `day` enthält immer den geplanten Tag.

Zur Darstellung im Kalender: [Kalender](17-calendar.html).
