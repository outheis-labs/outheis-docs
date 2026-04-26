
# Agenda

*Zeitmanagement durch drei einfache Dateien.*

---

## Die drei Dateien

outheis verwaltet deinen Zeitplan über zwei Markdown-Dateien in deinem Vault:

```
vault/Agenda/
├── Agenda.md     # Heute: Zeitplan, Aufgaben, Notizen
└── Exchange.md   # Asynchroner Dialog: System ↔ Benutzer

~/.outheis/human/webui/pages/
└── agenda.json    # Single source of truth für Kalenderansicht
```

### Agenda.md

Dein Tag auf einen Blick. Die Standardvorlage:

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

Die Struktur ist benutzerkonfigurierbar über `DailyTemplate.md` in deinem Vault. Sobald du dein bevorzugtes Layout etabliert hast, bewahrt outheis es bei jeder Aktualisierung genau — nur der Inhalt ändert sich, nie die Struktur.

outheis liest diese Datei, versteht deine Verpflichtungen und beantwortet Fragen wie "bin ich heute nachmittag frei?" oder "was steht morgen an?".

### Exchange.md

Asynchroner Dialog zwischen dir und outheis:

```markdown
# Exchange

---

## 2026-04-08T10:15:00 – Frage

Welcher Tag passt für das Meeting mit X?

- [ ] Akzeptieren
- [ ] Ablehnen

---
```

Schreibe eine `>`-Antwort direkt unter einem offenen Eintrag oder hake eine Box ab — cato verarbeitet sie beim nächsten Lauf.

## Stündliche Überprüfung

Um 55 Minuten nach jeder vollen Stunde (konfigurierbar) läuft der Agenda-Agent.

### Bedingte Ausführung

Vor der Verarbeitung prüft outheis Datei-Hashes:

```
~/.outheis/human/cache/agenda/hashes.json
```

Wenn sich seit dem letzten Lauf nichts geändert hat, wird kein LLM-Aufruf gemacht. Das spart API-Kosten bei gleichzeitiger Reaktionsfähigkeit.

**Ausnahmen:** Morgen- (04:55) und Abendläufe (23:55) sind unbedingt, um Tagesübergänge korrekt zu behandeln.

### Verarbeitungsschritte

1. **Hash-Prüfung** — Aktuelle Dateien mit gespeicherten Hashes vergleichen
2. **Exchange prüfen** — Nach deinen Antworten suchen, Lernfortschritte extrahieren
3. **Agenda überprüfen** — Anmerkungen, Kommentare, Erledigungen bemerken
4. **Hashes aktualisieren** — Neue Datei-Hashes für nächsten Vergleich speichern
5. **Diffs cachen** — `.prev`-Versionen für Debugging speichern

### Anmerkungen

Eine `>`-Zeile unmittelbar unter einem Eintrag ist eine direkte Anweisung an cato:

```markdown
#action-required #topic-admin
Lieferanten wegen Lieferdatum anrufen
> erledigt, Bestätigung bis Freitag erwartet
```

cato klassifiziert jede Anmerkung in einen von drei Typen:

| Typ | Erkannt an | Aktion |
|---|---|---|
| **Erledigung** | erledigt, fertig, bestätigt, abgeschlossen | Eintrag aus Agenda.md entfernen |
| **Verschieben** | später, nächste Woche, [zukünftiges Datum] | Aus Agenda.md entfernen, Datum in agenda.json aktualisieren |
| **Korrektur** | Erklärung, Umformulierung, neuer Kontext | Eintrag an Ort und Stelle neu schreiben, behalten |

Die `>`-Zeile wird nach der Verarbeitung immer entfernt.

### Zeitfenster

Stündliche Überprüfungen laufen standardmäßig nur zwischen 04:55 und 23:55. Keine Überprüfungen nachts. In `config.json` konfigurierbar:

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

## Manuelle Aktualisierung

Du kannst eine sofortige Agenda-Aktualisierung auslösen:

- "aktualisiere daily"
- "aktualisiere meine agenda"
- "update daily"
- "refresh agenda"

Das umgeht die Hash-Prüfung und führt sofort eine vollständige Überprüfung durch. Nützlich nach vielen Änderungen oder vor Terminabfragen.

## Struktur erstellen

Wenn outheis startet und der Agenda-Agent aktiviert ist, erstellt er das Verzeichnis automatisch. Du kannst auch manuell erstellen:

```bash
mkdir -p ~/Documents/Vault/Agenda
touch ~/Documents/Vault/Agenda/{Agenda,Exchange}.md
```

## Nach deinem Zeitplan fragen

Sobald eingerichtet, kannst du fragen:

- "Was steht heute an?"
- "Bin ich morgen nachmittag frei?"
- "Wann ist mein nächster Termin mit X?"
- "Schreib auf: Meeting mit Y am Freitag 10 Uhr"

outheis liest deine Agenda-Dateien und antwortet natürlich.

### Leseabfragen

Wenn du die Agenda abrufst ("Agenda", "was steht heute an", "gib mir die Agenda"), gibt cato den Inhalt von Agenda.md wörtlich zurück — keine Neuformatierung, keine Zusammenfassung. Der Dateiinhalt ist die Antwort. Relay leitet ihn direkt weiter ohne zweiten LLM-Aufruf.

## Integration mit anderen Agenten

**Relay (ou)** leitet Terminabfragen an Agenda weiter. Leseabfragen ("Agenda", "was steht heute") werden direkt an cato weitergeleitet, der Agenda.md wörtlich zurückgibt. Schreib- und Aktualisierungsabfragen durchlaufen die vollständige Tool-Schleife.

**Data-Agent (zeno)** kann deinen Vault durchsuchen, schreibt aber nicht in Agenda-Dateien.

**Action-Agent (hiro)** kann Aufgaben ausführen (E-Mails senden, Kalendereinträge erstellen), aber Agenda verwaltet, was geplant ist.

**Pattern-Agent (rumi)** beobachtet deine Planungsmuster und kann:

- Rules erstellen wie "Benutzer bevorzugt keine Meetings vor 10:00"
- Wiederkehrende Aufgaben bemerken und Automatisierung vorschlagen
- In Exchange.md schreiben, wenn Seed-Dateien Genehmigung benötigen

## Speicherung

```
vault/Agenda/
├── Agenda.md             # Deine Arbeitsdatei
└── Exchange.md           # Asynchroner Dialog

~/.outheis/human/webui/pages/
└── agenda.json           # Single source of truth für Kalenderansicht

~/.outheis/human/cache/agenda/
└── hashes.json           # SHA256-Hashes zur Änderungserkennung
```

Der Cache ist neu erstellbar — jederzeit löschen und outheis baut ihn neu auf.

## agenda.json

Die Kalenderansicht wird von `agenda.json` gesteuert — einer strukturierten JSON-Datei, die als Single Source of Truth für alle geplanten Einträge dient.

### Zweck

Dein Vault enthält Daten in vielen Dateien: Projektdeadlines, Geburtstage in Kontaktnotizen, wiederkehrende Ereignisse in Projektdokumenten. Der Data-Agent (zeno) scannt diese nächtlich und schreibt erkannte Einträge nach `agenda.json`. Der Agenda-Agent (cato) schreibt auch benutzererstellte Einträge direkt. Das WebUI erlaubt interaktives Bearbeiten.

### Funktionsweise

Der Data-Agent (zeno) führt um 03:30 (konfigurierbar) einen nächtlichen Scan durch:

1. **Vault scannen** — Alle Dateien auf datumrelevante Inhalte durchsuchen (per LLM-Extraktion)
2. **Änderungen erkennen** — Hash-basierter Cache; nur neue oder geänderte Dateien werden neu verarbeitet
3. **Einträge schreiben** — Erkannte Einträge werden nach `agenda.json` geschrieben mit Quelldateipfad
4. **Quellverfolgung** — Jeder Eintrag trägt ein `source`-Feld das seine Herkunft angibt

Der Agenda-Agent (cato) läuft stündlich (standardmäßig um :55 jeder Stunde) und:
1. Liest `agenda.json` und `Agenda.md` um den aktuellen Stand zu verstehen
2. Verarbeitet Benutzeranmerkungen (Zeilen beginnend mit `>` in Agenda.md)
3. Aktualisiert Einträge in `agenda.json` basierend auf Benutzerentscheidungen
4. Schreibt das aktualisierte `Agenda.md`

Das WebUI erlaubt direkte Manipulation von Einträgen in `agenda.json` via Drag-and-Drop, Größenänderung und Bearbeitung.

### Format

Einträge in `agenda.json` verwenden ein strukturiertes Format mit Snowflake-IDs:

```json
{
  "id": "7430000000000001",
  "type": "fixed",
  "facet": "work",
  "title": "Project Alpha Deadline",
  "day": 0,
  "start": "09:00",
  "end": "11:00",
  "tags": ["#date-2026-04-15", "#action-required"],
  "source": "projects/alpha.md"
}
```

Für die vollständige Schemareferenz siehe [agenda.json Referenz](16-agenda-json.html).

### Vollständigkeit von Einträgen

Damit der Agenda-Agent einen Eintrag zuverlässig einplanen kann, braucht jeder Eintrag einen von zwei Ankern:

