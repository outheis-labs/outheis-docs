---
title: Agenda
---

# Agenda

*Zeitmanagement durch drei einfache Dateien.*

## Die drei Dateien

outheis verwaltet deinen Zeitplan über drei Markdown-Dateien in deinem Vault:

```
vault/Agenda/
├── Daily.md      # Heute: Zeitplan, Aufgaben, Notizen
├── Inbox.md      # Schnellerfassung: Benutzer → System
└── Exchange.md   # Asynchroner Dialog: System ↔ Benutzer
```

### Daily.md

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

Die Struktur ist benutzerkonfigurierbar. Sobald du dein bevorzugtes Layout etabliert hast, bewahrt outheis es bei jeder Aktualisierung genau — nur der Inhalt ändert sich, nie die Struktur.

outheis liest diese Datei, versteht deine Verpflichtungen und beantwortet Fragen wie "bin ich heute nachmittag frei?" oder "was steht morgen an?".

### Inbox.md

Schnellerfassung ohne Struktur. Wenn du einen Gedanken hast, aber nicht darüber nachdenken möchtest, wohin er gehört:

```markdown
# Inbox

*Drop anything here. outheis processes it hourly.*

---

meeting mit X nächste woche, wichtig
zahnarzt anrufen
projekt alpha deadline verschoben auf april
```

outheis verarbeitet dies stündlich:

- Erkennt Aufgaben → verschiebt in Daily.md
- Unklare Einträge → fragt über Exchange.md
- Notizen → behält oder archiviert

### Exchange.md

Asynchroner Dialog zwischen dir und outheis. Wird automatisch beim Start erstellt:

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

**Wichtig:** Exchange.md ist für Fragen von outheis an dich. Schreibe deine Antworten unter "Your response:". outheis nimmt sie bei der nächsten stündlichen Überprüfung auf.

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
2. **Inbox verarbeiten** — Einträge parsen, Aufgaben nach Daily verschieben, Unklares → Exchange
3. **Exchange prüfen** — Nach deinen Antworten suchen, Lernfortschritte extrahieren
4. **Daily überprüfen** — Anmerkungen, Kommentare, Erledigungen bemerken
5. **Hashes aktualisieren** — Neue Datei-Hashes für nächsten Vergleich speichern
6. **Diffs cachen** — `.prev`-Versionen für Debugging speichern

### Anmerkungen

Zeilen, die unmittelbar nach einer Aufgabe mit `>` beginnen, werden als Anweisungen verarbeitet:

```markdown
- [ ] Report schreiben
> verschieben auf nächste Woche
```

Unterstützte Aktionen:

| Anmerkung | Effekt |
|-----------|--------|
| `> erledigt` oder `> ✓` | Eintrag entfernen (als erledigt markieren) |
| `> verschieben auf [Datum]` | Auf das angegebene Datum verschieben |
| `> wiedervorlage am [Datum]` | Eintrag für dieses Datum einplanen |
| `> nicht mehr wichtig` | Eintrag löschen |

Die `>`-Zeile selbst wird nach der Verarbeitung immer entfernt.

### Zeitfenster

Stündliche Überprüfungen laufen standardmäßig nur zwischen 04:55 und 23:55. Keine Überprüfungen nachts (00:55–03:55). In `config.json` konfigurierbar:

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

## Manuelle Aktualisierung

Du kannst eine sofortige Agenda-Aktualisierung auslösen:

- "aktualisiere daily"
- "aktualisiere meine agenda"
- "update daily"
- "refresh agenda"

Das umgeht die Hash-Prüfung und führt sofort eine vollständige Überprüfung durch. Nützlich nach vielen Änderungen oder vor Terminabfragen.

## Struktur erstellen

Wenn outheis startet und der Agenda-Agent aktiviert ist, erstellt er das Verzeichnis mit Vorlagen:

```bash
outheis start
# Creates vault/Agenda/ with Daily.md, Inbox.md, Exchange.md
```

Vorlagen enthalten hilfreiche Struktur und Emoji-Abschnitte. Du kannst auch manuell erstellen:

```bash
mkdir -p ~/Documents/Vault/Agenda
touch ~/Documents/Vault/Agenda/{Daily,Inbox,Exchange}.md
```

## Nach deinem Zeitplan fragen

Sobald eingerichtet, kannst du fragen:

- "Was steht heute an?"
- "Bin ich morgen nachmittag frei?"
- "Wann ist mein nächster Termin mit X?"
- "Schreib auf: Meeting mit Y am Freitag 10 Uhr"

outheis liest deine Agenda-Dateien und antwortet natürlich.

### Leseabfragen

