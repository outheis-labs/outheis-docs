---
title: Memory
---

# Memory

*Was outheis über dich erinnert — und wie.*

## Memory vs. Vault

outheis pflegt zwei separate Wissensspeicher:

| | Memory | Vault |
|---|--------|-------|
| **Zweck** | Meta-Wissen über dich | Deine Arbeitsinhalte |
| **Enthält** | Fakten, Präferenzen, Kontext | Dokumente, Notizen, Projekte |
| **Aktualisiert von** | Agents während Interaktion, Pattern-Agent, explizite Marker | Von dir direkt |
| **Format** | Strukturiertes JSON | Markdown-Dateien |

**Memory** beantwortet: *Wer ist diese Person? Wie soll ich arbeiten?*

**Vault** beantwortet: *Welche Informationen haben sie?*

## Memory-Typen

### user

Persönliche Fakten, die sich selten ändern.

Beispiele:

- "User is 35 years old"
- "Children: Leo (8) and Emma (5)"

- "Lives in Munich"
- "Works as a software engineer"

**Zerfall:** Dauerhaft (bis korrigiert)

### feedback

Wie du möchtest, dass outheis sich verhält.

Beispiele:

- "Prefers short, direct answers"
- "Respond in German unless asked otherwise"
- "Don't explain technical concepts — user is an expert"

**Zerfall:** Dauerhaft (bis korrigiert)

### context

Womit du dich gerade beschäftigst.

Beispiele:

- "Working on Project Alpha mobile app"
- "Preparing for conference talk next week"
- "Learning Japanese"

**Zerfall:** Standardmäßig 14 Tage (verblasst, wenn nicht mehr relevant)

## Wie Memory erstellt wird

Memory wird über drei Kanäle geschrieben:

### 1. Expliziter Marker (`!`)

Stelle jeder Nachricht `!` voran, um sie sofort zu speichern:

```
! I am 35 years old
→ Stored in user memory, agent responds with this knowledge

! please always give short answers
→ Stored in feedback memory, agent adapts immediately

! I'm currently working on Project Alpha
→ Stored in context memory (14 day decay)
```

Die Klassifizierung erfolgt automatisch basierend auf dem Inhalt. Der `!`-Marker ist eine Abkürzung — er entspricht "merke dir das", ist aber kürzer. Der agent speichert die Information UND verwendet sie sofort im aktuellen Gespräch.

### 2. Agents während der Interaktion

Agents können erkennen, wenn du etwas Merkenswürdiges mitteilst:

- Du erwähnst deinen Geburtstag → agent kann es speichern
- Du äußerst eine Präferenz → agent kann sie speichern
- Du beschreibst ein aktuelles Projekt → agent kann es als Kontext speichern

Das geschieht durch Urteilsvermögen — nicht durch starre Regeln. Agents sind angewiesen, relevante Informationen zu bemerken, aber nicht zu viel zu extrahieren. Nicht jede Aussage wird Memory — nur was für zukünftige Interaktionen wirklich nützlich erscheint.

### 3. Pattern-Agent-Extraktion

rumi läuft nächtlich um 04:00 und:

1. überprüft aktuelle Gespräche
2. extrahiert merkwürdige Informationen, die agents möglicherweise verpasst haben
3. konsolidiert Duplikate und löst Widersprüche auf
4. weist Konfidenzwerte zu
5. bereinigt abgelaufene Einträge
6. erwägt die Förderung stabiler Muster zu User Rules

Du kannst das manuell auslösen: `outheis pattern`

## Memory-Konsolidierung

Mit der Zeit sammelt Memory Duplikate oder widersprüchliche Einträge an. rumi behandelt das bei seinem geplanten Lauf:

- **Duplikate**: "Has pending tasks: X, Y" und "Current pending tasks: X, Y" → behält den neueren

- **Widersprüche**: "User is 35" und "User is 36" → behält den neueren oder explizit markierten

- **Überholte Einträge**: Kontext, der aktualisiert wurde → entfernt die ältere Version

Das ist kein mechanischer Prozess — rumi verwendet Urteilsvermögen, um zu entscheiden, was konsolidiert werden soll, mit einem Bias zum Behalten bei Unsicherheit.

## Zeitliches Bewusstsein

Nicht alles sollte für immer gespeichert werden.

**Als dauerhaftes Fakt gespeichert:**

- "User has two children"
- "Prefers formal communication"

**NICHT gespeichert (temporärer Zustand):**

- "User seems frustrated today"
- "User is tired"
- "User is stressed about deadline"

Alle agents unterscheiden stabile Eigenschaften von vorübergehenden Stimmungen. Eine frustrierte Nachricht ist kein Persönlichkeitsmerkmal — es ist ein Moment.

## Memory anzeigen und bearbeiten

### CLI

```bash
# View all memory
outheis memory

# Add entry manually
outheis memory --add "user:My birthday is March 15"

# Clear a type
outheis memory --clear context
```

### Anzeigeformat

```
Memory
----------------------------------------

[user] (3 entries)
  1. User is 35 years old
  2. Children: Leo (8), Emma (5) [!]
  3. Lives in Munich [90%]

[feedback] (1 entries)
  1. Prefers short answers [!]

[context] (2 entries)
  1. Working on Project Alpha [↓12d]
  2. Preparing conference talk [↓5d]
```

Marker:

- `[!]` — Explizit über `!`-Marker gespeichert
- `[90%]` — Konfidenz unter 100 %
- `[↓12d]` — Läuft in 12 Tagen ab

## Speicherung