| Anker | Bedeutung |
|-------|-----------|
| `#date-YYYY-MM-DD` in tags | Zeitlicher Anker — zeige diesen Eintrag ab diesem Datum in der Agenda |
| `#action-required` in tags | Kein Datum — dauerhaft sichtbar bis explizit entschieden |

Einträge ohne einen dieser Anker sind semantisch unvollständig: der Agent kann nicht wissen, wann oder ob er sie anzeigen soll.

**Erinnerungsdatum vs. Ereignisdatum** — `#date` steuert *wann der Eintrag erscheint*, nicht zwingend wann das Ereignis stattfindet. Bei einem Geburtstag fallen beide zusammen. Bei "erinnere mich am 3. Mai an die Veranstaltung am 30. Juni" ist `#date-2026-05-03` der Trigger; der 30. Juni gehört in den Eintragstext.

**Überfällige Einträge** — liegt ein `#date` in der Vergangenheit und wurde keine Entscheidung festgehalten, bleibt der Eintrag sichtbar. Überfällig = muss entschieden werden.

#### Erledigung — `#done-YYYY-MM-DD`

Wenn du einen Eintrag als erledigt markierst (via `> erledigt`-Anmerkung in Agenda.md), speichert outheis das Erledigungsdatum:

```
#done-2026-04-14 #date-2026-04-10 #action-required
Alex Smith mailen — Empfehlung zur Weiterbildung
```

Das `#done-*`-Tag wird in `agenda.json` und in die Quell-Vault-Datei geschrieben. Erledigte Einträge werden sofort aus der Agenda gefiltert und tauchen nie wieder auf.

Nach einer konfigurierbaren Aufbewahrungsfrist werden erledigte Einträge automatisch aus `agenda.json` entfernt:

```json
{
  "agents": {
    "agenda": {
      "retention": 90
    }
  }
}
```

Der Standard ist kein Aufbewahrungslimit (`null`). Setze `retention` auf die Anzahl der Tage, nach denen erledigte Einträge entfernt werden.

### Zeit-Tags

Items ohne feste Uhrzeit sind *volatil* — sie erscheinen am richtigen Tag, haben aber keine Position auf dem Zeitstrahl. Um ein Item zeitlich zu verankern, wird `#time-HH:MM-HH:MM` ergänzt:

| Tags in agenda.json | Bedeutung |
|---|---|
| `#date-2026-04-28` | Volatil — erscheint am 28. April, keine feste Zeit |
| `#date-2026-04-28 #time-09:00-10:30` | Fest — 28. April, 09:00–10:30 |
| `#date-2026-04-28 #date-2026-04-30 #time-12:00-18:00` | Mehrtätig — beginnt 28. April 12:00, endet 30. April 18:00 |
| `#action-required #time-00:35` | Volatil mit Dauer — schwebt frei, im Kalender als begrenzte Box |
| `#action-required` | Dauerhaft volatil — kein Datum, immer sichtbar |

### Konfiguration

```json
{
  "schedule": {
    "vault_scan": {
      "enabled": true,
      "time": ["03:30"]
    }
  }
}
```

### Manueller Auslöser

Du kannst fragen: "scanne den vault nach terminen" oder "aktualisiere agenda", um den Scan sofort auszuführen.

## Kalenderansicht

Das WebUI enthält einen interaktiven Kalender-Tab, der den Zeitplan visuell darstellt. Er wird von `agenda.json` angetrieben — einer strukturierten Projektion, die cato bei jedem stündlichen Lauf zusammen mit Agenda.md erzeugt.

Zur vollständigen Dokumentation der Kalender-Features: [Kalender](17-calendar.html). Zum Datenformat: [agenda.json Referenz](16-agenda-json.html).

## Konfiguration

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

| Einstellung | Standard | Beschreibung |
|-------------|---------|--------------|
| `enabled` | true | Agenda-Agent aktivieren/deaktivieren |
| `time` | 04:55–23:55 stündlich | Liste der Ausführungszeiten |

## Best Practices

1. **Agenda.md einfach halten** — 🧘 Persönlich + 📅 Heute + 🗓️ Diese Woche reicht
2. **Mit `>` annotieren** — `> verschieben auf ...` oder `> erledigt` verwenden, um cato anzuweisen ohne die Aufgabe selbst zu bearbeiten
3. **Exchange beantworten wenn möglich** — Kein Druck, aber es hilft outheis zu lernen
4. **outheis die Struktur verwalten lassen** — Auf den Inhalt konzentrieren, nicht die Formatierung
5. **Manuelle Aktualisierung sparsam nutzen** — Stündlich reicht meistens aus