Wenn du die Agenda abrufst ("Agenda", "was steht heute an", "gib mir die Agenda"), gibt cato den Inhalt von Daily.md wörtlich zurück — keine Neuformatierung, keine Zusammenfassung. Der Dateiinhalt ist die Antwort. Relay leitet ihn direkt weiter ohne zweiten LLM-Aufruf.

## Integration mit anderen Agenten

**Relay (ou)** leitet Terminabfragen an Agenda weiter. Leseabfragen ("Agenda", "was steht heute") werden direkt an cato weitergeleitet, der Daily.md wörtlich zurückgibt. Schreib- und Aktualisierungsabfragen durchlaufen die vollständige Tool-Schleife.

**Data-Agent (zeno)** kann deinen Vault durchsuchen, schreibt aber nicht in Agenda-Dateien.

**Action-Agent (hiro)** kann Aufgaben ausführen (E-Mails senden, Kalendereinträge erstellen), aber Agenda verwaltet, was geplant ist.

**Pattern-Agent (rumi)** beobachtet deine Planungsmuster und kann:

- Rules erstellen wie "Benutzer bevorzugt keine Meetings vor 10:00"

- Wiederkehrende Aufgaben bemerken und Automatisierung vorschlagen
- In Exchange.md schreiben, wenn Seed-Dateien Genehmigung benötigen

## Speicherung

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

Der Cache ist neu erstellbar — jederzeit löschen und outheis baut ihn neu auf.

## Shadow.md

Ein Staging-Bereich für chronologische Einträge, die im Vault erkannt wurden.

### Zweck

Dein Vault enthält Daten in vielen Dateien: Projektdeadlines, Geburtstage in Kontaktnotizen, wiederkehrende Ereignisse in Projektdokumenten. Shadow.md sammelt diese automatisch, damit Agenda sie zur richtigen Zeit anzeigen kann.

### Funktionsweise

Der Data-Agent (zeno) führt um 03:30 (konfigurierbar) einen nächtlichen Scan durch:

1. **Vault scannen** — Alle Dateien auf datumrelevante Inhalte durchsuchen
2. **Muster erkennen** — Deadlines, Geburtstage, Termine, wiederkehrende Ereignisse
3. **Neue Einträge anhängen** — Shadow.md ergänzen ohne bestehende Inhalte zu überschreiben
4. **Quellverfolgung** — Jeder Eintrag verweist auf seine Ursprungsdatei

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

| Icon | Typ | Beispiel |
|------|-----|---------|
| ⏰ | Deadline | Projektfälligkeiten |
| 🎂 | Geburtstag | Kontaktgeburtstage |
| 📅 | Termin | Feste Kalendereinträge |
| 🔄 | Wiederkehrend | Wöchentliche/monatliche Ereignisse |
| ☐ | Aufgabe | Zeitgebundene Aufgaben |

### Integration mit Daily

Der Agenda-Agent liest Shadow.md und zeigt relevante Einträge in Daily.md an. Wenn du fragst "was steht diese Woche an?", prüft outheis sowohl deinen expliziten Zeitplan als auch Shadows erkannte Daten.

### Konfiguration

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

### Manueller Auslöser

Du kannst fragen: "scanne den vault nach terminen" oder "aktualisiere shadow", um den Scan sofort auszuführen.

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
      "hourly_at_minute": 55,
      "start_hour": 4,
      "end_hour": 23
    }
  }
}
```

| Einstellung | Standard | Beschreibung |
|-------------|---------|--------------|
| `enabled` | true | Agenda-Agent aktivieren/deaktivieren |
| `hourly_at_minute` | 55 | Minute jeder Stunde für die Überprüfung |
| `start_hour` | 4 | Erste Stunde des Tages zum Ausführen (einschließlich) |
| `end_hour` | 23 | Letzte Stunde des Tages zum Ausführen (einschließlich) |

## Best Practices

1. **Daily.md einfach halten** — 🧘 Morgen + 🔴 Zeitplan + 🟠 Aufgaben reicht
2. **Inbox für Schnellerfassung nutzen** — Nicht denken, einfach reinschreiben
3. **Exchange beantworten wenn möglich** — Kein Druck, aber es hilft outheis zu lernen
4. **Mit `>` kommentieren** — `> verschieben auf ...` oder `> erledigt` verwenden, um outheis anzuweisen ohne die Aufgabe selbst zu bearbeiten
5. **outheis die Struktur verwalten lassen** — Auf den Inhalt konzentrieren, nicht die Formatierung
6. **Manuelle Aktualisierung sparsam nutzen** — Stündlich reicht meistens aus