```
~/.outheis/human/memory/
├── user.json           # Personal facts
├── feedback.json       # Working preferences
├── context.json        # Current focus
└── pattern/            # Pattern agent's learning
    └── strategies.md
```

Jede Memory-Datei enthält zeitgestempelte Einträge mit Metadaten:

```json
{
  "type": "user",
  "updated_at": "2025-03-28T14:30:00",
  "entries": [
    {
      "content": "User is 35 years old",
      "created_at": "2025-03-28T14:30:00",
      "updated_at": "2025-03-28T14:30:00",
      "confidence": 1.0,
      "source_count": 1,
      "decay_days": null,
      "is_explicit": true
    }
  ]
}
```

## Migration

Um bestehendes Wissen von Claude.ai oder anderen Quellen zu importieren, verwende den Migrations-Workflow. Siehe [Migration](migration.md) für Details.

Kurzübersicht:
1. `vault/Migration/` mit deinen `.json`- oder `.md`-Dateien erstellen
2. Im Chat "memory migrate" sagen
3. Einträge in `Migration.md` prüfen und markieren
4. Erneut "memory migrate" sagen, um anzuwenden
5. `vault/Migration/` löschen, wenn fertig

## Pattern-Agent-Meta-Memory

rumi hat sein eigenes Memory in `~/.outheis/human/memory/pattern/`. Hier speichert er:

- Welche Extraktionsstrategien für dich funktionieren
- Muster im Kommunikationsstil
- Meta-Insights über seinen eigenen Prozess

Dieses Memory zerfällt nicht — so wird rumi mit der Zeit besser darin, zu verstehen, was dir wichtig ist.

## Integration mit Agents

Memory wird automatisch in Agenten-System-Prompts injiziert:

```
# Memory

## About the user
- User is 35 years old
- Children: Leo (8), Emma (5)

## Working preferences
- Prefers short answers

## Current context
- Working on Project Alpha
```

Agents nutzen das natürlich — sie kündigen nicht "Ich erinnere mich, dass..." an, sondern wissen es einfach.

## Korrektur

Wenn outheis falsche Informationen hat:

1. **Explizite Korrektur:** `! I'm 36, not 35`
2. **CLI-Bearbeitung:** `outheis memory --clear user`, dann neu hinzufügen
3. **Direkte Dateibearbeitung:** JSON in `~/.outheis/human/memory/` modifizieren

Explizite (`!`)-Einträge haben Vorrang — agents überschreiben sie nicht mit Extraktionen niedrigerer Konfidenz.

---

## Rules

Rules sind die stabile Destillation von Memory — Verhaltensprinzipien, die bestimmen, wie outheis mit dir arbeitet.

### Zwei Schichten

| | System Rules | User Rules |
|---|--------------|------------|
| **Quelle** | Entwickler | Entstanden aus Interaktion |
| **Zweck** | Grenzen, Fähigkeiten | Stil, Präferenzen |
| **Ort** | `src/outheis/agents/rules/` | `~/.outheis/human/rules/` |
| **Veränderlichkeit** | Ändert sich mit Code-Updates | Wächst mit der Zeit |

**System Rules** definieren, was ein agent *kann* — architektonische Beschränkungen.

**User Rules** definieren, wie ein agent es *tun soll* — dein Arbeitsstil.

### Wie User Rules entstehen

User Rules schreibst du nicht direkt. Sie entstehen aus Memory durch den Pattern-Agenten.

rumi überprüft Memory bei seinem nächtlichen Lauf und sucht nach Mustern, die stabil genug geworden sind, um als Rules kodifiziert zu werden. Das ist kein mechanischer Prozess mit festen Schwellenwerten — der agent verwendet Urteilsvermögen:

- Eine einmal klar geäußerte starke Präferenz könnte eine Rule werden
- Etwas oft beiläufig Erwähntes vielleicht nicht
- Explizite Korrekturen zählen immer mehr als Inferenzen

Wenn rumi ein stabiles Muster identifiziert, schreibt er es in `~/.outheis/human/rules/{agent}.md`:

```markdown
# User Rules for Relay Agent

- User prefers concise responses  <!-- 2026-03-30 -->
- Respond in German unless the user writes in English  <!-- 2026-03-28 -->
```

### Memory vs. Rules

| | Memory | Rules |
|---|--------|-------|
| **Zeitskala** | Tage bis Wochen | Monate bis Jahre |
| **Flüchtigkeit** | Kann ablaufen, häufig aktualisiert | Stabil einmal etabliert |
| **Inhalt** | Fakten, Beobachtungen | Prinzipien, Muster |
| **Beispiel** | "User is 35 years old" | "User prefers brevity" |

Memory ist *was wir wissen*. Rules sind *wie wir arbeiten*.

### Speicherung

```
~/.outheis/human/rules/
├── common.md      # Applies to all agents
├── relay.md       # Conversation style
├── data.md        # Search behavior
├── agenda.md      # Scheduling preferences
└── pattern.md     # Extraction behavior
```

### CLI

```bash
# View all rules
outheis rules

# View rules for specific agent
outheis rules relay

# View only user rules (emergent)
outheis rules --user

# View only system rules (architectural)
outheis rules --system
```

### Kohärente Persönlichkeit

outheis besteht aus fünf agents — du erlebst einen Assistenten. Rules bewahren diese Kohärenz:

- **Common rules** sichern konsistentes Verhalten über alle agents
- **Agenten-spezifische Rules** ermöglichen angemessene Spezialisierung
- **User Rules** passen das gesamte System an deinen Arbeitsstil an

Mit der Zeit entwickelt outheis eine stabile Persönlichkeit — nicht programmiert, sondern gewachsen aus dem gemeinsamen Arbeiten.
